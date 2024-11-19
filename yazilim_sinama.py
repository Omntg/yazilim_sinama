import librosa
import librosa.display
import matplotlib.pyplot as plt

# Ses dosyasını yükle
file_path = r'C:\Users\osman\Music\Y2meta.app - Farazi - (Bir) Fotoğrafın Rüyası (Remastered) (128 kbps).waw'
y, sr = librosa.load(file_path, sr=None)

# Dalga formu grafiği
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Dalga Formu')
plt.xlabel('Zaman (s)')
plt.ylabel('Genlik')
plt.show()

import numpy as np

# Spektrogram
plt.figure(figsize=(10, 6))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spektrogram (Log Frekans)')
plt.show()

# Histogram
plt.figure(figsize=(8, 5))
plt.hist(y, bins=50, color='c', edgecolor='k')
plt.title('Ses Amplitüd Histogramı')
plt.xlabel('Amplitüd')
plt.ylabel('Frekans')
plt.show()
