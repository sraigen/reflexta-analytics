#!/usr/bin/env python3
"""
Sidebar AI Chat Bot for Reflexta Analytics Platform.
Provides a sidebar-based AI chat interface that's always accessible.
"""

import streamlit as st
from datetime import datetime
from src.enhanced_ai_assistant import get_enhanced_ai_assistant


def render_sidebar_ai_chat():
    """Render a sidebar AI chat interface that's always accessible."""
    
    # Initialize chat history if not exists
    if "sidebar_chat_history" not in st.session_state:
        st.session_state.sidebar_chat_history = []
    
    # Initialize AI assistant if not exists
    if "sidebar_ai_assistant" not in st.session_state:
        st.session_state.sidebar_ai_assistant = get_enhanced_ai_assistant()
    
    # Sidebar AI Chat CSS
    st.markdown("""
    <style>
    /* Sidebar AI Chat Styling */
    .sidebar-ai-chat {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f6 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-ai-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sidebar-ai-header h4 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .sidebar-ai-header p {
        margin: 0.3rem 0 0 0;
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    .sidebar-ai-messages {
        max-height: 300px;
        overflow-y: auto;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: white;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .sidebar-ai-message {
        margin-bottom: 0.8rem;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .sidebar-ai-message.user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        max-width: 85%;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    .sidebar-ai-message.ai {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        color: #1e293b;
        margin-right: auto;
        border: 1px solid rgba(148, 163, 184, 0.2);
        max-width: 85%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-ai-message strong {
        display: block;
        margin-bottom: 0.3rem;
        font-size: 0.8rem;
        opacity: 0.8;
    }
    
    .sidebar-ai-input {
        margin-bottom: 1rem;
    }
    
    .sidebar-ai-input input {
        width: 100%;
        padding: 0.6rem 0.8rem;
        border: 1px solid #e2e8f6;
        border-radius: 8px;
        font-size: 0.9rem;
        background: white;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-ai-input input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
    }
    
    .sidebar-ai-buttons {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-ai-btn {
        flex: 1;
        padding: 0.5rem 0.8rem;
        border: none;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sidebar-ai-btn.primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    .sidebar-ai-btn.primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .sidebar-ai-btn.secondary {
        background: #f1f5f9;
        color: #64748b;
        border: 1px solid #e2e8f6;
    }
    
    .sidebar-ai-btn.secondary:hover {
        background: #e2e8f6;
    }
    
    .sidebar-ai-suggestions {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 8px;
        padding: 0.8rem;
    }
    
    .sidebar-ai-suggestion {
        display: block;
        margin: 0.3rem 0;
        padding: 0.4rem 0.6rem;
        background: white;
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 6px;
        font-size: 0.8rem;
        color: #92400e;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }
    
    .sidebar-ai-suggestion:hover {
        background: #fef3c7;
        transform: translateY(-1px);
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .sidebar-ai-chat {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .sidebar-ai-messages {
        background: #1e293b;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .sidebar-ai-message.ai {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        color: #f1f5f9;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .sidebar-ai-input input {
        background: #334155;
        border: 1px solid rgba(148, 163, 184, 0.3);
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .sidebar-ai-input input::placeholder {
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar AI Chat Interface
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-ai-chat">
            <div class="sidebar-ai-header">
                <h4>🤖 AI Assistant</h4>
                <p>Your Analytics Companion</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.sidebar_chat_history:
            st.markdown("**💬 Chat History:**")
            for message in st.session_state.sidebar_chat_history:
                message_class = "user" if message['type'] == 'user' else "ai"
                st.markdown(f"""
                <div class="sidebar-ai-message {message_class}">
                    <strong>{'You' if message['type'] == 'user' else 'AI'}:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sidebar-ai-message ai">
                <strong>AI:</strong> Hello! I'm your AI assistant for Reflexta Analytics Platform. 
                I can help you understand dashboards, KPIs, and provide insights about your data. 
                How can I assist you today?
            </div>
            """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input(
            "Ask me anything...",
            placeholder="e.g., What does 'Budget Utilization' mean?",
            key="sidebar_chat_input"
        )
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💬 Ask AI", key="sidebar_send_btn", use_container_width=True):
                if user_input and user_input.strip():
                    # Add user message
                    st.session_state.sidebar_chat_history.append({
                        'type': 'user',
                        'content': user_input,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    if st.session_state.sidebar_ai_assistant:
                        try:
                            with st.spinner("🤖 AI is thinking..."):
                                ai_response = st.session_state.sidebar_ai_assistant.ask_ai(user_input)
                            
                            # Add AI response
                            st.session_state.sidebar_chat_history.append({
                                'type': 'ai',
                                'content': ai_response,
                                'timestamp': datetime.now()
                            })
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.error("AI Assistant not available")
                    
                    st.rerun()
                else:
                    st.warning("Please enter a question!")
        
        with col2:
            if st.button("🗑️ Clear", key="sidebar_clear_btn", use_container_width=True):
                st.session_state.sidebar_chat_history = []
                st.rerun()
        
        # Suggested questions
        if st.session_state.sidebar_ai_assistant:
            suggested_questions = st.session_state.sidebar_ai_assistant.get_suggested_questions()
            
            st.markdown("**💡 Quick Questions:**")
            
            # Show 3 suggested questions
            for i, question in enumerate(suggested_questions[:3]):
                if st.button(f"💭 {question}", key=f"sidebar_suggested_{i}", use_container_width=True):
                    # Auto-process the question
                    st.session_state.sidebar_chat_history.append({
                        'type': 'user',
                        'content': question,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    try:
                        with st.spinner("🤖 AI is thinking..."):
                            ai_response = st.session_state.sidebar_ai_assistant.ask_ai(question)
                        
                        st.session_state.sidebar_chat_history.append({
                            'type': 'ai',
                            'content': ai_response,
                            'timestamp': datetime.now()
                        })
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    
                    st.rerun()
        else:
            st.warning("AI Assistant not available. Please check your API configuration.")
