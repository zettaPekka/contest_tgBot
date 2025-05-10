from aiogram.types import Message, ContentType


async def check_message_type(message: Message):
    if message.content_type != ContentType.TEXT:
        await message.answer('Введите корректное значение')
        return False
    return True

async def check_digit(message: Message):
    if message.content_type != ContentType.TEXT or not message.text.isdigit():
        await message.answer('Введите корректное значение')
        return False
    return True
