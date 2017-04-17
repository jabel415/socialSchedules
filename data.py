import csv
import requests, re
import MySQLdb
import hashlib
import html5lib
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup



class fetchData(object):

    ''' initialize headless browser and navigate to uncc selfservice schedule page '''
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get('https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_dyn_sched')

    def config_payloag(self, term='201780', subj='ACCT'):
        data = [
                ('term_in', term),
                ('call_proc_in', 'bwckctlg.p_disp_dyn_ctlg'),
                ('sel_subj', 'dummy'),
                ('sel_levl', 'dummy'),
                ('sel_schd', 'dummy'),
                ('sel_coll', 'dummy'),
                ('sel_divs', 'dummy'),
                ('sel_dept', 'dummy'),
                ('sel_attr', 'dummy'),
                ('sel_subj', subj),
                ('sel_crse_strt', ''),
                ('sel_crse_end', ''),
                ('sel_title', ''),
                ('sel_levl', '%'),
                ('sel_schd', '%'),
                ('sel_coll', '%'),
                ('sel_divs', '%'),
                ('sel_dept', '%'),
                ('sel_from_cred', ''),
                ('sel_to_cred', ''),
                ('sel_attr', '%'),
                ]
        return data

    def call_server(self, url, method="get", data=None, timeout=10):
        if isinstance(timeout, int):
            try:
                if method == "get":
                    r = requests.get(url, timeout=int(timeout))
                else:
                    if data != None:
                        r = requests.post(url, timeout=int(timeout), data=data)
                    else:
                        return ("Error", "You must post data.")
                if r.status_code == 200:
                    return r.content
                else:
                    return ("Error", r.status_code, r.text)
            except requests.exceptions.Timeout:
                return ("Error", "Timeout reached")
        else:
            return ("Error", "Timeout must be an integer")

    def get_search_page(self, term):
        self.dropDown = Select(self.driver.find_element_by_id('term_input_id'))
        self.dropDown.select_by_value(term)
        submit = self.driver.find_element_by_xpath('/html/body/div[3]/form/input[2]').click()
        parser = BeautifulSoup(self.driver.page_source, 'html5lib')
        return parser

    def get_courses_page(self, term, subj):
        page_html = self.call_server('https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_display_courses', method='post', data=self.config_payloag(term=term, subj=subj), timeout=20)
        #parser = self.parse_html(page_html)
        parser = BeautifulSoup(page_html, 'html5lib')
        return parser

    def get_subjects(self, term, subj):
        subjects = {}
        subject_html = self.get_courses_page(term, subj)
        #subject_html = self.call_server('https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_display_courses', method='post', data=self.config_payloag(term=term, subj=subj), timeout=20)
        #subject_html = BeautifulSoup(subject_html, 'html5lib')
        for option in subject_html.find(id="subj_id").find_all('option'):
            subjects[str(option['value'])] = str(option.text)
        return subjects

    def get_courses(self, term, subj):
        courses = {}
        #subjects = self.get_subjects(term, subj)
        #for key, val in sorted(subjects.items()):
        courses_html = self.get_courses_page(term, subj)
        for course in courses_html.find_all('td', class_='nttitle'):
            course_num = course.text.split()[1]
            course_title = ' '.join(course.text.split()[3:])
            courses[course_num] = course_title
        return courses

    def get_sections(self, term, subj):
        def search(subj, course_num):
            subjSelect = Select(self.driver.find_element_by_xpath('//*[@id="subj_id"]'))
            subjSelect.select_by_value(subj)
            self.driver.find_element_by_xpath('//*[@id="crse_id"]').send_keys(course_num)
            self.driver.find_element_by_xpath('/html/body/div[3]/form/input[12]').click()
        available_subj = []
        sections = {}
        courses = {}
        search_page = self.get_search_page(term)
        for option in search_page.find(id="subj_id").find_all('option'):
            available_subj.append(str(option['value']))
        subjects = self.get_subjects(term, subj)
        for key, val in (subjects.items()):
            not_available = False
            if key not in available_subj:
                not_available = True
                break
            if not_available:
                continue

            courses = self.get_courses(term, key)
            for k, v in courses.iteritems():
                search(key, k)
                parser = BeautifulSoup(self.driver.page_source, 'html5lib')

                no_results = False
                # Check if no results found page
                for head in parser.find_all('td', class_='pldefault'):
                    header = head.text.encode('utf-8')
                    if header == '\nNo classes were found that meet your search criteria\n\n':
                        self.driver.find_element_by_xpath('/html/body/div[3]/table[2]/tbody/tr/td/a').click()
                        no_results = True
                        break
                if no_results:
                    continue

                for section in parser.find_all('th'):
                    header = section.text.encode('utf-8').split( ' - ')
                    print header
                    #course_name = header[0]
                    #crn = header[1]
                    # TODO further pasing of sections if found in search

    ''' navigate through selfservice site to get course information for every subject for any passed in term (semester) '''
    def getCourses(self, term='201750'):
        subjects = {}
        courseData = []
        self.dropDown = Select(self.driver.find_element_by_id('term_input_id'))
        # Select semester
        self.dropDown.select_by_value(term)
        submit = self.driver.find_element_by_xpath('/html/body/div[3]/form/input[2]').click()
        pageHTML = BeautifulSoup(self.driver.page_source, 'html.parser')
        for option in pageHTML.find(id="subj_id").find_all('option'):
            subjects[str(option['value'])] = str(option.text)
        for key, val in sorted(subjects.items()):
            if str.isalpha(key) and len(key) == 4:

                subjSelect = Select(self.driver.find_element_by_xpath('//*[@id="subj_id"]'))
                subjSelect.select_by_value(key)
                self.driver.find_element_by_xpath('/html/body/div[3]/form/input[12]').click()
                source = self.driver.page_source
                pageHTML = BeautifulSoup(self.driver.page_source, 'html.parser')
                z=0
                a=0

                for course in pageHTML.find_all('th'):
                    header = ((course.text))#.split(' - '))
                #    #courseData.append([header])

        #        for info in pageHTML.find_all('td', class_='dddefault'):
        #            rows = info.find_all('td')
        #            rows = [elem.text for elem in rows]
        #            if len(rows) > 0:
        #                rows = [x.encode('UTF-8') for x in rows]
        #                courseData[z][a].append(rows)
        #                z+=1
        #        self.driver.find_element_by_link_text('Return to Previous').click()
        # return array of every course holding
        #return courseData
        ''' courseData[x] = [['Principles of ACCT I', '30011', 'ACCT 2121', '001'],['Class', '8:00 am - 9:30 am', 'MTWRF', 'Friday 116', 'May 22, 2017 - Jun 26, 2017', 'Lecture', 'Shirley Alyce  Hunter (P)']] '''

    def csvOut(self):
        myfile = open('data.csv', 'wb')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for x in self.getCourses():
            wr.writerow(x)

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

