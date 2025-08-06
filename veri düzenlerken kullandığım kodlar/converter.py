import pdfplumber
import pandas as pd
import os
#yapay zeka ile yazıldı
#pdf teki tabloları excele dönüştürüyor



# PDF'lerin bulunduğu klasör
klasor_yolu = "veriler"
# Excel çıktılarını saklamak için klasör oluştur
cikti_klasoru = "cikti_excel"
os.makedirs(cikti_klasoru, exist_ok=True)

# Her PDF dosyasını sırayla işle
for dosya_adi in os.listdir(klasor_yolu):
    if dosya_adi.endswith(".pdf"):
        pdf_yolu = os.path.join(klasor_yolu, dosya_adi)
        print(f"🔄 Dönüştürülüyor: {dosya_adi}")

        tum_sayfalar = []
        with pdfplumber.open(pdf_yolu) as pdf:
            for sayfa in pdf.pages:
                tablo = sayfa.extract_table()
                if tablo:
                    df = pd.DataFrame(tablo[1:], columns=tablo[0])
                    tum_sayfalar.append(df)

        if tum_sayfalar:
            sonuc_df = pd.concat(tum_sayfalar, ignore_index=True)
            excel_adi = dosya_adi.replace(".pdf", ".xlsx")
            sonuc_df.to_excel(os.path.join(cikti_klasoru, excel_adi), index=False)
            print(f"✅ Kaydedildi: {excel_adi}")
        else:
            print(f"⚠️ Tablo bulunamadı: {dosya_adi}")
