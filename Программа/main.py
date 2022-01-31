from tkinter import *
from tkinter import ttk
import glob
from tkinter import messagebox
from tkinter import filedialog
import cv2
import random
from random import randint
import ffmpeg
import os

def enc():
    files = glob.glob('frames/*')
    for f in files:
        os.remove(f)
    try:
        (ffmpeg.input(origin_video_file)
         .output('frames/%04d.png',
                 start_number=0)
         .run(capture_stdout=True, capture_stderr=True))
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))

    DIR = "frames/"
    print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    frames = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    img0 = cv2.imread('frames/0000.png', cv2.IMREAD_COLOR)  ###
    height, width = img0.shape[:2]  ###
    #key = input("Введите ключ\n")
    key1 = key.get()
    random.seed(key1)
    #opentext = open('text.txt', encoding='UTF-8')
    opentext = open(origin_text_file, encoding='UTF-8')
    text = opentext.read()
    dlina = len(text)
    a = dlina * 3 + 2
    mass = [-1] * a
    p = 0

    'Заполнение пикселей символами текста'
    while (p < dlina + 1):
        pixel = False
        k = randint(0, frames - 1)  # Номер кадра
        img = cv2.imread('frames/%04d.png' % k, cv2.IMREAD_COLOR)  # Открытие кадра
        h = randint(0, height - 1)  # Поиск свободного пикселя
        w = randint(0, width - 1)
        for j in range(0, p * 3, 3):
            if (mass[j] == k) & (mass[j + 1] == h) & (
                    mass[j + 2] == w):  # Проверка, заполнен ли пиксель
                print("da")
                pixel = True
                break
        if pixel:
            # print(h, w)
            continue
        (b, g, r) = img[h, w]

        'Перевод пикселей в двоичные числа'
        bb = format(b, 'b')  # Синий цвет
        for i in range(8 - len(bb)):
            bb = ('0' + bb)

        gg = format(g, 'b')  # Зеленый цвет
        for i in range(8 - len(gg)):
            gg = ('0' + gg)

        rr = format(r, 'b')  # Красный цвет
        for i in range(8 - len(rr)):
            rr = ('0' + rr)

        'Обработка символа'
        if (p == dlina):
            s = format(0, 'b')  # Последний "нулевой" символ
            for i in range(8 - len(s)):
                s = ('0' + s)  # Расширение до 8 бит
        else:
            s = format(ord(text[p].encode('cp1251')), 'b')  # Получение числа символа
            for i in range(8 - len(s)):
                s = ('0' + s)  # Расширение до 8 бит

        'Заполнение пикселя символом'
        rr = rr[:5] + s[:3]  # Красный цвет
        gg = gg[:6] + s[3:5]  # Зеленый цвет
        bb = bb[:5] + s[5:]  # Синий цвет

        img[h, w] = (int(bb, 2), int(gg, 2), int(rr, 2))  # Перевод цветов в целые числа и сохранение на изображении
        mass[p * 3] = k
        mass[p * 2 + 3] = h  # Сохранение заполненного пикселя
        mass[p * 2 + 3] = w  #
        print("Пиксель №", p, " - номер кадра: ", k, " - высота: ", h, "; широта: ", w)  ###
        cv2.imwrite('frames/%04d.png' % k, img)
        p = p + 1

    # Сборка видео
    (
        ffmpeg
            .input('frames/%04d.png', framerate=24)
            .output('STEG_VIDEO.mp4', codec='copy')
            .overwrite_output()
            .run()
    )
    messagebox.showinfo('Успешно!', "Закодированный видеофайл сохранён")

