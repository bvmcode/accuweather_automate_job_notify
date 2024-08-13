import json
import requests
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from dotenv import dotenv_values

def get_jobs():
    with open("config.json", "r") as f:
        config = json.loads(f.read())
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
    creds = dict(dotenv_values(".env"))
    jobs = get_jobs()
    host = 'smtp.office365.com'
    conn = smtplib.SMTP(host, 587)
    conn.starttls()
    user = creds["EMAIL"]
    pwd = creds["PASS"]
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = user
    msg['Subject'] = 'Accuweather Jobs'
    message = "\n".join(jobs)
    msg.attach(MIMEText(message))
    context = ssl.create_default_context()
    with smtplib.SMTP(host, 587) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(user, pwd)
        server.sendmail(user, user, msg.as_string())


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(send_email, 'cron', minute='0', hour='16', day='*', year='*', month='*')
    scheduler.start()
