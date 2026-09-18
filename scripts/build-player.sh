#!/usr/bin/env bash
set -euo pipefail
cd /work
export DEVKITPRO=/opt/devkitpro
export DEVKITARM="$DEVKITPRO/devkitARM"
export PATH="$DEVKITPRO/tools/bin:$DEVKITARM/bin:$PATH"
cd vendor/player
make -j1 build/allnewgsm-bare.gba
arm-none-eabi-nm -S --defined-only build/allnewgsm-bare.elf > /work/build/player-symbols.txt
cp build/allnewgsm-bare.gba /work/build/player.gba
