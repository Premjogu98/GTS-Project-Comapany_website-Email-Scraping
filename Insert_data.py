from datetime import datetime
import Global_var
import time
import mysql.connector
import sys, os
import pymysql.cursors


def CompanyInfoDB_connection():
    connection = ''
    a = 0
    while a == 0:
        try:
            # connection = pymysql.connect(host='192.168.0.202',
            #                              user='ams',
            #                              password='amsbind',
            #                              db='CompanyInfoDB',
            #                              charset='utf8',
            #                              cursorclass=pymysql.cursors.DictCursor)
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


def insert_into_CompanyInfoDB(Company_Name, Company_Address, Company_Phone, Company_Website, Disting_Email_list):
    Org_NAME = Company_Name
    Address = Company_Address
    city = ''
    state = ''
    pincode = ''
    country = 'IN'
    contact_name = ''
    telphone = Company_Phone
    fax = ''
    mobile_no = ''
    Emailid = ''
    skype_id = ''
    website = Company_Website
    product_services = ''
    cpv = ''
    source = 'mca.gov.in-google.com'
    doc_path = ''
    status = ''
    user = '5'  # 5 for Prem
    CompanyInfoDB_Local = CompanyInfoDB_connection()
    CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
    a = True
    while a ==  True:
        try:
            if len(Disting_Email_list) >= 1:
                for dis_email in Disting_Email_list:
                    global loop
                    loop = True
                    while loop == True:
                        try:
                            CompanyInfoDB_Local = CompanyInfoDB_connection()
                            CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                            Duplicate_Email = "Select A_id from CompanyInfoIndia where email_id = '" + str(dis_email) + "'"
                            CompanyInfoDB_cursorLocal.execute(Duplicate_Email)
                            # CompanyInfoDB_Local.commit()
                            results = CompanyInfoDB_cursorLocal.fetchall()
                            # CompanyInfoDB_Local.close()
                            # CompanyInfoDB_cursorLocal.close()
                            loop = False
                            if len(results) > 0:
                                print('Duplicate Email')
                                loop = False
                            else:
                                # CompanyInfoDB_Local = CompanyInfoDB_connection()
                                # CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                                # Insert On CompanyInfoIndia====================================================================
                                insert_data = "INSERT INTO CompanyInfoIndia(org_name,Address,city,state,pincode,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                values = (
                                str(Org_NAME), str(Address), str(city), str(state), str(pincode), str(country),
                                str(contact_name), str(telphone), str(fax), str(mobile_no), str(dis_email),
                                str(skype_id), str(website), str(product_services), str(cpv), str(source),
                                str(doc_path), str(status), str(user))
                                CompanyInfoDB_cursorLocal.execute(insert_data, values)
                                CompanyInfoDB_Local.commit()
                                # print('Insert On CompanyInfoIndia Table')
                                # Insert On CompanyInfo_Final ==================================================================
                                insert_On_L2L_data = "INSERT INTO CompanyInfo_Final(org_name,Address,city,state,pincode,country,contact_name,telphone,fax,mobile_no,email_id,skype_id,website,product_services,cpv,source,doc_path,status,user)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                insert_On_L2L_values = (
                                    str(Org_NAME), str(Address), str(city), str(state), str(pincode), str(country),
                                    str(contact_name),
                                    str(telphone), str(fax), str(mobile_no), str(dis_email), str(skype_id),
                                    str(website),
                                    str(product_services), str(cpv), str(source), str(doc_path), str(status), str(user))

                                CompanyInfoDB_cursorLocal.execute(insert_On_L2L_data, insert_On_L2L_values)
                                CompanyInfoDB_Local.commit()
                                # CompanyInfoDB_Local.close()
                                # CompanyInfoDB_cursorLocal.close()
                                # print('Insert On CompanyInfo_Final Table')
                            loop = False
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                                  fname,
                                  "\n", exc_tb.tb_lineno)
                            loop = True
                            CompanyInfoDB_Local.close()
                            time.sleep(15)

                # Update On Website Status ==================================================================
                # CompanyInfoDB_Local = CompanyInfoDB_connection()
                # CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                Update_Website_Status = "UPDATE mcagovin_orgnames SET email_status = 'Y' WHERE Company_Name = '" + str(
                    Company_Name) + "'"
                CompanyInfoDB_cursorLocal.execute(Update_Website_Status)
                CompanyInfoDB_Local.commit()
                print('Update email_status TO YES(Y) On mcagovin_orgnames Table')
                # CompanyInfoDB_Local.close()
                # CompanyInfoDB_cursorLocal.close()
            else:
                CompanyInfoDB_Local = CompanyInfoDB_connection()
                CompanyInfoDB_cursorLocal = CompanyInfoDB_Local.cursor()
                Update_Website_Status = "UPDATE mcagovin_orgnames SET email_status = 'N' WHERE Company_Name = '" + str(
                    Company_Name) + "'"
                CompanyInfoDB_cursorLocal.execute(Update_Website_Status)
                CompanyInfoDB_Local.commit()
                print('Update email_status TO NO(N) On mcagovin_orgnames Table')
            CompanyInfoDB_Local.close()
            CompanyInfoDB_cursorLocal.close()
                # loop = False
            a = False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            a = True
            CompanyInfoDB_cursorLocal.close()
            CompanyInfoDB_Local.close()
            time.sleep(15)







