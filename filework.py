import json
import aiofiles
import asyncio
from config import database


async def load_stats():
    try:
        async with aiofiles.open(database, "r", encoding="utf-8") as f:
            try:
                data = await f.read()
                stats = json.loads(data)
                new_stats = {}
                for key, value in stats.items():
                    try:
                        new_stats[int(key)] = value
                    except ValueError:
                        await print(f"Не удалось преобразовать ключ '{key}' в целое число. Пропускаем.")
                        new_stats[key] = value
                stats = new_stats
            except json.JSONDecodeError:
                stats = {}
                print("Файл stats.json пуст или содержит невалидный JSON.  Загружен пустой словарь.")
            return stats
    except FileNotFoundError:
        return {}

async def save_stats(stats):
    try:
        async with aiofiles.open(database, "w", encoding="utf-8") as f:
            await f.write(json.dumps(stats, indent=4, ensure_ascii=False))
    except FileNotFoundError:
        return {}