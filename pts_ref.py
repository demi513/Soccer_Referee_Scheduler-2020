#! python3

from logging import info
from time import monotonic
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from os import path

from google.auth import credentials
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from os import path, stat
import pickle
from pprint import pprint
from datetime import datetime, timedelta
import smtplib


def load():
    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = InstalledAppFlow.from_client_secrets_file(path.join(path.dirname(__file__), 'client_secret.json'), scopes=scopes) 
    credentials = flow.run_console()
    pickle.dump(credentials, open(path.join(path.dirname(__file__), 'token.pkl'), 'wb'))

def create_event(name, starttime, duration_minutes, description=None, location=None):
    endtime = starttime + timedelta(minutes=duration_minutes)
    starttime = starttime.strftime("%Y-%m-%dT%H:%M:%S-04:00")
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%S-04:00")
    event = {
        'summary': name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': starttime
        },
        'end': {
            'dateTime': endtime
        },
        'colorId': 10,
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 60},
            {'method': 'popup', 'minutes': 45},
            ],
        },
        }
    result = service.events().list(calendarId='primary', timeMin=starttime, timeMax=endtime).execute()['items']
    #check if already their
    for i in range(len(result)):
        if result[i]['summary'] == name and result[i]['start']['dateTime'] == starttime and result[i]['end']['dateTime']:
            return
    with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as smtp:
        smtp.login('<Your Email>', '<Your emails Password>')
        subject = 'A modification has been made to your soccer ref schedule'
        body = f"summary: {name} \nstart: {starttime} \nduration: {duration_minutes} "
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail('<Your Email>', '<Your Email>', msg)
    return service.events().insert(calendarId='primary', body=event).execute()


options = Options()
options.headless = True
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(options=options, executable_path=path.join(path.dirname(__file__), 'geckodriver'))
driver.get('http://www.tsisports.ca/soccer/ptsref/login2.aspx')

username = driver.find_element_by_xpath('//*[@id="MainContent_txtUser"]')
username.send_keys('<Your pts_ref username>')

password = driver.find_element_by_xpath('//*[@id="MainContent_txtPass"]')
password.send_keys('<Your pts_ref Password>')

log_in = driver.find_element_by_xpath('//*[@id="MainContent_cmdLogin"]')
log_in.click()

driver.get('http://www.tsisports.ca/soccer/ptsref/frm_listMatchArb.aspx?type=NEXT')

#loading google api
load()
credentials = pickle.load(open(path.join(path.dirname(__file__), 'token.pkl'), 'rb'))
service = build('calendar','v3', credentials=credentials)

#location
number_of_games = int(driver.find_element_by_xpath('//*[@id="MainContent_listMatchsArbitre1_lblNoGames"]').text.split(' ')[0])
for i in range(1, number_of_games+1):
    day, location, _, teams = driver.find_element_by_xpath(f'/html/body/form/div[4]/div[2]/table/tbody/tr[{i}]/td/div/div[2]').text.splitlines()
    age = driver.find_element_by_xpath(f'/html/body/form/div[4]/div[2]/table/tbody/tr[{i}]/td/div/div[1]/h4[2]')
    duration = 90    
    year_month_day, hours_minutes = day.split(' ')
    year, month, day = year_month_day.split('-')
    hours, minutes = hours_minutes.split(':')
    type_of_ref = driver.find_element_by_xpath(f'/html/body/form/div[4]/div[2]/table/tbody/tr[{i}]/td/div/div[1]/h4[1]').text
    create_event(f'Soccer Reff {location}', datetime(int(year), int(month), int(day), int(hours), int(minutes)), duration,f'teams: {teams} \n type: {type_of_ref}')

driver.close()

