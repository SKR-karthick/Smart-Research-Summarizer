import streamlit as st
from typing import Dict, Any

def initialize_session_state():
    """Initialize session state variables."""
    session_vars = {
        'document_text': None,
        'document_name': None,
        'document_processed': False,
        'document_summary': None,
        'mode': None,
        'qa_history': [],
        'challenge_questions': None,
        'user_answers': [],
        'evaluations': []
    }
    
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value

def reset_session_state():
    """Reset all session state variables."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()

def get_session_state_summary() -> Dict[str, Any]:
    """Get a summary of current session state for debugging."""
    return {
        'document_processed': st.session_state.get('document_processed', False),
        'document_name': st.session_state.get('document_name', 'None'),
        'mode': st.session_state.get('mode', 'None'),
        'qa_history_count': len(st.session_state.get('qa_history', [])),
        'has_challenge_questions': st.session_state.get('challenge_questions') is not None
    }

def clean_text_for_display(text: str, max_length: int = 200) -> str:
    """
    Clean and truncate text for display purposes.
    
    Args:
        text: Input text
        max_length: Maximum length of output text
        
    Returns:
        Cleaned and truncated text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    cleaned = ' '.join(text.split())
    
    # Truncate if too long
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "..."
    
    return cleaned

def format_confidence_score(score: float) -> str:
    """Format confidence score for display."""
    if score >= 0.8:
        return f"🟢 High confidence ({score:.2f})"
    elif score >= 0.5:
        return f"🟡 Medium confidence ({score:.2f})"
    else:
        return f"🔴 Low confidence ({score:.2f})"

def validate_input(text: str, min_length: int = 5, max_length: int = 1000) -> bool:
    """
    Validate user input text.
    
    Args:
        text: Input text to validate
        min_length: Minimum required length
        max_length: Maximum allowed length
        
    Returns:
        True if valid, False otherwise
    """
    if not text or not text.strip():
        return False
    
    text_length = len(text.strip())
    return min_length <= text_length <= max_length

def extract_keywords(text: str, max_keywords: int = 5) -> list:
    """
    Extract key words from text for basic analysis.
    
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Simple keyword extraction
    words = text.lower().split()
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    
    # Filter and count words
    word_count = {}
    for word in words:
        word = word.strip('.,!?;:"()[]{}')
        if len(word) > 3 and word not in stop_words:
            word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]]
