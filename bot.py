##------> MATPLOIT CONFIGURATION TO WORK IN VPS <------##
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
##----------------------------------------------##

from bs4 import BeautifulSoup
import requests
import telebot
import threading
import time
import matplotlib.pyplot as plt
from matplotlib import *
from datetime import datetime
import os
import tweepy
import numpy as np

##---------------------------> Twitter Token <---------------------------##
auth = tweepy.OAuthHandler(" ", " ")
auth.set_access_token(" ", " ")
api = tweepy.API(auth)



##---------------------------> Telegram Variables <---------------------------##
channel_id = ' '
token = ' '
bot = telebot.TeleBot(token)


##---------------------------> GRAPH VARIABLES <---------------------------##
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
x = ['J22', 'J23', 'J24', 'J25', 'J26', 'J27', 'J28', 'J29', 'J30', 'J31', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20', 'M21', 'M22', 'M23', 'M24', 'M25', 'M26']
y = [580, 845, 1317, 2015, 2800, 4581, 6058, 7813, 9823, 11950, 14553, 17391, 20630, 24545, 28266, 31439, 34876, 37552, 40553, 43099, 45134, 59287, 64438, 67100, 69197, 71329, 73332, 75184, 75700, 76677, 77673, 78651, 79205,80087, 80828, 81820, 83112, 84615, 86604, 88585, 90443, 93016, 95314, 98425, 102050, 106099, 109991, 114381, 118914, 126204, 134540, 145483, 156433, 169450, 189683, 198426, 219240, 245669, 276113, 308231, 338724, 381645, 422829, 471311, 532237]
y_recovered = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 504, 643, 907, 1173, 1562, 2083, 2684, 3323, 4043, 4803, 5987, 6808, 8196, 9538, 10973, 12712, 14553, 16357, 18524, 20895, 22650, 24991, 27466, 30051, 32805, 36520, 39430, 42330, 45122, 48108, 50944, 53524, 55605, 57609, 60172, 62278, 64056, 66621, 68307, 70360, 72575, 75925, 77453, 79629, 82624, 85334, 88163, 91573, 95495, 98627, 102069, 108879, 114228, 123942]
y_deaths = [17, 25, 41, 56, 80, 106, 132, 170, 213, 259, 304, 362, 426, 492, 565, 638, 724, 813, 910, 1018, 1115, 1261, 1383, 1526, 1669, 1775, 1873, 2009, 2126, 2247, 2360, 2460, 2618, 2699, 2763, 2800, 2858, 2923, 2977, 3050, 3117, 3202, 3285, 3387, 3494, 3599, 3827, 4025, 4296, 4628, 4981, 5428, 5833, 6520, 7162, 7979, 8951, 10030, 11386, 13011, 14640, 16513, 18894, 21282, 24073]
y_infected = [563, 786, 1238, 1910, 2669, 4415, 5823, 7519, 9439, 11448, 13921, 16525, 19561, 23146, 26528, 29239, 32069, 34055, 36320, 38038, 39216, 52039, 56247, 57378, 57990, 58581, 58747, 58662, 57217, 55906, 54418, 53541, 51596, 49922, 48014, 46215, 43734, 42262, 41297, 40413, 39218, 38870, 38505, 39433, 40947, 42328, 43886, 46300, 48031, 53279, 59168, 67413, 75717, 85544, 95623, 107556, 124459, 146709, 172591, 196473, 224192, 260248, 294801, 335525, 383850]

xh = []
yh = [] 


##---------------------------> WEBS TO GET DATA <---------------------------##
url = 'https://www.worldometers.info/coronavirus/'
url_news = 'http://feeds.bbci.co.uk/news/world/rss.xml'


##---------------------------> SEND MESSAGE FUNCTION <---------------------------##
def send_message(text, cid):
        bot.send_message(cid,text)


##---------------------------> BOT COMMAND HANDLER <---------------------------##
class handle:

        def commands(message):
                txt = message.text

                if '/graph' in txt.split()[0]:
                        photo = open(f'img/day/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}.png', 'rb')
                        bot.send_photo(message.chat.id, photo)
                        
                elif '/info' in txt.split()[0]:
                        handle.info(message)

                elif '/total' in txt.split()[0]:
                        send_message(requestbot(), message.chat.id)

                elif '/help' in txt.split()[0]:
                        send_message("Commands:\n\n/info country - Information about that country\n/total - Total coronavirus data \n/graph - Show graph about coronavirus growth", message.chat.id)




        def info(message):
                try:
                        pais = ' '.join(message.text.split()[1:])
                        send_message(request(pais), message.chat.id)
                        
                except Exception as E:
                        print(E)
                        send_message('Please, use a country/zone from the list', message.chat.id)




##---------------------------> REQUESTS AND DATA TREATMENT <---------------------------##

def requestbot():
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'html.parser')
        all = soup.find_all('div', class_='maincounter-number')
        infected = all[0].text.replace(',', '').strip()
        deaths = all[1].text.replace(',', '').strip()
        recovered = all[2].text.replace(',', '').strip()
        
        active = int(infected) - int(deaths) - int(recovered)


        return f'[Total] Active {active} | Deaths {deaths} | Recovered {recovered}'


