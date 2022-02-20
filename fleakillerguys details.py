# fleakillerguy
'''Ms. Harshal Lad'''
from bs4 import BeautifulSoup 
import re
import time
import requests
import sys
import json 
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
import mysql.connector
mydb = mysql.connector.connect(
 host="localhost",
  user="root",
  password="Anishad@123",
  database="abc"
)
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS `fleakillerguys_op`(
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Product_Title` varchar(900) DEFAULT NULL,
    `sku` varchar(600) DEFAULT NULL,
    `parent_sku` varchar(600) DEFAULT NULL,
    `vnp` varchar(600) DEFAULT NULL,
    `product_description_short` text,
    `product_description_long` text,
    `image1` varchar(1500) DEFAULT NULL,
    `category` text,
    `sub_category` text,
    `Product_link` text,
    `discontinued`int DEFAULT '0',
    `previous_vnp`decimal(7,2) DEFAULT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1
""")


def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "Differences between vnp  "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    filename = "File_name_with_extension"
    attachment = open('./fleakillerguys_vnp.csv', "rb")
    
    parter1 = MIMEBase('application', 'octet-stream')
    parter1.set_payload((attachment).read())
    encoders.encode_base64(parter1)
    parter1.add_header('Content-Disposition', 'attachment', filename='fleakillerguys_vnp.csv')
    msg.attach(parter1)
    
    attachment = open('./fleakillerguys_sku.csv', "rb")
    parter2 = MIMEBase('application', 'octet-stream')
    parter2.set_payload((attachment).read())
    encoders.encode_base64(parter2)
    parter2.add_header('Content-Disposition', 'attachment', filename='fleakillerguys_sku.csv')
    msg.attach(parter2)
    
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def anand():

    count=1
    payload={'username': 'dans', 'password': 'Construction1','wc_website_input':'','woocommerce-login-nonce': '5641f8c76e','_wp_http_referer': '/my-account/','login': 'Log+in'}
    mycursor = mydb.cursor()
    Query = ("select * from  `fleakillerguys_categories` where `processed` = '0'")
    mycursor.execute(Query)
    records = mycursor.fetchall()
    #print(records)
    if records != []:
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE `fleakillerguys_op`  SET previous_vnp = vnp")
    new_prod = []
    for rows in records:
  
        category=rows[1]
        sub_category=rows[2]
        # print(sub_category)
        url=rows[3]
        mycursor = mydb.cursor()     
        mycursor.execute("UPDATE `fleakillerguys_categories` SET `processed` = '1' WHERE page_url = %s", (url,))
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}   
        with requests.Session() as s:
            response3 = s.post('https://www.fleakillerguys.com/my-account/', headers = headers,data=payload)
            response = s.get(url, headers = headers )
            html = response.text
            soup = BeautifulSoup(html,'lxml')
            main_tag=soup.find('main',attrs = {'id':'site-main-content'})
            ul_tag=main_tag.find('ul',attrs = {'class':'products columns-4'})
            a_tag=ul_tag.findAll('a')
            for a in a_tag:
               
                link=a.get('href')
                # print(link)
                response2 = s.get(link, headers = headers )
                html2 = response2.text
                soup2 = BeautifulSoup(html2,'lxml')
                data=soup2.find('div',attrs = {'class':'summary entry-summary'})
                # print(data)
                title = ''
                title=data.find('h1',attrs = {'class':'product_title entry-title'}).text.encode().decode('latin1').replace('ÃƒÂ¢Ã‚â‚¬Ã‚â€œ','--').replace('ÃƒÂ¢Ã‚â‚¬Ã‚Â³','"').replace('ÃƒÆ’Ã‚Â¢Ãƒâ€šÃ¢â€šÂ¬Ãƒâ€šÃ‚Â³','"').replace('ÃƒÆ’Ã‚Â¢Ãƒâ€šÃ¢â€šÂ¬Ãƒâ€šÃ¢â‚¬Å“','--').replace('â','')
                # print(title)
                # price=0
                details = soup2.find("script", {"type":"application/ld+json"})
                details = str(details).replace('<script type="application/ld+json">',"").replace('</script>','')
                details = eval(details)
                y = details["@graph"][-1]["offers"][0]
                for i in y:
                
                    try:
                        if i == "price":
                            price = y[i]
                            # print(price)
                    except Exception as e:
                        pass
                        # print(e)
                    # print(price)
                y = details["@graph"][-1]
                for i in y:
                    
                    try:
                        if i == "name":
                            name = y[i]
                    except Exception as e:
                        pass
                            # print(e)

                    try:
                        if i == "sku":
                            sku_val = y[i]
                            sku_val=('FL01'+sku_val).replace(' ','').replace('-','')
                    except Exception as e:
                        pass
                            # print(e)
                    try:
                        if i == "description":
                            desc_val = y[i]
                    except Exception as e:
                        pass
                            # print(e)
                    try:
                        if i == "image":
                            img = y[i].replace("\\","")
                    except Exception as e:
                        pass
                            # print(e)
                long_desc = re.search('class="woocommerce-Tabs-panel woocommerce-Tabs-panel--description.*?Description(.*?)</p>',str(soup2),flags = re.S)
            
                if long_desc :
                    long_desc = long_desc.group(1)
                    long_desc = re.sub('<.*?>','',long_desc,flags=re.S)
                else :
                    long_desc = ''
                

                if title=='' or price==0:
                    discontinued='1'
                else:
                    discontinued='0'    
                myresult =''
                try:
                    mycursor = mydb.cursor() 
                    mycursor.execute("SELECT id FROM `fleakillerguys_op` WHERE Product_Title = %s", (title,))
                    myresult = mycursor.fetchall()
                    # print(myresult)
                except Exception as e:
                    pass
                    # print (e)
                if myresult == []:
                    mycursor = mydb.cursor()
                    new_prod.append(sku_val)
                    val=list(zip((title,),(sku_val,),(sku_val,),(price,),(desc_val,),(long_desc,),(img,),(category,),(sub_category,),(link,),(discontinued,)))
                    # print(val) 
                    mycursor = mydb.cursor()
                
                    sql = """insert into `fleakillerguys_op`(`Product_Title`, `sku`, `parent_sku`,`vnp`,`product_description_short`,`product_description_long`,`image1`,`category`,`sub_category`,`Product_link`,`discontinued`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 
                    mycursor.executemany(sql,val)
                    mydb.commit()
                else:
                    mycursor = mydb.cursor()
                    mycursor.execute("UPDATE `fleakillerguys_op` SET `vnp`= %s WHERE Product_Title= %s", (price,title,)) 
                    mydb.commit()
                    
    mycursor = mydb.cursor()    
    mycursor.execute("select sku,vnp,previous_vnp from fleakillerguys_op")
    result = mycursor.fetchall()
    with open('fleakillerguys_vnp.csv', 'w',  newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer = csv.DictWriter(outcsv, fieldnames = ["sku", "vnp", "previous_vnp"])
            writer.writeheader()
    with open('fleakillerguys_sku.csv', 'w',  newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer = csv.DictWriter(outcsv, fieldnames = ["sku"])
        writer.writeheader()
    

    for x in result:
        sku=x[0]
        vnp= x[1]
        pvnp= x[2]
        if vnp!=pvnp:
            with open('fleakillerguys_vnp.csv', 'a', newline='') as vnpcsv:
                writer = csv.writer(vnpcsv)
                writer = csv.DictWriter(vnpcsv, fieldnames =[sku,vnp,pvnp])
                writer.writeheader()
    for i in new_prod:
        with open('fleakillerguys_sku.csv', 'a', newline='') as vnpcsv:
            writer = csv.writer(vnpcsv)
            writer = csv.DictWriter(vnpcsv, fieldnames =[i])
            writer.writeheader()

            
def main():
    try:
        anand()
        s = "Script Executed Successfully"
        mail_send(s)
        print(s)
    except:
        s = "Script Executed Unsuccessfully"
        print(s)

if __name__ == "__main__":
    main()                          
    