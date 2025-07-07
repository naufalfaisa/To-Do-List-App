# TaskMasterPro

Sebuah aplikasi To-Do List berbasis terminal.

## Features

- **ID Otomatis** — Setiap tugas memiliki ID unik otomatis (`T001`, `T002`, dst).
- **Prioritas Tugas** — 4 tingkat prioritas: LOW, MEDIUM, HIGH, URGENT.
- **Deadline & Reminder** — Atur deadline dan dapatkan pengingat untuk tugas yang mendekati tenggat (≤ 3 hari).
- **Tandai Selesai** — Tandai tugas yang telah diselesaikan.
- **Hapus Tugas** — Hapus tugas tertentu dengan ID.
- **Undo / Redo** — Kembalikan atau ulangi perubahan terakhir.
- **Penyimpanan Lokal** — Semua data tersimpan di file `database_todolist.txt`.

## Usage

Jalankan dengan command:

```bash
python TaskMasterPro.py
```

Setelah dijalankan kamu bisa memilih menu berikut:

```bash
[1] Tambah Tugas Baru
[2] Lihat Semua Tugas
[3] Tandai Selesai
[4] Hapus Tugas
[5] Undo Operasi
[6] Redo Operasi
[7] Lihat Reminder
[8] Set Deadline
[9] Keluar
```

## Information

File database_todolist.txt menyimpan setiap tugas dalam format berikut:

```bash
ID|Nama Tugas|Prioritas|Deadline|Status
```
example:

```bash
T001|Belajar GitHub|3|12-07-2025|Belum Selesai
```
## Project Structure

```bash
TaskMasterPro/
│
├── TaskMasterPro.py       # File utama program
└── database_todolist.txt  # File penyimpanan data (akan dibuat otomatis)
```

## Dependencies

- Python 3.x
- Tidak membutuhkan library eksternal (menggunakan os, datetime, collections, queue)

## License

Proyek ini bebas digunakan untuk keperluan pribadi atau edukasi.

## Authors

- **Naufal Faisa**
- **Fuad Rizqi Abrori**

