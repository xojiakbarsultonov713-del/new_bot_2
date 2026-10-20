import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

# 1. @BotFather bergan rasmiy token ulandi
BOT_TOKEN = "8908370640:AAFxc3a-aCUuGJ9J3s8opE3kG2yDMRbyrI4"

# ⚠️ O'ZINGIZNING TELEGRAM ID RAQAMINGIZNI SHU YERGA YOZING!
# (Telegramda @userinfobot orqali ID raqamingizni bilib olishingiz mumkin)
ADMIN_ID = 5039354291  # <--- Raqamni almashtiring

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Boshlang'ich ballar (O'zgaruvchi xotirada saqlanadi)
scores = {
    1: 95,  # IT va Sun'iy Intellekt
    2: 90,  # Fanlar to'garagi
    3: 88,  # Ma'naviyat va ma'rifat
    4: 82,  # Ijodiy ishlar va madaniyat
    5: 75,  # Sport va salomatlik
    6: 70,  # Maktab Sardorlari
    7: 63   # Ijtimoiy loyihalar
}

# /start buyrug'i uchun javob
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Salom, {message.from_user.full_name}!\n"
        f"🏫 **18-maktab** IT va Sun'iy intellekt koordinatorining rasmiy botiga xush kelibsiz!\n\n"
        f"Kerakli bo'limni tanlash uchun pastdagi menyudan foydalaning yoki buyruqlarni yuboring."
    )

# /school buyrug'i uchun javob
@dp.message(Command("school"))
async def cmd_school(message: types.Message):
    await message.answer(
        "🏫 **18-maktab haqida ma'lumot:**\n\n"
        "Maktabimiz zamonaviy bilim va texnologiyalar o'chog'idir. "
        "Bu yerda o'quvchilar chuqurlashtirilgan fanlar va zamonaviy to'garaklarda tahsil olishadi."
    )

# /coordinators buyrug'i (Kengash tuzilmasidagi 7 ta rasmiy koordinator)
@dp.message(Command("coordinators"))
async def cmd_coordinators(message: types.Message):
    coordinators_text = (
        "👥 **18-maktab Kengash tuzilmasi va Koordinatorlar:**\n\n"
        "👑 **Kelajak lideri:** [Ism va familiya yoziladigan joy]\n"
        "🧠 **Maktab maslahatchisi:** [Ism va familiya yoziladigan joy]\n\n"
        "📌 **Yo'nalish koordinatorlari:**\n\n"
        "1. 📘 **Ta'lim koordinatorining boti**\n"
        "   - *Vazifasi:* Ta'lim jarayonlari va o'quvchilar takomilini muofiqlashtiradi.\n"
        "   - *Mas'ul:* [Ism va familiya]\n\n"
        "2. 💻 **IT va sun'iy intellekt koordinatorining boti (Siz)**\n"
        "   - *Vazifasi:* Raqamli yechimlar va innovatsiyalarni rivojlantiradi.\n"
        "   - *Mas'ul:* [Ism va familiya]\n\n"
        "3. 📷 **Media koordinatorining boti**\n"
        "   - *Vazifasi:* Maktab hayotini ommalashtiradi, axborot siyosatini yuritadi.\n"
        "   - *Mas'ul:* [Ism va familiya]\n\n"
        "4. 🎭 **Madaniyat koordinatorining boti**\n"
        "   - *Vazifasi:* Ijodiy loyihalar va madaniy tadbirlarni tashkil etadi.\n"
        "   - *Mas'ul:* [Ism va familiya]\n\n"
        "5. 🏃 **Sport koordinatorining boti**\n"
        "   - *Vazifasi:* Sog'lom turmush tarzini targ'ib etadi va sport tadbirlarini o'tkazadi.\n"
        "   - *Mas'ul:* [Ism va familiya]\n\n"
        "6. 🌿 **Ekologiya koordinatorining boti**\n"
        "   - *Vazifasi:* Tabiatni asrash va ekologik loyihalarni muofiqlashtiradi.\n"
        "   - *Mas'ul:* [Ism va familiya]\n\n"
        "7. 🤝 **Ijtimoiy tashabbus koordinatorining boti**\n"
        "   - *Vazifasi:* Volontyorlik va ijtimoiy loyihalarni tashkil etadi.\n"
        "   - *Mas'ul:* [Ism va familiya]"
    )
    await message.answer(coordinators_text)

