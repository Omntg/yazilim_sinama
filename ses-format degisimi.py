from pydub import AudioSegment

# Orijinal ses dosyasını yükle
audio = AudioSegment.from_file("ornek_ses_dosyasi.wav")

# Mono ve 16 kHz formatına dönüştür
audio = audio.set_channels(1).set_frame_rate(16000)

# Yeni dosyayı kaydet
audio.export("ornek_ses_dosyasi_mono.wav", format="wav")
print("Dosya başarıyla dönüştürüldü: ornek_ses_dosyasi_mono.wav")

