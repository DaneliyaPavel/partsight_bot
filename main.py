import os
os.environ["AIOGRAM_NO_UVLOOP"] = "1"      # работаем на чистом asyncio

import asyncio
import logging
import configparser
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile

import catalog_loader, parser_docx, matcher, generator_act


# ---------- конфигурация ----------
cfg = configparser.ConfigParser()
cfg.read("config.ini")

proxy_url = cfg["telegram"].get("PROXY_URL", None)  # оставьте пустым, если прокси не нужен
bot       = Bot(token=cfg["telegram"]["BOT_TOKEN"], proxy=proxy_url)
dp        = Dispatcher()


# ---------- /start ----------
@dp.message(F.text == "/start")
async def cmd_start(m: Message):
    await m.answer(
        "👋 Привет! Пришлите Word-запрос с перечнем ЗИП — и я верну акт с оценкой "
        "возможности производства («да»/«нет»)."
    )


# ---------- обработка присланного документа ----------
@dp.message(F.document)
async def doc_handler(m: Message):
    doc = m.document
    in_path = Path("incoming") / doc.file_name
    in_path.parent.mkdir(exist_ok=True)

    await bot.download(doc, destination=in_path)
    await m.reply(f"Файл «{in_path.name}» получен, начинаю обработку…")

    # тяжёлые вычисления выполняем в отдельном потоке
    act_path = await asyncio.to_thread(process_request, in_path)

    await m.reply_document(
        FSInputFile(act_path),
        caption="Готовый акт ✅"
    )


# ---------- бизнес-логика ----------
def process_request(file_path: Path) -> Path:
    items = parser_docx.parse_request_docx(file_path)

    packets = []
    for it in items:
        can = matcher.can_produce(
            it["naimenovanie"],
            catalog_pref                       # глобальный набор префиксов каталога
        )
        packets.append(
            dict(
                material     = it["material"],
                naimenovanie = it["naimenovanie"],
                vozmoznost   = "да" if can else "нет",
                rekomendacii = (
                    "Производство возможно."
                    if can else
                    "На данный момент производство отсутствует."
                ),
            )
        )

    # generator_act.build_act — синхронная функция
    return generator_act.build_act(packets)


# ---------- запуск ----------
async def main():
    global catalog_pref
    catalog_pref = await catalog_loader.load_catalog()
    logging.basicConfig(level=logging.INFO)
    print(f"Каталог загружен, 5-буквенных префиксов: {len(catalog_pref)}")

    # на всякий случай удаляем старый webhook и запускаем long-polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
