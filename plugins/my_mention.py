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

# minute_time%30 = 0 ならsubtract_time = 0
def timer(message,minute_time):
    SECONDS = 60 
    NOTIFICATION_TIME = 30 #通知時間(分)

    # 通知時間と同じかそれより小さい場合
    if minute_time - NOTIFICATION_TIME <= 0:
        sleep(minute_time*SECONDS)
        message.reply('{}分経過シマシタ... ***{}分未満'.format(minute_time,NOTIFICATION_TIME))
        message.reply('時間ニナッタタメ...タイマーヲ終了シマス ***通知時間未満')
        return


    #通知時間より大きい場合
    # 通知回数分ループを回す
    notification_times = math.floor(minute_time/NOTIFICATION_TIME)  #通知回数
    for i in range(1,notification_times+1): # 通知回数分繰り返し +1はしないといけない
        sleep(NOTIFICATION_TIME*SECONDS) 
        if NOTIFICATION_TIME*i >= 60: #60分 -> 1時間に換算する
            hour_time = math.floor(NOTIFICATION_TIME*i/60)
            message.reply('{}時間{}分経過シマシタ...残リ{}分デス ***i={}'.format(hour_time,NOTIFICATION_TIME*i-hour_time*60,minute_time-NOTIFICATION_TIME*i,i))
        else:
            message.reply('{}分経過シマシタ...残リ{}分デス ***i={}'.format(NOTIFICATION_TIME*i,minute_time-NOTIFICATION_TIME*i,i))

    #通知時間で割り切れない場合(あまりの時間がある場合)
    if minute_time%NOTIFICATION_TIME != 0:
        sleep(minute_time-notification_times*NOTIFICATION_TIME) #図りたい時間 - 通知回数*通知時間
        if minute_time >= 60:
            message.reply('{}時間{}分経過シマシタ... ***アマリアリ'.format(hour_time,minute_time-hour_time*60))
            message.reply('時間ニナッタタメ...タイマーヲ停止シマス')
        else:
            message.reply('{}分経過シマシタ.. ***アマリアリ'.format(minute_time))
            message.reply('時間ニナッタタメ...タイマーヲ停止シマス')
    #通知時間で割り切れた場合
    else:
        message.reply('時間ニナッタタメ...タイマーヲ停止シマス ***アマリナシ')

            


@respond_to('ハロー')
def mention_func(message):
    message.reply('ハローワールド！') # メンション

@respond_to('(.*)分タイマー')
def mention_func2(message,arg1):
    try:
        minute_time = int(arg1) #分
        if minute_time>300:
            message.reply('300分以上ノタイマーニハ対応シテイマセン')
        elif minute_time<1:
            message.reply('１分以上ニシテクダサイ')
        else:
            if minute_time>=60:
                hour_time = math.floor(minute_time/60)
                subtract_time = minute_time - hour_time*60
                message.reply('{}時間{}分後オシラセシマス'.format(hour_time,subtract_time))
            else:
                message.reply('{}分後オシラセシマス'.format(minute_time)) # メンション
        timer(message,minute_time)
    except ValueError:
        message.reply('分ノ前ハ数値ノミ入力シテクダサイ')

@listen_to('暇な人')
def listen_func(message):
    message.send('ワタシハ、テガアイテマスヨ！')      # ただの投稿
    message.reply('ナニカシマショウカ？')                           # メンション