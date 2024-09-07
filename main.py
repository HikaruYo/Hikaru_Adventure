import curses, time, random
from curses import wrapper

# Mendefinisikan senjata sebagai dictionary
senjata = {
    'Pedang panjang': {
        'damage': 6,
        'speed': 3,
        'health': 16,
        'max_health': 16,
    },
    'Pedang dua tangan': {
        'damage': 8,
        'speed': 1,
        'health': 18,
        'max_health': 18,
    },
    'Busur pendek': {
        'damage': 6,
        'speed': 5,
        'health': 15,
        'max_health': 15,
    }
}

# Kategori musuh
musuh_list = {
    'Goblin Hutan': {
        'name': 'Goblin Hutan',
        'damage': 3,
        'speed': 2,
        'health': 20,
        'drop_xp': 10,
    },
    'Orc': {
        'name': 'Orc',
        'damage': 5,
        'speed': 1,
        'health': 25,
        'drop_xp': 20,
    }
}

def level_up(stdscr, player_stats):
    # Isi penuh health sebelum memilih stat
    player_stats['health'] = player_stats['max_health']
    
    # Menawarkan peningkatan stat
    choice_made = False
    while not choice_made:
        stdscr.clear()
        stdscr.addstr("\nKamu naik level! Pilih salah satu stat untuk ditingkatkan:\n")
        stdscr.addstr("1. Health\n")
        stdscr.addstr("2. Damage\n")
        stdscr.addstr("3. Speed\n")
        stdscr.refresh()
        
        choice = stdscr.getkey()  # Menggunakan stdscr.getkey() untuk mendapatkan input

        if choice == '1':
            player_stats['max_health'] += 5
            player_stats['health'] = player_stats['max_health']
            stdscr.addstr(f"Health kamu meningkat menjadi {player_stats['max_health']}\n")
            choice_made = True
        elif choice == '2':
            player_stats['damage'] += 2
            stdscr.addstr(f"Damage kamu meningkat menjadi {player_stats['damage']}\n")
            choice_made = True
        elif choice == '3':
            player_stats['speed'] += 1
            stdscr.addstr(f"Speed kamu meningkat menjadi {player_stats['speed']}\n")
            choice_made = True
        else:
            stdscr.addstr("Pilihan tidak valid! Coba lagi.\n")
        
        stdscr.refresh()
        time.sleep(2)

