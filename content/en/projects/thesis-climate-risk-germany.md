---
title: Climate risk in the German stock market
subtitle: "Master's thesis: a daily measure of climate-risk attention in German news, and what it does to equity returns"
period: 2026 – 2027
year: 2026
role: Co-author, with a classmate
org: BI Norwegian Business School
tags: [Research, Climate finance, R, Data]
featured: true
order: 2
status: In progress, submission April 2027
summary: Does climate-risk news move German stock returns? To find out we're building a daily index of climate-risk attention from ten years of German news. The data pipeline turned out to be most of the work.
---
## The question

Climate risk reaches equity prices through two channels. Physical risk is floods, heat and drought. Transition risk is carbon prices, regulation and technology. We want a daily measure of how much attention each gets in German news, and then test whether that attention explains returns and volatility across sectors of the German market.

## The data pipeline

- **Source.** GDELT, the open database of world news. In Google BigQuery we filtered about 1.1 million German-language records from 2015 to 2025 down to climate-related coverage.
- **Sample.** A stratified sample of about 70,000 URLs, balanced across time and outlets, so that a busy year doesn't drown a quiet one.
- **Scrape.** Full text for about 35,000 of them, in R. Links from 2015 to 2018 were often dead; a pass through the Wayback Machine recovered around 7,000 of 10,700 dead links.
- **Clean.** Boilerplate, navigation and page furniture stripped. What's left is a corpus of about 27,000 articles.
- **Model.** Structural topic models at 25 and 40 topics, fitted in parallel sessions, with topics labelled and mapped to physical and transition risk.

## What I've learned so far

Data work is mostly deciding what counts: which outlets, which years, which words. One link once held the scraper for eight hours, so there is now a canary check that gives up on a page that doesn't answer. News archives are not complete either. Some outlets have months with nothing, so article volume has to be measured on a fixed panel of outlets, not on everything that happens to be there.

Tools: R (data.table, quanteda, stm, furrr) and SQL on BigQuery.