# /diagrams buyrug'i - endi ballar dinamik chiqadi!
@dp.message(Command("diagrams"))
async def cmd_diagrams(message: types.Message):
    # Status aniqlash funksiyasi (80% dan baland bo'lsa O'ta faol)
    def get_status(score):
        return "O'ta Faol 🔥" if score >= 80 else "Aktiv ⚡"

    text_caption = (
        "📊 **7 ta koordinatorning haftalik faollik ko'rsatkichlari:**\n\n"
        f"1. {get_status(scores[1])[:-1]} **IT va Sun'iy Intellekt** — {scores[1]}%\n"
        f"2. {get_status(scores[2])[:-1]} Fanlar to'garagi — {scores[2]}%\n"
        f"3. {get_status(scores[3])[:-1]} Ma'naviyat va ma'rifat — {scores[3]}%\n"
        f"4. {get_status(scores[4])[:-1]} Ijodiy ishlar va madaniyat — {scores[4]}%\n"
        f"5. {get_status(scores[5])[:-1]} Sport va salomatlik — {scores[5]}%\n"
        f"6. {get_status(scores[6])[:-1]} Maktab Sardorlari — {scores[6]}%\n"
        f"7. {get_status(scores[7])[:-1]} Ijtimoiy loyihalar — {scores[7]}%\n\n"
        "*Ko'rsatkichlar koordinator tomonidan qo'lda yangilanadi!*"
    )
    try:
        photo = FSInputFile("koordinatorlar_faolligi.png")
        await message.answer_photo(photo=photo, caption=text_caption)
    except Exception:
        await message.answer(text_caption)

# 🔐 FAQAT ADMIN UCHUN: Ballarni yangilash buyrug'i
@dp.message(Command("set_score"))
async def cmd_set_score(message: types.Message):
    # Xavfsizlik tekshiruvi: Yuborgan odam haqiqatdan ham adminsizmi?
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Kechirasiz, bu buyruqdan faqat IT Koordinator (Admin) foydalana oladi!")
        return

    try:
        # Buyruq matnini bo'laklarga ajratamiz (Masalan: /set_score 1 98 -> ['1', '98'])
        args = message.text.split()[1:]
        if len(args) != 2:
            await message.answer("ℹ️ To'g'ri foydalanish: `/set_score [koordinator_raqami] [yangi_ball]`\nMisol uchun: `/set_score 1 98`")
            return

        num = int(args[0])
        new_score = int(args[1])

       import os
import matplotlib.pyplot as plt
import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

IMG_PATH = "koordinatorlar_faolligi.png"

# Tasodifiy IT va AI faktlar ro'yxati
it_facts = [
    "🤖 Birinchi sun'iy intellekt dasturi 1951-yilda shaxmat o'ynash uchun yozilgan.",
    "💻 Dunyodagi birinchi dasturchi ayol kishi bo'lgan. Uning ismi - Ada Lavleys.",
    "🐍 Python dasturlash tili ilon nomi bilan emas, mashhur 'Monty Python' komediya shousi sharafiga nomlangan.",
    "🌐 Dunyodagi birinchi veb-sayt 1991-yilda yaratilgan va u hali ham ishlaydi (info.cern.ch).",
    "🧠 ChatGPT modeli inson miyasidagi neyronlarga o'xshash milliardlab parametrlarda ishlaydi."
]

# 📊 Diagrammani avtomatik rasm qilib chizuvchi funksiya
def generate_chart():
    names = ["IT & AI", "Fanlar", "Ma'naviyat", "Madaniyat", "Sport", "Sardorlar", "Ijtimoiy"]
    # Barcha koordinatorlar ballarini ro'yxatga olamiz
    current_scores = [scores[1], scores[2], scores[3], scores[4], scores[5], scores[6], scores[7]]
    
    # 80 dan baland bo'lsa ko'k, past bo'lsa to'q sariq rang berish
    colors = ['#1f77b4' if s >= 80 else '#ff7f0e' for s in current_scores]
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, current_scores, color=colors, edgecolor='black', linewidth=1.2)
    
    plt.title("18-maktab: Koordinatorlar haftalik faolligi (%)", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Faollik darajasi", fontsize=12)
    plt.ylim(0, 110)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ustunlar ustiga foiz raqamlarini chiqarish
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval}%", ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(IMG_PATH, dpi=150)
    plt.close()

