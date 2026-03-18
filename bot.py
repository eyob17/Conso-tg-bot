import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import AsyncGroq

# ==========================================
# CONFIGURATION (Loaded from Environment Variables)
# ==========================================
# We use os.getenv so your keys aren't visible in the code
BOT_TOKEN = "" 
ADMIN_GROUP_ID = -1003461910499   
GROQ_API_KEY = ""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

ai_client = AsyncGroq(api_key=GROQ_API_KEY)

# ... (The rest of your code remains exactly the same)
# ==========================================
# MULTILINGUAL UI STRINGS
# ==========================================
 
STRINGS = {
    "en": {
        "welcome": (
            "👋 Welcome to the <b>Conso.tg</b> Official Support Bot!\n\n"
            "I am an AI assistant here to help you navigate our Web3 console. "
            "Ask me anything or select an option below!"
        ),
        "language_prompt": "🌐 Please select your preferred language:",
        "language_set": "✅ Language set to <b>English</b>. How can I help you?",
        "ticket_prompt": (
            "🚨 <b>Open a Support Ticket:</b>\n"
            "Please type your issue below in a single message. "
            "My human team will get back to you shortly."
        ),
        "ticket_sent": "✅ Your ticket has been sent to the human support team. We will contact you soon!",
        "ticket_error": "❌ Sorry, there was an error sending your ticket.",
        "ticket_cancelled": "✅ Ticket cancelled. How else can I help you?",
        "ai_error": (
            "My AI brain is experiencing a brief connection issue! 🤖\n\n"
            "Please try again in a moment, or click the "
            "[🚨 Report a Bug / Open Ticket] button to speak to a human."
        ),
        "buttons": {
            "cp":       "🪙 What are Conso Points (CP)?",
            "ca":       "📊 How do CA Signals work?",
            "mini":     "📱 Mini Apps Parallel Guide",
            "coinbox":  "🎁 Using CoinBox",
            "ticket":   "🚨 Report a Bug / Open Ticket",
            "language": "🌐 Change Language",
            "cancel":   "🔙 Cancel",
        },
        "fallback": {
            "cp": (
                "🪙 <b>Conso Points (CP)</b> are earned through browsing, interacting, "
                "and participating in the Conso app. They will serve as the basis for "
                "future Web3 perks and rewards!"
            ),
            "ca": (
                "📊 <b>CA Signals</b> automatically detects and aggregates contract "
                "addresses mentioned in your group chats, giving you a clear, "
                "reviewable list of on-chain token signals."
            ),
            "mini": (
                "📱 <b>Mini Apps Parallel</b> allows you to run several Telegram Mini "
                "Apps at the same time! You can seamlessly switch between games, "
                "tools, and tasks without losing your place."
            ),
            "coinbox": (
                "🎁 <b>CoinBox</b> lets you send and claim red-packet style token "
                "rewards directly in group chats to heat up discussions."
            ),
            "default": (
                "My AI brain is experiencing a brief connection issue! 🤖\n\n"
                "Please try again in a moment, or click "
                "[🚨 Report a Bug / Open Ticket] to speak to a human."
            ),
        },
    },
 
    "zh": {
        "welcome": (
            "👋 欢迎使用 <b>Conso.tg</b> 官方支持机器人！\n\n"
            "我是一名 AI 助手，帮助您使用我们的 Web3 控制台。"
            "您可以直接提问或从下方选择一个选项！"
        ),
        "language_prompt": "🌐 请选择您的首选语言：",
        "language_set": "✅ 语言已设置为<b>中文</b>。我能帮您什么？",
        "ticket_prompt": (
            "🚨 <b>提交支持工单：</b>\n"
            "请在一条消息中输入您的问题，我们的人工团队将尽快回复您。"
        ),
        "ticket_sent": "✅ 您的工单已发送给人工支持团队，我们将尽快与您联系！",
        "ticket_error": "❌ 抱歉，发送工单时出现错误。",
        "ticket_cancelled": "✅ 工单已取消。还有什么我可以帮您的吗？",
        "ai_error": (
            "我的 AI 大脑遇到了短暂的连接问题！🤖\n\n"
            "请稍后再试，或点击下方 [🚨 报告错误 / 提交工单] 联系人工客服。"
        ),
        "buttons": {
            "cp":       "🪙 什么是 Conso 积分 (CP)？",
            "ca":       "📊 CA 信号如何运作？",
            "mini":     "📱 多 Mini App 并行指南",
            "coinbox":  "🎁 使用 CoinBox",
            "ticket":   "🚨 报告错误 / 提交工单",
            "language": "🌐 更换语言",
            "cancel":   "🔙 取消",
        },
        "fallback": {
            "cp": (
                "🪙 <b>Conso 积分 (CP)</b> 通过浏览、互动和参与 Conso 应用获得，"
                "将作为未来 Web3 福利和奖励的基础！"
            ),
            "ca": (
                "📊 <b>CA 信号</b>自动检测并汇总群聊中提到的合约地址，"
                "为您提供清晰可查的链上代币信号列表。"
            ),
            "mini": (
                "📱 <b>多 Mini App 并行</b>允许您同时运行多个 Telegram Mini App！"
                "可在游戏、工具和任务之间无缝切换。"
            ),
            "coinbox": (
                "🎁 <b>CoinBox</b> 让您在群聊中直接发送和领取红包式代币奖励，"
                "活跃社区氛围。"
            ),
            "default": (
                "我的 AI 大脑遇到了短暂的连接问题！🤖\n\n"
                "请稍后再试，或点击 [🚨 报告错误 / 提交工单] 联系人工客服。"
            ),
        },
    },
 
    "am": {
        "welcome": (
            "👋 እንኳን ወደ <b>Conso.tg</b> ኦፊሴላዊ ድጋፍ ቦት በደህና መጡ!\n\n"
            "የ Web3 ኮንሶላችንን እንዲጠቀሙ የሚረዳ AI ረዳት ነኝ። "
            "ማንኛውንም ጥያቄ ይጠይቁ ወይም ከታች ያሉ አማራጮችን ይምረጡ!"
        ),
        "language_prompt": "🌐 የሚፈልጉትን ቋንቋ ይምረጡ:",
        "language_set": "✅ ቋንቋ <b>አማርኛ</b> ሆኗል። እንዴት ልረዳዎ?",
        "ticket_prompt": (
            "🚨 <b>የድጋፍ ቲኬት ክፈት:</b>\n"
            "ችግርዎን በአንድ መልእክት ይጻፉ። የሰው ቡድናችን በቅርቡ ይመልስልዎታል።"
        ),
        "ticket_sent": "✅ ቲኬትዎ ለሰው ድጋፍ ቡድን ተልኳል። በቅርቡ እናገኝዎታለን!",
        "ticket_error": "❌ ይቅርታ፣ ቲኬትዎን ሲልኩ ስህተት ተፈጠረ።",
        "ticket_cancelled": "✅ ቲኬት ተሰርዟል። ሌላ ማድረግ የምፈልጉት ነገር አለ?",
        "ai_error": (
            "የ AI አዕምሮዬ ጊዜያዊ የግንኙነት ችግር አጋጥሞታል! 🤖\n\n"
            "ትንሽ ቆይተው እንደገና ይሞክሩ ወይም "
            "[🚨 ስህተት ሪፖርት አድርጉ / ቲኬት ክፈቱ] የሚለውን ይጫኑ።"
        ),
        "buttons": {
            "cp":       "🪙 Conso Points (CP) ምንድን ነው?",
            "ca":       "📊 CA Signals እንዴት ይሰራሉ?",
            "mini":     "📱 Mini Apps ትይዩ መመሪያ",
            "coinbox":  "🎁 CoinBox መጠቀም",
            "ticket":   "🚨 ስህተት ሪፖርት አድርጉ / ቲኬት ክፈቱ",
            "language": "🌐 ቋንቋ ይቀይሩ",
            "cancel":   "🔙 ሰርዝ",
        },
        "fallback": {
            "cp": (
                "🪙 <b>Conso Points (CP)</b> በConso app ውስጥ ማሰስ፣ መስተጋብር እና "
                "መሳተፍ ያስገኛቸዋል። ለወደፊት Web3 ጥቅሞች እና ሽልማቶች መሠረት ናቸው!"
            ),
            "ca": (
                "📊 <b>CA Signals</b> የቡድን ውይይቶቾ ውስጥ ያሉ contract addresses "
                "በራስ-ሰር ይለያሉ እና ይሰበስቧቸዋል።"
            ),
            "mini": (
                "📱 <b>Mini Apps ትይዩ</b> በተመሳሳይ ጊዜ ብዙ Telegram Mini Apps "
                "ለማስኬድ ያስችልዎታል!"
            ),
            "coinbox": (
                "🎁 <b>CoinBox</b> በቡድን ውይይቶቾ ውስጥ የቶከን ሽልማቶችን "
                "ለማስተላለፍ እና ለመቀበል ያስችልዎታል።"
            ),
            "default": (
                "የ AI አዕምሮዬ ጊዜያዊ የግንኙነት ችግር አጋጥሞታል! 🤖\n\n"
                "ትንሽ ቆይተው ይሞክሩ ወይም "
                "[🚨 ስህተት ሪፖርት አድርጉ / ቲኬት ክፈቱ] ይጫኑ።"
            ),
        },
    },
}
 
 
# ==========================================
# LANGUAGE INSTRUCTIONS FOR GROQ
# ==========================================
 
