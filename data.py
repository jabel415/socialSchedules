from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

# TODO doConnect, rateMyProf, seatsInfo

class Data(object):

    # intiate headless browser and navigate to uncc selfservice schedule page
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get('https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_dyn_sched')

    def getCourses(self):
        self.dropDown = Select(self.driver.find_element_by_id('term_input_id'))
        # TODO replace with parsed terms
        self.dropDown.select_by_value('201750') # First Summer 2017, using this as our proof of concept data for now
        submit = self.driver.find_element_by_xpath('/html/body/div[3]/form/input[2]').click()
        pageHTML = BeautifulSoup(self.driver.page_source, 'html.parser')
        subjects = {}
        # TODO precondition that only looks at letter based option to only select course subjects
        for option in pageHTML.find_all('option'):
            subjects[str(option['value'])] = str(option.text)

        #for key, val in subjects.items():
        #    if str.isalpha(key) and len(key) == 4:
                #print key, val
        subjSelect = Select(self.driver.find_element_by_xpath('//*[@id="subj_id"]'))
        subjSelect.select_by_value('ACCT') #change to key when in loop
        self.driver.find_element_by_xpath('/html/body/div[3]/form/input[12]').click()
        pageHTML = BeautifulSoup(self.driver.page_source, 'html.parser')
        # TODO change from dictionary to array
        courseData = {}
        for course in pageHTML.find_all('th', class_='ddtitle'):
            header = (str(course.text).split(' - '))
            ''' print header - ['Principles of ACCT I', '30011', 'ACCT 2121', '001'] '''
            courseData['title'] = header[0]
            courseData['crn'] = header[1]
            courseData['course'] = header[2]
            courseData['section'] = header[3]

        for info in pageHTML.find_all('td', class_='dddefault'):
            rows = info.find_all('td')
            rows = [elem.text for elem in rows]
            if len(rows) > 0:
                rows = [x.encode('UTF-8') for x in rows]
                ''' print rows - ['Class', '8:00 am - 9:30 am', 'MTWRF', 'Friday 116', 'May 22, 2017 - Jun 26, 2017', 'Lecture', 'Shirley Alyce  Hunter (P)'] '''
                courseData['type'] = rows[0]
                courseData['time'] = rows[1]
                courseData['days'] = rows[2]
                courseData['location'] = rows[3]
                courseData['dateRange'] = rows[4]
                courseData['scheduleType'] = rows[5]
                courseData['instructor'] = rows[6]

                # TODO print testing
        #for key, val in courseData.iteritems():
        #    print key, val
        #print pageHTML.prettify()


test = Data()
test.getCourses()
