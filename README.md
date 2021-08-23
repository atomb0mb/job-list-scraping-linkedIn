# HarvestOrb: Job-list-scraping-linkedIn

## Getting Started

### [Python](https://wiki.python.org/moin/BeginnersGuide/Download)

### [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### [Selenium Webdriver](https://www.selenium.dev/documentation/getting_started/)

## Notes
Remember to set up your email and password of linkedIn account.

Job title, location, and filter option for job type can be customize to your preferrence.

Utilize Google Devtools to view web elements and obtain [FULL Xpath](https://www.guru99.com/xpath-selenium.html#:~:text=XPath%20in%20Selenium%20is%20an,page%20using%20XML%20path%20expression.) to add your preferrenced filter option.


## Steps overview
This is the process of Selenium and BeautifulSoup extract the jobs from the job site.

Step 6, 8, 9, 10, 12 can be skipped because it is optional to filter or narrow down to get preferred jobs type.

1. Visit LinkedIn page
2. Click 'Sign In' button
3. Enter account credentials
4. Click 'Log or Sign In' button
5. Click 'Jobs' tab
6. Enter title and location in the text fields (This can be skipped)
7. Click 'Search' button
8. Click 'All filters' button (This can be skipped)
9. Check any or all preferred boxes (This can be skipped)
10. Click 'show results' (This can be skipped)
11. Click job post that shows on the left panel
11a. At the same time, the right panel will show more info about the company, job type, description, and requirement
11b. Repeat 11 and 11a. to until the end of job list
12. Click 'Reset' button (This can be skipped)
13. Click 'Sign Out'
