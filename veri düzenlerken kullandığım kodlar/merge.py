import pandas as pd
import os
import re

# Excel dosyalarının bulunduğu klasör
klasor_yolu = "veriler"  # ← klasör adını gerektiği şekilde değiştir

tum_veriler = []

for dosya_adi in os.listdir(klasor_yolu):
    if dosya_adi.endswith(".xlsx") or dosya_adi.endswith(".xls"):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
        df = pd.read_excel(dosya_yolu)

        # ---- Yıl Bilgisini Ayıkla ----
        yil_aranan = re.search(r"(\d{2})", dosya_adi)
        if yil_aranan:
            yil = int(yil_aranan.group(1))
            if yil < 30:  # 2030'dan küçükse 2000'li yıllar diye varsay
                yil += 2000
            else:
                yil += 1900
        else:
            yil = None  # Eğer yıl bulunamazsa None olarak ekle

        df["Yıl"] = yil

        # ---- Yerleştirme Türünü Belirle ----
        dosya_adi_kucuk = dosya_adi.lower()
        if "ek2" in dosya_adi_kucuk:
            df["Yerleştirme_Turu"] = "Ek2"
        elif "ek" in dosya_adi_kucuk:
            df["Yerleştirme_Turu"] = "Ek"
        else:
            df["Yerleştirme_Turu"] = "Ana"

        tum_veriler.append(df)

# Tüm verileri birleştir
birlesik_df = pd.concat(tum_veriler, ignore_index=True)

# Kontrol etmek için ilk birkaç satırı göster
print(birlesik_df[["Yıl", "Yerleştirme_Turu"]].drop_duplicates().head())
birlesik_df.to_excel("birlesik_veri.xlsx", index=False)
