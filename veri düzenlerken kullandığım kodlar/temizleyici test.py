import os
import pandas as pd
import re


#yapay zeka yardımıyla yazıldı
#eski formattaki temizlenmiş tabloların hesaplamasını yapıyor ve iişliyor


# Klasör yolları
girdi_klasoru = "temizlenecek2"
cikti_klasoru = "duzenlenmis"
os.makedirs(cikti_klasoru, exist_ok=True)

# Fonksiyonlar
def bolum_adi_ayikla(prog_adi):
    prog_adi = str(prog_adi)
    fakulte_idx = prog_adi.find("Fakültesi")
    yuksekokul_idx = prog_adi.find("Yüksekokulu")

    if fakulte_idx != -1 or yuksekokul_idx != -1:
        egitim_kurumu_idx = fakulte_idx if fakulte_idx != -1 else yuksekokul_idx
        sonrasi = prog_adi[egitim_kurumu_idx:]

        slash_sonra_idx = sonrasi.find("/")
        if slash_sonra_idx != -1:
            bolum_ve_devami = sonrasi[slash_sonra_idx + 1:]
            paren_idx = bolum_ve_devami.find("(")
            return bolum_ve_devami[:paren_idx].strip() if paren_idx != -1 else bolum_ve_devami.strip()
        else:
            last_slash_idx = prog_adi.rfind("/", 0, egitim_kurumu_idx)
            return prog_adi[last_slash_idx + 1 : egitim_kurumu_idx].strip() if last_slash_idx != -1 else prog_adi[:egitim_kurumu_idx].strip()
    else:
        last_slash_idx = prog_adi.rfind("/")
        after_slash = prog_adi[last_slash_idx + 1:] if last_slash_idx != -1 else prog_adi
        paren_idx = after_slash.find("(")
        return after_slash[:paren_idx].strip() if paren_idx != -1 else after_slash.strip()

def ogretim_dili_bul(x):
    #x = str(x).lower()
    if "(İngilizce)" in x:
        return "İngilizce"
    elif "(Almanca)" in x:
        return "Almanca"
    elif "(Fransızca)" in x:
        return "Fransızca"
    elif re.search(r"\((Arapça|Rusça|Japonca|Çince|Korece| Ermenice|İspanyolca|İtalyanca|Lehçe)\)", x):
        return re.search(r"\((.*?)\)", x).group(1).capitalize()
    else:
        return "Türkçe"

def burs_durumu_bul(x):
    if not isinstance(x, str):
        x = str(x)

    if "Tam Burslu" in x:
        return "Tam Burslu"
    elif "%75 Burslu" in x:
        return "%75 Burslu"
    elif "%25 İndirimli" in x:
        return "%75 Burslu"  # özel kuralın: %25 indirimli → %75 Burslu
    elif "%50" in x:
        return "%50 Burslu"
    elif "%25 Burslu" in x:
        return "%25 Burslu"
    elif "%75 İndirimli" in x:
        return "%25 Burslu"
    elif re.search(r"\(Burslu\)", x) and not re.search(r"%\d{1,2}", x):
        return "Tam Burslu"
    elif "Ücretli" in x:
        return "Ücretli"
    else:
        return "Devlet"


def ogretim_turu_bul(x):
    x = str(x).upper()
    if "(İÖ)" in x:
        return "İkinci Öğretim"
    elif "AÇIKÖĞRETİM" in x:
        return "Açıköğretim"
    else:
        return "Örgün"

def ekstra_bilgi_ayikla(prog_adi):
    prog_adi = str(prog_adi)
    parantez_icerikleri = re.findall(r"\((.*?)\)", prog_adi)
    ekstra_list = []

    ogretim_dilleri = {"İngilizce", "Almanca", "Fransızca", "Arapça", "Rusça", "Japonca", "Çince", "Korece"}
    burs_durumlari = {"tam burslu", "%75", "%50", "%25", "ücretli" , "burslu"}
    ogrenim_turu = {"İÖ", "Açıköğretim"}

    for icerik in parantez_icerikleri:
        icerik_kucuk = icerik.lower().strip()
        if (icerik_kucuk not in {x.lower() for x in ogretim_dilleri} and
            all(burs not in icerik_kucuk for burs in burs_durumlari) and
            icerik_kucuk not in {x.lower() for x in ogrenim_turu}):
            ekstra_list.append(icerik.strip())

    return "; ".join(ekstra_list) if ekstra_list else ""

