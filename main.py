from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
import asyncio
from config import BOT_TOKEN, WEBAPP_URL

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

class CardForm(StatesGroup):
    waiting_for_cards = State()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hola, envíame tus 10 tarjetas (una por línea):")
    await dp.fsm.set_state(message.from_user.id, CardForm.waiting_for_cards)

@dp.message(CardForm.waiting_for_cards)
async def receive_cards(message: Message, state: FSMContext):
    tarjetas = message.text.strip().split("\n")
    if len(tarjetas) != 10:
        await message.answer("Por favor, envía exactamente 10 tarjetas, una por línea.")
        return

    await message.answer("Verificando las tarjetas, por favor espera...")

    try:
        response = requests.post(f"{WEBAPP_URL}/verificar", json={"tarjetas": tarjetas})

        result = response.json()
    except Exception as e:
        await message.answer("Error al conectar con la WebApp.")
        return

    texto = "✅ Resultados de las tarjetas:\n\n"
    for card, estado in result.get("resultados", {}).items():
        texto += f"{card}: {'✅ Aprobada' if estado else '❌ Rechazada'}\n"

    await message.answer(texto)
    await state.clear()
    if __name__ == "__main__":
    import asyncio

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())

