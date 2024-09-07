import curses
import time
import random
from curses import wrapper

# Mendefinisikan senjata sebagai dictionary
senjata = {
    'Pedang panjang': {
        'damage': 6,
        'speed': 3,
        'health': 16,
    },
    'Pedang dua tangan': {
        'damage': 8,
        'speed': 1,
        'health': 18,
    },
    'Busur pendek': {
        'damage': 6,
        'speed': 5,
        'health': 15,
    }
}

# Kategori musuh
musuh_list = {
    'Goblin Hutan': {
        'name': 'Goblin Hutan',
        'damage': 3,
        'speed': 2,
        'health': 20
    },
    # 'Orc': {
    #     'damage': 5,
    #     'speed': 1,
    #     'health': 25
    # }
}

def main(stdscr):
    # Inisialisasi layar
    curses.curs_set(0)  # Menyembunyikan kursor
    stdscr.clear()
    
    # Epilog - Pemilihan Senjata
    epilog = True
    while epilog:
        stdscr.clear()
        stdscr.addstr("=== Kisah Petualangan Hikaru ===\n")
        stdscr.addstr("Bantu Hikaru untuk mengalahkan Raja Iblis dan menyelamatkan dunia!\n")
        stdscr.addstr("\nPilih senjatamu:\n")

        # Menampilkan pilihan senjata
        for i, nama_senjata in enumerate(senjata, 1):
            statistik_senjata = senjata[nama_senjata]
            stdscr.addstr(f"{i}. {nama_senjata} (Damage: {statistik_senjata['damage']}, "
                          f"Speed: {statistik_senjata['speed']}, Health: {statistik_senjata['health']})\n")

        # Mendapatkan input dari pemain
        stdscr.addstr("\nMasukkan pilihan senjatamu : ")
        stdscr.refresh()
        
        try:
            key = stdscr.getkey()
        except:
            key = ''

        # Menampilkan senjata yang dipilih pemain dan melanjutkan permainan
        if key == '1':
            stdscr.addstr("\nKamu memilih Pedang panjang!\n")
            pilihan_senjata = senjata['Pedang panjang']
            epilog = False
        elif key == '2':
            stdscr.addstr("\nKamu memilih Pedang dua tangan!\n")
            pilihan_senjata = senjata['Pedang dua tangan']
            epilog = False
        elif key == '3':
            stdscr.addstr("\nKamu memilih Busur pendek!\n")
            pilihan_senjata = senjata['Busur pendek']
            epilog = False
        else:
            stdscr.addstr("\nPilihan tidak valid! Coba lagi.\n")
        
        if not epilog:
            stdscr.addstr("\nTekan tombol apapun untuk melanjutkan!\n")
        stdscr.refresh()
        stdscr.getch()  # Menunggu pemain menekan tombol

    # Bersihkan layar dan masuk ke Stage 1
    musuh = musuh_list['Goblin Hutan']
    
    stdscr.clear()
    stdscr.addstr("=== Level 1 ===\n")
    stdscr.addstr("\nKamu memasuki hutan gelap dan mendengar suara langkah kaki...\n")
    stdscr.addstr(f"Kamu bertemu dengan {musuh['name']}!\n")
    stdscr.addstr("Bersiaplah untuk pertempuran!\n")
    stdscr.refresh()
    time.sleep(4)  # Memberikan waktu bagi pemain untuk membaca pesan

    # Masuk ke loop Stage 1
    stage1 = True
    while stage1:
        stdscr.clear()

        # Tampilkan status pemain dan musuh
        stdscr.addstr("=== Status ===\n")
        stdscr.addstr("Status Pemain:\n")
        stdscr.addstr(f"Health : {pilihan_senjata['health']}\n")
        stdscr.addstr(f"Damage : {pilihan_senjata['damage']}\n")
        stdscr.addstr(f"Speed  : {pilihan_senjata['speed']}\n\n")
        
        stdscr.addstr(f"Status {musuh['name']}:\n")
        stdscr.addstr(f"Health : {musuh['health']}\n")
        stdscr.addstr(f"Damage : {musuh['damage']}\n")
        stdscr.addstr(f"Speed  : {musuh['speed']}\n")

        stdscr.addstr("\n=== Aksi ===\n")
        stdscr.addstr("Tekan 'a' untuk menyerang, 'd' untuk menghindar, atau 'l' untuk lari!\n")
        stdscr.refresh()

        try:
            action = stdscr.getkey()
        except:
            action = ''

        # Aksi pemain
        if action.lower() == 'a':
            # Pemain menyerang
            stdscr.addstr("\nKamu memilih untuk menyerang!\n")
            stdscr.refresh()
            time.sleep(2)

            # Musuh memilih tindakan (50% kemungkinan menyerang, 50% kemungkinan menghindar)
            musuh_aksi = random.choice(['serang', 'menghindar'])
            if musuh_aksi == 'menghindar' and musuh['speed'] >= pilihan_senjata['speed']:
                stdscr.addstr(f"{musuh['name']} berhasil menghindar dari seranganmu!\n")
            else:
                musuh['health'] -= pilihan_senjata['damage']
                stdscr.addstr(f"Kamu menyerang {musuh['name']} dan mengurangi {pilihan_senjata['damage']} health musuh!\n\n")
            
            stdscr.refresh()
            time.sleep(2)

            if musuh['health'] <= 0:
                stdscr.addstr(f"\nKamu telah mengalahkan {musuh['name']}!\n")
                stdscr.refresh()
                stage1 = False
            else:
                # Serangan balasan dari musuh
                if musuh_aksi == 'serang':
                    stdscr.addstr(f"{musuh['name']} menyerang balik!\n")
                    pilihan_senjata['health'] -= musuh['damage']
                    stdscr.addstr(f"{musuh['name']} menyerang kamu dan mengurangi {musuh['damage']} health kamu!\n")
                else:
                    stdscr.addstr(f"{musuh['name']} memilih untuk bertahan dan menghindar!\n")
                stdscr.refresh()
                time.sleep(2)

                if pilihan_senjata['health'] <= 0:
                    stdscr.addstr("\nKamu kalah dalam pertempuran...\n")
                    stdscr.refresh()
                    stage1 = False
        
        elif action.lower() == 'd':
            # Pemain mencoba menghindar
            stdscr.addstr(f"Kamu mencoba menghindar!\n")
            stdscr.refresh()
            time.sleep(2)

            if pilihan_senjata['speed'] > musuh['speed']:
                stdscr.addstr(f"Kamu berhasil menghindar dari serangan {musuh['name']}!\n")
            else:
                stdscr.addstr(f"Kamu gagal menghindar dari serangan {musuh['name']}!\n")
                pilihan_senjata['health'] -= musuh['damage']
                stdscr.addstr(f"{musuh['name']} menyerang kamu dan mengurangi {musuh['damage']} health kamu!\n")
            stdscr.refresh()
            time.sleep(2)

        elif action.lower() == 'l':
            stdscr.addstr("\nKamu memutuskan untuk lari dari pertarungan!\n")
            stdscr.refresh()
            stage1 = False
            time.sleep(2)
        else:
            stdscr.addstr("\nAksi tidak valid! Coba lagi.\n")
            stdscr.refresh()
            time.sleep(2)

    # Setelah pertarungan selesai
    stdscr.clear()
    stdscr.addstr("\n=== Pertarungan Selesai ===\n")
    if pilihan_senjata['health'] > 0 and musuh['health'] <= 0:
        stdscr.addstr(f"Selamat! Kamu berhasil mengalahkan {musuh['name']} dan melanjutkan petualanganmu.\n")
    elif pilihan_senjata['health'] <= 0:
        stdscr.addstr("Sayang sekali, kamu telah kalah dalam pertempuran.\n")
    else:
        stdscr.addstr("Kamu berhasil keluar dari pertarungan.\n")
    
    stdscr.addstr("\nTekan tombol apapun untuk keluar dari permainan.\n")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
