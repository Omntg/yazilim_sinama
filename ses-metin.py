import requests
import base64

# API anahtarınızı buraya yerleştirin
api_key = "AIzaSyDzqCh3rXwyq8CF-eUpOFkuyCLaOPcQPcg"

# Dönüştürülmüş ses dosyasının yolu
audio_path = "ornek_ses_dosyasi_mono.wav"

# Ses dosyasını okuma ve base64 ile encode etme
with open(audio_path, "rb") as audio_file:
    audio_content = audio_file.read()
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')

# API URL
url = f"https://speech.googleapis.com/v1p1beta1/speech:recognize?key={api_key}"

# API'ye gönderilecek veriyi yapılandırın
data = {
    "config": {
        "encoding": "LINEAR16",  # Ses dosyası LINEAR16 formatında olmalı
        "sampleRateHertz": 16000,  # 16 kHz frekansında olmalı
        "languageCode": "tr-TR"  # Türkçe dil ayarı
    },
    "audio": {
        "content": audio_base64  # Base64 formatında ses verisi
    }
}

# API'ye istek gönderme
response = requests.post(url, json=data)

# Cevabı kontrol et ve yazdır
if response.status_code == 200:
    result = response.json()
    if 'results' in result:
        for res in result.get("results", []):
            print("Tanınan metin:", res['alternatives'][0]['transcript'])
    else:
        print("Sonuç bulunamadı.")
else:
    print("Hata oluştu:", response.text)






