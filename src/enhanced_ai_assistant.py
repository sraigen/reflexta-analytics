#!/usr/bin/env python3
"""
Enhanced AI Assistant module for Reflexta Analytics Platform.
Provides intelligent chatbot functionality with real data integration using DeepSeek API.
"""

import json
import requests
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd


class EnhancedAIAssistant:
    """Enhanced AI Assistant with real data integration for dashboard help and insights."""
    
    def __init__(self, api_key: str):
        """Initialize the AI assistant with DeepSeek API key."""
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        
    def get_real_dashboard_context(self) -> Dict[str, Any]:
        """Get current dashboard context with real data for AI responses."""
        try:
            from src.db import get_conn
            from src.finance_queries import get_finance_kpis, get_finance_summary
            from src.procurement_queries import get_procurement_kpis, get_procurement_summary
            
            # Get real data from database with default date range
            conn = get_conn()
            
            # Set default date range (last 30 days)
            from datetime import datetime, timedelta
            today = datetime.now().date()
            from_date = today - timedelta(days=30)
            to_date = today
            
            # Get current KPIs with date parameters
            finance_kpis = get_finance_kpis(from_date, to_date, None)
            procurement_kpis = get_procurement_kpis(from_date, to_date, None)
            
            # Get department summaries with date parameters
            finance_summary = get_finance_summary(from_date, to_date, None)
            procurement_summary = get_procurement_summary(from_date, to_date, None)
            
            # Build context with real data
            context = {
                "current_dashboard": "Executive Dashboard",
                "real_data": {
                    "finance_metrics": {
                        "total_revenue": finance_kpis.get('total_revenue', 0),
                        "total_expenses": finance_kpis.get('total_expenses', 0),
                        "net_income": finance_kpis.get('net_income', 0),
                        "total_transactions": finance_kpis.get('total_transactions', 0),
                        "revenue_growth": finance_kpis.get('revenue_growth', 0),
                        "expense_growth": finance_kpis.get('expense_growth', 0)
                    },
                    "procurement_metrics": {
                        "total_orders": procurement_kpis.get('total_orders', 0),
                        "total_spend": procurement_kpis.get('total_spend', 0),
                        "avg_order_value": procurement_kpis.get('avg_order_value', 0),
                        "active_vendors": procurement_kpis.get('active_vendors', 0),
                        "order_growth": procurement_kpis.get('order_growth', 0),
                        "spend_growth": procurement_kpis.get('spend_growth', 0)
                    },
                    "department_data": {
                        "finance_departments": self._convert_dataframe_to_json(finance_summary),
                        "procurement_departments": self._convert_dataframe_to_json(procurement_summary)
                    }
                },
                "available_modules": [
                    "Finance Dashboard - Budget management, transaction tracking, cost center analysis",
                    "Procurement Dashboard - Vendor management, order tracking, category analysis", 
                    "Analytics Dashboard - Executive business intelligence and reporting",
                    "Database Analysis - Schema exploration and data quality checks"
                ],
                "data_insights": self._generate_data_insights(finance_kpis, procurement_kpis, finance_summary, procurement_summary),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return context
            
        except Exception as e:
            # Return fallback context with basic information
            return {
                "current_dashboard": "Executive Dashboard",
                "real_data": {
                    "finance_metrics": {"error": "Data access temporarily unavailable"},
                    "procurement_metrics": {"error": "Data access temporarily unavailable"},
                    "department_data": {"error": "Data access temporarily unavailable"}
                },
                "available_modules": [
                    "Finance Dashboard - Budget management, transaction tracking, cost center analysis",
                    "Procurement Dashboard - Vendor management, order tracking, category analysis", 
                    "Analytics Dashboard - Executive business intelligence and reporting",
                    "Database Analysis - Schema exploration and data quality checks"
                ],
                "data_insights": ["⚠️ Real-time data access temporarily unavailable"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fallback_mode": True
            }
    
    def _convert_dataframe_to_json(self, df):
        """Convert pandas DataFrame to JSON-serializable format."""
        try:
            if df is None or df.empty:
                return []
            
            # Convert DataFrame to records and handle any non-serializable values
            records = []
            for _, row in df.iterrows():
                record = {}
                for col in df.columns:
                    value = row[col]
                    # Handle pandas Series and other non-serializable types
                    if hasattr(value, 'item'):  # pandas scalar
                        record[col] = value.item()
                    elif hasattr(value, 'tolist'):  # numpy array
                        record[col] = value.tolist()
                    else:
                        record[col] = str(value) if value is not None else None
                records.append(record)
            
            return records
            
        except Exception as e:
            return [{"error": f"Failed to convert data: {str(e)}"}]
    
    def _generate_data_insights(self, finance_kpis, procurement_kpis, finance_summary, procurement_summary):
        """Generate insights from real data."""
        insights = []
        
        try:
            # Finance insights
            if finance_kpis.get('net_income', 0) > 0:
                insights.append(f"✅ Positive net income of ${finance_kpis.get('net_income', 0):,.0f}")
            else:
                insights.append(f"⚠️ Negative net income of ${finance_kpis.get('net_income', 0):,.0f}")
            
            if finance_kpis.get('revenue_growth', 0) > 0:
                insights.append(f"📈 Revenue growth of {finance_kpis.get('revenue_growth', 0):.1f}%")
            
            # Procurement insights
            if procurement_kpis.get('total_orders', 0) > 0:
                insights.append(f"📦 {procurement_kpis.get('total_orders', 0)} total orders processed")
            
            if procurement_kpis.get('avg_order_value', 0) > 0:
                insights.append(f"💰 Average order value: ${procurement_kpis.get('avg_order_value', 0):,.0f}")
            
            # Department insights
            if not finance_summary.empty:
                top_spender = finance_summary.loc[finance_summary['spent'].idxmax()] if 'spent' in finance_summary.columns else None
                if top_spender is not None:
                    insights.append(f"🏢 {top_spender.get('department', 'Unknown')} has highest spending: ${top_spender.get('spent', 0):,.0f}")
            
            if not procurement_summary.empty:
                top_procurement = procurement_summary.loc[procurement_summary['total_value'].idxmax()] if 'total_value' in procurement_summary.columns else None
                if top_procurement is not None:
                    insights.append(f"🛒 {top_procurement.get('department', 'Unknown')} has highest procurement: ${top_procurement.get('total_value', 0):,.0f}")
            
        except Exception as e:
            insights.append(f"⚠️ Error generating insights: {str(e)}")
        
        return insights
    
    def ask_ai(self, question: str) -> str:
        """Ask the AI assistant a question with real data context."""
        try:
            # Get real dashboard context
            context = self.get_real_dashboard_context()
            
            # Build enhanced prompt with real data or fallback
            if context.get('fallback_mode', False):
                system_prompt = f"""You are an AI assistant for Reflexta Data Intelligence, an enterprise analytics platform. 
                
                CURRENT STATUS: Real-time data access is temporarily unavailable, but I can still help with general analytics guidance.
                
                AVAILABLE MODULES:
                - Finance Dashboard: Budget management, transaction tracking, cost center analysis
                - Procurement Dashboard: Vendor management, order tracking, category analysis
                - Analytics Dashboard: Executive business intelligence and reporting
                - Database Analysis: Schema exploration and data quality checks
                
                When answering questions:
                1. Explain what the metrics mean and how they're typically calculated
                2. Provide general guidance on how to interpret and use these metrics
                3. Suggest best practices for data analysis and dashboard usage
                4. Explain how to access specific data in the dashboards
                5. Be helpful and educational about analytics concepts
                
                Always be helpful and provide valuable guidance even without real-time data access."""
            else:
                # Safely serialize context to JSON
                try:
                    context_json = json.dumps(context, indent=2, default=str)
                except Exception as e:
                    context_json = f"Data context available but contains complex objects: {str(e)}"
                
                system_prompt = f"""You are an AI assistant for Reflexta Data Intelligence, an enterprise analytics platform. 
                
                CURRENT REAL DATA CONTEXT:
                {context_json}
                
                You have access to real-time data from the following modules:
                - Finance Dashboard: Budget management, transaction tracking, cost center analysis
                - Procurement Dashboard: Vendor management, order tracking, category analysis
                - Analytics Dashboard: Executive business intelligence and reporting
                - Database Analysis: Schema exploration and data quality checks
                
                When answering questions:
                1. Use the ACTUAL data values provided in the context
                2. Provide specific insights based on real metrics
                3. Reference actual department performance and KPIs
                4. Give actionable recommendations based on current data
                5. Be specific about numbers, percentages, and trends
                6. If asked about metrics, explain what they mean AND provide current values
                
                Always be helpful, accurate, and data-driven in your responses."""
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: API request failed with status {response.status_code}"
                
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def get_suggested_questions(self) -> List[str]:
        """Get context-aware suggested questions based on real data."""
        try:
            context = self.get_real_dashboard_context()
            
            # Generate dynamic suggestions based on real data
            suggestions = []
            
            if context.get('real_data', {}).get('finance_metrics', {}).get('net_income', 0) < 0:
                suggestions.append("Why is our net income negative and how can we improve it?")
            
            if context.get('real_data', {}).get('procurement_metrics', {}).get('total_orders', 0) > 0:
                suggestions.append("What are our top performing procurement categories?")
            
            if context.get('real_data', {}).get('finance_metrics', {}).get('total_revenue', 0) > 0:
                suggestions.append("Which department has the highest revenue contribution?")
            
            # Add general suggestions
            suggestions.extend([
                "What does 'Budget Utilization' mean in our current data?",
                "How do I filter data by department in the dashboards?",
                "Explain the procurement metrics and their current values",
                "What insights can I get from our current financial performance?",
                "How is our vendor performance looking?",
                "What are the key trends in our spending patterns?"
            ])
            
            return suggestions[:6]  # Return top 6 suggestions
            
        except Exception as e:
            return [
                "What does 'Budget Utilization' mean?",
                "How do I filter data by department?",
                "Explain the procurement metrics",
                "What insights can I get from this dashboard?"
            ]


def get_enhanced_ai_assistant() -> Optional[EnhancedAIAssistant]:
    """Get enhanced AI assistant instance if API key is available."""
    try:
        # Try to get API key from Streamlit secrets
        api_key = None
        
        # Method 1: Try direct access to secrets
        try:
            if hasattr(st, 'secrets') and st.secrets:
                api_key = st.secrets.get("deepseek_api_key")
        except Exception:
            pass
        
        # Method 2: Try alternative access methods
        if not api_key:
            try:
                import os
                # Try environment variable as fallback
                api_key = os.getenv("DEEPSEEK_API_KEY")
            except Exception:
                pass
        
        # Method 3: Fallback to working API key for immediate functionality
        if not api_key:
            api_key = "sk-0f8f14e071d34831aabf892ea372de2f"
        
        # Validate API key
        if api_key and api_key.startswith("sk-") and len(api_key) > 20:
            return EnhancedAIAssistant(api_key)
        else:
            return None
            
    except Exception as e:
        return None
