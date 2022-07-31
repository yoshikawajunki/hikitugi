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
import math

import time
from datetime import datetime, timedelta
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from oauth2client.file import Storage


OAUTH_SCOPE = 'http###tivity.read'
DATA_SOURCE = "deri###ted_steps"
REDIRECT_URI = 'urn##2.0:oob'

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
SPREADSHEET_KEY = '1P-Xbx##XTFOUGs'#歩数ログ（DERC用）
point_SPREADSHEET_KEY = '1pCaCy###gh_A'#DDG-database+チャットログ

#共有設定したスプレッドシートを指定
#DB用
workbook = gc2.open_by_key(SPREADSHEET_KEY)
point_workbook = gc.open_by_key(point_SPREADSHEET_KEY)

#スプレッドシートの中のワークシート名を直接指定
worksheet = workbook.worksheet('歩数')
point_worksheet = point_workbook.worksheet('ユーザー関連')

#スプレッドシート操作終わり


all_user =["shikina","shimamoto","komori","shimaoka","hiramoto","asakura","huruyama","banno","morinaga","sumitani","iwata","yamato","test"]
all_user_ID = ["U027Q6WHLE6","U027PK6D0JW","U027QFP2C58","U028326L1MX","U02139ND4DV","U027WGBEYBW","U02837DK4CR","U0283604X89","U01E9ANJQKC","U021WLAQYC9","U028D4W5A8G","U027VRLLCJG","aaa"]



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


def postData(data):#pythonからGASを呼び出すための関数
    if(data is None):
      print("params is empty")
      return False

    print("ここまで")
    payload = {
        "data": data
    }
    url = "https://script.google.com/macros/s/AKfycbw######3gRO-wXhyaXfGV/exec"
    headers = {
        'Content-Type': 'application/json',
    }
    print("ここまで１")
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if(response.status_code == 200 and response.text == "success"):
        print("post success!")
        return True
    print("ここまで３")
    print(json.dumps(payload))
    print(response.text)
    print(response.status_code)
    return False



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



def slackpost(num,kakeperson,kekka,kekkapoint,lv1point,lv12point):#ポイントを更新する関数
  token = "xoxb-11####qAt93OH0c" #歩数通知
  client = WebClient(token)
  #自分のuserID取ってくる
  user_id = all_user_ID[num]#評価相手のslackのIDを取ってくる。
  # DMを開き，channelidを取得する．
  print(user_id)
  res = client.conversations_open(users=user_id)
  dm_id = res['channel']['id']

  # DMを送信する
  client.chat_postMessage(channel=dm_id, text = 
  all_user[num] + "さんが昨日の歩数でレベル１で得たポイントは" + str(lv1point) + "、賭けた人は " + kakeperson + "で賭けの結果は" + kekka + "、レベル1,2により変動するポイントは" + str(lv12point) + "で、あなたの所持ポイントは" + str(kekkapoint) + "になりました。"
  )


def pointupdate(kakeperson,rank,mNumber,kakeozzu,kakepoint,overallpoint,lv1point):#ポイントを更新する関数
  if rank == 0:#1位の場合×1.2
    kakerank = 1.2

  elif rank == 1:#2位の場合×1.1
    kakerank = 1.1

  elif rank == 2:#3位の場合×1
    kakerank = 1
  
  kekka = "seikou"
  updatepoint = math.floor(kakerank * kakeozzu * kakepoint - kakepoint) #更新するポイントは（順位に応じた数値×賭けオッズ×賭けたポイント）math.floorは小数点切り捨て

  point_worksheet.update_cell(3 + mNumber, 5 , updatepoint + overallpoint + lv1point )#全体のポイント
  

  slackpost(mNumber,kakeperson,kekka,updatepoint + overallpoint + lv1point, lv1point ,lv1point + updatepoint)#slackへの投稿

def randomkake():#0~11の中でランダムな数字を吐き出す関数
  return(random.randint(0, 11))

