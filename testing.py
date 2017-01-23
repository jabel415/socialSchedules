import requests

r = requests.get('https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_dyn_sched')
payload1 = {'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
           'p_term': '201710'}
print r