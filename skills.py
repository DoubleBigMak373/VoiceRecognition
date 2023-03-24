import os,webbrowser,sys,requests,subprocess, voice


def weather():
    params = {
        "q": "Volgograd",
        "units": "metric",
        "lang": "ru",
        "appid": f"{API_KEY}",
    }
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather",params= params)

        if not response:
            raise
        w = response.json()
        voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов, ощущается, "
                      f"как {round(w['main']['feels_like'])}")
    except:
        voice.speaker('Произошла ошибка при попытке запроса к ресурсу API, проверь код')

def offpc():
    os.system("shutdown \s")
    print("пк выключен")

def browser():
    webbrowser.open("https://www.youtube.com/",new = 2)
    print("браузер запущен")

def game():
    subprocess.Popen("путь к exe")

def offbot():
    sys.exit()

def passive():
    pass