from datetime import date

from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from intel_hub.db.repository import HubRepository
from intel_hub.db.session import SessionLocal


class TelegramNotifier:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token) if token else None

    async def send_message(self, chat_id: int, text: str) -> None:
        if self.bot is None:
            return
        await self.bot.send_message(chat_id=chat_id, text=text)


class TelegramBotService:
    def __init__(self, token: str):
        self.token = token
        self.app = Application.builder().token(token).build()
        self._register_handlers()

    def _register_handlers(self) -> None:
        self.app.add_handler(CommandHandler("start", self.handle_start))
        self.app.add_handler(CommandHandler("domains", self.handle_domains))
        self.app.add_handler(CommandHandler("alert", self.handle_alert))
        self.app.add_handler(CommandHandler("topics", self.handle_topics))
        self.app.add_handler(CommandHandler("digest", self.handle_digest))

    def run_polling(self) -> None:
        self.app.run_polling(drop_pending_updates=True)

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None:
            return
        chat = update.effective_chat
        with SessionLocal() as db:
            repo = HubRepository(db)
            repo.upsert_subscriber(
                {
                    "chat_id": chat.id,
                    "username": update.effective_user.username if update.effective_user else None,
                    "alert_level": "high",
                    "domain_filter": ["crypto"],
                    "topic_filter": None,
                    "is_active": True,
                }
            )
        await update.message.reply_text("구독이 시작되었습니다. /domains, /alert, /topics 명령을 사용하세요.")

    async def handle_domains(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None or update.message is None:
            return
        args = context.args
        domain_filter = ["crypto"] if not args else [arg.strip() for arg in args[0].split(",") if arg.strip()]
        if "all" in domain_filter:
            domain_filter = ["crypto", "ai_ml"]
        with SessionLocal() as db:
            repo = HubRepository(db)
            repo.update_subscriber_filters(update.effective_chat.id, domain_filter=domain_filter)
        await update.message.reply_text(f"도메인 필터가 설정되었습니다: {', '.join(domain_filter)}")

    async def handle_alert(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None or update.message is None:
            return
        level = context.args[0] if context.args else "high"
        if level not in {"all", "high", "critical"}:
            await update.message.reply_text("/alert {all|high|critical} 형식으로 입력하세요.")
            return

        with SessionLocal() as db:
            repo = HubRepository(db)
            repo.update_subscriber_filters(update.effective_chat.id, alert_level=level)
        await update.message.reply_text(f"알림 레벨이 {level}로 설정되었습니다.")

    async def handle_topics(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None or update.message is None:
            return
        if not context.args:
            await update.message.reply_text("/topics BTC,SOL 형식으로 입력하세요.")
            return
        topics = [topic.strip().upper() for topic in context.args[0].split(",") if topic.strip()]
        with SessionLocal() as db:
            repo = HubRepository(db)
            repo.update_subscriber_filters(update.effective_chat.id, topic_filter=topics)
        await update.message.reply_text(f"관심 토픽이 설정되었습니다: {', '.join(topics)}")

    async def handle_digest(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None or update.message is None:
            return
        domain = context.args[0] if context.args else "crypto"
        if domain not in {"crypto", "ai_ml"}:
            await update.message.reply_text("/digest {crypto|ai_ml} 형식으로 입력하세요.")
            return
        target_date = date.today()
        with SessionLocal() as db:
            repo = HubRepository(db)
            digests = repo.list_digests(domain, target_date)

        if not digests:
            await update.message.reply_text("오늘 생성된 다이제스트가 아직 없습니다.")
            return

        domain_label = "🪙 Crypto" if domain == "crypto" else "🤖 AI/ML"
        lines = [f"{domain_label} {target_date} 다이제스트"]
        for digest in digests[:8]:
            lines.append(f"- {digest.topic}: {digest.summary}")
        await update.message.reply_text("\n".join(lines))