# 🔐 Yangilangan ball kiritish buyrug'i (Avvalgi /set_score ustiga yoziladi va rasm chizadi)
@dp.message(Command("set_score"))
async def cmd_set_score_updated(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Kechirasiz, bu buyruqdan faqat IT Koordinator (Admin) foydalana oladi!")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            await message.answer("ℹ️ To'g'ri foydalanish: `/set_score [koordinator_raqami] [yangi_ball]`\nMisol uchun: `/set_score 1 98`")
            return

        num = int(args[0])
        new_score = int(args[1])

        if num in scores and 0 <= new_score <= 100:
            scores[num] = new_score
            
            # 🔥 BALL YANGILANISHI BILAN RASMNI AVTOMATIK QAYTADAN CHIZAMIZ!
            generate_chart()
            
            await message.answer(f"✅ Muvaffaqiyatli yangilandi va yangi diagramma avtomatik chizildi!\n{num}-koordinatorning yangi bali: **{new_score}%**")
        else:
            await message.answer("❌ Xatolik! Koordinator raqami 1-7 gacha, ball esa 0-100 gacha bo'lishi shart.")
    except Exception:
        await message.answer("❌ Xatolik! Iltimos faqat raqamlardan foydalaning.")

# 📩 /suggest buyrug'i (Anonim takliflar ko'rsatmasi)
@dp.message(Command("suggest"))
async def cmd_suggest(message: types.Message):
    await message.answer(
        "💡 **Anonim taklif yuborish bo'limi!**\n\n"
        "Xatingizni quyidagi ko'rinishda yuboring:\n"
        "`/send_suggest [Sizning matningiz]`\n\n"
        "*Eslatma: Sizning shaxsingiz (ismingiz) koordinatorga ko'rinmaydi!*"
    )

# Anonim xatni adminga jo'natish
@dp.message(Command("send_suggest"))
async def cmd_send_suggest(message: types.Message):
    try:
        suggest_text = message.text.split(maxsplit=1)[1]
        await bot.send_message(chat_id=ADMIN_ID, text=f"📩 **Yangi anonim taklif tushdi:**\n\n\"{suggest_text}\"")
        await message.answer("✅ Rahmat! Sizning anonim taklifingiz muvaffaqiyatli yuborildi.")
    except IndexError:
        await message.answer("❌ Xatolik! Matn yozing. Misol: `/send_suggest Maktabda cyber musobaqa qilaylik.`")

# 💡 /fact buyrug'i (Tasodifiy faktlar)
@dp.message(Command("fact"))
async def cmd_fact(message: types.Message):
    await message.answer(f"💡 **Qiziqarli IT fakt:**\n\n{random.choice(it_facts)}")

# 🏆 /competitions buyrug'i (Musobaqalar)
@dp.message(Command("competitions"))
async def cmd_competitions(message: types.Message):
    competitions_text = (
        "🏆 **18-maktab: IT va AI Musobaqalari**\n\n"
        "🥇 **1. Kibersport turniri** (15-noyabr)\n"
        "💻 **2. Python tanlovi** (28-noyabr)\n\n"
        "🤖 *Musobaqalarda qatnashish uchun koordinatorga murojaat qiling!*"
    )
    await message.answer(competitions_text)

# 🏠 Bosh sahifa tugmalari klaviaturasi
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏫 Maktab haqida"), KeyboardButton(text="👥 Koordinatorlar")],
            [KeyboardButton(text="📊 Faollik Diagrammasi"), KeyboardButton(text="🤖 IT va AI bo'limi")],
            [KeyboardButton(text="💡 Qiziqarli Faktlar"), KeyboardButton(text="🏆 IT Musobaqalar")],
            [KeyboardButton(text="📩 Taklif yuborish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang..."
    )
    return keyboard

# 🏠 Tugmalar bosilganda ularga mos buyruqlarni chaqiruvchi tizim
@dp.message(lambda message: message.text in [
    "🏫 Maktab haqida", "👥 Koordinatorlar", "📊 Faollik Diagrammasi", 
    "🤖 IT va AI bo'limi", "💡 Qiziqarli Faktlar", "🏆 IT Musobaqalar", "📩 Taklif yuborish"
])
async def handle_keyboard_buttons(message: types.Message):
    if message.text == "🏫 Maktab haqida": await cmd_school(message)
    elif message.text == "👥 Koordinatorlar": await cmd_coordinators(message)
    elif message.text == "📊 Faollik Diagrammasi": await cmd_diagrams(message)
    elif message.text == "🤖 IT va AI bo'limi": await cmd_it_ai(message)
    elif message.text == "💡 Qiziqarli Faktlar": await cmd_fact(message)
    elif message.text == "🏆 IT Musobaqalar": await cmd_competitions(message)
    elif message.text == "📩 Taklif yuborish": await cmd_suggest(message)

# 🚀 Loyihani ishga tushiruvchi yakuniy g'ishtcha
async def main():
    if not os.path.exists(IMG_PATH):
        try: generate_chart()
        except Exception: pass
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
