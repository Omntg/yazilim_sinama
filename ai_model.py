import os
from pydub import AudioSegment
import librosa
import librosa.feature
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib


# MP3'ten WAV'a dönüştürme ve parçalara bölme
mp3_dir = r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\baris-mhoca-ugur-mp3"
wav_dir = r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\baris-mhoca-ugur-wav"

if not os.path.exists(wav_dir):
    os.makedirs(wav_dir)

# MP3 dosyalarını dönüştür ve 3 saniyelik parçalara böl
print("MP3 dosyaları WAV formatına dönüştürülüyor ve parçalara bölünüyor...")
for mp3_file in os.listdir(mp3_dir):
    if mp3_file.endswith(".mp3"):
        audio = AudioSegment.from_mp3(os.path.join(mp3_dir, mp3_file))
        chunk_length_ms = 3000  # 3 saniye 

        # Ses dosyasını 1.5 saniyelik parçalara böl
        for i, chunk in enumerate(audio[::chunk_length_ms]):
            parca_dosya_adı = f"{mp3_file[:-4]}_parca{i}.wav"
            chunk.export(os.path.join(wav_dir, parca_dosya_adı), format="wav")

print("Dönüştürme ve bölme işlemi tamamlandı.")

# MFCC, Delta, Delta-Delta ve FM özelliklerini çıkarma
mfcc_dir = r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\baris-mhoca-ugur-mfcc"
if not os.path.exists(mfcc_dir):
    os.makedirs(mfcc_dir)

print("MFCC, Delta, Delta-Delta ve FM özellikleri çıkarılıyor...")
n_mfcc = 13  # MFCC vektör sayısı
for wav_file in os.listdir(wav_dir):
    if wav_file.endswith(".wav"):
        dosya_yolu = os.path.join(wav_dir, wav_file)
        ses, sr = librosa.load(dosya_yolu, sr=None)

        # MFCC ve türevlerini çıkar
        mfcc = librosa.feature.mfcc(y=ses, sr=sr, n_mfcc=n_mfcc)
        delta_mfcc = librosa.feature.delta(mfcc)
        delta2_mfcc = librosa.feature.delta(mfcc, order=2)
        fm = np.mean(mfcc, axis=1, keepdims=True)  # FM: Ortalama MFCC değerleri

        # FM'i zaman eksenine göre genişlet
        fm_expanded = np.tile(fm, (1, mfcc.shape[1]))  # FM genişletilmiş: (13, zaman)

        # Özellikleri birleştir
        combined_features = np.vstack((mfcc, delta_mfcc, delta2_mfcc, fm_expanded))

        # Özellikleri .npy formatında kaydet
        npy_dosya_adı = wav_file.replace(".wav", ".npy")
        np.save(os.path.join(mfcc_dir, npy_dosya_adı), combined_features)

print("MFCC, Delta, Delta-Delta ve FM özellikleri başarıyla çıkarıldı.")


# 3. Model Eğitimi
print("Model eğitimi başlatılıyor...")
X = []
y = []

# Özellik dosyalarını yükle
for feature_file in os.listdir(mfcc_dir):
    if feature_file.endswith('.npy'):
        feature_path = os.path.join(mfcc_dir, feature_file)
        features = np.load(feature_path)
        X.append(np.mean(features, axis=1))  # Özellik vektörünü ortalamasını alarak tek boyutlu yap
        y.append(feature_file.split('_')[0])  # Etiket olarak dosya adının başlangıcı kullanılır

X = np.array(X)
y = np.array(y)

# Etiketleri sayısallaştır
le = LabelEncoder()
y = le.fit_transform(y)

# Veriyi eğitim ve test kümelerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model oluştur ve eğit
model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
model.fit(X_train, y_train)

# Modelin doğruluğunu değerlendir
accuracy = model.score(X_test, y_test)
print(f"Model doğruluğu: {accuracy:.4f}")

# Modeli kaydet
model_path = r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\mlp_modelv2.pkl"
joblib.dump(model, model_path)
print(f"Model başarıyla kaydedildi: {model_path}\n")

# 4. Performans Değerlendirme
print("Model performansı değerlendiriliyor...")
y_pred = model.predict(X_test)

print("Sınıflandırma Raporu:")
print(classification_report(y_test, y_pred))

print("Karışıklık Matrisi:")
print(confusion_matrix(y_test, y_pred))

