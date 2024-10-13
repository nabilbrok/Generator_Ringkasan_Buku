import subprocess
import sys

# Fungsi untuk menginstal pustaka jika belum ada
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Daftar pustaka yang dibutuhkan
required_packages = ['requests']

# Memeriksa dan menginstal setiap pustaka yang dibutuhkan
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} tidak ditemukan, menginstal...")
        install(package)

import requests
import json
import os
from datetime import datetime

# Fungsi untuk mengambil data buku dari Google Books API
def get_books_data(query, file_name, max_results=5, lang='id', total_pages=1):
    url_template = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict={lang}&maxResults={max_results}&startIndex={{}}"
    
    with open(file_name, 'w', encoding='utf-8') as file:
        for page in range(total_pages):
            start_index = page * max_results
            url = url_template.format(start_index)
            response = requests.get(url)

            if response.status_code == 200:
                books = response.json()
                for item in books.get('items', []):
                    title = item['volumeInfo'].get('title', 'Tidak ada judul')
                    authors = item['volumeInfo'].get('authors', ['Tidak ada pengarang'])
                    publisher = item['volumeInfo'].get('publisher', 'Tidak ada penerbit')
                    description = item['volumeInfo'].get('description', 'Tidak ada ringkasan')
                    
                    # Menulis hasil ke file
                    file.write(f"Judul: {title}\n")
                    file.write(f"Pengarang: {', '.join(authors)}\n")
                    file.write(f"Penerbit: {publisher}\n")
                    file.write(f"Ringkasan: {description}\n")
                    file.write('-' * 40 + '\n')
                    
                    # Juga mencetak ke konsol
                    print(f"Judul: {title}\n")
                    print(f"Pengarang: {', '.join(authors)}\n")
                    print(f"Penerbit: {publisher}\n")
                    print(f"Ringkasan: {description}\n")
                    print('-' * 40 + '\n')
            else:
                print(f"Error: {response.status_code}")
                break
    
    print(f"File anda disimpan sebagai {file_name}")


# Mengambil input dari pengguna
buku_apa = input("Mau buku apa? (fiksi/nonfiksi): ")
jumlah_halaman = int(input("Berapa halaman hasil yang ingin diambil? "))

# Buat folder jika belum ada
folder = "file_ringkasan_indo"
if not os.path.exists(folder):
    os.makedirs(folder)

# Menambahkan timestamp agar file tidak overwrite
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
nama_file = f"{folder}/{buku_apa}_{timestamp}.txt"

# Mengambil data buku fiksi berbahasa Indonesia
if buku_apa.lower() == "fiksi":
    print("Buku Fiksi:")
    get_books_data(f"fiction", nama_file, max_results=5, lang='id', total_pages=jumlah_halaman)

# Mengambil data buku non-fiksi berbahasa Indonesia
elif buku_apa.lower() == "nonfiksi":
    print("Buku Non-Fiksi:")
    get_books_data(f"non-fiction", nama_file, "buku_nonfiksi_indo.txt", max_results=5, lang='id', total_pages=jumlah_halaman)

keluar = input("Tekan 'Enter' untuk keluar...")