class dbConnect(object):

    def __init__(self):
        self.db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="8sg0e$yF",
                                  db="smart_schedules")
        self.cursor = self.db.cursor()

    def is_user(self, email):
        val = self.cursor.execute("SELECT COUNT(*) FROM users WHERE email=%s", (email))
        return bool(val)

    def create_user(self, f_name, l_name, student_id, email, password, is_ninernet, major="", concentration="", yr_num=1, picture="", notes=""):
        if not self.is_user(email):
            cpassword = ""
            pass_md5 = hashlib.md5(password).hexdigest()
            self.cursor.execute("INSERT INTO users(firstName, lastName, studentID, email, password, cpassword, major, class_year, concentration, picture_url, is_ninernet, notes)" \
                                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (f_name, l_name, student_id, email, pass_md5, cpassword, major, yr_num, concentration, picture, is_ninernet, notes))
            return True
        else:
            return False

    def get_user_by_email(self, email):
        if self.is_user(email):
            user_info = self.cursor.execute("SELECT * FROM users WHERE email=%s", (email))
            return user_info
        else:
            return False

    #def authenticate(self, email, password):
    #    if self.is_user(email):


    '''
    def dbConnect(self):
        control = connection.cursor()
        courseData = self.getCourses()
        for x in range(0, len(courseData)):
            course = {
                'crn': courseData[x][1],
                'course_name': courseData[x][0],
                'subject': courseData[x][2],  # Strip crn from string
                'course_num': courseData[x][2],  # String crn from string
                'credits': '',  # TODO get credit data
                'course_title': courseData[x][2],
                'start_date': courseData[x][0],
                'end_date': courseData[x][0],
                'start_time': '',
                'end_time': '',
                'days': '',
                'instructor_name': '',
                'location': '',
                'year': '',
                'semester': '',
                'seat_capacity': '',
                'seat_accounted': '',
                'seats_remaining': '',
                'instructors_id': ''
            }
        return control
        '''





test = fetchData()
test.get_sections(term='201780', subj='')
#test.call_server('https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_display_courses', method='post', data=test.config_payloag(term='201780', subj=''), timeout=20)

#test.getSeatsByCrn()