import newspaper
import asyncio
import openai
from openai import AsyncOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import time

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY is None:
    raise ValueError("Please set the OPENAI_API_KEY in .env file.")

openai.api_key = OPENAI_API_KEY
async_openai_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
)

import instructor
instructor.apatch(async_openai_client)


def get_article_from_url(url):
    try:
        # Scrape the web page for content using newspaper
        article = newspaper.Article(url)
        # Download the article's content with a timeout of 10 seconds
        article.download()
        # Check if the download was successful before parsing the article
        if article.download_state == 2:
            article.parse()
            # Get the main text content of the article
            article_text = article.text
            return article_text
        else:
            print("Error: Unable to download article from URL:", url)
            return None
    except Exception as e:
        print("An error occurred while processing the URL:", url)
        print(str(e))
        return None

MAX_RETRIES = 3
RETRY_DELAY = 2
MODEL_FUNCTION = "gpt-3.5-turbo-1106"




async def generate_ideas(user_prompt,response_model):
    """Generates a response using OpenAI API and caches it if enabled."""
    response = None

    for attempt in range(MAX_RETRIES):
        try:
            resut: response_model = await async_openai_client.chat.completions.create(
                model=MODEL_FUNCTION,
                response_model=response_model,
                messages=[{"role": "user", "content": user_prompt}]
            )

            return resut
        except Exception as e:
            if attempt < MAX_RETRIES - 1:  # don't wait after the last attempt
                await asyncio.sleep(RETRY_DELAY * (2**attempt))
            else:
                print(f"generate_ideas failes after max retries: {e}")
                return None

        return response

