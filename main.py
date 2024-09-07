import curses, time, random
from curses import wrapper

senjata = {
    'Pedang panjang': {
        'damage': 7,
        'speed': 4,
        'health': 16,
        'max_health': 16,
    },
    'Pedang dua tangan': {
        'damage': 10,
        'speed': 2,
        'health': 18,
        'max_health': 18,
    },
    'Busur pendek': {
        'damage': 7,
        'speed': 5,
        'health': 15,
        'max_health': 15,
    }
}

musuh_list = {
    'Goblin Hutan': {
        'name': 'Goblin Hutan',
        'damage': 3,
        'speed': 2,
        'health': 20,
        'drop_xp': 10,
        'dodge_chance': 0.3,
    },
    'Orc': {
        'name': 'Orc',
        'damage': 5,
        'speed': 1,
        'health': 25,
        'drop_xp': 20,
        'dodge_chance': 0.1,
    },
    'Giant Snake': {
        'name': 'Giant Snake',
        'damage': 4,
        'speed': 3,
        'health': 23,
        'drop_xp': 25,
        'dodge_chance': 0.2,
    }
}

def level_up(stdscr, player_stats):
    player_stats['health'] = player_stats['max_health']
    choice_made = False
    while not choice_made:
        stdscr.clear()
        stdscr.addstr("Kamu naik level! Pilih salah satu stat untuk ditingkatkan:\n")
        stdscr.addstr("1. Health\n")
        stdscr.addstr("2. Damage\n")
        stdscr.addstr("3. Speed\n")
        stdscr.refresh()
        
        choice = stdscr.getkey()

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

def tampilkan_status(stdscr, player_stats, musuh, player_level, player_exp):
    stdscr.addstr("=== Status ===\n")
    stdscr.addstr(f"Level Pemain : {player_level}\n")
    stdscr.addstr(f"Health : {player_stats['health']}/{player_stats['max_health']}\n")
    stdscr.addstr(f"Damage : {player_stats['damage']}\n")
    stdscr.addstr(f"Speed  : {player_stats['speed']}\n")
    stdscr.addstr(f"XP     : {player_exp}\n\n")
    
    stdscr.addstr(f"Status {musuh['name']}:\n")
    stdscr.addstr(f"Health : {musuh['health']}\n")
    stdscr.addstr(f"Damage : {musuh['damage']}\n")
    stdscr.addstr(f"Speed  : {musuh['speed']}\n")

def stage_1(stdscr, player_stats, player_level, player_exp):
    musuh = musuh_list['Goblin Hutan']
    drop_xp = musuh['drop_xp']

    stdscr.clear()
    stdscr.addstr("=== Stage 1 ===\n")
    stdscr.addstr("\nKamu memasuki hutan gelap dan mendengar suara langkah kaki...\n")
    stdscr.addstr(f"Kamu bertemu dengan {musuh['name']}!\n")
    stdscr.addstr("Bersiaplah untuk pertempuran!\n")
    stdscr.refresh()
    time.sleep(4)

    stage1 = True
    while stage1:
        stdscr.clear()
        tampilkan_status(stdscr, player_stats, musuh, player_level, player_exp)

        stdscr.addstr("\n=== Aksi ===\n")
        stdscr.addstr("Tekan 'a' untuk menyerang, 'd' untuk menghindar, atau 'l' untuk lari!\n")
        stdscr.refresh()

        action = stdscr.getkey()

        if action == 'a':
            if player_stats['speed'] >= musuh['speed']:
                # Cek apakah musuh berhasil menghindar
                if random.random() > musuh['dodge_chance']:
                    musuh['health'] -= player_stats['damage']
                    stdscr.addstr("Kamu menyerang terlebih dahulu!\n")
                    if musuh['health'] > 0:
                        player_stats['health'] -= musuh['damage']
                        stdscr.addstr(f"Musuh membalas dengan serangan dan menyebabkan {musuh['damage']} damage!\n")
                    else:
                        stdscr.addstr(f"Kamu telah mengalahkan {musuh['name']}!\n")
                        player_exp += drop_xp
                        stdscr.addstr(f"Kamu mendapatkan {drop_xp} XP!\n")
                        if player_exp >= 8:
                            level_up(stdscr, player_stats)
                        stage1 = False
                else:
                    stdscr.addstr(f"{musuh['name']} berhasil menghindari seranganmu!\n")
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr("Musuh menyerang lebih cepat dan melukai kamu!\n")

        elif action == 'd':
            if random.random() > 0.5:
                stdscr.addstr("Kamu berhasil menghindari serangan!\n")
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr(f"Kamu gagal menghindar dan terkena {musuh['damage']} damage!\n")
        elif action == 'l':
            if random.random() > 0.5:
                stdscr.addstr("Kamu berhasil melarikan diri!\n")
                stage1 = False
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr("Kamu gagal melarikan diri dan terkena serangan musuh!\n")
        else:
            stdscr.addstr("Aksi tidak valid!\n")
        
        if player_stats['health'] <= 0:
            stdscr.addstr("Kamu tewas dalam pertempuran...\n")
            stage1 = False

        stdscr.refresh()
        time.sleep(2)

