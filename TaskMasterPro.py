import os
import datetime
from collections import deque
from queue import PriorityQueue

# File database
FILE_NAME = "database_todolist.txt"

undo_stack = deque()
redo_stack = deque()

# Generate id
def generate_id(todolist):
    if not todolist:
        return "T001"
    existing_ids = [int(tugas['id'][1:]) for tugas in todolist if tugas['id'].startswith('T')]
    next_id = max(existing_ids, default=0) + 1
    return f"T{next_id:03d}"

# Label prioritas
def label_prioritas(nilai):
    mapping = {
        1: "LOW",
        2: "MEDIUM",
        3: "HIGH",
        4: "URGENT"
    }
    return mapping.get(nilai, f"TIDAK DIKETAHUI ({nilai})")

# Simpan ke database
def save_todo(todolist):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for item in todolist:
            f.write(f"{item['id']}|{item['tugas']}|{item['prioritas']}|{item['deadline']}|{item['status']}\n")

# Muat dari database
def load_todo():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        data = []
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
                id_, tugas, prioritas, deadline, status = parts
                data.append({
                    'id': id_,
                    'tugas': tugas,
                    'prioritas': int(prioritas),
                    'deadline': deadline,
                    'status': status
                })
    return data

# Tambah Tugas
def tambah_tugas(todolist):
    nama_tugas = input("Nama tugas: ").strip()
    if not nama_tugas:
        print("\nNama tugas tidak boleh kosong!")
        input("\nENTER untuk kembali")
        return
    
    try:
        prioritas = int(input("Prioritas (1:Low, 2:Medium, 3:High, 4:Urgent): "))
        if prioritas not in [1, 2, 3, 4]:
            raise ValueError
    except ValueError:
        print("\nInput tidak valid!")
        input("\nENTER untuk kembali")
        return

    deadline = input("Masukkan deadline baru (DD-MM-YYYY): ").strip()
    try:
        deadline_obj = datetime.datetime.strptime(deadline, "%d-%m-%Y")
        deadline = deadline_obj.strftime("%d-%m-%Y")
    except ValueError:
        print("\nFormat tanggal tidak valid!")
        input("\nENTER untuk kembali")
        return

    if nama_tugas and deadline:
        id_tugas = generate_id(todolist)
        tugas_baru = {
            'id': id_tugas,
            'tugas': nama_tugas,
            'prioritas': prioritas,
            'deadline': deadline,
            'status': "Belum Selesai"
        }
        todolist.append(tugas_baru)
        undo_stack.append(("hapus", tugas_baru))
        redo_stack.clear()
        save_todo(todolist)
        print(f"\nTugas berhasil ditambahkan dengan ID: {id_tugas}")
    else:
        print("\nInput tidak lengkap")
    input("\nENTER untuk kembali")

# Lihat Tugas
def lihat_tugas(todolist):
    if not todolist:
        print("\nTugas kosong")
    else:
        sorted_list = sorted(todolist, key=lambda x: -x['prioritas'])
        print()
        for tugas in sorted_list:
            label = label_prioritas(tugas['prioritas'])
            print(f"-[{label}] {tugas['id']} | {tugas['tugas']} | Deadline: {tugas['deadline']} | [{tugas['status']}]")
    input("\nENTER untuk kembali")

def cari_tugas_by_id(todolist, id_tugas):
    for tugas in todolist:
        if tugas['id'] == id_tugas:
            return tugas
    return None

# Tandai selesai
def tandai_selesai(todolist):
    if not todolist:
        print("\nTugas kosong")
        input("\nENTER untuk kembali")
        return

    sorted_list = sorted(todolist, key=lambda x: -x['prioritas'])
    print()
    for tugas in sorted_list:
        label = label_prioritas(tugas['prioritas'])
        print(f"[{label}] {tugas['id']}: {tugas['tugas']} [{tugas['status']}]")

    id_tugas = input("\nMasukkan ID tugas yang ingin ditandai selesai: ").strip().upper()
    tugas = cari_tugas_by_id(todolist, id_tugas)
    if tugas:
        status_lama = tugas['status']
        tugas['status'] = "Selesai"
        undo_stack.append(("edit status", tugas['id'], status_lama))
        redo_stack.clear()
        save_todo(todolist)
        print("\nTugas ditandai sebagai selesai")
    else:
        print("\nID tidak ditemukan")
    input("\nENTER untuk kembali")

# Hapus Tugas
def hapus_tugas(todolist):
    if not todolist:
        print("\nTugas kosong")
        input("\nENTER untuk kembali")
        return

    sorted_list = sorted(todolist, key=lambda x: -x['prioritas'])
    print()
    for tugas in sorted_list:
        label = label_prioritas(tugas['prioritas'])
        print(f"[{label}] {tugas['id']}: {tugas['tugas']} [{tugas['status']}]")

    id_tugas = input("\nMasukkan ID tugas yang ingin dihapus: ").strip().upper()
    tugas = cari_tugas_by_id(todolist, id_tugas)
    if tugas:
        todolist.remove(tugas)
        undo_stack.append(("tambah", tugas))
        redo_stack.clear()
        save_todo(todolist)
        print(f"\nTugas '{tugas['tugas']}' berhasil dihapus")
    else:
        print("\nID tidak ditemukan")
    input("\nENTER untuk kembali")

