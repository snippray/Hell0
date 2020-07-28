import socks
import socket
from mechanize import Browser
from mechanize import HTTPError,URLError,BrowserStateError,FormNotFoundError
from bs4 import  BeautifulSoup

class Scraper:

    def __init__(self):
        self.socks_proxy_host = '127.0.0.1'
        self.socks_proxy_port = 9150
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,self.socks_proxy_host,self.socks_proxy_port)
        socket.socket = socks.socksocket
        socket.create_connection = self.create_connection

    def create_connection(self,address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock

    def scrape(self,url):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        try:
            br.open(url)
            br.select_form(nr=0)
            resp=br.submit(name="agree",label="Yes, I agree")
            soup = BeautifulSoup(resp.read(),'html.parser')
            Exploits = []
            exploit_table_contents = soup.find_all('div',{'class':'ExploitTableContent'})
            for item in exploit_table_contents:
                exploit = {}
                tds = item.find_all('div',{'class':'td'})
                exploit['Date'] = tds[0].text
                exploit['DESCRIPTION'] = tds[1].find('a').text
                exploit['Link'] = 'http://mvfjfugdwgc5uwho.onion'+tds[1].find('a')['href']
                exploit['TYPE'] = tds[2].text
                exploit['HITS'] = tds[3].text
                exploit['GOLD'] = tds[9].text.replace('\t','')
                exploit['AUTHOR'] = tds[10].find('a').text
                Exploits.append(exploit)
            return Exploits
        except (HTTPError,URLError,BrowserStateError,FormNotFoundError) as e:
            print(e)
            return []


    def get_exploit_info(self,url):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        try: 
            br.open(url)
            br.select_form(nr=0)
            resp=br.submit(name="agree",label="Yes, I agree")
            soup = BeautifulSoup(resp.read(),'html.parser')
            exploit_view_table = soup.find_all('div',{'class':'exploit_view_table_content'})
            exploit_info = {}
            exploit_info['link'] = url
            for item in exploit_view_table:
                tds = item.find_all('div',{'class':'td'})
                if(tds[0].text == 'Full title'):
                    exploit_info[tds[0].text] = tds[1].find('a').text
                else:
                    exploit_info[tds[0].text] = tds[1].text

            return exploit_info
        except (HTTPError,URLError,BrowserStateError,FormNotFoundError) as e:
            print(e)
            return {}