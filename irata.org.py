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
    browser.get('https://irata.org/de/members?limit=999')
    time.sleep(3)
    total_list = []
    div_count = 1
    for total_comapny in browser.find_elements_by_xpath('//*[@class="media"]'):
        all_detail = []
        company_name = ''
        country = ''
        href = ''
        for company_name in browser.find_elements_by_xpath(f'//*[@id="main-container"]/div/div/div[3]/div[{str(div_count)}]/div/a/h3'):
            company_name = company_name.get_attribute('innerText').strip()
            break
        all_detail.append(company_name)
        for country in browser.find_elements_by_xpath(f'//*[@id="main-container"]/div/div/div[3]/div[{str(div_count)}]/div/p'):
            country = country.get_attribute('outerHTML').replace('\n', '').strip()
            country = re.sub('\s+', ' ', country)
            country = country.partition("</span>")[2].partition("<br>")[0].strip()
            break
        all_detail.append(country)
        for href in browser.find_elements_by_xpath(f'//*[@id="main-container"]/div/div/div[3]/div[{str(div_count)}]/div/p/a'):
            href = href.get_attribute('href').strip()
            break
        all_detail.append(href)
        div_count += 1
        print(all_detail)
        total_list.append(all_detail)
    count = 209
    for list_of_details in total_list[209:]:
        a = True
        while a == True:
            try:
                browser.get(list_of_details[2])
                time.sleep(2)
                detail_panel = ''
                for detail_panel in browser.find_elements_by_xpath('//*[@class="panel-body"]'):
                    detail_panel =  detail_panel.get_attribute('outerHTML').replace('\n', '').strip()
                    detail_panel = re.sub('\s+', ' ', detail_panel)
                    break

                company_name = list_of_details[0]
                print('company_name: ',company_name)

                href = list_of_details[2]
                print('href: ',href)

                country = list_of_details[1]
                if 'Korea (South)' in country:
                    country = 'KR'
                else:
                    country = Get_country_code(country)
                if country == '':
                    pass
                print('country: ',country)
                website = ''
                for website in browser.find_elements_by_xpath('//*[@class="body_text"]'):
                    website =  website.get_attribute('href').strip()
                    break
                print('website: ',website)

                tel = detail_panel.partition("Telefon:</strong>")[2].partition("<strong>Adresse:")[0].replace('<br>','').strip()
                print('tel: ',tel)

                main_address = ''
                streetAddress = ''
                for streetAddress in browser.find_elements_by_xpath('//*[@itemprop="streetAddress"]'):
                    streetAddress = streetAddress.get_attribute('innerText').strip()
                    main_address += streetAddress+', '
                    break
                print('streetAddress: ',streetAddress)
                addressRegion = ''
                for addressRegion in browser.find_elements_by_xpath('//*[@itemprop="addressRegion"]'):
                    addressRegion = addressRegion.get_attribute('innerText').strip()
                    main_address += addressRegion+', '
                    break
                print('addressRegion: ',addressRegion)
                addressLocality = ''
                for addressLocality in browser.find_elements_by_xpath('//*[@itemprop="addressLocality"]'):
                    addressLocality = addressLocality.get_attribute('innerText').strip()
                    main_address += addressLocality+', '
                    break
                print('addressLocality: ',addressLocality)
                addressCountry = ''
                for addressCountry in browser.find_elements_by_xpath('//*[@itemprop="addressCountry"]'):
                    addressCountry = addressCountry.get_attribute('innerText').strip()
                    main_address += addressCountry+', '
                    break
                print('addressCountry: ',addressCountry)
                postalCode = ''
                for postalCode in browser.find_elements_by_xpath('//*[@itemprop="postalCode"]'):
                    postalCode = postalCode.get_attribute('innerText').strip()
                    main_address += postalCode
                    break
                print('postalCode: ',postalCode)

                main_address = main_address.strip().rstrip(',')
                print('main_address: ',main_address)

                contact_name = detail_panel.partition('Technical Authority:</strong>')[2].partition("</p>")[0].replace('<br>','').strip()
                print('contact_name: ',contact_name)
                email = ''
                for email in browser.find_elements_by_xpath('//*[@class="btn btn-success btn-block btn-lg"]'):
                    email =  email.get_attribute('href')
                    email = email.partition("mailto:")[2].strip()
                    break
                print('email: ',email)
                if email != "":
                    insert_details(main_address, email, tel,contact_name,country,company_name,href,website)
                count +=1
                print(f'Links Done: {str(count)} / {str(len(total_list))}')
                a = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                    "\n",
                    exc_tb.tb_lineno)
                time.sleep(5)
                a = True


def insert_details(main_address, email, tel,contact_name,country,company_name,href,website):
    Org_NAME = str(company_name).replace("'",'')
    Address = str(main_address).replace("'",'')
    city = ''
    state = ''
    country = str(country).replace("'",'')
    contact_name = str(contact_name).replace("'",'')
    telphone = str(tel)
    fax = ''
    mobile_no = ''
    Emailid = str(email)
    skype_id = ''
    website = str(website)
    product_services = ''
    cpv = ''
    source = 'irata.org'
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
                country = country.replace("'",'')
                CompanyInfoDB_Local = CompanyInfoDB_connection()
                CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                # country_code = country.capitalize()
                Country_code = "SELECT `Code` FROM `dms_country_tbl` WHERE `Country` = '"+str(country)+"'"
                # print(Country_code)
                CompanyInfoDB_cursorLocal.execute(Country_code)
                results = CompanyInfoDB_cursorLocal.fetchone()
                try:
                    results = results[0]
                except:pass
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