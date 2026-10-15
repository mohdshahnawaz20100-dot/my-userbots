print(f"🔍 SESSION_STRING length: {len(SESSION_STRING) if SESSION_STRING else 'NONE'}")
print(f"🔍 API_ID: {API_ID}")# main.py
import asyncio
import random
import time
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.users import GetFullUserRequest
from config import (API_ID, API_HASH, SESSION_STRING, OWNER_ID,
                    WEATHER_API_KEY, GEMINI_API_KEY)

# ============================================
# 🤖 CLIENT SETUP (StringSession)
# ============================================
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ============================================
# 💕 SHAYARI COLLECTION
# ============================================
SHAYARI = {
    "love": [
        "तेरे बिना अधूरी है ये ज़िंदगी मेरी,\nतू ही तो है मेरी जान, मेरी बेगम मेरी 💕",
        "मोहब्बत में डूब जाना भी क्या कमाल है,\nतेरे बिना जीना भी क्या बवाल है ❤️",
        "तेरी आँखों में डूब जाना चाहता हूँ,\nतेरी बाहों में खो जाना चाहता हूँ 💗",
    ],
    "sad": [
        "अब तो आँसू भी शिकायत करते हैं,\nतेरे बिना दिल में बगावत करते हैं 💔",
        "टूट कर बिखरना भी एक फन है,\nमुस्कुरा कर जीना भी एक जुनून है 🥀",
    ],
    "miss": [
        "हर रोज़ तेरी कमी खलती है,\nतेरी तस्वीर आँखों में पलती है 💭",
        "तेरे बिना ये दिल उदास रहता है,\nहर पल तेरा ही इंतज़ार रहता है 💞",
    ],
    "wife": [
        "मेरी बीवी मेरी जान है,\nउसके बिना ये दिल वीरान है 💍",
        "तू मेरी दुनिया, तू मेरी जान,\nतू ही मेरी हर दुआ का जवाब 💖",
        "सात फेरे, सात वचन,\nतू मेरी है हर जनम 🌹",
    ],
    "dosti": [
        "दोस्ती में ना कोई दिन ना कोई रात होती है,\nबस यादों की बरसात होती है 🤝",
    ],
    "zindagi": [
        "ज़िंदगी एक किताब है,\nहर दिन एक नया पन्ना है 📖",
    ],
    "bewafa": [
        "बेवफाई का गिला क्या करें,\nहम तो उसे भी दुआ देते हैं 💔",
    ],
}

