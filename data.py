import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup



class Data(object):

    ''' initialize headless browser and navigate to uncc selfservice schedule page '''
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get('https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_dyn_sched')

    # TODO
    ''' connect to postgresql database '''
    def dbConnect(self):
        return

    ''' navigate through selfservice site to get course information for every subject for any passed in term (semester) '''
    def getCourses(self, term='201750'):
        subjects = {}
        courseData = []
        self.dropDown = Select(self.driver.find_element_by_id('term_input_id'))
        # self.dropDown.select_by_value('201750')
        self.dropDown.select_by_value(term) # First Summer 2017, using this as our proof of concept data for now
        submit = self.driver.find_element_by_xpath('/html/body/div[3]/form/input[2]').click()
        pageHTML = BeautifulSoup(self.driver.page_source, 'html.parser')
        for option in pageHTML.find(id="subj_id").find_all('option'):
            subjects[str(option['value'])] = str(option.text)
        for key, val in sorted(subjects.items()):
            if str.isalpha(key) and len(key) == 4:
                subjSelect = Select(self.driver.find_element_by_xpath('//*[@id="subj_id"]'))
                subjSelect.select_by_value(key) #change to key when in loop
                self.driver.find_element_by_xpath('/html/body/div[3]/form/input[12]').click()
                pageHTML = BeautifulSoup(self.driver.page_source, 'html.parser')
                z=0
                for course in pageHTML.find_all('th', class_='ddtitle'):
                    header = ((course.text).split(' - '))
                    courseData.append([header])
                for info in pageHTML.find_all('td', class_='dddefault'):
                    rows = info.find_all('td')
                    rows = [elem.text for elem in rows]
                    if len(rows) > 0:
                        rows = [x.encode('UTF-8') for x in rows]
                        courseData[z].append(rows)
                        z+=1
                self.driver.find_element_by_link_text('Return to Previous').click()
        # return array of every course holding
        return courseData
        ''' courseData[x] = [['Principles of ACCT I', '30011', 'ACCT 2121', '001'],['Class', '8:00 am - 9:30 am', 'MTWRF', 'Friday 116', 'May 22, 2017 - Jun 26, 2017', 'Lecture', 'Shirley Alyce  Hunter (P)']] '''

    ''' get seat data per crn '''
    def getSeatsByCrn(self, crn='40005', term='201770'):
        seats = []
        r = requests.get('https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_detail_sched?term_in=' + term + '&crn_in=' + crn)
        pageHTML = BeautifulSoup(r.text, 'html.parser')
        for row in pageHTML.find_all('td', class_='dddefault', text=re.compile(r'[0-9]{0,4}')):
            seats.append(row.text)
        return seats
    '''
        seats[0] - capacity
        seats[1] - actual
        seats[2] - remaining
        seats[3] - waitlist capacity
        seats[4] - waitlist actual
        seats[5] - waitlist remaining
    '''

    # TODO
    ''' get data for every professor from ratemyprofessor.com '''
    def getProfRating(self, prof):
        return


test = Data()
#test.getCourses()
test.getSeatsByCrn()