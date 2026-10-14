"""
ŞAMPİYONDLE - LoLdle tarzı League of Legends şampiyon tahmin oyunu
Sadece Python ile gelen tkinter kullanır, ek kurulum gerekmez.

Gizli bir şampiyon seçilir. Bir şampiyon adı yazıp tahmin edersin ve
özelliklerinin gizli şampiyonla ne kadar uyuştuğu renklerle gösterilir:
  Yeşil  = Tamamen doğru
  Sarı   = Kısmen doğru (birden fazla değeri olan alanlarda)
  Kırmızı= Yanlış
  Yıl sütununda ↑ = gizli şampiyon daha yeni, ↓ = daha eski

Not: Şampiyon verileri elle girilmiştir. Hatalı bir bilgi görürsen
aşağıdaki SAMPIYONLAR listesinden kolayca düzeltebilir veya yeni
şampiyon ekleyebilirsin.
"""
import tkinter as tk
from tkinter import ttk
import random
import re
import datetime

# ------------------------------------------------------------ Şampiyon verisi
K, E, D = "Kadın", "Erkek", "Diğer"

# (Ad, Cinsiyet, [Pozisyon], [Irk], Kaynak, Menzil, [Bölge], Çıkış yılı)
SAMPIYONLAR = [
    ("Aatrox", E, ["Top"], ["Darkin"], "Özel", "Yakın", ["Shurima"], 2013),
    ("Ahri", K, ["Mid"], ["Vastaya"], "Mana", "Uzak", ["Ionia"], 2011),
    ("Akali", K, ["Mid", "Top"], ["İnsan"], "Enerji", "Yakın", ["Ionia"], 2010),
    ("Alistar", E, ["Support"], ["Minotor"], "Mana", "Yakın", ["Runeterra"], 2009),
    ("Amumu", E, ["Jungle"], ["Yordle"], "Mana", "Yakın", ["Shurima"], 2009),
    ("Annie", K, ["Mid", "Support"], ["İnsan"], "Mana", "Uzak", ["Runeterra"], 2009),
    ("Ashe", K, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Freljord"], 2009),
    ("Blitzcrank", D, ["Support"], ["Golem"], "Mana", "Yakın", ["Zaun"], 2009),
    ("Braum", E, ["Support"], ["İnsan"], "Mana", "Yakın", ["Freljord"], 2014),
    ("Caitlyn", K, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Piltover"], 2011),
    ("Darius", E, ["Top"], ["İnsan"], "Mana", "Yakın", ["Noxus"], 2012),
    ("Diana", K, ["Jungle", "Mid"], ["İnsan"], "Mana", "Yakın", ["Targon"], 2012),
    ("Draven", E, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Noxus"], 2012),
    ("Ekko", E, ["Jungle", "Mid"], ["İnsan"], "Mana", "Yakın", ["Zaun"], 2015),
    ("Ezreal", E, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Piltover"], 2010),
    ("Fiora", K, ["Top"], ["İnsan"], "Mana", "Yakın", ["Demacia"], 2012),
    ("Fizz", E, ["Mid"], ["Yordle"], "Mana", "Yakın", ["Bilgewater"], 2011),
    ("Galio", E, ["Mid", "Support"], ["Golem"], "Mana", "Yakın", ["Demacia"], 2010),
    ("Garen", E, ["Top"], ["İnsan"], "Kaynaksız", "Yakın", ["Demacia"], 2010),
    ("Gragas", E, ["Jungle", "Top"], ["İnsan"], "Mana", "Yakın", ["Freljord"], 2010),
    ("Graves", E, ["Jungle"], ["İnsan"], "Kaynaksız", "Uzak", ["Bilgewater"], 2011),
    ("Hecarim", E, ["Jungle"], ["Ruh"], "Mana", "Yakın", ["Gölgeli Adalar"], 2012),
    ("Heimerdinger", E, ["Top", "Mid"], ["Yordle"], "Mana", "Uzak", ["Piltover"], 2009),
    ("Irelia", K, ["Top", "Mid"], ["İnsan"], "Mana", "Yakın", ["Ionia"], 2010),
    ("Janna", K, ["Support"], ["Ruh"], "Mana", "Uzak", ["Zaun"], 2009),
    ("Jarvan IV", E, ["Jungle"], ["İnsan"], "Mana", "Yakın", ["Demacia"], 2011),
    ("Jax", E, ["Top", "Jungle"], ["İnsan"], "Mana", "Yakın", ["Runeterra"], 2009),
    ("Jhin", E, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Ionia"], 2016),
    ("Jinx", K, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Zaun"], 2013),
    ("Kai'Sa", K, ["ADC"], ["İnsan", "Void"], "Mana", "Uzak", ["Shurima", "Void"], 2018),
    ("Katarina", K, ["Mid"], ["İnsan"], "Kaynaksız", "Yakın", ["Noxus"], 2009),
    ("Kayn", E, ["Jungle"], ["İnsan", "Darkin"], "Kaynaksız", "Yakın", ["Ionia"], 2017),
    ("Kennen", E, ["Top"], ["Yordle"], "Enerji", "Uzak", ["Ionia"], 2010),
    ("Kha'Zix", E, ["Jungle"], ["Void"], "Mana", "Yakın", ["Void"], 2012),
    ("Lee Sin", E, ["Jungle"], ["İnsan"], "Enerji", "Yakın", ["Ionia"], 2009),
    ("Leona", K, ["Support"], ["İnsan"], "Mana", "Yakın", ["Targon"], 2011),
    ("Lucian", E, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Demacia"], 2013),
    ("Lulu", K, ["Support"], ["Yordle"], "Mana", "Uzak", ["Bandle City"], 2012),
    ("Lux", K, ["Mid", "Support"], ["İnsan"], "Mana", "Uzak", ["Demacia"], 2010),
    ("Malphite", E, ["Top"], ["Golem"], "Mana", "Yakın", ["Ixtal"], 2009),
    ("Master Yi", E, ["Jungle"], ["Vastaya"], "Mana", "Yakın", ["Ionia"], 2009),
    ("Miss Fortune", K, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Bilgewater"], 2010),
    ("Nasus", E, ["Top"], ["Yükselmiş"], "Mana", "Yakın", ["Shurima"], 2009),
    ("Nidalee", K, ["Jungle"], ["İnsan"], "Mana", "Uzak", ["Ixtal"], 2009),
    ("Orianna", K, ["Mid"], ["Golem"], "Mana", "Uzak", ["Piltover"], 2011),
    ("Poppy", K, ["Top", "Jungle"], ["Yordle"], "Mana", "Yakın", ["Demacia"], 2010),
    ("Pyke", E, ["Support"], ["İnsan"], "Mana", "Yakın", ["Bilgewater"], 2018),
    ("Quinn", K, ["Top"], ["İnsan"], "Mana", "Uzak", ["Demacia"], 2013),
    ("Rakan", E, ["Support"], ["Vastaya"], "Mana", "Yakın", ["Ionia"], 2017),
    ("Riven", K, ["Top"], ["İnsan"], "Kaynaksız", "Yakın", ["Noxus"], 2011),
    ("Sett", E, ["Top"], ["Vastaya"], "Özel", "Yakın", ["Ionia"], 2020),
    ("Shen", E, ["Top"], ["İnsan"], "Enerji", "Yakın", ["Ionia"], 2010),
    ("Singed", E, ["Top"], ["İnsan"], "Mana", "Yakın", ["Zaun"], 2009),
    ("Sona", K, ["Support"], ["İnsan"], "Mana", "Uzak", ["Demacia"], 2010),
    ("Swain", E, ["Mid"], ["İnsan"], "Mana", "Uzak", ["Noxus"], 2010),
    ("Sylas", E, ["Mid"], ["İnsan"], "Mana", "Yakın", ["Demacia"], 2019),
    ("Teemo", E, ["Top"], ["Yordle"], "Mana", "Uzak", ["Bandle City"], 2009),
    ("Thresh", E, ["Support"], ["Ruh"], "Mana", "Uzak", ["Gölgeli Adalar"], 2013),
    ("Tristana", K, ["ADC"], ["Yordle"], "Mana", "Uzak", ["Bandle City"], 2009),
    ("Tryndamere", E, ["Top"], ["İnsan"], "Özel", "Yakın", ["Freljord"], 2009),
    ("Twisted Fate", E, ["Mid"], ["İnsan"], "Mana", "Uzak", ["Bilgewater"], 2009),
    ("Vayne", K, ["ADC"], ["İnsan"], "Mana", "Uzak", ["Demacia"], 2011),
    ("Veigar", E, ["Mid"], ["Yordle"], "Mana", "Uzak", ["Bandle City"], 2009),
    ("Vel'Koz", D, ["Mid", "Support"], ["Void"], "Mana", "Uzak", ["Void"], 2014),
    ("Vi", K, ["Jungle"], ["İnsan"], "Mana", "Yakın", ["Piltover"], 2012),
    ("Viktor", E, ["Mid"], ["İnsan"], "Mana", "Uzak", ["Zaun"], 2011),
    ("Vladimir", E, ["Mid", "Top"], ["İnsan"], "Özel", "Uzak", ["Noxus"], 2010),
    ("Warwick", E, ["Jungle"], ["İnsan"], "Mana", "Yakın", ["Zaun"], 2009),
    ("Xayah", K, ["ADC"], ["Vastaya"], "Mana", "Uzak", ["Ionia"], 2017),
    ("Yasuo", E, ["Mid"], ["İnsan"], "Özel", "Yakın", ["Ionia"], 2013),
    ("Yone", E, ["Mid", "Top"], ["İnsan", "Ruh"], "Kaynaksız", "Yakın", ["Ionia"], 2020),
    ("Zed", E, ["Mid"], ["İnsan"], "Enerji", "Yakın", ["Ionia"], 2012),
]

SUTUNLAR = ["Şampiyon", "Cinsiyet", "Pozisyon", "Irk", "Kaynak",
            "Menzil", "Bölge", "Çıkış Yılı"]

# ------------------------------------------------------------ Renkler
BG = "#0a1628"
PANEL = "#12243d"
ALTIN = "#c8aa6e"
YESIL = "#2e9e4f"
SARI = "#d9a82b"
KIRMIZI = "#b8353a"
GIZLI = "#33475b"
ISIM_BG = "#1d3557"

DURUM_RENK = {"dogru": YESIL, "kismi": SARI, "yanlis": KIRMIZI}


def norm(metin):
    """Arama için: küçük harf, sadece harf/rakam."""
    return re.sub(r"[^a-z0-9]", "", metin.lower())


def karsilastir(tahmin, hedef):
    """Her sütun için (gösterilecek metin, durum) listesi döndürür."""
    sonuc = [(tahmin[0], "dogru" if tahmin[0] == hedef[0] else "yanlis")]
    for i in range(1, 7):
        t, h = tahmin[i], hedef[i]
        if isinstance(t, list):
            a, b = set(t), set(h)
            if a == b:
                durum = "dogru"
            elif a & b:
                durum = "kismi"
            else:
                durum = "yanlis"
            sonuc.append((", ".join(t), durum))
        else:
            sonuc.append((t, "dogru" if t == h else "yanlis"))
    yil_t, yil_h = tahmin[7], hedef[7]
    if yil_t == yil_h:
        sonuc.append((str(yil_t), "dogru"))
    else:
        ok = "↑" if yil_h > yil_t else "↓"
        sonuc.append((f"{yil_t} {ok}", "yanlis"))
    return sonuc


class Loldle:
    def __init__(self, root):
        self.root = root
        root.title("Şampiyondle - LoLdle tarzı tahmin oyunu")
        root.configure(bg=BG)
        root.geometry("960x680")
        root.minsize(900, 560)

        self.sampiyonlar = sorted(SAMPIYONLAR, key=lambda s: s[0])
        self.liste_isimler = [s[0] for s in self.sampiyonlar]

        self.arayuz_kur()
        self.yeni_oyun()

    # ------------------------------------------------------------ Arayüz
    def arayuz_kur(self):
        ust = tk.Frame(self.root, bg=BG)
        ust.pack(fill="x", padx=16, pady=(12, 4))

        tk.Label(ust, text="ŞAMPİYONDLE", bg=BG, fg=ALTIN,
                 font=("Georgia", 26, "bold")).pack(side="left")

        # Renk açıklaması
        lej = tk.Frame(ust, bg=BG)
        lej.pack(side="right")
        for renk, yazi in ((YESIL, "Doğru"), (SARI, "Kısmen"), (KIRMIZI, "Yanlış")):
            tk.Label(lej, text="  ", bg=renk).pack(side="left", padx=(10, 3))
            tk.Label(lej, text=yazi, bg=BG, fg="white",
                     font=("Arial", 9)).pack(side="left")
        tk.Label(lej, text="   ↑ ↓ = yıl daha yeni / eski", bg=BG, fg="#9fb3c8",
                 font=("Arial", 9)).pack(side="left")

        tk.Label(self.root, text="Gizli şampiyonu özelliklerinden tahmin et!",
                 bg=BG, fg="#9fb3c8", font=("Arial", 11)).pack(anchor="w", padx=18)

        # Giriş satırı
        giris_satir = tk.Frame(self.root, bg=BG)
        giris_satir.pack(fill="x", padx=16, pady=10)

        self.giris = tk.Entry(giris_satir, font=("Arial", 14), width=26,
                              bg=PANEL, fg="white", insertbackground="white",
                              relief="flat", highlightthickness=2,
                              highlightbackground="#2a4468",
                              highlightcolor=ALTIN)
        self.giris.pack(side="left", ipady=6)
        self.giris.bind("<KeyRelease>", self.yazi_degisti)
        self.giris.bind("<Return>", lambda e: self.tahmin_et())
        self.giris.bind("<Down>", lambda e: self.liste_hareket(1))
        self.giris.bind("<Up>", lambda e: self.liste_hareket(-1))
        self.giris.bind("<Escape>", lambda e: self.liste_gizle())

        self.buton_stili = dict(font=("Arial", 11, "bold"), relief="flat",
                                cursor="hand2", padx=14, pady=6)
        tk.Button(giris_satir, text="Tahmin Et", bg=ALTIN, fg="#1a1a1a",
                  command=self.tahmin_et, **self.buton_stili
                  ).pack(side="left", padx=(8, 4))
        tk.Button(giris_satir, text="Yeni Oyun", bg="#2a4468", fg="white",
                  command=self.yeni_oyun, **self.buton_stili
                  ).pack(side="left", padx=4)
        tk.Button(giris_satir, text="Günün Şampiyonu", bg="#2a4468", fg="white",
                  command=self.gunluk_oyun, **self.buton_stili
                  ).pack(side="left", padx=4)
        tk.Button(giris_satir, text="Pes Et", bg="#6b2a2a", fg="white",
                  command=self.pes_et, **self.buton_stili
                  ).pack(side="left", padx=4)

        # Öneri listesi (girişin altında açılır)
        self.oneri = tk.Listbox(self.root, font=("Arial", 12), height=6,
                                bg=PANEL, fg="white", selectbackground=ALTIN,
                                selectforeground="#1a1a1a", relief="flat",
                                activestyle="none", highlightthickness=1,
                                highlightbackground=ALTIN)
        self.oneri.bind("<ButtonRelease-1>", self.oneri_tiklandi)

        # Durum çubuğu
        self.durum = tk.Label(self.root, text="", bg=BG, fg="white",
                              font=("Arial", 12, "bold"), anchor="w")
        self.durum.pack(fill="x", padx=18, pady=(0, 6))

        # Tablo başlıkları
        self.baslik = tk.Frame(self.root, bg=BG)
        self.baslik.pack(fill="x", padx=16)
        for s in SUTUNLAR:
            tk.Label(self.baslik, text=s, width=13, bg=BG, fg=ALTIN,
                     font=("Arial", 10, "bold")).pack(side="left", padx=2)

        # Kaydırılabilir tahmin tablosu
        kap = tk.Frame(self.root, bg=BG)
        kap.pack(fill="both", expand=True, padx=16, pady=(2, 10))
        self.tuval = tk.Canvas(kap, bg=BG, highlightthickness=0)
        kaydirma = ttk.Scrollbar(kap, orient="vertical", command=self.tuval.yview)
        self.tuval.configure(yscrollcommand=kaydirma.set)
        kaydirma.pack(side="right", fill="y")
        self.tuval.pack(side="left", fill="both", expand=True)
        self.tablo = tk.Frame(self.tuval, bg=BG)
        self.tuval.create_window((0, 0), window=self.tablo, anchor="nw")
        self.tablo.bind("<Configure>", lambda e: self.tuval.configure(
            scrollregion=self.tuval.bbox("all")))
        self.tuval.bind_all("<MouseWheel>", lambda e: self.tuval.yview_scroll(
            int(-e.delta / 120) if e.delta else 0, "units"))
        self.tuval.bind_all("<Button-4>", lambda e: self.tuval.yview_scroll(-1, "units"))
        self.tuval.bind_all("<Button-5>", lambda e: self.tuval.yview_scroll(1, "units"))

    # ------------------------------------------------------------ Oyun akışı
    def sifirla(self):
        for w in self.tablo.winfo_children():
            w.destroy()
        self.satirlar = []
        self.tahminler = set()
        self.bitti = False
        self.animasyon = False
        self.sayac = 0
        self.liste_gizle()
        self.giris.delete(0, "end")
        self.giris.focus_set()

    def yeni_oyun(self):
        self.sifirla()
        self.hedef = random.choice(self.sampiyonlar)
        self.mod = "Rastgele"
        self.durum_yaz("Rastgele bir şampiyon seçildi. İlk tahminini yap!", "white")

    def gunluk_oyun(self):
        self.sifirla()
        bugun = datetime.date.today().isoformat()
        self.hedef = random.Random(bugun).choice(self.sampiyonlar)
        self.mod = "Günlük"
        self.durum_yaz(f"Günün şampiyonu ({bugun}) seçildi. Herkes aynı şampiyonu arıyor!",
                       "white")

    def pes_et(self):
        if self.bitti or self.animasyon:
            return
        self.bitti = True
        self.durum_yaz(f"Pes ettin. Gizli şampiyon: {self.hedef[0]}", "#ff8a8a")

    def durum_yaz(self, metin, renk):
        self.durum.config(text=metin, fg=renk)

    # ------------------------------------------------------------ Otomatik tamamlama
    def eslesenler(self, metin):
        n = norm(metin)
        if not n:
            return []
        uygun = [ad for ad in self.liste_isimler
                 if n in norm(ad) and ad not in self.tahminler]
        uygun.sort(key=lambda ad: (not norm(ad).startswith(n), ad))
        return uygun[:8]

    def yazi_degisti(self, olay):
        if olay.keysym in ("Return", "Up", "Down", "Escape"):
            return
        sonuclar = self.eslesenler(self.giris.get())
        self.oneri.delete(0, "end")
        if not sonuclar:
            self.liste_gizle()
            return
        for ad in sonuclar:
            self.oneri.insert("end", ad)
        self.oneri.selection_set(0)
        self.oneri.config(height=len(sonuclar))
        self.oneri.place(in_=self.giris, x=0, rely=1.0, relwidth=1.0)
        self.oneri.lift()

    def liste_gizle(self):
        self.oneri.place_forget()

    def liste_hareket(self, yon):
        if not self.oneri.winfo_ismapped():
            return "break"
        mevcut = self.oneri.curselection()
        idx = mevcut[0] if mevcut else -1
        yeni = max(0, min(self.oneri.size() - 1, idx + yon))
        self.oneri.selection_clear(0, "end")
        self.oneri.selection_set(yeni)
        self.oneri.see(yeni)
        return "break"

    def oneri_tiklandi(self, olay):
        idx = self.oneri.nearest(olay.y)
        if 0 <= idx < self.oneri.size():
            self.tahmin_et(self.oneri.get(idx))

    # ------------------------------------------------------------ Tahmin
    def tahmin_et(self, ad=None):
        if self.bitti:
            self.durum_yaz("Oyun bitti. Yeni Oyun'a basarak tekrar oyna!", "#9fb3c8")
            return
        if self.animasyon:
            return

        if ad is None:
            if self.oneri.winfo_ismapped() and self.oneri.curselection():
                ad = self.oneri.get(self.oneri.curselection()[0])
            else:
                yazilan = norm(self.giris.get())
                tam = [a for a in self.liste_isimler if norm(a) == yazilan]
                if tam:
                    ad = tam[0]
                else:
                    sonuc = self.eslesenler(self.giris.get())
                    ad = sonuc[0] if sonuc else None

        if ad is None:
            self.durum_yaz("Böyle bir şampiyon bulunamadı.", "#ff8a8a")
            return
        if ad in self.tahminler:
            self.durum_yaz(f"{ad} için zaten tahmin yaptın.", "#ffd479")
            return

        veri = next(s for s in self.sampiyonlar if s[0] == ad)
        self.tahminler.add(ad)
        self.sayac += 1
        self.giris.delete(0, "end")
        self.liste_gizle()
        self.satir_ekle(veri)

    def satir_ekle(self, veri):
        sonuc = karsilastir(veri, self.hedef)
        satir = tk.Frame(self.tablo, bg=BG)
        if self.satirlar:
            satir.pack(fill="x", pady=2, before=self.satirlar[0])
        else:
            satir.pack(fill="x", pady=2)
        self.satirlar.insert(0, satir)

        hucreler = []
        for i in range(len(SUTUNLAR)):
            h = tk.Label(satir, text="?", width=13, height=3, bg=GIZLI, fg="white",
                         font=("Arial", 10, "bold"), wraplength=96)
            h.pack(side="left", padx=2)
            hucreler.append(h)

        self.animasyon = True
        self.durum_yaz(f"Tahmin #{self.sayac}: {veri[0]}", "white")
        for i, (metin, durum) in enumerate(sonuc):
            self.root.after(i * 280, self.hucre_ac, hucreler[i], metin, durum, i)
        self.root.after(len(sonuc) * 280 + 100, self.tahmin_bitti, veri)

    def hucre_ac(self, hucre, metin, durum, i):
        renk = ISIM_BG if i == 0 else DURUM_RENK[durum]
        hucre.config(text=metin, bg=renk)

    def tahmin_bitti(self, veri):
        self.animasyon = False
        if veri[0] == self.hedef[0]:
            self.bitti = True
            self.durum_yaz(
                f"TEBRİKLER! {self.hedef[0]} doğru cevaptı. "
                f"{self.sayac} tahminde buldun!", "#7dff9a")
        else:
            self.durum_yaz(f"{veri[0]} değil. Toplam tahmin: {self.sayac}", "white")
        self.giris.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    Loldle(root)
    root.mainloop()