LANGUAGE_INSTRUCTIONS = {
    "en": "Always respond in English.",
    "zh": "Always respond in Simplified Chinese (简体中文). All your replies must be in Chinese.",
    "am": "Always respond in Amharic (አማርኛ). All your replies must be in Amharic.",
}
 
 
# ==========================================
# SYSTEM PROMPT
# ==========================================
 
SYSTEM_PROMPT_BASE = (
    "You are the Official AI Support Assistant for Conso.tg, the premier "
    "Telegram-native Web3 console developed by xFinite Ltd. Your role is to "
    "provide expert-level technical support and strategic guidance for the "
    "Conso ecosystem.\n\n"
 
    "CORE OPERATIONAL RULES\n"
    "NO EXTERNAL LINKS: Do not provide URLs to any site except internal "
    "Telegram links (e.g., @ConsoChatOfficial).\n"
    "STRICT BRANDING: Only discuss Conso.tg. Do not mention or compare other "
    "Web3 tools or companies.\n"
    "PROFESSIONAL NARRATIVE: Your answers must be clean, technical, and professional.\n"
    "HUMAN HANDOFF: If a question is unrelated to Conso or involves a complex "
    "technical failure, direct the user to the Report a Bug / Open Ticket button "
    "or @ConsoChatOfficial for human support.\n\n"
 
    "KNOWLEDGE BASE\n\n"
 
    "1. CONSO POINTS (CP)\n"
    "CP is an all-scenario points system tracking browsing, interaction, and participation.\n"
    "Earning: Scroll to earn, Play to earn (up to 12 mini apps simultaneously), "
    "Chat to earn (every message sent/received earns CPs), Events.\n"
    "Topic Recommendations: 5 CPs for recommending a high-signal channel with PASS ID.\n"
    "Believers Gift (weekly USDT): requires 1,000+ CPs and 10+ referrals.\n"
    "Future Utility: Web3 rewards, voting rights, potential USDT conversion.\n\n"
 
    "2. ON-CHAIN INTELLIGENCE & CA SIGNALS\n"
    "CA Signals: Auto-detects and aggregates contract addresses from group chats.\n"
    "Price Cards: Live-updating token price cards via ticker or CA.\n\n"
 
    "3. WORKFLOW OPTIMIZATION\n"
    "Mini Apps Parallel: Run multiple Telegram Mini Apps simultaneously.\n"
    "Explore: Discovery of high-alpha channels.\n"
    "Web3: Curated institutional-grade news.\n"
    "Follow: Clean timeline of all subscribed channels.\n"
    "CoinBox: Red-packet style token rewards in Telegram groups.\n\n"
 
    "4. TECHNICAL SPECS\n"
    "Current Stable Version: 1.5.1 (Released February 2026).\n"
    "System Requirements: Android 7.0+ or iOS 16+.\n"
    "Troubleshooting: Clear Telegram cache and update the app.\n"
    "Data Rights: Encrypted transit; request data deletion via support.\n\n"
 
    "5. mBOX TYPES\n"
    "Newbie mBox: Join Official Channel, Community Group, Follow on X (up to 0.2 USDT)\n"
    "Starter mBox: Download App, Login to activate (up to 0.5 USDT)\n"
    "Builder mBox: Mine 180+ CPs, Share story on TG & X (up to 0.5 USDT)\n"
    "Believers Gift: Invite 10 friends, Hold 1000 CPs (weekly)\n"
    "Mystery Box: Open every 6 hours (up to 77 USDT)\n"
    "Hidden mBox: Share with TG friends (both get rewards)\n"
    "Boinkers Lucky Box: Limited collab (up to 0.5 USDT)\n\n"
 
    "6. COINBOX STREAK\n"
    "Day 1: White Box | Day 3: Silver Box (up to 0.2 USDT) | "
    "Day 5: Gold Box (up to 0.5 USDT) | Day 7: Diamond Box (up to 100 USDT)\n\n"
 
    "MANDATORY RESPONSE PROTOCOL\n"
    "If a user asks about anything not covered above, respond:\n"
    "I am the Conso.tg AI Assistant. My expertise is strictly limited to the "
    "Conso console and its Web3 features. For your specific request, please use "
    "the Report a Bug / Open Ticket button or visit @ConsoChatOfficial."
)
 
 
# ==========================================
# HELPER FUNCTIONS
# ==========================================
 