def stage_2(stdscr, player_stats, player_level, player_exp):
    musuh = musuh_list['Orc']
    drop_xp = musuh['drop_xp']

    stdscr.clear()
    stdscr.addstr("=== Stage 2 ===\n")
    stdscr.addstr("\nSetelah berhasil keluar dari hutan, kamu bertemu dengan Orc besar!\n")
    stdscr.addstr("Bersiaplah untuk pertempuran sengit!\n")
    stdscr.refresh()
    time.sleep(4)

    stage2 = True
    while stage2:
        stdscr.clear()
        tampilkan_status(stdscr, player_stats, musuh, player_level, player_exp)

        stdscr.addstr("\n=== Aksi ===\n")
        stdscr.addstr("Tekan 'a' untuk menyerang, 'd' untuk menghindar, atau 'l' untuk lari!\n")
        stdscr.refresh()

        action = stdscr.getkey()

        if action == 'a':
            if player_stats['speed'] >= musuh['speed']:
                # Cek apakah musuh berhasil menghindar
                if random.random() > musuh['dodge_chance']:
                    musuh['health'] -= player_stats['damage']
                    stdscr.addstr("Kamu menyerang terlebih dahulu!\n")
                    if musuh['health'] > 0:
                        player_stats['health'] -= musuh['damage']
                        stdscr.addstr(f"Musuh membalas dengan serangan dan menyebabkan {musuh['damage']} damage!\n")
                    else:
                        stdscr.addstr(f"Kamu telah mengalahkan {musuh['name']}!\n")
                        player_exp += drop_xp
                        stdscr.addstr(f"Kamu mendapatkan {drop_xp} XP!\n")
                        if player_exp >= 16:
                            level_up(stdscr, player_stats)
                        stage2 = False
                else:
                    stdscr.addstr(f"{musuh['name']} berhasil menghindari seranganmu!\n")
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr("Musuh menyerang lebih cepat dan melukai kamu!\n")

        elif action == 'd':
            if random.random() > 0.5:
                stdscr.addstr("Kamu berhasil menghindari serangan!\n")
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr(f"Kamu gagal menghindar dan terkena {musuh['damage']} damage!\n")
        elif action == 'l':
            if random.random() > 0.5:
                stdscr.addstr("Kamu berhasil melarikan diri!\n")
                stage2 = False
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr("Kamu gagal melarikan diri dan terkena serangan musuh!\n")
        else:
            stdscr.addstr("Aksi tidak valid!\n")
        
        if player_stats['health'] <= 0:
            stdscr.addstr("Kamu tewas dalam pertempuran...\n")
            stage2 = False

        stdscr.refresh()
        time.sleep(2)

