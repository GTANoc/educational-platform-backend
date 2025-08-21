# ai_agents.py
import json
from ai_services import call_claude, call_gemini, call_openai

class SummarizerAgent:
    def run(self, text_chunk: str) -> str:
        print("--- Summarizer Agent at work ---")
        prompt = f"لخص النص التالي من كتاب مدرسي في جملتين بحد أقصى، مع الحفاظ على المفهوم العلمي الأساسي:\n\n{text_chunk}"
        # Claude ممتاز في الملخصات الدقيقة
        return call_claude(prompt)

class MindmapAgent:
    def run(self, text_chunk: str) -> dict:
        print("--- Mindmap Agent at work ---")
        prompt = f"""
        حول النص التالي إلى بيانات JSON صالحة لخريطة ذهنية.
        يجب أن يحتوي الـ JSON على قائمة 'nodes' وقائمة 'edges'.
        اجعل العناوين (labels) في العقد قصيرة جدًا وواضحة (كلمة أو كلمتين).
        النص: "{text_chunk}"
        """
        # Gemini قوي في توليد JSON المنظم
        response_str = call_gemini(prompt)
        try:
            json_str = response_str.strip().replace("```json", "").replace("```", "")
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("!!! Mindmap Agent failed to decode JSON.")
            return {}

class QAAgent:
    def run(self, text_chunk: str) -> list:
        print("--- Q&A Agent at work ---")
        prompt = f"""
        استخرج سؤالين مهمين مع إجاباتهما من النص التالي.
        أريد النتيجة بصيغة JSON تحتوي على قائمة، كل عنصر فيها هو object به 'question' و 'answer'.
        يجب أن تكون الأسئلة والإجابات باللغة العربية.
        النص: "{text_chunk}"
        """
        # ChatGPT جيد في فهم الأسئلة
        response_str = call_openai(prompt)
        try:
            json_str = response_str.strip().replace("```json", "").replace("```", "")
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("!!! Q&A Agent failed to decode JSON.")
            return []

class VideoScriptAgent:
    def run(self, text_chunk: str) -> str:
        print("--- Video Script Agent at work ---")
        prompt = f"""
        أنت خبير في كتابة سيناريو لفيديو تعليمي قصير (أسلوب Mootion) مدته 30 ثانية.
        اكتب سيناريو جذابًا ومفصلاً للنص التالي، مع وصف دقيق للمشاهد، وحركة الكاميرا، والمؤثرات الصوتية والبصرية.
        اجعل اللغة بسيطة ومناسبة لطلاب المرحلة الابتدائية.
        النص: "{text_chunk}"
        """
        # Claude جيد في الكتابة الإبداعية
        return call_claude(prompt)

class WhiteboardScriptAgent:
    def run(self, text_chunk: str) -> str:
        print("--- Whiteboard Script Agent at work ---")
        prompt = f"""
        أنت خبير في كتابة سيناريو لفيديو سبورة بيضاء (أسلوب Viewscriber).
        اكتب سيناريو خطوة بخطوة لشرح النص التالي. صف حركة اليد وهي ترسم كل شكل وتكتب كل كلمة.
        يجب أن يكون الشرح مبسطًا وواضحًا.
        النص: "{text_chunk}"
        """
        # ChatGPT جيد في الشرح المنظم
        return call_openai(prompt)