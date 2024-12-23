import sounddevice as sd
import librosa
import numpy as np
import joblib

# Sınıf isimlerini tanımla
encoder_path = r"C:\\Users\\osman\\.vscode\\extensions\\ms-python.python-2024.16.1-win32-x64\\python_files\\Yeni klasör\\label_encoder.pkl"
model_path = r"C:\\Users\\osman\\.vscode\\extensions\\ms-python.python-2024.16.1-win32-x64\\python_files\\Yeni klasör\\mlp_modelv2.pkl"

# Model ve encoder'ı yükle
model = joblib.load(model_path)
le = joblib.load(encoder_path)

# Ses kaydı için ayarlar
fs = 44100  # Örnekleme frekansı
sure = 3    # Kayıt süresi (saniye)

print("Ses kaydediliyor...\n")
# Mikrofon ile ses kaydı al
kaydedilen_ses = sd.rec(int(sure * fs), samplerate=fs, channels=1, dtype='float32')
sd.wait()  # Kayıt tamamlanana kadar bekle
print("Ses kaydı tamamlandı!\n")

# Kaydedilen sesi işleme
ses = kaydedilen_ses.flatten()  # 1D array'e dönüştür

# MFCC ve özellik çıkarımı
n_mfcc = 13
mfcc = librosa.feature.mfcc(y=ses, sr=fs, n_mfcc=n_mfcc)
delta_mfcc = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
fm = np.mean(mfcc, axis=1, keepdims=True)
fm_expanded = np.tile(fm, (1, mfcc.shape[1]))

# Özellikleri birleştir
combined_features = np.vstack((mfcc, delta_mfcc, delta2_mfcc, fm_expanded))
X_new = np.mean(combined_features, axis=1).reshape(1, -1)  # Model girişine uygun şekil

# Tahmin yap
etiket = model.predict(X_new)[0]
tahmin = le.inverse_transform([etiket])[0]

# Sonucu yazdır
print(f"Tahmin edilen kişi: {tahmin}")
