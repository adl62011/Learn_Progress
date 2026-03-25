from time import sleep

import requests
import json
import time
from datetime import datetime


class CryptoTracker:

    def __init__(self, coin_id: str, nama_tampil: str):

        self.coin_id  = coin_id
        self.nama     = nama_tampil

        self.BASE_URL = "https://api.coingecko.com/api/v3"


        self.harga_usd  = None
        self.harga_idr  = None
        self.market_cap = None
        self.volume_24h = None
        self.perubahan  = None

        print(f"✅ Tracker siap untuk: {self.nama}")



    def ambil_harga(self) -> bool:
        """Ambil harga koin dari CoinGecko API."""

        print(f"\n🌐 Mengambil data {self.nama}...")


        url = f"{self.BASE_URL}/simple/price"


        params = {
            "ids"             : self.coin_id,
            "vs_currencies"   : "usd,idr",
            "include_market_cap"  : "true",
            "include_24hr_vol"    : "true",
            "include_24hr_change" : "true",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()


            data = response.json()

            if self.coin_id not in data:
                print(f"❌ Koin tidak ditemukan.")
                return False

            koin_data = data[self.coin_id]


            self.harga_usd  = koin_data.get("usd", 0)
            self.harga_idr  = koin_data.get("idr", 0)
            self.market_cap = koin_data.get("usd_market_cap", 0)
            self.volume_24h = koin_data.get("usd_24h_vol", 0)
            self.perubahan  = koin_data.get("usd_24h_change", 0)

            print(f"✅ Data {self.nama} berhasil!")
            return True

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

        if self.harga_usd is None:
            print(f"⚠️  Data belum ada! Panggil ambil_harga() dulu.")
            return

        arah = "📈" if self.perubahan >= 0 else "📉"

        waktu = datetime.now().strftime("%d %B %Y  %H:%M")

        print("\n" + "=" * 45)
        print(f"  💰  {self.nama.upper()}")
        print(f"  🕐  {waktu}")
        print("=" * 45)


        print(f"  Harga (USD)  : $ {self.harga_usd:,.2f}")
        print(f"  Harga (IDR)  : Rp {self.harga_idr:,.0f}")
        print(f"  Market Cap   : $ {self.market_cap:,.0f}")
        print(f"  Perubahan 24j: {arah} {self.perubahan:.2f}%")
        print("=" * 45)


    def simpan_laporan(self) -> None:
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




class PortfolioTracker(CryptoTracker):

    def __init__(self, coin_id: str, nama_tampil: str, jumlah_dimiliki: float):


        super().__init__(coin_id, nama_tampil)

        self.jumlah_dimiliki = jumlah_dimiliki
        self.nilai_portfolio = None


    def hitung_portfolio(self) -> float:

        if self.harga_usd is None:
            print("⚠️  Ambil data harga dulu!")
            return 0.0


        self.nilai_portfolio = self.jumlah_dimiliki * self.harga_usd
        return self.nilai_portfolio


    def tampilkan_portfolio(self) -> None:

        self.tampilkan_info()

        nilai     = self.hitung_portfolio()


        print(f"\n  📊 PORTOFOLIO KAMU")
        print(f"  Jumlah dimiliki : {self.jumlah_dimiliki} {self.nama}")
        print(f"  Nilai (USD)     : $ {nilai:,.2f}")

        if self.harga_idr is not None and self.harga_idr > 0:
            nilai_idr = self.jumlah_dimiliki * self.harga_idr
            print(f"  Nilai (IDR)     : Rp {nilai_idr:,.0f}")
        else:
            print(f"  Nilai (IDR)     : Data tidak tersedia")
        print("=" * 45)


def bandingkan_koin(daftar_koin: list) -> None:

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


    for koin in daftar_koin:
        arah = "▲" if koin.perubahan >= 0 else "▼"
        print(
            f"  {koin.nama:<15}"
            f" ${koin.harga_usd:>11,.2f}"
            f"  {arah}{abs(koin.perubahan):.2f}%"
        )

    print("=" * 50)


    terbaik  = max(koin_valid, key=lambda k: k.perubahan)
    terburuk = min(koin_valid, key=lambda k: k.perubahan)

    print(f"\n  🏆 Terbaik 24j : {terbaik.nama} ({terbaik.perubahan:+.2f}%)")
    print(f"  📉 Terlemah    : {terburuk.nama} ({terburuk.perubahan:+.2f}%)")
    print("=" * 50)



def ringkasan_pasar(daftar_koin: list) -> None:
    koin_valid = [k for k in daftar_koin if k.harga_usd is not None]

    if not koin_valid:
        print("⚠️  Tidak ada data koin untuk dirangkum.")
        return

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
        time.sleep(5)   # Jeda agar tidak kena rate limit API

    bitcoin.tampilkan_info()

    # -- DEMO 2: Bandingkan koin --
    print("\n📌 DEMO 2: Bandingkan semua koin")
    bandingkan_koin(semua)

    # -- DEMO 3: Portfolio tracker --
    print("\n📌 DEMO 3: Hitung portofolio")
    my_btc = PortfolioTracker("bitcoin", "BTC", jumlah_dimiliki=1) # jumlahnya
    sleep(3)
    my_btc.ambil_harga()
    sleep(3)
    my_btc.tampilkan_portfolio()

    # -- DEMO 4: Bonus --
    print("\n📌 DEMO 4: Ringkasan pasar (SOAL BONUS)")
    ringkasan_pasar(semua)

    # -- Simpan laporan --
    bitcoin.simpan_laporan()

    print("\n✅ Selesai! Cek apakah semua output muncul dengan benar.")
    print("=" * 45)

