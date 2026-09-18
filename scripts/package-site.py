#!/usr/bin/env python3
from pathlib import Path
import base64, hashlib, json, re, html
root = Path(__file__).resolve().parents[1]
rom = (root / 'build/player.gba').read_bytes()
assert 192 <= len(rom) < 256 * 1024, 'Unexpected player size'
assert rom[0xb2] == 0x96, 'Not a GBA header'
assert (sum(rom[0xa0:0xbd]) + rom[0xbd] + 0x19) & 255 == 0, 'Invalid GBA checksum'
symbols = {}
for line in (root / 'build/player-symbols.txt').read_text().splitlines():
    cols = line.split()
    if len(cols) == 4:
        addr, size, kind, name = cols
        symbols[name] = (int(addr, 16), int(size, 16))
meta = {}
for key, symbol, size in [('album', 'albumName', 28), ('artist', 'artistName', 28), ('palette', 'leopard_Palette', 512), ('bitmap', 'leopard_Bitmap', 16384)]:
    address, actual = symbols[symbol]; offset = address - 0x08000000
    assert actual == size, (symbol, actual)
    assert 192 <= offset and offset + size <= len(rom), (symbol, hex(address))
    meta[key] = dict(offset=offset, size=size)
ranges = sorted((v['offset'], v['offset'] + v['size']) for v in meta.values())
assert all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:]))
for key, marker in [('album', b'GBA_WEB_ALBUM_V1'), ('artist', b'GBA_WEB_ARTIST_V1')]:
    assert rom[meta[key]['offset']:].startswith(marker)
payload = dict(version=1, rom=base64.b64encode(rom).decode(), meta=meta, sha256=hashlib.sha256(rom).hexdigest())
page = (root / 'web/index.html').read_text()
old = '<script id="rom-data" type="application/json">null</script>'
assert page.count(old) == 1
page = page.replace(old, '<script id="rom-data" type="application/json">' + json.dumps(payload, separators=(',', ':')) + '</script>')
encoder = (root / 'build/gsm-encoder.js').read_text()
assert not re.search(r'</script', encoder, re.I), 'Unsafe terminator in generated encoder'
old = '<script id="gsm-engine" type="text/plain"></script>'
assert page.count(old) == 1
page = page.replace(old, '<script id="gsm-engine" type="text/plain">' + encoder + '</script>')
out = root / 'dist'; out.mkdir(exist_ok=True)
(out / 'index.html').write_text(page); (out / '.nojekyll').touch()
notices = ['GBA Album Studio - an open-source project by MMirNetwork\nThis identifies the project edition, not ownership of the upstream components.\n\nThird-party copyright and license notices\n', 'Player upstream: https://github.com/benwiley4000/gsmplayer-gba\nPinned commit: b159d5d415fd49efca50ff6d539d9b55487f0cce\n', (root / 'vendor/player/TOAST-COPYRIGHT.txt').read_text(), '\nlibgsm 1.0.24\n', (root / 'vendor/gsm/COPYRIGHT').read_text()]
for name in ['gbfs.h', 'libgbfs.c']:
    text = (root / 'vendor/player/src' / name).read_text()
    notices.append('\n' + name + '\n' + text[:text.index('*/')+2])
(out / 'THIRD-PARTY-NOTICES.txt').write_text('\n'.join(notices))
credits = '<details class="details"><summary>Third-party licenses &amp; notices</summary><pre style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px">' + html.escape('\n'.join(notices)) + '</pre></details>'
assert page.count('<!-- THIRD_PARTY_NOTICES -->') == 1
page = page.replace('<!-- THIRD_PARTY_NOTICES -->', credits)
(out / 'index.html').write_text(page)
(root / 'build/manifest.json').write_text(json.dumps(payload, indent=2))
print(f'Site embedded: {len(rom):,} bytes player, {len(encoder):,} chars encoder.')