# ============================================
# 💕 LOVE MESSAGES
# ============================================
LOVE_MESSAGES = {
    "lovewife": "💖 **मेरी प्यारी बीवी के लिए** 💖\n\nतुम मेरी ज़िंदगी का सबसे हसीन हिस्सा हो,\nमेरी हर खुशी का सबसे प्यारा किस्सा हो।\n\nतेरे बिना अधूरा हूँ मैं,\nतेरे साथ ही पूरा हूँ मैं। 💕\n\nतुम्हारा ही,\nतुम्हारा 💍",
    "jaan": "💗 **मेरी जान,**\n\nतुम हो तो सब कुछ है,\nतुम नहीं तो कुछ भी नहीं।\n\nहमेशा तुम्हारा 💕",
    "missyou": "💭 **I Miss You Jaan** 💭\n\nतेरे बिना ये दिल उदास रहता है,\nहर पल तेरा ही इंतज़ार रहता है 💞",
    "goodnight": "🌙 **Good Night Meri Jaan** 🌙\n\nमीठे सपने तुम्हें मिलें,\nहर खुशी तुम्हें मिले 💖\n\nSweet dreams my love 😘",
    "goodmorning": "🌅 **Good Morning Meri Jaan** 🌅\n\nतेरी सुबह हो हसीन,\nतेरा हर दिन हो रंगीन 💕",
    "sorry": "🙏 **Sorry Meri Jaan** 🙏\n\nGalti ho gayi mujhse,\nMaaf kar do mujhe 💔\n\nTumhare bina kuch acha nahi lagta 💗",
    "propose": "💍 **Will You Be Mine Forever?** 💍\n\nतू मेरी दुनिया, तू मेरी जान,\nतू ही मेरी हर दुआ का जवाब।\n\nहर जनम तुझे ही चाहूँगा,\nहर जनम तुझसे ही प्यार करूँगा 💖",
    "forever": "♾️ **Forever Together** ♾️\n\nना कोई दूरी, ना कोई जुदाई,\nबस तेरे साथ हर जनम 💕",
    "pyar": "❤️ **मेरा प्यार** ❤️\n\nतेरे बिना ये दिल अधूरा है,\nतू मेरी हर खुशी का सबब है 💗",
    "dil": "💓 **Dil Se** 💓\n\nYe dil sirf tumhara hai,\nHar dhadkan tumhara naam leti hai 💖",
    "soulmate": "🫶 **Meri Soulmate** 🫶\n\nतू मेरी रूह का हिस्सा है,\nतू मेरी हर साँस का सबब है 💕",
    "kiss": "😘 **Ek Kiss Meri Jaan Ko** 😘\n\nतेरे होंठों की मिठास,\nमेरे दिल की आस 💗",
    "huglove": "🤗 **Warm Hug Meri Jaan** 🤗\n\nतेरी बाहों में खो जाना,\nहर दर्द भुला जाना 💕",
    "wife": "💍 **Meri Biwi Meri Jaan** 💍\n\nतू मेरी दुनिया, तू मेरी जान,\nतू ही मेरी हर दुआ का जवाब 💖",
    "begum": "🌹 **Meri Begum** 🌹\n\nतू मेरी बेगम, मैं तेरा शौहर,\nतू मेरी दुनिया, मैं तेरा घर 💕",
    "queen": "👑 **Meri Rani** 👑\n\nतू मेरी रानी, मैं तेरा राजा,\nतू मेरी जान, मैं तेरा जहाँ 💖",
    "jannat": "🌸 **Meri Jannat** 🌸\n\nतू मेरी जन्नत, तू मेरी दुआ,\nतू मेरी हर खुशी का सबब 💕",
    "romantic": "✨ **तुम्हारे लिए** ✨\n\nतेरी आँखों में डूब जाना चाहता हूँ,\nतेरी बाहों में खो जाना चाहता हूँ।\nतू मेरी है, बस मेरी ही रहे,\nहर जनम तुझे ही पाना चाहता हूँ। 💖",
}

# ============================================
# ⚙️ BASIC COMMANDS
# ============================================
@client.on(events.NewMessage(pattern=r'^\.help$'))
async def help_cmd(event):
    await event.reply("""
⚙️ **USERBOT MENU** ⚙️

🔹 **BASIC**
.help .alive .profile .id .ping

🤖 **AI**
.ai <question> — Ask anything

🌤️ **WEATHER**
.weather <city> — Weather report
.forecast <city> — 5-day forecast

💕 **LOVE MENU**
.lovewife .jaan .missyou .goodnight
.goodmorning .sorry .propose .forever
.pyar .dil .soulmate .kiss .huglove
.wife .begum .queen .jannat .romantic

💌 **SHAYARI**
.shayari — random
.shayari love / sad / miss / wife
.shayari dosti / zindagi / bewafa

🎲 **FUN**
.flip .dice .hearts <text>
    """)


@client.on(events.NewMessage(pattern=r'^\.alive$'))
async def alive_cmd(event):
    me = await client.get_me()
    await event.reply(
        f"🤖 **Userbot Online**\n"
        f"👤 {me.first_name}\n"
        f"⚡ Status: Running\n"
        f"💕 Love Mode: ON"
    )


