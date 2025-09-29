"""
AI Assistant module for Reflexta Analytics Platform.
Provides intelligent chatbot functionality using DeepSeek API.
"""

import json
import requests
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd


class AIAssistant:
    """AI Assistant for dashboard help and data insights."""
    
    def __init__(self, api_key: str):
        """Initialize the AI assistant with DeepSeek API key."""
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        
    def get_dashboard_context(self) -> Dict[str, Any]:
        """Get current dashboard context for AI responses."""
        try:
            # Get current page info
            current_page = st.session_state.get('current_page', 'Executive Dashboard')
            
            # Get available KPIs and data context
            context = {
                "current_dashboard": current_page,
                "available_modules": [
                    "Finance Dashboard - Budget management, transaction tracking, cost center analysis",
                    "Procurement Dashboard - Vendor management, order tracking, category analysis", 
                    "Analytics Dashboard - Executive business intelligence and reporting",
                    "Database Analysis - Schema exploration and data quality checks"
                ],
                "common_kpis": [
                    "Total Revenue - Sum of all revenue transactions",
                    "Total Expenses - Sum of all expense transactions", 
                    "Net Income - Revenue minus expenses",
                    "Budget Utilization - Percentage of budget used",
                    "Total Orders - Number of procurement orders",
                    "Order Completion Rate - Percentage of completed orders",
                    "Vendor Performance - Vendor ratings and delivery metrics"
                ],
                "data_sources": [
                    "Finance Transactions - Revenue and expense data",
                    "Procurement Orders - Purchase orders and vendor data",
                    "Department Budgets - Budget allocations and spending",
                    "Vendor Information - Vendor details and performance metrics"
                ],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return context
            
        except Exception as e:
            st.error(f"Error getting dashboard context: {str(e)}")
            return {"error": str(e)}
    
    def format_context_for_ai(self, context: Dict[str, Any], user_question: str) -> str:
        """Format context and user question for AI processing."""
        
        context_prompt = f"""
You are an expert business intelligence assistant for Reflexta Data Intelligence, a comprehensive analytics platform.

CURRENT DASHBOARD CONTEXT:
- Dashboard: {context.get('current_dashboard', 'Executive Dashboard')}
- Available Modules: {', '.join(context.get('available_modules', []))}
- Common KPIs: {', '.join(context.get('common_kpis', []))}
- Data Sources: {', '.join(context.get('data_sources', []))}
- Current Time: {context.get('timestamp', 'Unknown')}

USER QUESTION: {user_question}

INSTRUCTIONS:
1. Provide helpful, accurate responses about the analytics platform
2. Explain KPIs, metrics, and dashboard functionality clearly
3. Suggest relevant actions or navigation tips
4. Use professional, business-friendly language
5. If asked about data interpretation, provide insights and recommendations
6. Keep responses concise but informative (2-3 paragraphs max)
7. If you don't know something specific, suggest where to find it

RESPONSE FORMAT:
- Use markdown formatting for better readability
- Include emojis sparingly for visual appeal
- Provide actionable advice when possible
- Reference specific dashboard features when relevant
"""
        
        return context_prompt
    
    def ask_ai(self, user_question: str) -> str:
        """Send question to DeepSeek API and return response."""
        
        try:
            # Get dashboard context
            context = self.get_dashboard_context()
            
            # Format prompt for AI
            formatted_prompt = self.format_context_for_ai(context, user_question)
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional business intelligence assistant for Reflexta Data Intelligence analytics platform. Provide helpful, accurate, and actionable responses about dashboard functionality, KPIs, and data insights."
                    },
                    {
                        "role": "user", 
                        "content": formatted_prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            # Make API request
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                return ai_response
            else:
                return f"❌ **API Error {response.status_code}**: {response.text}"
                
        except requests.exceptions.Timeout:
            return "⏰ **Request Timeout**: The AI service is taking too long to respond. Please try again."
        except requests.exceptions.RequestException as e:
            return f"🌐 **Connection Error**: Unable to connect to AI service. Error: {str(e)}"
        except Exception as e:
            return f"❌ **Unexpected Error**: {str(e)}"
    
    def get_suggested_questions(self) -> List[str]:
        """Get suggested questions for users."""
        return [
            "What does 'Budget Utilization' mean?",
            "How do I filter data by department?",
            "Explain the procurement metrics",
            "What insights can I get from this dashboard?",
            "How do I export reports?",
            "What do these KPIs tell me about performance?",
            "How can I improve procurement efficiency?",
            "What trends should I watch for?"
        ]


def get_ai_assistant() -> Optional[AIAssistant]:
    """Get AI assistant instance if API key is available."""
    try:
        # Try to get API key from Streamlit secrets
        api_key = None
        
        # Method 1: Direct access to secrets
        try:
            api_key = st.secrets["deepseek_api_key"]
        except (KeyError, AttributeError):
            pass
        
        # Method 2: Try get method
        if not api_key:
            try:
                api_key = st.secrets.get("deepseek_api_key")
            except (KeyError, AttributeError):
                pass
        
        # Method 3: Environment variable as fallback
        if not api_key:
            import os
            api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # Debug information
        if api_key:
            # Check if API key looks valid
            if api_key.startswith("sk-") and len(api_key) > 20:
                return AIAssistant(api_key)
            else:
                st.error(f"Invalid API key format: {api_key[:10]}...")
                return None
        else:
            st.error("DeepSeek API key not found in secrets or environment variables")
            return None
            
    except Exception as e:
        st.error(f"Error initializing AI assistant: {str(e)}")
        return None


def format_ai_response(response: str) -> str:
    """Format AI response for better display."""
    # Add some basic formatting improvements
    if "**" in response:
        # Already has markdown formatting
        return response
    else:
        # Add some basic formatting
        return f"🤖 **AI Assistant**: {response}"
