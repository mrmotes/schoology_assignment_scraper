#!/bin/zsh

log_message() {
    timestamp=$(date +"%Y-%m-%d %H:%M:%S,$(printf "%03d" $(( $(date +%N) / 1000000 )) )")
    message="$1"
    echo "$timestamp - INFO - $message" >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt
}

log_message "Starting script execution"

source /Users/motes/Projects/schoology_assignment_scraper/motes-env/bin/activate

log_message "Virtual environmentn activated"

PATH=/Users/motes/Projects/schoology_assignment_scraper/motes-env/bin:$PATH

log_message "PATH updated"
log_message "Starting app.py"

python /Users/motes/Projects/schoology_assignment_scraper/code/app.py -v >> /Users/motes/Projects/schoology_assignment_scraper/code/logs/cron_logs.txt 2>&1

log_message "Completed app.py"
log_message "Ending script execution"