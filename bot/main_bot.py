import asyncio
import json
import logging
import os
from datetime import datetime
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME, DEFAULT_WELCOME_MESSAGE, WAITING_MESSAGE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient(SESSION_NAME + "_telethon", API_ID, API_HASH)

JSON_FILE = "clients_data.json"
TIMER_SECONDS = 60 

def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"known_users": [], "active_timers": {}}

def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def check_timer(user_id, user_name):
    """ Taymer vaqtini tekshiruvchi asinxron funksiya """
    await asyncio.sleep(TIMER_SECONDS)
    
    data = load_data()
    # Taymerni tekshiramiz: Hozirgi taymerni boshlanish vaqtidan hisoblaymiz.
    timer_info = data.get("active_timers", {}).get(str(user_id))
    
    if timer_info:
        timer_start_time = datetime.fromisoformat(timer_info)
        time_diff = (datetime.now() - timer_start_time).total_seconds()
        
        # Agar vaqt farqi haqiqatan ham 60 sekund bo'lsa (ya'ni mijoz qayta yozib vaqtni uzaytirmagan bo'lsa)
        if time_diff >= TIMER_SECONDS - 2: 
            warning_msg = f"⚠️ DIQQAT! Operator mijozga javob bermadi!\n👤 Mijoz: {user_name}\n⏳ Kutish vaqti: {TIMER_SECONDS} soniyadan oshdi."
            
            # Adminga (o'zingizning Saved Messages) xabar yuboriladi
            await client.send_message("me", warning_msg)
            logger.warning(f"[OGOHLANTIRISH] {user_name} ga o'z vaqtida javob berilmadi!")
            
            # Taymerni o'chiramiz (takroriy xabar ketmasligi uchun)
            del data["active_timers"][str(user_id)]
            save_data(data)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_incoming_message(event):
    sender = await event.get_sender()
    if sender.bot:
        return
        
    user_id = str(sender.id)
    user_name = sender.first_name or "Mijoz"
    msg_text = event.text.strip().lower()
    
    data = load_data()
    
    is_new_user = user_id not in data["known_users"]
    
    # 1. Mijoz 1-marta yozsa yoxud "/start" ni yuborsa -> Asosiy xabar boradi
    if is_new_user or msg_text == "/start":
        if is_new_user:
            data["known_users"].append(user_id)
            
        await event.reply(DEFAULT_WELCOME_MESSAGE)
        logger.info(f"Yangi mijozga (yoki /start) avto-javob yuborildi: {user_name}")
        
    # 2. Agar mijoz avval yozgan bo'lsa va yana narsa yozsa -> Kutib turing xabari boradi
    else:
        # Faqatgina, agar operator u mijozga umuman javob berishga ulgurmagan bo'lsagina Kutib turing jo'natamiz.
        # (Agar hohlasangiz har bir xabariga 'kutib turing' borishi ham mumkin, lekin odatda asabga tegmasligi uchun quyidagicha qilinadi)
        if user_id in data.get("active_timers", {}):
            await event.reply(WAITING_MESSAGE)
            logger.info(f"Kutayotgan mijozga 'kutib turing' xabari yuborildi: {user_name}")
        else:
            # Agar oldin javob berilgan (ya'ni taymer o'chgan), lekin bugun yana yozdi
            await event.reply(WAITING_MESSAGE)

    # 3. Taymerni ishga tushiramiz (Mijozning oxirgi xabari qachon kelganini saqlaymiz)
    data.setdefault("active_timers", {})
    data["active_timers"][user_id] = datetime.now().isoformat()
    save_data(data)
    
    # Taymer-nazoratchini chaqiramiz
    asyncio.create_task(check_timer(user_id, user_name))

@client.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
async def handle_outgoing_message(event):
    chat_id = str(event.chat_id)
    
    data = load_data()
    # 4. Operator javob yozganda: Taymer darhol bekor qilinadi.
    if chat_id in data.get("active_timers", {}):
        del data["active_timers"][chat_id]
        save_data(data)
        logger.info(f"✅ Operator {chat_id} ID li mijozga javob berdi. Taymer bekor qilindi.")

async def main():
    await client.start()
    print("--------------------------------------------------")
    print("🤖 UserBot (To'liq Mantiq Rejimi) ishga tushdi!")
    print(f"⏳ Taymer vaqti (ogohlantirish uchun): {TIMER_SECONDS} soniyaga sozlangan.")
    print("Ma'lumotlar bazasi: clients_data.json")
    print("--------------------------------------------------")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
