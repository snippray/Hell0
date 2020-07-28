from fuzzywuzzy import fuzz
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from DBInterface import DB
from Scraper import Scraper
import time

Email = 'mr.developer0111@gmail.com'
Password = 'yqsxdryjgqvuyegz'

# https://myaccount.google.com/lesssecureapps

def compare(exploits,softwares,sysinfo,date,types):
    print('Comparing exploits and system info started...')
    matched_items = []
    for exploit in exploits:
        if exploit['Date'] == date and exploit['TYPE'] in types:
            for software_name in softwares:
                ratio = fuzz.token_set_ratio(software_name[0].lower(),exploit['DESCRIPTION'].lower())
                if ratio>=75 and exploit not in matched_items: 
                    print('Your Software: ' + software_name[0] + ' | Exploit: ' + exploit['DESCRIPTION'] + ' | Ratio:' + str(ratio))
                    matched_items.append(exploit)
            if 'hardware' in types:
                for key,value in sysinfo.items():
                    if key in ['os_name','cpu_name','gpu','bios_name','bios_manufacturer']:
                        ratio = fuzz.token_set_ratio(str(value).lower(),exploit['DESCRIPTION'].lower())
                        if ratio>=75 and exploit not in matched_items: 
                            print('Your System: ' + str(value) + ' | Exploit: ' + exploit['DESCRIPTION'] + ' | Ratio:' + str(ratio))
                            matched_items.append(exploit)
    print('Comparing exploits and system info done!')
    print(str(len(matched_items)) + ' matched item(s) found!')
    return matched_items

# ------------------------------------------------------------------------------------------------------------
def send_mail(server,sender_email,subject,receiver_email,content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html_data = ''
    for item in content:  
        more_info = ''  
        full_title = '<ul><li><h3>{0}</h3><ul>'.format(item['Full title'])
        for key,value in item.items():
            if key == 'link':
                more_info += '<li><p>{0} : <a href=\"{1}\">View</a></p></li>'.format(key,value)
            else:
                more_info += '<li><p>{0} : {1}<p></li>'.format(key,value)
        full_title += more_info + '</ul></li></ul>'
        html_data += full_title

    html = '''
        <!doctype html>
        <html lang="en">
        <body>
        <h2>new exploits of 0day.today</h2>
        {0}
        </body>
        </html>'''.format(html_data)

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    content = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(content)

    # Create secure connection with server and send email
    try:
        server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception:
        print("Can't send mail!")
        return False
# ------------------------------------------------------------------------------------------------------------     
def send_exploits_to_emails(exploits,emails,DB_NAME):
    print('Checking the emails to be sent started...')
    db = DB()
    conn = db.create_connection(DB_NAME)
    email2exploits = dict()
    links2info = dict()
    for email in emails:
        exploits_of_email = []
        for exploit in exploits:
            if not db.link_was_sent_to_email(conn,exploit['Link'],email):
                exploits_of_email.append(exploit['Link'])
                links2info[exploit['Link']] = None
        if len(exploits_of_email)>0:
            email2exploits[email] = exploits_of_email
    
    emails_count = len(email2exploits.keys())
    print('{0} email(s) must be sent!'.format(emails_count)) 

    if emails_count !=0:
        scraper = Scraper()
        print('Scraping exploits information strated!please wait...')
        i=1
        for link in links2info.keys():
            print(str(i) + '/' + str(len(links2info.keys())))
            link_info = scraper.get_exploit_info(link)
            if link_info != {}:
                links2info[link] = link_info
            else:
                links2info.pop(link,None)
            i = i+1
        print('Scraping exploits information done!')
        try:
            print('Sending emails started!please wait...')
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(Email,Password)
                for email,links in email2exploits.items():
                    if send_mail(server,Email,'New exploits of 0day.today',email,[value for key,value in links2info.items() if key in links]):
                        emails_to_db = [[link,email,time.strftime('%d-%m-%Y')] for link in links]
                        db.insert_emails(conn,emails_to_db)
            print('Sending emails done!')
        except Exception:
            print("Can't login to mail server!! Please check your mail server authentication policy!")