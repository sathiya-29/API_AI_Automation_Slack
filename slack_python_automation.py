import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from openai import OpenAI


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")


# --------------------------------------------------
# Validate configuration
# --------------------------------------------------

if not SLACK_BOT_TOKEN:
    raise RuntimeError("SLACK_BOT_TOKEN is missing in .env")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing in .env")

if not SLACK_CHANNEL_ID:
    raise RuntimeError("SLACK_CHANNEL_ID is missing in .env")


# --------------------------------------------------
# Create clients
# --------------------------------------------------

slack_client = WebClient(
    token=SLACK_BOT_TOKEN
)

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)


# --------------------------------------------------
# Send message to Slack
# --------------------------------------------------

def send_to_slack(message):

    response = slack_client.chat_postMessage(
        channel=SLACK_CHANNEL_ID,
        text=message
    )

    return response


# --------------------------------------------------
# Ask AI for ingredients
# --------------------------------------------------

def get_recipe_ingredients(recipe_name):

    prompt = f"""
You are a recipe ingredient assistant.

The user wants to prepare:

{recipe_name}

Identify all ingredients/products required to prepare this recipe.

Return ONLY this format:

🛒 Ingredients Required

• Ingredient - quantity
• Ingredient - quantity
• Ingredient - quantity

Rules:
- Include all important ingredients.
- Include approximate quantities for 4 people.
- Mention optional ingredients as "(optional)".
- Correct obvious spelling mistakes.
- Do not provide cooking instructions.
- Do not provide explanations.
- Do not use JSON.
- Do not use a code block.
"""

    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip()


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main():

    print("=" * 60)
    print("🍳 Slack Recipe Bot")
    print("=" * 60)

    recipe_name = input("Enter recipe name: ").strip()

    if not recipe_name:
        print("❌ Please enter a recipe name.")
        return

    print()
    print(f"Recipe: {recipe_name}")

    # ----------------------------------------------
    # Step 1: Send recipe request to Slack
    # ----------------------------------------------

    print("→ Sending recipe request to Slack...")

    send_to_slack(
        f"🍳 Recipe requested: *{recipe_name}*"
    )

    print("✓ Recipe request sent to Slack")

    # ----------------------------------------------
    # Step 2: Ask AI
    # ----------------------------------------------

    print("→ Asking AI for ingredients...")

    ingredients = get_recipe_ingredients(
        recipe_name
    )

    print("✓ AI generated ingredient list")

    # ----------------------------------------------
    # Step 3: Send AI response to Slack
    # ----------------------------------------------

    print("→ Sending ingredients to Slack...")

    send_to_slack(
        ingredients
    )

    print("✓ Ingredients sent to Slack")

    print()
    print("=" * 60)
    print("✅ Recipe automation completed")
    print("=" * 60)


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    main()