#!/usr/bin/env python3
"""Adapt only the pinned upstream checkout."""
from pathlib import Path
import re, sys
root = Path(sys.argv[1]); src = root / 'src'
p = root / 'Makefile'
s = p.read_text().replace('-bare_mb', '-bare')
s = s.replace('CFLAGS := -g -Wall -O2', 'CFLAGS := -g -Wall -O2 -std=gnu11 -fno-strict-aliasing')
assert '-bare_mb' not in s
p.write_text(s)
(src / 'asm.S').rename(src / 'asm.s')
(src / 'album_info.h').write_text('extern const char artistName[28];\nextern const char albumName[28];\n')
(src / 'leopard.pal.c').write_text('const char artistName[28] __attribute__((used, aligned(4))) = "GBA_WEB_ARTIST_V1";\nconst char albumName[28] __attribute__((used, aligned(4))) = "GBA_WEB_ALBUM_V1";\nconst unsigned short leopard_Palette[256] __attribute__((used, aligned(4))) = {0x7fff, 0};\n')
(src / 'leopard.raw.c').write_text('const unsigned char leopard_Bitmap[16384] __attribute__((used, aligned(4))) = {16};\n')
p = src / 'libgsm.c'; s = p.read_text()
s, n = re.subn(r"song_name_len < max_len && playback->curr_song_name\[song_name_len\] != '\.'", lambda m: "song_name_len < max_len - 1 && playback->curr_song_name[song_name_len] != '\\0' && playback->curr_song_name[song_name_len] != '.'", s)
assert n == 1, 'Upstream title parser changed'
s, n = re.subn(r'(if\s*\(cmd & CMD_START_SONG\)\s*\{)', r'\1\n    playback->decode_pos = 160;\n    playback->last_sample = 0;', s)
assert n == 1
s, n = re.subn(r'src \+ src_len - 33 \* 60', 'src + (src_len > 33 * 60 ? src_len - 33 * 60 : 0)', s)
assert n == 1
p.write_text(s)
p = src / 'hud.c'; s = p.read_text()
s, n = re.subn(r"curr_char = offset < 0 \? ' ' : playback->curr_song_name\[offset\];", "curr_char = (offset < 0 || (unsigned int)offset >= playback->curr_song_name_len) ? ' ' : playback->curr_song_name[offset];", s)
assert n == 1, 'Upstream marquee changed'
# Ten 16-pixel text rows fit the GBA's 160-pixel display. Keep upstream
# copyrights visible below the project identity instead of removing them.
info_screen = """void showGSMPlayerCopyrightInfo() {
  hud_wline(0, "Open-source project");
  hud_wline(1, "by MMirNetwork");
  hud_wline(2, artistName);
  hud_wline(3, albumName);
  hud_wline(4, "Based on GSM Player for GBA");
  hud_wline(5, "(C) 2004,2019 Damian Yerrick");
  hud_wline(6, "Album-art fork: Ben Wiley");
  hud_wline(7, "J. Degener & C. Bormann");
  hud_wline(8, "and Toast contributors");
  hud_wline(9, "(See TOAST-COPYRIGHT.txt)");
}"""
s, n = re.subn(r'void\s+showGSMPlayerCopyrightInfo\s*\(\s*(?:void\s*)?\)\s*\{[^}]*\}', lambda m: info_screen, s)
assert n == 1, 'Upstream info screen changed'
# The info page uses row zero, which upstream playback normally leaves blank.
# Clear it when returning to the player so the branding does not remain there.
s, n = re.subn(r'(void\s+hud_show_instructions\s*\(\s*(?:void\s*)?\)\s*\{)', lambda m: m.group(1) + '\n  hud_wline(0, "");', s)
assert n == 1, 'Upstream controls screen changed'
p.write_text(s)
print('Player adapted: cartridge linking, fixed-size ROM fields, bounded title rendering.')
