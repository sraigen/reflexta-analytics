#!/usr/bin/env python3
"""
Professional Popup AI Chat Bot for Reflexta Analytics Platform.
"""

import streamlit as st
from datetime import datetime
from src.enhanced_ai_assistant import get_enhanced_ai_assistant


def render_popup_chat():
    """Render a professional popup AI chat interface."""
    
    # Initialize chat history if not exists
    if "popup_chat_history" not in st.session_state:
        st.session_state.popup_chat_history = []
    
    # Initialize AI assistant if not exists
    if "popup_ai_assistant" not in st.session_state:
        st.session_state.popup_ai_assistant = get_enhanced_ai_assistant()
    
    # Professional CSS for popup chat
    st.markdown("""
    <style>
    .popup-chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 400px;
        height: 600px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
        backdrop-filter: blur(20px);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .popup-chat-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 1.5rem;
        text-align: center;
        border-radius: 20px 20px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .popup-chat-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .popup-chat-header h3 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
        background: linear-gradient(45deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .popup-chat-header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    .popup-chat-messages {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f6 100%);
        max-height: 400px;
    }
    
    .popup-chat-message {
        margin-bottom: 1rem;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
        animation: slideIn 0.3s ease-out;
    }
    
    .popup-chat-message.user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .popup-chat-message.ai {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        color: #1e293b;
        margin-right: auto;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .popup-chat-input {
        padding: 1rem;
        background: white;
        border-top: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .popup-chat-input input {
        width: 100%;
        padding: 0.8rem 1rem;
        border: 2px solid #e2e8f6;
        border-radius: 12px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    }
    
    .popup-chat-input input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .popup-chat-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.8rem;
    }
    
    .popup-chat-btn {
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
    
    .popup-chat-btn.primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .popup-chat-btn.primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    .popup-chat-btn.secondary {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f6 100%);
        color: #64748b;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .popup-chat-btn.secondary:hover {
        background: linear-gradient(135deg, #e2e8f6 0%, #cbd5e1 100%);
    }
    
    .popup-chat-suggestions {
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-top: 1px solid rgba(251, 191, 36, 0.3);
    }
    
    .popup-chat-suggestion {
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
    
    .popup-chat-suggestion:hover {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
    }
    
    .popup-chat-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1001;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .popup-chat-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(99, 102, 241, 0.6);
    }
    
    .popup-chat-toggle:active {
        transform: scale(0.95);
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
    
    .popup-chat-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .popup-chat-close:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.1);
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .popup-chat-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .popup-chat-messages {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    }
    
    .stApp[data-theme="dark"] .popup-chat-message.ai {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        color: #f1f5f9;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .popup-chat-input {
        background: #1e293b;
        border-top: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .popup-chat-input input {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        border: 2px solid rgba(148, 163, 184, 0.3);
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .popup-chat-input input::placeholder {
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Toggle button for chat
    if "popup_chat_open" not in st.session_state:
        st.session_state.popup_chat_open = False
    
    # Chat toggle button
    if st.button("🤖", key="popup_chat_toggle", help="Open AI Assistant"):
        st.session_state.popup_chat_open = not st.session_state.popup_chat_open
        st.rerun()
    
    # Popup chat interface
    if st.session_state.popup_chat_open:
        # Chat header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%); 
                    color: white; padding: 1.5rem; text-align: center; border-radius: 12px; 
                    margin-bottom: 1rem; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);">
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">🤖 AI Assistant</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Your Analytics Companion</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.popup_chat_history:
            st.markdown("**💬 Chat History:**")
            for message in st.session_state.popup_chat_history:
                if message['type'] == 'user':
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
                                color: white; padding: 0.8rem 1rem; border-radius: 12px; 
                                margin: 0.5rem 0; text-align: right; max-width: 85%; margin-left: auto;">
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%); 
                                color: #1e293b; padding: 0.8rem 1rem; border-radius: 12px; 
                                margin: 0.5rem 0; border: 1px solid rgba(148, 163, 184, 0.2); 
                                max-width: 85%; margin-right: auto;">
                        <strong>AI:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Start a conversation with the AI Assistant!")
        
        # Chat input
        user_input = st.text_input(
            "Ask me anything about the dashboard...",
            placeholder="e.g., What does 'Budget Utilization' mean?",
            key="popup_chat_input"
        )
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("💬 Ask AI", key="popup_send_btn", use_container_width=True):
                if user_input and user_input.strip():
                    # Add user message
                    st.session_state.popup_chat_history.append({
                        'type': 'user',
                        'content': user_input,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    if st.session_state.popup_ai_assistant:
                        try:
                            with st.spinner("🤖 AI is thinking..."):
                                ai_response = st.session_state.popup_ai_assistant.ask_ai(user_input)
                            
                            # Add AI response
                            st.session_state.popup_chat_history.append({
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
            if st.button("🗑️ Clear", key="popup_clear_btn", use_container_width=True):
                st.session_state.popup_chat_history = []
                st.rerun()
        
        with col3:
            if st.button("❌ Close", key="popup_close_btn", use_container_width=True):
                st.session_state.popup_chat_open = False
                st.rerun()
        
        # Suggested questions
        if st.session_state.popup_ai_assistant:
            suggested_questions = st.session_state.popup_ai_assistant.get_suggested_questions()
            
            st.markdown("**💡 Quick Questions:**")
            
            # Show 3 suggested questions
            for i, question in enumerate(suggested_questions[:3]):
                if st.button(f"💭 {question}", key=f"popup_suggested_{i}", use_container_width=True):
                    # Auto-process the question
                    st.session_state.popup_chat_history.append({
                        'type': 'user',
                        'content': question,
                        'timestamp': datetime.now()
                    })
                    
                    # Get AI response
                    try:
                        with st.spinner("🤖 AI is thinking..."):
                            ai_response = st.session_state.popup_ai_assistant.ask_ai(question)
                        
                        st.session_state.popup_chat_history.append({
                            'type': 'ai',
                            'content': ai_response,
                            'timestamp': datetime.now()
                        })
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    
                    st.rerun()
        else:
            st.warning("AI Assistant not available. Please check your API configuration.")


def render_chat_toggle():
    """Render the floating chat toggle button."""
    st.markdown("""
    <div class="popup-chat-toggle" onclick="document.querySelector('.popup-chat-container').style.display='block'">
        🤖
    </div>
    """, unsafe_allow_html=True)
