from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys, os
import ctypes
import pymysql.cursors

import wx
import random
import re
import Global_var
from Insert_data import insert_into_CompanyInfoDB
from bs4 import BeautifulSoup
from htmldom import htmldom
import urllib.request
import urllib.parse
import requests
import html


def Local_connection_links():
    connection = ''
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
            try:
                connection.close()
            except:pass


def Collect_EMAIL():
    mydb_Local = Local_connection_links()
    mycursorLocal = mydb_Local.cursor()
    a = 0
    while a == 0:
        try:
            Company_Name_List = []
            address_List = []
            phone_List = []
            Website_List = []
            mycursorLocal.execute("SELECT Company_Name, address, phone, website FROM mcagovin_orgnames WHERE website_status = 'Y' AND email_status IS NULL")  # LIMIT 10000
            rows = mycursorLocal.fetchall()
            for row in rows:
                Company_Name = "%s" % (row["Company_Name"])
                address = "%s" % (row["address"])
                phone = "%s" % (row["phone"])
                links = "%s" % (row["website"])
                Company_Name_List.append(Company_Name)
                address_List.append(address)
                phone_List.append(phone)
                if links != 'http://www.salesbee.io/':  #
                    Website_List.append(links)
                else:pass
            time.sleep(2)
            print("Number OF website Get From Database: ", len(Website_List))
            Nav_WEBSITE(Website_List, Company_Name_List, address_List, phone_List)
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


