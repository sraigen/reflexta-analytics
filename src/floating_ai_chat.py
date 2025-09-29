#!/usr/bin/env python3
"""
Floating AI Chat Bot for Reflexta Analytics Platform.
Provides a floating AI chat interface that's always visible.
"""

import streamlit as st
from datetime import datetime
from src.enhanced_ai_assistant import get_enhanced_ai_assistant


def render_floating_ai_chat():
    """Render a floating AI chat interface that's always visible."""
    
    # Initialize chat history if not exists
    if "floating_chat_history" not in st.session_state:
        st.session_state.floating_chat_history = []
    
    # Initialize AI assistant if not exists
    if "floating_ai_assistant" not in st.session_state:
        st.session_state.floating_ai_assistant = get_enhanced_ai_assistant()
    
    # Initialize chat state
    if "floating_chat_open" not in st.session_state:
        st.session_state.floating_chat_open = False
    
    # Floating AI Chat CSS
    st.markdown("""
    <style>
    /* Floating AI Chat Button */
    .floating-ai-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse 2s infinite;
    }
    
    .floating-ai-button:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(99, 102, 241, 0.6);
    }
    
    .floating-ai-button:active {
        transform: scale(0.95);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 8px 25px rgba(99, 102, 241, 0.8); }
        100% { box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4); }
    }
    
    /* Floating Chat Panel */
    .floating-chat-panel {
        position: fixed;
        top: 0;
        right: 0;
        width: 400px;
        height: 100vh;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-left: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: -8px 0 32px rgba(0, 0, 0, 0.15);
        z-index: 1001;
        display: flex;
        flex-direction: column;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .floating-chat-panel.open {
        transform: translateX(0);
    }
    
    /* Chat Header */
    .floating-chat-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .floating-chat-header h3 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .floating-chat-header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Chat Messages */
    .floating-chat-messages {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f6 100%);
        max-height: calc(100vh - 200px);
    }
    
    .floating-chat-message {
        margin-bottom: 1rem;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
        animation: slideIn 0.3s ease-out;
    }
    
    .floating-chat-message.user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .floating-chat-message.ai {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        color: #1e293b;
        margin-right: auto;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .floating-chat-message strong {
        display: block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Chat Input */
    .floating-chat-input {
        padding: 1rem;
        background: white;
        border-top: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .floating-chat-input input {
        width: 100%;
        padding: 0.8rem 1rem;
        border: 2px solid #e2e8f6;
        border-radius: 12px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        margin-bottom: 0.8rem;
    }
    
    .floating-chat-input input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .floating-chat-buttons {
        display: flex;
        gap: 0.5rem;
    }
    
    .floating-chat-btn {
        flex: 1;
        padding: 0.6rem 1rem;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .floating-chat-btn.primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .floating-chat-btn.primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    .floating-chat-btn.secondary {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f6 100%);
        color: #64748b;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .floating-chat-btn.secondary:hover {
        background: linear-gradient(135deg, #e2e8f6 0%, #cbd5e1 100%);
    }
    
    /* Suggested Questions */
    .floating-chat-suggestions {
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-top: 1px solid rgba(251, 191, 36, 0.3);
    }
    
    .floating-chat-suggestion {
        display: inline-block;
        margin: 0.2rem;
        padding: 0.4rem 0.8rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 8px;
        font-size: 0.8rem;
        color: #92400e;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .floating-chat-suggestion:hover {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .floating-chat-panel {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-left: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .floating-chat-messages {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    }
    
    .stApp[data-theme="dark"] .floating-chat-message.ai {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        color: #f1f5f9;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .floating-chat-input {
        background: #1e293b;
        border-top: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .floating-chat-input input {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        border: 2px solid rgba(148, 163, 184, 0.3);
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .floating-chat-input input::placeholder {
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Floating AI Chat Toggle Button (always visible)
    if st.button("🤖", key="floating_ai_toggle", help="Open AI Assistant", type="primary"):
        st.session_state.floating_chat_open = not st.session_state.floating_chat_open
        st.rerun()
    
    # Floating Chat Panel
    if st.session_state.floating_chat_open:
        st.markdown("""
        <div class="floating-chat-panel open">
            <div class="floating-chat-header">
                <h3>🤖 AI Assistant</h3>
                <p>Your Analytics Companion</p>
            </div>
            
            <div class="floating-chat-messages">
        """, unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.floating_chat_history:
            for message in st.session_state.floating_chat_history:
                message_class = "user" if message['type'] == 'user' else "ai"
                st.markdown(f"""
                <div class="floating-chat-message {message_class}">
                    <strong>{'You' if message['type'] == 'user' else 'AI'}:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="floating-chat-message ai">
                <strong>AI:</strong> Hello! I'm your AI assistant for Reflexta Analytics Platform. 
                I can help you understand dashboards, KPIs, and provide insights about your data. 
                How can I assist you today?
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input(
            "Ask me anything about the dashboard...",
            placeholder="e.g., What does 'Budget Utilization' mean?",
            key="floating_chat_input"
        )
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💬 Ask AI", key="floating_send_btn", use_container_width=True):
                if user_input and user_input.strip():
                    # Add user message
                    st.session_state.floating_chat_history.append({
                        'type': 'user',
                        'content': user_input,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    if st.session_state.floating_ai_assistant:
                        try:
                            with st.spinner("🤖 AI is thinking..."):
                                ai_response = st.session_state.floating_ai_assistant.ask_ai(user_input)
                            
                            # Add AI response
                            st.session_state.floating_chat_history.append({
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
            if st.button("🗑️ Clear", key="floating_clear_btn", use_container_width=True):
                st.session_state.floating_chat_history = []
                st.rerun()
        
        # Suggested questions
        if st.session_state.floating_ai_assistant:
            suggested_questions = st.session_state.floating_ai_assistant.get_suggested_questions()
            
            st.markdown("**💡 Quick Questions:**")
            
            # Show 4 suggested questions
            for i, question in enumerate(suggested_questions[:4]):
                if st.button(f"💭 {question}", key=f"floating_suggested_{i}", use_container_width=True):
                    # Auto-process the question
                    st.session_state.floating_chat_history.append({
                        'type': 'user',
                        'content': question,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    try:
                        with st.spinner("🤖 AI is thinking..."):
                            ai_response = st.session_state.floating_ai_assistant.ask_ai(question)
                        
                        st.session_state.floating_chat_history.append({
                            'type': 'ai',
                            'content': ai_response,
                            'timestamp': datetime.now()
                        })
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    
                    st.rerun()
        else:
            st.warning("AI Assistant not available. Please check your API configuration.")
        
        st.markdown("</div>", unsafe_allow_html=True)
