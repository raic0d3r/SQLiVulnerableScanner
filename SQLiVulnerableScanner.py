import re, requests, os, sys
from time import time as timer	
from multiprocessing.dummy import Pool
from pathlib import Path
from colorama import Fore								
from colorama import Style
####### Colors	 ######	
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
        os.mkdir('CMS')
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


def getoption():
    url = input("{}[1]{} ENTER WEBSITE : ".format(fg, fw))
    print("\n{}[+] Vulnerability: SQLi{}\n".format(fg, sn))
    print("{}{}Finding SQLi entry points in the domain...{}\n\n".format(sn, fc, sn))
    os.system("gau "+url+"| gf sqli | tee sqli_paramaters.txt")
    print("\n")
    print("{}{}Checking if the entry points are vulnerable...{}\n\n" .format(sn, fc, sn))
    os.system("sqlmap -m sqli_paramaters.txt -v 3 --batch --random-agent --level 5 --risk 3 | tee -a sqli.txt")

def installreq():
    print("\n{}[+] Installing Requirement{}\n".format(fg, sn))
    os.system("sudo su")
    os.system("go install github.com/tomnomnom/gf@latest && go install github.com/lc/gau@latest")
    os.system("cp ~/go/bin/gau /usr/bin && cp ~/go/bin/gf /usr/bin/")
    print("\n{}Installed Done{}\n".format(fg, sn))
    os.system("git clone https://github.com/Sherlock297/gf_patterns.git && cd gf_patterns/ && cp *.json ~/.gf")
    getoption()

banners()
path_to_file = '/usr/bin/gau'
path_to_file1 = '/usr/bin/gf'
path = Path(path_to_file)
path1 = Path(path_to_file1)

if path.is_file() & path1.is_file():
    print(f'The file {path_to_file} & {path_to_file1} exists')
    getoption()
else:
    print(f'The file {path_to_file} & {path_to_file1} does not exist')
    installreq()
