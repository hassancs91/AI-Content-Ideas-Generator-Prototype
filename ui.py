# Import necessary libraries
import streamlit as st
import asyncio
import json
from pydantic import BaseModel
from typing import List
from serp import search_google_web_automation
from my_functions import get_article_from_url, generate_ideas


prompt = "extract 5-10 content ideas from the [post], and return the list in json format, [post]: {post}"

# Define the Ideas class
class Ideas(BaseModel):
    ideas: List[str]

# Async function to process the main logic
async def main(search_query, st):
    try:
        search_results = search_google_web_automation(search_query, 10)
        all_ideas = []

        # Initialize progress bar
        progress_bar = st.progress(0)
        total_results = len(search_results)
        
        for index, result in enumerate(search_results):
            try:
                # Update progress bar
                progress_bar.progress((index + 1) / total_results)

                result_url = result["url"]
                result_content = get_article_from_url(result_url)

                if result_content:
                    result_prompt = prompt.format(post=result_content)
                    ideas_object = await generate_ideas(result_prompt, Ideas)

                    if ideas_object and ideas_object.ideas:
                        all_ideas.extend(ideas_object.ideas)
            except Exception as e:
                st.error(f"Error processing search result {result}: {e}")

        # Display the number of records
        st.write(f"Number of Ideas Generated: {len(all_ideas)}")

        # Convert the ideas to JSON and display in an expander
        json_output = json.dumps(all_ideas, indent=4)
        with st.expander("View Generated Ideas (JSON)"):
            st.json(json_output)

    except Exception as e:
        st.error(f"Error fetching search results: {e}")
    finally:
        # Ensure progress bar is filled when process is complete
        progress_bar.progress(100)

# Streamlit UI setup
st.title("Content Idea Generator")

# User input fields
search_query = st.text_input("Enter the search query:", "AI in marketing")

# Button to trigger the process
if st.button("Generate Ideas"):
    # Run the main function asynchronously
    asyncio.run(main(search_query, st))
