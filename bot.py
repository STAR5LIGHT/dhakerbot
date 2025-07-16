from keep_alive import keep_alive
import asyncio
import json
import os
import random
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, ChatMemberHandler, filters as custom_filters

TOKEN = "8149833194:AAGaUWhgoF2bUVVzE4-RT6IeUn2zJALiImg"
GROUPS_FILE = "groups.json"

AZKAR_LIST = [
    "سبحان الله وبحمده، سبحان الله العظيم.",
    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.",
    "اللهم صلِّ وسلم على نبينا محمد.",
    "أستغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه.",
    "اللهم اجعلنا من الذاكرين الشاكرين.",
    "اللهم إني أعوذ بك من الهم والحزن والعجز والكسل.",
    "اللهم ثبت قلبي على دينك.",
    "اللهم أعني على ذكرك وشكرك وحسن عبادتك.",
    "اللهم ارحم موتانا وموتى المسلمين.",
    "اللهم ارزقنا حسن الخاتمة.",
    "اللهم اجعل القرآن ربيع قلوبنا.",
    "اللهم طهر قلوبنا من النفاق وأعمالنا من الرياء.",
    "اللهم اجعلنا من التوابين واجعلنا من المتطهرين.",
    "اللهم إنك عفوٌ تحب العفو فاعفُ عنا.",
    "اللهم بارك لنا في أيامنا وذكّرنا بك في كل حين.",
    "اللهم اجعلنا من الذين يستمعون القول فيتبعون أحسنه.",
    "اللهم اجعل آخر كلامنا لا إله إلا الله.",
    "اللهم زدنا ولا تنقصنا، وأكرمنا ولا تهنا.",
    "اللهم اجعلنا من أهل الجنة، وارزقنا الفردوس الأعلى بغير حساب.",
    "اللهم أحيي قلوبنا بالإيمان، واغفر لنا ولآبائنا وأمهاتنا.",
    "اللهم آمن روعاتنا، واستر عوراتنا، واغفر ذنوبنا.",
    "اللهم اجعلنا هداة مهتدين، غير ضالين ولا مضلين.",
    "اللهم قنا عذابك يوم تبعث عبادك.",
    "اللهم إنك قلت وقولك الحق: (فاذكروني أذكركم)، فاذكرنا برحمتك.",
    "اللهم وفقنا لما تحب وترضى، وخذ بنواصينا للبر والتقوى.",
    "اللهم اجعلنا ممن طال عمره وحسن عمله.",
]

def load_chats():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_chats(chats):
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(chats), f)

chat_ids = load_chats()

async def private_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟩 إضافة البوت إلى قروب", url="https://t.me/AjrRemindBot?startgroup=true")],
            [InlineKeyboardButton("📢 إضافة البوت إلى قناة", url="https://t.me/AjrRemindBot?startchannel=true")],
            [InlineKeyboardButton("📎 قناة ذِكر", url="https://t.me/Dhikkkr")]
        ])
        await update.message.reply_text(
            """مرحباً بك.<br><br>
قال النبي ﷺ: <b>من دلّ على خير فله مثل أجر فاعله</b><br><br>
هذا البوت يقوم بإرسال الأذكار تلقائيًا كل 15 دقيقة في القروبات أو القنوات.<br>
اضغط على أحد الأزرار لإضافة البوت أو زيارة <b>قناة ذِكر</b> 📎""",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

async def handle_new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.my_chat_member.chat
    status = update.my_chat_member.new_chat_member.status
    if status in ["member", "administrator"]:
        if chat.id not in chat_ids:
            chat_ids.add(chat.id)
            save_chats(chat_ids)
            print(f"✅ تمت إضافة {chat.title or chat.id} ({chat.type}) إلى القائمة.")

async def send_athkar_every_15_minutes(bot: Bot):
    while True:
        zekr = random.choice(AZKAR_LIST)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📎 قناة ذِكر", url="https://t.me/Dhikkkr")]
        ])
        for chat_id in list(chat_ids):
            try:
                await bot.send_message(chat_id=chat_id, text=zekr, parse_mode="HTML", reply_markup=keyboard)
            except Exception as e:
                print(f"⚠️ خطأ في الإرسال إلى {chat_id}: {e}")
        await asyncio.sleep(15 * 60)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(custom_filters.ChatType.PRIVATE & custom_filters.TEXT, private_welcome))
    app.add_handler(ChatMemberHandler(handle_new_chat, chat_member_types=["my_chat_member"]))
    asyncio.create_task(send_athkar_every_15_minutes(app.bot))
    print("✅ البوت يعمل ويرسل الأذكار كل 15 دقيقة.")
    await app.run_polling()

if __name__ == "__main__":
    keep_alive()
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
