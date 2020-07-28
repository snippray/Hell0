from Systeminfo import SystemInfo
from DBInterface import DB
from Scraper import Scraper
import argparse
import textwrap
import time
from Utils import *

# ------------------------------------------------------------------------------------------------------------        
if __name__=="__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''
                                                    ----------------------------------------------
                                                    With this software you can extract your system
                                                    hardware and software information and find last
                                                    exploits related to your system.
                                                    ----------------------------------------------
                                                    '''))
    parser.add_argument('-db','--dbname',type=str, action='store', help="databse file name ,usage: -c <databasename.db>")
    parser.add_argument('-u','--update', action='store_true', help="update system information in database file")
    parser.add_argument('-s','--show', action='store_true', help="show your system softwares/hardwares information")
    parser.add_argument('-w','--windows', action='store_true', help="find windows exploits")
    parser.add_argument('-hw','--hardware', action='store_true', help="find hardware exploits")
    parser.add_argument('-m','--multiple', action='store_true', help="find multiple exploits")
    parser.add_argument('-d','--date', action='store',default=time.strftime('%d-%m-%Y'), help="find exploits of this date,usage: -d "+time.strftime('%d-%m-%y'))
    parser.add_argument('-e','--emails', action='store', help="emails list text file name, usage: -e emails.txt")

    

    args = parser.parse_args()
    date = args.date
    types = []

    if args.windows:
        types.append('windows')
        types.append('win32')
    if args.hardware:
        types.append('hardware')
    if args.multiple:
        types.append('multiple')

    if args.dbname:
        DB_NAME = args.dbname
        if args.update:
            print('DB updating started...\n'+'-'*50)
            print('Finding system information started...\n'+'-'*50)
            sysinfo = SystemInfo()
            db = DB()
            conn = db.create_connection(DB_NAME)
            db.create_tables(conn,DB_NAME)
            system_id = db.insert_system_info(conn,sysinfo.host_name,sysinfo.os_name,sysinfo.os_architecture,sysinfo.os_version,
                                                sysinfo.cpu_name,sysinfo.cpu_cores,str(sysinfo.gpu),sysinfo.bios_name,sysinfo.bios_version,sysinfo.bios_manufacturer)
            print('Saving system information into DB done!\n'+'-'*50)
            if system_id is not None:
                print('Finding system softwares information started,please wait...\n'+'-'*50)
                softwares = sysinfo.get_system_softwares()
                print('Finding system softwares information Done!\n'+'-'*50)
                for item in softwares:
                    item.append(system_id)
                db.insert_softwares(conn,softwares)
                print('Saving system softwares information into DB done!\n'+'-'*50)
            conn.close()
        if args.emails:
            with open(args.emails,'r+') as f:
                emails = f.readlines()
            if args.windows or args.hardware or args.multiple:
                db = DB()
                conn = db.create_connection(DB_NAME)
                softwares = db.select_softwares_name(conn)
                sysinfo = SystemInfo()
                if args.show:
                    attrs = vars(sysinfo)
                    print('Here is Your System Hardware Information:\n'+'-'*50)
                    print('\n'.join("%s: %s" % item for item in attrs.items()))
                    print('Here is Your System Softwares Information:\n'+'-'*50)
                    print('\n'.join("%s" % item for item in softwares))                    
                conn.close()
                if len(softwares)==0:
                    print('System softwares not found! Add -u to the previous command\n'+'-'*50)
                else:
                    scraper = Scraper()
                    print('Finding exploits started,please wait...\n'+'-'*50)
                    url = 'http://mvfjfugdwgc5uwho.onion/date/{0}'.format(date)
                    exploits = scraper.scrape(url)
                    if len(exploits)>0:
                        print('Founded Exploits:\n'+'-'*50)
                        for item in exploits:
                            print(item['DESCRIPTION'] + '| Type: ' + item['TYPE'])
                        print('Finding exploits done!\n'+'-'*50)
                        matched_exploits = compare(exploits,softwares,vars(sysinfo),date,types)
                        send_exploits_to_emails(matched_exploits,emails,DB_NAME)
        else:
            print('Error!Enter emails text file name,usage: -e emails.txt\n'+'-'*50)
    else:
        print('Error!Enter database file name,usage: -db <databasename.db>\n'+'-'*50)