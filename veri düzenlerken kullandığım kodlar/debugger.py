import pandas as pd
import os

duzenlenmis_klasoru = r"C:\Users\DİLA\Desktop\staj\kodlar\duzenlenmis"
dosya_adi = "test_kayit.xlsx"
duzenlenmis_yol = os.path.join(duzenlenmis_klasoru, dosya_adi)

if not os.path.exists(duzenlenmis_klasoru):
    os.makedirs(duzenlenmis_klasoru)

df = pd.DataFrame({"a":[1,2,3], "b":[4,5,6]})

try:
    df.to_excel(duzenlenmis_yol, index=False)
    print(f"Dosya başarıyla kaydedildi: {duzenlenmis_yol}")
except Exception as e:
    print(f"Hata oluştu: {e}")
