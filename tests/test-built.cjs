const fs=require('node:fs'),assert=require('node:assert/strict');
const {api}=require('./test-web.cjs');
const html=fs.readFileSync('dist/index.html','utf8');
const p=JSON.parse(html.match(/<script id="rom-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const base=new Uint8Array(Buffer.from(p.rom,'base64'));
const bytes=new Uint8Array(fs.readFileSync('build/smoke.gsm'));
const rgba=new Uint8ClampedArray(65536);for(let i=0;i<rgba.length;i+=4){rgba[i]=80;rgba[i+1]=150;rgba[i+2]=30;rgba[i+3]=255;}
const gbfs=api.makeGBFS([{title:'440 Hz test',data:bytes}]);
const rom=api.patchROM(base,p.meta,'Browser smoke test','GBA Album Studio',api.quantizeRGBA(rgba),gbfs);
assert.equal(rom[0xb2],0x96);fs.writeFileSync('build/smoke-test.gba',rom);
console.log('PASS: built player patched with real GSM audio. Emulator playback remains a manual check.');
