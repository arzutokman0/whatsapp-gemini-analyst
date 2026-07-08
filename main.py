import os
import requests
from fastapi import FastAPI, Request, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SISTEM_PROMPTU = (
    "Sen yetenekli bir asistansın. Eğer kullanıcı bir belge veya görsel gönderdiyse, "
    "içeriğini maksimum 3-4 cümleyle, çok kısa, maddeler halinde ve Türkçe olarak özetle. "
    "Asla uzun paragraflar yazma ve Markdown formatlamalarını (**, * vb.) kullanma."
)

@app.post("/webhook")
async def whatsapp_bot(request: Request):
    form_data = await request.form()
    
    Body = form_data.get("Body", "")
    From = form_data.get("From", "")
    MediaUrl0 = form_data.get("MediaUrl0", None)
    ContentType0 = form_data.get("ContentType0", None)
    
    print("\n--- 📥 YENİ İSTEK GELDİ ---")
    print(f"📱 Mesaj: {Body} | Kimden: {From} | Medya Linki: {MediaUrl0}")
    
    icerik_listesi = []
    
    if MediaUrl0:
        try:
            print("⏳ Dosya doğrudan indiriliyor...")
            response = requests.get(MediaUrl0, timeout=15)
            print(f"📊 İndirme Durum Kodu: {response.status_code}")
            
            if response.status_code == 200:
                # --- [AKILLI TÜM SİSTEMİ] ---
                # Dosyanın gerçek içeriğine bakarak türünü tayin ediyoruz
                dosya_baslangici = response.content[:4]
                
                if dosya_baslangici.startswith(b'%PDF'):
                    mime_turu = "application/pdf"
                else:
                    mime_turu = "image/jpeg" # Varsayılan olarak görsel kabul et
                    
                print(f"📂 Gerçek İçerikten Saptanan Dosya Türü: {mime_turu}")
                
                dosya_verisi = types.Part.from_bytes(
                    data=response.content,
                    mime_type=mime_turu
                )
                icerik_listesi.append(dosya_verisi)
                print("✨ Dosya başarıyla hafızaya alındı.")
            else:
                print("❌ Twilio dosya indirmeyi reddetti.")
        except Exception as e:
            print(f"❌ Dosya indirme hatası: {e}")
            
    soru_metni = f"{SISTEM_PROMPTU}\n\nSoru: {Body if Body else 'Bu dosyayı analiz et.'}"
    icerik_listesi.append(soru_metni)
    
    try:
        print("🧠 Gemini'ye gönderiliyor...")
        cevap = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=icerik_listesi
        )
        
        temiz_cevap = cevap.text.replace("**", "").replace("* ", "• ")
        print(f"📝 Yanıt İçeriği: {temiz_cevap}")
        
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(temiz_cevap)
        msg.to = From 
        
        return Response(content=str(resp), media_type="application/xml")
        
    except Exception as e:
        print(f"❌ Gemini Hatası: {e}")
        resp = MessagingResponse()
        resp.message("Üzgünüm, dosyayı okurken bir sorun oluştu. Tekrar dener misin?")
        return Response(content=str(resp), media_type="application/xml")