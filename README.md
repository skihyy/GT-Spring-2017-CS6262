# Headless Browser Simulate / Redirect Browser   

This crawler inside `/browser_simulator` will crawl all pages including redirect pages. For example, `r1.html` redirects to `r2.html` then to `r3.html`. The crawler will crawl `r1.html`, `r2.html`, and `r3.html` with `[HTTP:200]` and ignores `[HTTP:300]` status code. Instead, it will retrieve redirect links in the HTML pages or JS files to maunally redirect.

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

### 1.4 All-in-one Crawler
- There are still some problems in it. Currently, the JS redirect cannot be simulated by Phantom JS. To be specific, I cannot stop redirecting in Phantom.
- For some pages, the CSV output is really wried. This will be solved in the future.
- **NOTE:** the page sources crawled is all rendered by PhantomJS. Scrapy Spider is only used for finding the redirect link in JS files.

## 2 Installation

### 2.1 Requirements
- `environment_readme.txt` is provided that `Python`, `Scrapy` in Python, `NodeJS`, and `PhantomJS` in NodeJS is needed for running the program.

### 2.2 To Start
- Tp start a spider, in the `/browser_simulator` directory, typing `scrapy crawl spider-name` to start.
- `scrapy-name` can be `all_in_one_spider`, `headless_spider`, `html_redirect_spider`, and `js_redirect_spider`.

## 3 Todo
- Fix PhantomJS failed to stop redirect function.
- Wirte a new middleware of saving data. Currently, CSV for big webpages will be shown in messy.
- Robust improvement.

# Good Software Download Crawler

The crawler inside `/browser_simulator` will try to cralw download links for good software (only `exe`) for CNET, and Firehourse. Only the most popular ones will be crawled.

## 1 Specifications

### 1.1 CNET

All links will be located at `http://download.cnet.com/s/software/windows-free/?sort=most-popular` section. The start page and end page can be customized.

### 1.2 Firehorse

All links will be located at `http://www.filehorse.com/popular/` section. The start page and end page can be customized.

### 1.3 Spider Types

A normal crawler, PhantomJS with Selenium crawler are provided based on the preferences.

## 2 Installation

This section is almost the same as `Headless Browser Simulate / Redirect Browser`. Please refer to the above section for details.

# Decision Trees for Malware Detection

## 1 Data

Data are all `csv` files or `xslx` files. But to be noted that only `csv` files can be used in ML.

## 2 Installation

### 2.1 Requirements

- `Python` 2.7.10
- `numpy` module in `Python` is needed for running. 

### 2.2 Running the decision tree

`
from RandomForest import MachineLearning

ml = MachineLearning() # will start to training the ree

ml.voting(data) # predicting a tuple of data, the data can be gathered from user
`

## 3 Some Configurations

- line #`27`, control depth of the tree.
- line #`77`, using binary split.
- line #`441`, control percentage of good data in each training set.

***
#### Updated by YH @ Apr 19, 2017.
