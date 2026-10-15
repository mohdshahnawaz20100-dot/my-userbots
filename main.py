# main.py
from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
import asyncio
import random
import os
from config import API_ID, API_HASH, SESSION_NAME, OWNER_ID

from config import API_ID, API_HASH, SESSION_STRING, OWNER_ID, WEATHER_API_KEY, GEMINI_API_KEY

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
    "default": [
        "तेरे बिना अधूरी है ये ज़िंदगी मेरी,\nतू ही तो है मेरी जान 💕",
    ],
}

# ============================================
# 💕 LOVE MESSAGES
# ============================================
LOVE_MESSAGES = {
    "lovewife": """
💖 **मेरी प्यारी बीवी के लिए** 💖

तुम मेरी ज़िंदगी का सबसे हसीन हिस्सा हो,
मेरी हर खुशी का सबसे प्यारा किस्सा हो।

तेरे बिना अधूरा हूँ मैं,
तेरे साथ ही पूरा हूँ मैं। 💕

तुम्हारा ही,
तुम्हारा 💍
""",
    "jaan": "💗 **मेरी जान,**\n\nतुम हो तो सब कुछ है,\nतुम नहीं तो कुछ भी नहीं।\n\nहमेशा तुम्हारा 💕",
    "missyou": "💭 **I Miss You Jaan** 💭\n\nतेरे बिना ये दिल उदास रहता है,\nहर पल तेरा ही इंतज़ार रहता है 💞",
    "goodnight": "🌙 **Good Night Meri Jaan** 🌙\n\nमीठे सपने तुम्हें मिलें,\nहर खुशी तुम्हें मिले 💖\n\nSweet dreams my love 😘",
    "goodmorning": "🌅 **Good Morning Meri Jaan** 🌅\n\nतेरी सुबह हो हसीन,\nतेरा हर दिन हो रंगीन 💕",
    "sorry": "🙏 **Sorry Meri Jaan** 🙏\n\nGalti ho gayi mujhse,\nMaaf kar do mujhe 💔\n\nTumhare bina kuch acha nahi lagta 💗",
    "propose": """
💍 **Will You Be Mine Forever?** 💍

तू मेरी दुनिया, तू मेरी जान,
तू ही मेरी हर दुआ का जवाब।

हर जनम तुझे ही चाहूँगा,
हर जनम तुझसे ही प्यार करूँगा 💖
""",
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
    "romantic": """
✨ **तुम्हारे लिए** ✨

तेरी आँखों में डूब जाना चाहता हूँ,
तेरी बाहों में खो जाना चाहता हूँ।
तू मेरी है, बस मेरी ही रहे,
हर जनम तुझे ही पाना चाहता हूँ। 💖
""",
}

# ============================================
# ⚙️ BASIC COMMANDS
# ============================================
@client.on(events.NewMessage(pattern=r'^\.help$'))
async def help_cmd(event):
    menu = """
⚙️ **USERBOT MENU** ⚙️

🔹 **BASIC**
.help .alive .profile .id .info

🤖 **AI**
.ai <question>

📥 **DOWNLOAD**
.dl <link> — Insta/TikTok/FB/Twitter
.play <song> — YouTube
.save .saveaudio .savemsg

👤 **PROFILE**
.clone .reclone .ghost .unghost
.saveprofile .restoreprofile

🛡️ **ADMIN**
.admins .addadmin .deladmin
.mute .unmute .gmute .gunmute
.ban .unban .lock .unlock

👥 **GROUP**
.tagall .tagall2 .stoptag
.raid .purge .throw .stop

💕 **LOVE MENU**
.lovewife .jaan .missyou .goodnight
.goodmorning .sorry .propose .forever
.pyar .dil .soulmate .kiss .huglove
.wife .begum .queen .jannat .romantic

💌 **SHAYARI**
.shayari — random
.shayari love / sad / miss / wife
.shayari dosti / zindagi / bewafa

🎵 **MUSIC**
.lyrics .songinfo .spotify .trending

🎨 **FUN**
.ping .flip .dice
.animate .spinner .matrix .hearts
    """
    await event.reply(menu)