def Nav_WEBSITE(Website_List, Company_Name_List, address_List, phone_List):
    browser = webdriver.Chrome(executable_path=str('D:\\PycharmProjects\\Comapany_WEBSITE&MAIL\\chromedriver.exe'))
    browser.maximize_window()
    time.sleep(1)
    Email_found = 0
    Contact_Us_Email_found = 0
    Count = 0
    Company_Name_Count = 0
    address_List_Count = 0
    phone_List_Count = 0
    for website in Website_List:
        a = 0
        while a == 0:
            try:
                browser.get(website)
                time.sleep(2)
                try:
                    alert = browser.switch_to_alert()  # Close Alert Popup
                    alert.dismiss()
                except:pass
                Company_name1 = Company_Name_List[Company_Name_Count]
                Company_name = Company_name1.replace("'", "''")
                Company_Address = address_List[address_List_Count]
                Company_Phone = phone_List[phone_List_Count]
                Company_Website = str(website)
                Contact_Us_Email_List = []
                Email_List = []
                get_website_outerHTML = ''
                for get_website_outerHTML in browser.find_elements_by_xpath('/html'):
                    get_website_outerHTML = get_website_outerHTML.get_attribute('outerHTML')
                    break
                get_website_outerHTML = get_website_outerHTML.lower()
                get_website_outerHTML = get_website_outerHTML.replace('\n', ' ')
                get_website_outerHTML = get_website_outerHTML.replace("(at)", "@")
                get_website_outerHTML = get_website_outerHTML.replace("(dot)", ".")
                get_website_outerHTML = get_website_outerHTML.replace("[at]", "@")
                get_website_outerHTML = get_website_outerHTML.replace("[dot]", ".")
                get_website_outerHTML = get_website_outerHTML.replace("( at )", "@")
                get_website_outerHTML = get_website_outerHTML.replace("( dot )", ".")
                get_website_outerHTML = get_website_outerHTML.replace("[ at ]", "@")
                get_website_outerHTML = get_website_outerHTML.replace("[ dot ]", ".")
                get_website_outerHTML = get_website_outerHTML.replace("%20", "")
                get_website_outerHTML = get_website_outerHTML.replace("%27", '')
                get_website_outerHTML = re.sub(' +', ' ',
                                               str(get_website_outerHTML))  # remove Multiple Spaces From String

                # Anchor_Tag = re.findall(r"(?<=<a).*?(?=</a>)", str(get_website_outerHTML))
                # print(Anchor_Tag)
                # ======================================================================================
                Script_Tag = re.findall(r"(?<=<script).*?(?=</script>)", str(get_website_outerHTML))
                for tag in Script_Tag:
                    get_website_outerHTML = get_website_outerHTML.replace(str(tag), '')
                # ======================================================================================
                Meta_Tag = re.findall(r'(?<=<meta).*?(?=>)', str(get_website_outerHTML))
                for tag1 in Meta_Tag:
                    get_website_outerHTML = get_website_outerHTML.replace(str(tag1), '')
                # ======================================================================================
                get_website_outerHTML = get_website_outerHTML.replace('<script', '').replace('</script>', '').replace(
                    '<script type="text/javascript">', '').replace('<meta', '').replace('%20','').replace("%27", '').replace("mailto:%0", '').replace('<!--','').replace('-->','')\
                    .replace('email:-','').replace('mailto:','').replace('mailto:%20','').replace('mailto:%27','')
                # =====================================================================================================
                # Email_regex = r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)'
                # Email = re.findall(Email_regex, get_website_outerHTML, re.M | re.I)
                # print(Email)
                # =====================================================================================================
                # Email = re.findall(r'[\w\.-]+@[\w\.-]+', get_website_outerHTML)
                # ====================================================================================================
                Count += 1
                print('Company Name ' + str(Count) + ': ', website)
                Email_regex = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)", get_website_outerHTML)

                print('Email Regex Through Found Email: ', Email_regex)

                for EMail in Email_regex:
                    Extension = ['.jpeg', '.png','.io','.xls','xyz.com','.doc','.jpeg','.pdf','.gif','.jpg','example','facebook','test@','test','amazon','naukri','wikipedia','tenders','tender']
                    if not any(x in EMail for x in Extension):
                        if EMail not in Email_List:
                            EMail = EMail.replace('%20','').replace("%27", '').replace("mailto:%0", '').replace('<!--','').replace('-->','')\
                    .replace('email:-','').replace('mailto:','').replace('mailto:%20','').replace('mailto:%27','').replace('--','')
                            Email_List.append(EMail)
                            Email_found += 1
                    else:
                        pass
                # print('Proper Email Address: ', Global_var.Email_List)
                # print('=============================================================================================\n')
                time.sleep(2)
                global found
                found = 0
                try:
                    try:
                        for Click_on_Contact_us in browser.find_elements_by_link_text('CONTACT US'):
                            Click_on_Contact_us.click()
                            time.sleep(3)
                            found += 1
                            break
                    except:
                        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                        for Click_on_Contact_us in browser.find_elements_by_link_text('CONTACT US'):
                            Click_on_Contact_us.click()
                            time.sleep(3)
                            found += 1
                            break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact Us'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact Us'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('CONTACTUS'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('CONTACTUS'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('contact us'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('contact us'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('ContactUs'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('ContactUs'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('contactus'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('contactus'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contactus'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contactus'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact us'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact us'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('contact'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('Contact'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_link_text('CONTACT'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_link_text('CONTACT'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="CONTACT US"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="CONTACT US"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="Contact Us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="Contact Us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="CONTACTUS"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="CONTACTUS"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="contact us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(5)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="contact us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(5)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="ContactUs"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="ContactUs"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="contactus"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="contactus"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="Contactus"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="Contactus"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="Contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="Contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@value="contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="Contact us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="Contact us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="ontact us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="contact us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="Contact Us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="Contact Us"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="CONTACT US"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="CONTACT US"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="contactus"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="contactus"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        try:
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="Contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                        except:
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll Down
                            for Click_on_Contact_us in browser.find_elements_by_xpath('//*[@title="Contact"]'):
                                Click_on_Contact_us.click()
                                time.sleep(3)
                                found += 1
                                break
                except:pass
                try:
                    if found == 0:
                        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                        headers = {'User-Agent': user_agent, }
                        request = urllib.request.Request(website, None, headers)  # The assembled request
                        response = urllib.request.urlopen(request)
                        html_data: str = response.read()
                        soup = BeautifulSoup(html_data)
                        for a_tag in soup.findAll('a'):
                            a_tag_list = []
                            global href
                            href = ''
                            href = a_tag.get('href')
                            a_tag_list.append(a_tag)
                            for tag in a_tag_list:
                                if 'href="/' in href:
                                    href = href.replace('href="/', 'href="'+str(website)+'/').replace('//', '/')
                                else:pass
                                if '>contactus<' in tag or '>contact<' in tag or '>enquiry<' in tag:
                                    browser.get(href)
                                    found += 1
                                    break
                except:pass
                if found != 0:
                    try:
                        alert = browser.switch_to_alert()  # Close Alert Popup
                        alert.dismiss()
                    except:
                        pass
                    try:
                        browser.switch_to.window(browser.window_handles[1])
                    except:
                        browser.switch_to.window(browser.window_handles[0])
                    Contact_Us_PAGE_outerHTML = ''
                    for Contact_Us_PAGE_outerHTML in browser.find_elements_by_xpath('/html'):
                        Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.get_attribute('outerHTML')
                        break
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.lower()
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace('\n', '')
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("(at)", "@")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("(dot)", ".")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("[at]", "@")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("[dot]", ".")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("( at )", "@")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("( dot )", ".")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("[ at ]", "@")
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace("[ dot ]", ".")
                    Contact_Us_PAGE_outerHTML = re.sub(' +', ' ', str(Contact_Us_PAGE_outerHTML))  # remove Multiple Spaces From String
                    # ======================================================================================
                    Contact_Us_PAGE_Script_Tag = re.findall(r"(?<=<script).*?(?=</script>)", str(Contact_Us_PAGE_outerHTML))
                    for tag in Contact_Us_PAGE_Script_Tag:
                        Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace(str(tag), '')
                    # ======================================================================================
                    Contact_Us_Meta_Tag = re.findall(r'(?<=<meta).*?(?=>)', str(Contact_Us_PAGE_outerHTML))
                    for tag1 in Contact_Us_Meta_Tag:
                        Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace(str(tag1), '')
                    # ======================================================================================
                    Contact_Us_PAGE_outerHTML = Contact_Us_PAGE_outerHTML.replace('<script', '').replace('</script>','').replace(
                        '<script type="text/javascript">', '').replace('<meta', '')

                    Contact_Us_Email_regex = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)", Contact_Us_PAGE_outerHTML)

                    print('Email Regex Through Found Contact US Page Email: ', Contact_Us_Email_regex)

                    for Contact_Us_EMail in Contact_Us_Email_regex:
                        Extension = ['.jpeg', '.png', '.io', '.xls', 'xyz.com', '.doc', '.jpeg', '.pdf', '.gif', '.jpg',
                                     'example', 'facebook', 'test@', 'test', 'amazon', 'naukri', 'wikipedia', 'tenders',
                                     'tender']
                        if not any(x in Contact_Us_EMail for x in Extension):
                            if Contact_Us_EMail not in Contact_Us_Email_List:
                                Contact_Us_EMail = Contact_Us_EMail.replace('%20', '').replace("%27", '').replace("mailto:%0", '').replace(
                                    '<!--', '').replace('-->', '').replace('email:-', '').replace('mailto:', '').replace('mailto:%20', '').replace('mailto:%27', '').replace('--','')
                                Contact_Us_Email_List.append(Contact_Us_EMail)
                                Contact_Us_Email_found += 1
                        else:
                            pass
                else:pass
                # Remove Duplicate From List
                Disting_Email_list = []
                for email in Email_List:
                    if email not in Disting_Email_list:
                        Disting_Email_list.append(email)
                    else:pass
                # Remove Duplicate From List
                for Contact_email in Contact_Us_Email_List:
                    if Contact_email not in Disting_Email_list:
                        Disting_Email_list.append(Contact_email)
                    else:pass
                print('Disting_Email_list: ', Disting_Email_list)
                try:
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                except:
                    browser.switch_to.window(browser.window_handles[0])
                insert_into_CompanyInfoDB(Company_name, Company_Address, Company_Phone, Company_Website,Disting_Email_list)
                Company_Name_Count += 1
                address_List_Count += 1
                phone_List_Count += 1
                a = 1
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                      exc_tb.tb_lineno)
                a = 0
                time.sleep(10)

    import wx
    app = wx.App()
    wx.MessageBox('All Process Are Done', 'Improve_Website_Rank', wx.OK | wx.ICON_INFORMATION)
    print('All Process Are Done')
    browser.close()
    sys.exit()


Collect_EMAIL()
