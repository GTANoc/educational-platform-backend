# pdf_parser.py

# --- تثبيت المكتبات المطلوبة ---
# pip install fastapi uvicorn python-multipart "PyMuPDF<1.24.0" pillow openai

import fitz  # PyMuPDF
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
from PIL import Image 
import io

# --- تهيئة التطبيق ---
app = FastAPI(
    title="خدمة استيعاب ومعالجة المحتوى",
    description="تقوم بتحليل ملفات PDF واستخراج النصوص والصور والجداول.",
    version="1.4.0", # تم تحديث الإصدار
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- الدوال الأساسية ---

def process_pdf(file_content: bytes, output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(stream=file_content, filetype="pdf")
    structured_content = []

    print(f"بدء معالجة الملف: {doc.page_count} صفحات.")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_data = {"page_number": page_num + 1, "content": []}

        # 1. استخراج النصوص
        text = page.get_text("text", sort=True)
        if text.strip():
            page_data["content"].append({
                "id": f"text_{uuid.uuid4()}",
                "type": "full_text", 
                "data": text
            })

        # 2. استخراج الصور (الطريقة النهائية - تصوير الصفحة ثم القص)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            try:
                # الحصول على إحداثيات وموقع الصورة داخل الصفحة
                bbox = page.get_image_bbox(img)
                
                # تصوير الصفحة بالكامل بجودة عالية (300 DPI)
                page_pix = page.get_pixmap(dpi=300)
                
                # قص الصورة من الصفحة المصورة باستخدام إحداثياتها
                # يتم ضرب الإحداثيات في معامل الجودة (dpi/72)
                clip_rect = bbox * (300/72)
                
                # إنشاء صورة جديدة فارغة بأبعاد الصورة المقصوصة
                cropped_pix = fitz.Pixmap(fitz.csRGB, clip_rect.irect)
                
                # نسخ بيانات البكسل من صورة الصفحة الكبيرة إلى الصورة الصغيرة المقصوصة
                cropped_pix.copy(page_pix, clip_rect.irect)

                image_bytes = cropped_pix.tobytes("png")
                image_ext = "png"

                descriptive_name = f"image_{img_index}"
                image_filename = f"page{page_num+1}_{descriptive_name}.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                page_data["content"].append({
                    "id": f"image_{uuid.uuid4()}",
                    "type": "image", 
                    "path": image_path, 
                    "ai_description": "وصف سيتم إنشاؤه بواسطة الذكاء الاصطناعي"
                })
            except Exception as e:
                print(f"فشل استخراج الصورة {img_index} في صفحة {page_num + 1}: {e}")

        structured_content.append(page_data)
        print(f"تمت معالجة الصفحة {page_num + 1}")

    doc.close()
    return structured_content

# --- الواجهة البرمجية (API Endpoint) ---

@app.post("/process-pdf/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="الملف يجب أن يكون من نوع PDF.")

    try:
        file_content = await file.read()
        output_folder = "processed_content"
        result = process_pdf(file_content, output_folder)
        
        json_output_path = os.path.join(output_folder, "structured_content.json")
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        return {
            "message": "تمت معالجة الملف بنجاح!",
            "output_json": json_output_path,
            "content": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء المعالجة: {str(e)}")
