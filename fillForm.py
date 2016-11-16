# getting the  data fom excel
import openpyxl
wb = openpyxl.load_workbook('C:\Work\workspace\GISP\url.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')
a = sheet['A2']
url = "http://" + a.value
print(url)


#Contacts page
import requests
from bs4 import BeautifulSoup

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
links = soup.find_all('a')
for link in links:
    #print(link.get('href'))
    if "Contact" in link.text:
         if "http" in link.get('href'):
            url_contact = link
         else:
            #print("<a href='%s'> %s </a>" %(link.get('href'), link.text ))
            url_contact = url + '/' + link.get('href')
print(url_contact)






import mechanize
br2 = mechanize.Browser()
br2.open(url_contact)
for g in br2.forms():
    print g




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.PhantomJS()
#driver.set_window_size(1120, 550)
driver.get(url_contact)

def check_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

f= open('C:/Work/workspace/GISP/firstname.txt', "r")

for line in f:
    cn =line.strip()
    print cn
    #cName = driver.find_element_by_id(cn)
    isExist = check_exists_by_id(cn)
    if isExist :
        cName = driver.find_element_by_id(cn)
        cName.send_keys("Shekhar")
        break



#cn = 'CustomerName'
#driver.find_element_by_id(cn).send_keys("Selenium")
driver.find_element_by_id("EmailAddress").send_keys("selenium@gmail.com")
driver.find_element_by_id("PhoneNumber").send_keys("7760566333")
driver.find_element_by_id("btnSend").click()

driver.quit()



