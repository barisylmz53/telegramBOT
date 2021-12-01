from telethon import client
from telethon.client import messages
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import os,sys
import csv
import random
import time

import gonderilecekMesaj

api_id = ""
api_hash = ""
phone = ""

SLEEP_TIME = 30

client = TelegramClient(phone,api_id,api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input("Kodu giriniz: "))


users = []
with open(r"nembers.csv", encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows,None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
    
    print("[1] Kullanici ID ile mesaj at\n[2] Kullanci Adi ile mesaj at")
    mode = int(input("Seciniz: "))

    message = gonderilecekMesaj.message

    for user in users:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = client.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user['id'],user['access_hash'])
        else:
            print("[!] Gecersiz Mod, Cikis yapiliyor..")
            client.disconnect()
            sys.exit()     
        try:
            print("[+] Mesaj su kullaniciya gonderiliyor: ", user['name'])
            client.send_message(receiver,message.format(user['name']))
            print("[+] {} Saniye bekleniyor..".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)
        except PeerFloodError:
            print("[!] Telegram Flood hatasi alindi. \n[!] Program simdilik durduruluyor.\n[!] Daha sonra tekrar dene.")
            client.disconnect()
            sys.exit()
        except Exception as e:
            print("[!] Hata: ",e)
            print("[!] Devam etmeye calisiyorum.")
            continue
    client.disconnect()
    print("Basarili. Tum kullanicilara mesaj gonderildi.")


