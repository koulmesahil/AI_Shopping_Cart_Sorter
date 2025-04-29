import streamlit as st
import random
import uuid
import emoji
import time
from datetime import datetime
import os
import json

# Food categories and items for the game
FOOD_CATEGORIES = {
    "Fruits": {
        "emoji": "🍎",
        "items": ["Apple", "Banana", "Orange", "Grapes", "Strawberry", "Watermelon", 
                 "Pineapple", "Mango", "Blueberries", "Peach", "Pear", "Kiwi"]
    },
    "Vegetables": {
        "emoji": "🥕",
        "items": ["Carrot", "Broccoli", "Spinach", "Tomato", "Cucumber", "Lettuce", 
                 "Potato", "Corn", "Peas", "Bell Pepper", "Onion", "Celery"]
    },
    "Dairy": {
        "emoji": "🥛",
        "items": ["Milk", "Cheese", "Yogurt", "Butter", "Ice Cream", "Cream", 
                 "Cottage Cheese", "Chocolate Milk", "Milkshake"]
    },
    "Grains": {
        "emoji": "🍞",
        "items": ["Bread", "Rice", "Pasta", "Cereal", "Oatmeal", "Crackers", 
                 "Bagel", "Tortilla", "Pancake", "Waffle"]
    },
    "Protein": {
        "emoji": "🥩",
        "items": ["Chicken", "Eggs", "Fish", "Beans", "Nuts", "Turkey", 
                 "Tofu", "Peanut Butter", "Tuna"]
    }
}

# Additional categories for higher levels
ADVANCED_CATEGORIES = {
    "Sweets": {
        "emoji": "🍬",
        "items": ["Candy", "Chocolate", "Cake", "Cookies", "Donut", "Lollipop", 
                 "Cupcake", "Gummy Bears", "Jelly Beans"]
    },
    "Drinks": {
        "emoji": "🥤",
        "items": ["Water", "Juice", "Soda", "Lemonade", "Tea", "Coffee", 
                 "Smoothie", "Hot Chocolate"]
    },
    "Snacks": {
        "emoji": "🍿",
        "items": ["Popcorn", "Chips", "Pretzels", "Granola Bar", "Trail Mix", 
                 "Fruit Snacks", "Cheese Sticks"]
    }
}

def init_session_state():
    """Initialize session state variables if they don't exist"""
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    
    if 'child_name' not in st.session_state:
        st.session_state.child_name = ''
        
    if 'child_age' not in st.session_state:
        st.session_state.child_age = '5'
        
    if 'score' not in st.session_state:
        st.session_state.score = 0
        
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
        
    if 'total_attempts' not in st.session_state:
        st.session_state.total_attempts = 0
        
    if 'current_items' not in st.session_state:
        st.session_state.current_items = []
        
    if 'current_baskets' not in st.session_state:
        st.session_state.current_baskets = []
        
    if 'selected_item' not in st.session_state:
        st.session_state.selected_item = None
        
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ''
        
    if 'feedback_type' not in st.session_state:
        st.session_state.feedback_type = ''
        
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []

