from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys, os
import ctypes
import pymysql.cursors
import wx
import random
from bs4 import BeautifulSoup
app = wx.App()
import re


def Local_connection_links():
    a = 0
    while a == 0:
        try:
            connection = pymysql.connect(host='192.168.0.202',
                                         user='ams',
                                         password='amsbind',
                                         db='CompanyInfoDB',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.connect  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def Collect_Link():
    mydb_Local = Local_connection_links()
    mycursorLocal = mydb_Local.cursor()
    a = 0
    while a == 0:
        try:

            mydb_Local = Local_connection_links()
            mycursorLocal = mydb_Local.cursor()
            Links_List = []
            mycursorLocal.execute("SELECT Company_Name FROM mcagovin_orgnames WHERE website_status = '' LIMIT 0,10000")
            # mycursorLocal.execute("SELECT Company_Name FROM mcagovin_orgnames WHERE Company_Name= 'ADVANCE AGRICULTURE & TECHNICAL INFORMATION PRIVATE LIMITED'")
            rows = mycursorLocal.fetchall()
            for row in rows:
                links = "%s" % (row["Company_Name"])
                if links not in Links_List:
                    Links_List.append(links)
            time.sleep(2)
            print("Number OF Link Get From Database: ", len(Links_List))
            Nav_Links(Links_List)
            a = 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            try:
                mydb_Local.close()
                mycursorLocal.close()
            except:pass
            a = 0
            time.sleep(10)


def Nav_Links(Links_List):
    Global_Link_Found = 0
    Global_Link_NOT_Found = 0
    Global_Link_inserted = 0
    Count = 0
    browser = webdriver.Chrome(executable_path=str('D:\\PycharmProjects\\Comapany_WEBSITE&MAIL\\chromedriver.exe'))
    browser.maximize_window()
    time.sleep(1)
    mydb_Local = Local_connection_links()
    mycursorLocal = mydb_Local.cursor()

    for Company_name in Links_List:
        a = 0
        while a == 0:
            try:
                Company_name = Company_name.replace("'", "''").replace('\\','')  # Most Important When inserting Company Name
                browser.get('https://www.google.com/')
                time.sleep(2)
                Count += 1
                for Search_text in browser.find_elements_by_xpath('//*[@class="gLFyf gsfi"]'):
                    Search_text.send_keys(str(Company_name))
                    Search_text.send_keys(Keys.ENTER)
                    # Sleep_Time = random.randint(10, 15)
                    time.sleep(5)
                    break
                a = 1
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                      exc_tb.tb_lineno)
                a = 0
                time.sleep(5)

        print('Website NO:  ' + str(Count),  Company_name)
        Find_Link = ''.strip()
        Find_address = ''
        Find_Contact = ''
        if Find_Link == "":
            try:
                variable = 0
                xpath = 0
                while variable == 0:
                    xpath += 1
                    if xpath != 10:
                        for get_website_outerHTML in browser.find_elements_by_xpath('//*[@class="rhscol col rhstc' + str(xpath) + '"]'):
                            get_website_outerHTML = get_website_outerHTML.get_attribute('outerHTML')
                            get_website_outerHTML = get_website_outerHTML.replace('\n','')
                            soup = BeautifulSoup(get_website_outerHTML)
                            for a_tag in soup.findAll('a'):
                                # print(a_tag)
                                if 'Website' in a_tag:
                                    # print(a_tag)
                                    Find_Link = a_tag.get('href')
                                    print(Find_Link)
                                    Find_address = get_website_outerHTML.partition("Address</a>: </span>")[2].partition("</span>")[0]
                                    clean_HTML_TAG = re.compile('<.*?>')
                                    Find_address = re.sub(clean_HTML_TAG, '', Find_address)
                                    Find_address = re.sub(' +', ' ', str(Find_address)).strip().replace(',,,',',').replace(',,', ',').replace("'", "''")  # remove Multiple Spaces From String
                                    print(Find_address)

                                    Find_Contact = get_website_outerHTML.partition("Phone</a>: </span>")[2].partition("</span>")[0]
                                    clean_HTML_TAG = re.compile('<.*?>')
                                    Find_Contact = re.sub(clean_HTML_TAG, '', Find_Contact)
                                    Find_Contact = re.sub(' +', ' ', str(Find_Contact)).strip()
                                    print(Find_Contact)
                                    Global_Link_Found += 1
                                    print('Web site Found : ', Global_Link_Found)
                            variable = 1
                    else:
                        variable = 1
            except:
                pass
        # ======================================================================================================
        mydb_Local = Local_connection_links()
        mycursorLocal = mydb_Local.cursor()
        if Find_Link != "":
            MyLoop = 0
            while MyLoop == 0:
                try:
                    mydb_Local = Local_connection_links()
                    mycursorLocal = mydb_Local.cursor()
                    Update_Website_Status = "UPDATE mcagovin_orgnames SET website = '"+str(Find_Link)+"',address = '"+str(Find_address)+"',phone = '"+str(Find_Contact)+"', website_status = 'Y' WHERE Company_Name = '" + str(Company_name) + "'"
                    mycursorLocal.execute(Update_Website_Status)
                    mydb_Local.commit()
                    Global_Link_inserted += 1
                    print('Global_Link_inserted : ', Global_Link_inserted)
                    MyLoop = 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                          fname, "\n", exc_tb.tb_lineno)
                    MyLoop = 0
                    mydb_Local.close()
                    mycursorLocal.close()
                    time.sleep(5)
        else:
            MyLoop1 = 0
            while MyLoop1 == 0:
                try:
                    mydb_Local = Local_connection_links()
                    mycursorLocal = mydb_Local.cursor()
                    Update_Website_Status = "UPDATE mcagovin_orgnames SET website_status = 'N' WHERE Company_Name = '" + str(Company_name) + "'"
                    mycursorLocal.execute(Update_Website_Status)
                    mydb_Local.commit()
                    Global_Link_NOT_Found += 1
                    print('Global_Company_not_Found : ', Global_Link_NOT_Found)
                    MyLoop1 = 1
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                          fname, "\n", exc_tb.tb_lineno)
                    MyLoop1 = 0
                    try:
                        mydb_Local.close()
                        mycursorLocal.close()
                    except:pass
                    time.sleep(5)

    print('Web Site Found: '+str(Global_Link_Found))
    print('Web Site Not Found : ' + str(Global_Link_NOT_Found))
    print('Website Inserted: '+str(Global_Link_inserted))


Collect_Link()
