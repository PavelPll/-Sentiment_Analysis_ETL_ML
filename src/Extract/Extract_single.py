import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from time import sleep
import pandas as pd

# GET the interval of categories to extract
if len(sys.argv)!=3:
    print('We have to extract around 1000 cathegories')
    print('It will take several days')
    print('Please specify the interval by two integer arguments')
    print('in order to decrease the extraction time and avoid possible errors')
    print('<FOR EXAMPLE for the first 100 categories: python3 Extract.py 0 100>')
    print('The extraction results see in 0-100.csv')
    sys.exit(1)  # abort because of error

start = int(sys.argv[1])
end = int(sys.argv[2])
#print(start, end)

# SET the driver
chromedriver = "/usr/bin/chromedriver" # see Dockerfile for driver installation inside docker container c1
os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

# GET the list of Software categories and the list of the corresponding websites for extraction
driver.get("https://www.capterra.fr/directory")
list_logiciels = driver.find_elements(By.CLASS_NAME, "list-group-item list-group-item-action border-0 fw-bold".replace(' ',"."))
logiciels = []
webIs = []
for el in list_logiciels:
    webI = el.get_attribute("href")
    webIs.append(webI)
    #logiciels.append(el.text)
driver.close()
print("Nlogiciels: ", len(webIs))

# GET all pages for each website
webIIs = []
for webI in tqdm(webIs[start:end]):
    print(webI)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(webI)
    sleep(5)
    N5_1 = driver.find_elements(By.CLASS_NAME, "card product-card-new mb-3 border-seaglass pt-2".replace(' ',"."))
    sleep(2)
    for el in N5_1:
        try:   
            N5_2 = el.find_elements(By.CLASS_NAME, "col-sm-3".replace(' ',"."))
            sleep(2)
            Ncomments = int(str(N5_2[0].text).replace(u"\u202f", ""))
            if Ncomments>500:
                print(Ncomments)
                el_webI = el.find_elements(By.CLASS_NAME, "mos-star-rating d-inline-flex align-top flex-wrap column-gap-2 evnt fw-bold".replace(' ',"."))
                webIIs.append(el_webI[0].get_attribute("href") + '?countries[]=fr#facets')
                #webIIs.append(webI[0].get_attribute("href") )
        except:
           pass
    driver.close()
    #sleep(5)
print("----------------------------")
print(webIIs)

# START the extraction
records = []
ind = 0
categories_pattern = "i18n-translation_container pt-4 py-3 py-md-5 review-card"
#i18n-translation_container pt-4 py-3 py-md-5 review-card 
categories_pattern = categories_pattern.replace(' ',".")

#driver = webdriver.Chrome(options=chrome_options)
for webII in tqdm(webIIs):
    print("webII: ", webII)
    driver = webdriver.Chrome(options=chrome_options)
    sleep(1)
    # driver.get(webII + '?countries[]=fr#facets')
    driver.get(webII)
    sleep(1)
    categories_list = driver.find_elements(By.CLASS_NAME,categories_pattern)
    try:
        el_pages = driver.find_elements(By.CLASS_NAME, "page-link".replace(' ',"."))
        l = len(el_pages)
        Npages = int(el_pages[l-2].text)
    except:
        Npages = 1
    print("Npages: ", Npages)
    #driver.quit()
    sleep(1)
    
    for page in range(Npages):
        #htt = webII + '?page=' + str(page+1) + '?countries[]=fr#facets'
        #htt = str(webII) + '?countries[]=fr#facets' + '?page=' + str(page+1) 
        htt = webII + '?page=' + str(page+1) 
        #htt = 'https://www.capterra.fr/reviews/163335/gotowebinar?countries[]=fr#facets?countries[]=fr#facets?page=1'
        print(htt)
        driver = webdriver.Chrome(options=chrome_options)
        sleep(1)
        driver.get(htt)
        sleep(1)
        categories_list = driver.find_elements(By.CLASS_NAME,categories_pattern)
        print("categories_list: ", len(categories_list) )
    
        for el in categories_list:
        #el = categories_list[2]
        #if (1==1):
            try:
                record = {}
                ind = ind + 1
                
                el_comment = el.find_elements(By.CLASS_NAME, "col-lg-7".replace(' ',"."))
                el_review_score = el.find_elements(By.CLASS_NAME, "ms-1")

                el_name1 = el.find_elements(By.CLASS_NAME, "col-lg-5 mb-3 mb-lg-0".replace(' ',"."))
                el_name2 = el_name1[0].find_elements(By.CLASS_NAME, "h5 fw-bold mb-2".replace(' ',".")) 
                #el_comments2 = el_comments[0].find_elements(By.XPATH, "//*[@class='col-lg-7']/p/span")

                el_date1 = el_comment[0].find_elements(By.CLASS_NAME, "ms-2".replace(' ',"."))

                el_title1 = el_comment[0].find_elements(By.CLASS_NAME, "h5 fw-bold".replace(' ',"."))

                el_duration2 = el_name1[0].find_elements(By.CLASS_NAME, "col-12 col-md-6 col-lg-12 pt-3 pt-md-0 pt-lg-3 text-ash".replace(' ',"."))
                el_duration3 = el_duration2[0].find_elements(By.CLASS_NAME, "mb-2".replace(' ',"."))
                #print(el_duration3)
                duration = ""
                for d in el_duration3:
                    if "Temps d'utilisation du logiciel" in d.text:
                        duration = d.text
    
                review_score = el_review_score[0].text
                comment = el_comment[0].text.split("Commentaires : ")
                #print(comment)
                #print("title:", el_title1[0].text)
                
                if (len(comment)>1):
                    comment = comment[1].split("\n")[0]
                    name = el_name2[0].text
                    the_date = el_date1[0].text
                    title = el_title1[0].text
                    #print("===============")
        
                    record["comment"] = comment
                    record['date_experience'] = duration
                    record['review_score'] = review_score
                    record['timestamp'] = the_date
                    record['title'] = title
                    record['user_name'] = name

                    records.append(record)
                #driver.close()
                sleep(1)
            except:
                ind = ind - 1
                pass
        print("len: ", len(records))
        driver.close()
        sleep(5)

    # SAVE the extracted data to file
    filename = str(start)+"_"+str(end)+".csv"
    df = pd.DataFrame(records)
    # df.to_csv("../data_csv/"+filename, index=False)
    df.to_csv("../../data_csv/"+filename, index=False)
