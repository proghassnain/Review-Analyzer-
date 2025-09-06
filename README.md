# 📝 Review Analyzer

A powerful AI-driven web application that analyzes product reviews using Google's Gemini AI to extract key insights, sentiment, pros, and cons automatically.

## 🚀 Features

- **Smart Review Analysis**: Automatically extracts key themes, sentiment, pros, and cons from any product review
- **Interactive Web Interface**: Clean, modern Streamlit UI with real-time analysis
- **Sentiment Detection**: Color-coded sentiment analysis (Positive, Negative, Neutral)
- **Key Themes Extraction**: Identifies main topics discussed in the review
- **Pros & Cons Identification**: Automatically separates positive and negative aspects
- **Export Results**: Download analysis results as text files
- **Example Reviews**: Pre-loaded examples for quick testing
- **Error Handling**: Robust error handling with user-friendly messages

## 🛠️ Technology Stack

- **AI Model**: Google Gemini 2.0 Flash
- **Framework**: Streamlit
- **AI Integration**: LangChain Google GenAI
- **Language**: Python 3.8+
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

Before running the application, ensure you have:

1. Python 3.8 or higher installed
2. A Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))
3. Required Python packages (see installation section)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd review-analyzer
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Packages
```bash
pip install streamlit langchain-google-genai python-dotenv
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

**⚠️ Important**: Never commit your `.env` file to version control. Add it to your `.gitignore` file.

## 🚀 Running the Application

### Command Line Method
```bash
streamlit run app.py
```

### Alternative Method
```bash
python -m streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Basic Usage

1. **Start the Application**: Run the command above to launch the web interface
2. **Check API Status**: The sidebar will show if your Google API key is properly configured
3. **Enter Review**: Paste any product review in the text area
4. **Analyze**: Click the "🔍 Analyze Review" button
5. **View Results**: See the structured analysis with sentiment, themes, pros, and cons
6. **Download**: Optionally download the results as a text file

### Using Example Reviews

The sidebar includes pre-loaded example reviews for quick testing:
- Samsung Galaxy S24 Ultra (Mixed sentiment)
- MacBook Air M2 (Positive sentiment)
- Restaurant Review (Negative sentiment)

Simply select an example and click "Load Example" to populate the text area.

### Understanding the Results

- **🎭 Sentiment Analysis**: Color-coded overall sentiment with emoji indicators
- **📋 Summary**: AI-generated summary of the review
- **🏷️ Key Themes**: Main topics and themes identified in the review
- **✅ Pros**: Positive aspects mentioned in the review
- **❌ Cons**: Negative aspects or criticisms found in the review

## 🎨 Features in Detail

### Sentiment Analysis
- **Positive**: Green background with 😊 emoji
- **Negative**: Red background with 😞 emoji  
- **Neutral**: Yellow background with 😐 emoji

### Theme Extraction
Key themes are displayed in organized cards with black text for optimal readability.

### Export Functionality
Download complete analysis results in a formatted text file for offline reference or reporting.

## 🔍 Troubleshooting

### Common Issues

1. **"Google API Key not found" Error**
   - Ensure your `.env` file exists in the pro