@client.on(events.NewMessage(pattern=r'^\.id$'))
async def id_cmd(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await reply.get_sender()
        await event.reply(f"👤 **User ID:** `{user.id}`\n📛 **Name:** {user.first_name}")
    else:
        sender = await event.get_sender()
        await event.reply(f"👤 **Your ID:** `{sender.id}`")


@client.on(events.NewMessage(pattern=r'^\.ping$'))
async def ping_cmd(event):
    start = time.time()
    msg = await event.reply("🏓 Pinging...")
    end = time.time()
    await msg.edit(f"🏓 **Pong!**\n⚡ Latency: `{round((end - start) * 1000)}ms`")


@client.on(events.NewMessage(pattern=r'^\.profile$'))
async def profile_cmd(event):
    sender = await event.get_sender()
    try:
        full = await client(GetFullUserRequest(sender.id))
        bio = full.full_user.about or "No bio"
    except Exception:
        bio = "N/A"

    text = (
        f"👤 **Your Profile**\n"
        f"📛 Name: {sender.first_name or ''} {sender.last_name or ''}\n"
        f"🆔 ID: `{sender.id}`\n"
        f"📝 Username: @{sender.username if sender.username else 'None'}\n"
        f"💬 Bio: {bio}"
    )
    await event.reply(text)


# ============================================
# 💕 LOVE COMMANDS
# ============================================
@client.on(events.NewMessage(
    pattern=r'^\.(lovewife|jaan|missyou|goodnight|goodmorning|sorry|propose|forever|pyar|dil|soulmate|kiss|huglove|wife|begum|queen|jannat|romantic)$'
))
async def love_cmd(event):
    cmd = event.pattern_match.group(1)
    msg = LOVE_MESSAGES.get(cmd, "💕 I Love You!")
    await event.reply(msg)


# ============================================
# 💌 SHAYARI COMMAND
# ============================================
@client.on(events.NewMessage(pattern=r'^\.shayari(?:\s+(\w+))?$'))
async def shayari_cmd(event):
    category = event.pattern_match.group(1)
    if not category or category not in SHAYARI:
        category = random.choice(list(SHAYARI.keys()))

    shayari = random.choice(SHAYARI[category])
    header = {
        "love": "💕 **Love Shayari** 💕",
        "sad": "💔 **Sad Shayari** 💔",
        "miss": "💭 **Miss You Shayari** 💭",
        "wife": "💍 **Wife Special Shayari** 💍",
        "dosti": "🤝 **Dosti Shayari** 🤝",
        "zindagi": "📖 **Zindagi Shayari** 📖",
        "bewafa": "🥀 **Bewafa Shayari** 🥀",
    }.get(category, "✨ **Shayari** ✨")

    await event.reply(f"{header}\n\n{shayari}")


# ============================================
# 🤖 AI COMMAND (Gemini)
# ============================================
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


# ============================================
# 🌤️ WEATHER COMMAND
# ============================================
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

        temp = r["main"]["temp"]
        feels = r["main"]["feels_like"]
        humidity = r["main"]["humidity"]
        desc = r["weather"][0]["description"].title()
        wind = r["wind"]["speed"]

        msg = (
            f"🌤️ **Weather — {city.title()}**\n\n"
            f"🌡️ Temp: `{temp}°C`\n"
            f"🤔 Feels like: `{feels}°C`\n"
            f"💧 Humidity: `{humidity}%`\n"
            f"💨 Wind: `{wind} m/s`\n"
            f"📝 {desc}"
        )
        await event.reply(msg)
    except Exception as e:
        await event.reply(f"❌ Error: `{str(e)[:200]}`")


# ============================================
# 🌤️ FORECAST COMMAND
# ============================================
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
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"].title()
            msg += f"📅 `{date}`\n🌡️ {temp}°C — {desc}\n\n"

        await event.reply(msg)
    except Exception as e:
        await event.reply(f"❌ Error: `{str(e)[:200]}`")


# ============================================
# 🎲 FUN COMMANDS
# ============================================
@client.on(events.NewMessage(pattern=r'^\.flip$'))
async def flip_cmd(event):
    await event.reply(random.choice(["🪙 **Heads!**", "🪙 **Tails!**"]))


@client.on(events.NewMessage(pattern=r'^\.dice$'))
async def dice_cmd(event):
    await event.reply(f"🎲 **You rolled: {random.randint(1, 6)}**")


@client.on(events.NewMessage(pattern=r'^\.hearts(?:\s+(.+))?$'))
async def hearts_cmd(event):
    text = event.pattern_match.group(1) or "Love You"
    hearts = " ".join(["❤️"] * 10)
    await event.reply(f"{hearts}\n**{text}**\n{hearts}")


# ============================================
# 🚀 START
# ============================================
async def main():
    await client.start()
    me = await client.get_me()
    print("=" * 50)
    print("✅ USERBOT STARTED!")
    print(f"👤 Logged in as: {me.first_name} (@{me.username})")
    print(f"🆔 ID: {me.id}")
    print("💕 Love Mode: ON")
    print("=" * 50)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
