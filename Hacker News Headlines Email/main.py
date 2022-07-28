from http import server
from xmlrpc.client import Server
import requests #http requests
from decouple import config

FROM = config('EMAIL')
PASS = config('PASSWORD')

from bs4 import BeautifulSoup #web scraping 
#Send the mail
import smtplib
#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

#system date and time manipulation
import datetime
now  = datetime.datetime.now()

#email content placeholder
content = ''

def extract_news(url):
    print('Extracting Hacker News Stories...')
    ctn = ''
    ctn += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign':''})):
        ctn += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text != 'More' else '')
    return ctn

ctn = extract_news('https://news.ycombinator.com/')
content += ctn
content += ('<br>------<br>')
content += ('<br><br> End of Message')

#Lets send the email

print('Composing Email...')

#Update your email details

SERVER = 'smtp.gmail.com' #"your smtp server"
PORT = 587 #your port number
TO = 'mosesbuta123@gmail.com' # "your to eamil ids"  # can be a list

#fp = open(file_name, 'rb')
#Create a text/plain message
#msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.text')
msg['Subject'] = 'Top News | Stories HN [Automated Email]' + ' '+ str(now.day)+ '-'+ str(now.month) + '-'+ str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
#fp.close()

print('Initiating Server...')
server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')
server.quit()