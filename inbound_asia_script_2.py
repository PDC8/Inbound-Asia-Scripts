import requests
import csv
from bs4 import BeautifulSoup
import re




page = 1

#this opens as csv fiel called output.csv and puts the following text as the column headings
with open('output.csv', mode='w') as csvfile: 
    colname = ["會員編號", "統一編號", "負責人", "公司名稱", "公司地址", "公司電話", "公司傳真", "E-Mail", "網址", "工廠地址", "工廠電話", "工廠傳真", "主要營業項目", "產品許可證"]
    writer = csv.DictWriter(csvfile, fieldnames=colname)
    writer.writeheader()
    csvfile.close
    
#looking at the website you find a pattern. It's the following URL plus whatever page number you are at
#seeing this you can iterate via a while loop until the last page which is page 22

while page < 22: 
    URL = "https://www.tmbia.org.tw/member.php?&page=" + str(page)
    # getting response object
    res = requests.get(URL)

    # Initialize the object with the document
    soup = BeautifulSoup(res.content, "html.parser")

    company_list = soup.find_all(class_='member_List')[1:] #finds the list of all the content

    #We see that from the list of content each of them has a URL that directs to more detailed information about the content
    #Looking throught the detailed websites we find a pattern taht it's just tmbia.org followed by the href given from the content list
    for company in company_list:
        URL_detailed = "https://www.tmbia.org.tw/" + company.find('a')['href']
        res_detailed = requests.get(URL_detailed)
        soup_detailed = BeautifulSoup(res_detailed.content, "html.parser")
        contact_info = soup_detailed.find_all(class_="member_Table_List")
        title = soup_detailed.find(class_="member_Title").text
        list = []

        #Since the detailed content is in table format we can just get all the <Td> values put it into a list and then put that list into the csv file as a new row
        for contact in contact_info:
            list.append(contact.find(class_="member_Table_Td").text)

        with open('output.csv', mode='a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list)
        csvfile.close
    page += 1   


#Summary: There is a webpage with 21 pages you want to loop through that but within each page
# There are about 10 clickable links that redirect you to a more detailed webpage about them so
# you have to loop through those 10 links and get the table information from them and add them to 
# a new CSV file row