
import telebot
from telebot import types
import requests
import config

bot = telebot.TeleBot(config.bot_token)

icon = {'01d': '☀️', '01n': '🌕',
        '02d': '🌤️', '02n': '☁️',
        '03d': '☁️', '03n': '☁️',
        '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️',
        '10d': '🌦️', '10n': '🌧️',
        '11d': '🌩️', '11n': '🌩️',
        '13d': '❄️', '13n': '❄️',
        '50d': '🌫️', '50n': '🌫️'
        }


@bot.message_handler(commands=["start", "help"])
def welcome(message):
    bot.send_message(message.chat.id, f'Привет <b>{message.from_user.first_name}</b>!\nЧтобы узнать погоду, '
                                      f'\nПросто напиши название города.', parse_mode='html')


@bot.message_handler()
def weather(message: types.Message):
    data = weather_request(message.text)

    if data['cod'] != '404':
        city = data['name']
        main_weather = data['weather'][0]['description']
        temp = int(data['main']['temp'] - 273.15)
        feels = int(data['main']['feels_like'] - 273.15)
        humidity = data['main']['humidity']
        pressure = int(data['main']['pressure'] / 1.333)
        wind = data['wind']['speed']
        weather_icon = data['weather'][0]['icon']
        bot.send_message(message.chat.id, f'<b><ins>{city}</ins> {icon[weather_icon]}{main_weather}</b>\n\n'
                                          f'Температура       <b>{temp}°C</b>\n'
                                          f'Ощущается на     <b>{feels}°C</b>\n'
                                          f'Влажность           <b>{humidity}%</b>\n'
                                          f'Давление             <b>{pressure} мм рт.ст.</b>\n'
                                          f'Ветер                    <b>{wind} м/с</b>', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Я не смог найти такой город 😕\nПопробуй еще раз')


def weather_request(x):
    try:
        api = config.weather_api
        res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={x}&appid={api}&lang=ru')
        print(res.text)
        print(res.json())
        print(res)
        data = res.json()
        return data
    except:
        return


if __name__ == '__main__':
    bot.infinity_polling()
