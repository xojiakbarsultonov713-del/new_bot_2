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

        if num in scores and 0 <= new_score <= 100:
            scores[num] = new_score
            await message.answer(f"✅ Muvaffaqiyatli yangilandi!\n{num}-koordinatorning yangi bali: **{new_score}%**")
        else:
            await message.answer("❌ Xatolik! Koordinator raqami 1-7 gacha, ball esa 0-100 gacha bo'lishi shart.")
    except ValueError:
        await message.answer("❌ Xatolik! Iltimos faqat raqamlardan foydalaning.")

# /it_ai buyrug'i
@dp.message(Command("it_ai"))
async def cmd_it_ai(message: types.Message):
    await message.answer(
        "🤖 **IT va Sun'iy intellekt yo'nalishi:**\n\n"
        "Bu bo'limda siz dasturlash (Python, Scratch), robototexnika va AI texnologiyalari "
        "bo'yicha o'tiladigan darslar haqida ma'lumot olasiz."
    )

async def main():
    print("Bot xavfsizlik tizimi bilan ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
