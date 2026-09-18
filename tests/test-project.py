"""Offline regression checks using explicit synthetic source/build fixtures."""
from pathlib import Path
import tempfile, subprocess, shutil, re, json, hashlib
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    p=Path(td); (p/'src').mkdir()
    (p/'Makefile').write_text('CFLAGS := -g -Wall -O2\nTARGET-bare_mb.gba\n')
    (p/'src/asm.S').write_text('.ARM\n')
    (p/'src/libgsm.c').write_text("while (song_name_len < max_len && playback->curr_song_name[song_name_len] != '.') {}\nif (cmd & CMD_START_SONG) {\nsrc + src_len - 33 * 60;\n}\n")
    (p/'src/hud.c').write_text("curr_char = offset < 0 ? ' ' : playback->curr_song_name[offset];\nvoid showGSMPlayerCopyrightInfo() { hud_wline(1, artistName); }\nvoid hud_show_instructions() { hud_wline(1, \" Play: A/B\"); }\n")
    subprocess.run(['python3',str(root/'scripts/prepare-player.py'),str(p)],check=True)
    hud=(p/'src/hud.c').read_text()
    info=hud[hud.index('void showGSMPlayerCopyrightInfo'):hud.index('void hud_show_instructions')]
    rows=re.findall(r'hud_wline\((\d+),\s*"([^"]*)"\)',info)
    assert rows[0]==('0','Open-source project')
    assert rows[1]==('1','by MMirNetwork')
    assert len(rows)==8  # plus artist and album variables
    assert all(len(text)<=28 and int(row)<10 for row,text in rows)
    assert info.index('MMirNetwork')<info.index('Damian Yerrick')<info.index('Ben Wiley')
    assert 'J. Degener & C. Bormann' in info and 'and Toast contributors' in info
    assert '(See TOAST-COPYRIGHT.txt)' in info
    controls = hud[hud.index('void hud_show_instructions'):]
    assert 'hud_wline(0, "");' in controls
    assert 'hud_wline(8, "");' in controls
    assert not re.search(r'hud_wline\(9,\s*""\)', controls)
    # Replay the literal row writes to model repeated info -> playback changes.
    # Rows 1-7 are refreshed by upstream; row 9 by drawHUDFrame before controls.
    def apply_literals(body, screen):
        for row, text in re.findall(r'hud_wline\((\d+),\s*"([^"\n]*)"\)', body):
            screen[int(row)] = text
    screen = [''] * 10
    for _ in range(5):
        apply_literals(info, screen)
        assert screen[8] == 'and Toast contributors'
        screen[9] = '01 Track title 00:12'
        for row in range(1, 8):
            screen[row] = 'Controls' if row <= 5 else ''
        apply_literals(controls, screen)
        assert screen[0] == screen[8] == ''
        assert screen[9] == '01 Track title 00:12'

    assert '\x00' not in (p/'src/libgsm.c').read_text()
    print('PASS: info rows fit GBA, MMirNetwork first, upstream credits retained, return-to-player rows 0/8 cleared, status preserved over five transitions.')
with tempfile.TemporaryDirectory() as td:
    p=Path(td)
    for folder in ['scripts','web']:
        shutil.copytree(root/folder,p/folder)
    (p/'build').mkdir();rom=bytearray(20001);rom[0xb2]=0x96
    for offset,text in [(256,b'GBA_WEB_ALBUM_V1'),(284,b'GBA_WEB_ARTIST_V1')]:
        rom[offset:offset+len(text)]=text
    rom[0xbd]=(-sum(rom[0xa0:0xbd])-0x19)&255
    (p/'build/player.gba').write_bytes(rom)
    (p/'build/player-symbols.txt').write_text('08000100 0000001c R albumName\n0800011c 0000001c R artistName\n08000138 00000200 R leopard_Palette\n08000338 00004000 R leopard_Bitmap\n')
    (p/'build/gsm-encoder.js').write_text('/* synthetic fixture, not a functioning encoder */')
    (p/'vendor/player/src').mkdir(parents=True);(p/'vendor/gsm').mkdir(parents=True)
    (p/'vendor/player/TOAST-COPYRIGHT.txt').write_text('Test <notice>')
    (p/'vendor/gsm/COPYRIGHT').write_text('Codec fixture notice')
    for name in ['gbfs.h','libgbfs.c']:
        (p/'vendor/player/src'/name).write_text('/* fixture license */')
    subprocess.run(['python3',str(p/'scripts/package-site.py')],check=True)
    page=(p/'dist/index.html').read_text()
    assert '<!-- THIRD_PARTY_NOTICES -->' not in page
    assert page.index('About this project')<page.index('Third-party licenses &amp; notices')
    assert 'Test &lt;notice&gt;' in page and 'Codec fixture notice' in page
    assert 'Quellen und Lizenzhinweise' not in page
    manifest=json.loads((p/'build/manifest.json').read_text())
    assert manifest['sha256']==hashlib.sha256(rom).hexdigest()
    subprocess.run(['node',str(root/'tests/test-web.cjs'),str(p/'dist/index.html')],check=True)
    print('PASS: synthetic packaging, English notices, notice order, escaped copyright text and ROM hash.')
print('No full GBA/WASM build or emulator test was performed by these fixture tests.')