def request(pais):
        web = requests.get(url).text
        soup = BeautifulSoup(web, 'html.parser')
        tr = soup.find_all('tr')
        for td in tr:
               	td_lookup = td.find_all('td')
                for num in range(len(td_lookup)):
                        if 'text-align:left' in str(td_lookup[num]) and pais.lower() == td_lookup[num].text.lower():

                                variables = [str(td_lookup[num + 1].text), str(td_lookup[num + 2].text), str(td_lookup[num + 3].text), str(td_lookup[num  + 4].text), str(td_lookup[num  + 5].text), str(td_lookup[num  + 6].text), str(td_lookup[num  + 7].text), str(td_lookup[num + 8].text)] 
                                
                                for num in range(len(variables)):
                                        if variables[num].replace(' ', '') == '':
                                                variables[num] = '0'

                                data = [variable.replace(' ', '') for variable in variables]
                                return f'[{pais.upper()}] Cases: {data[0]} - Today: {data[1]} - Active: {data[5]} - Critical: {data[6]}| Deaths: {data[2]} - Today: {data[3]} | Recovered: {data[4]} | Cases every M: {data[7]}'
                                break                           
                        else:
                                pass





##---------------------------> MAIN FUNCTION <---------------------------##

def channel():
        last_new = ''
        cases = 0
        last_cases = 0
        while True:
                time.sleep(2*60)
                if f'{months[datetime.now().month - 1][0]}{datetime.now().day - 1}' not in x: 
                        updategraphdaily()

                if datetime.now().minute < 2:
                        output = requestbot()
                        send_message(output , channel_id)
                        api.update_status(output + '\n\n#CORONAVIRUS #NEWS #COVID19')
                        if last_cases == 0:
                                last_cases = int(requestbot().split()[2])
                        else:
                                cases = int(requestbot().split()[2]) 
                                total = cases - last_cases
                                percentaje = round(total/cases * 100, 2)
                                last_cases = cases

                                api.update_status(f'[{datetime.now().day}/{datetime.now().month - 1} - {datetime.now().hour}:0{datetime.now().minute}] New {total} cases (+{porcentaje})\n\n#CORONAVIRUS #NEWS #COVID19')
                                send_message(f'[{datetime.now().day}/{datetime.now().month - 1} - {datetime.now().hour}:0{datetime.now().minute}] New {total} cases (+{porcentaje})', channel_id)

                        updategraphhourly()
                        
                web = requests.get(url_news).text

                soup = BeautifulSoup(web, 'lxml-xml')
                item = soup.find('item')
                link = item.find('link').text
                content = requests.get(link).text

                if link != last_new:
                        if 'Coronavirus' in content or 'coronavirus' in content:
                             send_message(link, channel_id)
                             api.update_status('#CORONAVIRUS #NEWS #COVID19\n' + link)
                             last_new = link

                        



                
##---------------------------> GRAPHS <---------------------------##

def updategraphdaily(): 
        value = int(requestbot().split()[2])
        recovered =  int(requestbot().split()[5])
        deaths = int(requestbot().split()[8])
        infected = value - (recovered + deaths)

        x.append(f'{months[datetime.now().month - 1][0]}{datetime.now().day - 1}')
        y.append(value)
        y_recovered.append(recovered)
        y_deaths.append(deaths)
        y_infected.append(infected)

        graph()
        photo = open(f'img/day/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}.png', 'rb')     
        bot.send_photo(channel_id, photo)
        api.update_with_media(f'img/day/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}.png', 'Coronavirus Growth')


def updategraphhourly():
        global xh, yh
        if str(datetime.now().hour) == '0':
                plt.figure(figsize=(20,10))
                plt.bar(xh,yh)
                plt.title('Coronavirus growth today', fontweight="bold")
                plt.xlabel('Hour')
                plt.ylabel('Cases')
                plt.tick_params(axis='x', rotation=90)
                for c,d in zip(xh,yh):
                        plt.text(c, d + 1000, str(d), rotation=90, horizontalalignment="center")


                xh = [] 
                yh = []

                plt.savefig(f'img/24/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}24H.png', bbox_inches='tight')
                photo = open(f'img/24/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}24H.png', 'rb')
                bot.send_photo(channel_id, photo)
                api.update_with_media(f'img/24/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}24H.png', 'Coronavirus Growth Today')

        
        xh.append(datetime.now().hour) 
        yh.append(int(requestbot().split()[2]))



def graph(custom=None):
    plt.figure(figsize=(20,10))
    plt.bar(x, y_deaths, color="#191919", label='Deaths')
    plt.bar(x, y_recovered, bottom=y_deaths, color="#42AA05", label='Recovered')
    plt.bar(x, y_infected, bottom=np.array(y_deaths) + np.array(y_recovered), color="#AA0505", label='Infected')
    plt.title('Coronavirus growth', fontweight="bold")
    plt.xlabel('Day')
    plt.ylabel('Cases')
    plt.tick_params(axis='x', rotation=90)
    plt.legend()
    for c,d in zip(x,y):
            plt.text(c, d + 6000, str(d), rotation=90, horizontalalignment="center")
    
    plt.savefig(f'img/day/{months[datetime.now().month - 1][0]}{datetime.now().day - 1}.png', bbox_inches='tight')


##---------------------------> BOT MESSAGE HANDLER <---------------------------##
@bot.message_handler(func=lambda message: True)
def main(message):
        if message.text[0] == '/':
                handle.commands(message)


thread = threading.Thread(target=channel)
thread.start()


bot.polling()
