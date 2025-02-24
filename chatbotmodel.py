"""
Chatbot module for handling medical conversations using LLMs.
"""
from typing import Dict, Any, Optional
import requests
from .config import LLM_MODEL, LLM_API_KEY, AVAILABLE_MODELS
from .utils import logger

class MedicalChatbot:
    def __init__(self):
        self.model = LLM_MODEL
        self.api_key = LLM_API_KEY
        self.model_config = AVAILABLE_MODELS.get(self.model, AVAILABLE_MODELS['gpt-4'])
        
        # Medical context prompt to guide the LLM
        self.system_prompt = """
        You are a medical assistant chatbot. Your role is to:
        1. Help users understand their symptoms and potential health risks
        2. Provide general health information and recommendations
        3. Suggest when to seek professional medical help
        
        Important guidelines:
        - Always clarify that you're an AI assistant, not a doctor
        - Recommend consulting healthcare professionals for specific medical advice
        - Focus on general health information and preventive measures
        - Be clear about limitations and uncertainties
        - Use simple, clear language to explain medical concepts
        """

    def format_prompt(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Format the prompt with user input and any available context."""
        prompt = f"{self.system_prompt}\n\nUser Query: {user_input}\n"
        
        if context:
            # Add relevant health metrics if available
            health_metrics = context.get('health_metrics', {})
            if health_metrics:
                prompt += "\nRelevant Health Information:\n"
                for metric, value in health_metrics.items():
                    prompt += f"- {metric}: {value}\n"
            
            # Add any previous medical history
            medical_history = context.get('medical_history', [])
            if medical_history:
                prompt += "\nRelevant Medical History:\n"
                for item in medical_history:
                    prompt += f"- {item}\n"
        
        prompt += "\nPlease provide a helpful response based on this information:"
        return prompt

    async def call_openai(self, prompt: str) -> str:
        """Make API call to OpenAI's GPT-4."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.model_config['temperature'],
                "max_tokens": self.model_config['max_tokens']
            }
            
            response = requests.post(
                f"{self.model_config['api_base']}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return "I apologize, but I'm having trouble processing your request. Please try again later."
                
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again later."

    async def call_medpalm(self, prompt: str) -> str:
        """Make API call to Google's MedPaLM 2."""
        # Note: This is a placeholder. Actual implementation would depend on Google's API
        try:
            # Simulate MedPaLM 2 call
            return "MedPaLM 2 integration coming soon. Using fallback response."
        except Exception as e:
            logger.error(f"Error calling MedPaLM API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again later."

    async def call_biogpt(self, prompt: str) -> str:
        """Make API call to Microsoft's BioGPT."""
        # Note: This is a placeholder. Actual implementation would depend on Microsoft's API
        try:
            # Simulate BioGPT call
            return "BioGPT integration coming soon. Using fallback response."
        except Exception as e:
            logger.error(f"Error calling BioGPT API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again later."

    async def get_response(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user input and return a response using the selected LLM.
        """
        try:
            # Format the prompt with user input and context
            prompt = self.format_prompt(user_input, context)
            
            # Call appropriate LLM based on configuration
            if self.model == 'gpt-4':
                response = await self.call_openai(prompt)
            elif self.model == 'medpalm-2':
                response = await self.call_medpalm(prompt)
            elif self.model == 'biogpt':
                response = await self.call_biogpt(prompt)
            else:
                response = await self.call_openai(prompt)  # Default to GPT-4
            
            return {
                "response": response,
                "model_used": self.model
            }
            
        except Exception as e:
            logger.error(f"Error getting chatbot response: {str(e)}")
            return {
                "error": "I apologize, but I'm having trouble processing your request. Please try again later.",
                "model_used": self.model
            }

# Initialize the chatbot
medical_chatbot = MedicalChatbot()
