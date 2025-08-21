# ai_services.py
import os
from dotenv import load_dotenv
import openai
import google.generativeai as genai
import anthropic

# تحميل مفاتيح API من ملف .env
load_dotenv()

# --- إعدادات العملاء ---
# تأكد من أن مفاتيحك موجودة في ملف .env
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# --- دوال التغليف ---

def call_openai(prompt: str) -> str:
    """
    دالة مغلفة لاستدعاء نماذج OpenAI (ChatGPT).
    """
    print("--> Calling OpenAI API...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # يمكنك تغييره إلى gpt-4o
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "Error from OpenAI"

def call_gemini(prompt: str) -> str:
    """
    دالة مغلفة لاستدعاء نماذج Google (Gemini).
    """
    print("--> Calling Gemini API...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return "Error from Gemini"

def call_claude(prompt: str) -> str:
    """
    دالة مغلفة لاستدعاء نماذج Anthropic (Claude).
    """
    print("--> Calling Claude API...")
    try:
        message = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229", # يمكنك تغييره إلى Opus
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return "Error from Claude"