def dec():
    try:
        (ffmpeg.input(enc_video_file)
         .output('frames2/%04d.png',
                 start_number=0)
         .run(capture_stdout=True, capture_stderr=True))
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))

    DIR = "frames2/"
    print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    frames = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    img = cv2.imread('frames2/0000.png', cv2.IMREAD_COLOR)
    height, width = img.shape[:2]
    #key = input("Введите ключ\n")
    key2 = txt.get()
    random.seed(key2)
    # dlina = 20
    # mass = [-1]*dlina*2
    mass = []
    p = 0
    text = []
    s2 = 1
    while (chr(s2) != chr(0)):
        pixel = False
        k = randint(0, frames - 1)
        img = cv2.imread('frames2/%04d.png' % k, cv2.IMREAD_COLOR)
        h = randint(0, height - 1)
        w = randint(0, width - 1)
        for j in range(0, p * 3, 3):
            if (mass[j] == h) & (mass[j + 1] == w):  # Проверка, пройден ли пиксель
                print("da")
                pixel = True
                break
        if pixel:
            # print(h, w)
            continue
        (b, g, r) = img[h, w]

        'Перевод пикселей в двоичные числа'
        bb = format(b, 'b')  # Синий цвет
        for i in range(8 - len(bb)):
            bb = ('0' + bb)

        gg = format(g, 'b')  # Зеленый цвет
        for i in range(8 - len(gg)):
            gg = ('0' + gg)

        rr = format(r, 'b')  # Красный цвет
        for i in range(8 - len(rr)):
            rr = ('0' + rr)

        s = rr[5:] + gg[6:] + bb[5:]
        s2 = (int(s, 2))  # Извлеченный из пикселя символ
        if (s2 > 192) & (s2 < 255):
            # print(chr(s2 + 848))
            text.append(chr(s2 + 848))
        else:
            # print(chr(s2))
            text.append(chr(s2))
        # mass[p*2] = h     # Сохранение заполненного пикселя
        # mass[p*2+1] = w
        mass.append(k)
        mass.append(h)
        mass.append(w)
        # print("Пиксель №", p, " - высота: ", h, "; широта: ", w)
        p = p + 1
    # for i in range(len(text)):
    #     print(text[i])
    str_a = ''.join(text)
    print(str_a)
    gottext = open('resulttext.txt', 'w', encoding="utf-8")
    gottext.write(str_a)
    vivod.configure(text=str_a)

def opentext():
    global origin_text_file
    origin_text_file = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
    # opentext = open(origin_text_file, encoding='UTF-8')
    # global text

def openvideo():
    global origin_video_file
    origin_video_file = filedialog.askopenfilename(filetypes=(("Videofiles", "*.mp4"), ("all files", "*.*")))
    # global img
    # img = origin_video_file

def openvideo2():
    files = glob.glob('frames2/*')
    for f in files:
        os.remove(f)
    global enc_video_file
    enc_video_file = filedialog.askopenfilename(filetypes=(("Videofiles", "*.mp4"), ("all files", "*.*")))
    # global encimg
    # encimg = enc_video_file

# Интерфейс программы
window = Tk()
window.title("VideoSteg")
window.geometry('550x400')

# Создание вкладок
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Кодирование')
tab_control.add(tab2, text='Декодирование')
# Первая вкладка-----------------------------------------------------------
btn1 = Button(tab1, width=40, height=1, text="Выбрать видеофайл", command = openvideo)
# btn1.grid(column=0, row=0)
btn1.place(x=100, y=10)
btn2 = Button(tab1, width=40, height=1, text="Выбрать исходный текст", command = opentext)
# btn2.grid(column=0, row=1)
btn2.place(x=100, y = 50)
key = Entry(tab1, width=40)
# key1 = key.get()
# txt.grid(column=0, row=3)
key.place(x = 100, y = 95)
lbl1 = Label(tab1, text="Ввод ключа",)
# lbl1.grid(column=1, row=3)
lbl1.place(x = 430, y = 95)
btn3 = Button(tab1, width=40, height=1, text="Закодировать текст", command = enc)
# btn.grid(column=0, row=4)
btn3.place(x = 100, y = 130)
# adigabze = Label(tab1, text="")
# adigabze.grid(column=0, row=5)
# Вторая вкладка-----------------------------------------------------------------
btn = Button(tab2, width=40, height=1, text="Выбрать закодированный видеофайл", command = openvideo2)
btn.place(x = 100, y = 10)
# btn.grid(column=0, row=0)
txt = Entry(tab2, width=40)
txt.place(x = 100, y = 55)
# key2 = txt.get()
# txt.grid(column=0, row=1)
lbl2 = Label(tab2, text="Ввод ключа")
lbl2.place(x = 430, y = 55)
# lbl2.grid(column=1, row=1)
btn = Button(tab2, width=40, height=1, text="Получить исходный текст", command = dec)
btn.place(x = 100, y = 90)
# btn.grid(column=0, row=2)
vivod = Label(tab2, text="")
vivod.place(x = 0, y = 130)
# vivod.grid(column=0, row=3)
tab_control.pack(expand=1, fill='both')
window.mainloop()