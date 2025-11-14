import re

class SafetyMonitor:
    def __init__(self):
        self.crisis_keywords = {
            "high_risk": [
                "suicide", "kill myself", "end my life", "want to die",
                "don't want to live", "better off dead"
            ],
            "medium_risk": [
                "can't go on", "hopeless", "no point", "give up",
                "nothing matters", "can't take it"
            ]
        }
        
        self.emergency_contacts = {
            "us": "988 (Suicide & Crisis Lifeline)",
            "uk": "116 123 (Samaritans)", 
            "ca": "1-833-456-4566 (Canada Crisis Services)"
        }
    
    def assess_risk_level(self, user_message: str) -> str:
        """Assess risk level from user message"""
        message_lower = user_message.lower()
        
        for keyword in self.crisis_keywords["high_risk"]:
            if keyword in message_lower:
                return "high_risk"
        
        for keyword in self.crisis_keywords["medium_risk"]:
            if keyword in message_lower:
                return "medium_risk"
        
        return "low_risk"
    
    def get_crisis_response(self, risk_level: str) -> str:
        """Get appropriate crisis response"""
        if risk_level == "high_risk":
            return """
            🚨 **I'm deeply concerned about your safety.**

            **Please contact emergency services immediately:**
            • Call 988 (Suicide & Crisis Lifeline)
            • Text HOME to 741741 (Crisis Text Line)
            • Go to your nearest emergency room

            You deserve support from trained professionals right now.
            """
        
        elif risk_level == "medium_risk":
            return """
            🤗 **It sounds like you're going through an incredibly difficult time.**

            **Please consider reaching out to:**
            • A trusted friend or family member
            • A mental health professional
            • A support group in your community

            Would you like help finding local mental health resources?
            """
        
        return None