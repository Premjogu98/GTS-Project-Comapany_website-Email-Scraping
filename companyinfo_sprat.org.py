from selenium import webdriver
import time
import sys, os
import re
import mysql.connector
import sys, os
import html


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
    browser.get('https://sprat.org/members-list-2/')
    time.sleep(3)
    div = 137
    total_comapnylen = browser.find_elements_by_xpath('//*[@class="col-md-12 memberWrap"]')
    for total_comapny in browser.find_elements_by_xpath('//*[@class="col-md-12 memberWrap"]'):
        a = True
        while a == True:
            try:
                print(f'companyCount: {str(div)}')
                Email = browser.find_elements_by_xpath(f'//*[@id="products"]/div[{str(div)}]/div/div[1]/a')
                Email = Email[0].get_attribute('href').strip()
                Email = str(Email).partition(":")[2].strip()
                print('Email:',Email)
                
                if Email != '':
                    Company_Name = browser.find_elements_by_xpath(f'//*[@id="products"]/div[{str(div)}]/div/div[2]/h4')
                    Company_Name = Company_Name[0].get_attribute('innerText').strip()
                    print('Company_Name:',Company_Name)

                    contact_name = browser.find_elements_by_xpath(f'//*[@id="products"]/div[{str(div)}]/div/div[2]/h5')
                    contact_name = contact_name[0].get_attribute('innerText').strip()
                    print('contact_name:',contact_name)
                    
                    address = browser.find_elements_by_xpath(f'//*[@id="products"]/div[{str(div)}]/div/div[3]/p')
                    address = address[0].get_attribute('innerText').strip()
                    # print(address)

                    country = ''
                    if address == ',':
                        address = ''
                    else:
                        country = str(address).partition(",")[2].strip().upper()
                        if 'USA' in country:
                            country = 'US'
                        elif 'CANADA' in country:
                            country = 'CA'
                        elif 'NETHERLANDS' in country:
                            country = 'NL'
                        elif 'MEXICO' in country:
                            country = 'MX'
                        elif 'UNITED ARAB EMIRATES' in country:
                            country = 'AE'
                        elif 'AUSTRALIA' in country:
                            country = 'AU'
                        elif 'SWEDEN' in country:
                            country = 'SE'
                        elif 'ARGENTINA' in country:
                            country = 'AR'
                        elif 'HONG KONG' in country:
                            country = 'HK'
                        elif 'TURKEY' in country:
                            country = 'TR'
                        elif 'ITALY' in country:
                            country = 'IT'
                        elif 'INDIA' in country:
                            country = 'IN'
                        elif 'BRAZIL' in country:
                            country = 'BR'
                        elif 'DENMARK' in country:
                            country = 'DR'
                        elif 'UNITED KINGDOM' in country:
                            country = 'UK'
                        elif 'CHINA' in country:
                            country = 'CN'
                        elif 'TX' in country:
                            country = 'US'
                        elif 'ALGERIA' in country:
                            country = 'DZ'
                        elif 'GERMANY' in country:
                            country = 'DE'
                        else:
                            country = Get_country_code(country)
                    print('address:',address)
                    print('country:',country)

                    mobile = browser.find_elements_by_xpath(f'//*[@id="products"]/div[{str(div)}]/div/div[3]/span')
                    mobile = mobile[0].get_attribute('innerText').strip()
                    print('mobile:',mobile)
                    insert_details(address, Email, mobile,Company_Name,country,contact_name)
                div += 1
                a = False
                if div == len(total_comapnylen):
                    break
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                    "\n",
                    exc_tb.tb_lineno)
                time.sleep(5)
                a = True


def insert_details(address, Email, mobile,Company_Name,Country,contact_name):
    Org_NAME = str(Company_Name)
    Address = str(address)
    city = ''
    state = ''
    country = str(Country)
    contact_name = contact_name
    telphone = str(mobile)
    fax = ''
    mobile_no = str(mobile)
    Emailid = str(Email)
    skype_id = ''
    website = ''
    product_services = ''
    cpv = ''
    source = 'sprat.org'
    doc_path = ''
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