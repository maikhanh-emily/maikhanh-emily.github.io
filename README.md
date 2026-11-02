# Mai Khanh Do · portfolio

Personal site: projects, experience and writing, in English and Vietnamese. Plain HTML built by a small Python script and published with GitHub Pages. No framework, no Node.

## Hướng dẫn nhanh (tiếng Việt)

**Xem thử trên máy**

```bash
python build.py --serve --drafts
```

rồi mở <http://127.0.0.1:8765>. Bỏ `--drafts` nếu không muốn thấy bài nháp.

**Viết bài mới.** Tạo một file trong `content/en/posts/` (tiếng Anh) hoặc `content/vi/posts/` (tiếng Việt), tên file bắt đầu bằng ngày:

```
content/vi/posts/2026-12-15-ten-bai.md
```

với phần đầu file:

```markdown
---
title: Tên bài
date: 2026-12-15
tags: [Chủ đề, Chủ đề khác]
summary: Một câu tóm tắt, hiện trong danh sách bài.
---
Nội dung viết bằng Markdown. Có thể dùng **đậm**, *nghiêng*, danh sách, link, ảnh.
```

Thêm `draft: true` nếu chưa muốn đăng (bài sẽ không được build khi push). Nếu bài kể chuyện đã xảy ra từ trước, thêm `happened: 9/2023`: mục Bài viết sẽ xếp theo năm đó, còn `date` vẫn là ngày viết và hiện trong bài. Thêm `project: ten-du-an` để bài tự liên kết tới trang dự án.

**Thêm dự án.** Tạo `content/en/projects/ten-du-an.md` và, nếu muốn, `content/vi/projects/ten-du-an.md` cùng tên file. Thiếu bản tiếng Việt thì site tự hiện bản tiếng Anh kèm một dòng báo. Các trường ở đầu file: `title`, `subtitle`, `period`, `year`, `role`, `org`, `tags`, `featured` (true thì lên trang chủ), `order` (thứ tự), `status`, `summary`, `art_caption` (chú thích dưới hình minh họa).

**Minh họa cho dự án.** Thêm một file `content/illustrations/ten-du-an.svg`, cùng tên với file dự án, dùng chung cho cả hai ngôn ngữ. Hình sẽ tự hiện trên thẻ dự án và ở đầu trang dự án. Không có file SVG thì thẻ chỉ hiện chữ. Bài viết cũng dùng được: đặt tên SVG trùng phần tên bài (không có ngày), hình sẽ hiện ở đầu bài. Hai bản ngôn ngữ của một bài nên trùng tên file để nút đổi ngôn ngữ dẫn thẳng sang bản kia. Màu trong SVG dùng các biến `--a-*` trong `static/style.css`, nên tự đổi theo chế độ sáng/tối.

**Sửa danh thiếp, kinh nghiệm, học vấn, kỹ năng.** Mỗi ngôn ngữ có một thư mục `content/<lang>/` với `strings.yml` (chữ trên giao diện và phần danh thiếp), `experience.yml`, `education.yml`, `recognition.yml`, `skills.yml`, `about.md`, `now.md`.

**Link LinkedIn, GitHub, file CV, địa chỉ site.** Sửa `site.yml`. Nút nào để trống sẽ tự ẩn.

**Đổi ảnh.** Thay `static/portrait.jpg` (ảnh vuông, 900×900 là đủ) và `static/og-image.jpg` (1200×630, hiện khi chia sẻ link).

**Đăng lên web.** Sau khi sửa:

```bash
git add -A
git commit -m "Thêm bài mới"
git push
```

GitHub Actions tự build và đăng trong khoảng một phút. Xem tiến trình ở tab *Actions* của repo.

## Setting up GitHub Pages (once)

1. Create a public repository named `<your-username>.github.io`.
2. Push this folder to it, branch `main`.
3. In the repository: *Settings → Pages → Build and deployment → Source: GitHub Actions*.
4. Wait for the *Build and deploy to GitHub Pages* workflow to finish, then open `https://<your-username>.github.io`.
5. Put that address in `site.yml` under `url`, commit and push again. It feeds the RSS feed, link previews and the vCard.

If you'd rather keep the repository under another name (say `portfolio`), the site lives at `https://<your-username>.github.io/portfolio/`. Links are relative, so nothing else changes.

## How it's built

```
site.yml                shared settings: name, links, portrait, languages
content/<lang>/         everything a reader sees, one folder per language
  strings.yml           interface text, hero and card
  about.md, now.md      the About section and the Now page
  experience.yml        timeline on the front page
  education.yml         degrees
  recognition.yml       awards and recognition
  skills.yml            skill chips
  projects/*.md         one file per project, same filename across languages
  posts/YYYY-MM-DD-*.md blog posts
content/illustrations/  one SVG per project, same filename as the project, shared across languages
templates/              Jinja2 templates (base, index, projects, project, blog, post, page, tag, 404)
static/                 style.css, main.js, favicon.svg, portrait.jpg, og-image.jpg
build.py                the whole build: Markdown + YAML → dist/
.github/workflows/      builds dist/ and deploys it to GitHub Pages on every push to main
```

`python build.py` writes the site to `dist/`. The default language sits at the root and every other language under `/<lang>/`, each with its own `feed.xml`. A `contact.vcf` at the root is the downloadable contact card. Links are written root-relative so the output works at any base path.

Requirements: Python 3.10+, `pip install -r requirements.txt` (markdown, Jinja2, PyYAML).

## Content rules worth keeping

- Nothing from Planck's pipeline, customers, investors or funding status goes on the site. Architecture, approach and round-number scale are fine.
- No phone number, address, student numbers or email address. LinkedIn is the only contact route, because anything printed on a public page gets harvested for spam and scams.
- Vietnamese voice: "tôi" on the front page, projects, experience and the Now page, which recruiters read; "mình" only in posts. Write it as natural Vietnamese, never word by word from the English.
- Illustrations are schematic. No real pipeline data, and nothing that suggests a result a project hasn't reached.
- Posts marked `draft: true` never reach the public build. Only `python build.py --drafts` on your own machine shows them.
