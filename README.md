## Обратная связь и просьба сообщества

Привет!  
Я сделал этот эмулятор GNSS COM для короткого теста, он получился довольно узкоспециализированным (работа с NMEA-синтаксисом). Было бы очень интересно узнать ваше мнение:  
- Может ли этот проект быть полезен кому-то ещё?  
- Есть ли идеи по доработке или замечания?

Если у вас есть минутка — просто взгляните на проект и напишите пару слов! Любая обратная связь или просто отзыв будут очень ценны. Спасибо!

---
English version below:

## Feedback & Community Request

Hi!  
I created this GNSS COM emulator as a quick, specialized project for NMEA syntax testing. I’d love to hear your feedback:
- Do you think this could be useful for anyone?
- Any ideas, comments, or suggestions?

Even a quick look or a short comment would mean a lot — thanks!


## Russian
# Вступление
Этот инструмент был создан в качестве помощи с настройкой каких-либо: репитеров GPS, ЭКНИС, РЛС, любительских проектов с использованием GPS.
# Установка
1. Скачайте репозиторий `git clone https://github.com/DanilDanko/GNSS-COM-Emulator.git`
2. Установите зависимости
`pip install -r requirements.txt`
3. Задайте начальные данные в константах в начале кода
4. Запустите код
`python main.py`
5. Введите COM-порт для передачи данных
6. Введите скорость передачи данных
7. Готово! Данные отправляются каждые 2 секунды
# P.S.
Проект будет дополняться по возможности, добавляться новые функции и инструменты

## English
# Introduction
This tool was created to help with the configuration of any GPS repeaters, EGNOS, radar, and amateur projects using GPS.
# Installation
1. Download the repository `git clone https://github.com/DanilDanko/GNSS-COM-Emulator.git`
2. Install the dependencies
`pip install -r requirements.txt`
3. Set the initial data in the constants at the beginning of the code
4. Run the code
`python main.py`
5. Enter the COM-port for data transfer
6. Enter the data transfer rate
7. Done! Data is sent every 2 seconds
# P.S.
The project will be updated as possible, with new features and tools added
