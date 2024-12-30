from transformers import pipeline

# Türkçe metin analizi için fonksiyon
def turkish_emotion_analysis(text):
    # Hugging Face Türkçe duygu analizi modeli
    emotion_model = pipeline("text-classification", model="savasy/bert-base-turkish-sentiment-cased")
    
    # Tahmin edilen duygu sonuçlarını al (ilk 3 sonucu döndürüyoruz)
    results = emotion_model(text, top_k=3)
    
    # Sonuçları yüzdelik olarak dönüştür
    emotions = {res['label']: res['score'] for res in results}
    total_score = sum(emotions.values())
    emotions_percentage = {emotion: round(score / total_score * 100, 2) for emotion, score in emotions.items()}
    
    return emotions_percentage

# Örnek kullanım
if __name__ == "__main__":
    text = "Bugün hava çok güzel ama kendimi biraz kararsiz hissediyorum."
    emotion_results = turkish_emotion_analysis(text)
    
    # Sonuçları ekrana yazdır
    print("Türkçe Metin Analizi Sonucu:")
    for emotion, percentage in emotion_results.items():
        print(f"{emotion.capitalize()}: %{percentage}")
