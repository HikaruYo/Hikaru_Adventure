import curses, time, random
from curses import wrapper

senjata = {
    'Pedang panjang': {
        'damage': 7, 
        'speed': 4, 
        'health': 16, 
        'max_health': 16
    },
    'Pedang dua tangan': {
        'damage': 10, 
        'speed': 2, 
        'health': 18, 
        'max_health': 18
    },
    'Busur pendek': {
        'damage': 7, 
        'speed': 5, 
        'health': 15, 
        'max_health': 15
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
        'message': 'Kamu bertemu dengan Goblin Hutan di tengah hutan gelap!',
    },
    'Orc': {
        'name': 'Orc', 
        'damage': 5, 
        'speed': 1, 
        'health': 25, 
        'drop_xp': 20, 
        'dodge_chance': 0.1,
        'message': 'Seekor Orc besar menghadangmu di tepi sungai yang berbahaya!',
    },
    'Giant Snake': {
        'name': 'Giant Snake', 
        'damage': 4, 
        'speed': 3, 
        'health': 23, 
        'drop_xp': 25, 
        'dodge_chance': 0.2,
        'message': 'Ular Raksasa muncul dari semak-semak yang lebat!',
    }
}

def tampilkan_status(stdscr, player_stats, musuh, player_level, player_exp):
    stdscr.addstr(f"=== Status ===\n")
    stdscr.addstr(f"Level Pemain : {player_level}\n")
    stdscr.addstr(f"Health : {player_stats['health']}/{player_stats['max_health']}\n")
    stdscr.addstr(f"Damage : {player_stats['damage']}\n")
    stdscr.addstr(f"Speed  : {player_stats['speed']}\n")
    stdscr.addstr(f"XP     : {player_exp}\n\n")
    
    stdscr.addstr(f"Status {musuh['name']}:\n")
    stdscr.addstr(f"Health : {musuh['health']}\n")
    stdscr.addstr(f"Damage : {musuh['damage']}\n")
    stdscr.addstr(f"Speed  : {musuh['speed']}\n")

def aksi_pertarungan(stdscr, player_stats, musuh, player_exp):
    stdscr.addstr("\n=== Aksi ===\n")
    stdscr.addstr("Tekan 'a' untuk menyerang, 'd' untuk menghindar, atau 'l' untuk lari!\n")
    stdscr.refresh()
    action = stdscr.getkey()

    if action == 'a':
        if player_stats['speed'] >= musuh['speed']:
            if random.random() > musuh['dodge_chance']:
                musuh['health'] -= player_stats['damage']
                stdscr.addstr("Kamu menyerang terlebih dahulu!\n")
                if musuh['health'] <= 0:
                    stdscr.addstr(f"{musuh['name']} telah mati!\n")
                    return "menang", musuh['drop_xp']
                player_stats['health'] -= musuh['damage']
                stdscr.addstr(f"Musuh membalas dengan serangan dan menyebabkan {musuh['damage']} damage!\n")
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
            return "lari", 0
        else:
            player_stats['health'] -= musuh['damage']
            stdscr.addstr("Kamu gagal melarikan diri dan terkena serangan musuh!\n")
    else:
        stdscr.addstr("Aksi tidak valid!\n")
    
    if player_stats['health'] <= 0:
        stdscr.addstr("Kamu tewas dalam pertempuran...\n")
        return "kalah", 0
    
    return "lanjut", 0

def level_up(stdscr, player_stats):
    player_stats['health'] = player_stats['max_health']
    pilihan = ['Health', 'Damage', 'Speed']
    while True:
        stdscr.clear()
        stdscr.addstr("Kamu naik level! Pilih salah satu stat untuk ditingkatkan:\n1. Health\n2. Damage\n3. Speed\n")
        stdscr.refresh()
        choice = stdscr.getkey()
        if choice in ['1', '2', '3']:
            stat = pilihan[int(choice) - 1].lower()
            if stat == 'health':
                player_stats['max_health'] += 5
                player_stats['health'] = player_stats['max_health']
            else:
                player_stats[stat] += 2 if stat == 'damage' else 1
            stdscr.addstr(f"{pilihan[int(choice) - 1]} kamu meningkat!\n")
            stdscr.refresh()
            time.sleep(2)
            break
        else:
            stdscr.addstr("Pilihan tidak valid! Coba lagi.\n")

def xp_required_for_level(level):
    if level == 1:
        return 8
    elif level == 2:
        return 12
    elif level == 3:
        return 14
    elif level == 4:
        return 16
    elif level == 5:
        return 18
    elif level == 6:
        return 20
    elif level == 7:
        return 24
    else:
        return 30

def stage(stdscr, player_stats, player_level, player_exp, musuh_name):
    musuh = musuh_list[musuh_name]
    stdscr.clear()
    stdscr.addstr(f"=== {musuh_name} ===\n{musuh['message']}\n")
    stdscr.refresh()
    time.sleep(4)

    while True:
        stdscr.clear()
        tampilkan_status(stdscr, player_stats, musuh, player_level, player_exp)
        result, gained_xp = aksi_pertarungan(stdscr, player_stats, musuh, player_exp)
        
        if result == "menang":
            stdscr.addstr(f"Kamu telah mengalahkan {musuh['name']}!\n")
            stdscr.addstr(f"Kamu mendapatkan {gained_xp} XP!\n")
            player_exp += gained_xp
            
            # Cek apakah pemain naik level
            while player_exp >= xp_required_for_level(player_level) and player_level < 8:
                player_exp -= xp_required_for_level(player_level)
                player_level += 1
                level_up(stdscr, player_stats)
                
            break
        elif result in ["kalah", "lari"]:
            break

        stdscr.refresh()
        time.sleep(2)
    
    return player_level, player_exp

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr("Ini adalah kisah Hikaru sang petualang!\n")
    stdscr.addstr("Bantu Hikaru untuk mengalahkan Raja Iblis dan selamatkan dunia!\n")
    stdscr.addstr("Pilih senjata yang akan kamu gunakan:\n")
    stdscr.addstr("1. Pedang panjang\n")
    stdscr.addstr("2. Pedang dua tangan\n")
    stdscr.addstr("3. Busur pendek\n")
    stdscr.refresh()

    pilihan = stdscr.getkey()
    if pilihan in ['1', '2', '3']:
        pilihan_senjata = list(senjata.values())[int(pilihan) - 1]
        stdscr.addstr(f"Kamu memilih {list(senjata.keys())[int(pilihan) - 1]}!\n")
        stdscr.addstr("Bersiaplah, petualanganmu dimulai...\n")
    else:
        stdscr.addstr("Pilihan tidak valid! Keluar dari game...\n")
        stdscr.refresh()
        time.sleep(2)
        return

    stdscr.refresh()
    time.sleep(2)

    player_level, player_exp = 1, 0
    for musuh_name in musuh_list.keys():
        player_level, player_exp = stage(stdscr, pilihan_senjata, player_level, player_exp, musuh_name)

wrapper(main)
