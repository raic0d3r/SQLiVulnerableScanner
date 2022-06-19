import re, requests, os, sys
import html, urllib.request, urllib.error
import socket, socks, urllib.parse 
from time import time as timer  
from multiprocessing.dummy import Pool
from pathlib import Path
from colorama import Fore                               
from colorama import Style
from stem import Signal
from stem.control import Controller
from urllib import parse

#from web import web
####### Colors   ###### 
fr  =   Fore.RED                                            
fc  =   Fore.CYAN                                           
fw  =   Fore.WHITE                                          
fg  =   Fore.GREEN                                          
sd  =   Style.DIM                                           
sn  =   Style.NORMAL                                        
sb  =   Style.BRIGHT
                                        
#######################

def banners():
    try:
        os.mkdir('logs')
    except:
        pass
        
    banner = """{}

                   ...          
                 ;::::;           ::
               ;::::; :;        :::::: 
              ;::::;  :;   SQLi Scanner
             ;:::::'   :;     By RaiC0d3r
            ;:::::;     ;.
           ,:::::'       ;           OOO\
           ::::::;       ;          OOOOO\{}
           ;:::::;       ;         OOOOOOOO
          ,;::::::;     ;'         / OOOOOOO
        ;:::::::::`. ,,,;.        /  / DOOOOOO
      .';:::::::::::::::::;,     /  /     DOOOO
     ,::::::;::::::;;;;::::;,   /  /        DOOO
    ;`::::::`'::::::;;;::::: ,#/  /          DOOO
    :`:::::::`;::::::;;::: ;::#  /            DOOO  {}
    ::`:::::::`;:::::::: ;::::# /              DOO
    `:`:::::::`;:::::: ;::::::#/               DOO
     :::`:::::::`;; ;:::::::::##                OO
     ::::`:::::::`;::::::::;:::#                OO
     `:::::`::::::::::::;'`:;::#                O
      `:::::`::::::::;' /  / `:#
       ::::::`:::::;'  /  /   `#                                                                                            

        \n""".format(fg, fr, fg, sn)
        
    print(banner)

sql_errors = {
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server"),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
    "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string", r"Microsoft OLE DB Provider for ODBC Drivers"),
    "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r".*Syntax error.*query expression"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
    "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
    "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
    "Sybase": (r"Warning.*sybase.*", r"Sybase message")
}

Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

def check(html):
    """check SQL error is in HTML or not"""
    for db, errors in sql_errors.items():
        for error in errors:
            if re.compile(error).search(html):
                #print "\n" + db
                return True, db
    return False, None
    
def getoption():
    url = input("\n\033[92m[!]\033[91m ENTER WEBSITE (Ex: evil.com): ")
    start = timer()
    singlescan(url)
    print('Finished in : ' + str(timer() - start) + ' seconds')
    print("\n")


def singlescan(url):
    print("\n{}[+] Vulnerability: SQLi{}\n".format(fg, sn))
    print("{}{}Finding SQLi entry points in the domain...{}\n\n".format(sn, fc, sn))
    Req = urllib.request.urlopen('http://web.archive.org/cdx/search/cdx?url=*.'+url+'/*&output=html&fl=original&collapse=urlkey', timeout=10).read().decode("utf8").splitlines()
    for url in Req:
        print("{}{}[]==> {}{}\n\n" .format(sn, fc, url, sn))
        if re.search('(.*?)(.php\?|.asp\?|.apsx\?|.jsp\?)(.*?)=(.*?)', url):
            print("{}{}[😍]Checking if the entry points are vulnerable...{}\n\n" .format(sn, fc, sn))
            #print("{}{}[]==> {}{}\n\n" .format(sn, fc, url, sn))
            scanner(url)
            #Threads = ThreadPool.map(scanner, url)
        else:
            print("{}{}[😞]Not Found SQLi entry points in the domain...{}\n\n" .format(sn, fc, sn))



def scanner(url):
    try:
        payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
        for payload in payloads:
            website = url + payload
            source = urllib.request.urlopen(website).read()
            mystr = source.decode("utf8")
            #source = html.unescape(r.text)
            if mystr:
                vulnerable, db = check(mystr)
                if vulnerable and db != None:
                    print("\n{}[✓] Vulnerable =>{}{}\n".format(fg, website, sn))
                    open('SQLiVulnerable.txt', 'a').write(website+'\n')
                    
    except urllib.error.URLError:
        pass

    except urllib.error.HTTPError:
        pass        

    except KeyboardInterrupt:
        raise KeyboardInterrupt

    except:
        pass

banners()
getoption()
