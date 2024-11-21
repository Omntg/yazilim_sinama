"""import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Gerekli dil modellerini indir
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# Örnek metin
metin = "Bugün futbol oynadım ve çok eğlendim!"

# Kelimeleri küçük harfe çevirip tokenize et
kelimeler = word_tokenize(metin.lower())

# Türkçe stopwords listesine göre filtreleme
nltk.download('stopwords')
stop_words = stopwords.words('turkish')  # Türkçe durdurma kelimeleri
temiz_kelimeler = [kelime for kelime in kelimeler if kelime not in stop_words]

print(temiz_kelimeler)"""
import requests
from bs4 import BeautifulSoup

# Hedef URL
url = "https://www.ntvspor.net/"  # Gerçek URL'yi buraya girin

# Sayfayı çekme
response = requests.get(url)

# Sayfa başarılı bir şekilde çekildi mi kontrol et
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Başlıkları toplama (a etiketinde ve doğru sınıfta arama)
    basliklar = []
    for baslik in soup.find_all('a', class_="text-elipsis-3 card-text-link"):  # Doğru sınıf adını kullanıyoruz
        basliklar.append(baslik.text.strip())  # .strip() boşlukları temizler

    # Eğer başlıklar varsa, bunları yazdır
    if basliklar:
        print("Futbol Haber Başlıkları:")
        for baslik in basliklar:
            print("-", baslik)
    else:
        print("Başlıklar bulunamadı.")
else:
    print(f"Sayfa yüklenemedi. HTTP durumu: {response.status_code}")




