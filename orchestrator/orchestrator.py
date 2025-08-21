# orchestrator.py
from fastapi import FastAPI, Body, HTTPException
import json
# استيراد الخبراء الذين أنشأناهم
from ai_agents import SummarizerAgent, MindmapAgent, QAAgent, VideoScriptAgent, WhiteboardScriptAgent

app = FastAPI(title="العقل المفكر المتقدم (مدير الخبراء)")

# --- تهيئة الخبراء (إنشاء نسخة من كل خبير) ---
summarizer = SummarizerAgent()
mindmapper = MindmapAgent()
qa_generator = QAAgent()
video_scripter = VideoScriptAgent()
whiteboard_scripter = WhiteboardScriptAgent()

@app.post("/orchestrate/")
async def orchestrate(payload: dict = Body(...)):
    try:
        structured_content = payload['content']
        final_lesson = []

        for page in structured_content:
            page_output = {"page_number": page['page_number'], "elements": []}
            for element in page['content']:
                # نعالج فقط النصوص التي تزيد عن 150 حرف لنتجنب العناوين القصيرة
                if element['type'] == 'full_text' and len(element['data'].strip()) > 150:
                    text = element['data']
                    print(f"\n>>> Processing text from page {page['page_number']}...")
                    
                    # المدير يوزع العمل على الخبراء
                    summary = summarizer.run(text)
                    mindmap = mindmapper.run(text)
                    qa_pairs = qa_generator.run(text)
                    video_script = video_scripter.run(text)
                    whiteboard_script = whiteboard_scripter.run(text)
                    
                    # المدير يجمع النتائج في تقرير واحد
                    page_output['elements'].append({"type": "summary", "data": summary})
                    if mindmap.get("nodes"): # نتأكد أن الخريطة ليست فارغة
                        page_output['elements'].append({"type": "mindmap", "data": mindmap})
                    if qa_pairs:
                        page_output['elements'].append({"type": "q&a", "data": qa_pairs})
                    
                    page_output['elements'].append({"type": "video_script", "data": video_script})
                    page_output['elements'].append({"type": "whiteboard_script", "data": whiteboard_script})

                else:
                    # النصوص القصيرة والصور تضاف كما هي
                    page_output['elements'].append(element)
            
            final_lesson.append(page_output)

        with open("final_interactive_lesson.json", 'w', encoding='utf-8') as f:
            json.dump(final_lesson, f, ensure_ascii=False, indent=4)
            
        return {"message": "تم إنشاء الدرس التفاعلي المتقدم بنجاح!", "data": final_lesson}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))