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
    stdscr.clear()
    
    # Epilog - Pemilihan Senjata
    epilog = True
    while epilog:
        stdscr.clear()
        stdscr.addstr("Ini adalah kisah petualangan Hikaru!\n")
        stdscr.addstr("Bantu Hikaru untuk mengalahkan Raja Iblis dan menyelamatkan dunia!\n")
        stdscr.addstr("\nPilih senjatamu!\n")

        # Menampilkan pilihan senjata
        for i, nama_senjata in enumerate(senjata, 1):
            statistik_senjata = senjata[nama_senjata]
            stdscr.addstr(f"{i}. {nama_senjata} (damage = {statistik_senjata['damage']}, "
                          f"speed = {statistik_senjata['speed']}, health = {statistik_senjata['health']})\n")

        # Mendapatkan input dari pemain
        stdscr.addstr("\nMasukkan pilihan senjatamu: ")
        stdscr.refresh()
        
        key = stdscr.getkey()

        # Menampilkan senjata yang dipilih pemain dan melanjutkan permainan
        if key == '1':
            stdscr.addstr("\nKamu memilih Pedang panjang!\n")
            stdscr.addstr("\nTekan tombol apapun untuk melanjutkan!\n")
            pilihan_senjata = senjata['Pedang panjang']
            epilog = False
        elif key == '2':
            stdscr.addstr("\nKamu memilih Pedang dua tangan!\n")
            stdscr.addstr("\nTekan tombol apapun untuk melanjutkan!\n")
            pilihan_senjata = senjata['Pedang dua tangan']
            epilog = False
        elif key == '3':
            stdscr.addstr("\nKamu memilih Busur pendek!\n")
            stdscr.addstr("\nTekan tombol apapun untuk melanjutkan!\n")
            pilihan_senjata = senjata['Busur pendek']
            epilog = False
        else:
            stdscr.addstr("\nPilihan tidak valid! Coba lagi.\n")
        
        stdscr.refresh()
        stdscr.getch()  # Menunggu pemain menekan tombol

    # Bersihkan layar dan masuk ke Level 1
    stdscr.clear()
    stdscr.addstr("Level 1: Selamat datang di dunia yang penuh tantangan!\n")
    stdscr.addstr("\nKamu memasuki hutan gelap dan mendengar suara langkah kaki...\n")
    stdscr.addstr("Kamu bertemu dengan Goblin Hutan!\n")
    stdscr.addstr("Bersiaplah untuk pertempuran!\n")
    stdscr.refresh()
    time.sleep(2)

    # Masuk ke loop Level 1
    level1 = True
    while level1:
        stdscr.clear()

        # Tampilkan status pemain dan goblin
        stdscr.addstr("Status Pemain:\n")
        stdscr.addstr(f"Health: {pilihan_senjata['health']}\n")
        stdscr.addstr(f"Damage: {pilihan_senjata['damage']}\n")
        stdscr.addstr(f"Speed: {pilihan_senjata['speed']}\n\n")
        
        stdscr.addstr("Status Goblin:\n")
        stdscr.addstr(f"Health: {goblin['health']}\n")
        stdscr.addstr(f"Damage: {goblin['damage']}\n")
        stdscr.addstr(f"Speed: {goblin['speed']}\n")

        stdscr.addstr("\nTekan 'a' untuk menyerang, atau 'l' untuk lari!\n")
        stdscr.refresh()

        action = stdscr.getkey()

        if action == 'a':
            # Tentukan siapa yang menyerang duluan berdasarkan speed
            if pilihan_senjata['speed'] >= goblin['speed']:
                # Pemain menyerang duluan
                goblin['health'] -= pilihan_senjata['damage']
                stdscr.addstr(f"\nKamu menyerang goblin dan mengurangi {pilihan_senjata['damage']} health goblin!\n")
                
                if goblin['health'] <= 0:
                    stdscr.addstr("\nKamu telah mengalahkan Goblin!\n")
                    level1 = False
                else:
                    # Goblin menyerang balik
                    pilihan_senjata['health'] -= goblin['damage']
                    stdscr.addstr(f"Goblin menyerang balik dan mengurangi {goblin['damage']} health kamu!\n")
                    if pilihan_senjata['health'] <= 0:
                        stdscr.addstr("\nKamu kalah dalam pertempuran...\n")
                        level1 = False
            else:
                # Goblin menyerang duluan
                pilihan_senjata['health'] -= goblin['damage']
                stdscr.addstr(f"\nGoblin menyerang lebih cepat dan mengurangi {goblin['damage']} health kamu!\n")
                
                if pilihan_senjata['health'] <= 0:
                    stdscr.addstr("\nKamu kalah dalam pertempuran...\n")
                    level1 = False
                else:
                    # Pemain menyerang setelah goblin
                    goblin['health'] -= pilihan_senjata['damage']
                    stdscr.addstr(f"Kamu menyerang goblin dan mengurangi {pilihan_senjata['damage']} health goblin!\n")
                    if goblin['health'] <= 0:
                        stdscr.addstr("\nKamu telah mengalahkan Goblin!\n")
                        level1 = False
        elif action == 'l':
            stdscr.addstr("\nKamu memutuskan untuk lari dari pertarungan!\n")
            level1 = False
        else:
            stdscr.addstr("\nAksi tidak valid! Coba lagi.\n")
        
        stdscr.refresh()
        stdscr.getch()  # Menunggu sebelum melanjutkan loop berikutnya

    stdscr.addstr("\nTekan tombol apapun untuk keluar dari permainan.\n")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
