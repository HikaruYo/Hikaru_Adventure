import curses
import time
from curses import wrapper

# Mendefinisikan senjata sebagai dictionary
senjata = {
    'Pedang panjang': {
        'damage': 5,
        'speed': 3,
        'health': 14,
    },
    'Pedang dua tangan': {
        'damage': 8,
        'speed': 1,
        'health': 18,
    },
    'Busur pendek': {
        'damage': 4,
        'speed': 6,
        'health': 10,
    }
}

# Status lawan
goblin = {
    'damage': 3,
    'speed': 2,
    'health': 10
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

    # Bersihkan layar dan masuk ke Level 1
    stdscr.clear()
    stdscr.addstr("=== Level 1 ===\n")
    stdscr.addstr("\nKamu memasuki hutan gelap dan mendengar suara langkah kaki...\n")
    stdscr.addstr("Kamu bertemu dengan Goblin Hutan!\n")
    stdscr.addstr("Bersiaplah untuk pertempuran!\n")
    stdscr.refresh()
    time.sleep(5)  # Memberikan waktu bagi pemain untuk membaca pesan

    # Masuk ke loop Level 1
    level1 = True
    while level1:
        stdscr.clear()

        # Tampilkan status pemain dan goblin
        stdscr.addstr("=== Status ===\n")
        stdscr.addstr("Status Pemain:\n")
        stdscr.addstr(f"Health : {pilihan_senjata['health']}\n")
        stdscr.addstr(f"Damage : {pilihan_senjata['damage']}\n")
        stdscr.addstr(f"Speed  : {pilihan_senjata['speed']}\n\n")
        
        stdscr.addstr("Status Goblin:\n")
        stdscr.addstr(f"Health : {goblin['health']}\n")
        stdscr.addstr(f"Damage : {goblin['damage']}\n")
        stdscr.addstr(f"Speed  : {goblin['speed']}\n")

        stdscr.addstr("\n=== Aksi ===\n")
        stdscr.addstr("Tekan 'a' untuk menyerang, atau 'l' untuk lari!\n")
        stdscr.refresh()

        try:
            action = stdscr.getkey()
        except:
            action = ''

        if action.lower() == 'a':
            # Tentukan siapa yang menyerang duluan berdasarkan speed
            if pilihan_senjata['speed'] >= goblin['speed']:
                # Pemain menyerang duluan
                stdscr.addstr("\nKamu menyerang duluan!\n")
                stdscr.refresh()
                time.sleep(3)

                # Pemain menyerang
                goblin['health'] -= pilihan_senjata['damage']
                stdscr.addstr(f"Kamu menyerang goblin dan mengurangi {pilihan_senjata['damage']} health goblin!\n")
                stdscr.refresh()
                time.sleep(2)

                if goblin['health'] <= 0:
                    stdscr.addstr("\nKamu telah mengalahkan Goblin!\n")
                    stdscr.refresh()
                    level1 = False
                else:
                    # Goblin menyerang balik
                    stdscr.addstr("\nGoblin menyerang balik!\n")
                    stdscr.refresh()
                    time.sleep(3)

                    pilihan_senjata['health'] -= goblin['damage']
                    stdscr.addstr(f"Goblin menyerang kamu dan mengurangi {goblin['damage']} health kamu!\n")
                    stdscr.refresh()
                    time.sleep(2)

                    if pilihan_senjata['health'] <= 0:
                        stdscr.addstr("\nKamu kalah dalam pertempuran...\n")
                        stdscr.refresh()
                        level1 = False
            else:
                # Goblin menyerang duluan
                stdscr.addstr("\nGoblin menyerang duluan!\n")
                stdscr.refresh()
                time.sleep(3)

                # Goblin menyerang
                pilihan_senjata['health'] -= goblin['damage']
                stdscr.addstr(f"Goblin menyerang kamu dan mengurangi {goblin['damage']} health kamu!\n")
                stdscr.refresh()
                time.sleep(2)

                if pilihan_senjata['health'] <= 0:
                    stdscr.addstr("\nKamu kalah dalam pertempuran...\n")
                    stdscr.refresh()
                    level1 = False
                else:
                    # Pemain menyerang setelah goblin
                    stdscr.addstr("\nKamu menyerang goblin!\n")
                    stdscr.refresh()
                    time.sleep(3)

                    goblin['health'] -= pilihan_senjata['damage']
                    stdscr.addstr(f"Kamu menyerang goblin dan mengurangi {pilihan_senjata['damage']} health goblin!\n")
                    stdscr.refresh()
                    time.sleep(2)

                    if goblin['health'] <= 0:
                        stdscr.addstr("\nKamu telah mengalahkan Goblin!\n")
                        stdscr.refresh()
                        level1 = False

        elif action.lower() == 'l':
            stdscr.addstr("\nKamu memutuskan untuk lari dari pertarungan!\n")
            stdscr.refresh()
            level1 = False
            time.sleep(2)
        else:
            stdscr.addstr("\nAksi tidak valid! Coba lagi.\n")
            stdscr.refresh()
            time.sleep(2)

    # Setelah pertarungan selesai
    stdscr.clear()
    stdscr.addstr("\n=== Pertarungan Selesai ===\n")
    if pilihan_senjata['health'] > 0 and goblin['health'] <= 0:
        stdscr.addstr("Selamat! Kamu berhasil mengalahkan Goblin dan melanjutkan petualanganmu.\n")
    elif pilihan_senjata['health'] <= 0:
        stdscr.addstr("Sayang sekali, kamu telah kalah dalam pertempuran.\n")
    else:
        stdscr.addstr("Kamu berhasil keluar dari pertarungan.\n")
    
    stdscr.addstr("\nTekan tombol apapun untuk keluar dari permainan.\n")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
