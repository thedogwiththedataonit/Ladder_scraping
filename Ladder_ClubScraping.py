
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import math
import os

import os.path
from os import path

#url = "https://illinois.campuslabs.com/engage/organizations"

#name = ""                          #Use for automation name find, not full school name though
#for letter in ind_url[8:-1]:
#   name += letter
#   if letter == ".":
#       school_name = name[:-1]
#       break


school_clubs = [["UIUC", "https://illinois.campuslabs.com/engage/organizations"],
                ["University of Washington-Seattle", "https://washington.campuslabs.com/engage/organizations"],
                ["UC Berkeley", "https://callink.berkeley.edu/organizations"],
                ["Missouri S&T", "https://mst.campuslabs.com/engage/organizations"],
                ["UT Austin", "https://utexas.campuslabs.com/engage/organizations"],
                ] 


"============================================================================================="
def getButton(browser):
    browser.execute_script("document.getElementsByTagName('button')[0].click()")

"============================================================================================="

def scrollDown(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

"============================================================================================="

def createCSV(driver, url_list, school_name, ind_url):
    global writeFiles
    global writeFile

    arr = ['School', 'Number', 'Organization Name', 'Email', 'Phone Number', 'Fax Number'] #  The Labels for each of the columns for the csv file
    index = 1  # index variable used to number each organization when being put in csv file

    #if os.path.exists("./School_Clubs.csv"):     #removes existing file
    #    os.remove("./School_Clubs.csv")

    with open("./School_Clubs.csv", 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(arr)

    writeFile.close()

    for i in url_list:
        time.sleep(1)
        #  goes to specific website url
        driver.get(ind_url + i.rsplit('/', 1)[1])
        #  creates soup of html
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        arr = []

        info = soup.find_all('span', {'class': 'sr-only'})
        length = len(info)
        arr.append(school_name)
        arr.append(index)
        arr.append(soup.find('h1').text.strip())

        
        if length != 0:
            for k in range(length):
                try:
                    arr.append(info[k].find_parent('div').find_next_sibling('div').text.rsplit(":", 1)[1].strip())
                except:
                    pass

        print(arr)
        with open("./School_Clubs.csv", 'a') as writeFiles:
            writer = csv.writer(writeFiles)
            writer.writerow(arr)

        index += 1

    writeFiles.close()

"============================================================================================="

def updateCSV(driver, url_list, school_name, ind_url):
    global writeFiles
    global writeFile

     #  The Labels for each of the columns for the csv file
    index = 1  # index variable used to number each organization when being put in csv file


    for i in url_list:
        time.sleep(1)
        #  goes to specific website url
        driver.get(ind_url + i.rsplit('/', 1)[1])
        #  creates soup of html
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        arr = []

        info = soup.find_all('span', {'class': 'sr-only'})
        length = len(info)
        arr.append(school_name)
        arr.append(index)
        arr.append(soup.find('h1').text.strip())

        
        if length != 0:
            for k in range(length):
                try:
                    arr.append(info[k].find_parent('div').find_next_sibling('div').text.rsplit(":", 1)[1].strip())
                except:
                    pass

        print(arr)
        with open("./School_Clubs.csv", 'a') as writeFiles:
            writer = csv.writer(writeFiles)
            writer.writerow(arr)

        index += 1

    writeFiles.close()
    return

"============================================================================================="

def parse(school_name, url, ind_url):
    try:
        print("Running...")
        driver = webdriver.Chrome(executable_path=r"C:\Users\Thomas Park\Documents\chromedriver_win32\chromedriver")
        child_list = []
        driver.get(url)
        time.sleep(2)

        clubs = math.ceil((int(driver.find_element_by_xpath("//div[@id='org-search-results']/following-sibling::div").find_element_by_xpath(".//*").text.rsplit(None, 1)[1][:-1]) - 10)/10)
        clubs += 5

        while clubs != 0:
            time.sleep(0.5)
            scrollDown(driver)
            try:
                getButton(driver)
            except:
                break

            clubs -= 1

        for child in BeautifulSoup(driver.page_source, "html.parser").find('div', {'id': 'org-search-results'}).find_all('a'):
            child_list.append(child['href'])

        #  creates CSV file
        exists = path.exists("School_Clubs.csv")
        if exists == True:
            updateCSV(driver, child_list, school_name, ind_url)
        else:   
            createCSV(driver, child_list, school_name, ind_url)

        print("Finished!")
    except:
        pass
        print("Error Occurred while running. Program Stopped.")

"============================================================================================="

def driver(school_clubs):
    for school in school_clubs:
        school_name = school[0]
        url = school[1]
        ind_url = school[1][:-1] + "/"

        parse(school_name, url, ind_url)

    return "Completed.."

"============================================================================================="


print(driver(school_clubs))
