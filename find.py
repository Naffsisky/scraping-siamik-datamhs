import pandas as pd

# Nama file CSV yang telah diunduh sebelumnya
input_csv_file = 'data_mahasiswa_informatika.csv'
output_csv_file = 'nama_sama_di_kelas_tertentu.csv'

# Kelas yang ingin dicari
kelas_tertentu = ['daftarMahasiswa.asp?kelas=394AB00658A38719F016BE4D2B90081FD109450111E4DDB4&progdi=8F03EB399646C04C3B0DF86396E072BCA7CD81D559C019B2&kode=8DC3AFBFFC26EB76727EE57F9434796C31C58598494EDC893F1AC1F1213CDC54', 'daftarMahasiswa.asp?kelas=D9EB0371437B276C5C3C0C27473534BEB36380195A64D79A&progdi=CC48F718C85E9A22CE96AABF44430CAE11FDE23E897FB58F&kode=5E7D1729E6A57EC0B9B100C4570018F147C7766F8EFEF46D39BF8B7D93BFDA80', 'daftarMahasiswa.asp?kelas=11B5D22E27D6CAF8B63471DFEF7B6BFA2A98A39C5478C6EC&progdi=828F63DE3D90EE7B19E85E1B46A62007D97A4C4FF62D2955&kode=828F63DE3D90EE7B19E85E1B46A620077DF59B744E9B91D5C7E638E78B8320C3', 'daftarMahasiswa.asp?kelas=3E623785EDF687D93F5641A4CB806C826C96CD940CE0E568&progdi=142719B00C350F1E6FC3265F8096DC2C997008F990AD322C&kode=FF639EF0F29835B80415F3B0892A5506C389ED76E4A4E7BF3B35FFAA31D37DD9', 'daftarMahasiswa.asp?kelas=E7B129218A7C0316E839E6AED481486FF4EF12BAFA4788B9&progdi=B15F0D7D9E87BDA2213DC551B545824F3FF5AF410A520C4E&kode=B15F0D7D9E87BDA2213DC551B545824F54944135AECC4CA16C8057A97BD15CAA']

# Baca data dari file CSV
df = pd.read_csv(input_csv_file)

# Pastikan data yang dibaca benar
print("Data yang dibaca dari file CSV:")
print(df.head())

# Filter data berdasarkan kelas tertentu
filtered_df = df[df['LinkUnique'].isin(kelas_tertentu)]

# Menyaring nama yang ada di kedua kelas
names_in_kelas = {}
for kelas in kelas_tertentu:
    names_in_kelas[kelas] = set(filtered_df[filtered_df['LinkUnique'] == kelas]['Nama'])

# Temukan nama yang ada di kedua kelas
common_names = names_in_kelas[kelas_tertentu[0]]
for kelas in kelas_tertentu[1:]:
    common_names &= names_in_kelas[kelas]

# Simpan nama-nama yang ditemukan ke file CSV baru
names_df = pd.DataFrame(common_names, columns=['Nama'])
names_df.to_csv(output_csv_file, index=False)

print("Nama yang sama di kelas", kelas_tertentu, "berhasil disimpan ke:", output_csv_file)