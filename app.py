import streamlit as st
import random
import time
import json
import os
from datetime import datetime
import pandas as pd
import numpy as np
import requests
from io import BytesIO
import emoji
from game_utils import (
    init_session_state, 
    generate_items_for_level, 
    check_sorting, 
    get_feedback,
    save_session_data,
    get_emoji_for_item
)
from ui_utils import load_css, show_celebration, display_avatar
from hf_utils import get_bot_response

# Set page configuration
st.set_page_config(
    page_title="Shopping Sorter - Learn & Play!",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS for child-friendly visuals
load_css()

# Initialize session state variables
init_session_state()

# Main app structure
def main():
    
    st.markdown("<h1 class='game-title'>🛒 Shopping Sorter 🛒</h1>", unsafe_allow_html=True)

    
    # Show appropriate page based on session state
    if st.session_state.page == 'welcome':
        show_welcome_page()
    elif st.session_state.page == 'instructions':
        show_instructions_page()
    elif st.session_state.page == 'game':
        show_game_page()
    elif st.session_state.page == 'results':
        show_results_page()
    else:
        show_welcome_page()  # Default to welcome page

def show_welcome_page():
    st.markdown("<div class='welcome-container'>", unsafe_allow_html=True)
    
    # Animated shopping cart
    st.markdown("""
    <div class='welcome-animation'>
        <div class='cart-container'>
            <div class='cart'>🛒</div>
            <div class='items'>
                <span class='item'>🍎</span>
                <span class='item'>🥕</span>
                <span class='item'>🍌</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome section
    st.markdown("<div style='text-align: center;'><h2 class='welcome-text'>Welcome to Shopping Sorter!</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<p class='intro-text'>Let's learn about food groups while shopping!</p>", unsafe_allow_html=True)
        
        # Child name input
        st.markdown("<h3>What's your name?</h3>", unsafe_allow_html=True)
        name = st.text_input("", key="name_input", placeholder="Type your name here...", max_chars=15)
        
        # Age selection with emoji numbers
        st.markdown("<h3>How old are you?</h3>", unsafe_allow_html=True)
        age_options = ["3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
        age = st.selectbox("", age_options, index=2)
        
        # Start button
        if st.button("Let's Go Shopping! 🚀", key="start_button"):
            if name:
                st.session_state.child_name = name
                st.session_state.child_age = ["3", "4", "5", "6", "7"][age_options.index(age)]
                st.session_state.page = 'instructions'
                st.experimental_rerun()
            else:
                st.warning("Please tell us your name first!")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_instructions_page():
    st.markdown(f"<h1 class='greeting'>Hello, {st.session_state.child_name}! 👋</h1>", unsafe_allow_html=True)
    
    # Create two columns: left for image, right for example
    left_col, right_col = st.columns([1, 1])

    # Left column: image
    with left_col:
        st.image("instructions.png", width=500)

    with right_col:
        st.markdown("<h3>For example:</h3>", unsafe_allow_html=True)

        # 🧺 Example 1
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown("<div class='example-item'>🍎</div>", unsafe_allow_html=True)
            st.markdown("<p class='example-label'>Apple</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='example-arrow'>➡️</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='example-basket'>🧺</div>", unsafe_allow_html=True)
            st.markdown("<p class='example-label'>Fruits Basket</p>", unsafe_allow_html=True)

        # 🥦 Example 2
        col4, col5, col6 = st.columns([1, 1, 1])
        with col4:
            st.markdown("<div class='example-item'>🥦</div>", unsafe_allow_html=True)
            st.markdown("<p class='example-label'>Broccoli</p>", unsafe_allow_html=True)
        with col5:
            st.markdown("<div class='example-arrow'>➡️</div>", unsafe_allow_html=True)
        with col6:
            st.markdown("<div class='example-basket'>🥗</div>", unsafe_allow_html=True)
            st.markdown("<p class='example-label'>Veggies Basket</p>", unsafe_allow_html=True)

        # 🥛 Example 3
        col7, col8, col9 = st.columns([1, 1, 1])
        with col7:
            st.markdown("<div class='example-item'> 🧀 </div>", unsafe_allow_html=True)
            st.markdown("<p class='example-label'>Cheese</p>", unsafe_allow_html=True)
        with col8:
            st.markdown("<div class='example-arrow'>➡️</div>", unsafe_allow_html=True)
        with col9:
            st.markdown("<div class='example-basket'>🥛</div>", unsafe_allow_html=True)
            st.markdown("<p class='example-label'>Dairy Basket</p>", unsafe_allow_html=True)

        # Create 3 columns and put the button in the center one
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("##")  # Adds a bit of vertical space
            st.markdown("##")  # Adds a bit of vertical space
            st.markdown("##")  # Adds a bit of vertical space


            if st.button("🛒 Start Shopping!", key="start_game_button"):
                items, baskets = generate_items_for_level(
                    st.session_state.current_level,
                    int(st.session_state.child_age)
                )
                st.session_state.current_items = items
                st.session_state.current_baskets = baskets
                st.session_state.page = 'game'
                st.experimental_rerun()



def show_game_page():
    # Display game header with score and level
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown(f"<div class='score-display'>Stars: {st.session_state.score} ⭐</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: center;'><h2>Level {st.session_state.current_level}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='score-display'>Items: {len(st.session_state.current_items)}</div>", unsafe_allow_html=True)
    
    # Display feedback if any
    if st.session_state.feedback:
        st.markdown(f"<div class='feedback feedback-{st.session_state.feedback_type}'>{st.session_state.feedback}</div>", 
                   unsafe_allow_html=True)
    
    # Check if we need new items for this level
    if not st.session_state.current_items:
        items, baskets = generate_items_for_level(st.session_state.current_level, 
                                                  int(st.session_state.child_age))
        st.session_state.current_items = items
        st.session_state.current_baskets = baskets
    
    # Game container
    st.markdown("<div class='game-container'>", unsafe_allow_html=True)
    
    # Display store items
    st.markdown("<div class='store-section'>", unsafe_allow_html=True)
    st.markdown("<h3>Pick an item from the store:</h3>", unsafe_allow_html=True)
    
    # Display items in rows of 4
    items_per_row = 4
    for i in range(0, len(st.session_state.current_items), items_per_row):
        cols = st.columns(items_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(st.session_state.current_items):
                item = st.session_state.current_items[idx]
                with col:
                    #st.markdown(f"<div class='item-card' id='{item['id']}'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='item-emoji'>{get_emoji_for_item(item['type'], item['name'])}</div>", 
                               unsafe_allow_html=True)
                    st.markdown(f"<div class='item-name'>{item['name']}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    if st.button(f"Pick", key=f"item_{idx}"):
                        st.session_state.selected_item = item
                        st.experimental_rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display baskets for sorting
    st.markdown("<div class='baskets-section'>", unsafe_allow_html=True)
    st.markdown("<h3>Put it in the right basket:</h3>", unsafe_allow_html=True)
    
    basket_cols = st.columns(len(st.session_state.current_baskets))
    
    # If an item is selected, enable sorting
    if st.session_state.selected_item:
        selected_item = st.session_state.selected_item
        
        # Show selected item above baskets
        st.markdown(f"""
        <div class='selected-item-container'>
            <div class='selected-item-emoji'>{get_emoji_for_item(selected_item['type'], selected_item['name'])}</div>
            <div class='selected-item-prompt'>Where does the {selected_item['name']} go?</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display baskets
        for i, basket_col in enumerate(basket_cols):
            if i < len(st.session_state.current_baskets):
                basket = st.session_state.current_baskets[i]
                with basket_col:
                    #st.markdown(f"<div class='basket' id='{basket['id']}'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='basket-emoji'>{basket['emoji']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='basket-label'>{basket['label']}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    if st.button(f"Place Here", key=f"basket_{i}"):
                        # Process the sorting
                        is_correct = check_sorting(selected_item, basket)
                        st.session_state.total_attempts += 1
                        
                        # Update game history
                        game_event = {
                            "level": st.session_state.current_level,
                            "item": {"type": selected_item["type"], "name": selected_item["name"]},
                            "basket": basket["label"],
                            "is_correct": is_correct,
                            "timestamp": time.time()
                        }
                        st.session_state.game_history.append(game_event)
                        
                        if is_correct:
                            # Remove the item from current items
                            st.session_state.current_items = [s for s in st.session_state.current_items 
                                                           if s["id"] != selected_item["id"]]
                            st.session_state.score += max(1, st.session_state.current_level)
                            
                            # Generate feedback from bot
                            try:
                                bot_feedback = get_bot_response(
                                    f"Give a very short, fun, child-friendly positive feedback (max 10 words) for correctly sorting {selected_item['name']} into {basket['label']}. Make it enthusiastic. Include an emoji."
                                )
                                feedback = bot_feedback if bot_feedback else f"Great job! {selected_item['name']} goes in {basket['label']}! 🎉"
                            except:
                                feedback = f"Great job! {selected_item['name']} goes in {basket['label']}! 🎉"
                                
                            st.session_state.feedback = feedback
                            st.session_state.feedback_type = "positive"
                            
                            # Check if level is complete
                            if not st.session_state.current_items:
                                show_celebration()
                                st.session_state.current_level += 1
                                new_items, new_baskets = generate_items_for_level(
                                    st.session_state.current_level, 
                                    int(st.session_state.child_age)
                                )
                                st.session_state.current_items = new_items
                                st.session_state.current_baskets = new_baskets
                                st.session_state.feedback = f"Level {st.session_state.current_level-1} Complete! Moving to Level {st.session_state.current_level}! 🎉"
                                st.session_state.feedback_type = "positive"
                            
                            st.session_state.selected_item = None
                            st.experimental_rerun()
                        else:
                            # Wrong answer
                            try:
                                bot_feedback = get_bot_response(
                                    f"Give a short, gentle, encouraging feedback (max 10 words) for a young child incorrectly sorting {selected_item['name']} into {basket['label']}. Make it child-friendly. Include an emoji."
                                )
                                feedback = bot_feedback if bot_feedback else f"Not quite! Try another basket for {selected_item['name']}. 🤔"
                            except:
                                feedback = f"Not quite! Try another basket for {selected_item['name']}. 🤔"
                                
                            st.session_state.feedback = feedback
                            st.session_state.feedback_type = "negative"
                            st.experimental_rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add learning tip if available
    if st.session_state.selected_item:
        item = st.session_state.selected_item
        try:
            learning_tip = get_bot_response(
                f"Give a simple, fun fact about {item['name']} that a {st.session_state.child_age} year old child would find interesting. Keep it to one short, simple sentence. Include an emoji."
            )
            if learning_tip:
                st.markdown(f"<div class='learning-tip'>{learning_tip}</div>", unsafe_allow_html=True)
        except:
            pass
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add end game button
    if st.button("Finish Shopping", key="finish_button"):
        save_session_data()
        st.session_state.page = 'results'
        st.experimental_rerun()

def show_results_page():
    st.markdown(f"<h1 class='results-title'>Great Shopping, {st.session_state.child_name}! 🎉</h1>", unsafe_allow_html=True)
    
    # Shopping results animation
    st.markdown("""
    <div class='results-animation'>
        <div class='cart-full'>
            🛒
            <div class='cart-items'>
                <span>🍎</span>
                <span>🥕</span>
                <span>🥛</span>
                <span>🍌</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"<div class='final-score'>You earned {st.session_state.score} stars! ⭐</div>", unsafe_allow_html=True)
        
        # Calculate performance metrics
        correct_answers = sum(1 for event in st.session_state.game_history if event["is_correct"])
        accuracy = correct_answers / max(1, st.session_state.total_attempts) * 100
        
        st.markdown(f"""
        <div class='achievements-card'>
            <h3>Your Shopping Trip:</h3>
            <ul>
                <li>Reached Level: {st.session_state.current_level}</li>
                <li>Items Sorted: {st.session_state.total_attempts}</li>
                <li>Correct Sorts: {correct_answers}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Display badges based on performance
        badges = []
        
        if st.session_state.current_level >= 3:
            badges.append({
                "name": "Super Shopper", 
                "emoji": "🛒", 
                "description": "Completed multiple shopping levels!"
            })
        
        if accuracy >= 80:
            badges.append({
                "name": "Sorting Star", 
                "emoji": "⭐", 
                "description": "Great at sorting items!"
            })
            
        if st.session_state.score >= 15:
            badges.append({
                "name": "Food Expert", 
                "emoji": "🍽️", 
                "description": "Knows where foods belong!"
            })
        
        if not badges:
            badges.append({
                "name": "Shopping Helper", 
                "emoji": "🛍️", 
                "description": "Learning to sort foods!"
            })
        
        st.markdown("<h3>Your Badges:</h3>", unsafe_allow_html=True)
        for badge in badges:
            st.markdown(f"""
            <div class='badge'>
                <div class='badge-emoji'>{badge["emoji"]}</div>
                <div class='badge-info'>
                    <div class='badge-name'>{badge["name"]}</div>
                    <div class='badge-description'>{badge["description"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Get learning summary from Hugging Face model
    try:
        # Count the most common categories the child interacted with
        categories = {}
        for event in st.session_state.game_history:
            if event["basket"] not in categories:
                categories[event["basket"]] = 1
            else:
                categories[event["basket"]] += 1
        
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:2]
        top_categories_str = ", ".join([cat[0] for cat in top_categories])
        
        learning_summary = get_bot_response(
            f"Give a very short, encouraging summary (2-3 sentences) for a {st.session_state.child_age} year old child named {st.session_state.child_name} who has been learning about food groups. They worked especially with {top_categories_str}. Be positive and encouraging about their learning journey. Make it very child-friendly."
        )
        
        if learning_summary:
            st.markdown(f"<div class='learning-summary'>{learning_summary}</div>", unsafe_allow_html=True)
    except:
        pass
    
    # Play again or exit options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Shop Again 🔄", key="play_again_button"):
            # Reset game state but keep name and age
            st.session_state.score = 0
            st.session_state.total_attempts = 0
            st.session_state.current_level = 1
            st.session_state.current_items = []
            st.session_state.current_baskets = []
            st.session_state.feedback = ''
            st.session_state.game_history = []
            st.session_state.page = 'instructions'
            st.experimental_rerun()
    
    with col2:
        if st.button("New Shopper 👋", key="new_player_button"):
            # Complete reset
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'welcome'
            st.experimental_rerun()
    
    # Display progress graph
    if len(st.session_state.game_history) > 5:
        st.markdown("<h3>Your Shopping Progress:</h3>", unsafe_allow_html=True)
        
        # Convert game history to DataFrame
        df = pd.DataFrame(st.session_state.game_history)
        df['timestamp_str'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%H:%M:%S')
        
        # Calculate cumulative correct answers
        correct_df = df[df['is_correct']].copy()
        if not correct_df.empty:
            correct_df['cumulative_correct'] = range(1, len(correct_df) + 1)
            
            # Simple progress chart
            chart_data = correct_df[['timestamp_str', 'cumulative_correct']]
            st.line_chart(chart_data.set_index('timestamp_str'))

# Run the main app
if __name__ == "__main__":
    main()
