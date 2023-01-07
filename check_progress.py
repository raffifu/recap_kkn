from Simaster import Simaster
from dotenv import load_dotenv, set_key, get_key

load_dotenv()

USERNAME = get_key(".env", "USERNAME")
PASSWORD = get_key(".env", "PASSWORD")

UGM_SESSION = get_key(".env", "UGM_SESSION")

if not USERNAME or not PASSWORD:
    raise RuntimeError("Username or Password not found")

simaster = Simaster(credential={
    "username": USERNAME,
    "password": PASSWORD
}, session=UGM_SESSION)

data_proker = simaster.data_proker()

total = {"Tema": 0, "Non Tema": 0, "Bantu": 0}

def cetak_proker(title, data, jenis):
    print(f'-----------------------------------------------------------------')
    print(f'{title}')
    print(f'-----------------------------------------------------------------')
    
    idx = 1
    durasi = 0
    for d in data:
        if d['jenis'] != jenis:
            continue

        print(f'{idx}. {d["RPP"]}')
        for kegiatan in d['kegiatan']:
            print(f'    {kegiatan["durasi"]} jam: {kegiatan["judul"]}')
            durasi += kegiatan['durasi']
        idx += 1
    
    print(f'Total Durasi: {durasi} jam')
    
    return durasi

detail_proker = None
for proker in data_proker:
    detail_proker = simaster.detail_proker(proker['url'])

    durasi = cetak_proker(title=f'{proker["jenis"]} - {proker["title"]}', data=detail_proker, jenis='pokok')
    total[proker['jenis']] += durasi


# Proker Bantu
durasi = cetak_proker("PROGRAM KERJA BANTU", detail_proker, 'bantu')
total['Bantu'] += durasi

print("-----------------------------------------------------------------")
for jenis, durasi in total.items():
    print(f'{jenis}: {durasi} jam')

keseluruhan = total["Tema"] + total["Non Tema"] + total["Bantu"]

print(f'Durasi Keseluruhan: {keseluruhan} jam')
print(f'Progress: {(keseluruhan) / 288 * 100:.2f}%')
print("-----------------------------------------------------------------")