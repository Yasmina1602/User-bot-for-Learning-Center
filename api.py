import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from config import DEFAULT_WELCOME_MESSAGE, WAITING_MESSAGE

app = FastAPI(title="O'quv Markazi UserBot API")

# CORS (Frontend bemalol bog'lanishi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML fayllarini topish papkasi
templates = Jinja2Templates(directory="templates")

JSON_FILE = "clients_data.json"

def get_stats():
    """ JSON bazasidan joriy statistikani o'qib olish """
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "total_clients": len(data.get("known_users", [])),
                "waiting_clients": len(data.get("active_timers", {})),
                "waiting_list": data.get("active_timers", {})
            }
    return {"total_clients": 0, "waiting_clients": 0, "waiting_list": {}}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """ Asosiy Admin Panel sahifasi """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/stats")
async def api_stats():
    """ Dashboard uchun jonli ma'lumot uzatuvchi API """
    return get_stats()

@app.get("/api/settings")
async def api_settings():
    """ Joriy xabarlarni qaytaruvchi API """
    return {
        "welcome_message": DEFAULT_WELCOME_MESSAGE,
        "waiting_message": WAITING_MESSAGE
    }

if __name__ == "__main__":
    import uvicorn
    # API serverni ishga tushirish (8000 dagi zombi jarayonlarga halaqit bermasligi uchun 8080 da ochamiz)
    uvicorn.run(app, host="127.0.0.1", port=8080)
