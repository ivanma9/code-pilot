import logging
from groq import Groq
import os
from dotenv import load_dotenv
import json

logger = logging.getLogger(__name__)

# Load .env file from the project root directory
load_dotenv()

class AIService:
    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY") or logger.error("GROQ_API_KEY not found in environment variables"),
        )
    
    def generate_suggestions(self, text: str, context: str, language: str) -> list:
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful programming assistant. 
                        Your responses must be in the following JSON format:
This is an example for the output format for the this example text and context:
example 
----------------------------
text: 
---
while (i <= 
---

context:
---
n = len(arr)
int i = 0;
while (i <=
---
{
    "suggestions": [
        {"text": "while(i <= n) {\n print(arr[i]) \n i++ \n}"},
        {"text": "for(i = 0; i < n; i++) {\n print(arr[i]) \n}"},
        {"text": "while(i <= n)"}
    ]
}
----------------------------
    Rules:
    Please provide suggestions that are relevant to the code and context.
    Please only provide the suggested, revised code change, NOT the explanation. 
    Please provide up to 3 suggestions.
    Please provide suggestions in the given language of the code.
    """
                    },
                    {
                        "role": "user",
                        "content": f"Context: {context}\nCode: {text}\nProvide suggestions for this code in the language of the code {language}. Make sure the suggestions are returned inorder of most relevant to least relevant. Let's think this through step by step."
                    }
                ],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.7,
                max_tokens=1000,
                response_format={ "type": "json_object" }
            )
            
            # Extract the content and parse it as JSON
            response_content = completion.choices[0].message.content
            try:
                parsed_response = json.loads(response_content)
                suggestions = parsed_response.get('suggestions', [])
                # Return the suggestions in the explicit format
                return {"suggestions": suggestions}
            except json.JSONDecodeError:
                logger.error(f"[{__name__}] Failed to parse JSON response: {response_content}")
                return {"suggestions": []}
            
        except Exception as e:
            logger.error(f"[{__name__}] Error generating AI suggestions: {str(e)}")
            return {"suggestions": []} 