import asyncio
import os
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import qrcode
from config import API_ID, API_HASH, SESSION_NAME

# Telethon mijozini yaratamiz
client = TelegramClient(SESSION_NAME + "_telethon", API_ID, API_HASH, device_model="PC 64bit", system_version="Windows 10", app_version="1.0")

async def main():
    await client.connect()
    
    if not await client.is_user_authorized():
        qr_login = await client.qr_login()
        print("QR Code yaratilmoqda...")
        
        img = qrcode.make(qr_login.url)
        qr_file = "telegram_qr.png"
        img.save(qr_file)
        
        print("✅ QR Code yaratildi va rasm sifatida ochilmoqda...")
        os.startfile(qr_file)
        
        print("Kutmoqdamiz... (Vaqtingiz: 2 daqiqa)")
        
        try:
            await qr_login.wait(120) 
            print("\n🎉 Muvaffaqiyatli ulandi! Sizning hisobingiz tizimga bog'landi.")
            
        except SessionPasswordNeededError:
            print("\n⚠️ Ikki bosqichli parol (2FA) so'ralmoqda!")
            password = input("Iltimos, Telegram (2FA) parolingizni kiriting: ")
            await client.sign_in(password=password)
            print("\n🎉 Muvaffaqiyatli ulandi! Sizning hisobingiz tizimga bog'landi.")
            
        except Exception as e:
            print(f"\n❌ Xato yuz berdi: {e}")
            
        if os.path.exists(qr_file):
            os.remove(qr_file)
    else:
        print("\n✅ Sessiya allaqachon mavjud va ulangan!")
        
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"Akkaunt egasi: {me.first_name} (@{me.username})")

if __name__ == '__main__':
    client.loop.run_until_complete(main())
