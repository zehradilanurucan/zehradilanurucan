import pandas as pd
import os
#yapay zeka ile yapıldı
#belirli bir kelimeyi içeren bütün satırları siliyor


# 🔧 Ayarlar
klasor_yolu = "satırlı"  # Excel dosyalarının bulunduğu klasör
aranan_kelime = "Yerl."  # Silinmesini istediğin kelime
yeni_klasor = "temizlenmis"  # Temizlenmiş dosyaların kaydedileceği klasör

# 📁 Çıktı klasörü oluştur (varsa atla)
os.makedirs(yeni_klasor, exist_ok=True)

# 📂 Klasördeki tüm dosyaları gez
for dosya in os.listdir(klasor_yolu):
    if dosya.endswith(".xlsx") or dosya.endswith(".xls"):
        dosya_yolu = os.path.join(klasor_yolu, dosya)

        try:
            # Excel dosyasını oku
            df = pd.read_excel(dosya_yolu)

            # Kelimeyi içeren satırları sil (tüm sütunlarda arar)
            df_temiz = df[
                ~df.apply(lambda row: row.astype(str).str.contains(aranan_kelime, case=False, na=False).any(), axis=1)]

            # Yeni dosya yolunu oluştur
            yeni_dosya_yolu = os.path.join(yeni_klasor, dosya)

            # Temizlenmiş dosyayı kaydet
            df_temiz.to_excel(yeni_dosya_yolu, index=False)

            print(f"{dosya} başarıyla temizlendi ve kaydedildi.")

        except Exception as e:
            print(f"{dosya} işlenirken hata oluştu: {e}")