def doluluk_orani(kontenjan, yerlesen):
    try:
        kontenjan = int(kontenjan)
        yerlesen = int(yerlesen)
        if yerlesen == 0 or kontenjan == 0:
            return 0
        else:
            return round((yerlesen / kontenjan) * 100, 2)
    except:
        return 0

def add_column_if_not_exists(df, col_name, default_value=None):
    if col_name not in df.columns:
        df[col_name] = default_value

# Dosyaları işle
for dosya_adi in os.listdir(girdi_klasoru):
    if dosya_adi.endswith(".xlsx"):
        dosya_yolu = os.path.join(girdi_klasoru, dosya_adi)
        df = pd.read_excel(dosya_yolu)

        try:
            # Excel dosyasını açmayı dene
            df = pd.read_excel(dosya_yolu)

            # Eğer veri tamamen boşsa
            if df.empty:
                print(f"{dosya_adi} atlandı → Dosya boş.")
                continue

            # Sütun isimlerini normalize et
            df.columns = df.columns.str.strip().str.lower()

            # Gerekli sütunlar
            gerekli_sutunlar = ["program adı", "kontenjan", "yerleşen"]
            eksik_sutunlar = [s for s in gerekli_sutunlar if s not in df.columns]

            if eksik_sutunlar:
                print(f"{dosya_adi} atlandı → Eksik sütun(lar): {eksik_sutunlar}")
                continue

            print(f"{dosya_adi} başarıyla yüklendi ✓")

        except Exception as e:
            print(f"{dosya_adi} atlandı → Hata oluştu: {e}")

        if not all(k in df.columns for k in ["program adı", "kontenjan", "yerleşen"]):
            continue

        print(f"{dosya_adi} sütunlar:", df.columns.tolist())

        # Gerekli sütunları ekle (yoksa)
        add_column_if_not_exists(df, "Üniversite Adı")
        add_column_if_not_exists(df, "Bölüm Adı")
        add_column_if_not_exists(df, "Öğretim Türü")
        add_column_if_not_exists(df, "Öğretim Dili")
        add_column_if_not_exists(df, "Burs Durumu")
        add_column_if_not_exists(df, "Doluluk Oranı (%)")
        add_column_if_not_exists(df, "Ekstra Bilgi")

        # Verileri işle
        df["Üniversite Adı"] = df["program adı"].apply(lambda x: re.search(r"^(.*?Üniversitesi)", str(x), re.IGNORECASE).group(1) if re.search(r"^(.*?Üniversitesi)", str(x), re.IGNORECASE) else None)
        df["Bölüm Adı"] = df["program adı"].apply(bolum_adi_ayikla)
        df["Öğretim Türü"] = df["program adı"].apply(ogretim_turu_bul)
        df["Öğretim Dili"] = df["program adı"].apply(ogretim_dili_bul)
        df["Burs Durumu"] = df["program adı"].apply(burs_durumu_bul)
        df["Doluluk Oranı (%)"] = df.apply(lambda row: doluluk_orani(row["kontenjan"], row["yerleşen"]), axis=1)
        df["Ekstra Bilgi"] = df["program adı"].apply(ekstra_bilgi_ayikla)

        print(f"İşlenen dosya: {dosya_adi}")
        print(f"Satır sayısı: {len(df)}")

        duzenlenmis_yol = os.path.join("duzenlenmis", dosya_adi)
        print(f"Tam kayıt yolu: {os.path.abspath(duzenlenmis_yol)}")

        try:
            df.to_excel(duzenlenmis_yol, index=False)
            print(f"{dosya_adi} başarıyla duzenlenmis klasörüne kaydedildi ✓")
        except Exception as e:
            print(f"{dosya_adi} yazılırken hata oluştu: {e}")





