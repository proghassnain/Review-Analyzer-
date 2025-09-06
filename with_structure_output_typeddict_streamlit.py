import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Review Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sentiment-positive {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# Schema for the structured output
class Review(TypedDict):
    key_themes: Annotated[list[str], "A few key themes discussed in the review, in a list"]
    summary: str
    sentiment: Annotated[Literal["positive", "negative", "neutral"], "Return 'positive', 'negative', or 'neutral' based on the overall sentiment of the review."]
    pros: Annotated[Optional[list[str]], "A list of pros mentioned in the review"]
    cons: Annotated[Optional[list[str]], "A list of cons mentioned in the review"]

@st.cache_resource
def initialize_model():
    """Initialize the ChatGoogleGenerativeAI model"""
    try:
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1.5)
    except Exception as e:
        st.error(f"Error initializing model: {e}")
        return None

def analyze_review(model, review_text):
    """Analyze the review using the model"""
    try:
        result = model.with_structured_output(Review).invoke(review_text)
        return result
    except Exception as e:
        st.error(f"Error analyzing review: {e}")
        return None

def display_sentiment(sentiment):
    """Display sentiment with appropriate styling"""
    sentiment_classes = {
        "positive": "sentiment-positive",
        "negative": "sentiment-negative",
        "neutral": "sentiment-neutral"
    }
    
    sentiment_icons = {
        "positive": "😊",
        "negative": "😞",
        "neutral": "😐"
    }
    
    st.markdown(f"""
    <div class="{sentiment_classes.get(sentiment, 'sentiment-neutral')}">
        <strong>{sentiment_icons.get(sentiment, "😐")} Sentiment: {sentiment.title()}</strong>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📝 Review Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Check if API key is available
        api_key_available = bool(os.getenv("GOOGLE_API_KEY"))
        if api_key_available:
            st.success("✅ Google API Key loaded")
        else:
            st.error("❌ Google API Key not found")
            st.info("Please add your GOOGLE_API_KEY to your .env file")
        
        st.markdown("---")
        st.markdown("### About")
        st.info("This app analyzes product reviews using Google's Gemini AI to extract key themes, sentiment, pros, and cons.")
        
        st.markdown("### Example Reviews")
        example_reviews = {
            "Samsung Galaxy S24 Ultra": """I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast-whether I'm gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.
The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera-the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.
However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with bloatware-why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.""",
            
            "MacBook Air M2": """Just got the new MacBook Air with M2 chip and I'm blown away by the performance! The battery life is incredible - I can work for 10+ hours without charging. The new design is sleek and the display is gorgeous with excellent color accuracy.
However, it does get quite warm during intensive tasks and the webcam could be better. Also, the limited ports are still an issue. Overall, great laptop for the price point.""",
            
            "Restaurant Review": """Visited this restaurant last weekend and had a terrible experience. The service was incredibly slow - we waited 45 minutes just to order. When the food finally arrived, it was cold and bland. The prices are way too high for the quality you get. The only positive was the nice ambiance, but that doesn't make up for everything else. Won't be coming back."""
        }
        
        selected_example = st.selectbox("Choose an example:", [""] + list(example_reviews.keys()))
        if selected_example and st.button("Load Example"):
            st.session_state.review_text = example_reviews[selected_example]
    
    # Main content
    if not api_key_available:
        st.warning("⚠️ Please configure your Google API key in the .env file to use this app.")
        st.stop()
    
    # Initialize model
    model = initialize_model()
    if not model:
        st.error("❌ Failed to initialize the model. Please check your API key and internet connection.")
        st.stop()
    
    # Input section
    st.subheader("📝 Enter Your Review")
    
    # Get review text from session state if available
    default_text = st.session_state.get('review_text', '')
    
    review_text = st.text_area(
        "Paste your product review here:",
        value=default_text,
        height=200,
        placeholder="Enter a detailed product review to analyze its sentiment, themes, pros, and cons..."
    )
    
    # Update session state
    st.session_state.review_text = review_text
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Review", type="primary", use_container_width=True)
    
    if analyze_button and review_text.strip():
        with st.spinner("🤖 Analyzing your review..."):
            result = analyze_review(model, review_text)
        
        if result:
            st.success("✅ Analysis completed!")
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            # Sentiment - with safe access
            st.markdown("### 🎭 Sentiment Analysis")
            sentiment = result.get('sentiment', 'neutral')
            display_sentiment(sentiment)
            
            # Summary - with safe access
            st.markdown("### 📋 Summary")
            summary = result.get('summary', 'No summary available')
            st.info(summary)
            
            # Key Themes - with safe access
            key_themes = result.get('key_themes', [])
            if key_themes:
                st.markdown("### 🏷️ Key Themes")
                themes_cols = st.columns(min(len(key_themes), 4))
                for i, theme in enumerate(key_themes):
                    with themes_cols[i % 4]:
                        st.markdown(f"<div class='metric-card'>🏷️ {theme}</div>", unsafe_allow_html=True)
            
            # Pros and Cons - with safe access
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Pros")
                pros = result.get('pros', [])
                if pros:
                    for pro in pros:
                        st.markdown(f"• {pro}")
                else:
                    st.markdown("*No specific pros identified*")
            
            with col2:
                st.markdown("### ❌ Cons")
                cons = result.get('cons', [])
                if cons:
                    for con in cons:
                        st.markdown(f"• {con}")
                else:
                    st.markdown("*No specific cons identified*")
            
            # Download results
            st.markdown("---")
            results_text = f"""
Review Analysis Results
=====================

Sentiment: {sentiment.title()}

Summary:
{summary}

Key Themes:
{', '.join(key_themes)}

Pros:
{chr(10).join(['• ' + pro for pro in pros]) if pros else 'None identified'}

Cons:
{chr(10).join(['• ' + con for con in cons]) if cons else 'None identified'}
            """
            
            st.download_button(
                label="📥 Download Results",
                data=results_text,
                file_name="review_analysis.txt",
                mime="text/plain"
            )
    
    elif analyze_button:
        st.warning("⚠️ Please enter a review to analyze.")

if __name__ == "__main__":
    main()