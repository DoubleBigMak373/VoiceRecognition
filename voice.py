import pyttsx3

#Инициализация голосового движка
engine = pyttsx3.init()
engine.setProperty("rate", 200) #скорость речи

def speaker(text):
    engine.say(text)
    engine.runAndWait()