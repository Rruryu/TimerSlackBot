# coding: utf-8
import time
import threading
import math

from time import sleep
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

def hour_time(message,clocktime):
    hour1 = math.floor(clocktime/60) #時間
    if hour1>0:
        subtractTime = clocktime-hour1*60 #指定したminuteからhourを引く
        for i in range(hour1):
            sleep(hour1*1800)
            if i == 0:
                message.reply('{}分経過シマシタ'.format(30))
            if i >= 1:
                if i % 2 == 1:
                    message.reply('{}時間経過シマシタ'.format(i/2))
                elif i % 2 == 0:
                    message.reply('{}時間{}分経過シマシタ'.format((i/2),30))
        sleep(subtractTime)
        message.reply('{}時間{}分経過シマシタ。目的ノ時間ニナッタタメ、タイマーヲ終了シマス'.format(hour1,subtractTime))
    else:
        sleep(clocktime*60)
        message.reply('{}分経過シマシタ。目的ノ時間ニナッタタメ、タイマーヲ終了シマス'.format(clocktime))
    



@respond_to('ハロー')
def mention_func(message):
    message.reply('ハローワールド！') # メンション

@respond_to('(.*)分タイマー')
def mention_func2(message,arg1):
    try:
        time1 = int(arg1) #分
        if time1>300:
            message.reply('300分以上ノタイマーニハ対応シテイマセン')
        elif time1<1:
            message.reply('１分以上ニシテクダサイ')
        else:
            if time1>=60:
                hourTime = math.floor(time1/60)
                subtractTime = time1 - hourTime*60
                message.reply('{}時間{}分後オシラセシマス'.format(hourTime,subtractTime))
            else:
                message.reply('{}分後オシラセシマス'.format(time1)) # メンション
        hour_time(message,time1)
    except ValueError:
        message.reply('分ノ前ハ数値ノミ入力シテクダサイ')

@listen_to('暇な人')
def listen_func(message):
    message.send('ワタシハ、テガアイテマスヨ！')      # ただの投稿
    message.reply('ナニカシマショウカ？')                           # メンション