# Undo
def undo(todolist):
    if not undo_stack:
        print("\nTidak ada yang bisa di-undo")
    else:
        aksi = undo_stack.pop()
        print(f"\nUndo: {aksi[0]}")
        if aksi[0] == "hapus":
            tugas = aksi[1]
            todolist.remove(tugas)
            redo_stack.append(("tambah", tugas))
        elif aksi[0] == "tambah":
            tugas = aksi[1]
            todolist.append(tugas)
            redo_stack.append(("hapus", tugas))
        elif aksi[0] == "edit status":
            tugas = cari_tugas_by_id(todolist, aksi[1])
            if tugas:
                redo_stack.append(("edit status", tugas['id'], tugas['status']))
                tugas['status'] = aksi[2]
        elif aksi[0] == "edit deadline":
            tugas = cari_tugas_by_id(todolist, aksi[1])
            if tugas:
                redo_stack.append(("edit deadline", tugas['id'], tugas['deadline']))
                tugas['deadline'] = aksi[2]
        save_todo(todolist)
    input("\nENTER untuk kembali")

# Redo
def redo(todolist):
    if not redo_stack:
        print("\nTidak ada yang bisa di-redo")
    else:
        aksi = redo_stack.pop()
        print(f"\nRedo: {aksi[0]}")
        if aksi[0] == "hapus":
            tugas = aksi[1]
            todolist.remove(tugas)
            undo_stack.append(("tambah", tugas))
        elif aksi[0] == "tambah":
            tugas = aksi[1]
            todolist.append(tugas)
            undo_stack.append(("hapus", tugas))
        elif aksi[0] == "edit status":
            tugas = cari_tugas_by_id(todolist, aksi[1])
            if tugas:
                undo_stack.append(("edit status", tugas['id'], tugas['status']))
                tugas['status'] = aksi[2]
        elif aksi[0] == "edit deadline":
            tugas = cari_tugas_by_id(todolist, aksi[1])
            if tugas:
                undo_stack.append(("edit deadline", tugas['id'], tugas['deadline']))
                tugas['deadline'] = aksi[2]
        save_todo(todolist)
    input("\nENTER untuk kembali")

# Reminder
def lihat_reminder(todolist):
    if not todolist:
        print("\nTugas kosong")
        input("\nENTER untuk kembali")
        return

    today = datetime.date.today()
    pq = PriorityQueue()
    
    for tugas in todolist:
        try:
            deadline = datetime.datetime.strptime(tugas['deadline'], "%d-%m-%Y").date()
            days_left = (deadline - today).days
            if tugas['status'].lower() != "selesai" and 0 <= days_left <= 3:
                # Tambahkan ke antrian prioritas: (hari tersisa, tugas)
                pq.put((days_left, tugas))
        except ValueError:
            continue

    if pq.empty():
        print("\nTidak ada tugas mendekati deadline")
    else:
        print("\nTugas dengan deadline dalam 3 hari (urutan terdekat):")
        while not pq.empty():
            _, tugas = pq.get()
            label = label_prioritas(tugas['prioritas'])
            print(f"-[{label}] {tugas['id']} | {tugas['tugas']} | Deadline: {tugas['deadline']} | [{tugas['status']}]")

    input("\nENTER untuk kembali")

# Set Deadline
def set_deadline(todolist):
    if not todolist:
        print("\nTugas kosong")
        input("\nENTER untuk kembali")
        return

    sorted_list = sorted(todolist, key=lambda x: -x['prioritas'])
    print()
    for tugas in sorted_list:
        label = label_prioritas(tugas['prioritas'])
        print(f"[{label}] {tugas['id']}: {tugas['tugas']} [{tugas['status']}]")

    id_tugas = input("\nMasukkan ID tugas yang ingin diubah deadlinenya: ").strip().upper()
    tugas = cari_tugas_by_id(todolist, id_tugas)
    if not tugas:
        print("\nID tidak ditemukan")
        input("\nENTER untuk kembali")
        return

    deadline = input("Masukkan deadline baru (DD-MM-YYYY): ").strip()
    try:
        deadline_obj = datetime.datetime.strptime(deadline, "%d-%m-%Y")
        deadline = deadline_obj.strftime("%d-%m-%Y")
    except ValueError:
        print("\nFormat tanggal tidak valid!")
        input("\nENTER untuk kembali")
        return

    undo_stack.append(("edit deadline", tugas['id'], tugas['deadline']))
    redo_stack.clear()
    tugas['deadline'] = deadline
    save_todo(todolist)
    print("\nDeadline berhasil diperbarui")
    input("\nENTER untuk kembali")

# MENU
def menu():
    todolist = load_todo()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("========== TASKMASTER PRO ==========")
        print("Silakan pilih menu:")
        print("[1] Tambah Tugas Baru")
        print("[2] Lihat Semua Tugas")
        print("[3] Tandai Selesai")
        print("[4] Hapus Tugas")
        print("[5] Undo Operasi")
        print("[6] Redo Operasi")
        print("[7] Lihat Reminder")
        print("[8] Set Deadline")
        print("[9] Keluar")
        print("====================================")
        pilihan = input("Pilih: ")

        if pilihan == "1":
            tambah_tugas(todolist)
        elif pilihan == "2":
            lihat_tugas(todolist)
        elif pilihan == "3":
            tandai_selesai(todolist)
        elif pilihan == "4":
            hapus_tugas(todolist)
        elif pilihan == "5":
            undo(todolist)
        elif pilihan == "6":
            redo(todolist)
        elif pilihan == "7":
            lihat_reminder(todolist)
        elif pilihan == "8":
            set_deadline(todolist)
        elif pilihan == "9":
            print("\nTerima kasih telah menggunakan TASKMASTER PRO\n")
            break
        else:
            print("\nPilihan tidak valid.")
            input("\nENTER untuk kembali")

# Jalankan
menu()
