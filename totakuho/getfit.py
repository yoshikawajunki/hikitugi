import os
import json
import httplib2
import requests
import gspread
import json
import numpy as np
import slack     #https://blog.imind.jp/entry/2020/03/07/231631
import datetime
import schedule

import time
from datetime import datetime, timedelta
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from oauth2client.file import Storage


OAUTH_SCOPE = 'ht####ad'
DATA_SOURCE = "d#####ps"
REDIRECT_URI = 'ur###oob'

#スプレッドシート操作
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials_GSpread = ServiceAccountCredentials.from_json_keyfile_name('renkei_spreadsheet.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials_GSpread)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
#DB用
SPREADSHEET_KEY = '1V1##bF-jPA'#歩数ログ（研究室運営用）

#共有設定したスプレッドシートを指定
#DB用
workbook = gc.open_by_key(SPREADSHEET_KEY)

#スプレッドシートの中のワークシート名を直接指定
worksheet = workbook.worksheet('歩数')


#スプレッドシート操作終わり




def auth_data(CREDENTIALS_FILE):

    credentials = ""
    
    credentials = Storage(CREDENTIALS_FILE).get()
    
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)

    fitness_service = build('fitness', 'v1', http=http)

    return fitness_service


def retrieve_data(fitness_service, dataset):

    return fitness_service.users().dataSources(). \
        datasets(). \
        get(userId='me', dataSourceId=DATA_SOURCE, datasetId=dataset). \
        execute()


