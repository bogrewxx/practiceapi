import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters


OMDB_API_KEY = "8750210"
TELEGRAM_TOKEN = "7586998595:AAF7oV-lYaVNFHSdOfQPC1_RPDOwusC5aksdelllk"
OMDB_URL = "http://www.omdbapi.com/"


logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені назву фільму, і я знайду інформацію про нього 🍿")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_title = update.message.text
    async with httpx.AsyncClient() as client:
        params = {
            "t": movie_title,
            "apikey": OMDB_API_KEY,
            "plot": "short",
            "r": "json"
        }
        response = await client.get(OMDB_URL, params=params)
        data = response.json()

        if data.get("Response") == "False":
            await update.message.reply_text(f"На жаль, фільм '{movie_title}' не знайдено.")
        else:
            title = data.get("Title", "Невідомо")
            year = data.get("Year", "Невідомо")
            plot = data.get("Plot", "Немає опису")
            rating = data.get("imdbRating", "Немає")
            genre = data.get("Genre", "Невідомо")
            poster = data.get("Poster", "")

            message = (
                f"🎬 <b>{title}</b> ({year})\n"
                f"⭐️ Рейтинг IMDb: {rating}\n"
                f"🎭 Жанр: {genre}\n"
                f"📝 Опис: {plot}"
            )

            await update.message.reply_photo(photo=poster, caption=message, parse_mode="HTML")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🎥 Бот запущено. Очікує повідомлень...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
