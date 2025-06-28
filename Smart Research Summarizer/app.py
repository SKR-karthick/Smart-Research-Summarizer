import streamlit as st
import os
from document_processor import DocumentProcessor
from ai_assistant import AIAssistant
from utils import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("📚 Smart Research Assistant")
    st.markdown("Upload a document and interact with it using AI-powered features")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file",
            type=['pdf', 'txt'],
            help="Upload a document to analyze and interact with. PDF text extraction has been enhanced for better results."
        )
        
        if uploaded_file is not None:
            if st.button("Process Document", type="primary"):
                with st.spinner("Processing document..."):
                    try:
                        # Process the document
                        processor = DocumentProcessor()
                        text = processor.extract_text(uploaded_file)
                        
                        if text:
                            st.session_state.document_text = text
                            st.session_state.document_name = uploaded_file.name
                            st.session_state.document_processed = True
                            
                            # Generate summary
                            assistant = AIAssistant()
                            summary = assistant.generate_summary(text)
                            st.session_state.document_summary = summary
                            
                            st.success("Document processed successfully!")
                            st.rerun()
                        else:
                            st.error("Could not extract text from the document.")
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
    
    # Main content area
    if st.session_state.document_processed:
        # Display document info and summary
        st.header(f"📄 {st.session_state.document_name}")
        
        # Summary section
        st.subheader("📝 Document Summary")
        st.info(st.session_state.document_summary)
        
        # Mode selection
        st.subheader("🎯 Choose Interaction Mode")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("❓ Ask Anything", type="secondary", use_container_width=True):
                st.session_state.mode = "ask_anything"
                st.rerun()
        
        with col2:
            if st.button("🧠 Challenge Me", type="secondary", use_container_width=True):
                st.session_state.mode = "challenge_me"
                st.rerun()
        
        # Mode-specific content
        if st.session_state.mode == "ask_anything":
            ask_anything_mode()
        elif st.session_state.mode == "challenge_me":
            challenge_me_mode()
    
    else:
        # Welcome message
        st.markdown("""
        ## Welcome to the Smart Research Assistant!
        
        This AI-powered tool helps you:
        - **Upload** PDF or TXT documents
        - **Get automatic summaries** of your documents
        - **Ask questions** about the content
        - **Take challenges** with auto-generated questions
        
        ### How to get started:
        1. Upload a document using the sidebar
        2. Click "Process Document" to analyze it
        3. Choose your interaction mode
        """)

def ask_anything_mode():
    st.subheader("❓ Ask Anything Mode")
    st.markdown("Ask any question about your document. The AI will answer based on the document content.")
    
    # Question input
    question = st.text_input(
        "What would you like to know about the document?",
        placeholder="Enter your question here..."
    )
    
    if st.button("Get Answer", type="primary") and question:
        with st.spinner("Finding answer..."):
            try:
                assistant = AIAssistant()
                answer, justification = assistant.answer_question(
                    st.session_state.document_text, 
                    question
                )
                
                # Display answer
                st.success("**Answer:**")
                st.write(answer)
                
                st.info("**Justification:**")
                st.write(justification)
                
            except Exception as e:
                st.error(f"Error answering question: {str(e)}")
    
    # Display previous Q&A if any
    if 'qa_history' in st.session_state and st.session_state.qa_history:
        st.subheader("📋 Previous Questions & Answers")
        for i, qa in enumerate(reversed(st.session_state.qa_history)):
            with st.expander(f"Q{len(st.session_state.qa_history)-i}: {qa['question'][:50]}..."):
                st.write(f"**Q:** {qa['question']}")
                st.write(f"**A:** {qa['answer']}")
                st.write(f"**Justification:** {qa['justification']}")

def challenge_me_mode():
    st.subheader("🧠 Challenge Me Mode")
    st.markdown("Test your understanding with AI-generated questions based on the document.")
    
    # Generate questions if not already done
    if 'challenge_questions' not in st.session_state or st.session_state.challenge_questions is None:
        if st.button("Generate Questions", type="primary"):
            with st.spinner("Generating questions..."):
                try:
                    assistant = AIAssistant()
                    questions = assistant.generate_questions(st.session_state.document_text)
                    st.session_state.challenge_questions = questions
                    st.session_state.user_answers = [""] * len(questions)
                    st.session_state.evaluations = [None] * len(questions)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating questions: {str(e)}")
    else:
        # Display questions and collect answers
        st.markdown("**Answer the following questions based on the document:**")
        
        for i, question in enumerate(st.session_state.challenge_questions):
            st.markdown(f"**Question {i+1}:** {question}")
            
            # User answer input
            user_answer = st.text_area(
                f"Your answer for Question {i+1}:",
                value=st.session_state.user_answers[i],
                key=f"answer_{i}"
            )
            st.session_state.user_answers[i] = user_answer
            
            # Evaluate answer button
            if st.button(f"Evaluate Answer {i+1}", key=f"eval_{i}") and user_answer:
                if user_answer.strip():
                    with st.spinner(f"Evaluating answer {i+1}..."):
                        try:
                            assistant = AIAssistant()
                            evaluation = assistant.evaluate_answer(
                                st.session_state.document_text,
                                question,
                                user_answer.strip()
                            )
                            st.session_state.evaluations[i] = evaluation
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error evaluating answer: {str(e)}")
            
            # Display evaluation if available
            if st.session_state.evaluations[i]:
                eval_data = st.session_state.evaluations[i]
                if eval_data['is_correct']:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect")
                
                st.info(f"**Feedback:** {eval_data['feedback']}")
                st.write(f"**Justification:** {eval_data['justification']}")
            
            st.divider()
        
        # Reset questions button
        if st.button("Generate New Questions", type="secondary"):
            del st.session_state.challenge_questions
            del st.session_state.user_answers
            del st.session_state.evaluations
            st.rerun()

if __name__ == "__main__":
    main()
