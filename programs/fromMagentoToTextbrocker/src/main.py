
import ConfigParser
import xmlrpclib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import sys
from datetime import date

import threading
#from send_mail import send_mail


__author__ = 'Carlos Espinosa'
class item(object):
    def __init__(self):
        self.sku=''
        self.itemShortDesc=''
        self.itemDesc=''
        self.itemName=''

class getInfo(threading.Thread):
    def __init__(self):
        pass
    def run(self,item):
        self.sku=item.sku
        token = server.login(mg_username, mg_password)
        infoproduct = server.call(token, 'catalog_product.info',[self.sku])
        item.itemName= infoproduct['name']
        item.itemShortDesc=infoproduct['short_description']
        item.itemDesc=infoproduct['description']
        send=writeFile(item)     
        
class writeFile():
    def __init__(self,item):
        item.itemName= item.itemName if item.itemName else ''
        item.itemShortDesc= item.itemShortDesc if item.itemShortDesc else ''
        item.itemDesc= item.itemDesc if item.itemDesc else ''
        instructions=introduction+"\n\n"+item.itemName+"\n\n" +"Short Description:\n"+item.itemShortDesc+"\n"  +"Long Description:\n"+item.itemDesc+"\n" 
        
        lineToWrite=[item.itemName,'100','500','3','1','1163',instructions.encode(encoding='UTF-8',errors='strict')]
        outfile.writerow(lineToWrite)        


class Main(threading.Thread):
    def __init__(self):
        pass
    def run(self):
        for row in infile:
            Item=item()
            Item.sku = row[0]+" "  
            get=getInfo()
            get.run(Item)

       


if __name__ == "__main__":
    filename=sys.argv[1]
    infile = csv.reader(open(filename)) 
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    #tip="magento_test"
    tip="magento_live"
    mg_url = config.get(tip, "mg_url")
    mg_username = config.get(tip, "mg_username")
    mg_password = config.get(tip, "mg_password")
    mail=config.get('mail', "mails")
    outfile = csv.writer(open(str(date.today())+"_orderElectricAvenue.csv", "wb"), delimiter=';',quoting=csv.QUOTE_ALL)
    server = xmlrpclib.ServerProxy(mg_url)
    
    introduction="""
    Please rewrite both areas and keep the HTML structure. 
-For the Title, see if you can add some specification like for example, Original: Sony Cyber-shot DSC-RX100 Digital Camera (Black) Rewrite: Sony Cyber-shot DSC-RX100 Digital Camera 20.2 MP (Black) (maximum 70 characters)
-For the short description please use a similar amount of bullets. 
-For the long description rewrite that content keeping the HTML structure and about  50% of words of the original content. Try to keep technical details, needs to pass copyscape check.

    """
    
    main = Main()
    main.run()


