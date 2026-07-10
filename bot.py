import json, os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN="8878176103:AAEKkT1-Z2t7is1ZbGTvIlhrTBSpaPNCzn8"
OWNER_ID=6488037485
GROUP_FILE="groups.json"

SELL_VIDEO_ID="BAACAgUAAxkBAAFOtoVqUJ_17TK2zPPYSu9164_8OQ-sUgAC2B0AApJbgVY7SkcS_qv4FTwE"
AUDIT_VIDEO_ID="BAACAgUAAxkBAAFOtqpqUKIdn2Y_GRC1ZdYcxmB7mECqWwAC3R0AApJbgVZKjoE_8TR5WzwE"
FREEZE_VIDEO_ID="BAACAgUAAxkBAAFOtqFqUKEyVnqSQiTHuvr-9dBLg-s_jAAC3B0AApJbgVbNztD3lm0ZCDwE"

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
DEFAULT_REPLY="Customer Support:\n@Goodfortune1\n@nagurry\n@fafa1209"

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


async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        await update.message.reply_text(update.message.video.file_id)


async def auto_reply(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    m = update.message.text.lower()

    if m=="sell":
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

app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("announce", announce))
app.add_handler(MessageHandler(filters.ALL, track_group), group=0)

app.add_handler(MessageHandler(filters.VIDEO, get_video_id), group=1)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply), group=1)
app.run_polling()
