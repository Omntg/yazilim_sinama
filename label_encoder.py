from sklearn.preprocessing import LabelEncoder
import joblib

# Etiketleri dönüştürme
y = ['baris', 'mhoca', 'ugur']  # Etiketlerinizin listesi

# LabelEncoder'ı eğitin
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# LabelEncoder'ı kaydedin
joblib.dump(le, r"C:\Users\osman\.vscode\extensions\ms-python.python-2024.16.1-win32-x64\python_files\Yeni klasör\label_encoder.pkl")

print("LabelEncoder kaydedildi.")
