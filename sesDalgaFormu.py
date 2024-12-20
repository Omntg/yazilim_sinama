import librosa
import librosa.display
import matplotlib.pyplot as plt

# Ses dosyasını yükle
audio_path = "ornek_ses_dosyasi_mono.wav"  # Proje klasörüne eklemen gerek
audio, sr = librosa.load(audio_path)

# Ses dalgasını çizdir
plt.figure(figsize=(10, 4))
librosa.display.waveshow(audio, sr=sr)
plt.title("Ses Dalga Formu")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Genlik")
plt.show()



