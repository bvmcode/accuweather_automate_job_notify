import json
import os
import requests
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup


with open("config.json", "r") as f:
    config = json.loads(f.read())

def get_jobs():
    resp = requests.get(config["accuweather_url"])
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_words = config["job_titles"]
    current_jobs = []
    for i in soup.find_all('a'):
        for word in title_words:
            if word in i.text.lower():
                job_title = f"{i.text.strip()} - {i.attrs['href']}"
                current_jobs.append(job_title)
    return current_jobs


def send_email():
    jobs = get_jobs()
    if jobs:
        host = os.getenv("HOST")
        pwd = os.getenv("PASS")
        user = os.getenv("EMAIL")
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = user
        msg['Subject'] = 'Accuweather Jobs'
        message = "\n".join(jobs)
        msg.attach(MIMEText(message))
        conn = smtplib.SMTP(host, 587)
        conn.starttls()
        context = ssl.create_default_context()
        with smtplib.SMTP(host, 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo() 
            server.login(user, pwd)
            server.sendmail(user, user, msg.as_string())


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(send_email, 'cron', minute='0', hour=config["exec_hour"], day='*', year='*', month='*')
    scheduler.start()
