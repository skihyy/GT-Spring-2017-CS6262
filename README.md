# Headless Browser Simulate / Redirect Browser   

This crawler will crawl all pages including redirect pages. For example, `r1.html` redirects to `r2.html` then to `r3.html`. The crawler will crawl `r1.html`, `r2.html`, and `r3.html` with `[HTTP:200]` and ignores `[HTTP:300]` status code. Instead, it will retrieve redirect links in the HTML pages or JS files to maunally redirect.

***

## 1 Crawlers
### 1.1 HTML Redirect Crawler
- This is a test version.
- HTML redirect is based on meta element `meta[@http-equiv="refresh" and @content]/@content`.
- Need to make it robust.  

### 1.2 JS Redirect Crawler
- JS has too many possible ways to do redirects. It can be scripts embeded in HTML page, or in a single JS files.
- Currently, the crawler will try to look for `window.location.href` first. If not existed, then all JS files will be parsed and if `//script[@type="text/javascript" and @src]/@src` exist, redirects will be marked as true.
- Need to make it suitable for as many as redirect ways possible.

### 1.3 Headless Browser Simulator Crawler
- For some pages, if directly crawl all HTML elements, then some parts may be ingored since JS will render those part.
- Instead of using default `Selector` in the `Scrapy`, `selenium` and `PhantomJS` is used inside `Scrapy` to crawl pages rendered by JS.
- May use `CasperJS` in the future. But currently, `selenium` only supports `PhantomJS`.

## 2 Todo
- Merge 3 cralwers.
- Make it robust.
- Make it suitable for all situations.
- Make it efficient (low priority).
