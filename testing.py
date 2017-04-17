import requests
import urllib
from bs4 import BeautifulSoup


r = requests.get('https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_dyn_sched')
payload1 = {'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
           'p_term': '201710'}

'''term_in=201780&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy
&sel_subj=ACCT&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_attr=%25&begin_hh=0&begin_mi=0&
begin_ap=a&end_hh=0&end_mi=0&end_ap=a'''

term='201780'
subj = 'ACCT'

'''data = {
    'term_in': term,
    'sel_subj': 'dummy',
    #'sel_day': 'dummy',
    'sel_schd': 'dummy',
    #'sel_insm': 'dummy',
    #'sel_camp': 'dummy',
    'sel_levl': 'dummy',
    'sel_coll': 'dummy',
    'sel_divs': 'dummy',
    'sel_dept': 'dummy',
    #'sel_sess': 'dummy',
    #'sel_instr': 'dummy',
    #'sel_ptrm': 'dummy',
    'sel_attr': 'dummy',
    'sel_subj': subj,
    'sel_crse_strt': '',
    'sel_crse_end': '',
    'sel_title': '',
    'sel_schd': '%',
    'sel_levl': '%',
    'sel_coll': '%',
    'sel_divs': '%',
    'sel_dept': '%',
    #'sel_insm': '%',
    'sel_from_cred': '',
    'sel_to_cred': '',
    #'sel_camp': '%',
    #'sel_levl': '%',
    #'sel_ptrm': '%',
    'sel_attr': '%',
    #'begin_hh': '0',
    #'begin_mi': '0',
    #'begin_ap': 'a',
    #'end_hh': '0',
    #'end_mi': '0',
    #'end_ap': 'a',
    'call_proc_in': 'bwckctlg.p_disp_dyn_ctlg'
        }'''

data=[('term_in','201780'),
('call_proc_in', 'bwckctlg.p_disp_dyn_ctlg'),
('sel_subj','dummy'),
('sel_levl','dummy'),
('sel_schd','dummy'),
('sel_coll','dummy'),
('sel_divs','dummy'),
('sel_dept','dummy'),
('sel_attr','dummy'),
('sel_subj', ''),#'ACCT'),
('sel_crse_strt',''),
('sel_crse_end',''),
('sel_title',''),
('sel_levl','%'),
('sel_schd','%'),
('sel_coll','%'),
('sel_divs','%'),
('sel_dept','%'),
('sel_from_cred',''),
('sel_to_cred',''),
('sel_attr','%'),
]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Host': 'selfservice.uncc.edu',
    'Origin': 'https://selfservice.uncc.edu',
    'Referer': 'https://selfservice.uncc.edu/pls/BANPROD/bwckgens.p_proc_term_date'
}

cookie = {'__cfduid': 'd8901f6820826fc9d17d8c020532f5c4e1480365574',
          '__unam': 'a49b7f5-158b9c9bab6-5214072d-8',
          '__utma': '71266260.157634453.1480360556.1488237453.1490754888.6',
          '__utmz': '71266260.1490754888.6.6.utmcsr=library.uncc.edu|utmccn=(referral)|utmcmd=referral|utmcct=/',
          'accessibility': 'false',
          '_ga': 'GA1.2.157634453.1480360556'}

def call_server(url, method="get", data=None, timeout=10):
    if isinstance(timeout, int): #checks to see whether timeout is an integer
        try:
            if method == "get":
                r = requests.get(url, timeout=int(timeout))
            else:
                if data != None:
                    r = requests.post(url, timeout=int(timeout), data=data)
                else:
                    return ("Error", "You must post data.")
            if r.status_code == 200:
                pageHTML = BeautifulSoup(r.text, 'html.parser')
                return pageHTML

            else:
                return ("Error", r.status_code, r.text)
        except requests.exceptions.Timeout:
            return ("Error", "Timeout reached")
    else:
        return ("Error", "Timeout must be an integer")

#print call_server('https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_display_courses', method='post', data=data, timeout=20)

a = ['asd', 'dawd', 'dawdawdad']
b = 'asd'
if b in a:
    print 'Match'