"""
Chat UI components for AI Assistant integration.
Provides user-friendly chat interface with professional styling.
"""

import streamlit as st
from typing import List, Dict, Any
from datetime import datetime
from src.ai_assistant import get_ai_assistant, format_ai_response


def render_chat_interface():
    """Render the main chat interface in sidebar."""
    
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = get_ai_assistant()
    
    # Chat interface styling
    st.markdown("""
    <style>
    .chat-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f6 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .chat-message {
        background: white;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 3px solid #6366f1;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-left: 3px solid #4f46e5;
    }
    
    .chat-message.ai {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 3px solid #0ea5e9;
    }
    
    .suggested-question {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f6 100%);
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.85rem;
    }
    
    .suggested-question:hover {
        background: linear-gradient(135deg, #e2e8f6 0%, #cbd5e1 100%);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if AI assistant is available
    if st.session_state.ai_assistant is None:
        st.error("🤖 AI Assistant not available. Please configure DeepSeek API key in secrets.")
        return
    
    # Chat header
    st.markdown("""
    <div class="chat-container">
        <h4 style="margin: 0 0 1rem 0; color: #1e293b; text-align: center;">🤖 AI Assistant</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("**💬 Conversation History**")
        
        # Show last 3 messages to keep sidebar clean
        recent_messages = st.session_state.chat_history[-3:]
        
        for message in recent_messages:
            if message['type'] == 'user':
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai">
                    <strong>AI:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_question = st.text_input(
        "Ask me anything about the dashboard...",
        placeholder="e.g., What does 'Budget Utilization' mean?",
        key="chat_input"
    )
    
    # Chat buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💬 Ask AI", use_container_width=True, key="ask_ai_btn"):
            if user_question.strip():
                # Add user message to history
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': user_question,
                    'timestamp': datetime.now()
                })
                
                # Get AI response
                with st.spinner("🤖 AI is thinking..."):
                    ai_response = st.session_state.ai_assistant.ask_ai(user_question)
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'content': ai_response,
                    'timestamp': datetime.now()
                })
                
                # Clear input and rerun
                st.session_state.chat_input = ""
                st.rerun()
            else:
                st.warning("Please enter a question!")
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Suggested questions
    if st.session_state.ai_assistant:
        suggested_questions = st.session_state.ai_assistant.get_suggested_questions()
        
        st.markdown("**💡 Suggested Questions**")
        
        # Show 4 suggested questions
        for i, question in enumerate(suggested_questions[:4]):
            if st.button(f"💭 {question}", key=f"suggested_{i}", use_container_width=True):
                # Set the question as input
                st.session_state.chat_input = question
                st.rerun()
    
    # AI status indicator
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; padding: 0.5rem; background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); border-radius: 6px; border: 1px solid #22c55e;">
        <small style="color: #166534;">🤖 AI Assistant Ready</small>
    </div>
    """, unsafe_allow_html=True)


def render_quick_help():
    """Render quick help section for common questions."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 8px; padding: 1rem; margin: 1rem 0; border: 1px solid #f59e0b;">
        <h5 style="margin: 0 0 0.5rem 0; color: #92400e;">💡 Quick Help</h5>
        <p style="margin: 0; color: #92400e; font-size: 0.9rem;">
            Ask the AI assistant about KPIs, dashboard features, data interpretation, or navigation help.
        </p>
    </div>
    """, unsafe_allow_html=True)


def get_chat_stats() -> Dict[str, Any]:
    """Get chat statistics for display."""
    if 'chat_history' not in st.session_state:
        return {"total_messages": 0, "user_messages": 0, "ai_messages": 0}
    
    chat_history = st.session_state.chat_history
    total_messages = len(chat_history)
    user_messages = len([msg for msg in chat_history if msg['type'] == 'user'])
    ai_messages = len([msg for msg in chat_history if msg['type'] == 'ai'])
    
    return {
        "total_messages": total_messages,
        "user_messages": user_messages,
        "ai_messages": ai_messages
    }
