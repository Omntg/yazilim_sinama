import librosa
import numpy as np
import joblib

# Modelin yolu
model_yolu = r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\mlp_model.pkl"

# Modeli yükleyin
model = joblib.load(model_yolu)

# Ses dosyasının yolu (örneğin, 'test_audio.wav')
ses_dosyasi_yolu = r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\mikrofon_tahmin\mh.wav"

# Ses dosyasını yükleyin
ses, sr = librosa.load(ses_dosyasi_yolu, sr=None)

# MFCC özelliklerini çıkarın
n_mfcc = 128  # MFCC sayısı
frame_length = 25  # milisaniye cinsinden
frame_stride = 10  # milisaniye cinsinden

# MFCC hesaplama
mfcc = librosa.feature.mfcc(y=ses, sr=sr, n_mfcc=n_mfcc, hop_length=int(frame_stride * sr / 1000),
                             n_fft=int(frame_length * sr / 1000))

# Özelliklerin ortalamasını alın
mfcc_ortalama = np.mean(mfcc, axis=1)

# Modelin tahmin yapabilmesi için veriyi şekillendirin
X_input = np.array([mfcc_ortalama])

# Tahmin yapın
tahmin = model.predict(X_input)

# LabelEncoder'ı yükleyin
le = joblib.load(r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\label_encoder.pkl")

# Tahmin edilen kişi
tahmin_etiketi = le.inverse_transform(tahmin)
print(f"Tahmin edilen kişi: {tahmin_etiketi[0]}")