def stage_3(stdscr, player_stats, player_level, player_exp):
    musuh = musuh_list['Giant Snake']
    drop_xp = musuh['drop_xp']

    stdscr.clear()
    stdscr.addstr("=== Stage 3 ===\n")
    stdscr.addstr("\nSaat berjalan melalui lembah, seekor Giant Snake muncul dari balik bebatuan!\n")
    stdscr.addstr("Pertarungan besar dimulai!\n")
    stdscr.refresh()
    time.sleep(4)

    stage3 = True
    while stage3:
        stdscr.clear()
        tampilkan_status(stdscr, player_stats, musuh, player_level, player_exp)

        stdscr.addstr("\n=== Aksi ===\n")
        stdscr.addstr("Tekan 'a' untuk menyerang, 'd' untuk menghindar, atau 'l' untuk lari!\n")
        stdscr.refresh()

        action = stdscr.getkey()

        if action == 'a':
            if player_stats['speed'] >= musuh['speed']:
                if random.random() > musuh['dodge_chance']:
                    musuh['health'] -= player_stats['damage']
                    stdscr.addstr("Kamu menyerang terlebih dahulu!\n")
                    if musuh['health'] > 0:
                        player_stats['health'] -= musuh['damage']
                        stdscr.addstr(f"Musuh membalas dengan serangan dan menyebabkan {musuh['damage']} damage!\n")
                    else:
                        stdscr.addstr(f"Kamu telah mengalahkan {musuh['name']}!\n")
                        player_exp += drop_xp
                        stdscr.addstr(f"Kamu mendapatkan {drop_xp} XP!\n")
                        stage3 = False
                else:
                    stdscr.addstr(f"{musuh['name']} berhasil menghindari seranganmu!\n")
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr("Musuh menyerang lebih cepat dan melukai kamu!\n")

        elif action == 'd':
            if random.random() > 0.5:
                stdscr.addstr("Kamu berhasil menghindari serangan!\n")
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr(f"Kamu gagal menghindar dan terkena {musuh['damage']} damage!\n")
        elif action == 'l':
            if random.random() > 0.5:
                stdscr.addstr("Kamu berhasil melarikan diri!\n")
                stage3 = False
            else:
                player_stats['health'] -= musuh['damage']
                stdscr.addstr("Kamu gagal melarikan diri dan terkena serangan musuh!\n")
        else:
            stdscr.addstr("Aksi tidak valid!\n")
        
        if player_stats['health'] <= 0:
            stdscr.addstr("Kamu tewas dalam pertempuran...\n")
            stage3 = False

        stdscr.refresh()
        time.sleep(2)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    stdscr.addstr("Selamat datang di Game Petualangan!\n")
    stdscr.addstr("Pilih senjata yang akan kamu gunakan:\n")
    stdscr.addstr("1. Pedang panjang\n")
    stdscr.addstr("2. Pedang dua tangan\n")
    stdscr.addstr("3. Busur pendek\n")
    stdscr.refresh()

    pilihan = stdscr.getkey()
    pilihan_senjata = None
    if pilihan == '1':
        pilihan_senjata = senjata['Pedang panjang']
    elif pilihan == '2':
        pilihan_senjata = senjata['Pedang dua tangan']
    elif pilihan == '3':
        pilihan_senjata = senjata['Busur pendek']
    else:
        stdscr.addstr("Pilihan tidak valid! Keluar dari game...\n")
        stdscr.refresh()
        time.sleep(2)
        return

    player_level = 1
    player_exp = 0
    exp_to_level_2 = 8
    exp_to_level_3 = 16

    stage_1(stdscr, pilihan_senjata, player_level, player_exp)
    stage_2(stdscr, pilihan_senjata, player_level, player_exp)
    stage_3(stdscr, pilihan_senjata, player_level, player_exp)

wrapper(main)
