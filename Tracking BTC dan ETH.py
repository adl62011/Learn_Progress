
import requests
import json
import time
from datetime import datetime


class CryptoTracker:                              # SOAL 1A — Isi nama class-nya: "CryptoTracker"
    """Blueprint untuk melacak harga satu koin crypto."""

    def __init__(self, coin_id: str, nama_tampil: str):   # SOAL 1B — Isi nama konstruktor yang benar
        """
        Inisialisasi tracker.
        coin_id     = ID koin di CoinGecko, contoh: "bitcoin"
        nama_tampil = Nama tampil, contoh: "Bitcoin"
        """

        self.coin_id  = coin_id             # SOAL 1C — Simpan parameter coin_id ke self
        self.nama     = nama_tampil     # (ini sudah diisi, lihat polanya!)

        self.BASE_URL = "https://api.coingecko.com/api/v3"

        # Atribut data — kosong dulu, diisi setelah panggil API
        self.harga_usd  = None
        self.harga_idr  = None
        self.market_cap = None
        self.volume_24h = None
        self.perubahan  = None

        print(f"✅ Tracker siap untuk: {self.nama}")



    def ambil_harga(self) -> bool:
        """Ambil harga koin dari CoinGecko API."""

        print(f"\n🌐 Mengambil data {self.nama}...")

        # SOAL 2A — Buat URL dengan menggabungkan BASE_URL dan endpoint
        # Hint: f"{self.BASE_URL}/????"
        url = f"{self.BASE_URL}/simple/price"

        # SOAL 2B — Lengkapi parameter yang dikirim ke API
        # Hint: "ids" harus diisi dengan self.coin_id
        params = {
            "ids"             : self.coin_id,           # SOAL 2B — Isi dengan atribut coin_id dari object ini
            "vs_currencies"   : "usd,idr",
            "include_market_cap"  : "true",
            "include_24hr_vol"    : "true",
            "include_24hr_change" : "true",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            # SOAL 2C — Ubah respons dari server menjadi dictionary Python
            # Hint: method .json() pada object response
            data = response.json()

            if self.coin_id not in data:
                print(f"❌ Koin tidak ditemukan.")
                return False

            koin_data = data[self.coin_id]

            # SOAL 2D — Simpan harga USD ke atribut self.harga_usd
            # Hint: koin_data.get("usd", 0)
            self.harga_usd  = koin_data.get("usd", 0)     # SOAL 2D — key JSON untuk harga USD
            self.harga_idr  = koin_data.get("idr", 0)   # (ini contoh yang sudah diisi)
            self.market_cap = koin_data.get("usd_market_cap", 0)
            self.volume_24h = koin_data.get("usd_24h_vol", 0)
            self.perubahan  = koin_data.get("usd_24h_change", 0)

            print(f"✅ Data {self.nama} berhasil!")
            return True                  # SOAL 2E — Return apa kalau berhasil? (True atau False)

        except requests.exceptions.ConnectionError:
            print("❌ Tidak ada koneksi internet.")
            return False
        except requests.exceptions.Timeout:
            print("❌ Server tidak merespons.")
            return False
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error HTTP: {e}")
            return False


    def tampilkan_info(self) -> None:
        """Tampilkan data koin ke layar dengan rapi."""

        # SOAL 3A — Cek apakah data sudah diambil
        # Hint: if self.??? is None:
        if self.harga_usd is None:
            print(f"⚠️  Data belum ada! Panggil ambil_harga() dulu.")
            return

        # SOAL 3B — Tentukan emoji berdasarkan arah harga
        # Hint: "📈" kalau self.perubahan >= 0, kalau tidak "📉"
        arah = "📈" if self.perubahan >= 0 else "📉"

        waktu = datetime.now().strftime("%d %B %Y  %H:%M")

        print("\n" + "=" * 45)
        print(f"  💰  {self.nama.upper()}")
        print(f"  🕐  {waktu}")
        print("=" * 45)

        # SOAL 3C — Tampilkan harga USD dengan format f-string
        # Hint: f"  Harga (USD)  : $ {self.???:,.2f}"
        print(f"  Harga (USD)  : $ {self.harga_usd:,.2f}")
        print(f"  Harga (IDR)  : Rp {self.harga_idr:,.0f}")   # (contoh sudah diisi)
        print(f"  Market Cap   : $ {self.market_cap:,.0f}")
        print(f"  Perubahan 24j: {arah} {self.perubahan:.2f}%")
        print("=" * 45)


    def simpan_laporan(self) -> None:
        """Simpan data ke file JSON."""
        if self.harga_usd is None:
            print("⚠️  Tidak ada data.")
            return

        tanggal   = datetime.now().strftime("%Y%m%d")
        nama_file = f"laporan_{self.coin_id}_{tanggal}.json"

        laporan = {
            "koin"      : self.nama,
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "harga_usd" : self.harga_usd,
            "harga_idr" : self.harga_idr,
            "perubahan" : self.perubahan
        }

        with open(nama_file, "w", encoding="utf-8") as file:
            json.dump(laporan, file, indent=2, ensure_ascii=False)

        print(f"💾 Disimpan ke: {nama_file}")




class PortfolioTracker(CryptoTracker):            # SOAL 4A — Isi nama class induk yang diwarisi
    """
    Turunan dari CryptoTracker.
    Bisa semua yang CryptoTracker bisa + hitung nilai portofolio.
    """

    def __init__(self, coin_id: str, nama_tampil: str, jumlah_dimiliki: float):

        # SOAL 4B — Panggil konstruktor class induk
        # Hint: super().???(coin_id, nama_tampil)
        super().__init__(coin_id, nama_tampil)

        self.jumlah_dimiliki = jumlah_dimiliki
        self.nilai_portfolio = None


    def hitung_portfolio(self) -> float:
        """Hitung total nilai portofolio dalam USD."""

        if self.harga_usd is None:
            print("⚠️  Ambil data harga dulu!")
            return 0.0

        # SOAL 4C — Hitung nilai portofolio
        # Hint: jumlah koin yang dimiliki × harga per koin (USD)
        self.nilai_portfolio = self.jumlah_dimiliki * self.harga_usd
        return self.nilai_portfolio


    def tampilkan_portfolio(self) -> None:
        """Tampilkan info lengkap + portofolio."""

        # SOAL 4D — Panggil method tampilkan_info() dari class induk
        # Hint: self.???()
        self.tampilkan_info()

        nilai     = self.hitung_portfolio()


        print(f"\n  📊 PORTOFOLIO KAMU")
        print(f"  Jumlah dimiliki : {self.jumlah_dimiliki} {self.nama}")
        print(f"  Nilai (USD)     : $ {nilai:,.2f}")
        # SESUDAH (aman)
        if self.harga_idr is not None and self.harga_idr > 0:
            nilai_idr = self.jumlah_dimiliki * self.harga_idr
            print(f"  Nilai (IDR)     : Rp {nilai_idr:,.0f}")
        else:
            print(f"  Nilai (IDR)     : Data tidak tersedia")
        print("=" * 45)


def bandingkan_koin(daftar_koin: list) -> None:
    """Tampilkan tabel perbandingan semua koin."""

    # SOAL 5A — Filter koin yang sudah punya data (harga_usd bukan None)
    # Hint: [k for k in daftar_koin if k.??? is not None]
    koin_valid = [k for k in daftar_koin if k.perubahan is not None]

    if not koin_valid:
        print("⚠️  Tidak ada data.")
        return

    jumlah_koin = len(koin_valid)
    total_market_cap = 0

    print("\n" + "=" * 50)
    print("  📊 PERBANDINGAN HARGA CRYPTO")
    print("=" * 50)
    print(f"  {'Nama':<15} {'Harga USD':>12} {'24j %':>8}")
    print("-" * 50)

    # SOAL 5B — Loop setiap koin dan tampilkan datanya
    # Hint: for koin in ???:
    for koin in daftar_koin:
        arah = "▲" if koin.perubahan >= 0 else "▼"
        print(
            f"  {koin.nama:<15}"
            f" ${koin.harga_usd:>11,.2f}"
            f"  {arah}{abs(koin.perubahan):.2f}%"
        )

    print("=" * 50)

    # SOAL 5C — Cari koin dengan kenaikan terbesar menggunakan max()
    # Hint: max(koin_valid, key=lambda k: k.???)
    terbaik  = max(koin_valid, key=lambda k: k.perubahan)
    terburuk = min(koin_valid, key=lambda k: k.perubahan)  # (ini sudah diisi)

    print(f"\n  🏆 Terbaik 24j : {terbaik.nama} ({terbaik.perubahan:+.2f}%)")
    print(f"  📉 Terlemah    : {terburuk.nama} ({terburuk.perubahan:+.2f}%)")
    print("=" * 50)



def ringkasan_pasar(daftar_koin: list) -> None:
    koin_valid = [k for k in daftar_koin if k.harga_usd is not None]

    if not koin_valid:
        print("⚠️  Tidak ada data koin untuk dirangkum.")
        return

    # ✅ Sekarang sejajar dengan if — di LUAR blok if
    jumlah_koin      = len(koin_valid)
    total_market_cap = 0
    total_perubahan  = 0

    for k in koin_valid:
        total_market_cap += k.market_cap
        total_perubahan  += k.perubahan

    rata_rata_24j = total_perubahan / jumlah_koin
    mc_formatted  = f"$ {total_market_cap / 1_000_000_000_000:.2f} T"

    print("\n" + "=" * 30)
    print("=== RINGKASAN PASAR ===")
    print(f"Koin dipantau    : {jumlah_koin}")
    print(f"Rata-rata 24j    : {rata_rata_24j:+.2f}%")
    print(f"Total market cap : {mc_formatted}")
    print("=" * 30)


    # ??? TULIS KODE KAMU DI SINI ???
        # Hapus 'pass' ini kalau sudah mulai nulis kode



if __name__ == "__main__":

    print("=" * 45)
    print("  🚀 LATIHAN PYTHON — CRYPTO TRACKER")
    print("=" * 45)

    # -- DEMO 1: Class dasar --
    print("\n📌 DEMO 1: Buat object dan ambil harga")
    bitcoin  = CryptoTracker("bitcoin",  "BTC")
    ethereum = CryptoTracker("ethereum", "ETH")
    solana = CryptoTracker("solana", "SOL")


    semua = [bitcoin, ethereum, solana]

    for koin in semua:
        koin.ambil_harga()
        time.sleep(3)   # Jeda agar tidak kena rate limit API

    bitcoin.tampilkan_info()

    # -- DEMO 2: Bandingkan koin --
    print("\n📌 DEMO 2: Bandingkan semua koin")
    bandingkan_koin(semua)

    # -- DEMO 3: Portfolio tracker --
    print("\n📌 DEMO 3: Hitung portofolio")
    my_btc = PortfolioTracker("bitcoin", "BTC", jumlah_dimiliki=0.01) # jumlahnya
    my_btc.harga_usd = bitcoin.harga_usd  # Salin langsung dari object bitcoin
    my_btc.harga_idr = bitcoin.harga_idr
    my_btc.market_cap = bitcoin.market_cap
    my_btc.volume_24h = bitcoin.volume_24h
    my_btc.perubahan = bitcoin.perubahan
    my_btc.tampilkan_portfolio()  # Langsung tampilkan, tidak perlu ambil_harga()

    # -- DEMO 4: Bonus --
    print("\n📌 DEMO 4: Ringkasan pasar (SOAL BONUS)")
    ringkasan_pasar(semua)

    # -- Simpan laporan --
    bitcoin.simpan_laporan()

    print("\n✅ Selesai! Cek apakah semua output muncul dengan benar.")
    print("=" * 45)
