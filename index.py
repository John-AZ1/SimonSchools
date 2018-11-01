import requests
import os
import datetime
import getpass
import re
import time

session = requests.Session()

try:
    username = os.environ['simon_user']
except KeyError:
    print('Enviroment variable simon_user')
    username = input('Simon Username: ')

try:
    password = os.environ['simon_password']
except KeyError:
    print('Enviroment variable simon_password')
    password = getpass.getpass('Simon Password: ')

try:
    url = os.environ['simon_url']
except KeyError:
    url = 'intranet.stpats.vic.edu.au'

logon_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

logon_data = {
  'curl': 'Z2F',
  'flags': '0',
  'forcedownlevel': '0',
  'formdir': '3',
  'trusted': '1',
  'username': username,
  'password': password,
  'SubmitCreds': 'Log On'
}

logon = session.post('https://'+url+'/CookieAuth.dll?Logon', headers=logon_headers, data=logon_data)
print("Logon ok:", logon.ok)

asp_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

asp_params = (
    ('ReturnUrl', '/'),
)

asp_response = requests.get('https://intranet.stpats.vic.edu.au/Login/Default.aspx', headers=asp_headers, params=asp_params, )
print("ASP ok:", asp_response.ok)
print(asp_response.cookies.get_dict())

adAuth_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://intranet.stpats.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

adAuth_params = (
    ('ReturnUrl', '/'),
)

adAuth_data = {
  '__VIEWSTATE': '3XxL8wr4uiSbJd8CTOjmnok6LROKySZq8vManM9/fFHJAjkbOIlkRtfhKkqq/8p8rhRZTlUYbCHSW0ZZgMQVX+3Zv+NKLiVJWtPLr2Gk0au54X5kyeaKBWHrOxJSbmO36nc61UaDT3jQy8N/1GE0B/doDig0P4Z1X1qGVfN5swqpXnipwnKGeIN+/11WoAvDU2Z8PUssUZhIuwGGN1si3qo2A56a6PGDDDf+nKBTEa6qwDJC7TYWrEJfujDeEse702rKhzz8sSkTvYpYj667p0w67rtC8zf1VLD0+PjwTpvwKGJq45LFFMgIeuox0MMHuAtPPMhJW84rDYlqbGkqKqBhc2U1L8Q2rCStSRRvmo+GgFED0S0KrF+tKMsB7gjXq7qBOaGBFK8mI44j3bx2CeegqYrxv+t6evA4Bkplgbd+HVM53D/z8XkT7RAulPogxyTutASvr5gpybfvYI0cCnusP6GbEdAU+Vkj+vdqeGU76GSi2bqKQZOXcosC/XFtHWPgdx8FDNwnz3PV2wcWk07C0vBpA1JIdPR2nCcaWCOML4msz4Dgxzco3QPz7Ix1vJ6GUANzKgyTX4TNT/0gNQ==',
  '__VIEWSTATEGENERATOR': '25748CED',
  '__EVENTVALIDATION': '0rwo5H4FZTgbjG8CBqqqdqzDwUA1W+hyI0jSYD0nZafRobnxHcdOrUNWhOl4FSG2WHvu4JLXzSnRssQdqJhLzgSgrl+uD8OGNHwoJbTJ5B1hWgSzDenLrpERZ9oZ64i4a31AGLphYtDmlk6uTykUS3+BOiGsOi8dU+xaweaoTM2MEvT5tcj+JzeojrzQeCuFtWtuItzGRyaeMWXirI37mQ==',
  'Version': '3.13.2.0',
  'inputUsername': username, 
  'inputPassword': password,
  'buttonLogin': 'Sign in'
}

adAuth_response = session.post('https://intranet.stpats.vic.edu.au/Login/Default.aspx', headers=adAuth_headers, params=adAuth_params, data=adAuth_data)

print("adAuth ok:", adAuth_response.ok)
print(session.cookies.get_dict())

today = datetime.datetime.today().strftime('%Y-%m-%d')

def get_TT(date):
    timetable_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://'+url+'/',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    timetable_data = '{"selectedDate":"'+date+'","selectedGroup":"STURT"}'
    
    timetable_response = session.post('https://'+url+'/Default.asmx/GetTimetable', headers=timetable_headers,  data=timetable_data) 
    print("Timetable ok:", timetable_response.ok)
    return(timetable_response)

def print_TT(timetable):
    print(timetable.json()['d']['Info'])
    periods = timetable.json()['d']['Periods']
    for period in periods:
        for schClass in period['Classes']:
            print('-------------------------')
            print(schClass['TimeTableClass'])
            print(schClass['TeacherName'])
            print(schClass['Room'])

def print_mark():
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://'+url+'/WebModules/LearningAreas/Tasks/Assessment/SubmitTask.aspx?NavBarItem=ViewAssessmentTasks&TaskID=15605&Class=18998&Inactive=False',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    
    data = '{"taskID":"15717","subjectClassID":"19484"}'
    
    response = session.post('https://'+url+'/WebModules/LearningAreas/Tasks/Assessment/SubmitTask.aspx/GetTaskSubmissionInfo', headers=headers, data=data)
    print("Mark ok:", response.ok)
    print(response.json()['d']['TaskResult']['FinalResult'])

def get_average(guid, sem):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://'+url+'/WebModules/Profiles/Student/LearningResources/LearningAreaTasks.aspx?UserGUID=cf3e1f97-210f-4e35-a693-b4c176d9d94d',
    'Content-Type': 'application/json; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

    data = '{"guidString":"'+guid+'","fileSeq":'+str(sem)+'}'

    response = session.post('https://'+url+'/WebModules/Profiles/Student/LearningResources/LearningAreaTasks.aspx/getClasses', headers=headers, data=data) 
    
    print("Average ok:", response.ok)

    resultRegx = re.compile(r'(?:\d+ \/ \d+ \((\d+)%\)|(\d+)%)')
    scoreList = []    

    for subjClass in response.json()['d']['SubjectClasses']:
        for task in subjClass['Tasks']:
            finalScore = int([ x for x in resultRegx.findall(task['FinalResult'])[0] if x != ''][0]) if resultRegx.findall(task['FinalResult']) else None 
            if finalScore:
            	scoreList.append(finalScore)

    try:
        print(sum(scoreList) / len(scoreList)) 
    except ZeroDivisionError:
        print('No Tasks this semester')

def get_guid():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://'+url+'/WebModules/Profiles/Student/LearningResources/LearningAreaTasks.aspx?UserGUID=cf3e1f97-210f-4e35-a693-b4c176d9d94d',
        'Content-Type': 'application/json; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    
    params = (
        (str(int(time.time() * 1000)), ''),
    )
    
    response = session.post('https://'+url+'/Default.asmx/GetUserInfo', headers=headers, params=params)
    print("GUID ok:", response.ok)
    guidRegx = re.compile(r'.*?GUID=(.*)')
    return(guidRegx.search(response.json()['d']['UserPhotoUrl']).group(1))

# timetable = get_TT(today)
# print_TT(timetable)
# print_mark()
guid = get_guid()
# 29 = 2016, 1st Semester
semester = int(input('Semester Code: '))
get_average(guid, semester)

