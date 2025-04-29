import requests
import time
import random

# Fallback responses in case the API is unavailable
FALLBACK_POSITIVE_FEEDBACK = [
    "Fantastic job! 🌟",
    "You got it right! 🎉",
    "Amazing sorting! 👏",
    "Perfect match! 💯",
    "You're a sorting star! ⭐",
    "Great shopping skills! 🛒",
    "Excellent choice! 🏆",
    "That's correct! 🎯",
    "Super smart! 🧠",
    "Wow, you're good at this! 🥳"
]

FALLBACK_NEGATIVE_FEEDBACK = [
    "Try another basket! 🤔",
    "Not quite right, try again! 🔄",
    "Let's try a different basket! 🧺",
    "Almost there, one more try! 👍",
    "Think about where this food comes from! 💭",
    "Hmm, not that one. Try again! 🧐",
    "Let's think about this food! 🍽️",
    "Good effort! Try another basket! 🚀",
    "Another basket might be better! 🛍️",
    "Keep trying, you'll get it! 💪"
]

FALLBACK_FUN_FACTS = {
    "Apple": "Apples float in water because they're 25% air! 🍎",
    "Banana": "Bananas are berries, but strawberries aren't! 🍌",
    "Carrot": "Carrots can help you see in the dark! 🥕",
    "Milk": "Milk helps make your bones strong! 🥛",
    "Bread": "Bread dough rises because of tiny bubbles! 🍞",
    "Chicken": "Chickens are related to dinosaurs! 🦖",
    "Rice": "Rice is eaten by half the people on Earth every day! 🍚",
    "Eggs": "Some eggs have spots to help hide them! 🥚",
    "Cheese": "Cheese is milk that's been transformed! 🧀",
    "Strawberry": "Strawberries wear their seeds on the outside! 🍓",
}

def get_bot_response(prompt, max_retries=2):
    """
    Try to get a response from a language model API.
    Falls back to pre-written responses if API fails.
    
    This is a simplified version that doesn't actually call an external API
    to avoid requiring API keys.
    """
    try:
        # In a real implementation, this would call a language model API
        # Example:
        # response = requests.post(
        #     "https://api.huggingface.co/models/gpt2",
        #     json={"inputs": prompt},
        #     headers={"Authorization": f"Bearer {API_KEY}"}
        # )
        # return response.json()[0]["generated_text"]
        
        # For this implementation, we'll just use fallback responses
        if "positive feedback" in prompt.lower():
            return random.choice(FALLBACK_POSITIVE_FEEDBACK)
        elif "negative feedback" in prompt.lower() or "incorrect" in prompt.lower():
            return random.choice(FALLBACK_NEGATIVE_FEEDBACK)
        elif "fact about" in prompt.lower():
            item_name = prompt.split("fact about")[1].split("that")[0].strip()
            # Try to find a matching fact
            for food, fact in FALLBACK_FUN_FACTS.items():
                if food.lower() in item_name.lower():
                    return fact
            # Return a generic fact if no match
            return f"Did you know foods give us energy to play and grow? 🌱"
        elif "summary" in prompt.lower():
            name = prompt.split("named")[1].split("who")[0].strip()
            return f"Great job shopping today, {name}! You're learning so much about different foods and where they belong. Keep exploring and learning! 🌟"
        else:
            # Generic response for other prompts
            return "You're doing great! Keep learning about foods! 🍎🥕🍌"
            
    except Exception as e:
        # In case of any error, return None
        print(f"Error getting bot response: {e}")
        return None