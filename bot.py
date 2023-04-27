import telebot
import Weather
import requests, json
from dotenv import load_dotenv


def weather(city, API_KEY):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        temperature = int(data['main']['temp'] - 273.15)
        return temperature
    else:
        print("Error in HTTP request")


bot = telebot.TeleBot(Weather.telegram_api_key)


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, "Здравствуйте! Я - бот показывающий текущую погоду \U0001F31E по городу.")
    bot.send_message(message.chat.id, "Введите название города, чтобы продолжить")
    bot.register_next_step_handler(msg, print_weather)


def print_weather(message):
    city = message.text
    temperature = weather(city, Weather.weather_api_key)
    msg = bot.reply_to(message, f"Текущая температура: {temperature}°C")
    bot.send_message(message.chat.id, "Введите название города, чтобы продолжить")
    bot.register_next_step_handler(msg, print_weather)


bot.polling()