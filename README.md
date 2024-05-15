# Schoology Assignment Scraper
A simple application for scraping assignment data from Schoology, reformatting it for clarity, and storing it in both a local, SQLite database as well as an Airtable base. 

## Why?
I am a divorced parent with a 13-year-old son who has ADHD. Giving him the proper support in school is a challenge. To complicate things further, Schoology, the online platform MNPS uses for class assignments, resources, and grading, is garbage. Each time I sit down to help make a study or homework plan, I am left sifting through a lot of junk on Schoology where I come out of it with more questions than answers. After a disappointing interaction with a school teacher who didn't understand some of my frustrations, I decided to automate the process of making sense of Schoology.

## What?
I am not a _programmer_, but I know a little bit. This application is written in Python using primarily BeautifulSoup, SQLAlchemy, and pyairtable. I have a cron job set up to run this application once at 8:00 am and again at 4:00 pm, Monday through Friday, from the start of August until the end of May. The code itself scrapes assignment and grade information from Schoology. This data is cleaned up and organized before being stored locally on my machine and synced to a base in Airtable. The code references a few tables from Airtable to dynamically grab the course assignments that are relevant at any given time (e.g., new courses year over year).

## Who?
I have developed this for my personal use. It's aimed at solving a problem specific to me. That said, with a little know-how, this could be easily repurposed for others. The majority of the work in this application is web scrapping, so anticipate a fair amount of reworking. I cannot speak to the consistency of Schoology from school to school.
