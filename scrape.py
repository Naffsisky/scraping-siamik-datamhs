import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL halaman yang ingin di-scrape
url = 'https://siamik.upnjatim.ac.id/siamik2022/html/siamik/daftarMtKuliah.asp?progdi=409883C3DD51F628BA048C93B2CA511354F70F765E746D00'
base_url = 'https://siamik.upnjatim.ac.id/siamik2022/html/siamik/'
nama_file = 'data_mahasiswa_informatika.csv'

# Mengirim permintaan GET ke URL
response = requests.get(url)

print("Please wait while the data is being scraped...")

# Jika permintaan berhasil (status code 200)
if response.status_code == 200:
    # Parsing halaman HTML menggunakan BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Cari semua baris <tr> dalam tabel
    rows = soup.find_all('tr', onmouseover=True)

    # Inisialisasi list untuk menyimpan data
    data = []

    # Loop melalui setiap baris dan ambil data dari kolom <td>
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 6:  # Pastikan jumlah kolom sesuai
            no = cells[0].get_text(strip=True)
            
            # Mengambil KodeMtKuliah dan Link
            kode_link_tag = cells[1].find('a')
            kode_mtkuliah = kode_link_tag.get_text(strip=True)
            kode_unique = kode_link_tag['href']
            kode_link = base_url + kode_link_tag['href']

            nama_mtkuliah = cells[2].get_text(strip=True)
            sks = cells[3].get_text(strip=True)
            kelas = cells[4].get_text(strip=True)
            jumlah = cells[5].get_text(strip=True)

            # Mengakses halaman dari link yang ada di KodeMtKuliah
            detail_response = requests.get(kode_link)
            if detail_response.status_code == 200:
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                
                # Mencari tabel mahasiswa di halaman detail
                detail_rows = detail_soup.find_all('tr', onmouseover=True)

                # Loop melalui setiap baris di tabel mahasiswa
                for detail_row in detail_rows:
                    detail_cells = detail_row.find_all('td')
                    if len(detail_cells) == 5:  # Pastikan jumlah kolom sesuai
                        detail_no = detail_cells[0].get_text(strip=True)
                        npm = detail_cells[1].get_text(strip=True)
                        nama = detail_cells[2].get_text(strip=True)
                        detail_sks = detail_cells[3].get_text(strip=True)
                        ukt = detail_cells[4].get_text(strip=True)

                        # Simpan data dalam dictionary
                        data.append({
                            'No': no,
                            'KodeMtKuliah': kode_mtkuliah,
                            'NamaMtKuliah': nama_mtkuliah,
                            'SKS': sks,
                            'Kelas': kelas,
                            'Jumlah': jumlah,
                            'Detail_No': detail_no,
                            'NPM': npm,
                            'Nama': nama,
                            'Detail_SKS': detail_sks,
                            'UKT': ukt,
                            'LinkUnique': kode_unique,
                            'Link': kode_link
                        })

    # Konversi data ke DataFrame pandas
    df = pd.DataFrame(data)

    # Simpan ke file CSV
    df.to_csv(nama_file, index=False)

    print("Data berhasil disimpan ke", nama_file)
else:
    print(f"Gagal mengambil halaman web. Status code: {response.status_code}")