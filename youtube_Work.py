from selenium import webdriver
import time
import sys, os
import mysql.connector
import datetime


def test():
    data_count = 0
    browser = webdriver.Chrome(executable_path='D:\\PycharmProjects\\Comapany_WEBSITE&MAIL\\chromedriver.exe')
    browser.maximize_window()
    Search_keyword = 'heartfulness'
    browser.get('https://www.youtube.com/results?search_query='+Search_keyword)
    time.sleep(2)
    video_deatails = ''
    channel_link = ['https://www.youtube.com/channel/UCoG2o8WtvYh8sCS40pUFtCg','https://www.youtube.com/channel/UCJiYdoZ48Gip9QFhkml4zMg']
    video_links = []
    y = 1080
    a = True
    while a == True:
        try:
            if len(video_links) < 500:
                for video_deatails in browser.find_elements_by_xpath('//*[@class="text-wrapper style-scope ytd-video-renderer"]'):
                    b = True
                    while b == True:
                        try:
                            video_deatails = video_deatails.get_attribute('outerHTML')
                            youtube_channel_link = video_deatails.partition('class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false"')[2].partition(">")[0]
                            youtube_channel_link = youtube_channel_link.partition('href="')[2].partition('"')[0]
                            youtube_channel_link = "https://www.youtube.com"+youtube_channel_link
                            print(youtube_channel_link)

                            youtube_video_link = video_deatails.partition('yt-simple-endpoint style-scope ytd-video-renderer')[2].partition('>')[0]
                            youtube_video_link = youtube_video_link.partition('href="')[2].partition('"')[0]
                            youtube_video_link = "https://www.youtube.com" + youtube_video_link
                            print(youtube_video_link)

                            if youtube_video_link not in video_links:
                                video_links.append(youtube_video_link)
                                if youtube_channel_link not in channel_link:
                                    browser.execute_script("window.open('');")
                                    browser.switch_to.window(browser.window_handles[1])
                                    browser.get(str(youtube_video_link))
                                    time.sleep(3)
                                    video_Title = ''
                                    video_Views = ''
                                    video_Date = ''
                                    channel_subscribers = ''
                                    channel_name = ''
                                    desc = ''
                                    comments = ''
                                    hash_tag = ''

                                    keywordFound = False

                                    for video_Title in browser.find_elements_by_xpath('//*[@class="title style-scope ytd-video-primary-info-renderer"]'):
                                        video_Title = video_Title.get_attribute('innerText').strip()
                                        break
                                    print(video_Title)

                                    for video_Views in browser.find_elements_by_xpath('//*[@class="view-count style-scope yt-view-count-renderer"]'):
                                        video_Views = video_Views.get_attribute('innerText').replace('views','').replace(',','').strip()
                                        break
                                    print(video_Views)

                                    for video_Date in browser.find_elements_by_xpath('//*[@id="date"]'):
                                        video_Date = video_Date.get_attribute('innerText').replace('•', '').strip()
                                        cont = False
                                        if 'hours' in video_Date:
                                            cont = True
                                        if 'min' in video_Date:
                                            cont = True
                                        if 'Hours' in video_Date:
                                            cont = True
                                        if 'Min' in video_Date:
                                            cont = True
                                        if cont ==  True:
                                            now = datetime.datetime.now()
                                            video_Date = now.strftime("%b %d, %Y")
                                        break
                                    print(video_Date)

                                    for channel_subscribers in browser.find_elements_by_xpath('//*[@id="owner-sub-count"]'):
                                        channel_subscribers = channel_subscribers.get_attribute('innerText').replace('subscribers', '').strip()
                                        break
                                    print(channel_subscribers)
                                    for channel_name in browser.find_elements_by_xpath('//*[@id="text-container"]'):
                                        channel_name = channel_name.get_attribute('innerText').strip()
                                        break
                                    print(channel_name)

                                    for hash_tag in browser.find_elements_by_xpath('//*[@class="super-title style-scope ytd-video-primary-info-renderer"]'):
                                        hash_tag = hash_tag.get_attribute('innerText').strip()
                                        break
                                    print(hash_tag)

                                    try:
                                        for more_button_desc in browser.find_elements_by_xpath('//*[@class="more-button style-scope ytd-video-secondary-info-renderer"]'):
                                            more_button_desc.click()
                                            time.sleep(1)
                                            break
                                    except:pass

                                    for desc in browser.find_elements_by_xpath('//*[@id="description"]'):
                                        desc = desc.get_attribute('innerText')
                                        break
                                    print(desc)

                                    for comments in browser.find_elements_by_xpath('//*[@id="comments"]'):
                                        comments = comments.get_attribute('innerText')
                                        break
                                    print(comments)

                                    if Search_keyword.lower() in video_Title.lower():
                                        keywordFound = True
                                    if Search_keyword.lower() in comments.lower():
                                        keywordFound = True
                                    if Search_keyword.lower() in desc.lower():
                                        keywordFound = True
                                    if Search_keyword.lower() in hash_tag.lower():
                                        keywordFound = True
                                    if Search_keyword.lower() in channel_name.lower():
                                        keywordFound = True

                                    if keywordFound == True:
                                        # Local_Connection_Function()
                                        data_insert(video_Title,video_Views,video_Date,channel_subscribers,channel_name,youtube_video_link,youtube_channel_link,Search_keyword,data_count)
                                        data_count += 1
                                        print('Kitna Mila hai Bhai youtube videos: ' + str(data_count))
                                    else:pass
                                    browser.close()
                                    browser.switch_to.window(browser.window_handles[0])
                                else:pass
                            else:pass
                            b = False
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                                  fname,
                                  "\n", exc_tb.tb_lineno)
                            b = True
                browser.execute_script("window.scrollTo(0, "+str(y)+")")
                y += 1080
                a = True
            else:
                print('Work Done')
                browser.close()
                a = False
                quit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            a = True
            time.sleep(3)


def Local_Connection_Function():
    a = 0
    while a == 0:
        try:
            mydb_Local = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                passwd='Premjogu007',
                database='youtube')
            print('SQL Local Connection Connected')
            return mydb_Local
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Error ON : " + " " + str(sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
            print(Error_text)
            a = 0
            time.sleep(5)


def data_insert(video_Title,video_Views,video_Date,channel_subscribers,channel_name,youtube_video_link,youtube_channel_link,Search_keyword,data_count):
    mydb_Local = Local_Connection_Function()
    mycursorLocal = mydb_Local.cursor()
    c = True
    while c == True:
        try:
            Duplicate_Email = "Select * from youtube_scraper where video_url = '" + str(youtube_video_link) + "'"
            mycursorLocal.execute(Duplicate_Email)
            results = mycursorLocal.fetchall()
            if len(results) > 0:
                print('Duplicate video')
                c = False
            else:
                insert_data = "INSERT INTO youtube_scraper(video_title,video_url,video_view,video_upload_date,channel_name,channel_url,channel_subscriber,found_keyword)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (str(video_Title), str(youtube_video_link), str(video_Views), str(video_Date), str(channel_name),
                          str(youtube_channel_link), str(channel_subscribers), str(Search_keyword))
                mycursorLocal.execute(insert_data, values)
                mydb_Local.commit()
                print('Insert')
                c = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            c = True
            time.sleep(3)

test()


