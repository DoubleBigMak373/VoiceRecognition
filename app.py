#!/usr/bin/env python3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import sounddevice as sd
import vosk

import queue
import json

import words
from skills import *
import voice


q = queue.Queue()

model = vosk.Model('voice_small') #Голосовая модель vosk, в папке проекта

device = sd.default.device #Будет использоваться устройство ввода звука по умолчанию. python -m sounddevice просмотр устройств.
samplerate = int(sd.query_devices(device[0],'input')['default_samplerate']) #Получаем частоту микрофона.
#48000

def callback(indata, frames, time, status):
    '''
    Добавляет в очередь семплы из потока.
    вызывается каждый раз при наполнении blocksize
    в sd.RawInputStream'''
    q.put(bytes(indata))

def recognize(data,vectorizer,clf): #Анализ распознанной речи
    #Проверяем есть ли имя бота в data
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # Удаляем имя бота из текста
    data.replace(list(trg)[0],'')

    #Получаем вектор текста
    #Сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    # Озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name,""))

    #Запуск функции из skills
    exec(func_name + "()")

def main():
    '''
       Обучаем матрицу ИИ
       и постоянно слушаем микрофон
    '''
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # Постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device= device[0],
                           dtype="int16", channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data,vectorizer,clf)
            #else:
               #print(rec.PartialResult())

if __name__ == "__main__":
    main()