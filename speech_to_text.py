import speech_recognition as sr

def speech_to_text():
    # Recognizer ve mikrofon nesnesi oluştur
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mikrofon hazır, konuşmaya başlayabilirsiniz...")
        try:
            # Kullanıcıdan ses al
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Ses işleniyor, lütfen bekleyin...")
            # Google Speech API ile konuşmayı metne dönüştür
            text = recognizer.recognize_google(audio_data, language="tr-TR")
            print(f"Tanınan Metin: {text}")
            
            # Kelime sayısını hesapla
            word_count = len(text.split())
            print(f"Metindeki Kelime Sayısı: {word_count}")
            
            return text, word_count
        except sr.UnknownValueError:
            print("Ses anlaşılamadı, tekrar deneyin.")
            return None, 0
        except sr.RequestError:
            print("Google API'ye ulaşılamadı. İnternet bağlantınızı kontrol edin.")
            return None, 0
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return None, 0

if __name__ == "__main__":
    result, word_count = speech_to_text()
    if result:
        print(f"Sonuç: {result}")
        print(f"Kelime Sayısı: {word_count}")
    else:
        print("Metin dönüştürülemedi.")
