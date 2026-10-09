import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

# Telethon mijozini yaratamiz
client = TelegramClient(SESSION_NAME + "_telethon", API_ID, API_HASH, device_model="PC 64bit", system_version="Windows 10", app_version="1.0")

async def main():
    print("Telethon orqali Telegram'ga ulanmoqdamiz...")
    await client.start()
    print("\n✅ Muvaffaqiyatli ulandik! Sessiya tayyor.")
    me = await client.get_me()
    print(f"Akkaunt: {me.first_name} (@{me.username})")

if __name__ == '__main__':
    client.loop.run_until_complete(main())
