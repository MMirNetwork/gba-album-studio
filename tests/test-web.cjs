const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=process.argv[2]||'web/index.html';
const html=fs.readFileSync(path,'utf8');
const code=html.match(/<script>\s*('use strict';[\s\S]*?)<\/script>/)[1];
new vm.Script(code);
const pure=code.split('// END PURE FUNCTIONS')[0];
const env={Uint8Array,Uint8ClampedArray,DataView,TextEncoder,console};
vm.createContext(env);vm.runInContext(pure+'\nglobalThis.api={ascii,trackName,makeGBFS,patchROM,quantizeRGBA};',env);
const {ascii,trackName,makeGBFS,patchROM,quantizeRGBA}=env.api;
assert.equal(ascii('M\u00f6tley Cr\u00fce \u2014 Stra\u00dfe',60),'Moetley Cruee - Strasse');
assert.equal(trackName('One.two'),'One-two');assert.equal(trackName('  '),'Untitled');
const frame=new Uint8Array(33);frame[0]=0xd0;
const gbfs=makeGBFS([{title:'Zebra',data:frame},{title:'Alpha',data:frame}]);
const v=new DataView(gbfs.buffer);assert.equal(Buffer.from(gbfs.subarray(0,16)).toString(),'PinEightGBFS\r\n\x1a\n');
assert.equal(v.getUint16(22,true),2);assert.equal(v.getUint32(16,true),gbfs.length);
assert.equal(Buffer.from(gbfs.subarray(32,41)).toString(),'Zebra.gsm');
assert.equal(Buffer.from(gbfs.subarray(104,113)).toString(),'Alpha.gsm');
assert.equal(v.getUint32(100,true)%16,0);assert.equal(v.getUint32(172,true)%16,0);
assert.equal(gbfs[v.getUint32(100,true)],0xd0);
assert.throws(()=>makeGBFS([]));assert.throws(()=>makeGBFS([{title:'Bad',data:new Uint8Array(33)}]));
assert.throws(()=>makeGBFS([{title:'Bad',data:new Uint8Array(34)}]));
assert.throws(()=>makeGBFS(Array(100).fill({title:'A',data:frame})));
const rgba=new Uint8ClampedArray(128*128*4);for(let i=0;i<rgba.length;i+=4){rgba[i]=255;rgba[i+3]=255;}
const art=quantizeRGBA(rgba,16);assert.equal(art.palette.length,512);assert.equal(art.bitmap.length,16384);assert.equal(art.bitmap[0],16);assert.equal(new DataView(art.palette.buffer).getUint16(32,true),31);
rgba.fill(0);for(let y=0;y<128;y++)for(let x=0;x<128;x++){const i=(y*128+x)*4;rgba[i]=x<8?255:0;rgba[i+1]=y<8?255:0;rgba[i+3]=255;}
const tiled=quantizeRGBA(rgba,16);assert.equal(tiled.bitmap[0],tiled.bitmap[63]);assert.notEqual(tiled.bitmap[0],tiled.bitmap[64]);assert.notEqual(tiled.bitmap[0],tiled.bitmap[1024]);assert.ok([...tiled.bitmap].every(x=>x>=16&&x<32));
const base=new Uint8Array(20001);base[0xb2]=0x96;
const meta={album:{offset:256,size:28},artist:{offset:284,size:28},palette:{offset:312,size:512},bitmap:{offset:824,size:16384}};
const rom=patchROM(base,meta,'Album','Artist',art,gbfs);assert.equal(rom.length,20224+gbfs.length);assert.equal(Buffer.from(rom.subarray(256,261)).toString(),'Album');assert.equal((rom.subarray(0xa0,0xbe).reduce((a,b)=>a+b,0)+0x19)&255,0);assert.equal(rom[20224],80);assert.equal(base[256],0);
assert.throws(()=>patchROM(base,{...meta,album:{offset:0,size:28}},'A','B',art,gbfs));
assert.throws(()=>patchROM(base,{...meta,artist:{offset:256,size:28}},'A','B',art,gbfs));
assert.throws(()=>patchROM(base,meta,'A','B',art,new Uint8Array(32*1024*1024)));
console.log('PASS: JS syntax, ASCII names, GBFS64 order/alignment, GSM validation, cover quantization/tiling, ROM patching, checksum, size/overlap guards.');
module.exports={api:env.api};

// English UI and attribution order are part of the source contract.
assert.ok(html.includes('<html lang="en">'));
const about=html.slice(html.indexOf('id="projectInfo"'));
assert.ok(about.includes('An open-source project') || about.includes('an open-source project'));
assert.ok(about.indexOf('MMirNetwork') < about.indexOf('Damian Yerrick'));
assert.ok(about.indexOf('MMirNetwork') < about.indexOf('Ben Wiley'));
assert.ok(html.includes('Third-party licenses') || html.includes('<!-- THIRD_PARTY_NOTICES -->'));
console.log('PASS: English document language and MMirNetwork-first project attribution.');
