#!/usr/bin/env bash
set -euo pipefail
cd /work
src=vendor/gsm/src
sources=(add code debug decode long_term lpc preprocess rpe gsm_destroy gsm_decode gsm_encode gsm_create gsm_explode gsm_implode gsm_option gsm_print short_term table)
args=()
for s in "${sources[@]}"; do args+=("$src/$s.c"); done
emcc "${args[@]}" -Ivendor/gsm/inc -O3 -DSASR -DNeedFunctionPrototypes=1 \
  -s MODULARIZE=1 -s EXPORT_NAME=createGSM -s SINGLE_FILE=1 \
  -s ENVIRONMENT=worker,node -s ALLOW_MEMORY_GROWTH=1 -s FILESYSTEM=0 \
  -s EXPORTED_FUNCTIONS='["_gsm_create","_gsm_destroy","_gsm_encode","_gsm_decode","_malloc","_free"]' \
  -o build/gsm-encoder.js
