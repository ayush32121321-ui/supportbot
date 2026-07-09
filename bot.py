import json
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    ContextTypes, filters
)

TOKEN = "8878176103:AAEKkT1-Z2t7is1ZbGTvIlhrTBSpaPNCzn8"
OWNER_ID = 6488037485
GROUP_FILE = "groups.json"

SELL_MESSAGE = """🚀 Want Your Sell to Be Faster?

✅ Create multiple UPI IDs.
✅ Add multiple wallets and bank accounts.
✅ Switch your primary UPI ID and primary bank account regularly.
✅ If you're still not getting sell orders, try using a different bank account.

These steps may help improve your chances of getting sell orders faster.
"""

OTP_MESSAGE ="""⚠️ Important Notice for All Users

Dear Users,

Agar aapka UPI Wallet offline ho gaya hai, toh OTP baar-baar request mat karein.

❌ 1 hour ke andar baar-baar OTP request karne par 24 hours tak naya OTP receive nahi ho sakta.

✅ Recommendation:
• 1 hour mein maximum 2 OTP requests karein.
• Har OTP request ke beech kam se kam 20 minutes ka gap rakhein.

🙏 Thank you for your cooperation
"""

AUDIT_MESSAGE = """Payment screenshot aur UID bhejiye.
Please wait, team aapki madad karegi.
"""

FREEZE_MESSAGE = """If you unlink your UPI account while withdrawing funds, the funds may be frozen.
"""

DEFAULT_REPLY = """प्रिय सदस्य,

कृपया अपनी समस्या का स्क्रीनशॉट और अपना ID साथ में भेजें।

Customer Support:
@Goodfortune1
@nagurry
@fafa1209
"""

knowledge_base={
"sell":SELL_MESSAGE,"sell fast":SELL_MESSAGE,"sell boost":SELL_MESSAGE,"sell problem":SELL_MESSAGE,
"otp":OTP_MESSAGE,"otp failed":OTP_MESSAGE,"otp faild":OTP_MESSAGE,"otp problem":OTP_MESSAGE,"sms":OTP_MESSAGE,
"audit":AUDIT_MESSAGE,"buy":AUDIT_MESSAGE,"buy problem":AUDIT_MESSAGE,
"freeze":FREEZE_MESSAGE,"frozen":FREEZE_MESSAGE}
support_keywords=["help me","support me","admin","please help me"]

def load_groups():
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE,"r") as f: return json.load(f)
    return []

def save_group(gid):
    groups=load_groups()
    if gid not in groups:
        groups.append(gid)
        with open(GROUP_FILE,"w") as f: json.dump(groups,f)

async def track_group(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_chat.type in ["group","supergroup"]:
        save_group(update.effective_chat.id)

async def auto_reply(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    m=update.message.text.lower()
    for k,v in knowledge_base.items():
        if k in m:
            await update.message.reply_text(v); return
    for k in support_keywords:
        if k in m:
            await update.message.reply_text(DEFAULT_REPLY); return

async def announce(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!=OWNER_ID:
        await update.message.reply_text("❌ Permission denied"); return
    msg=" ".join(context.args)
    if not msg:
        await update.message.reply_text("Usage:\n/announce your message"); return
    sent=0
    for gid in load_groups():
        try:
            await context.bot.send_message(gid,f"📢 Announcement\n\n{msg}")
            sent+=1
        except: pass
    await update.message.reply_text(f"✅ Announcement sent to {sent} groups")

app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("announce",announce))
app.add_handler(MessageHandler(filters.ALL,track_group),group=0)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,auto_reply),group=1)
print("Support Bot Running...")
app.run_polling()
