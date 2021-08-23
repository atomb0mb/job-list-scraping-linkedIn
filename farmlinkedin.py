
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from traceback import format_exc
import pandas as pd
import time
from datetime import date
from config import linkedIn

# Today's date
today = date.today()


from bs4 import BeautifulSoup

# LinkedIn account and credential
emailKey = linkedIn['user']
passKey = linkedIn['passwd']

# Information to process - Modify if necessary
titleKey = "Software Developer"
locationKey = "New York, United States"


options = webdriver.ChromeOptions()
# Fix headless issue
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# Comment out if want to visualize
options.add_argument('--headless') 

driver = webdriver.Chrome(options=options)

# Navigate to url and get current page source for b4soup
driver.get("https://www.linkedin.com/")

driver.implicitly_wait(3) # seconds

def login():
    # Click on button sign in
    driver.find_element(By.CLASS_NAME, 'nav__button-secondary').click()

    # Find username and password fields
    usrname = driver.find_element(By.ID, "username")
    pw = driver.find_element(By.ID, "password")

    # Enter username and password into fields
    usrname.send_keys(emailKey)
    pw.send_keys(passKey)

    # Now click on button since there is only a button in this page
    driver.find_element(By.TAG_NAME, 'button').click()

    print('Entered credential and login.\n')


def clickJobIcon():
    # Wait for page to load then find job icon
    try:
        jobIcon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/header/div/nav/ul/li[3]/a'))
        )
    except:
        print ("Exception happened:\n%s" % (format_exc()))
        driver.quit()
    finally:
        time.sleep(2)
        jobIcon.click()
        print('Navigated to job section.\n')


def fieldsForLocationTitle(): 
    # Fill in the fields: title and location then search
    try:
        titleField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]'))
        )
    except:
        print ("Exception happened:\n%s" % (format_exc()))
        driver.quit()

    finally:
        time.sleep(1)
        titleField.send_keys(titleKey)
        locationField = driver.find_element(By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div[2]/input[1]')
        locationField.send_keys(locationKey)

        # Click search button    
        driver.find_element(By.XPATH, '//*[@id="global-nav-search"]/div/div[2]/button[1]').click()
        print('Enter job title and location in textfields..\n')
        time.sleep(1)
        print('Job title: ', titleKey)
        print('Location : ', locationKey)
        time.sleep(1)
        print('\nSearch Job by preferred job title and location...\n')


def filterCheckList():

    try:
        filterButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[3]/section/div/div/div/div/div/button'))
        )
    except:
        print ("Exception happened:\n%s" % (format_exc()))
        driver.quit()
    finally:
        filterButton.click()
        print('Navigated to filter tab..\n')

    time.sleep(1)

    # Need to configurate if we need diff options
    # This doesn't include all check boxes from filter list - implement as needed
    try:
        # internCheckBox = WebDriverWait(driver, 10).until(
        #     # Internship
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/ul/li[3]/fieldset/div/ul/li[1]/label'))
        # )
        entryLevelCheckBox = WebDriverWait(driver, 5).until(
            # Entry Level
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/ul/li[3]/fieldset/div/ul/li[2]/label'))
        )
        fullTimeCheckBox = WebDriverWait(driver, 3).until(
            # Full time
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/ul/li[5]/fieldset/div/ul/li[1]/label'))
        )
        # remoteCheckBox = WebDriverWait(driver, 2).until(
        #     # Remote - On - Is off by default
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/ul/li[6]/fieldset/div/div/span'))
        # )
        # DO NOT DO THIS
        # You will get Stale Element Exception when the properties of the element which you are trying to perform an operation on has changed.
        # Because when all the checkbox is clicked, the searchBox property will be changed due to LinkedIn search design
        # searchButton = WebDriverWait(driver, 5).until(
        #     # Search
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/button[2]'))
        # )
    except:
        print ("Exception happened:\n%s" % (format_exc()))
        driver.quit()
    finally:
        # internCheckBox.click()
        #print("Checked 'Intern'")
        time.sleep( 1 )
        entryLevelCheckBox.click()
        print("Checked 'Entry level'")
        time.sleep( 1 )
        fullTimeCheckBox.click()
        print("Checked 'Full time'")
        time.sleep( 1 )
        # remoteCheckBox.click()
        #print('Remote Box Checked.')
        # time.sleep( 1 )

    time.sleep(2)
    # Click search
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/button[2]').click()
    print('\nFiltered job type.\n')


