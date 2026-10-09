import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "user_bot_session")

# Admin notify chat ID (operator javob bermasa shunga ogohlantirish boradi)
NOTIFY_CHAT_ID = os.getenv("NOTIFY_CHAT_ID", "")

# Redis va DB sozlamalari
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Default avto-javob matni (1-marta yozgan mijozlarga)
DEFAULT_WELCOME_MESSAGE = os.getenv(
    "DEFAULT_WELCOME_MESSAGE",
    """
    🎓 *[O'QUV MARKAZI NOMI]* _Bilim sari ishonchli qadam!_

    Assalomu alaykum! 👋
    O'quv markazimizga xush kelibsiz!

    📚 *Bizda siz:*

    🔹 Ingliz tilini Beginner'dan Advanced darajagacha o'rganishingiz
    🔹 IELTS va Milliy sertifikat imtihonlariga tayyorlanishingiz
    🔹 Abituriyentlar uchun fanlardan puxta bilim olishingiz
    🔹 Maktab fanlarini mustahkamlashingiz
    🔹 Individual yoki guruhli mashg'ulotlarda qatnashishingiz mumkin.

    ✨ *Nega aynan biz?*

    ✅ Tajribali va malakali ustozlar
    ✅ Zamonaviy ta'lim metodikasi
    ✅ Har bir o'quvchiga individual yondashuv
    ✅ Muntazam test va natijalar tahlili
    ✅ Natijaga yo'naltirilgan ta'lim

    🎯 *Bizning maqsadimiz —*
    shunchaki bilim berish emas, balki sizga yuqori natijaga erishishda yordam berish!

    📲 *Kurslar, narxlar va dars jadvali haqida ma'lumot olish uchun biz bilan bog'laning.*

    🚀 *Kelajagingiz uchun eng yaxshi investitsiya — bu bilim!*

    📍 *Manzil:* [Manzil]
    📞 *Telefon:* [Telefon raqam]
    💬 *Telegram / Instagram:* [Havola]

    🎓 *[O'QUV MARKAZI NOMI]*
    _Bilim. Natija. Kelajak._
"""
)

# Kutish matni (mijoz javob yozganda operator ulgurmagan bo'lsa)
WAITING_MESSAGE = os.getenv(
    "WAITING_MESSAGE",
    "⏳ Iltimos biroz kuting, operatorlarimiz hozir band. Tez orada sizga albatta javob beramiz!"
)

