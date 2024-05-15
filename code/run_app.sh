#!/bin/zsh

echo "Starting script execution at $(date)" >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt
source /Users/motes/Projects/schoology_assignment_scraper/motes-env/bin/activate
echo "Virtual environment activated" >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt
PATH=/Users/motes/Projects/schoology_assignment_scraper/motes-env/bin:$PATH
echo "PATH updated" >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt
python /Users/motes/Projects/schoology_assignment_scraper/code/app.py -v >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt 2>&1
echo "Script execution completed at $(date)" >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt