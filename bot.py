import json, os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN="8878176103:AAEKkT1-Z2t7is1ZbGTvIlhrTBSpaPNCzn8"
OWNER_ID=6488037485
GROUP_FILE="groups.json"
GROUP_USERS_FILE = "group_users.json"
REWARD_FILE = "reward_history.json"
SUPPORT_FILE = "support.json"
TICKET_FILE = "ticket.json"
SUPPORT_GROUP_ID = -1003992031604
ALREADY_PENDING = """⏳ Already Pending

Your reward request has already been submitted.

Please wait for verification.
"""
WAITING_PHOTO = False
WAITING_VIDEO = False
ANNOUNCE_CHAT_ID = None
USER_UID = {}
WAITING_SUPPORT = {}
USER_PROBLEM = {}
SUPPORT_STAGE = {}
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
    GROUP_USERS_FILE = "group_users.json"

def load_group_users():
    if os.path.exists(GROUP_USERS_FILE):
        with open(GROUP_USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_group_users(data):
    with open(GROUP_USERS_FILE, "w") as f:
        json.dump(data, f)
def load_rewards():
    if os.path.exists(REWARD_FILE):
        with open(REWARD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_rewards(data):
    with open(REWARD_FILE, "w") as f:
        json.dump(data, f)


def load_support():
    if os.path.exists(SUPPORT_FILE):
        with open(SUPPORT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_support(data):
    with open(SUPPORT_FILE, "w") as f:
        json.dump(data, f)


def create_ticket():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"last_ticket": 1000}

    data["last_ticket"] += 1

    with open(TICKET_FILE, "w") as f:
        json.dump(data, f)

    return data["last_ticket"]


def save_group(gid):
    g = load_groups()
    if gid not in g:
        g.append(gid)
        with open(GROUP_FILE, "w") as f:
            json.dump(g, f)
async def track_group(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat and update.effective_chat.type in ("group", "supergroup"):

        save_group(update.effective_chat.id)

        users = load_group_users()

        user_id = str(update.effective_user.id)

        users[user_id] = {
            "name": update.effective_user.first_name or "User",
            "username": update.effective_user.username or ""
        }

        save_group_users(users)

        print("GROUP USER SAVED:", user_id)


async def is_admin(update, context):
    return update.effective_user.id == OWNER_ID
    return True

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    return member.status in ["administrator", "creator"]


async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        await update.message.reply_text(update.message.video.file_id)


async def support_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    support_data = load_support()

    if str(user_id) in support_data:
        if support_data[str(user_id)].get("status") == "OPEN":
            await update.message.reply_text(
                "💙 Bhai, humne aapki problem pehle hi receive kar li hai.\n\n"
                "Bas thoda patience rakho, aapka problem solve zaroor hoga."
            )
            return

    if SUPPORT_STAGE.get(user_id) != "screenshot":
        return

    ticket = create_ticket()

    support_data[str(user_id)] = {
        "ticket": ticket,
        "status": "OPEN"
    }

    save_support(support_data)

    msg = await context.bot.send_photo(
        chat_id=SUPPORT_GROUP_ID,
        photo=update.message.photo[-1].file_id,
        caption=(
            f"🎫 Ticket Number: #{ticket}\n\n"
            f"👤 User Name: {update.effective_user.full_name}\n"
            f"📱 Username: @{update.effective_user.username or 'None'}\n"
            f"🆔 Telegram User ID: {user_id}\n"
            f"🆔 UID: {USER_UID.get(user_id, 'N/A')}\n\n"
            f"📝 Problem:\n"
            f"{USER_PROBLEM.get(user_id, 'Not provided')}"
        )
    )

    support_data[str(user_id)]["group_message_id"] = msg.message_id
    save_support(support_data)

    SUPPORT_STAGE.pop(user_id, None)

    await update.message.reply_text(
        f"✅ Screenshot received successfully.\n\n"
        f"🎫 Ticket Number: #{ticket}\n\n"
        "Our Support Team will contact you soon.\n\n"
        "Thank you for your patience."
    )


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    if update.message.text.startswith("/tag"):
        if not await is_admin(update, context):
            return

        users = load_group_users()

        if not users:
            await update.message.reply_text("❌ No users saved")
            return

        text = "📢 Attention Everyone\n\n"

        for uid, data in users.items():
            name = data.get("name", "User")
            text += f'<a href="tg://user?id={uid}">{name}</a> '

        await update.message.reply_text(
            text,
            parse_mode="HTML"
        )
        return
    if update.message.text.lower().startswith("tag "):

        if not await is_admin(update, context):
            return

        users = load_group_users()

        text = "📢 Attention Everyone\n\n"

        for uid, data in users.items():
            name = data.get("name", "User")
            text += f'<a href="tg://user?id={uid}">{name}</a> '

        text += "\n\n" + update.message.text[4:]

        await update.message.reply_text(
            text,
            parse_mode="HTML"
        )
        return
    m = update.message.text.lower()

    import re

    uid = re.search(r"\b\d{6,12}\b", m)

    # ================= REWARD SYSTEM =================
    if uid and ("#1" in m or "#2" in m or "#5" in m or "done" in m):

        rewards = load_rewards()
        uid_text = uid.group()

        if "done" in m:
            if await is_admin(update, context):
                await update.message.reply_text(DONE_MESSAGE)
            return

        if "#1" in m:
            key = f"{uid_text}_task"

            if key in rewards:
                await update.message.reply_text(ALREADY_PENDING)
                return

            rewards[key] = True
            save_rewards(rewards)

            await update.message.reply_text(TASK_REWARD)
            return

        if "#2" in m:
            key = f"{uid_text}_team"

            if key in rewards:
                await update.message.reply_text(ALREADY_PENDING)
                return

            rewards[key] = True
            save_rewards(rewards)

            await update.message.reply_text(TEAM_REWARD)
            return

        if "#5" in m:
            key = f"{uid_text}_newuser"

            if key in rewards:
                await update.message.reply_text(ALREADY_PENDING)
                return

            rewards[key] = True
            save_rewards(rewards)

            await update.message.reply_text(NEWUSER_REWARD)
            return


        # ================= SUPPORT SYSTEM =================

    if uid:
        USER_UID[update.effective_user.id] = uid.group()
        SUPPORT_STAGE[update.effective_user.id] = "problem"

        await update.message.reply_text(
            "✅ UID received successfully.\n\n"
            "📝 Please describe your problem."
        )
        return

    if SUPPORT_STAGE.get(update.effective_user.id) == "problem":
        USER_PROBLEM[update.effective_user.id] = update.message.text
        SUPPORT_STAGE[update.effective_user.id] = "screenshot"

        await update.message.reply_text(
            "📸 Please send a screenshot of your problem.\n\n"
            "Your support ticket will be generated after receiving the screenshot."
        )
        return

    if m == "sell":
        await update.message.reply_text(SELL_MESSAGE)
        await update.message.reply_video(SELL_VIDEO_ID)
        return

    if any(x in m for x in ["sell fast", "sell boost", "sell problem"]):
        await update.message.reply_text(SELL_MESSAGE)
        return

    if m == "buy" or m == "audit" or "buy problem" in m:
        await update.message.reply_text(AUDIT_MESSAGE)
        await update.message.reply_video(AUDIT_VIDEO_ID)
        return

    if "freeze" in m or "frozen" in m:
        await update.message.reply_text(FREEZE_MESSAGE)
        await update.message.reply_video(FREEZE_VIDEO_ID)
        return

    otp = ["otp", "otp failed", "otp faild", "otp problem", "sms"]
    if any(x in m for x in otp):
        await update.message.reply_text(OTP_MESSAGE)
        return

    if any(x in m for x in support_keywords):
        await update.message.reply_text(DEFAULT_REPLY)
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != SUPPORT_GROUP_ID:
        return

    if not update.message.reply_to_message:
        return

    caption = update.message.reply_to_message.caption or ""

    import re
    m = re.search(r"Telegram User ID:\s*(\d+)", caption)

    if not m:
        return

    user_id = int(m.group(1))

    if update.message.text.lower() == "close":
        support = load_support()
        support.pop(str(user_id), None)
        save_support(support)

        await context.bot.send_message(
            user_id,
            "✅ Your issue has been closed.\n\nThank you."
        )

        await update.message.reply_text("✅ Ticket Closed")
        return

    await context.bot.send_message(
        user_id,
        f"📩 Support Reply\n\n{update.message.text}"
    )

    await update.message.reply_text("✅ Reply Sent")
async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Permission denied")
        return

    msg = " ".join(context.args)

    if not msg:
        await update.message.reply_text("Usage: /announce your message")
        return

    c = 0
    for gid in load_groups():
        try:
            await context.bot.send_message(gid, f"📢 Announcement\n\n{msg}")
            c += 1
        except:
            pass

    await update.message.reply_text(f"Sent to {c} groups")


async def announcephoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WAITING_PHOTO, ANNOUNCE_CHAT_ID

    if update.effective_user.id != OWNER_ID:
        return

    WAITING_PHOTO = True
    ANNOUNCE_CHAT_ID = update.effective_chat.id

    await update.message.reply_text(
        "📸 Please send the photo with a caption."
    )

async def announcevideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WAITING_VIDEO, ANNOUNCE_CHAT_ID

    if update.effective_user.id != OWNER_ID:
        return

    WAITING_VIDEO = True
    ANNOUNCE_CHAT_ID = update.effective_chat.id

    await update.message.reply_text(
        "🎥 Please send the video with a caption."
    )


async def announcement_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global WAITING_PHOTO, WAITING_VIDEO, ANNOUNCE_CHAT_ID

    if update.effective_user.id != OWNER_ID:
        return

    if update.effective_chat.id != ANNOUNCE_CHAT_ID:
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
        return
async def reply_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Reply command received")
    if not await is_admin(update, context):
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply TicketNumber Message")
        return

    ticket_number = int(context.args[0])
    reply_text = " ".join(context.args[1:])

    support_data = load_support()

    for uid, data in support_data.items():
        if data.get("ticket") == ticket_number:
            await context.bot.send_message(
                int(uid),
                f"📩 Support Reply\n\n{reply_text}"
            )

            await update.message.reply_text(
                f"✅ Reply sent to Ticket #{ticket_number}"
            )
            return

    await update.message.reply_text("❌ Ticket not found.")
async def close_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /close TicketNumber")
        return

    ticket_number = int(context.args[0])

    support_data = load_support()

    for uid, data in support_data.items():
        if data.get("ticket") == ticket_number:
            support_data[uid]["status"] = "CLOSED"
            save_support(support_data)

            await context.bot.send_message(
                int(uid),
                "✅ Ticket Closed\n\n"
                "Your issue has been solved.\n\n"
                "Thank you for contacting Support."
            )

            await update.message.reply_text(
                f"✅ Ticket #{ticket_number} closed successfully."
            )
            return

    await update.message.reply_text("❌ Ticket not found.")
async def groupid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_chat.id))
async def tag_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("TAG COMMAND RECEIVED")
    if not await is_admin(update, context):
        return

    users = load_group_users()

    if not users:
        await update.message.reply_text("No saved users")
        return

    text = "📢 Attention Everyone\n\n"

    for uid, data in users.items():
        name = data.get("name", "User")
        text += f'<a href="tg://user?id={uid}">{name}</a> '

    if context.args:
        text += "\n\n" + " ".join(context.args)

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("announce", announce))
app.add_handler(CommandHandler("announcephoto", announcephoto))
app.add_handler(CommandHandler("announcevideo", announcevideo))

app.add_handler(MessageHandler(filters.ALL, track_group), group=0)

app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, announcement_media), group=1)
app.add_handler(
    MessageHandler(
        filters.PHOTO,
        support_screenshot
    ),
    group=2
)
app.add_handler(MessageHandler(filters.VIDEO, get_video_id), group=1)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply), group=1)
app.add_handler(CommandHandler("groupid", groupid))
app.add_handler(CommandHandler("reply", reply_ticket))
app.add_handler(CommandHandler("close", close_ticket))
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.REPLY,
        admin_reply
    ),
    group=3
)
app.add_handler(CommandHandler("tag", tag_users))
app.run_polling()

                          
