from database import Base, engine, SessionLocal
import re

async def get_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_cookie(cookie: str, key: str):
    cookies = dict(token.split('=') for token in cookie.split('; ') if token.strip())
    return cookies.get(key)

def get_preferred_language(accept_language: str) -> str:
    """
    Extracts the preferred language from the Accept-Language header.

    Args:
        accept_language (str): The Accept-Language header value.

    Returns:
        str: The preferred language code (ru or en).
    """

    if not accept_language:
        return 'en'

    # Split the Accept-Language header value by comma
    languages = accept_language.split(',')

    # Iterate over the languages and extract the language code
    for language in languages:
        # Remove any whitespace
        language = language.strip()

        # Extract the language code and quality value
        match = re.match(r'^(\w+)(?:;q=(\d.\d+))?$', language)
        if match:
            language_code = match.group(1)

            # Check if the language code is "ru" or "en"
            if language_code in ['ru', 'en']:
                return language_code

    # Return "en" as the default language if no preferred language is found
    return 'en'
