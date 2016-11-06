import email
import email.mime.application
import smtplib

import yaml

'''This is a module  receives an email address and auto send email with CV file both in pdf and word formats.
    The input argument is a path to yaml configuration file, where all mail settings are written.'''


def handleMail(receiver):
    if(len(receiver) == 0):
        print 'no mail!'
        return
    config = readConfig()
    msg = createMail(receiver, config)
    attachFile(config['word']['path'], config['word']['fname'], config['word']['ext'], msg)
    attachFile(config['pdf']['path'], config['pdf']['fname'], config['pdf']['ext'], msg)
    sendMail(config["mail_auth"]['email'], receiver, config["mail_auth"]['password'], msg)

#take argument from user as the path to find yaml configuration file
def readConfig():
    with open("C:\Users\Mirit\PycharmProjects\FBScraper\FBScraper\config.yml", 'r') as f:
        config = yaml.load(f)
        return config

def createMail(receiver, config):
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = config["mail_content"]['subject']
    msg['From'] = config["mail_auth"]['email']
    msg['To'] = receiver
    msg['Bcc'] = config["mail_auth"]['bcc']
    body = email.mime.Text.MIMEText(config["mail_content"]['content'])
    msg.attach(body)
    print 'attached mail body '
    return msg

#generic function to attach file of some type to the mail
def attachFile(filePath, filename, fileType, msg):
    with open(filePath, 'rb') as fp:
        att = email.mime.application.MIMEApplication(fp.read(), _subtype=fileType)
        fp.close()
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(att)
        print 'finished reading' + fileType
        return msg

def sendMail(sender, receiver, password, msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender, [receiver], msg.as_string())
    server.quit()
    print 'sent :-)'
