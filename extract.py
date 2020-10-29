import requests
import config
from lxml import html
from bs4 import BeautifulSoup
import re

''' get all of students inforamtion from elearning...'''

# get {authenticity_token} from first page of elearning site for login
session_requests = requests.session()

login_url = "https://elearning.hsu.ac.ir/login/index.php/"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]

# start the login
# get username and password for login {test}

payload = {
	"username": config.username, 
	"password": config.password, 
	"logintoken": authenticity_token
}

result = session_requests.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
)
# login done

url = 'https://elearning.hsu.ac.ir/my/index.php?lang=en'
result = session_requests.get(
	url, 
	headers = dict(referer = url)
)

# start scraping the web by beautiful soup {bs4}


soup = BeautifulSoup(result.content, 'html.parser')
print(result.status_code)

# # print title
# print('title is : ', soup.title.string, sep=" ")

# # print username
user = soup.find("span", attrs={"class": "usertext mr-1"}).contents[0]
print('سلام ',user ,sep=" ")
# # print online user
# print('online users >>>>>>')
# online_user = soup.findAll('div', {'class': "user"})

# for i in online_user:
#     print(i.find('img').next_sibling)

''' start extract informaiton of lessons and students '''

for link in soup.find_all('a', {"class" : "list-group-item list-group-item-action", "data-parent-key" : "mycourses"}):
    url = link.get('href')
    print("lesson url: ", url)
    result = session_requests.get(url, headers = dict(referer = url))
    soup = BeautifulSoup(result.content, 'html.parser')

    # Get the name of each lesson
    header = soup.find('div', {'class' : 'page-context-header'}).h1.get_text()
    print("name of lesson : ", header)

    # Get link of students page
    participants_link = soup.find('a', {"data-key" : "participants"}).get('href')
    print("participants_link : ", participants_link)

    ### start the Get all students
    result = session_requests.get(participants_link, headers = dict(referer = participants_link))
    soup = BeautifulSoup(result.content, 'html.parser')
    
    # Get number of student in the class
    participant_count = int(soup.find('div', {"class" : "userlist"}).p.get_text().strip('تعداد شرکت‌کنندگان : '))
    print("participant : ", participant_count)

    # Get currect page of all students in the current class
    showall = soup.find('div', {'id':'showall'})
    if showall:
        all_students_page_link = showall.a.get('href')
    else:
        all_students_page_link = participants_link
    print("showall: ", all_students_page_link)

    # Get special link of every student
    result = session_requests.get(all_students_page_link, headers = dict(referer = all_students_page_link))
    soup = BeautifulSoup(result.content, 'html.parser')
    students_link = soup.find_all('th', {'id' : re.compile('^user-index-participants*')})
    for i in range(0, participant_count):
        students_link[i] = students_link[i].a.get('href')
        # print(students_link[i])
        # get { student name } from every student
        result = session_requests.get(students_link[i], headers = dict(referer = students_link[i]))
        soup = BeautifulSoup(result.content, 'html.parser')
        student_name = soup.find_all('div', attrs={'class' : "page-context-header"}) 
        print(student_name[1].h2.get_text())

        # get { student code -or- email } from every student
        #TODO separate student_code from email
        # if student code -or- email was hidden
        try:
            student_code_or_email = soup.find('dt', text='آدرس پست الکترونیک').next_sibling.a.get_text().strip('@sun.hsu.ac.ir')
        except:
            student_code_or_email = "hidden"
        print(student_code_or_email)
        
        # get { role } of student
        student_role = soup.find('dt', text="نقش‌ها").next_sibling.a.get_text()
        print(student_role)
        
        # get { student's lessons } 
        #TODO go to currect page of all lessons <<done>>
        # if number of student's lessons <= 8 
        try:
            student_lessons_link = soup.find('a', {'title' : "مشاهده موارد بیشتر"}).get('href')        
        except:
            student_lessons_link = students_link[i]
        result = session_requests.get(student_lessons_link, headers = dict(referer = student_lessons_link))
        soup = BeautifulSoup(result.content, 'html.parser')
        student_lessons = soup.find('dt', text="درس‌ها").next_sibling.ul.find_all('li')
        for lesson in student_lessons:
            print(lesson.get_text())

        # get students picture url {if he/she has}
        try:
            student_img = soup.find('img', {'class' : "defaultuserpic"})
        except expression as identifier:
            pass
        student_img = soup.find('div', {'class' : "page-header-image"}).a.img
        if "defaultuserpic" in student_img.get('class'):
            student_img = None
        else:
            student_img = student_img.get('src')
        print(student_img)