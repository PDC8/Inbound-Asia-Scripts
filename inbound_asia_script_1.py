import requests
import csv
from bs4 import BeautifulSoup
import re




page = 1

#open a csv file that puts the follow colname as the column headers
with open('output.csv', mode='w') as csvfile:
    colname = ["公司", "營業項目", "營業住址", "公司電話", "電子信箱", "網址"]
    writer = csv.DictWriter(csvfile, fieldnames=colname)
    writer.writeheader()
    csvfile.close
    

# we find a pattern that the URL is the same for each page except for the fact that the last page number changes
# so we can utilize that to get all 9 pages of the website    
while page < 10:
    URL = "https://www.kcmica.org/Member?page=" + str(page)
    # getting response object
    res = requests.get(URL)

    # Initialize the object with the document
    soup = BeautifulSoup(res.content, "html.parser")

    contact_info = soup.find_all(class_="col-sm-6 info-blocks")

    # if we just retreive the text through .find and .text there are a bunch of whitespaces
    # and the built in .strip method doesn't work and it would give us the column headers
    # the work around is the index method. You index the header and find the substring in between to just get the text you want
    for info in contact_info:
        title = info.find(class_="title_h3").text
        texts = info.find_all('p')
        for words in texts:
            x = words.text
            index1 = x.index("營業項目")
            index2 = x.index("營業住址")
            index3 = x.index("公司電話")
            index4 = x.index("電子信箱")
            try:
                index5 = x.index("網址") #not all information have a blank for 網址 so we have to do a try except error
            except ValueError:
                index5 = -1
            
            #using re.sub we can remove the whitespaces that we couldn't with .strip
            if index1 != -1:
                col1 = re.sub("(?m)^\s+", "", x[index1+5:index2])
            if index2 != -1:
                col2 = re.sub("(?m)^\s+", "", x[index2+5:index3])
            if index3 != -1:
                col3 = re.sub("(?m)^\s+", "", x[index3+5:index4])
            if index4 != -1:
                col4 = re.sub("(?m)^\s+", "", x[index4+5:index5])
            if index5 != -1:
                col5 = re.sub("(?m)^\s+", "", x[index5+3:])
            else:
                col5 = ""

            #we add it to a new row in the csv file 
            list = [title , col1 , col2 , col3 , col4 , col5]
            with open('output.csv', mode='a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(list)
            csvfile.close
    page += 1


#Summary: Use a while loop to go through all 9 pages of the website
# use find_all to list out all the text on the page 
# use the built-in in function to index the heading so that when you substring you are only left with the information you want
# use re.sub to trim whitespaces
# add the information to csv