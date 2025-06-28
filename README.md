# Smart Research Assistant

A Streamlit-based application that helps users analyze and interact with documents through AI-powered features.

## Features

- **Document Upload**: Support for PDF and TXT files
- **Auto Summary**: Generates concise summaries (≤150 words) 
- **Ask Anything Mode**: Free-form question answering based on document content
- **Challenge Me Mode**: Auto-generated comprehension questions with evaluation
- **Grounded Responses**: All answers include justifications from the source document

## 🚀 Quick Deployment to Streamlit Cloud

1. **Fork/Clone** this repository to your GitHub account
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Sign in** with your GitHub account
4. **Click "New app"**
5. **Select** your repository and set:
   - **Main file path**: `app.py`
   - **Python version**: 3.8+
6. **Click "Deploy"**

Your app will be live in minutes at `https://your-app-name.streamlit.app`

## Setup Instructions

### Prerequisites
- Python 3.8 or later
- Streamlit
- PyPDF2

### Local Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd ResearchSummarizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

**For Windows users:**
Double-click `run_app.bat` or run in command prompt:
```bash
streamlit run app.py --server.port 8501
```

**For Mac/Linux users:**
Run in terminal:
```bash
chmod +x run_app.sh
./run_app.sh
```

Or directly:
```bash
streamlit run app.py --server.port 8501
```

4. Open your browser and go to `http://localhost:8501`

### Important Note
If you see "This site can't be reached" error, make sure you're accessing the correct URL that appears in your terminal after running the command. It's usually `http://localhost:8501`, not port 5000.

## Project Structure

```
smart-research-assistant/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document text extraction
├── ai_assistant.py       # Text processing and analysis
├── utils.py              # Utility functions
├── sample_document.txt   # Sample document for testing
└── README.md            # This file
```

## How to Use

### 1. Upload Document
- Use the sidebar to upload a PDF or TXT file
- Click "Process Document" to analyze the content
- View the auto-generated summary

### 2. Ask Anything Mode
- Enter any question about your document
- Get answers based on the document content
- View justifications for each answer

### 3. Challenge Me Mode
- Click "Generate Questions" to create comprehension questions
- Answer the questions in the text areas
- Click "Evaluate Answer" to get feedback
- All evaluations include justifications from the document

## Architecture

### Simple Text Processing
The application uses lightweight text processing instead of heavy AI models:
- **Summarization**: Extractive approach using keyword detection
- **Question Answering**: Keyword matching and context retrieval
- **Question Generation**: Template-based with document adaptation
- **Answer Evaluation**: Keyword overlap analysis

### Key Components

1. **DocumentProcessor**: Handles PDF and TXT file text extraction
2. **AIAssistant**: Manages text analysis and processing features
3. **Utils**: Session state management and helper functions
4. **App**: Main Streamlit interface and user interaction

## Technical Details

- **Framework**: Streamlit for web interface
- **Language**: Python
- **Text Processing**: Regex and string manipulation
- **PDF Support**: Basic text extraction without external dependencies
- **Session Management**: Streamlit session state

## Limitations

- PDF extraction works best with simple, text-based PDFs
- Complex or scanned PDFs may not extract properly
- For best results, use TXT files or simple PDF documents

## Sample Usage

1. Upload the included `sample_document.txt`
2. Try asking: "What is AI used for in healthcare?"
3. Test the Challenge Me mode with generated questions
4. All responses will reference the source document

## Contributing

This is a simplified implementation designed for educational purposes and basic document analysis tasks.
