import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Token truy cập bot
TOKEN = "7580021843:AAH2upfyhnkgmwp6EoH4C0hDCN--dOiXROI"

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------------------
# Handler cho lệnh /start
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # reset dữ liệu người dùng nếu có
    text = ("Tôi là chatbot của Solona SuperTeam và tôi ở đây để hỗ trợ bạn trong các tác vụ liên quan đến sự kiện.\n"
            "Bạn cần tôi giúp điều gì?")
    keyboard = [
        [InlineKeyboardButton("Event", callback_data="events")],
        [InlineKeyboardButton("Truy cập Solona SuperTeam", url="https://solonasuperteam.com")],
        [InlineKeyboardButton("FAQ", callback_data="faq")],
        [InlineKeyboardButton("Truy cứu địa điểm ăn uống", callback_data="food")],
        [InlineKeyboardButton("Assistant", callback_data="assistant_menu")],
        [InlineKeyboardButton("Knowledge Portal", callback_data="portal_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

# ---------------------------
# Lệnh /portal - Knowledge Portal
# ---------------------------
async def portal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    query = message_text[len("/portal"):].strip() if len(message_text) > len("/portal") else ""
    if query:
        # Nếu query chứa từ khóa thì trả lời mặc định
        if "Solona" in query:
            await update.message.reply_text("Thông tin Solona: Solona là công ty tiên phong về các giải pháp công nghệ, luôn hướng tới sự đổi mới.")
        elif "Superteam" in query:
            await update.message.reply_text("Thông tin Superteam: Superteam là đối tác chiến lược với nhiều dự án và sự kiện quy mô, chuyên mang đến giá trị sáng tạo.")
        else:
            await update.message.reply_text("Không có dữ liệu")
    else:
        text = "Knowledge Portal - Vui lòng chọn một tùy chọn:"
        keyboard = [
            [InlineKeyboardButton("About us", callback_data="about_us")],
            [InlineKeyboardButton("Khác", callback_data="portal_other")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)

# ---------------------------
# Lệnh /assistant - Twitter Management Assistant
# ---------------------------
async def assistant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Twitter Management Assistant:\n"
            "Danh sách hỗ trợ:\n"
            "1. Hỗ trợ kỹ thuật: 0123456789\n"
            "2. Hỗ trợ sự kiện: 0987654321\n"
            "3. Hỗ trợ marketing: 0911222333")
    keyboard = [
        [InlineKeyboardButton("Khác", callback_data="assistant_other")],
        [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# ---------------------------
# Lệnh /FAQ
# ---------------------------
async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "FAQ - Hãy chọn câu hỏi để xem câu trả lời:"
    keyboard = [
        [InlineKeyboardButton("Làm thế nào để đăng ký sự kiện?", callback_data="faq_1")],
        [InlineKeyboardButton("Sự kiện có tính phí không?", callback_data="faq_2")],
        [InlineKeyboardButton("Làm sao để nhận thông báo cập nhật?", callback_data="faq_3")],
        [InlineKeyboardButton("Khác", callback_data="faq_other")],
        [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# ---------------------------
# Lệnh /event
# ---------------------------
async def event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Các sự kiện đang diễn ra tại Đà Nẵng:\n\n"
            "1. Hội thảo Công nghệ 4.0\n   Thời gian: 20/03/2023, 10:00 AM\n   Địa điểm: Khách sạn Novotel\n\n"
            "2. Triển lãm Nghệ thuật Hiện đại\n   Thời gian: 21/03/2023, 2:00 PM\n   Địa điểm: Bảo tàng Nghệ thuật\n\n"
            "3. Workshop Kỹ năng Lãnh đạo\n   Thời gian: 22/03/2023, 9:00 AM\n   Địa điểm: Trung tâm Hội nghị")
    keyboard = [
        [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# ---------------------------
# Lệnh /eat - Search For Places To Eat
# ---------------------------
async def eat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("food_type", None)
    context.user_data.pop("food_area", None)
    context.user_data.pop("food_budget", None)
    text = "Bạn muốn ăn gì? Vui lòng chọn loại hình:"
    keyboard = [
        [InlineKeyboardButton("Ăn vặt", callback_data="food_type:anvat")],
        [InlineKeyboardButton("Bữa ăn chính", callback_data="food_type:bua_chinh")],
        [InlineKeyboardButton("Ăn chay", callback_data="food_type:an_chay")],
        [InlineKeyboardButton("Khác", callback_data="food_type:other")],
        [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

# ---------------------------
# Callback Query Handler - Xử lý các lựa chọn từ Inline Keyboard
# ---------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # Menu chính và điều hướng
    if data == "start":
        await start(update, context)

    # ---------------------------
    # Event và chi tiết event
    # ---------------------------
    elif data == "events":
        keyboard = [
            [InlineKeyboardButton("Hội thảo Công nghệ 4.0", callback_data="event_tech")],
            [InlineKeyboardButton("Triển lãm Nghệ thuật Hiện đại", callback_data="event_art")],
            [InlineKeyboardButton("Workshop Kỹ năng Lãnh đạo", callback_data="event_lead")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = ("Các sự kiện đang diễn ra tại Đà Nẵng:\n\n"
                "1. Hội thảo Công nghệ 4.0\n   Thời gian: 20/03/2023, 10:00 AM\n   Địa điểm: Khách sạn Novotel\n\n"
                "2. Triển lãm Nghệ thuật Hiện đại\n   Thời gian: 21/03/2023, 2:00 PM\n   Địa điểm: Bảo tàng Nghệ thuật\n\n"
                "3. Workshop Kỹ năng Lãnh đạo\n   Thời gian: 22/03/2023, 9:00 AM\n   Địa điểm: Trung tâm Hội nghị")
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif data.startswith("event_"):
        event_type = data.split("_")[1]
        if event_type == "tech":
            text = ("Hội thảo Công nghệ 4.0:\n"
                    "- Thời gian: 20/03/2023, 10:00 AM\n"
                    "- Địa điểm: Khách sạn Novotel, Đà Nẵng\n"
                    "- Nội dung: Cập nhật các xu hướng Công nghệ 4.0 và ứng dụng thực tiễn.")
        elif event_type == "art":
            text = ("Triển lãm Nghệ thuật Hiện đại:\n"
                    "- Thời gian: 21/03/2023, 2:00 PM\n"
                    "- Địa điểm: Bảo tàng Nghệ thuật, Đà Nẵng\n"
                    "- Nội dung: Trưng bày các tác phẩm nghệ thuật độc đáo và sáng tạo.")
        elif event_type == "lead":
            text = ("Workshop Kỹ năng Lãnh đạo:\n"
                    "- Thời gian: 22/03/2023, 9:00 AM\n"
                    "- Địa điểm: Trung tâm Hội nghị, Đà Nẵng\n"
                    "- Nội dung: Phát triển kỹ năng lãnh đạo và quản lý nhóm hiệu quả.")
        keyboard = [
            [InlineKeyboardButton("Trở về danh sách sự kiện", callback_data="events")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    # ---------------------------
    # FAQ và các câu hỏi chi tiết
    # ---------------------------
    elif data == "faq":
        keyboard = [
            [InlineKeyboardButton("Làm thế nào để đăng ký sự kiện?", callback_data="faq_1")],
            [InlineKeyboardButton("Sự kiện có tính phí không?", callback_data="faq_2")],
            [InlineKeyboardButton("Làm sao để nhận thông báo cập nhật?", callback_data="faq_3")],
            [InlineKeyboardButton("Khác", callback_data="faq_other")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("FAQ - Hãy chọn câu hỏi để xem câu trả lời:", reply_markup=reply_markup)

    elif data.startswith("faq_"):
        faq_id = data.split("_")[1]
        if faq_id == "1":
            text = ("Câu hỏi: Làm thế nào để đăng ký sự kiện?\n"
                    "Trả lời: Bạn có thể đăng ký qua trang web của chúng tôi hoặc trực tiếp tại sự kiện.")
        elif faq_id == "2":
            text = ("Câu hỏi: Sự kiện có tính phí không?\n"
                    "Trả lời: Hầu hết các sự kiện đều miễn phí, chỉ có một số sự kiện đặc biệt có thể có phí.")
        elif faq_id == "3":
            text = ("Câu hỏi: Làm sao để nhận thông báo cập nhật?\n"
                    "Trả lời: Bạn sẽ nhận được thông báo qua Telegram và email khi có sự thay đổi.")
        keyboard = [
            [InlineKeyboardButton("Trở về FAQ", callback_data="faq")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif data == "faq_other":
        context.user_data["awaiting_input"] = "faq"
        await query.edit_message_text("Vui lòng nhập câu hỏi của bạn:", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))

    # ---------------------------
    # Quy trình truy cứu địa điểm ăn uống
    # ---------------------------
    elif data == "food":
        context.user_data.pop("food_type", None)
        context.user_data.pop("food_area", None)
        context.user_data.pop("food_budget", None)
        text = "Bạn muốn ăn gì? Vui lòng chọn loại hình:"
        keyboard = [
            [InlineKeyboardButton("Ăn vặt", callback_data="food_type:anvat")],
            [InlineKeyboardButton("Bữa ăn chính", callback_data="food_type:bua_chinh")],
            [InlineKeyboardButton("Ăn chay", callback_data="food_type:an_chay")],
            [InlineKeyboardButton("Khác", callback_data="food_type:other")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif data.startswith("food_type:"):
        option = data.split(":")[1]
        if option == "other":
            context.user_data["awaiting_input"] = "food_type"
            await query.edit_message_text("Nhập loại hình ăn bạn muốn:", 
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))
        else:
            context.user_data["food_type"] = option
            text = "Bạn muốn ăn ở khu vực nào? Vui lòng chọn khu vực:"
            keyboard = [
                [InlineKeyboardButton("Bán đảo Sơn Trà", callback_data="food_area:sontra")],
                [InlineKeyboardButton("Cẩm Lệ", callback_data="food_area:camle")],
                [InlineKeyboardButton("Hải Châu", callback_data="food_area:hch")],
                [InlineKeyboardButton("Ngũ Hành Sơn", callback_data="food_area:nguhanhson")],
                [InlineKeyboardButton("Hòa Vang", callback_data="food_area:hoavang")],
                [InlineKeyboardButton("Khác", callback_data="food_area:other")],
                [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)

    elif data.startswith("food_area:"):
        option = data.split(":")[1]
        if option == "other":
            context.user_data["awaiting_input"] = "food_area"
            await query.edit_message_text("Nhập khu vực bạn muốn ăn:", 
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))
        else:
            context.user_data["food_area"] = option
            text = "Budget cho một bữa ăn của bạn là bao nhiêu? Vui lòng chọn mức ngân sách:"
            keyboard = [
                [InlineKeyboardButton("Dưới 100k", callback_data="food_budget:low")],
                [InlineKeyboardButton("100k - 300k", callback_data="food_budget:medium")],
                [InlineKeyboardButton("Trên 300k", callback_data="food_budget:high")],
                [InlineKeyboardButton("Khác", callback_data="food_budget:other")],
                [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)

    elif data.startswith("food_budget:"):
        option = data.split(":")[1]
        if option == "other":
            context.user_data["awaiting_input"] = "food_budget"
            await query.edit_message_text("Nhập mức ngân sách của bạn:", 
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))
        else:
            context.user_data["food_budget"] = option
            food_type = context.user_data.get("food_type", "không xác định")
            food_area = context.user_data.get("food_area", "không xác định")
            text = (f"Dựa trên lựa chọn của bạn:\n"
                    f"- Loại hình: {food_type}\n"
                    f"- Khu vực: {food_area}\n"
                    f"- Budget: {option}\n\n"
                    "Dưới đây là gợi ý một số quán ăn tại Đà Nẵng:\n"
                    "1. Quán A - Món đặc trưng: Bún chả\n"
                    "2. Quán B - Món đặc trưng: Phở bò\n"
                    "3. Quán C - Món đặc trưng: Cơm gà")
            keyboard = [[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)

    # ---------------------------
    # Assistant menu
    # ---------------------------
    elif data == "assistant_menu":
        # Gọi trực tiếp hàm assistant_command nếu cần
        text = ("Twitter Management Assistant:\n"
                "Danh sách hỗ trợ:\n"
                "1. Hỗ trợ kỹ thuật: 0123456789\n"
                "2. Hỗ trợ sự kiện: 0987654321\n"
                "3. Hỗ trợ marketing: 0911222333")
        keyboard = [
            [InlineKeyboardButton("Khác", callback_data="assistant_other")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif data == "assistant_other":
        context.user_data["awaiting_input"] = "assistant"
        await query.edit_message_text("Vui lòng nhập lĩnh vực cần hỗ trợ của bạn:", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))

    # ---------------------------
    # Portal menu
    # ---------------------------
    elif data == "portal_menu":
        text = "Knowledge Portal - Vui lòng chọn một tùy chọn:"
        keyboard = [
            [InlineKeyboardButton("About us", callback_data="about_us")],
            [InlineKeyboardButton("Khác", callback_data="portal_other")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif data == "about_us":
        text = ("Solona SuperTeam là đối tác hàng đầu trong lĩnh vực tổ chức sự kiện, "
                "luôn cam kết mang đến trải nghiệm sáng tạo và chuyên nghiệp cho khách hàng.")
        keyboard = [
            [InlineKeyboardButton("Trở về portal", callback_data="portal_menu")],
            [InlineKeyboardButton("Trở về trang chính", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif data == "portal_other":
        context.user_data["awaiting_input"] = "portal"
        await query.edit_message_text("Vui lòng nhập câu hỏi của bạn:", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))
        
# ---------------------------
# Text Handler - Xử lý input nhập tay khi chọn "Khác"
# ---------------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "awaiting_input" in context.user_data:
        field = context.user_data.pop("awaiting_input")
        # Hiển thị phản hồi mặc định do chưa có dữ liệu thực tế
        await update.message.reply_text("Không có dữ liệu", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Trở về trang chính", callback_data="start")]]))
    else:
        await update.message.reply_text("Vui lòng sử dụng các lệnh hoặc nút được cung cấp.")

# ---------------------------
# Hàm main
# ---------------------------
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("portal", portal_command))
    application.add_handler(CommandHandler("assistant", assistant_command))
    application.add_handler(CommandHandler("FAQ", faq_command))
    application.add_handler(CommandHandler("event", event_command))
    application.add_handler(CommandHandler("eat", eat_command))
    
    # CallbackQuery Handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Text messages (cho input "Khác")
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
