from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from time import strftime, gmtime
from login import *
from email.message import EmailMessage
import smtplib
import time
from huawei_lte_api.enums.client import ResponseEnum

def  SendMail(contenct):
    email_subject = "Alert from Huawei router"
    sender_email_address = "kusinczky@gmail.com"
    receiver_email_address = "info.kusinczky@gmail.com"
    email_smtp = "smtp.gmail.com"
    email_password = "ictr yglk eldq yxrb"
    
    # create an email message object
    message = EmailMessage()  
    # open image as a binary file and read the contents
    # with open(fileName, 'rb') as file:
    #     image_data = file.read()
  
    message.set_content(contenct)
    # attach image to email
    #message.add_attachment(image_data, maintype='image',subtype='jpg', filename=fileName)
  

    # configure email headers
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
 
    try:
        # create an SMTP client session object    
        server = smtplib.SMTP(email_smtp, '587')
        # identify this client to the SMTP server
        server.ehlo()
        # secure the SMTP connection
        server.starttls()
        server.login(sender_email_address, email_password)
        # login to email account
        # send email
        server.send_message(message)
        # close connection to server
        server.quit()
    except Exception as e:
        print(str(e) + strftime(" - EMAIL - %Y-%m-%d %H:%M:%S", gmtime()))
      


# with Connection('http://192.168.8.1/') as connection: For limited access, I have valid credentials no need for limited access
temp=''
while True:    
    try:
        with Connection(f'http://{ip}/', login, password) as connection:
            client = Client(connection)
            if (temp != client.device.information().get('WanIPAddress')):
                temp=client.device.information().get('WanIPAddress')
                SendMail("WanIPAdress is changed. "+ temp + strftime(" - %Y-%m-%d %H:%M:%S", gmtime()))
                print(str(client.device.signal().get('cell_id')))
                print(temp)
            if client.device.signal().get('cell_id') == None:
                print("Internet is down. Devices is rebooting. " + strftime(" - %Y-%m-%d %H:%M:%S", gmtime()))
                client.device.reboot()
                SendMail("Internet is down. Devices is rebooting. " + strftime(" - %Y-%m-%d %H:%M:%S", gmtime()))            
                time.sleep(120) 
            connection.close()
            time.sleep(300)
    except Exception as e:       
        print(str(e) + strftime(" - %Y-%m-%d %H:%M:%S", gmtime()))
        SendMail("Alert. "+ str(e) + strftime(" - %Y-%m-%d %H:%M:%S", gmtime()))
        time.sleep(180)
    
        