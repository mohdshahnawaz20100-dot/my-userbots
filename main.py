# main.py
import asyncio
import random
import time
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.users import GetFullUserRequest
from config import (API_ID, API_HASH, SESSION_STRING, OWNER_ID,
                    WEATHER_API_KEY, GEMINI_API_KEY)

# Debug prints
print("=" * 50)
print(f"SESSION_STRING length: {len(SESSION_STRING) if SESSION_STRING else 'NONE'}")
print(f"API_ID: {API_ID}")
print("=" * 50)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ========== SHAYARI ==========
SHAYARI = {
    "love": [
        "तेरे बिना अधूरी है ये ज़िंदगी मेरी,\nतू ही तो है मेरी जान, मेरी बेगम मेरी 💕",
        "मोहब्बत में डूब जाना भी क्या कमाल है,\nतेरे बिना जीना भी क्या बवाल है ❤️",
    ],
    "sad": [
        "अब तो आँसू भी शिकायत करते हैं,\nतेरे बिना दिल में बगावत करते हैं 💔",
    ],
    "miss": [
        "हर रोज़ तेरी कमी खलती है,\nतेरी तस्वीर आँखों में पलती है 💭",
    ],
    "wife": [
        "मेरी बीवी मेरी जान है,\nउसके बिना ये दिल वीरान है 💍",
        "तू मेरी दुनिया, तू मेरी जान,\nतू ही मेरी हर दुआ का जवाब 💖",
    ],
    "dosti": ["दोस्ती में ना कोई दिन ना कोई रात होती है,\nबस यादों की बरसात होती है 🤝"],
    "zindagi": ["ज़िंदगी एक किताब है,\nहर दिन एक नया पन्ना है 📖"],
    "bewafa": ["बेवफाई का गिला क्या करें,\nहम तो उसे भी दुआ देते हैं 💔"],
}

# ========== LOVE MESSAGES ==========
LOVE_MESSAGES = {
    "lovewife": "💖 **मेरी प्यारी बीवी के लिए** 💖\n\nतुम मेरी ज़िंदगी का सबसे हसीन हिस्सा हो,\nमेरी हर खुशी का सबसे प्यारा किस्सा हो।\n\nतेरे बिना अधूरा हूँ मैं,\nतेरे साथ ही पूरा हूँ मैं। 💕\n\nतुम्हारा ही,\nतुम्हारा 💍",
    "jaan": "💗 **मेरी जान,**\n\nतुम हो तो सब कुछ है,\nतुम नहीं तो कुछ भी नहीं।\n\nहमेशा तुम्हारा 💕",
    "missyou": "💭 **I Miss You Jaan** 💭\n\nतेरे बिना ये दिल उदास रहता है,\nहर पल तेरा ही इंतज़ार रहता है 💞",
    "goodnight": "🌙 **Good Night Meri Jaan** 🌙\n\nमीठे सपने तुम्हें मिलें,\nहर खुशी तुम्हें मिले 💖",
    "goodmorning": "🌅 **Good Morning Meri Jaan** 🌅\n\nतेरी सुबह हो हसीन,\nतेरा हर दिन हो रंगीन 💕",
    "sorry": "🙏 **Sorry Meri Jaan** 🙏\n\nGalti ho gayi mujhse,\nMaaf kar do mujhe 💔",
    "propose": "💍 **Will You Be Mine Forever?** 💍\n\nतू मेरी दुनिया, तू मेरी जान,\nतू ही मेरी हर दुआ का जवाब।\n\nहर जनम तुझे ही चाहूँगा 💖",
    "forever": "♾️ **Forever Together** ♾️\n\nना कोई दूरी, ना कोई जुदाई,\nबस तेरे साथ हर जनम 💕",
    "pyar": "❤️ **मेरा प्यार** ❤️\n\nतेरे बिना ये दिल अधूरा है,\nतू मेरी हर खुशी का सबब है 💗",
    "dil": "💓 **Dil Se** 💓\n\nYe dil sirf tumhara hai,\nHar dhadkan tumhara naam leti hai 💖",
    "soulmate": "🫶 **Meri Soulmate** 🫶\n\nतू मेरी रूह का हिस्सा है 💕",
    "kiss": "😘 **Ek Kiss Meri Jaan Ko** 😘",
    "huglove": "🤗 **Warm Hug Meri Jaan** 🤗",
    "wife": "💍 **Meri Biwi Meri Jaan** 💍\n\nतू मेरी दुनिया, तू मेरी जान 💖",
    "begum": "🌹 **Meri Begum** 🌹\n\nतू मेरी बेगम, मैं तेरा शौहर 💕",
    "queen": "👑 **Meri Rani** 👑\n\nतू मेरी रानी, मैं तेरा राजा 💖",
    "jannat": "🌸 **Meri Jannat** 🌸\n\nतू मेरी जन्नत, तू मेरी दुआ 💕",
    "romantic": "✨ **तुम्हारे लिए** ✨\n\nतेरी आँखों में डूब जाना चाहता हूँ,\nतेरी बाहों में खो जाना चाहता हूँ। 💖",
}

