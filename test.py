import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

# Dosya yolu
file_path = r'C:\Users\osman\Music\Y2meta.app - Farazi (Remastered) (128 kbps).waw'

# Ses dosyasını yükleme (Orijinal Örnekleme Oranı ile)
y, sr = librosa.load(file_path, sr=None)
print(f"Orijinal Örnekleme Oranı: {sr} Hz")

# Yeni örnekleme oranı belirleme ve yeniden örnekleme
new_sr = 16000  # Yeni örnekleme oranı (ör. 16kHz)
y_resampled = librosa.resample(y, orig_sr=sr, target_sr=new_sr)
print(f"Yeni Örnekleme Oranı: {new_sr} Hz")

# Gürültü azaltma (Basit yöntem: sessiz bölgeleri temizleme)
y_denoised = librosa.effects.trim(y_resampled, top_db=20)[0]  # Sessizliği kırp

# Normalizasyon (Amplitüd değerlerini -1 ile 1 arasında ölçekleme)
y_normalized = librosa.util.normalize(y_denoised)

# İşlenmiş sesin kaydedilmesi
output_path = r'C:\Users\osman\Music\Processed_Audio.wav'
sf.write(output_path, y_normalized, new_sr)
print(f"İşlenmiş ses kaydedildi: {output_path}")

# Dalga formu grafiği
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y_normalized, sr=new_sr)
plt.title("Normalleştirilmiş ve Gürültüsü Azaltılmış Dalga Formu")
plt.xlabel("Zaman (s)")
plt.ylabel("Genlik")
plt.show()

# Spektrogram
plt.figure(figsize=(10, 6))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y_normalized)), ref=np.max)
librosa.display.specshow(D, sr=new_sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title("Spektrogram (Log Frekans)")
plt.show()

# Histogram
plt.figure(figsize=(8, 5))
plt.hist(y_normalized, bins=50, color="c", edgecolor="k")
plt.title("Normalleştirilmiş Ses Amplitüd Histogramı")
plt.xlabel("Amplitüd")
plt.ylabel("Frekans")
plt.show()
