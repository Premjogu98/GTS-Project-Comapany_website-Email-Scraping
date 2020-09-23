from selenium import webdriver
import time
import sys, os
import re
import mysql.connector
import sys, os
import html
import wx
app = wx.App()

def CompanyInfoDB_connection():
    connection = ''
    a = 0
    while a == 0:
        try:
            connection = mysql.connector.connect(
                host='185.142.34.92',
                user='ams',
                passwd='TgdRKAGedt%h',
                database='companyinfo_db',
                charset='utf8')
            return connection
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def Scraping_Company_Deatils():
    browser = webdriver.Chrome(executable_path=str('F:\\chromedriver.exe'))
    browser.maximize_window()
    browser.get('http://insurance-directories.com/companies/letter-all')
    time.sleep(3)
    company_links = []
    for company_href in browser.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/ul/li/a'):
        company_href = company_href.get_attribute('href')
        company_links.append(company_href)
        print(len(company_links),': ',company_href)
    count = 2293
    for href in company_links[2293:]:
        a = True
        while a == True:
            try:
                browser.get(href)
                time.sleep(2)
                company_name = ''
                try:
                    company_name = browser.find_elements_by_xpath('//*[@class="companyname"]')
                    company_name = company_name[0].get_attribute('innerText').strip().replace('&amp;','&')
                except:
                    company_name = ''
                print('company_name: ',company_name)
                contact_detail = browser.find_elements_by_xpath('//*[@class="contact-details shaded"]/p')
                address = ''
                try:
                    address = contact_detail[0].get_attribute('outerHTML').replace('<p>','').replace('</p>','').replace('<br>',', ').replace('&amp;','&').strip()
                    address = address.rstrip(',')
                except:
                    address= ''
                print('Address: ',address)
                Tel = ''
                try:
                    Tel = contact_detail[1].get_attribute('innerText').replace('Tel:','').strip()
                    if 'E-mail:' in Tel:
                        Tel = Tel.partition("E-mail:")[0].strip()
                    fax = Tel.partition("Fax:")[2].strip()
                    Tel = Tel.replace(fax,'').replace("Fax:",'')
                except:
                    Tel = ''
                print('Tel: ',Tel)
                website = ''
                try:
                    website = browser.find_elements_by_xpath('//*[@class="website"]')
                    website = website[0].get_attribute('innerText').replace('Website:','').strip()
                except:
                    website = ''
                print('website: ',website)

                email= ''
                for emailouter in browser.find_elements_by_xpath('//*[@class="contact-details shaded"]'):
                    emailouter = emailouter.get_attribute('outerHTML')
                    emailouter = re.sub('\s+', ' ', emailouter)
                    email = emailouter.partition("E-mail:")[2].partition("<br>")[0].strip()
                print('email: ',email)
                contact_person = ''
                for contact_person in browser.find_elements_by_xpath('//*[@class="personnel shaded"]/p'):
                    contact_person = contact_person.get_attribute('outerHTML').replace('<p>','').replace('</p>','').replace('\n',' ').replace('<br>',' , ').replace('&amp;','&').strip()
                    contact_person = re.sub('\s+', ' ', contact_person)
                    contact_person = contact_person.rstrip(',')
                    if len(contact_person) >= 95:
                        contact_person = contact_person[:95]+'...'
                    break
                print('contact_person: ',contact_person)

                category = browser.find_elements_by_xpath('//*[@class="company-type shaded"]/p')
                Company_type = ''
                Line_of_business = ''
                main_category = ''
                try:
                    Company_type = category[0].get_attribute('innerText').replace('&amp;','&').strip()
                    Company_type = re.sub('\s+', ' ', Company_type)
                    main_category += f'Company Type: {Company_type},'
                except:
                    pass
                try:
                    Line_of_business = category[1].get_attribute('innerText').replace('&amp;','&').strip()
                    Line_of_business = re.sub('\s+', ' ', Line_of_business)
                    main_category += f'Line Of Business: {Line_of_business}'
                except:
                    pass
                main_category = main_category.rstrip(',')
                print('main_category: ',main_category)
                if email != '':
                    insert_details(address, Tel, website,email,contact_person,main_category,href,company_name,fax)
                else:
                    #  wx.MessageBox('Email Error', 'Info', wx.OK | wx.ICON_ERROR)
                    pass
                count += 1
                print(f'Links Done: {str(count)} / {str(len(company_links))}')
                a = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
                wx.MessageBox('Error', 'Info', wx.OK | wx.ICON_ERROR)
                time.sleep(5)
                a = True
    
    wx.MessageBox('All Process Done', 'Info', wx.OK | wx.ICON_INFORMATION)