def generate_items_for_level(level, age):
    """Generate items and baskets for a given level"""
    # Scale difficulty based on level and age
    num_categories = min(3 + (level // 2), 5)  # Start with 3 categories, add more at higher levels
    items_per_category = min(2 + level, 5)     # Start with 2 items per category, increase with level
    
    # Reduce complexity for younger children
    if age < 5:
        num_categories = min(num_categories, 3)
        items_per_category = min(items_per_category, 3)
    
    # Select categories
    available_categories = list(FOOD_CATEGORIES.keys())
    
    # Add advanced categories for higher levels and older children
    if level >= 3 and age >= 5:
        available_categories.extend(list(ADVANCED_CATEGORIES.keys()))
    
    # Randomly select categories for this level
    random.shuffle(available_categories)
    selected_categories = available_categories[:num_categories]
    
    # Create baskets
    baskets = []
    for category in selected_categories:
        # Get the right category dictionary
        if category in FOOD_CATEGORIES:
            cat_dict = FOOD_CATEGORIES
        else:
            cat_dict = ADVANCED_CATEGORIES
            
        basket = {
            "id": f"basket_{uuid.uuid4()}",
            "label": category,
            "emoji": cat_dict[category]["emoji"]
        }
        baskets.append(basket)
    
    # Create items
    items = []
    for category in selected_categories:
        # Get the right category dictionary
        if category in FOOD_CATEGORIES:
            cat_dict = FOOD_CATEGORIES
        else:
            cat_dict = ADVANCED_CATEGORIES
            
        # Get a random selection of items from this category
        category_items = random.sample(cat_dict[category]["items"], 
                                      min(items_per_category, len(cat_dict[category]["items"])))
        
        for item_name in category_items:
            item = {
                "id": f"item_{uuid.uuid4()}",
                "name": item_name,
                "type": category
            }
            items.append(item)
    
    # Shuffle items
    random.shuffle(items)
    
    return items, baskets

def check_sorting(item, basket):
    """Check if an item is correctly sorted into a basket"""
    return item["type"] == basket["label"]

def get_feedback(is_correct, item, basket):
    """Generate feedback for sorting action"""
    if is_correct:
        return f"Great job! {item['name']} goes in {basket['label']}! 🎉"
    else:
        return f"Not quite! Try another basket for {item['name']}. 🤔"

def save_session_data():
    """Save session data to a file"""
    data = {
        "child_name": st.session_state.child_name,
        "child_age": st.session_state.child_age,
        "score": st.session_state.score,
        "highest_level": st.session_state.current_level,
        "total_attempts": st.session_state.total_attempts,
        "game_history": st.session_state.game_history,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate a filename with timestamp
    filename = f"data/game_session_{int(time.time())}.json"
    
    # Save to file
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    return filename

def get_emoji_for_item(item_type, item_name):
    """Get the appropriate emoji for an item"""
    # Try to find a direct emoji match for the item
    item_lower = item_name.lower()
    
    # Common emoji mappings
    emoji_map = {
        "apple": "🍎",
        "banana": "🍌",
        "orange": "🍊",
        "grapes": "🍇",
        "strawberry": "🍓",
        "watermelon": "🍉",
        "pineapple": "🍍",
        "mango": "🥭",
        "blueberries": "🫐",
        "peach": "🍑",
        "pear": "🍐",
        "kiwi": "🥝",
        "carrot": "🥕",
        "broccoli": "🥦",
        "tomato": "🍅",
        "cucumber": "🥒",
        "potato": "🥔",
        "corn": "🌽",
        "onion": "🧅",
        "milk": "🥛",
        "cheese": "🧀",
        "ice cream": "🍦",
        "bread": "🍞",
        "rice": "🍚",
        "pasta": "🍝",
        "pancake": "🥞",
        "waffle": "🧇",
        "chicken": "🍗",
        "eggs": "🥚",
        "fish": "🐟",
        "candy": "🍬",
        "chocolate": "🍫",
        "cake": "🎂",
        "cookies": "🍪",
        "donut": "🍩",
        "cupcake": "🧁",
        "water": "💧",
        "juice": "🧃",
        "soda": "🥤",
        "coffee": "☕",
        "popcorn": "🍿",
        "chips": "🍟",
    }
    
    # Return specific emoji if we have one
    if item_lower in emoji_map:
        return emoji_map[item_lower]
    
    # Otherwise use the category emoji
    if item_type in FOOD_CATEGORIES:
        return FOOD_CATEGORIES[item_type]["emoji"]
    elif item_type in ADVANCED_CATEGORIES:
        return ADVANCED_CATEGORIES[item_type]["emoji"]
    
    # Default emoji if all else fails
    return "🍽️"