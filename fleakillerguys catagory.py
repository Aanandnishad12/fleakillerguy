# "fleakillerguys_categories run is scuccessfull run its course "
from bs4 import BeautifulSoup 
import re
import time
import requests
import sys
import time
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import mysql.connector
import sys
def anand():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anishad@123",
    database="abc"
    )
    mycursor = mydb.cursor() 
    mycursor.execute("""CREATE TABLE if not exists `fleakillerguys_categories`(
    `id` int NOT NULL AUTO_INCREMENT,
    `category` varchar(250) NOT NULL,
    `sub_category` varchar(250) DEFAULT NULL,
    `page_url` varchar(250) NOT NULL,
    `processed` int NOT NULL DEFAULT '0',
    KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1
    """)

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}   
    def get_category(link):
        response = requests.get(link, headers = headers)
        # print(response.status_code)
        html = response.text
        soup = BeautifulSoup(html)
        return soup


    url='https://www.fleakillerguys.com/'
    soup= get_category(url)
    #print(soup) 
    data_tag=soup.find('div',attrs = {'class':'dropdown-menu'})
    ul_tag=data_tag.find('ul',attrs = {'class':'woo-category-nav'})
    li_tag=ul_tag.findAll('li')
    for li in li_tag:

        a_tag=li.find('a')
        link=a_tag.get('href')
        cat1=a_tag.text
        # print(cat1) 
        # print(link)
        myresult =''
        try:
            mycursor = mydb.cursor()     
            mycursor.execute("SELECT id FROM `fleakillerguys_categories` WHERE page_url = %s", (link,))
            myresult = mycursor.fetchall()
            # print(myresult)
        except Exception as e:
            pass
            # print (e)
        if myresult == []:  
         
            mycursor = mydb.cursor()
            val=list(zip((cat1,),(link,)))
            # print(val)
      
            sql = """insert into fleakillerguys_categories(`category`,`page_url`) values (%s,%s)""" 
            mycursor.executemany(sql,val) 
            mydb.commit() 
        try: 
            ul_tag2=li.find('ul',attrs = {'class':'children'})
            a_tag2=ul_tag2.find('a')
            link=a_tag2.get('href')
            cat2=a_tag2.text
            # print(cat2,'++') 
            # print(link,'++')
            myresult =''
            try:
                mycursor = mydb.cursor()     
                mycursor.execute("SELECT id FROM `fleakillerguys_categories` WHERE page_url = %s", (link,))
                myresult = mycursor.fetchall()
                # print(myresult)
            except Exception as e:
                pass
                # print (e)
            if myresult == []:
                 
                mycursor = mydb.cursor()
                val=list(zip((cat1,),(cat2,),(link,)))
                # print(val)
              
                sql = """insert into fleakillerguys_categories(`category`,`sub_category`,`page_url`) values (%s,%s,%s)""" 
                mycursor.executemany(sql,val) 
                mydb.commit()   
        except Exception as e:
            pass
            # print (e)
def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "fleakillerGuy catagory "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
def main():
    try:
        anand()
        s = "Script Executed Successfully "
        mail_send(s)
        print(s)
    except:
        s = "Script Executed Unsuccessfully"
        print(s)


if __name__ == "__main__":
    main()  