def main(stdscr):
    # Inisialisasi layar
    curses.curs_set(0)  # Menyembunyikan kursor
    stdscr.clear()
    
    # Inisialisasi level pemain
    player_level = 1
    player_exp = 0
    exp_to_level_2 = 8
    exp_to_level_3 = 16
    
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
    drop_xp = musuh['drop_xp']

    stdscr.clear()
    stdscr.addstr("=== Level 1 ===\n")
    stdscr.addstr("\nKamu memasuki hutan gelap dan mendengar suara langkah kaki...\n")
    stdscr.addstr(f"Kamu bertemu dengan {musuh['name']}!\n")
    stdscr.addstr("Bersiaplah untuk pertempuran!\n")
    stdscr.refresh()
    time.sleep(4)

    # Masuk ke loop Stage 1
    stage1 = True
    while stage1:
        stdscr.clear()

        # Tampilkan status pemain dan musuh
        stdscr.addstr("=== Status ===\n")
        stdscr.addstr(f"Level Pemain : {player_level}\n")
        stdscr.addstr("Status Pemain:\n")
        stdscr.addstr(f"Health : {pilihan_senjata['health']}\n")
        stdscr.addstr(f"Damage : {pilihan_senjata['damage']}\n")
        stdscr.addstr(f"Speed  : {pilihan_senjata['speed']}\n")
        stdscr.addstr(f"XP     : {player_exp}\n\n")
        
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
            if musuh_aksi == 'menghindar':
                if musuh['speed'] >= pilihan_senjata['speed']:
                    stdscr.addstr(f"{musuh['name']} berhasil menghindar dari seranganmu!\n")
                else:
                    stdscr.addstr(f"{musuh['name']} gagal menghindar karena kecepatan kamu lebih tinggi!\n")
                    musuh['health'] -= pilihan_senjata['damage']
                    stdscr.addstr(f"Kamu menyerang {musuh['name']} dan mengurangi {pilihan_senjata['damage']} health musuh!\n")
                    # Musuh tidak bisa menyerang balik jika gagal menghindar
                    stdscr.addstr(f"{musuh['name']} terlalu lambat untuk menyerang balik!\n")
            else:
                musuh['health'] -= pilihan_senjata['damage']
                stdscr.addstr(f"Kamu menyerang {musuh['name']} dan mengurangi {pilihan_senjata['damage']} health musuh!\n")
                # Musuh menyerang balik jika tidak menghindar
                stdscr.addstr(f"{musuh['name']} menyerang balik!\n")
                pilihan_senjata['health'] -= musuh['damage']
                stdscr.addstr(f"{musuh['name']} memberikan {musuh['damage']} damage!\n")

            stdscr.refresh()
            time.sleep(2)

            if pilihan_senjata['health'] <= 0:
                stdscr.addstr("\nKamu telah dikalahkan!\n")
                stdscr.refresh()
                time.sleep(3)
                break

            if musuh['health'] <= 0:
                stdscr.addstr(f"\nKamu telah mengalahkan {musuh['name']}!\n")
                stdscr.refresh()
                stage1 = False
                player_exp += drop_xp


        elif action.lower() == 'd':
            stdscr.addstr("\nKamu memilih untuk menghindar!\n")
            stdscr.refresh()
            time.sleep(2)

            if musuh['speed'] >= pilihan_senjata['speed']:
                stdscr.addstr(f"{musuh['name']} menyerangmu sebelum kamu bisa menghindar!\n")
                pilihan_senjata['health'] -= musuh['damage']
            else:
                stdscr.addstr(f"Kamu berhasil menghindari serangan {musuh['name']}!\n")
            
            stdscr.refresh()
            time.sleep(2)

            if pilihan_senjata['health'] <= 0:
                stdscr.addstr("\nKamu telah dikalahkan!\n")
                stdscr.refresh()
                time.sleep(3)
                break

        elif action.lower() == 'l':
            stdscr.addstr("\nKamu memilih untuk melarikan diri!\n")
            stdscr.refresh()
            time.sleep(2)
            stdscr.addstr(f"Kamu berhasil lari dari {musuh['name']}!\n")
            stdscr.refresh()
            break
        else:
            stdscr.addstr("\nAksi tidak valid, coba lagi!\n")
            stdscr.refresh()

        # Pemain kalah
        if pilihan_senjata['health'] <= 0:
            stdscr.addstr("\nKamu telah dikalahkan!\n")
            stdscr.refresh()
            time.sleep(3)
            break
    
    # Lanjut ke stage 2 jika pemain menang
    if not stage1:
        if player_exp >= exp_to_level_2:
            stdscr.addstr("\nKamu naik level ke Level 2!\n")
            stdscr.refresh()
            level_up(stdscr, pilihan_senjata)
            player_level = 2
        
        # Mulai Stage 2
        stdscr.clear()
        stdscr.addstr("=== Level 2 ===\n")
        stdscr.addstr("\nKamu memasuki rawa-rawa dan merasakan guncangan pada tanah...\n")
        stdscr.addstr(f"Kamu bertemu dengan {musuh['name']}!\n")
        stdscr.addstr("Bersiaplah untuk pertempuran!\n")
        stdscr.refresh()
        time.sleep(4)

        musuh = musuh_list['Orc']  # Stage 2 musuh

        stdscr.clear()
        stdscr.addstr("=== Level 2 ===\n")
        stdscr.addstr(f"Kamu bertemu dengan {musuh['name']}! Bersiaplah untuk bertarung lagi.\n")
        stdscr.refresh()

        stage2 = True
        while stage2:
            stdscr.clear()
            
            # Tampilkan status pemain dan musuh
            stdscr.addstr("=== Status ===\n")
            stdscr.addstr(f"Level Pemain : {player_level}\n")
            stdscr.addstr("Status Pemain:\n")
            stdscr.addstr(f"Health : {pilihan_senjata['health']}\n")
            stdscr.addstr(f"Damage : {pilihan_senjata['damage']}\n")
            stdscr.addstr(f"Speed  : {pilihan_senjata['speed']}\n")
            stdscr.addstr(f"XP     : {player_exp}\n\n")
            
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

            # Logika bertarung mirip seperti di stage 1
            if action.lower() == 'a':
                stdscr.addstr("\nKamu memilih untuk menyerang!\n")
                stdscr.refresh()
                time.sleep(2)

                # Musuh memilih tindakan (50% kemungkinan menyerang, 50% kemungkinan menghindar)
                musuh_aksi = random.choice(['serang', 'menghindar'])
                if musuh_aksi == 'menghindar':
                    if musuh['speed'] >= pilihan_senjata['speed']:
                        stdscr.addstr(f"{musuh['name']} berhasil menghindar dari seranganmu!\n")
                    else:
                        stdscr.addstr(f"{musuh['name']} gagal menghindar karena kecepatan kamu lebih tinggi!\n")
                        musuh['health'] -= pilihan_senjata['damage']
                        stdscr.addstr(f"Kamu menyerang {musuh['name']} dan mengurangi {pilihan_senjata['damage']} health musuh!\n")
                else:
                    musuh['health'] -= pilihan_senjata['damage']
                    stdscr.addstr(f"Kamu menyerang {musuh['name']} dan mengurangi {pilihan_senjata['damage']} health musuh!\n")

                stdscr.refresh()
                time.sleep(2)

                if musuh['health'] <= 0:
                    stdscr.addstr(f"\nKamu telah mengalahkan {musuh['name']}!\n")
                    stdscr.refresh()
                    stage2 = False
                    player_exp += musuh['drop_xp']
                    # Jika level up terjadi setelah pertempuran
                else:
                    # Musuh menyerang balik jika tidak kalah
                    stdscr.addstr(f"{musuh['name']} menyerang balik!\n")
                    stdscr.refresh()
                    time.sleep(2)
                    pilihan_senjata['health'] -= musuh['damage']
                    stdscr.addstr(f"{musuh['name']} memberikan {musuh['damage']} damage!\n")

                if pilihan_senjata['health'] <= 0:
                    stdscr.addstr("\nKamu telah dikalahkan!\n")
                    stdscr.refresh()
                    time.sleep(3)
                    break

            elif action.lower() == 'd':
                stdscr.addstr("\nKamu memilih untuk menghindar!\n")
                stdscr.refresh()
                time.sleep(2)

                if musuh['speed'] >= pilihan_senjata['speed']:
                    stdscr.addstr(f"{musuh['name']} menyerangmu sebelum kamu bisa menghindar!\n")
                    pilihan_senjata['health'] -= musuh['damage']
                else:
                    stdscr.addstr(f"Kamu berhasil menghindari serangan {musuh['name']}!\n")

                stdscr.refresh()
                time.sleep(2)

                if pilihan_senjata['health'] <= 0:
                    stdscr.addstr("\nKamu telah dikalahkan!\n")
                    stdscr.refresh()
                    time.sleep(3)
                    break

            elif action.lower() == 'l':
                stdscr.addstr("\nKamu memilih untuk melarikan diri!\n")
                stdscr.refresh()
                time.sleep(2)
                stdscr.addstr(f"Kamu berhasil lari dari {musuh['name']}!\n")
                stdscr.refresh()
                break

            else:
                stdscr.addstr("\nAksi tidak valid, coba lagi!\n")
                stdscr.refresh()

            # Pemain kalah
            if pilihan_senjata['health'] <= 0:
                stdscr.addstr("\nKamu telah dikalahkan!\n")
                stdscr.refresh()
                time.sleep(3)
                break
        
        stdscr.clear()
        stdscr.addstr(f"{musuh['name']} berhasil dikalahkan\n")
        
        # Berikan XP kepada pemain dan cek apakah naik level ke level 3
        player_exp += musuh['drop_xp']
        if player_exp >= exp_to_level_3:
            stdscr.addstr("\nKamu naik level ke Level 3!\n")
            stdscr.refresh()
            level_up(stdscr, pilihan_senjata)
            player_level = 3
        
        stdscr.addstr("\nTekan tombol apapun untuk melanjutkan.\n")
        stdscr.refresh()
        stdscr.getch()  # Menunggu pemain menekan tombol sebelum keluar

wrapper(main)
