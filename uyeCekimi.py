from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = ""
api_hash = ""
phone = ""
client = TelegramClient(phone,api_id,api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone,input('Telegram Kodu Giriniz:'))


chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))

chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Uye cekmek istedigin grubu seç:')
i=0

for g in groups:
    print(str(i) + "- " + g.title)
    i+=1

g_index = input("Grubu sec: ")
target_group = groups[int(g_index)]

print("Uyeler aliniyor...")

all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print("Dosyaya Yukleniyor...")

with open("nembers.csv","w",encoding="UTF-8") as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id','access hash','name','group','group id'])

    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = "Username YOK"
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = "Name YOK"
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = "LastName YOK"
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title,target_group.id])

print("Kullanicilar Yuklendi.")
client.disconnect()


        