def nanoseconds(nanotime):
    """
    ナノ秒に変換する
    """
    dt = datetime.fromtimestamp(nanotime // 1000000000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def logwrite(date, step):
    with open('./data/step.log', 'a') as outfile:
        outfile.write(str(date) + "," + str(step) + "\n")


def Run(CREDENTIAL,row,col):
    if __name__ == "__main__":

        authdata = auth_data(CREDENTIAL)

        # 前日分のデータを取得
        TODAY = datetime.today() - timedelta(days=1)
        STARTDAY = datetime(TODAY.year, TODAY.month, TODAY.day, 0, 0, 0)
        NEXTDAY = datetime(TODAY.year, TODAY.month, TODAY.day, 23, 59, 59)
        NOW = datetime.today()

        START = int(time.mktime(STARTDAY.timetuple())*1000000000)
        NEXT = int(time.mktime(NEXTDAY.timetuple())*1000000000)
        END = int(time.mktime(NOW.timetuple())*1000000000)
        data_set = "%s-%s" % (START, NEXT)

        while True:

            if END < NEXT:
                break

            dataset = retrieve_data(authdata, data_set)

            starts = []
            ends = []
            values = []
            for point in dataset["point"]:
                if int(point["startTimeNanos"]) > START:
                    starts.append(int(point["startTimeNanos"]))
                    ends.append(int(point["endTimeNanos"]))
                    values.append(point['value'][0]['intVal'])

            print("Steps:{}".format(sum(values)))

            step = sum(values)

            startdate = STARTDAY.date()
            logwrite(startdate, step)

            STARTDAY = STARTDAY + timedelta(days=1)
            NEXTDAY = NEXTDAY + timedelta(days=1)
            START = int(time.mktime(STARTDAY.timetuple())*1000000000)
            NEXT = int(time.mktime(NEXTDAY.timetuple())*1000000000)
            data_set = "%s-%s" % (START, NEXT)

            #スプレッドシートの自分の場所に書き込む
            worksheet.update_cell(row, col, sum(values))

def job():
  worlsheetrowlength =1 + len(worksheet.col_values(1) )#行の長さを取得する。
  print()

  Run("./secret/credentials",worlsheetrowlength,3)#よしかわ
  Run("./secret/credentials_chiba",worlsheetrowlength,4)#ちばくん
  Run("./secret/credentials_anar",worlsheetrowlength,5)#アナラ君
  Run("./secret/credentials_asakura",worlsheetrowlength,6)#朝倉君
  Run("./secret/credentials_sumitani",worlsheetrowlength,7)#すみたにさん
  Run("./secret/credentials_yamato",worlsheetrowlength,8)#やまとさん
  Run("./secret/credentials_hiramoto",worlsheetrowlength,9)#まさや
  Run("./secret/credentials_shikina",worlsheetrowlength,10)#識名君
  Run("./secret/credentials_morinaga",worlsheetrowlength,11)#たくま
  Run("./secret/credentials_banno",worlsheetrowlength,12)#バンノ
  Run("./secret/credentials_shionoya",worlsheetrowlength,13)#塩野谷
  Run("./secret/credentials_iwata",worlsheetrowlength,14)#こうき
  Run("./secret/credentials_furuyama",worlsheetrowlength,15)#ふるやまくん
  Run("./secret/credentials_shimamoto",worlsheetrowlength,16)#しまもとくん
  Run("./secret/credentials_komori",worlsheetrowlength,17)#こもりくん
  Run("./secret/credentials_suzuki",worlsheetrowlength,18)#鈴木先生
  Run("./secret/credentials_naito",worlsheetrowlength,19)#ないとうさん
  Run("./secret/credentials_shimaoka",worlsheetrowlength,20)#しまおかさん
  Run("./secret/credentials_zineb",worlsheetrowlength,21)#ジネブさん
  Run("./secret/credentials_watanabe",worlsheetrowlength,22)#わたなべさん
  Run("./secret/credentials_arita",worlsheetrowlength,23)#有田先生

  #以下、歩数を降順にしてslackに投稿

  #全員の名簿を配列として取ってくる。
  memberlist = worksheet.row_values(4)
  #余分な最初の２つを削除
  memberlist.pop(0)
  memberlist.pop(0)

  print(memberlist)

  #全員の歩数を配列として取ってくる。
  steplist = worksheet.row_values(worlsheetrowlength)
  #余分な最初の１つを削除
  steplist.pop(0)
  steplist.pop(0)

  print(steplist)

  steplist_int= [int(s) for s in steplist]#降順処理を行うためにstr型からint型へと変換


  #上の二つのmemberlistとsteplist_intを合わせて二次元配列にする。
  list = []
  list = [(memberlist[i],steplist_int[i]) for i in range(0, len(steplist_int), 1)]

  #１（歩数）の要素に注目してソート
  list = sorted(list, reverse=True, key=lambda x: x[1]) 

  #評価を通知するプログラム始まり
  OAUTH_TOKEN = 'xoxb-1997033449121-1978769063270-A9MR6m1XagfuZnWcUaZ5c4od' 
  CHANNEL_NAME = '#general'
  client = slack.WebClient(token=OAUTH_TOKEN)


  response = client.chat_postMessage(
  channel=CHANNEL_NAME,
  text=
  "昨日の歩数（敬称略）" + "\n" +
    list[0][0] +":" +str(list[0][1]) + "\n" +
    list[1][0] +":" +str(list[1][1]) + "\n" +
    list[2][0] +":" +str(list[2][1]) + "\n" +
    list[3][0] +":" +str(list[3][1]) + "\n" +
    list[4][0] +":" +str(list[4][1]) + "\n" +
    list[5][0] +":" +str(list[5][1]) + "\n" +
    list[6][0] +":" +str(list[6][1]) + "\n" +
    list[7][0] +":" +str(list[7][1]) + "\n" +
    list[8][0] +":" +str(list[8][1]) + "\n" +
    list[9][0] +":" +str(list[9][1]) + "\n" +
    list[10][0] +":" +str(list[10][1]) + "\n" +
    list[11][0] +":" +str(list[11][1]) + "\n" +
    list[12][0] +":" +str(list[12][1]) + "\n" +
    list[13][0] +":" +str(list[13][1]) + "\n" +
    list[14][0] +":" +str(list[14][1]) + "\n" +
    list[15][0] +":" +str(list[15][1]) + "\n" +
    list[16][0] +":" +str(list[16][1]) + "\n" + 
    list[17][0] +":" +str(list[17][1]) + "\n" +
    list[18][0] +":" +str(list[18][1]) + "\n" +
    list[19][0] +":" +str(list[19][1]) + "\n" +
    list[20][0] +":" +str(list[20][1]) 
    )
  #評価を通知するプログラム終わり

  #歩数を降順にしてslackに投稿終わり



  #1列目にまた新たな「あ」を加える。
  worksheet.update_cell(worlsheetrowlength, 1, "あ")

def oshirase(bunnshou):
  OAUTH_TOKEN = 'xoxb-1###cUaZ5c4od' 
  CHANNEL_NAME = '#おしらせ'
  client = slack.WebClient(token=OAUTH_TOKEN)


  response = client.chat_postMessage(
  channel=CHANNEL_NAME,
  text=bunnshou
  )

def asa():
 oshirase("おはようございます！\n アプリの同期を行ってください\n（Mii fit→(ヘルスケア)→Google fit）")

def yoru():
  oshirase("こんばんは！\n アプリの同期を行ってください！\n（Mii fit→(ヘルスケア)→Google fit）\n昨日の歩数はこの後10時半に発表されます！")  

schedule.every().day.at("22:30").do(job)
schedule.every().day.at("10:00").do(asa)
schedule.every().day.at("21:35").do(yoru)


while True:
  schedule.run_pending()
  time.sleep(60)