def insert_details(address, Tel, website,email,contact_person,main_category,href,Company_Name,fax):
    Org_NAME = str(Company_Name)
    Address = str(address)
    city = ''
    state = ''
    country = 'GB'
    contact_name = str(contact_person)
    telphone = str(Tel)
    fax = fax
    mobile_no = ''
    Emailid = str(email)
    skype_id = ''
    website = website
    product_services = str(main_category)
    cpv = ''
    source = 'insurance-directories.com'
    doc_path = str(href)
    status = ''
    user = '5'  # 5 for Prem
    CompanyInfoDB_Local = CompanyInfoDB_connection()
    a = True
    while a == True:
        try:
            CompanyInfoDB_Local = CompanyInfoDB_connection()
            CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()

            Duplicate_Email = "Select A_id from CompanyInfoInternational where email_id = '" + str(Emailid) + "'"
            CompanyInfoDB_cursorLocal.execute(Duplicate_Email)
            results = CompanyInfoDB_cursorLocal.fetchall()
            if len(results) > 0:
                print(' Duplicate Hai Ye Insert Nhi Hoga !!!')
                a = False
            else:
                insert_data_local = "INSERT INTO CompanyInfoInternational(org_name,Address,city,state,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (
                    str(Org_NAME), str(Address), str(city), str(state), str(country),
                    str(contact_name), str(telphone), str(fax), str(mobile_no), str(Emailid),
                    str(skype_id), str(website), str(product_services), str(cpv), str(source),
                    str(doc_path), str(status), str(user))
                CompanyInfoDB_cursorLocal.execute(insert_data_local, values)
                CompanyInfoDB_Local.commit()
                print('\nCompanyInfoInternational Main Insert Ho Gya Hai !!!')
                insert_On_L2L_data = "INSERT INTO CompanyInfo_Final(org_name,Address,city,state,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                insert_On_L2L_values = (
                    str(Org_NAME), str(Address), str(city), str(state), str(country),
                    str(contact_name),
                    str(telphone), str(fax), str(mobile_no), str(Emailid), str(skype_id),
                    str(website),
                    str(product_services), str(cpv), str(source), str(doc_path), str(status), str(user))

                CompanyInfoDB_cursorLocal.execute(insert_On_L2L_data, insert_On_L2L_values)
                CompanyInfoDB_Local.commit()
                print('CompanyInfo_Final Main Insert Ho Gya Hai !!!\n')
                a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                  fname,
                  "\n", exc_tb.tb_lineno)
            a = True
            wx.MessageBox('Error', 'Info', wx.OK | wx.ICON_ERROR)
            CompanyInfoDB_Local.close()
            time.sleep(10)


def Get_country_code(country):
    if country == 'USA':
        Country_code = 'US'
        return Country_code
    elif country == 'CONGO, DEM. REPUBLIC':
        Country_code = 'US'
        return Country_code
    elif country == 'COTE d IVOIRE':
        Country_code = 'CI'
        return Country_code
    elif country == 'FYR MACEDONIA':
        Country_code = 'MK'
        return Country_code
    elif country == 'KOREA (DEMOCRATIC PEOPLE S REPUBLIC OF)':
        Country_code = 'KP'
        return Country_code
    elif country == 'KOREA (REPUBLIC OF)':
        Country_code = 'KP'
        return Country_code
    elif country == 'PALESTINIAN TERRITORIES':
        Country_code = 'PS'
        return Country_code
    elif country == 'SLOVAK REPUBLIC':
        Country_code = 'SK'
        return Country_code
    elif country == 'STATELESS':
        Country_code = 'state'
        return Country_code
    elif country == 'UNITED STATES OF AMERICA':
        Country_code = 'US'
        return Country_code
    elif country == 'VIET NAM':
        Country_code = 'VN'
        return Country_code
    elif country == 'UNITED STATES':
        Country_code = 'US'
        return Country_code
    elif country == 'UNITED STATES MINOR OUTLYING ISLANDS':
        Country_code = 'UM'
        return Country_code
    elif 'QATAR' in country:
        Country_code = 'QA'
        return Country_code
    elif 'COLORADO' in country:
        Country_code = 'CO'
        return Country_code
    else:
        a = True
        while a == True:
            try:
                CompanyInfoDB_Local = CompanyInfoDB_connection()
                CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                # country_code = country.capitalize()
                Country_code = "SELECT `Code` FROM `dms_country_tbl` WHERE `Country` = '"+str(country)+"'"
                # print(Country_code)
                CompanyInfoDB_cursorLocal.execute(Country_code)
                results = CompanyInfoDB_cursorLocal.fetchone()
                results = results[0]
                print('Country code mil gaya hai!!!!!')
                return results
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                      "\n",
                      exc_tb.tb_lineno)
                time.sleep(5)
                a = True


Scraping_Company_Deatils()