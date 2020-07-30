from bs4 import BeautifulSoup
import requests
import telebot
import schedule

bot = telebot.TeleBot("1380969339:AAFgLsHADwLkM7sYASCrzpVQ0SrwfZX0L00")

class Parser:
    def __init__(self, link):
        self.link = link
    
    def get_info(self):
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61'}
            html_jobs = requests.get(self.link, headers=header)
            if  html_jobs.status_code == 200:
                soup_h = BeautifulSoup(html_jobs.text, 'html.parser')
                items_jobs = soup_h.find_all('div', class_='vacancy')
                jobs = {}
                for item in items_jobs:
                    jobs.update({item.find('a', class_='vt').get_text(): [item.find('a', class_='vt').get('href'), item.find('span', class_='cities').get_text()]})
            return jobs
        except Exception:
            return 'Error Occured!'

def tm():
    now = datetime.datetime.now()
    hour = now.hour+3
    if hour >= 6 and hour <12:
        daytime = 'Доброго ранку'
    elif hour >=12 and hour <18:
        daytime = 'Доброго дня'
    elif hour >=18 and hour <22:
        daytime = 'Доброго вечора'
    else:
        daytime = 'Доброї ночі'
    greeting = f'{daytime}'
    return greeting

def pm():
    try:
        jobs = Parser('https://jobs.dou.ua/vacancies/?category=Project%20Manager&search=%D0%9B%D1%8C%D0%B2%D1%96%D0%B2').get_info()
        bot.send_message(561488159, f"*{tm()}, Бодя!*\n{len(jobs)} вакансій по запиту 'project manager' у Львові:\n", parse_mode='Markdown')
        for key, value in jobs.items():
            position = key
            link = value[0]
            city = value[1]
            bot.send_message(561488159, f"[{position}]({link})\n{city}", parse_mode='Markdown', disable_web_page_preview=True)
    except Exception:
        bot.send_message(561488159, "Error")

schedule.every().day.at('15:00').do(pm)

while True:
    schedule.run_pending()
    time.sleep(45)