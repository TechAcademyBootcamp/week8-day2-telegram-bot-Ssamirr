import telegram
from bs4 import BeautifulSoup
import requests,webbrowser

def logger(func):
    def wrapper(*args, **kwars):
        result = None
        try:
            result = func(*args, **kwars)
            with open('logs.txt', 'a') as f:
                f.write(f'|{func.__name__}|{args}, {kwars}|{result}|True|\n')
            return result
        except:
            with open('logs.txt', 'a') as f:
                f.write(f'|{func.__name__}|{args}, {kwars}|{result}|False|\n')
    return wrapper

def main():
    bot = telegram.Bot(token="1288265003:AAGyWNwBq409rSu7_xe1TNVUpSvibtDYNvM")
    while True:
        echo(bot)
update_id = None
learning = False
ask_question = None
    
def echo(bot):
    global update_id
    global learning
    global ask_question
    global user_question_answer

    for update in bot.get_updates(offset=update_id,timeout=10):
        update_id = update.update_id + 1
        if update.message:
            message = update.message.text


            if message == "news":
                update.message.reply_text(news())


            elif message == "exchange":
                update.message.reply_text(exchange())
                    

            elif message == "weather":
               update.message.reply_text(weather())

            elif "google" in message:
              update.message.reply_text(google(message.split(' ')[1]))

             
            else:
              # update.message.reply_text(quiz(message))
              l_question=[]
              l_answer=[]
              with open('bot.txt','r+') as b:
                  b.seek(0)
                  for i in b.readlines():
                      if not i.split("-")[0] in l_question:
                          l_question.append(i.split("-")[0])
                          l_answer.append(i.split("-")[1])
                  for i in range (len(l_question)):
                      if l_question[i]==message:
                          update.message.reply_text(f"{l_answer[i]}")
                  if message == "beli" and ask_question:
                      learning=True
                      continue
                  elif learning==True:
                      learning=False
                      user_question_answer=message
                      update.message.reply_text("Cavab Verildi->Davam edin")
                      b.write(f"\n{ask_question}-{user_question_answer}")
                      ask_question=None
                  elif not message in l_question:
                      ask_question=message
                      update.message.reply_text("Bu suala cavab yoxdur.Cavab vermek isteyirsiniz (beli): ")
              

@logger                    
def news():
    response= requests.get('https://oxu.az/')
    soup=BeautifulSoup(response.text, features="html.parser")
    title = soup.findAll('div',{'class':'title'})
    link = soup.findAll("a",{"class":"news-i-inner"})
    for_news = ""
    for i in range(len(title)):
      for_news += f"{title[i].text} - https://oxu.az/{link[i]['href']}\n"
    return for_news

@logger
def exchange():
  response=requests.get("https://api.exchangeratesapi.io/latest").json()
  for_exchange = ""
  for i in response['rates']:
      for_exchange += f"{response['rates'][i]}--{i}\n"
  return for_exchange

@logger
def weather():
    response=requests.get('http://api.openweathermap.org/data/2.5/weather?appid=2b94272e8df26b0abdf7fc3a4beee70b&q=Baku').json()
    for_weather=" "
    for_weather += f"Country-{response['sys']['country']}\n"
    for_weather += f"City-{response['name']}\n"
    for i in response['weather']:
        for key,values in i.items():
            for_weather += f"{key}-{values}\n"
    for_weather += f"wind-speed-{response['wind']['speed']}\n"
    for key,values in response['main'].items():
        for_weather += f"{key}-{values}\n"
    return for_weather

@logger
def google(search):
  response=requests.get(f"https://www.google.com/search?q={search}")
  soup=BeautifulSoup(response.text,features="html.parser")
  search_title=soup.select('.vvjwJb')
  search_link=soup.select('.UPmit')
  for_google = ""
  for i in range(len(search_link)):
      link=search_link[i].text.replace('›','/').replace(" ","").split(",")[0]
      for_google += f"{search_title[i].text} -- link -> {link}\n"
  return for_google

# def quiz(message):
#   quiz_telegram = True
#   global learning
#   global ask_question
#   global user_question_answer
#   while quiz_telegram == True:
#       l_question=[]
#       l_answer=[]
#       with open('bot.txt','r+') as b:
#           b.seek(0)
#           for i in b.readlines():
#               if not i.split("-")[0] in l_question:
#                   l_question.append(i.split("-")[0])
#                   l_answer.append(i.split("-")[1])
#           for i in range (len(l_question)):
#               if l_question[i]==message:
#                   return f"{l_answer[i]}"
#           if message == "beli" and ask_question:
#               learning=True
#               continue
#           elif learning==True:
#               learning=False
#               user_question_answer=message
#               b.write(f"\n{ask_question}-{user_question_answer}")
#               ask_question=None
#               quiz_telegram = False
#               return "Cavab Verildi"
#           elif not message in l_question:
#               ask_question=message
#               return "Bu suala cavab yoxdur.Cavab vermek isteyirsiniz (beli): "



if __name__ == '__main__':
    main()