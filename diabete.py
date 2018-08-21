#!/usr/bin/python
# coding: utf8

import tkinter as tk
from PIL import Image,ImageTk
from tkinter import *
import json
import random
import tempfile
from gtts import gTTS
from snownlp import SnowNLP
import jieba
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import socket
import pyaudio
import wave
import time
import os
import string
from pygame import mixer


mixer.init()
mixer.music.set_volume(0.2)
def speak(sentence):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence,lang='zh-tw')
        tts.save("{}.mp3".format(fp.name))
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()

input=""
recognizer = aiy.cloudspeech.get_recognizer()
button=aiy.voicehat.get_button()
led=aiy.voicehat.get_led()
aiy.audio.get_recorder().start()
q_parse=[]
question=[]
question_parse=[]
parse_s=[]
true=[]
false=[]
true_index=[]
false_index=[]
solution=[]
sin_ques=[]
with open('Q&A.json', encoding='utf-8') as f1:
    data = json.load(f1)
    for i in range(0,17):
        question.append(data[i]['Q'])
        solution.append(data[i]['S'])
        if data[i]['A']=='T':
            true.append(i)
        elif data[i]['A']=='F':
            false.append(i)
t=0
now = 0
for strr in question:
    print('loading ',t,'/17...')
    question_parse.append([])
    temp = []
    temp = jieba.cut(strr,cut_all=False)
    for strr in temp:
        if(strr!='?' and strr !='？' and strr!='「' and strr!='」' and strr!='，' and strr!='【' and strr!='/' and strr!='】' and strr!='...'):
            question_parse[t].append(strr[0])
    t=t+1
s = SnowNLP(question_parse)
true_index = []
false_index = []
def offerque():
    global true_index
    global false_index
    true_index = random.sample(range(len(true)),5)
    false_index = random.sample(range(len(false)),10)
    print (true_index)
    print (false_index)


win=tk.Tk()
win.title("糖尿病迷思趣味問答機器人")
win.geometry('1280x720')
win.configure(bg='white')

bm=PhotoImage(file='/home/pi/AIY-voice-kit-python/src/cat.png')
var = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()
var4 = tk.StringVar()
var7 = tk.StringVar()
img=Label(win,image=bm,textvariable=var,font=('Arial',32),anchor='center')
img.bm=bm
img.pack()

#Title
t = tk.Label(win,text='糖尿病迷思趣味問答機器人',bg='white',fg='blue',font=('Arial',24),width=70,height=3,anchor='center')
t.pack()
t.place(x=0,y=0)

