import os
import base64
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.cloud import translate_v2 as translate
from google.cloud import language_v1

# Google Cloud Servis Hesabı JSON dosyasını ayarla
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Yetkilendirme belirteci oluşturma
def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())
    return credentials.token

# 1. Uzun süreli ses tanıma için işlev
def transcribe_long_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_content = audio_file.read()
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')

    url = "https://speech.googleapis.com/v1p1beta1/speech:longrunningrecognize"

    data = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "tr-TR"
        },
        "audio": {
            "content": audio_base64
        }
    }

    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        operation = response.json()
        operation_name = operation['name']
        print(f"İşlem Başlatıldı, Operation ID: {operation_name}")
        return operation_name
    else:
        print("Hata oluştu:", response.text)
        return None

# 2. İşlemi kontrol etme ve sonucu alma
def get_transcription_result(operation_name):
    url = f"https://speech.googleapis.com/v1/operations/{operation_name}"

    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("done"):
                if "response" in result:
                    transcription = " ".join(
                        res['alternatives'][0]['transcript']
                        for res in result['response'].get('results', [])
                    )
                    print("Tanınan metin:", transcription)
                    return transcription
                else:
                    print("Sonuç bulunamadı.")
                    return None
        else:
            print("Hata oluştu:", response.text)
            return None

# 3. Metni İngilizceye çevirme
def translate_to_english(text):
    try:
        translate_client = translate.Client()
        translation = translate_client.translate(text, target_language="en")
        print("\nÇevrilen Metin:", translation['translatedText'])
        return translation['translatedText']
    except Exception as e:
        print("Çeviri sırasında bir hata oluştu:", e)
        return None

# 4. İngilizce metin üzerinde konu analizi
def analyze_text(text):
    try:
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_entities(document=document)

        print("\n*** Metin Analizi Sonuçları ***")
        for entity in response.entities:
            print(f"Entity: {entity.name}")
            print(f"Type: {language_v1.Entity.Type(entity.type_).name}")
            print(f"Salience (Önem): {entity.salience:.2f}")
            print("-" * 30)

        return response.entities
    except Exception as e:
        print("Analiz sırasında bir hata oluştu:", e)
        return None

# Nihai İşlem
if __name__ == "__main__":
    audio_path = "ornek_ses_dosyasi_mono.wav"
    operation_name = transcribe_long_audio(audio_path)

    if operation_name:
        transcription = get_transcription_result(operation_name)

        if transcription:
            translated_text = translate_to_english(transcription)

            if translated_text:
                analyze_text(translated_text)