# ------------------------------------------  End of Filter Tab -------------------------------------------------

login()

time.sleep(2)

clickJobIcon()
 
fieldsForLocationTitle()

filterCheckList()

companyList = []
locationList = []
positionList = []
postDateList = []
jobIdList = []
typesList = []
linkList = []

time.sleep(2)

count = 1
print('Jobs found!')

# Loop through 25 jobs in this page
for x in range(25):

    time.sleep(3)
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li['+ str(count) +']/div/div'))
        )
    except:
        print ("Exception happened:\n%s" % (format_exc()))
        driver.quit()
    finally:
        time.sleep( 1 )
        ## Click current job post to show right panel 
        driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li['+ str(count) +']/div/div').click()

        currentUrl = driver.current_url
        linkList.append(str(currentUrl))
        time.sleep( 1 )
        

    time.sleep( 1 )

    # Start scraping right panel data
    soup = BeautifulSoup(driver.page_source, 'lxml')
    section = soup.find(class_='jobs-search__right-rail')
    company = section.find(class_='ember-view t-black t-normal')
    position = section.h2.string
    loc = section.find(class_='jobs-unified-top-card__bullet')
    postDate = section.find(class_='jobs-unified-top-card__posted-date')

    companyList.append(company.text.replace('\n', ''))
    positionList.append(position.replace('\n', ''))
    postDateList.append(postDate.text.replace('\n', ''))
    locationList.append(loc.text.replace('\n', ''))
    # I just want to extract first 2
    list = section.find_all(class_='jobs-unified-top-card__job-insight', limit=2)
    
    newString = ''
    for span in list:
        if newString != '':
            newString = newString + ' ' + span.span.text.replace('\n', '')
        else:    
            newString = newString + span.span.text.replace('\n', '')

    typesList.append(newString)
    print('Job post {:<2}'.format(count) + company.text.replace('\n', ''))
    count = count + 1

# B4 mining for job id
soup = BeautifulSoup(driver.page_source, 'lxml')

job_root = soup.find('ul', class_="jobs-search-results__list list-style-none")

jobs = job_root.find_all('li', class_='jobs-search-results__list-item occludable-update p0 relative ember-view')

for id in jobs:
    tempId = str(id.find(class_='job-card-container')['data-job-id'])
    jobIdList.append(tempId)

# We will add jobid later after html file is created
jobList = pd.DataFrame({
    "Job id": '',
    "Company": companyList,
    "Position": positionList,
    "Location": locationList,
    "Types": typesList,
    "Posted": postDateList
})
# Naming the html file by date
d = str(today.strftime("%m/%d/%Y").replace('/', ''))
d = d + '_joblist.html'
jobList.to_html(d)


# Opening and reading the html file
file = open(d, "r")
contents = file.read()

# Modify html file
soupy = BeautifulSoup(contents, 'lxml')
tr = soupy.tbody.find_all('tr')
i = 0
for j_id in jobIdList:
    new_tag = soupy.new_tag("a", href=linkList[i])
    new_tag.string = j_id
    tr[i].td.append(new_tag)
    i = i + 1

saveChanges = soupy.prettify()
# write to the file
with open(d, 'w') as file:
    file.write(saveChanges)

#Close file
file.close()

print('\nJob list saved in HTML: ' + str(d))

time.sleep(3)

# Reset filter
try:
    resetButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[3]/section/div/div/div/div/button'))
    )
except:
    print ("Exception happened:\n%s" % (format_exc()))
    driver.quit()
finally:
    resetButton.click()
    print('Reset job filter')

time.sleep(3)
# This might be LinkedIn's security measurement. 
# Selenium is unable to crawl into user's account section for the sign out button.
# Since we can't do sign out, I came with another solution.
# By navigating to this route, it allows user to log out.
driver.get("https://www.linkedin.com/m/logout")
print('Sign out')

time.sleep(2)

driver.quit()