import aiohttp

async def translate(joke_id, text, logger):
    url = "https://clients5.google.com/translate_a/t"
    params = {
        "client": "dict-chrome-ex",
        "sl": "auto",
        "tl": "de",
        "q": text
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                data = await response.json()
                # The translated text is the first item in the first sublist
                translated = data[0][0]
                logger.info(f"translated: {translated}")
                return {"id": joke_id, "translated_joke": translated}
    except Exception as e:
        logger.error(f"Translation failed for joke {joke_id}: {e}")
        return {"id": joke_id, "error": str(e)}