@client.on(events.NewMessage(pattern=r'^\.alive$'))
async def alive_cmd(event):
    await event.reply("🤖 **Userbot Online**\n⚡ Status: Running\n💕 Love Mode: ON")


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
    import time
    start = time.time()
    msg = await event.reply("🏓 Pinging...")
    end = time.time()
    await msg.edit(f"🏓 **Pong!**\n⚡ Latency: `{round((end - start) * 1000)}ms`")


# ============================================
# 💕 LOVE COMMANDS HANDLER
# ============================================
@client.on(events.NewMessage(pattern=r'^\.(lovewife|jaan|missyou|goodnight|goodmorning|sorry|propose|forever|pyar|dil|soulmate|kiss|huglove|wife|begum|queen|jannat|romantic)$'))
async def love_cmd(event):
    cmd = event.pattern_match.group(1)
    msg = LOVE_MESSAGES.get(cmd, "💕 I Love You!")
    await event.reply(msg)


# ============================================
# 💌 SHAYARI HANDLER
# ============================================
@client.on(events.NewMessage(pattern=r'^\.shayari(?:\s+(\w+))?$'))
async def shayari_cmd(event):
    category = event.pattern_match.group(1)
    if not category:
        category = random.choice(list(SHAYARI.keys()))
    
    if category not in SHAYARI:
        category = "default"
    
    shayari = random.choice(SHAYARI[category])
    header = {
        "love": "💕 **Love Shayari** 💕",
        "sad": "💔 **Sad Shayari** 💔",
        "miss": "💭 **Miss You Shayari** 💭",
        "wife": "💍 **Wife Special Shayari** 💍",
        "dosti": "🤝 **Dosti Shayari** 🤝",
        "zindagi": "📖 **Zindagi Shayari** 📖",
        "bewafa": "🥀 **Bewafa Shayari** 🥀",
        "default": "✨ **Shayari** ✨",
    }.get(category, "✨ **Shayari** ✨")
    
    await event.reply(f"{header}\n\n{shayari}")


# ============================================
# 🎲 FUN COMMANDS
# ============================================
@client.on(events.NewMessage(pattern=r'^\.flip$'))
async def flip_cmd(event):
    result = random.choice(["🪙 **Heads!**", "🪙 **Tails!**"])
    await event.reply(result)


@client.on(events.NewMessage(pattern=r'^\.dice$'))
async def dice_cmd(event):
    num = random.randint(1, 6)
    await event.reply(f"🎲 **You rolled: {num}**")


@client.on(events.NewMessage(pattern=r'^\.hearts(?:\s+(.+))?$'))
async def hearts_cmd(event):
    text = event.pattern_match.group(1) or "Love You"
    hearts = " ".join(["❤️"] * 10)
    await event.reply(f"{hearts}\n**{text}**\n{hearts}")


# ============================================
# 👤 PROFILE COMMANDS
# ============================================
@client.on(events.NewMessage(pattern=r'^\.profile$'))
async def profile_cmd(event):
    sender = await event.get_sender()
    try:
        full = await client(GetFullUserRequest(sender.id))
        bio = full.about or "No bio"
    except:
        bio = "N/A"
    
    text = f"""
👤 **Your Profile**
📛 Name: {sender.first_name or ''} {sender.last_name or ''}
🆔 ID: `{sender.id}`
📝 Username: @{sender.username if sender.username else 'None'}
💬 Bio: {bio}
    """
    await event.reply(text)


# ============================================
# 🚀 START
# ============================================
async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Userbot Started!")
    print(f"👤 Logged in as: {me.first_name} (@{me.username})")
    print(f"🆔 ID: {me.id}")
    print(f"💕 Love Mode: ON")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
