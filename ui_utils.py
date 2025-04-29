import streamlit as st
import random

def load_css():
    """Load custom CSS styles for the app"""
    st.markdown("""
    <style>
        /* Global Styles */
        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: #333;
            background-color: #f9f7f2;
        }
        
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Header Styles */
        .game-title {
            color: #FF6B6B;
            text-align: center;
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Welcome Page Styles */
        .welcome-container {
            text-align: center;
            padding: 20px;
            background-color: #fff;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .welcome-text {
            color: #4CAF50;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .intro-text {
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        .welcome-animation {
            height: 150px;
            position: relative;
            margin-bottom: 20px;
            overflow: hidden;
        }
        
        .cart-container {
            position: relative;
            animation: moveCart 8s infinite linear;
        }
        
        .cart {
            font-size: 4rem;
            position: absolute;
        }
        
        .items {
            position: absolute;
            top: -10px;
            left: 10px;
        }
        
        .item {
            font-size: 2rem;
            margin-right: 5px;
            animation: bounce 1s infinite alternate;
        }
        
        @keyframes moveCart {
            0% { transform: translateX(-100px); }
            50% { transform: translateX(calc(100% - 100px)); }
            100% { transform: translateX(-100px); }
        }
        
        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-10px); }
        }
        
        /* Instructions Page Styles */
        .greeting {
            color: #4CAF50;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .instructions-container {
            background-color: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        
        .instruction-step {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 10px;
        }
        
        .step-number {
            font-size: 2rem;
            margin-right: 15px;
            color: #FF6B6B;
        }
        
        .step-text {
            font-size: 1.2rem;
            flex-grow: 1;
        }
        
        .step-emoji {
            font-size: 2rem;
            margin-left: 15px;
        }
        
        .example-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .example-item, .example-basket {
            font-size: 3rem;
            margin: 10px;
        }
        
        .example-arrow {
            font-size: 2rem;
            margin: 10px;
        }
        
        .example-label {
            font-size: 1.2rem;
        }
        
        /* Game Page Styles */
        .score-display {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4CAF50;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .feedback {
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
        }
        
        .feedback-positive {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .feedback-negative {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .game-container {
            background-color: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .store-section, .baskets-section {
            margin-bottom: 20px;
        }
        
        .item-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.2s;
        }
        
        .item-card:hover {
            transform: scale(1.05);
        }
        
        .item-emoji {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        .item-name {
            font-size: 1.1rem;
            font-weight: bold;
        }
        
        .basket {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.2s;
        }
        
        .basket:hover {
            transform: scale(1.05);
        }
        
        .basket-emoji {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        .basket-label {
            font-size: 1.1rem;
            font-weight: bold;
        }
        
        .selected-item-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f5e9;
            border-radius: 10px;
        }
        
        .selected-item-emoji {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        .selected-item-prompt {
            font-size: 1.3rem;
            font-weight: bold;
            color: #4CAF50;
        }
        
        .learning-tip {
            background-color: #e0f7fa;
            color: #01579b;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.1rem;
            text-align: center;
            border-left: 5px solid #4fc3f7;
        }
        
        /* Results Page Styles */
        .results-title {
            color: #4CAF50;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .results-animation {
            height: 150px;
            position: relative;
            margin: 30px 0;
            text-align: center;
        }
        
        .cart-full {
            font-size: 4rem;
            position: relative;
            display: inline-block;
            animation: cartBounce 2s infinite alternate;
        }
        
        .cart-items {
            position: absolute;
            top: -20px;
            left: 10px;
            display: flex;
        }
        
        .cart-items span {
            font-size: 1.5rem;
            margin-right: 5px;
            animation: itemFloat 3s infinite alternate;
            animation-delay: calc(var(--i) * 0.5s);
        }
        
        @keyframes cartBounce {
            from { transform: translateY(0); }
            to { transform: translateY(-10px); }
        }
        
        @keyframes itemFloat {
            from { transform: translateY(0) rotate(0deg); }
            to { transform: translateY(-15px) rotate(10deg); }
        }
        
        .final-score {
            font-size: 2rem;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .achievements-card {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .achievements-card h3 {
            color: #FF6B6B;
            margin-bottom: 15px;
        }
        
        .achievements-card ul {
            list-style-type: none;
            padding-left: 10px;
        }
        
        .achievements-card li {
            margin: 10px 0;
            font-size: 1.1rem;
        }
        
        .badge {
            display: flex;
            align-items: center;
            background-color: #fff;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 15px 0;
        }
        
        .badge-emoji {
            font-size: 2.5rem;
            margin-right: 15px;
        }
        
        .badge-info {
            flex-grow: 1;
        }
        
        .badge-name {
            font-size: 1.2rem;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 5px;
        }
        
        .badge-description {
            font-size: 1rem;
            color: #666;
        }
        
        .learning-summary {
            background-color: #fff3e0;
            color: #e65100;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.2rem;
            text-align: center;
            border-left: 5px solid #ff9800;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        
        /* Avatar display */
        .avatar-container {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #4CAF50;
            background-color: #e8f5e9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

def show_celebration():
    """Display a celebration animation"""
    # Use JavaScript to show confetti animation
    st.markdown("""
    <script>
        // Confetti animation script would go here
        // Using placeholder comment as actual JS execution is limited in Streamlit
        console.log("Celebration animation triggered");
    </script>
    
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #4CAF50; animation: pulse 1s infinite;">🎉 Level Complete! 🎉</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio playback not supported in this example but would be ideal
    # Alternative: Use emojis and styling for visual celebration
    st.balloons()

def display_avatar():
    """Display a random cartoon avatar for the child"""
    # List of fun emoji avatars
    avatars = ["🐱", "🐶", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸"]
    
    # Select a random avatar if not already selected
    if 'avatar' not in st.session_state:
        st.session_state.avatar = random.choice(avatars)
    
    # Display the avatar
    st.markdown(f"""
    <div class="avatar-container">
        {st.session_state.avatar}
    </div>
    """, unsafe_allow_html=True)