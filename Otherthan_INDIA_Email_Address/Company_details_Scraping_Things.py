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
                host=str('192.168.0.202'),
                user=str('ams'),
                passwd=str('amsbind'),
                database=str('CompanyInfoDB'),
                charset=str('utf8'))
            return connection
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)
            connection.close()


def Scraping_Company_Deatils():
    browser = webdriver.Chrome(executable_path=str('D:\\PycharmProjects\\Comapany_WEBSITE&MAIL\\chromedriver.exe'))
    browser.maximize_window()
    count = 0
    a = True
    while a == True:
        try:
            File_Location = open("D:\\Company Websites.txt", "r")
            Website_List = File_Location.read()
            Company_website_crawler = [int(e) if e.isdigit() else e for e in Website_List.split('\n')]
            if len(Company_website_crawler) > 0:
                if str(Company_website_crawler[0]) != '':
                    browser.get(str(Company_website_crawler[0]))
                    time.sleep(2)
                    try:
                        for click_alert in browser.find_elements_by_xpath('//*[@id="cookie-alert"]/div/div/form/input'):
                            click_alert.click()
                            break
                    except:pass
                    time.sleep(3)
                    address = ''
                    Email = ''
                    mobile = ''
                    Company_website = ''
                    Company_product_Services_detail = ''
                    Company_Name = ''
                    Country = ''
                    for Company_Name in browser.find_elements_by_xpath('//*[@class="mastHead-heading"]'):
                        Company_Name = Company_Name.get_attribute('innerText').strip()
                        print(Company_Name)
                        break
                    for address in browser.find_elements_by_xpath('//*[@class="infoList-item ico-location-alt"]'):
                        address = address.get_attribute('innerHTML').strip()
                        address = html.unescape(str(address))
                        address = re.sub(' +', ' ', str(address)).replace('\n', '').replace('{}', '').replace(' <br>', '<br>')
                        break
                    Split_list = address.split('<br>')
                    Country = Split_list[-1].upper()
                    if Country != '':
                        Country = Get_country_code(Country)
                        Country = str(Country).upper().replace("'",'').replace(',','').replace(')','').replace('(','')
                        if Country == 'NONE':
                            Country = ''
                    else:
                        Country = ''
                    print(Country)
                    address = address.replace('<br>', ', ').replace("'",'')
                    print(address)
                    for mobile in browser.find_elements_by_xpath('//*[@class="infoList-item ico-mobile"]'):
                        mobile = mobile.get_attribute('innerText').strip()
                        print(mobile)
                        break
                    for Email in browser.find_elements_by_xpath('//*[@class="infoList-item ico-mail-alt"]'):
                        Email = Email.get_attribute('innerText').strip()
                        print(Email)
                        break
                    for Company_website in browser.find_elements_by_xpath('//*[@class="infoBlock-cta ico-globe-2"]'):
                        Company_website = Company_website.get_attribute('href').strip()
                        print(Company_website)
                        break
                    for Company_product_Services_detail in browser.find_elements_by_xpath('//*[@class="infoBlock-blurb"]'):
                        Company_product_Services_detail = Company_product_Services_detail.get_attribute('innerText').strip().replace("'",'')
                        Company_product_Services_detail = html.unescape(str(Company_product_Services_detail))
                        # print(Company_product_Services_detail)
                        break
                    if Email != '':
                        insert_details(address, Email, mobile, Company_website, Company_product_Services_detail, Company_Name, Country)
                del Company_website_crawler[0]
                Txt_file = open('D:\\Company Websites.txt', 'w')
                for href in Company_website_crawler:
                    Txt_file.write(href+'\n')
                Txt_file.close()
                count += 1
                print(count,'Insert Done:')
                a = True
            else:
                a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n",
                  exc_tb.tb_lineno)
            time.sleep(5)
            a = True


def insert_details(address, Email, mobile, Company_website, Company_product_Services_detail,Company_Name,Country):
    Org_NAME = str(Company_Name)
    Address = str(address)
    city = ''
    state = ''
    pincode = ''
    country = str(Country)
    contact_name = ''
    telphone = str(mobile)
    fax = ''
    mobile_no = str(mobile)
    Emailid = str(Email)
    skype_id = ''
    website = str(Company_website)
    product_services = str(Company_product_Services_detail)
    cpv = ''
    source = 'automation.com'
    doc_path = ''
    status = ''
    user = '5'  # 5 for Prem
    CompanyInfoDB_Local = CompanyInfoDB_connection()
    a = True
    while a == True:
        try:
            CompanyInfoDB_Local = CompanyInfoDB_connection()
            CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()

            Duplicate_Email = "Select A_id from CompanyInfoIndia where email_id = '" + str(Emailid) + "'"
            CompanyInfoDB_cursorLocal.execute(Duplicate_Email)
            results = CompanyInfoDB_cursorLocal.fetchall()
            if len(results) > 0:
                print(' Duplicate Hai Ye Insert Nhi Hoga !!!')
                a = False
            else:
                insert_data_local = "INSERT INTO CompanyInfoInternational(org_name,Address,city,state,pincode,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (
                    str(Org_NAME), str(Address), str(city), str(state), str(pincode), str(country),
                    str(contact_name), str(telphone), str(fax), str(mobile_no), str(Emailid),
                    str(skype_id), str(website), str(product_services), str(cpv), str(source),
                    str(doc_path), str(status), str(user))
                CompanyInfoDB_cursorLocal.execute(insert_data_local, values)
                CompanyInfoDB_Local.commit()
                print('\nCompanyInfoInternational Main Insert Ho Gya Hai !!!')
                insert_On_L2L_data = "INSERT INTO CompanyInfo_Final(org_name,Address,city,state,pincode,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                insert_On_L2L_values = (
                    str(Org_NAME), str(Address), str(city), str(state), str(pincode), str(country),
                    str(contact_name),
                    str(telphone), str(fax), str(mobile_no), str(Emailid), str(skype_id),
                    str(website),
                    str(product_services), str(cpv), str(source), str(doc_path), str(status), str(user))

                CompanyInfoDB_cursorLocal.execute(insert_On_L2L_data, insert_On_L2L_values)
                CompanyInfoDB_Local.commit()
                print('CompanyInfo_Final Main Insert Ho Gya Hai !!!')
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
    else:
        a = True
        while a == True:
            try:
                CompanyInfoDB_Local = CompanyInfoDB_connection()
                CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                country_code = country.capitalize()
                Country_code = "SELECT `Code` FROM `dms_country_tbl` WHERE `Country` = '"+str(country_code)+"'"
                # print(Country_code)
                CompanyInfoDB_cursorLocal.execute(Country_code)
                results = CompanyInfoDB_cursorLocal.fetchone()
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