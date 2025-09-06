import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Optional, Literal
import os

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

def get_api_key():
    """Get API key from Streamlit secrets or environment variables"""
    try:
        # First try Streamlit secrets (for cloud deployment)
        if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
            return st.secrets['GOOGLE_API_KEY']
        # Then try environment variables (for local development)
        elif os.getenv('GOOGLE_API_KEY'):
            return os.getenv('GOOGLE_API_KEY')
        else:
            return None
    except Exception as e:
        st.error(f"Error accessing API key: {e}")
        return None

@st.cache_resource
def initialize_model():
    """Initialize the ChatGoogleGenerativeAI model"""
    try:
        api_key = get_api_key()
        if not api_key:
            st.error("No API key found")
            return None
        
        # Initialize with explicit API key
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Updated model name
            temperature=0.7,  # Reduced temperature for more consistent results
            google_api_key=api_key
        )
        return model
    except Exception as e:
        st.error(f"Error initializing model: {e}")
        st.error("Please check your API key and internet connection.")
        return None

def analyze_review(model, review_text):
    """Analyze the review using the model"""
    try:
        with st.spinner("Processing with AI..."):
            result = model.with_structured_output(Review).invoke(review_text)
        
        # Ensure all required keys exist with defaults
        if isinstance(result, dict):
            processed_result = {
                'key_themes': result.get('key_themes', []),
                'summary': result.get('summary', 'No summary available'),
                'sentiment': result.get('sentiment', 'neutral'),
                'pros': result.get('pros', []),
                'cons': result.get('cons', [])
            }
            return processed_result
        else:
            st.error(f"Unexpected result format: {type(result)}")
            return None
            
    except Exception as e:
        st.error(f"Error analyzing review: {str(e)}")
        if "quota" in str(e).lower():
            st.error("API quota exceeded. Please check your Google AI usage limits.")
        elif "key" in str(e).lower():
            st.error("API key issue. Please verify your Google AI API key is valid.")
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
        api_key = get_api_key()
        if api_key:
            st.success("✅ Google API Key loaded")
        else:
            st.error("❌ Google API Key not found")
            st.info("For local development: Add GOOGLE_API_KEY to your .env file")
            st.info("For Streamlit Cloud: Add GOOGLE_API_KEY to your app secrets")
        
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
    if not api_key:
        st.warning("⚠️ Please configure your Google API key to use this app.")
        
        # Instructions for different platforms
        with st.expander(