def randomselect():#かけ対象と賭けポイントが決まっていなかったらこの関数で書きこむ。
  all_worksheet_after = np.array(worksheet.get_all_values())
  
  for ooo in range(12):#賭け対象と賭けポイントが決まっていなかったらランダムで決定される作業
    kakeper = all_worksheet_after[ 4 , 28 + ooo]
    if kakeper != all_user[0] and  kakeper != all_user[1] and  kakeper != all_user[2] and  kakeper != all_user[3] and  kakeper != all_user[4] and  kakeper != all_user[5] and  kakeper != all_user[6] and  kakeper != all_user[7] and  kakeper != all_user[8] and  kakeper != all_user[9] and  kakeper != all_user[10] and  kakeper != all_user[11] :#自分の明日賭けている人の名前が何もなかったら、ランダムに書き込む
      num = randomkake()
      for i in range(3):
        if num == ooo:
          num = randomkake()
      worksheet.update_cell( 5, ooo + 29, all_user[num])

    #ポイント数をランダムに書き込む
      num = randomkake()
      for i in range(3):
        if num == ooo:
          num = randomkake()
      worksheet.update_cell( 6, ooo + 29, "2000")


 

def job():
  all_worksheet = np.array(worksheet.get_all_values())#worksheetの全てのログを持ってくる。################################################
  one_row =all_worksheet[:, 0]#1列目を取ってくる（「あ」が並んでる列）長さを取得する。

  
  rownum = 1 #一列目の長さを格納するための変数(最初に+1しておく)
  for a in one_row:
    if a == "あ":
      rownum = rownum + 1
  
  print(rownum)

  Run("./secret/credentials_shikina",rownum,3)#識名君
  Run("./secret/credentials_shimamoto",rownum,4)#しまもとくん
  Run("./secret/credentials_komori",rownum,5)#こもりくん
  Run("./secret/credentials_shimaoka",rownum,6)#しまおかさん
  Run("./secret/credentials_hiramoto",rownum,7)#まさや
  Run("./secret/credentials_asakura",rownum,8)#朝倉君
  Run("./secret/credentials_furuyama",rownum,9)#ふるやまくん
  Run("./secret/credentials_banno",rownum,10)#バンノ
  Run("./secret/credentials_morinaga",rownum,11)#たくま
  Run("./secret/credentials_sumitani",rownum,12)#すみたにさん
  Run("./secret/credentials_iwata",rownum,13)#こうき
  Run("./secret/credentials_yamato",rownum,14)#やまとさん

  

  #以下、歩数を降順にしてslackに投稿


  all_worksheet_after = np.array(worksheet.get_all_values())#歩数取得の更新がされた後のworksheetの全てのログを持ってくる。################################################

  #全員の歩数を配列として取ってくる。
  steplist = all_worksheet_after[rownum - 1]

  lv1point = []
  for ss in range(12):
    lv1point.append(int(steplist[ss + 2])//10)#歩数を1/10して少数点以下切り捨てして、lv1のポイントを計算する。

  steplist_int = []
  #for s in range(len(all_user)):
  for s in range(12):
    steplist_int.append(int(steplist[s + 2])) #降順処理を行うためにstr型からint型へと変換


  #上の二つのmemberlistとsteplist_intを合わせて二次元配列にする。
  list = []
  list = [(all_user[i],steplist_int[i]) for i in range(0, len(steplist_int), 1)]

  #１（歩数）の要素に注目し降順に並び替える。
  list = sorted(list, reverse=True, key=lambda x: x[1]) 

  #評価を通知するプログラム始まり
  OAUTH_TOKEN = "xoxb-1156####At93OH0c" #歩数通知
  CHANNEL_NAME = '#歩数関連'#本当はgeneral
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
    list[11][0] +":" +str(list[11][1]) + "\n" 
    )
  #評価を通知するプログラム終わり

  #歩数を降順にしてslackに投稿終わり

  #1列目にまた新たな「あ」を加える。
  worksheet.update_cell(rownum, 1, "あ")



  ####賭け成功判定以下から####
  #やっていること:
  #昇順にした歩数の順番で自分の1番目が自分の賭けている人の名前ならば賭け成功で1.2倍を、2番目が自分の賭けている人の名前ならば賭け成功で1.1倍を、3番目が自分の賭けている人の名前ならば賭け成功で1.0倍をオッズ*自分の賭けポイントの計算に入れる。1,2,3の中に自分の名前があったらその順位はパスする。
 

  #DDG-database+チャットログの'ユーザー関連'の全てのログを持ってくる。
  all_point_worksheet = np.array(point_worksheet.get_all_values())
  ozzu = []#最初の時点でのオッズを一次元配列で格納

  for t in range(12):
    kakeperson = all_worksheet_after[ (rownum - 8)*3 + 8 , 28 + t]#自分の賭けている人の名前を取ってくる。
    kakepoint = float(all_worksheet_after[ (rownum - 8)*3 + 9 , 28 + t])#自分の賭けている人のポイント数を取ってくる。
    kakeozzu = float(all_worksheet_after[ (rownum - 8)*3 + 7 , 28 + t])#自分の賭けている人のオッズを取ってくる。
    name = all_user[t]#自分の名前を取ってくる。

    overallpoint = float(all_point_worksheet[2 + t , 4])#所持ポイントを格納
    
    
    ozzu.append(all_point_worksheet[2 + t , 7])#最初の時点でのオッズを一次元配列で格納

    
    rankaaa = 0
    for rank in range(4):#範囲を4にしてあるのは最後の一階で失敗の場合の分岐を行うため。
      

      if rank == 3:#
        worksheet.update_cell(3 * (rownum - 8) + 8 , 29 + t, "失敗")
        print(t)
        point_worksheet.update_cell(3 + t , 5 , overallpoint  + lv1point[t] - kakepoint )#全体のポイント
        kekka = "sippai"
        ####歩数関連のデータをslackに投稿する
        #投稿するもの:賭けてた人、賭け成功かどうか、レベル１のポイント、レベル２のポイント、計算後のポイント、
        slackpost(t,kakeperson,kekka,overallpoint  + lv1point[t] - kakepoint, lv1point[t], lv1point[t] - kakepoint )

      
      elif list[rankaaa][0] == kakeperson:#1,2,3位が賭けた相手の名前だったら成功
        print(t + 20)
        worksheet.update_cell(3 * (rownum - 8) + 8 , 29 + t, "成功")
        pointupdate(kakeperson,rank,t,kakeozzu,kakepoint,overallpoint,lv1point[t])
        break
    

      elif list[rankaaa][0] == name:#1,2,3位に自分の名前が入っていたら、
        print(t + 10)
        if list[rankaaa + 1][0] == kakeperson:#1,2,3位が賭けた相手の名前だったら成功
          print(t + 100)
          worksheet.update_cell(3 * (rownum - 8) + 8 , 29 + t, "成功")
          pointupdate(kakeperson,rank,t,kakeozzu,kakepoint,overallpoint,lv1point[t])
          break
        rankaaa = rankaaa + 2
      
      else :
        rankaaa = rankaaa + 1#1,2,3位に賭けた相手の名前がなかったらvを一つずつ足し合わせていく。


  ####賭け成功判定以上まで####

  ####賭けた相手・ポイントを保存する作業・オッズを書き込む作業以下から####

  for retu3 in range(12):#「明日分の賭け対象」セルに入っている情報から「明日分の賭け対象のオッズ」セルにオッズを書き込む。
    ozzuNum = all_user.index(all_worksheet[ 4 , retu3 + 28])
    worksheet.update_cell( 4, retu3 + 29, ozzu[ozzuNum])
  
  postData(rownum)#GASの「歩数計」を呼び出す。

  ####賭けた相手・ポイントを保存する作業・オッズを書き込む作業以上####


def oshirase(bunnshou):
  OAUTH_TOKEN = "xoxb-11567####en5qAt93OH0c"#吉川純輝ワークスペーす
  CHANNEL_NAME = '#歩数関連'#本当はおしらせ
  client = slack.WebClient(token=OAUTH_TOKEN)


  response = client.chat_postMessage(
  channel=CHANNEL_NAME,
  text=bunnshou
  )

def asa():
 oshirase("おはようございます！\n アプリの同期を行ってください\n（Mii fit→(ヘルスケア)→Google fit）")

def yoru():
  oshirase("こんばんは！\n アプリの同期を行ってください！\n（Mii fit→(ヘルスケア)→Google fit）")  

def kakemotivate():
  oshirase("歩数の通知まであと20分です！\n 賭け終わってない方は行ってください！！")  


schedule.every().day.at("23:00").do(job)
schedule.every().day.at("11:00").do(asa)
schedule.every().day.at("22:00").do(yoru)
schedule.every().day.at("22:40").do(kakemotivate)
schedule.every().day.at("22:50").do(randomselect)





while True:
  schedule.run_pending()
  time.sleep(60)