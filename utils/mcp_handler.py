import openai
import os
import json
from typing import Dict, List, Optional, Callable

class MCPHandler:
    """Model Context Protocol - Manages context and LLM interactions with tool calling"""
    
    def __init__(self, api_key: str, web_search_tool: Optional[Callable] = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.conversation_context = []
        self.web_search_tool = web_search_tool  # Reference to web search function
    
    def build_context_prompt(self, user_message: str, rag_context: List[Dict], risk_level: str) -> str:
        """Build comprehensive context for LLM"""
        
        # Start with safety guidelines
        prompt = """
        You are a compassionate mental health companion. Your role is to provide emotional support, CBT-inspired reflections, and general wellness guidance.

        CRITICAL SAFETY RULES:
        1. NEVER provide medical or psychological diagnoses
        2. NEVER suggest specific treatments or medications
        3. ALWAYS encourage professional help for serious concerns
        4. Focus on active listening, validation, and general coping strategies
        5. For crisis situations, provide emergency resources immediately

        """
        
        # Add RAG context
        if rag_context:
            prompt += "\nRELEVANT SUPPORT TECHNIQUES:\n"
            for context in rag_context:
                prompt += f"- {context['content']}\n"
        
        # Add risk context
        if risk_level != "low_risk":
            prompt += f"\nRISK LEVEL: {risk_level.upper()} - Prioritize safety and resource provision\n"
        
        # Add conversation context (last 3 exchanges)
        if self.conversation_context:
            prompt += "\nRECENT CONVERSATION CONTEXT:\n"
            for exchange in self.conversation_context[-3:]:
                prompt += f"User: {exchange['user']}\n"
                prompt += f"You: {exchange['assistant']}\n"
        
        prompt += f"\nCurrent User Message: {user_message}\n"
        prompt += "\nYour compassionate, supportive response:"
        
        return prompt
    
    def generate_response(self, user_message: str, rag_context: List[Dict], risk_level: str) -> str:
        """Generate LLM response with proper context"""
        
        prompt = self.build_context_prompt(user_message, rag_context, risk_level)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                   {"role": "system", "content": "You are a supportive, empathetic mental health companion."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Update conversation context
            self.conversation_context.append({
                "user": user_message,
                "assistant": ai_response
            })
            
            # Keep only last 5 exchanges to manage context length
            if len(self.conversation_context) > 5:
                self.conversation_context = self.conversation_context[-5:]
            
            return ai_response
            
        except Exception as e:
            return f"I'm here to listen. It seems I'm having some technical difficulties. How are you feeling right now?"
    
    def get_tool_definitions(self) -> List[Dict]:
        """Define tools/functions that LLM can use"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_mental_health_web",
                    "description": "Search the web for recent mental health information, latest research, current news, or real-time data about mental health topics. Use this when the user asks about recent developments, latest studies, current trends, or needs up-to-date mental health information that may not be in your knowledge base.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query for mental health information. Should be specific and include relevant mental health keywords."
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of search results to return (default: 3)",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    def generate_response_with_tools(self, user_message: str, rag_context: List[Dict], risk_level: str) -> str:
        """Generate LLM response with tool calling capability"""
        
        # Build system message with safety guidelines
        system_message = """You are a compassionate mental health companion. Your role is to provide emotional support, CBT-inspired reflections, and general wellness guidance.

CRITICAL SAFETY RULES:
1. NEVER provide medical or psychological diagnoses
2. NEVER suggest specific treatments or medications
3. ALWAYS encourage professional help for serious concerns
4. Focus on active listening, validation, and general coping strategies
5. For crisis situations, provide emergency resources immediately

You have access to a web search tool to find recent mental health information when needed. Use it when users ask about:
- Latest research or studies
- Recent news or developments
- Current trends or statistics
- Up-to-date information not in your training data

For general emotional support or known information, respond directly without using tools.
"""
        
        # Build user message with RAG context
        user_prompt = ""
        if rag_context:
            user_prompt += "RELEVANT MENTAL HEALTH KNOWLEDGE BASE:\n"
            for context in rag_context:
                user_prompt += f"- {context['content']}\n"
            user_prompt += "\n"
        
        if risk_level != "low_risk":
            user_prompt += f" RISK LEVEL: {risk_level.upper()} - Prioritize safety and resource provision\n\n"
        
        if self.conversation_context:
            user_prompt += "RECENT CONVERSATION:\n"
            for exchange in self.conversation_context[-3:]:
                user_prompt += f"User: {exchange['user']}\nYou: {exchange['assistant']}\n"
            user_prompt += "\n"
        
        user_prompt += f"Current User Message: {user_message}"
        
        # Prepare messages for LLM
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            # First LLM call with tool definitions
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.get_tool_definitions(),
                tool_choice="auto",  # Let LLM decide when to use tools
                temperature=0.7,
                max_tokens=500
            )
            
            response_message = response.choices[0].message
            
            # Check if LLM wants to use a tool
            if response_message.tool_calls:
                print(f"🔧 LLM decided to use tool: {response_message.tool_calls[0].function.name}")
                
                # Add assistant's tool call to messages
                messages.append(response_message)
                
                # Execute each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "search_mental_health_web":
                        if self.web_search_tool:
                            print(f"🔍 Executing web search: {function_args.get('query', '')[:50]}...")
                            
                            # Execute web search
                            search_results = self.web_search_tool(
                                query=function_args.get("query"),
                                max_results=function_args.get("max_results", 3)
                            )
                            
                            # Format results for LLM
                            tool_response = self._format_search_results(search_results)
                            
                            # Add tool response to messages
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": function_name,
                                "content": tool_response
                            })
                        else:
                            # No web search tool available
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": function_name,
                                "content": "Web search tool is not available. Please provide a response based on your existing knowledge."
                            })
                
                # Second LLM call with tool results
                print(" LLM processing search results and generating final response...")
                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                ai_response = final_response.choices[0].message.content.strip()
            else:
                # No tool calls, use direct response
                print(" LLM responding directly without tools")
                ai_response = response_message.content.strip()
            
            # Update conversation context
            self.conversation_context.append({
                "user": user_message,
                "assistant": ai_response
            })
            
            # Keep only last 5 exchanges
            if len(self.conversation_context) > 5:
                self.conversation_context = self.conversation_context[-5:]
            
            return ai_response
            
        except Exception as e:
            print(f" Error in generate_response_with_tools: {e}")
            return "I'm here to listen. It seems I'm having some technical difficulties. How are you feeling right now?"
    
    def _format_search_results(self, search_results: List[Dict]) -> str:
        """Format search results for LLM consumption"""
        if not search_results:
            return "No recent information found. Please provide a response based on your existing knowledge."
        
        formatted = "WEB SEARCH RESULTS:\n\n"
        for i, result in enumerate(search_results, 1):
            content = result.get('content', '')
            metadata = result.get('metadata', {})
            source = metadata.get('source', 'Unknown')
            
            formatted += f"Result {i}:\n"
            formatted += f"Content: {content}\n"
            formatted += f"Source: {source}\n\n"
        
        formatted += "\nPlease analyze these search results and provide a helpful, empathetic response to the user's question, incorporating relevant information from the search results."
        return formatted
    
