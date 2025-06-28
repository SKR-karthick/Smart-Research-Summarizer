import streamlit as st
from typing import List, Dict, Tuple, Optional
import re
import random

class AIAssistant:
    """Simple text-based assistant for document analysis and interaction."""
    
    def __init__(self):
        """Initialize the assistant."""
        pass
    
    def generate_summary(self, text: str) -> str:
        """
        Generate a concise summary of the document using simple text processing.
        
        Args:
            text: Document text
            
        Returns:
            Summary text (≤150 words)
        """
        try:
            # Simple extractive summarization
            sentences = text.split('. ')
            if len(sentences) < 3:
                return text[:150] + "..." if len(text) > 150 else text
            
            # Take first few sentences and key sentences with important keywords
            important_keywords = ['conclusion', 'result', 'finding', 'important', 'main', 'key', 'summary']
            
            summary_sentences = []
            # Add first 2 sentences
            summary_sentences.extend(sentences[:2])
            
            # Add sentences with important keywords
            for sentence in sentences[2:]:
                if any(keyword in sentence.lower() for keyword in important_keywords):
                    summary_sentences.append(sentence)
                    if len(summary_sentences) >= 5:
                        break
            
            summary = '. '.join(summary_sentences)
            
            # Ensure it's under 150 words
            words = summary.split()
            if len(words) > 150:
                summary = ' '.join(words[:150]) + "..."
            
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def answer_question(self, context: str, question: str) -> Tuple[str, str]:
        """
        Answer a question based on the document context using simple text matching.
        
        Args:
            context: Document text
            question: User's question
            
        Returns:
            Tuple of (answer, justification)
        """
        try:
            # Simple keyword-based question answering
            question_lower = question.lower()
            context_lower = context.lower()
            
            # Extract key question words
            question_words = [word.strip('?.,!') for word in question_lower.split() 
                            if len(word) > 3 and word not in ['what', 'where', 'when', 'why', 'how', 'which', 'who']]
            
            # Find relevant sentences
            sentences = context.split('. ')
            relevant_sentences = []
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                # Score sentence based on keyword matches
                score = sum(1 for word in question_words if word in sentence_lower)
                if score > 0:
                    relevant_sentences.append((sentence, score))
            
            # Sort by relevance and get best matches
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            
            if relevant_sentences:
                # Take the most relevant sentences
                answer_sentences = [sent[0] for sent in relevant_sentences[:2]]
                answer = '. '.join(answer_sentences)
                
                # Create justification
                justification = f"This answer is based on relevant sentences from the document that contain keywords: {', '.join(question_words[:3])}. Supporting text: '{answer_sentences[0][:100]}...'"
            else:
                # Fallback: return first few sentences mentioning any question word
                answer = "I couldn't find a specific answer to your question in the document."
                justification = "No relevant content found in the document for the given question."
            
            # Store in session state for history
            if 'qa_history' not in st.session_state:
                st.session_state.qa_history = []
            
            st.session_state.qa_history.append({
                'question': question,
                'answer': answer,
                'justification': justification
            })
            
            return answer, justification
        except Exception as e:
            return f"Error answering question: {str(e)}", "Could not process the question."
    
    def generate_questions(self, text: str) -> List[str]:
        """
        Generate comprehension questions based on the document using simple text analysis.
        
        Args:
            text: Document text
            
        Returns:
            List of generated questions
        """
        try:
            # Extract key information from text
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
            
            # Find important concepts and entities
            important_words = self._extract_key_concepts(text)
            
            # Generate different types of questions
            questions = []
            
            # 1. Main topic question
            if sentences:
                questions.append("What is the main topic or central theme discussed in this document?")
            
            # 2. Detail-based question
            if len(important_words) > 0:
                key_concept = important_words[0]
                questions.append(f"What information is provided about {key_concept} in the document?")
            
            # 3. Analysis question
            if len(sentences) > 3:
                questions.append("What are the key findings or conclusions presented in this document?")
            
            return questions
        except Exception as e:
            # Return template questions as fallback
            return self._generate_template_questions(text)
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from the text."""
        # Simple approach: find frequently mentioned meaningful words
        words = text.lower().split()
        word_freq = {}
        
        # Count meaningful words (length > 4, not common words)
        stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'said', 'each', 'which', 'their', 'time', 'than', 'many', 'some', 'very', 'what', 'know', 'just', 'first', 'into', 'over', 'think', 'also', 'back', 'after', 'work', 'life', 'only', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'}
        
        for word in words:
            word = re.sub(r'[^a-zA-Z]', '', word)
            if len(word) > 4 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top 3 most frequent meaningful words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:3] if freq > 1]
    
    def _clean_generated_question(self, question: str) -> str:
        """Clean and format generated questions."""
        # Remove common prefixes
        question = re.sub(r'^(question:|q:|generate|create|make)', '', question, flags=re.IGNORECASE)
        question = question.strip()
        
        # Ensure it ends with a question mark
        if not question.endswith('?'):
            question += '?'
        
        # Capitalize first letter
        if question:
            question = question[0].upper() + question[1:]
        
        return question
    
    def _generate_template_questions(self, text: str) -> List[str]:
        """Generate template questions as fallback."""
        # Extract key information
        sentences = text.split('.')[:10]  # First 10 sentences
        
        questions = [
            "What is the main topic or theme discussed in this document?",
            "What are the key points or arguments presented in the text?",
            "What conclusions or recommendations are made in the document?"
        ]
        
        return questions
    
    def _generate_template_question(self, text: str, index: int) -> str:
        """Generate a single template question."""
        templates = [
            "What is the main topic discussed in this document?",
            "What are the key findings or conclusions presented?",
            "What evidence or examples are provided to support the arguments?"
        ]
        
        return templates[index % len(templates)]
    
    def evaluate_answer(self, context: str, question: str, user_answer: str) -> Dict:
        """
        Evaluate user's answer to a generated question using simple text analysis.
        
        Args:
            context: Document text
            question: The question asked
            user_answer: User's response
            
        Returns:
            Dictionary with evaluation results
        """
        try:
            # Find relevant content in context for the question
            question_lower = question.lower()
            context_lower = context.lower()
            user_answer_lower = user_answer.lower().strip()
            
            # Extract key terms from question
            question_keywords = [word.strip('?.,!') for word in question_lower.split() 
                               if len(word) > 3 and word not in ['what', 'where', 'when', 'why', 'how', 'which', 'who', 'are', 'the', 'and', 'this', 'that']]
            
            # Find sentences in context that relate to the question
            sentences = context.split('. ')
            relevant_sentences = []
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                score = sum(1 for word in question_keywords if word in sentence_lower)
                if score > 0:
                    relevant_sentences.append((sentence, score))
            
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            
            # Extract expected answer content from most relevant sentences
            expected_content = []
            if relevant_sentences:
                expected_content = [sent[0] for sent in relevant_sentences[:2]]
                expected_text = '. '.join(expected_content).lower()
            else:
                expected_text = context_lower[:500]  # fallback to first part of document
            
            # Evaluate user answer
            is_correct = False
            feedback = ""
            
            # Check if user answer contains relevant keywords from expected content
            expected_words = set(word.strip('.,!?') for word in expected_text.split() if len(word) > 3)
            user_words = set(word.strip('.,!?') for word in user_answer_lower.split() if len(word) > 3)
            
            # Remove common words
            common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            expected_words -= common_words
            user_words -= common_words
            
            if expected_words and user_words:
                overlap = len(expected_words.intersection(user_words))
                overlap_ratio = overlap / len(expected_words) if expected_words else 0
                
                if overlap_ratio >= 0.3:  # 30% keyword overlap
                    is_correct = True
                    feedback = "Good job! Your answer captures key points from the document."
                elif overlap_ratio >= 0.1:
                    is_correct = False
                    feedback = "Your answer is partially correct but could include more specific details from the document."
                else:
                    is_correct = False
                    feedback = "Your answer needs improvement. Try to focus more on the specific information provided in the document."
            else:
                is_correct = False
                feedback = "Please provide a more detailed answer based on the document content."
            
            # Create justification from the most relevant sentence
            if relevant_sentences:
                justification = f"Based on the document: '{relevant_sentences[0][0][:150]}...'"
            else:
                justification = "Based on the overall document content."
            
            return {
                'is_correct': is_correct,
                'feedback': feedback,
                'justification': justification,
                'expected_keywords': list(expected_words)[:5]  # Show some expected keywords
            }
        except Exception as e:
            return {
                'is_correct': False,
                'feedback': f'Error evaluating answer: {str(e)}',
                'justification': 'Could not complete evaluation.'
            }
