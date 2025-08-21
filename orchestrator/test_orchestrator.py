# test_orchestrator.py
import requests
import json

ORCHESTRATOR_URL = "http://127.0.0.1:8000/orchestrate/"
INPUT_JSON_FILE = "structured_content.json"

def run_test():
    try:
        with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    except Exception as e:
        print(f"خطأ في قراءة الملف: {e}")
        return

    # نأخذ مجموعة من الصفحات للاختبار السريع (مثلاً من صفحة 26 إلى 35)
    test_payload = {"content": content_data[25:35]} 
    
    print("إرسال 10 صفحات إلى العقل المفكر...")
    try:
        # زيادة مهلة الانتظار لأن العملية قد تستغرق وقتاً طويلاً
        response = requests.post(ORCHESTRATOR_URL, json=test_payload, timeout=300) 
        response.raise_for_status()
        print("✅ نجحت العملية!")
        print("اذهب وتفحص ملف 'final_interactive_lesson.json' الجديد.")
    except requests.exceptions.RequestException as e:
        print(f"❌ فشل الاتصال بالخادم: {e}")

if __name__ == "__main__":
    run_test()