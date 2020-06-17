from selenium import webdriver
import time
import sys, os
import re


def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str('D:\\PycharmProjects\\Comapany_WEBSITE&MAIL\\chromedriver.exe'))
    browser.maximize_window()
    browser.get('https://www.automation.com/en-us/suppliers-and-integrator-directory')
    time.sleep(10)

    collect_companyLinks_Drop1(browser)


def collect_companyLinks_Drop1(browser):
    company_href_list = []
    a = 0
    loop_count = 0

    while a == 0:
        try:
            for dropdown in browser.find_elements_by_xpath(
                    '//*[@id="app-1"]/div/dynamic-html/div[1]/widget/div/dynamic-html/div/select/option[1]'):
                dropdown.click()
                break
            time.sleep(10)
            for next_page in range(665):
                for li_tag in range(1, 16, 1):
                    for company_href in browser.find_elements_by_xpath('//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[1]/div/dynamic-html/div/ul/li['+str(li_tag)+']/dynamic-html/div[2]/h3/a'):
                        company_href = company_href.get_attribute('href')
                        print(company_href)
                        company_href_list.append(company_href+'\n')
                        break
                if loop_count != 3:
                    try:
                        for NextPage in browser.find_elements_by_xpath(
                                '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[2]/div/dynamic-html/div/span[8]'):
                            NextPage.click()
                            time.sleep(4)
                            break
                        loop_count += 1
                    except:
                        pass
                else:
                    try:
                        for NextPage in browser.find_elements_by_xpath(
                                '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[2]/div/dynamic-html/div/span[9]'):
                            NextPage.click()
                            time.sleep(4)
                            break
                    except:
                        pass
            a = 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = 0
    collect_companyLinks_Drop2(company_href_list, browser)


def collect_companyLinks_Drop2(company_href_list,browser):
    a = 0
    loop_count = 0
    while a == 0:
        try:
            for dropdown in browser.find_elements_by_xpath(
                    '//*[@id="app-1"]/div/dynamic-html/div[1]/widget/div/dynamic-html/div/select/option[2]'):
                dropdown.click()
                break
            time.sleep(10)
            for next_page in range(200):
                for li_tag in range(1, 16, 1):
                    for company_href in browser.find_elements_by_xpath(
                            '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[1]/div/dynamic-html/div/ul/li[' + str(
                                    li_tag) + ']/dynamic-html/div[2]/h3/a'):
                        company_href = company_href.get_attribute('href')
                        print(company_href)
                        company_href_list.append(company_href+'\n')
                        break
                if loop_count != 3:
                    try:
                        for NextPage in browser.find_elements_by_xpath(
                                '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[2]/div/dynamic-html/div/span[8]'):
                            NextPage.click()
                            time.sleep(4)
                            break
                        loop_count += 1
                    except:pass
                else:
                    try:
                        for NextPage in browser.find_elements_by_xpath(
                                '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[2]/div/dynamic-html/div/span[9]'):
                            NextPage.click()
                            time.sleep(4)
                            break
                    except:pass
            a = 1

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = 0
    collect_companyLinks_Drop3(company_href_list, browser)


def collect_companyLinks_Drop3(company_href_list, browser):
    a = 0
    loop_count = 0

    while a == 0:
        try:
            for dropdown in browser.find_elements_by_xpath(
                    '//*[@id="app-1"]/div/dynamic-html/div[1]/widget/div/dynamic-html/div/select/option[3]'):
                dropdown.click()
                break
            time.sleep(10)
            for next_page in range(42):
                for li_tag in range(1, 16, 1):
                    for company_href in browser.find_elements_by_xpath(
                            '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[1]/div/dynamic-html/div/ul/li[' + str(
                                li_tag) + ']/dynamic-html/div[2]/h3/a'):
                        company_href = company_href.get_attribute('href')
                        print(company_href)
                        company_href_list.append(company_href+'\n')
                        break
                if loop_count != 3:
                    try:
                        for NextPage in browser.find_elements_by_xpath(
                                '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[2]/div/dynamic-html/div/span[8]'):
                            NextPage.click()
                            time.sleep(4)
                            break
                        loop_count += 1
                    except:
                        pass
                else:
                    try:
                        for NextPage in browser.find_elements_by_xpath(
                                '//*[@id="app-1"]/div/dynamic-html/div[4]/div/widget[2]/div/dynamic-html/div/span[9]'):
                            NextPage.click()
                            time.sleep(4)
                            break
                    except:pass
            a = 1

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = 0
    append_on_txt_File(company_href_list)


def append_on_txt_File(company_href_list):
    Txt_file = open('D:\\Company Websites.txt','w')
    disting_company_href_list = []
    for company_href in company_href_list:
        if company_href not in disting_company_href_list:
            disting_company_href_list.append(company_href)

    Txt_file.writelines(disting_company_href_list)
    Txt_file.close()
    import wx
    app = wx.App()
    wx.MessageBox('All Process Done', 'Info', wx.OK | wx.ICON_INFORMATION)


ChromeDriver()
