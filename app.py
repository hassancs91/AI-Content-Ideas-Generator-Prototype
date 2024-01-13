# Importing necessary libraries and functions
import json  # Used for working with JSON data
import asyncio  # Used for asynchronous programming
from pydantic import BaseModel  # Pydantic for data validation and settings management
from typing import List  # Used for type hinting
from serp import search_google_web_automation  # Custom function to automate Google searches
from my_functions import get_article_from_url, generate_ideas  # Custom functions for processing articles

# Setting input parameters
search_query = "AI in marketing"  # The query to search for
NUMBER_OF_RESULTS = 10  # Number of search results to process

# Template for the prompt to be used later
prompt = "extract 5-10 content ideas from the [post], and return the list in json format, [post]: {post}"

# Pydantic model for data validation
class Ideas(BaseModel):
    ideas: List[str]  # Defines a list of strings to store ideas

# Main asynchronous function
async def main():
    # Step 1: Fetch the top 100 search results
    try:
        # Fetch search results using a custom function
        search_results = search_google_web_automation(search_query,NUMBER_OF_RESULTS)
    except Exception as e:
        # Handle exceptions during search and print error message
        print(f"Error fetching search results: {e}")
        return

    # Step 2: Initialize a list to store all ideas
    all_ideas = []  # List to store the ideas generated

    # Step 3: Process each search result
    for result in search_results:
        try:
            # Extract URL from the search result
            result_url = result["url"]
            # Get article content from the URL using a custom function
            result_content = get_article_from_url(result_url)

            # If content is successfully retrieved
            if result_content:
                # Format the prompt with the retrieved content
                result_prompt = prompt.format(post=result_content)
                # Generate ideas using another custom asynchronous function
                ideas_object = await generate_ideas(result_prompt, Ideas)

                # If ideas are generated, extend the all_ideas list
                if ideas_object and ideas_object.ideas:
                    all_ideas.extend(ideas_object.ideas)
        except Exception as e:
            # Handle exceptions during processing of each result
            print(f"Error processing search result {result}: {e}")

    # Step 4: Convert the ideas to JSON and output
    # Serialize the list of ideas into a JSON formatted string
    json_output = json.dumps(all_ideas, indent=4)
    # Print the JSON string
    print(json_output)

# Check if the script is run directly and not imported
if __name__ == "__main__":
    # Run the main function using asyncio
    asyncio.run(main())