#choose mode
def click_game():
    global true_index
    global false_index
    print(len(false))
    true_index.clear()
    false_index.clear()
    sin_ques.clear()
    offerque()
    for i in range(0,5):
        sin_ques.append([])
        x = random.randint(0,2)
        print(x)
        if x==0:
            sin_ques[i].append(0)
            sin_ques[i].append(true[true_index[i]])
            sin_ques[i].append(false[false_index[2 * i]])
            sin_ques[i].append(false[false_index[2 * i + 1]])
        elif x==1:
            sin_ques[i].append(1)
            sin_ques[i].append(false[false_index[2 * i]])
            sin_ques[i].append(true[true_index[i]])
            sin_ques[i].append(false[false_index[2 * i + 1]])
        elif x==2:
            sin_ques[i].append(2)
            sin_ques[i].append(false[false_index[2 * i]])
            sin_ques[i].append(false[false_index[2 * i + 1]])
            sin_ques[i].append(true[true_index[i]])
  
    p1.place_forget()
    p2.pi=p2.place_info()
    p2.place_forget()
    ch.pi=ch.place_info()
    ch.place_forget()
    #win.update()
    #Question
    qq = tk.Label(win,textvariable=var7,bg='white',fg='black',font=('Arial',20),width=100,height=3,anchor='w')
    qq.pack()
    qq.place(x=0,y=20)
    q = tk.Label(win,textvariable=var,justify=tk.LEFT,bg='white',fg='blue',font=('Arial',20),width=100,height=4,anchor='w')
    q.pack()
    q.place(x=0,y=80)
    score=0
    s = tk.Label(win,textvariable=var3,bg='white',fg='red',font=('Arial',20),width=10,height=2,anchor='w')
    s.pack()
    s.place(x=1100,y=10)    
    var3.set("Score: "+str(score))
    #solution
    ss = tk.Label(win,textvariable=var2,justify=tk.LEFT,bg='white',fg='red',font=('Arial',20),width=75,height=10,anchor='nw')
    ss.pack()
    ss.place(x=0,y=500)
    global context
    context=""
    win.update()
    speak("歡迎來到遊戲模式一局五題單選題請選出正確的選項答對得二十分滿分為一百決定答案後按下按鈕說出你的答案答完後若有疑問可以按下按紐後問我為什麼或是直接進入下一題.......要開始囉")
    time.sleep(21)
    global now
    for i in range(0,5):
        talked=0
        now = i
        var7.set("Question"+str(now+1)+":")
        qaq=0
        s1 = '(1)'+question[sin_ques[i][1]]+'\n'+'(2)'+question[sin_ques[i][2]]+'\n'+'(3)'+question[sin_ques[i][3]]
        var.set(s1)
        s1+=".........決定後請按下按鈕說出一個答案"
        speak('第' + str(now+1) + '題............'+s1)
        win.update()
        while(True):
            print('Press button and speak')
            button.wait_for_press()
            print('Listening...')
            text=recognizer.recognize()
            print(text)
            if text is None:
                 print('Sorry, I did not hear you.')
                 speak("再說一次啦我沒聽到")
            elif '第一' in text:
                if talked==1:
                    speak('已經答過囉')
                elif sin_ques[now][0]==0 and talked==0:
                    speak('答對了')
                    var2.set('答對了')
                    score+=20
                    var3.set("Score: "+str(score))
                    win.update()
                    talked=1
                else:
                    if talked ==0:
                        speak('哭哭答錯了')
                        var2.set('哭哭答錯了')
                        win.update()
                        talked=1
                qaq=1
            elif '第二' in text:
                if talked==1:
                    speak('已經答過囉')
                elif sin_ques[now][0]==1 and talked==0:
                    speak('答對了')
                    var2.set('答對了')
                    score+=20
                    var3.set("Score: "+str(score))
                    win.update()
                    talked=1
                else:
                    if talked==0:
                        speak('哭哭答錯了')
                        var2.set('哭哭答錯了')
                        win.update()
                        talked=1
                qaq=1
            elif '第三' in text:
                if talked==1:
                    speak('已經答過囉')
                elif sin_ques[now][0]==2 and talked==0:
                    speak('答對了')
                    var2.set('答對了')
                    score+=20
                    var3.set("Score: "+str(score))
                    win.update()
                    talked=1
                else:
                    if talked ==0:
                        speak('哭哭答錯了')
                        var2.set('哭哭答錯了')
                        win.update()
                        talked=1
                qaq=1
            elif '詳解'in text or '為什麼' in text or '為啥' in text or '為何' in text or '壞' in text:
                if qaq==1:
                    hit_me()
                    win.update()
                else:
                    speak('請不要耍見喔')
            elif '下題' in text or '下一題' in text or '再來' in text or '結果' in text:
                if qaq==1:
                    var2.set("")
                    break
                else: 
                    speak('請不要耍見喔')
            else:
                speak('再說一次拜託')
    var.set("你的分數為"+str(score)+"!!!")
    win.update()
    speak("你的分數為"+str(score))
    time.sleep(5)    
    q.place_forget()
    q.pi=q.place_info()
    s.place_forget()
    s.pi=s.place_info()
    ss.place_forget()
    ss.pi=ss.place_info()
    qq.place_forget()
    qq.pi=qq.place_info()
    
    p1.place(p1.pi)
    p2.place(p2.pi)
    ch.place(ch.pi)            

    win.update()
    startgame()
    
               