# ========== BASIC ==========
@client.on(events.NewMessage(pattern=r'^\.help$'))
async def help_cmd(event):
    await event.reply("""
⚙️ **USERBOT MENU** ⚙️

🔹 **BASIC** → .help .alive .profile .id .ping
🤖 **AI** → .ai <question>
🌤️ **WEATHER** → .weather <city> / .forecast <city>

💕 **LOVE**
.lovewife .jaan .missyou .goodnight
.goodmorning .sorry .propose .forever
.pyar .dil .soulmate .kiss .huglove
.wife .begum .queen .jannat .romantic

💌 **SHAYARI** → .shayari (love/sad/miss/wife/dosti/zindagi/bewafa)
🎲 **FUN** → .flip .dice .hearts <text>
    """)

@client.on(events.NewMessage(pattern=r'^\.alive$'))
async def alive_cmd(event):
    me = await client.get_me()
    await event.reply(f"🤖 **Online**\n👤 {me.first_name}\n💕 Love Mode: ON")

@client.on(events.NewMessage(pattern=r'^\.id$'))
async def id_cmd(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await reply.get_sender()
        await event.reply(f"👤 **ID:** `{user.id}`\n📛 {user.first_name}")
    else:
        sender = await event.get_sender()
        await event.reply(f"👤 **Your ID:** `{sender.id}`")

@client.on(events.NewMessage(pattern=r'^\.ping$'))
async def ping_cmd(event):
    start = time.time()
    msg = await event.reply("🏓 Pinging...")
    end = time.time()
    await msg.edit(f"🏓 **Pong!** `{round((end - start) * 1000)}ms`")

@client.on(events.NewMessage(pattern=r'^\.profile$'))
async def profile_cmd(event):
    sender = await event.get_sender()
    try:
        full = await client(GetFullUserRequest(sender.id))
        bio = full.full_user.about or "No bio"
    except Exception:
        bio = "N/A"
    await event.reply(
        f"👤 **Your Profile**\n"
        f"📛 {sender.first_name or ''} {sender.last_name or ''}\n"
        f"🆔 `{sender.id}`\n"
        f"📝 @{sender.username if sender.username else 'None'}\n"
        f"💬 {bio}"
    )

# ========== LOVE ==========
@client.on(events.NewMessage(
    pattern=r'^\.(lovewife|jaan|missyou|goodnight|goodmorning|sorry|propose|forever|pyar|dil|soulmate|kiss|huglove|wife|begum|queen|jannat|romantic)$'
))
async def love_cmd(event):
    cmd = event.pattern_match.group(1)
    await event.reply(LOVE_MESSAGES.get(cmd, "💕 I Love You!"))

# ========== SHAYARI ==========
@client.on(events.NewMessage(pattern=r'^\.shayari(?:\s+(\w+))?$'))
async def shayari_cmd(event):
    category = event.pattern_match.group(1)
    if not category or category not in SHAYARI:
        category = random.choice(list(SHAYARI.keys()))
    header = {
        "love": "💕 **Love Shayari** 💕",
        "sad": "💔 **Sad Shayari** 💔",
        "miss": "💭 **Miss You Shayari** 💭",
        "wife": "💍 **Wife Special Shayari** 💍",
        "dosti": "🤝 **Dosti Shayari** 🤝",
        "zindagi": "📖 **Zindagi Shayari** 📖",
        "bewafa": "🥀 **Bewafa Shayari** 🥀",
    }.get(category, "✨ **Shayari** ✨")
    await event.reply(f"{header}\n\n{random.choice(SHAYARI[category])}")

# ========== AI ==========
@client.on(events.NewMessage(pattern=r'^\.ai\s+(.+)$'))
async def ai_cmd(event):
    question = event.pattern_match.group(1)
    if not GEMINI_API_KEY:
        await event.reply("❌ GEMINI_API_KEY set nahi hai.")
        return
    wait = await event.reply("🤖 Soch raha hoon...")
    try:
        from google import genai
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
        response = ai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )
        answer = response.text
        if len(answer) > 4000:
            answer = answer[:4000] + "..."
        await wait.edit(f"🤖 **AI:**\n\n{answer}")
    except Exception as e:
        await wait.edit(f"❌ Error: `{str(e)[:200]}`")