def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("language", "en")
 
 
def get_main_menu(lang: str = "en"):
    b = STRINGS[lang]["buttons"]
    keyboard = [
        [KeyboardButton(b["cp"])],
        [KeyboardButton(b["ca"])],
        [KeyboardButton(b["mini"])],
        [KeyboardButton(b["coinbox"])],
        [KeyboardButton(b["ticket"])],
        [KeyboardButton(b["language"])],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
 
 
def get_language_menu():
    keyboard = [
        [KeyboardButton("🇬🇧 English")],
        [KeyboardButton("🇨🇳 Chinese (中文)")],
        [KeyboardButton("🇪🇹 Amharic (አማርኛ)")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
 
 
def build_system_prompt(lang: str) -> str:
    instruction = LANGUAGE_INSTRUCTIONS.get(lang, LANGUAGE_INSTRUCTIONS["en"])
    return "LANGUAGE INSTRUCTION: " + instruction + "\n\n" + SYSTEM_PROMPT_BASE
 
 
# ==========================================
# HANDLERS
# ==========================================
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_ticket"] = False
    context.user_data["selecting_language"] = False
    lang = get_lang(context)
    await update.message.reply_text(
        STRINGS[lang]["welcome"],
        reply_markup=get_main_menu(lang),
        parse_mode="HTML",
    )
 
 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    lang = get_lang(context)
    s = STRINGS[lang]
    print("[" + lang.upper() + "] User: " + user_text)
 
    # Collect all button labels across every language for reliable detection
    all_language_buttons = {v["buttons"]["language"] for v in STRINGS.values()}
    all_ticket_buttons   = {v["buttons"]["ticket"]   for v in STRINGS.values()}
    all_cancel_buttons   = {v["buttons"]["cancel"]   for v in STRINGS.values()}
 
    # ── 1. Language selection mode ──────────────────────────────────────────
    if context.user_data.get("selecting_language"):
        mapping = {
            "🇬🇧 English":          "en",
            "🇨🇳 Chinese (中文)":    "zh",
            "🇪🇹 Amharic (አማርኛ)":  "am",
        }
        new_lang = mapping.get(user_text)
        if new_lang:
            context.user_data["language"] = new_lang
            context.user_data["selecting_language"] = False
            lang = new_lang
            s = STRINGS[lang]
            await update.message.reply_text(
                s["language_set"],
                reply_markup=get_main_menu(lang),
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text(
                s["language_prompt"],
                reply_markup=get_language_menu(),
            )
        return
 
    # ── 2. Language button pressed ──────────────────────────────────────────
    if user_text in all_language_buttons:
        context.user_data["selecting_language"] = True
        await update.message.reply_text(
            s["language_prompt"],
            reply_markup=get_language_menu(),
        )
        return
 
    # ── 3. Cancel ticket ────────────────────────────────────────────────────
    if context.user_data.get("awaiting_ticket") and user_text in all_cancel_buttons:
        context.user_data["awaiting_ticket"] = False
        await update.message.reply_text(
            s["ticket_cancelled"],
            reply_markup=get_main_menu(lang),
        )
        return
 
    # ── 4. Submit ticket ────────────────────────────────────────────────────
    if context.user_data.get("awaiting_ticket"):
        user = update.message.from_user
        ticket_text = (
            "<b>New Support Ticket</b>\n"
            "<b>From:</b> @" + (user.username or "unknown") +
            " (ID: " + str(user.id) + ")\n"
            "<b>Language:</b> " + lang.upper() + "\n"
            "<b>Message:</b> " + user_text
        )
        try:
            await context.bot.send_message(
                chat_id=ADMIN_GROUP_ID, text=ticket_text, parse_mode="HTML"
            )
            await update.message.reply_text(
                s["ticket_sent"], reply_markup=get_main_menu(lang)
            )
        except Exception as e:
            print("Ticket send error: " + str(e))
            await update.message.reply_text(
                s["ticket_error"], reply_markup=get_main_menu(lang)
            )
        context.user_data["awaiting_ticket"] = False
        return
 
    # ── 5. Ticket button pressed ────────────────────────────────────────────
    if user_text in all_ticket_buttons:
        context.user_data["awaiting_ticket"] = True
        cancel_kb = ReplyKeyboardMarkup(
            [[KeyboardButton(s["buttons"]["cancel"])]], resize_keyboard=True
        )
        await update.message.reply_text(
            s["ticket_prompt"], parse_mode="HTML", reply_markup=cancel_kb
        )
        return
 
    # ── 6. AI answer ────────────────────────────────────────────────────────
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    try:
        print("Asking Groq AI (lang=" + lang + ")...")
        completion = await ai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": build_system_prompt(lang)},
                {"role": "user",   "content": user_text},
            ],
            model="llama-3.3-70b-versatile",
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply, reply_markup=get_main_menu(lang))
        print("AI replied successfully.")
 
    except Exception as e:
        print("API error: " + str(e))
        fb = s["fallback"]
        text_lower = user_text.lower()
        if any(k in text_lower for k in ["point", "cp", "积分", "ነጥብ"]):
            fallback = fb["cp"]
        elif any(k in text_lower for k in ["signal", "ca"]):
            fallback = fb["ca"]
        elif any(k in text_lower for k in ["mini", "parallel", "ትይዩ"]):
            fallback = fb["mini"]
        elif any(k in text_lower for k in ["coinbox", "reward", "ሽልማት"]):
            fallback = fb["coinbox"]
        else:
            fallback = fb["default"]
 
        await update.message.reply_text(
            fallback, parse_mode="HTML", reply_markup=get_main_menu(lang)
        )
        print("Fallback reply sent.")
 
 
# ==========================================
# MAIN
# ==========================================
 
def main():
    print("Starting Conso.tg AI Support Bot (EN / ZH / AM)...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Bot is online.")
    app.run_polling()
 
 
if __name__ == "__main__":
    main()
 