def click_qaa():
    var2.set("")
    p1.place_forget()
    p2.pi=p2.place_info()
    p2.place_forget()
    ch.pi=ch.place_info()
    ch.place_forget()

    ques = tk.Label(win,textvariable=var4,bg='white',fg='red',font=('Arial',20),width=100,height=3,anchor='w')
    var4.set('請說出你的問題...')
    ques.pack()
    ques.place(x=0,y=80)
    speak('請說出你的問題...')
    win.update()   
    ans = tk.Label(win,textvariable=var3,bg='white',fg='red',font=('Arial',20),width=100,height=3,anchor='w')
    ans.pack()
    ans.place(x=0,y=500)
    while True:
        print('Press button and speak')
        button.wait_for_press()
        print('Listening...')
        text=recognizer.recognize()
        if text is None:
            print('Sorry, I did not hear you.')
            speak("再說一次啦我沒聽到")
        elif '離開' in text:
            p1.place(p1.pi)
            p2.place(p2.pi)
            ch.place(ch.pi)
            
            ques.pi=ques.place_info()
            ques.place_forget()
            ans.pi=ans.place_info()
            ans.place_forget()
            startgame()
        else:
            input = jieba.cut(text,cut_all=False)
            for str in input:
                q_parse.append(str[0])
            x = s.sim(q_parse)
            print('Q:',text)
            index_of_max = x.index(max(x))
            print('X:',x)
            tmp=0
            for k in x:
                tmp = tmp +k 
            q_parse.clear()
            print('A:',solution[index_of_max],index_of_max)
            if tmp==0:
                speak('沒有相關的問題喔')
            else:
                speak(solution[index_of_max])
                var4.set(question[index_of_max])
                var3.set(solution[index_of_max])
                win.update()
 
p1 = tk.Button(win,text='遊戲模式',bg='cyan',fg='red',font=('Arial',20),width=20,height=3,anchor='center',command=click_game)
p1.pack()
p1.place(x=520,y=200)
p1.pi=p1.place_info()
p2 = tk.Button(win,text='問答模式',bg='cyan',fg='red',font=('Arial',20),width=20,height=3,anchor='center',command=click_qaa)
p2.pack()
p2.place(x=520,y=400)
ch = tk.Label(win,text='請選擇模式',bg='white',fg='red',font=('Arial',20),width=20,height=3,anchor='center')
ch.pack()
ch.place(x=520,y=520)

ques = tk.Label(win,text='請說出你的問題...',bg='cyan',fg='red',font=('Arial',20),width=20,height=3,anchor='center')
context=""
on_hit = False
def hit_me():
    global on_hit
    global context
    if on_hit==False:
        if sin_ques[now][0]==0:
            context="正解為選項(1)"+"\n選項(2)"+solution[sin_ques[now][2]]+"\n選項(3)"+solution[sin_ques[now][3]]
            var2.set(context)
            speak(context)
        elif sin_ques[now][0]==1:
            context="正解為選項(2)"+"\n選項(1)"+solution[sin_ques[now][1]]+"\n選項(3)"+solution[sin_ques[now][3]]
            var2.set(context)
            speak(context)
        elif sin_ques[now][0]==2:
            context="正解為選項(3)"+"\n選項(1)"+solution[sin_ques[now][1]]+"\n選項(2)"+solution[sin_ques[now][2]]
            var2.set(context)
            speak(context)
     
def startgame():
    var.set("")
    var2.set("")
    var3.set("")
    var7.set("")
    win.update()
    global button
    speak("請選擇模式")
    while(True):
        print('Press button and speak')
        button.wait_for_press()
        print('Listening...')
        text=recognizer.recognize()
        print(text)
        if text is None:
            print('Sorry, I did not hear you.')
            speak("再說一次啦我沒聽到")
        elif '遊戲' in text:
            click_game()
            break
        elif '問答' in text:
            click_qaa()
            break
        else:
            speak('沒有這種模式喔')
startgame()
win.mainloop()