# ========== WEATHER ==========
@client.on(events.NewMessage(pattern=r'^\.weather\s+(.+)$'))
async def weather_cmd(event):
    city = event.pattern_match.group(1).strip()
    if not WEATHER_API_KEY:
        await event.reply("❌ WEATHER_API_KEY set nahi hai.")
        return
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        r = requests.get(url, timeout=10).json()
        if str(r.get("cod")) != "200":
            await event.reply(f"❌ City nahi mili: `{city}`")
            return
        await event.reply(
            f"🌤️ **{city.title()}**\n\n"
            f"🌡️ Temp: `{r['main']['temp']}°C`\n"
            f"🤔 Feels: `{r['main']['feels_like']}°C`\n"
            f"💧 Humidity: `{r['main']['humidity']}%`\n"
            f"💨 Wind: `{r['wind']['speed']} m/s`\n"
            f"📝 {r['weather'][0]['description'].title()}"
        )
    except Exception as e:
        await event.reply(f"❌ Error: `{str(e)[:200]}`")

@client.on(events.NewMessage(pattern=r'^\.forecast\s+(.+)$'))
async def forecast_cmd(event):
    city = event.pattern_match.group(1).strip()
    if not WEATHER_API_KEY:
        await event.reply("❌ WEATHER_API_KEY set nahi hai.")
        return
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        r = requests.get(url, timeout=10).json()
        if str(r.get("cod")) != "200":
            await event.reply(f"❌ City nahi mili: `{city}`")
            return
        daily = {}
        for item in r["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = item
        msg = f"🌤️ **5-Day Forecast — {city.title()}**\n\n"
        for date, item in list(daily.items())[:5]:
            msg += f"📅 `{date}` — `{item['main']['temp']}°C` — {item['weather'][0]['description'].title()}\n"
        await event.reply(msg)
    except Exception as e:
        await event.reply(f"❌ Error: `{str(e)[:200]}`")

# ========== FUN ==========
@client.on(events.NewMessage(pattern=r'^\.flip$'))
async def flip_cmd(event):
    await event.reply(random.choice(["🪙 **Heads!**", "🪙 **Tails!**"]))

@client.on(events.NewMessage(pattern=r'^\.dice$'))
async def dice_cmd(event):
    await event.reply(f"🎲 **You rolled: {random.randint(1, 6)}**")

@client.on(events.NewMessage(pattern=r'^\.hearts(?:\s+(.+))?$'))
async def hearts_cmd(event):
    text = event.pattern_match.group(1) or "Love You"
    h = " ".join(["❤️"] * 10)
    await event.reply(f"{h}\n**{text}**\n{h}")

# ========== START ==========
async def main():
    await client.start()
    me = await client.get_me()
    print("=" * 50)
    print("✅ USERBOT STARTED!")
    print(f"👤 {me.first_name} (@{me.username})")
    print(f"🆔 {me.id}")
    print("=" * 50)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
