from huawei_lte_api.Client import Device
from huawei_lte_api.AuthorizedConnection import Connection
from time import strftime, gmtime
from login import *
from email.message import EmailMessage
import smtplib
import time
import subprocess

def  SendMail(contenct):
    email_subject = "Alert from Huawei router"
    sender_email_address = "kusinczky@gmail.com"
    receiver_email_address = "info.kusinczky@gmail.com"
    email_smtp = "smtp.gmail.com"
    email_password = "oarc pdfs lkgy zuqo"
    
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
 
    # set smtp server and port
    server = smtplib.SMTP(email_smtp, '587')
    # identify this client to the SMTP server
    server.ehlo()
    # secure the SMTP connection
    server.starttls()
    
    # login to email account
    server.login(sender_email_address, email_password)
    # send email
    server.send_message(message)
    # close connection to server
    server.quit()


# with Connection('http://192.168.8.1/') as connection: For limited access, I have valid credentials no need for limited access
connection = Connection(f'http://{ip}/', login, password)
device = Device(connection)
temp=device.information().get('WanIPAddress')
while True:    
    try:       
        if (temp != device.information().get('WanIPAddress')):  
            temp=device.information().get('WanIPAddress')
            SendMail("WanIPAdress is changed. "+ temp + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print(str(device.signal().get('cell_id')))
        print(temp)
        if device.signal().get('cell_id') == None:
            print("Internet is down. Devices is rebooting. " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            device.reboot()
            SendMail("Internet is down. Devices is rebooting. " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))            
            time.sleep(60)  
        time.sleep(60)  
    except Exception as e:
        if(subprocess.check_output(["ping", "-c", "1", "http://{ip}/"])):
            connection = Connection(f'http://{ip}/', login, password)
            device = Device(connection)
        time.sleep(60)
        