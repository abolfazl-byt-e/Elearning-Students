import requests
import config
from lxml import html
from bs4 import BeautifulSoup

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
    participants = soup.find('a', {"data-key" : "participants"}).get('href')
    print(participants)
    

    
