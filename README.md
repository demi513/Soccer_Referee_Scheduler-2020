# Soccer Referee Scheduler

## What I learned
  - **Selenium WebDriver:** Automated browser actions with Selenium, particularly for web scraping and interacting with dynamic content.
  - **Google Calendar API:** Integrated Google Calendar API to create events and set reminders, enhancing automation and improving organization.
  - **OAuth2 Authentication:** Used Google's OAuth2 flow to authenticate and access the Google Calendar API securely.
  - **Email Notifications:** Implemented email notifications using smtplib to alert users about modifications to their calendar events.



## Overview
This Python script automates the process of managing soccer referee schedules. It scrapes game schedules from the TSI Sports platform, creates events on a Google Calendar, and sends email notifications for new or modified events. The project leverages Selenium for web automation, Google Calendar API for event creation, and SMTP for email notifications.

## Features
  - **Web Automation:** Logs into the TSI Sports platform, fetches game schedules, and retrieves relevant details.
  - **Google Calendar Integration:** Automatically creates events in a Google Calendar with detailed information about the games.
  - **Email Notifications:** Sends email alerts whenever an event is added or updated in the calendar.
  - **Headless Browser:** Runs in a headless Firefox browser for seamless automation.

## Prerequisites
  - Selenium WebDriver (geckodriver)
  - Google API Credentials for accessing Google Calendar.


## Setup
1. Install Required Libraries:
  `conda create --name <env> --file requirements.txt`
2. Google API Setup:
    - Enable the Google Calendar API in the Google Cloud Console.
    - Download the client_secret.json file and save it in the script directory.
3. Email Configuration:
    - Replace <Your Email> and <Your email's Password> in the script with your email credentials. For Gmail, ensure that "Allow less secure apps" is enabled or set up an App Password.
4. TSI Sports Login:
    - Replace <Your pts_ref username> and <Your pts_ref Password> in the script with your TSI Sports login credentials.
5. WebDriver:
    - Download the Firefox WebDriver (geckodriver) from Mozilla's GitHub and ensure it is executable.

