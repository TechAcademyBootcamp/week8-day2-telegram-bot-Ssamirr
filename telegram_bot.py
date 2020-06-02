import telegram
from bs4 import BeautifulSoup
import requests,webbrowser

def main():
    bot = telegram.Bot(token="1288265003:AAGyWNwBq409rSu7_xe1TNVUpSvibtDYNvM")
    while True:
        echo(bot)
update_id=None
    
def echo(bot):
    global update_id
    for update in bot.get_updates(offset=update_id,timeout=10):
        update_id = update.update_id + 1
        if update.message:
            message = update.message.text
            if message == "news":
                response= requests.get('https://oxu.az/')
                soup=BeautifulSoup(response.text, features="html.parser")
                title = soup.findAll('div',{'class':'title'})
                link = soup.findAll("a",{"class":"news-i-inner"})
                for i in range(len(title)):
                    update.message.reply_text(f"{title[i].text} - https://oxu.az/{link[i]['href']}")
                    
            elif message == "exchange":
                response=requests.get("https://api.exchangeratesapi.io/latest").json()
                for i in response['rates']:
                    update.message.reply_text(f"{response['rates'][i]}--{i}")

            elif message == "weather":
                response=requests.get('http://api.openweathermap.org/data/2.5/weather?appid=2b94272e8df26b0abdf7fc3a4beee70b&q=Baku').json()
                update.message.reply_text(f"Country-{response['sys']['country']}")
                update.message.reply_text(f"City-{response['name']}")

                for i in response['weather']:
                    for key,values in i.items():
                        update.message.reply_text(f"{key}-{values}")

                update.message.reply_text(f"wind-speed-{response['wind']['speed']}")
                for key,values in response['main'].items():
                    update.message.reply_text(f"{key}-{values}") 

            elif "google" in message:
                message = message.split(' ')[1]
                response=requests.get(f"https://www.google.com/search?q={update.message.text}")
                soup=BeautifulSoup(response.text,features="html.parser")
                search_title=soup.select('.vvjwJb')
                search_link=soup.select('.UPmit')
                for i in range(len(search_link)):
                    link=search_link[i].text.replace('›','/').replace(" ","").split(",")[0]
                    update.message.reply_text(f"{search_title[i].text} -- link -> {link}")

if __name__ == '__main__':
    main()
