import json, os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN="8878176103:AAEKkT1-Z2t7is1ZbGTvIlhrTBSpaPNCzn8"
OWNER_ID=6488037485
GROUP_FILE="groups.json"
WAITING_PHOTO = False
WAITING_VIDEO = False
SELL_VIDEO_ID="BAACAgUAAxkBAAPnalDB_HSeKrJsTS_Ymw47qEUOHKUAAtgdAAKSW4FWdedJ_-lG9D08BA"
AUDIT_VIDEO_ID="BAACAgUAAxkBAAPralDCa0yXxb5lYferYVvWnuwNJMsAAt0dAAKSW4FWsAF9ASSoxLc8BA"
FREEZE_VIDEO_ID="BAACAgUAAxkBAAPpalDCVY-zITe6MdYiwd1yUxKDQRgAAtwdAAKSW4FWEqvRTLMfAAGXPAQ"

SELL_MESSAGE= """🚀 Want Your Sell to Be Faster?

✅ Create multiple UPI IDs.
✅ Add multiple wallets and bank accounts.
✅ Switch your primary UPI ID and primary bank account regularly.
✅ If you're still not getting sell orders, try using a different bank account.

These steps may help improve your chances of getting sell orders faster.
"""
OTP_MESSAGE="""⚠️ Important Notice for All Users

Dear Users,

Agar aapka UPI Wallet offline ho gaya hai, toh OTP baar-baar request mat karein.

❌ 1 hour ke andar baar-baar OTP request karne par 24 hours tak naya OTP receive nahi ho sakta.

✅ Recommendation:
• 1 hour mein maximum 2 OTP requests karein.
• Har OTP request ke beech kam se kam 20 minutes ka gap rakhein.

🙏 Thank you for your cooperation
"""
AUDIT_MESSAGE="Payment screenshot aur UID bhejiye.\nPlease wait, team aapki madad karegi."
FREEZE_MESSAGE="""If you unlink your UPI account while withdrawing funds, the funds will be frozen, and you will bear the loss yourself.

The system flagged his behavior as fraudulent because you cut the UPI connection while the transaction was in progress; otherwise, why would you disable UPI during normal operations?
"""
DEFAULT_REPLY="""प्रिय सदस्य,

कृपया अपनी समस्या का स्क्रीनशॉट और अपना ID साथ में भेजें ताकि हम आपकी जल्द सहायता कर सकें।

Customer Support:
@Goodfortune1
@nagurry
@fafa1209
"""
TASK_REWARD = """🎁 Task Reward Request Received

Please wait.

Agar aapne required task successfully complete kiya hai, to Customer Support verification ke baad reward process kar diya jayega.

Normally reward next day process hota hai.
"""

TEAM_REWARD = """🎁 Team Volume Reward Request Received

Please wait.

Aapka team volume verify hone ke baad Customer Support reward process karegi.
"""

NEWUSER_REWARD = """🎁 New User Reward Request Received

Please wait.

Agar aapka invited user valid hai, to verification ke baad reward add kar diya jayega.
"""

DONE_MESSAGE = """🎉 Congratulations!

Your reward has been successfully verified and credited.

Thank you for your support.
Keep growing and keep earning! 💙
"""
support_keywords=["help me","support me","admin","please help me"]

def load_groups():
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE,"r") as f: return json.load(f)
    return []

def save_group(gid):
    g=load_groups()
    if gid not in g:
        g.append(gid)
        with open(GROUP_FILE,"w") as f: json.dump(g,f)

async def track_group(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_chat.type in ("group","supergroup"):
        save_group(update.effective_chat.id)


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        return True

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    return member.status in ["administrator", "creator"]


async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        await update.message.reply_text(update.message.video.file_id)


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    m = update.message.text.lower()

    import re

    uid = re.search(r"\b\d{6,12}\b", m)

    if uid:
        if "done" in m:
            if await is_admin(update, context):
                await update.message.reply_text(DONE_MESSAGE)
            return

        if "#1" in m:
            await update.message.reply_text(TASK_REWARD)
            return

        if "#2" in m:
            await update.message.reply_text(TEAM_REWARD)
            return

        if "#5" in m:
            await update.message.reply_text(NEWUSER_REWARD)
            return

    if m == "sell":
        ...
        await update.message.reply_text(SELL_MESSAGE)
        await update.message.reply_video(SELL_VIDEO_ID)
        return
    if any(x in m for x in ["sell fast","sell boost","sell problem"]):
        await update.message.reply_text(SELL_MESSAGE); return
    if m=="buy" or m=="audit" or "buy problem" in m:
        await update.message.reply_text(AUDIT_MESSAGE)
        await update.message.reply_video(AUDIT_VIDEO_ID); return
    if "freeze" in m or "frozen" in m:
        await update.message.reply_text(FREEZE_MESSAGE)
        await update.message.reply_video(FREEZE_VIDEO_ID); return
    otp=["otp","otp failed","otp faild","otp problem","sms"]
    if any(x in m for x in otp):
        await update.message.reply_text(OTP_MESSAGE); return
    if any(x in m for x in support_keywords):
        await update.message.reply_text(DEFAULT_REPLY)

async def announce(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!=OWNER_ID:
        await update.message.reply_text("Permission denied"); return
    msg=" ".join(context.args)
    if not msg:
        await update.message.reply_text("Usage: /announce your message"); return
    c=0
    for gid in load_groups():
        try:
            await context.bot.send_message(gid,f"📢 Announcement\n\n{msg}")
            c+=1
        except: pass
    await update.message.reply_text(f"Sent to {c} groups")
async def announcephoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WAITING_PHOTO
    if update.effective_user.id != OWNER_ID:
        return
    WAITING_PHOTO = True
    await update.message.reply_text("📸 Please send the photo with a caption.")

async def announcevideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WAITING_VIDEO
    if update.effective_user.id != OWNER_ID:
        return
    WAITING_VIDEO = True
    await update.message.reply_text("🎥 Please send the video with a caption.")
    async def announcement_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WAITING_PHOTO, WAITING_VIDEO

    if update.effective_user.id != OWNER_ID:
        return

    if WAITING_PHOTO and update.message.photo:
        caption = update.message.caption or ""
        photo = update.message.photo[-1].file_id

        count = 0
        for gid in load_groups():
            try:
                await context.bot.send_photo(
                    chat_id=gid,
                    photo=photo,
                    caption=caption
                )
                count += 1
            except:
                pass

        WAITING_PHOTO = False
        await update.message.reply_text(f"✅ Photo sent to {count} groups.")
        return

    if WAITING_VIDEO and update.message.video:
        caption = update.message.caption or ""
        video = update.message.video.file_id

        count = 0
        for gid in load_groups():
            try:
                await context.bot.send_video(
                    chat_id=gid,
                    video=video,
                    caption=caption
                )
                count += 1
            except:
                pass

        WAITING_VIDEO = False
        await update.message.reply_text(f"✅ Video sent to {count} groups.")
app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("announce", announce))
app.add_handler(CommandHandler("announcephoto", announcephoto))
app.add_handler(CommandHandler("announcevideo", announcevideo))

app.add_handler(MessageHandler(filters.ALL, track_group), group=0)

app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, announcement_media), group=1)

app.add_handler(MessageHandler(filters.VIDEO, get_video_id), group=1)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply), group=1)
app.run_polling()
