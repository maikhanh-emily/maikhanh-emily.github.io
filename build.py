#!/usr/bin/env python3
"""Build the portfolio site into dist/.

    python build.py              build
    python build.py --drafts     build, including posts marked `draft: true`
    python build.py --serve      build, then serve dist/ at http://127.0.0.1:8765
    python build.py --serve 8000 same, on another port

Content lives in content/<lang>/ (one folder per language), templates in
templates/, static files in static/. The default language is served at the
site root and every other language under /<lang>/. A project or page that has
no translation falls back to the default language with a small notice.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
import time
import unicodedata
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
DIST = ROOT / "dist"

FRONT_MATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.S)
POST_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
ABS_LINK = re.compile(r'((?:href|src|content)=")/(?!/)')
MONTHS_EN = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
DATA_FILES = ("experience", "education", "recognition", "skills")
PAGES = ("about", "now")


# ---------- helpers ----------

def load_yaml(path: Path, default=None):
    if not path.exists():
        return default
    return yaml.safe_load(path.read_text(encoding="utf-8")) or default


def parse_markdown_file(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    meta = (yaml.safe_load(m.group(1)) or {}) if m else {}
    body = text[m.end():] if m else text
    return meta, body


def render_markdown(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "attr_list", "toc"],
        output_format="html5",
    )


def slugify(value) -> str:
    s = unicodedata.normalize("NFKD", str(value)).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "item"


def as_date(value) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value)[:10])


def format_date(value, lang: str) -> str:
    d = as_date(value)
    if lang == "vi":
        return f"{d.day} tháng {d.month}, {d.year}"
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}"


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def project_sort_key(p):
    return (not p.get("featured"), p.get("order", 99), -int(p.get("year") or 0))


def clean_dir(path: Path) -> None:
    """Empty the output folder. Removes files first and retries, because a
    sync client (OneDrive) can hold a folder open for a moment after its
    files are deleted."""
    if not path.exists():
        path.mkdir(parents=True)
        return
    for child in list(path.rglob("*")):
        if child.is_file():
            try:
                child.unlink()
            except PermissionError:
                time.sleep(0.5)
                child.unlink()
    dirs = sorted((d for d in path.rglob("*") if d.is_dir()), key=lambda d: len(d.parts), reverse=True)
    for d in dirs:
        for attempt in range(6):
            try:
                d.rmdir()
                break
            except OSError:
                if attempt == 5:
                    break  # an empty folder the sync client still holds; harmless
                time.sleep(0.4 * (attempt + 1))


# ---------- loading ----------

def load_language(lang: str, include_drafts: bool) -> dict:
    base = CONTENT / lang
    data = {"lang": lang, "strings": load_yaml(base / "strings.yml", {})}
    for key in DATA_FILES:
        data[key] = load_yaml(base / f"{key}.yml", [])

    pages = {}
    for name in PAGES:
        path = base / f"{name}.md"
        if path.exists():
            meta, body = parse_markdown_file(path)
            pages[name] = {**meta, "slug": name, "html": render_markdown(body)}
    data["pages"] = pages

    projects = []
    for path in sorted((base / "projects").glob("*.md")):
        meta, body = parse_markdown_file(path)
        projects.append({**meta, "slug": path.stem, "html": render_markdown(body),
                         "tags": meta.get("tags") or [], "lang": lang})
    projects.sort(key=project_sort_key)
    data["projects"] = projects

    posts = []
    for path in sorted((base / "posts").glob("*.md")):
        meta, body = parse_markdown_file(path)
        if meta.get("draft") and not include_drafts:
            continue
        m = POST_NAME.match(path.stem)
        date = as_date(meta.get("date") or (m.group(1) if m else dt.date.today()))
        slug = meta.get("slug") or (m.group(2) if m else path.stem)
        posts.append({**meta, "slug": slug, "date": date, "html": render_markdown(body),
                      "tags": meta.get("tags") or [], "lang": lang,
                      "minutes": max(1, round(word_count(body) / 200))})
    posts.sort(key=lambda p: p["date"], reverse=True)
    data["posts"] = posts
    return data


def apply_fallbacks(data: dict, default: str):
    base = data[default]
    for lang, d in data.items():
        if lang == default:
            continue
        if not d["strings"]:
            d["strings"] = base["strings"]
        for key in DATA_FILES:
            if not d[key]:
                d[key] = base[key]
        have = {p["slug"] for p in d["projects"]}
        for p in base["projects"]:
            if p["slug"] not in have:
                d["projects"].append({**p, "fallback": True, "lang": lang})
        d["projects"].sort(key=project_sort_key)
        for name, page in base["pages"].items():
            d["pages"].setdefault(name, {**page, "fallback": True})


def collect_tags(d: dict) -> list:
    tags: dict[str, dict] = {}
    for p in d["projects"]:
        for t in p["tags"]:
            tags.setdefault(slugify(t), {"name": t, "slug": slugify(t), "projects": [], "posts": []})["projects"].append(p)
    for post in d["posts"]:
        for t in post["tags"]:
            tags.setdefault(slugify(t), {"name": t, "slug": slugify(t), "projects": [], "posts": []})["posts"].append(post)
    return sorted(tags.values(), key=lambda t: t["name"].lower())


# ---------- output ----------

def feed_xml(site: dict, d: dict, prefix: str) -> str:
    base_url = (site.get("url") or "").rstrip("/")
    name = site.get("name", "")
    items = []
    for post in d["posts"]:
        if post.get("draft"):
            continue
        link = f"{base_url}{prefix}blog/{post['slug']}/"
        pub = dt.datetime.combine(post["date"], dt.time(9, 0)).strftime("%a, %d %b %Y %H:%M:%S +0000")
        items.append(
            "<item>"
            f"<title>{escape(post['title'])}</title>"
            f"<link>{escape(link)}</link>"
            f"<guid>{escape(link)}</guid>"
            f"<pubDate>{pub}</pubDate>"
            f"<description>{escape(post.get('summary') or '')}</description>"
            "</item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0"><channel>'
        f"<title>{escape(name)}</title>"
        f"<link>{escape(base_url + prefix)}</link>"
        f"<description>{escape(d['strings'].get('meta_description', ''))}</description>"
        f"<language>{d['lang']}</language>"
        + "".join(items)
        + "</channel></rss>"
    )


def vcard(site: dict, strings: dict) -> str:
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{site.get('family_name', '')};{site.get('first_name', '')};;;",
        f"FN:{site.get('name', '')}",
    ]
    if site.get("nickname"):
        lines.append(f"NICKNAME:{site['nickname']}")
    title = (strings.get("hero") or {}).get("title")
    if title:
        lines.append("TITLE:" + title.replace(",", "\\,"))
    if site.get("email"):
        lines.append(f"EMAIL;TYPE=INTERNET,PREF:{site['email']}")
    if site.get("url"):
        lines.append(f"URL:{site['url']}")
    if site.get("linkedin"):
        lines.append(f"X-SOCIALPROFILE;TYPE=linkedin:{site['linkedin']}")
    location = (strings.get("hero") or {}).get("location")
    if location:
        lines.append("NOTE:" + location.replace(",", "\\,"))
    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


def build(include_drafts: bool = False) -> None:
    site = load_yaml(ROOT / "site.yml", {})
    default = site.get("default_lang", "en")
    langs = site.get("languages") or [default]
    data = {lang: load_language(lang, include_drafts) for lang in langs}
    apply_fallbacks(data, default)

    clean_dir(DIST)
    shutil.copytree(STATIC, DIST / "static", dirs_exist_ok=True)
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["slug"] = slugify
    year = dt.date.today().year

    def prefix_of(lang: str) -> str:
        return "/" if lang == default else f"/{lang}/"

    def alternates(kind: str, slug: str | None = None) -> list:
        out = []
        for lang in langs:
            d, prefix = data[lang], prefix_of(lang)
            if kind == "projects":
                url = prefix + "projects/"
            elif kind == "project":
                url = prefix + (f"projects/{slug}/" if any(p["slug"] == slug for p in d["projects"]) else "projects/")
            elif kind == "blog":
                url = prefix + "blog/"
            elif kind == "post":
                url = prefix + (f"blog/{slug}/" if any(p["slug"] == slug for p in d["posts"]) else "blog/")
            elif kind == "page":
                url = prefix + (f"{slug}/" if slug in d["pages"] else "")
            elif kind == "tag":
                url = prefix + (f"tags/{slug}/" if any(t["slug"] == slug for t in collect_tags(d)) else "")
            else:
                url = prefix
            out.append({"lang": lang, "url": url, "label": d["strings"].get("lang_name", lang)})
        return out

    def write(out_rel: str, template: str, lang: str, alts: list, **ctx) -> None:
        out = DIST / out_rel
        depth = len(Path(out_rel).parts) - 1
        root = "../" * depth if depth else "./"
        d = data[lang]
        other = next((a for a in alts if a["lang"] != lang), alts[0])
        context = {
            "site": site, "S": d["strings"], "L": prefix_of(lang), "lang": lang, "year": year,
            "alternates": alts, "alt_url": other["url"], "alt_lang": other["lang"],
            "canonical": "/" + out_rel.replace("index.html", ""),
            "fmt_date": lambda v: format_date(v, lang),
            **{k: d[k] for k in ("projects", "posts", "pages", *DATA_FILES)},
            **ctx,
        }
        html = env.get_template(template).render(**context)
        html = ABS_LINK.sub(lambda m: m.group(1) + root, html)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")

    pages_written = 0
    for lang in langs:
        d = data[lang]
        S = d["strings"]
        sub = prefix_of(lang).lstrip("/")
        name = site.get("name", "")
        desc = S.get("meta_description", "")
        tags = collect_tags(d)

        write(f"{sub}index.html", "index.html", lang, alternates("home"),
              section="home", page_title=name, page_description=desc)
        write(f"{sub}projects/index.html", "projects.html", lang, alternates("projects"),
              section="projects", tags=tags,
              page_title=f"{S['nav']['projects']} · {name}", page_description=S["labels"]["projects_intro"])
        for p in d["projects"]:
            related = [post for post in d["posts"] if post.get("project") == p["slug"]]
            write(f"{sub}projects/{p['slug']}/index.html", "project.html", lang, alternates("project", p["slug"]),
                  section="projects", p=p, related_posts=related, og_type="article",
                  page_title=f"{p['title']} · {name}", page_description=p.get("summary", ""))
        write(f"{sub}blog/index.html", "blog.html", lang, alternates("blog"),
              section="blog", page_title=f"{S['nav']['writing']} · {name}", page_description=S["labels"]["writing_intro"])
        for post in d["posts"]:
            related_project = next((p for p in d["projects"] if p["slug"] == post.get("project")), None)
            write(f"{sub}blog/{post['slug']}/index.html", "post.html", lang, alternates("post", post["slug"]),
                  section="blog", post=post, related_project=related_project, og_type="article",
                  page_title=f"{post['title']} · {name}", page_description=post.get("summary", ""))
        for slug, page in d["pages"].items():
            if slug == "about":
                continue  # rendered inside the front page
            write(f"{sub}{slug}/index.html", "page.html", lang, alternates("page", slug),
                  section=slug, page=page,
                  page_title=f"{page.get('title', slug)} · {name}", page_description=page.get("summary", ""))
        for tag in tags:
            write(f"{sub}tags/{tag['slug']}/index.html", "tag.html", lang, alternates("tag", tag["slug"]),
                  section="tags", tag=tag,
                  page_title=f"{tag['name']} · {name}", page_description=desc)
        (DIST / sub / "feed.xml").write_text(feed_xml(site, d, prefix_of(lang)), encoding="utf-8")
        pages_written += 4 + len(d["projects"]) + len(d["posts"]) + len(tags)

    write("404.html", "404.html", default, alternates("home"), section="404",
          page_title=f"404 · {site.get('name', '')}", page_description="")
    (DIST / "contact.vcf").write_text(vcard(site, data[default]["strings"]), encoding="utf-8")
    print(f"Built {pages_written} pages for {', '.join(langs)} into {DIST.relative_to(ROOT)}/"
          + (" (drafts included)" if include_drafts else ""))


def serve(port: int) -> None:
    handler = partial(SimpleHTTPRequestHandler, directory=str(DIST))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Serving at http://127.0.0.1:{port}/  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--drafts", action="store_true", help="include posts marked draft: true")
    parser.add_argument("--serve", nargs="?", const=8765, type=int, metavar="PORT", help="serve dist/ after building")
    args = parser.parse_args(argv)
    build(include_drafts=args.drafts)
    if args.serve:
        serve(args.serve)
    return 0


if __name__ == "__main__":
    sys.exit(main())
