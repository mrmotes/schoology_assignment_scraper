# Schoology Assignment Scraper
A simple application for scraping assignment data from Schoology, reformatting it for clarity, and storing it in both a local, SQLite database as well as an Airtable base. 

## Why?
I am a divorced parent with a distractable teenager and Schoology is kind of horrible. I want to be able to help support my son throughout middle school and high school, but each time I sit down to do so, I am left sifting through a lot of junk on Schoology, coming out with more questions than answers. After a disappointing interaction with a school teacher who didn't understand some of my frustrations, I decided to automate the process of making sense of Schoology.

## What?
I am not a _programmer_, but I know a little bit. This application is written in Python using primarily BeautifulSoup, SQLAlchemy, and pyairtable. I have a cron job set up to run this application once at 8:00 am and again at 4:00 pm, Monday through Friday, from the start of August until the end of May. The code itself scrapes assignment and grade information from Schoology. This data is cleaned up and organized before being stored locally on my machine and synced to a base in Airtable. The code references a few tables from Airtable to dynamically grab the course assignments that are relevant at any given time (e.g., new courses year over year).

## Who?
I have developed this for my personal use. It's aimed at solving a problem specific to me. That said, with a little know-how, this could be easily repurposed for others. The majority of the work in this application is web scrapping, so anticipate a fair amount of reworking. I cannot speak to the consistency of Schoology from school to school.
