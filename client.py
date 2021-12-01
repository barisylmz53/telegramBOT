from telethon import TelegramClient

name = "sendMessage"
api_id = ""
api_hash = ""

client = TelegramClient(name, api_id, api_hash)

async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello to myself!')

with client:
    client.loop.run_until_complete(main())