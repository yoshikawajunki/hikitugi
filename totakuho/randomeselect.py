#やっていること
#全員分の歩数を取得して「歩数ログ（DERC用）」に反映
#賭け成功/失敗を判定して書きこむ
#成功失敗に応じて、「DDG-database+チャットログ」にポイントを反映させる。
#歩数ログ(DERC)の今日分の賭け対象の～を消去して、明日分の賭けポイント～の部分を空にする。オッズを取得する。


import os
import json
import httplib2
import requests
import gspread
import json
import numpy as np
import slack     #https://blog.imind.jp/entry/2020/03/07/231631
from slack_sdk import WebClient
import datetime
import schedule
import random

import time
from datetime import datetime, timedelta
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from oauth2client.file import Storage


OAUTH_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'
DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

#スプレッドシート操作
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
#アクセス権限をオーバーしてしまうので、二つのgoogleアカウントを使用する。無印は「DDG-database+チャットログ」、2は「歩数ログ（DERC用）」
credentials_GSpread = ServiceAccountCredentials.from_json_keyfile_name('renkei_spreadsheet.json', scope)
credentials_GSpread2 = ServiceAccountCredentials.from_json_keyfile_name('renkei_spreadsheet2.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials_GSpread)
gc2 = gspread.authorize(credentials_GSpread2)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
#DB用
SPREADSHEET_KEY = '1P-XbxGTu9J2Tj5lEPCpkK7AOZrGzWOPFkPNEXTFOUGs'#歩数ログ（DERC用）
point_SPREADSHEET_KEY = '1pCaCydc3e2RiOigvN0demqvrCrGF20rv9sE88MHgh_A'#DDG-database+チャットログ

#共有設定したスプレッドシートを指定
#DB用
workbook = gc2.open_by_key(SPREADSHEET_KEY)
point_workbook = gc.open_by_key(point_SPREADSHEET_KEY)

#スプレッドシートの中のワークシート名を直接指定
worksheet = workbook.worksheet('歩数')
point_worksheet = point_workbook.worksheet('ユーザー関連')

#スプレッドシート操作終わり


all_user =["shikina","shimamoto","komori","shimaoka","hiramoto","asakura","huruyama","banno","morinaga","sumitani","iwata","yamato","test"]
all_user_ID = ["U027Q6WHLE6","U027PK6D0JW","U027QFP2C58","U028326L1MX","U02139ND4DV","U027WGBEYBW","U027VRLLCJG","U027VRLLCJG","U01E9ANJQKC","U021WLAQYC9","U028D4W5A8G","U027VRLLCJG"]


  #以下、歩数を降順にしてslackに投稿
def randomkake():#0~11の中でランダムな数字を吐き出す関数
  return(random.randint(0, 11))


all_worksheet_after = np.array(worksheet.get_all_values())#歩数取得の更新がされた後のworksheetの全てのログを持ってくる。################################################


  ####賭けた相手・ポイントを保存する作業・オッズを書き込む作業以下から####

for ooo in range(12):#賭け対象と賭けポイントが決まっていなかったらランダムで決定される作業
  if all_worksheet_after[ 4 , 28 + ooo] == " ":#自分の明日賭けている人の名前が何もなかったら、ランダムに書き込む
    num = randomkake()
    for i in range(3):
      if num == ooo:
        num = randomkake()
    worksheet.update_cell( 5, ooo + 29, all_user[num])

  if all_worksheet_after[ 5 , 28 + ooo] == " ":#自分の明日賭けている人のポイント数が何もなかったら、ランダムに書き込む
    num = randomkake()
    for i in range(3):
      if num == ooo:
        num = randomkake()
    worksheet.update_cell( 6, ooo + 29, "2000")



  ####賭けた相手・ポイントを保存する作業・オッズを書き込む作業以上####


