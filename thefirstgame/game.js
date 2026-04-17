const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

const TILE = 32;
const COLS = 20;
const ROWS = 15;
const MAX_WAVES = 20;
const MAX_LEVELS = 10;

// =========================
// 10张不同地图
// =========================
const LEVEL_PATHS = [
  // 1: S型
  [{x:0,y:2},{x:1,y:2},{x:2,y:2},{x:3,y:2},{x:4,y:2},{x:4,y:3},{x:4,y:4},{x:4,y:5},{x:5,y:5},{x:6,y:5},{x:7,y:5},{x:8,y:5},{x:8,y:6},{x:8,y:7},{x:8,y:8},{x:8,y:9},{x:9,y:9},{x:10,y:9},{x:11,y:9},{x:12,y:9},{x:12,y:10},{x:12,y:11},{x:12,y:12},{x:13,y:12},{x:14,y:12},{x:15,y:12},{x:16,y:12},{x:17,y:12},{x:18,y:12},{x:19,y:12}],
  // 2: 上横向曲折
  [{x:0,y:3},{x:1,y:3},{x:2,y:3},{x:3,y:3},{x:4,y:3},{x:5,y:3},{x:6,y:3},{x:6,y:4},{x:6,y:5},{x:6,y:6},{x:6,y:7},{x:6,y:8},{x:7,y:8},{x:8,y:8},{x:9,y:8},{x:10,y:8},{x:11,y:8},{x:12,y:8},{x:13,y:8},{x:13,y:7},{x:13,y:6},{x:13,y:5},{x:13,y:4},{x:13,y:3},{x:14,y:3},{x:15,y:3},{x:16,y:3},{x:17,y:3},{x:18,y:3},{x:19,y:3}],
  // 3: 纵向蛇形
  [{x:10,y:0},{x:10,y:1},{x:10,y:2},{x:10,y:3},{x:10,y:4},{x:9,y:4},{x:8,y:4},{x:7,y:4},{x:6,y:4},{x:5,y:4},{x:5,y:5},{x:5,y:6},{x:5,y:7},{x:5,y:8},{x:5,y:9},{x:5,y:10},{x:6,y:10},{x:7,y:10},{x:8,y:10},{x:9,y:10},{x:10,y:10},{x:11,y:10},{x:12,y:10},{x:13,y:10},{x:14,y:10},{x:15,y:10},{x:15,y:11},{x:15,y:12},{x:15,y:13},{x:15,y:14}],
  // 4: 螺旋
  [{x:0,y:0},{x:1,y:0},{x:2,y:0},{x:3,y:0},{x:4,y:0},{x:5,y:0},{x:6,y:0},{x:7,y:0},{x:8,y:0},{x:9,y:0},{x:10,y:0},{x:11,y:0},{x:12,y:0},{x:13,y:0},{x:14,y:0},{x:15,y:0},{x:16,y:0},{x:17,y:0},{x:18,y:0},{x:18,y:1},{x:18,y:2},{x:18,y:3},{x:18,y:4},{x:18,y:5},{x:18,y:6},{x:18,y:7},{x:18,y:8},{x:18,y:9},{x:18,y:10},{x:18,y:11},{x:18,y:12},{x:18,y:13},{x:17,y:13},{x:16,y:13},{x:15,y:13},{x:14,y:13},{x:13,y:13},{x:12,y:13},{x:11,y:13},{x:10,y:13},{x:9,y:13},{x:8,y:13},{x:7,y:13},{x:6,y:13},{x:5,y:13},{x:4,y:13},{x:3,y:13},{x:2,y:13},{x:1,y:13},{x:1,y:12},{x:1,y:11},{x:1,y:10},{x:1,y:9},{x:1,y:8},{x:1,y:7},{x:1,y:6},{x:1,y:5},{x:1,y:4},{x:1,y:3},{x:1,y:2},{x:2,y:2},{x:3,y:2},{x:4,y:2},{x:5,y:2},{x:6,y:2},{x:7,y:2},{x:8,y:2},{x:9,y:2},{x:10,y:2},{x:11,y:2},{x:12,y:2},{x:13,y:2},{x:14,y:2},{x:15,y:2},{x:16,y:2},{x:16,y:3},{x:16,y:4},{x:16,y:5},{x:16,y:6},{x:16,y:7},{x:16,y:8},{x:16,y:9},{x:16,y:10},{x:15,y:10},{x:14,y:10},{x:13,y:10},{x:12,y:10},{x:12,y:9},{x:12,y:8},{x:12,y:7},{x:12,y:6},{x:12,y:5},{x:12,y:4},{x:12,y:3},{x:13,y:3},{x:14,y:3},{x:14,y:4},{x:14,y:5},{x:14,y:6},{x:14,y:7},{x:14,y:8},{x:13,y:8}],
  // 5: Z型
  [{x:0,y:7},{x:1,y:7},{x:2,y:7},{x:3,y:7},{x:4,y:7},{x:5,y:7},{x:5,y:6},{x:5,y:5},{x:5,y:4},{x:5,y:3},{x:5,y:2},{x:6,y:2},{x:7,y:2},{x:8,y:2},{x:9,y:2},{x:10,y:2},{x:10,y:3},{x:10,y:4},{x:10,y:5},{x:10,y:6},{x:10,y:7},{x:10,y:8},{x:10,y:9},{x:10,y:10},{x:10,y:11},{x:10,y:12},{x:11,y:12},{x:12,y:12},{x:13,y:12},{x:14,y:12},{x:15,y:12},{x:15,y:11},{x:15,y:10},{x:15,y:9},{x:15,y:8},{x:15,y:7},{x:16,y:7},{x:17,y:7},{x:18,y:7},{x:19,y:7}],
  // 6: 左上到右下
  [{x:0,y:0},{x:0,y:1},{x:0,y:2},{x:0,y:3},{x:0,y:4},{x:0,y:5},{x:1,y:5},{x:2,y:5},{x:3,y:5},{x:4,y:5},{x:5,y:5},{x:6,y:5},{x:7,y:5},{x:8,y:5},{x:8,y:4},{x:8,y:3},{x:8,y:2},{x:9,y:2},{x:10,y:2},{x:11,y:2},{x:12,y:2},{x:13,y:2},{x:14,y:2},{x:15,y:2},{x:16,y:2},{x:16,y:3},{x:16,y:4},{x:16,y:5},{x:16,y:6},{x:16,y:7},{x:16,y:8},{x:15,y:8},{x:14,y:8},{x:13,y:8},{x:12,y:8},{x:11,y:8},{x:10,y:8},{x:9,y:8},{x:8,y:8},{x:7,y:8},{x:6,y:8},{x:5,y:8},{x:4,y:8},{x:4,y:9},{x:4,y:10},{x:4,y:11},{x:4,y:12},{x:4,y:13},{x:5,y:13},{x:6,y:13},{x:7,y:13},{x:8,y:13},{x:9,y:13},{x:10,y:13},{x:11,y:13},{x:12,y:13},{x:13,y:13},{x:14,y:13},{x:15,y:13},{x:16,y:13},{x:17,y:13},{x:18,y:13},{x:19,y:13}],
  // 7: W型
  [{x:0,y:2},{x:1,y:2},{x:2,y:2},{x:3,y:2},{x:4,y:2},{x:4,y:3},{x:4,y:4},{x:4,y:5},{x:4,y:6},{x:5,y:6},{x:6,y:6},{x:7,y:6},{x:8,y:6},{x:9,y:6},{x:9,y:5},{x:9,y:4},{x:9,y:3},{x:9,y:2},{x:10,y:2},{x:11,y:2},{x:12,y:2},{x:13,y:2},{x:14,y:2},{x:14,y:3},{x:14,y:4},{x:14,y:5},{x:14,y:6},{x:15,y:6},{x:16,y:6},{x:17,y:6},{x:18,y:6},{x:19,y:6}],
  // 8: 左下到右上
  [{x:0,y:13},{x:1,y:13},{x:2,y:13},{x:3,y:13},{x:4,y:13},{x:5,y:13},{x:5,y:12},{x:5,y:11},{x:5,y:10},{x:5,y:9},{x:5,y:8},{x:5,y:7},{x:5,y:6},{x:5,y:5},{x:5,y:4},{x:6,y:4},{x:7,y:4},{x:8,y:4},{x:9,y:4},{x:10,y:4},{x:11,y:4},{x:12,y:4},{x:12,y:5},{x:12,y:6},{x:12,y:7},{x:12,y:8},{x:12,y:9},{x:12,y:10},{x:13,y:10},{x:14,y:10},{x:15,y:10},{x:16,y:10},{x:17,y:10},{x:18,y:10},{x:18,y:9},{x:18,y:8},{x:18,y:7},{x:18,y:6},{x:18,y:5},{x:18,y:4},{x:18,y:3},{x:18,y:2},{x:19,y:2}],
  // 9: 十字
  [{x:0,y:7},{x:1,y:7},{x:2,y:7},{x:3,y:7},{x:4,y:7},{x:5,y:7},{x:6,y:7},{x:7,y:7},{x:7,y:6},{x:7,y:5},{x:7,y:4},{x:7,y:3},{x:7,y:2},{x:7,y:1},{x:7,y:0},{x:8,y:0},{x:9,y:0},{x:10,y:0},{x:11,y:0},{x:12,y:0},{x:13,y:0},{x:13,y:1},{x:13,y:2},{x:13,y:3},{x:13,y:4},{x:13,y:5},{x:13,y:6},{x:13,y:7},{x:13,y:8},{x:13,y:9},{x:13,y:10},{x:13,y:11},{x:13,y:12},{x:13,y:13},{x:13,y:14},{x:14,y:14},{x:15,y:14},{x:16,y:14},{x:17,y:14},{x:18,y:14},{x:19,y:14}],
  // 10: 终极
  [{x:0,y:1},{x:1,y:1},{x:2,y:1},{x:3,y:1},{x:3,y:2},{x:3,y:3},{x:3,y:4},{x:3,y:5},{x:4,y:5},{x:5,y:5},{x:6,y:5},{x:7,y:5},{x:8,y:5},{x:8,y:4},{x:8,y:3},{x:8,y:2},{x:8,y:1},{x:9,y:1},{x:10,y:1},{x:11,y:1},{x:12,y:1},{x:13,y:1},{x:14,y:1},{x:15,y:1},{x:15,y:2},{x:15,y:3},{x:15,y:4},{x:15,y:5},{x:15,y:6},{x:15,y:7},{x:15,y:8},{x:15,y:9},{x:15,y:10},{x:14,y:10},{x:13,y:10},{x:12,y:10},{x:11,y:10},{x:10,y:10},{x:9,y:10},{x:8,y:10},{x:7,y:10},{x:6,y:10},{x:5,y:10},{x:5,y:11},{x:5,y:12},{x:5,y:13},{x:6,y:13},{x:7,y:13},{x:8,y:13},{x:9,y:13},{x:10,y:13},{x:11,y:13},{x:12,y:13},{x:13,y:13},{x:14,y:13},{x:15,y:13},{x:16,y:13},{x:17,y:13},{x:18,y:13},{x:19,y:13}]
];

function getCurrentPath(){ return LEVEL_PATHS[(state.level - 1) % LEVEL_PATHS.length]; }

function tileToPx(t){ return {x:t.x*TILE, y:t.y*TILE}; }
function dist(a,b){ return Math.hypot(a.x-b.x, a.y-b.y); }
function randRange(min,max){ return Math.random()*(max-min)+min; }
function isPointInRect(px, py, rx, ry, rw, rh){ return px>=rx && px<=rx+rw && py>=ry && py<=ry+rh; }

// =========================
// 音频引擎
// =========================
class AudioEngine {
  constructor(){
    this.ctx = null;
    this.master = null;
    this.volume = 0.35;
    this.muted = false;
    this.bgmInterval = null;
    this.nextNoteTime = 0;
    this.tempo = 0.18;
    this.beatIndex = 0;
    this.initialized = false;
  }

  init(){
    if(this.initialized) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContext();
    this.master = this.ctx.createGain();
    this.master.gain.value = this.volume;
    this.master.connect(this.ctx.destination);
    this.initialized = true;
    this.startBgm();
  }

  setVolume(v){
    this.volume = v;
    if(this.master) this.master.gain.value = this.muted ? 0 : v;
  }

  toggleMute(){
    this.muted = !this.muted;
    if(this.master) this.master.gain.value = this.muted ? 0 : this.volume;
    return this.muted;
  }

  playTone({freq=440, type='square', duration=0.1, gain=0.1, when=0, slideTo=null}){
    if(!this.ctx || this.muted) return;
    const t = this.ctx.currentTime + when;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = type;
    o.frequency.setValueAtTime(freq, t);
    if(slideTo != null) o.frequency.exponentialRampToValueAtTime(Math.max(slideTo, 20), t+duration);
    g.gain.setValueAtTime(gain, t);
    g.gain.exponentialRampToValueAtTime(0.001, t+duration);
    o.connect(g).connect(this.master);
    o.start(t);
    o.stop(t+duration+0.05);
  }

  playNoise(duration=0.15, gain=0.15){
    if(!this.ctx || this.muted) return;
    const t = this.ctx.currentTime;
    const bufferSize = Math.floor(this.ctx.sampleRate * duration);
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for(let i=0;i<bufferSize;i++) data[i] = Math.random()*2-1;
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;
    const g = this.ctx.createGain();
    g.gain.setValueAtTime(gain, t);
    g.gain.exponentialRampToValueAtTime(0.001, t+duration);
    noise.connect(g).connect(this.master);
    noise.start(t);
  }

  sfxShoot(type='basic'){
    if(!this.ctx) return;
    if(type==='sniper') this.playTone({freq:600,type:'sawtooth',duration:0.25,gain:0.12,slideTo:150});
    else if(type==='slow') this.playTone({freq:900,type:'sine',duration:0.15,gain:0.1,slideTo:400});
    else if(type==='splash') this.playTone({freq:300,type:'square',duration:0.18,gain:0.12,slideTo:80});
    else this.playTone({freq:700,type:'square',duration:0.1,gain:0.1,slideTo:300});
  }

  sfxBuild(){
    if(!this.ctx) return;
    this.playTone({freq:400,type:'square',duration:0.08,gain:0.1});
    this.playTone({freq:600,type:'square',duration:0.08,gain:0.1,when:0.08});
    this.playTone({freq:800,type:'square',duration:0.15,gain:0.1,when:0.16});
  }

  sfxUpgrade(){
    if(!this.ctx) return;
    this.playTone({freq:523,type:'square',duration:0.1,gain:0.1});
    this.playTone({freq:659,type:'square',duration:0.1,gain:0.1,when:0.08});
    this.playTone({freq:783,type:'square',duration:0.1,gain:0.1,when:0.16});
    this.playTone({freq:1046,type:'square',duration:0.2,gain:0.1,when:0.24});
  }

  sfxSell(){
    if(!this.ctx) return;
    this.playTone({freq:800,type:'square',duration:0.08,gain:0.1});
    this.playTone({freq:500,type:'square',duration:0.12,gain:0.1,when:0.08});
  }

  sfxExplode(){
    if(!this.ctx) return;
    this.playNoise(0.2, 0.2);
    this.playTone({freq:150,type:'sawtooth',duration:0.25,gain:0.15,slideTo:50});
  }

  sfxWaveStart(){
    if(!this.ctx) return;
    [330,392,494,659].forEach((f,i)=>this.playTone({freq:f,type:'square',duration:0.15,gain:0.1,when:i*0.12}));
  }

  sfxLevelUp(){
    if(!this.ctx) return;
    [523,659,783,1046].forEach((f,i)=>this.playTone({freq:f,type:'square',duration:0.2,gain:0.12,when:i*0.12}));
  }

  sfxVictory(){
    if(!this.ctx) return;
    [392,523,659,783,1046,1318].forEach((f,i)=>this.playTone({freq:f,type:'square',duration:0.25,gain:0.12,when:i*0.12}));
  }

  sfxGameOver(){
    if(!this.ctx) return;
    [523,494,466,440,415,392,370,349].forEach((f,i)=>this.playTone({freq:f,type:'sawtooth',duration:0.25,gain:0.12,when:i*0.15}));
  }

  startBgm(){
    if(!this.ctx) return;
    const schedule = ()=>{
      if(!this.ctx) return;
      const t = this.ctx.currentTime;
      while(this.nextNoteTime < t + 0.5){
        this.playBgmNote(this.nextNoteTime);
        this.nextNoteTime += this.tempo;
        this.beatIndex++;
      }
    };
    this.bgmInterval = setInterval(schedule, 200);
  }

  playBgmNote(when){
    if(this.muted || this.volume <= 0.001) return;
    const base = [220, 261.63, 329.63, 392];
    const idx = this.beatIndex % 16;
    const noteIndex = [0,2,1,3,2,1,3,2,0,2,1,3,2,0,3,1][idx];
    const freq = base[noteIndex] * (Math.random() > 0.95 ? 2 : 1);
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = 'triangle';
    o.frequency.value = freq;
    g.gain.setValueAtTime(0.06, when);
    g.gain.exponentialRampToValueAtTime(0.001, when + 0.14);
    o.connect(g).connect(this.master);
    o.start(when);
    o.stop(when + 0.16);
  }

  stopBgm(){
    if(this.bgmInterval) clearInterval(this.bgmInterval);
    this.bgmInterval = null;
  }
}
const audio = new AudioEngine();
function initAudioOnInteraction(){
  if(!audio.initialized) audio.init();
}
['click','keydown','touchstart'].forEach(evt=>document.addEventListener(evt, initAudioOnInteraction, {once:true}));

// =========================
// 难度配置
// =========================
const DIFFICULTY = {
  easy:   { hpMul: 0.75, speedMul: 0.85, maxTowers: 999, label: '简单', desc: '简单难度：敌人血量-25%，速度-15%，塔位无限制' },
  normal: { hpMul: 1.0,  speedMul: 1.0,  maxTowers: 22,  label: '普通', desc: '普通难度：标准敌人，最多建造22座塔' },
  hard:   { hpMul: 1.45, speedMul: 1.25, maxTowers: 14,  label: '困难', desc: '困难难度：敌人血量+45%，速度+25%，最多建造14座塔' },
};

// =========================
// 塔定义
// =========================
const TOWER_DEFS = {
  basic:  { name:'机枪塔', price:50,  range:110, damage:5,  cooldown:35, color:'#e94560', projectileSpeed:6 },
  sniper: { name:'狙击塔', price:80,  range:190, damage:24, cooldown:110, color:'#00bfff', projectileSpeed:10 },
  slow:   { name:'冰霜塔', price:70,  range:95,  damage:2,  cooldown:28, color:'#00ffff', projectileSpeed:5 },
  splash: { name:'爆破塔', price:120, range:105, damage:8,  cooldown:55, color:'#ff8c00', projectileSpeed:5.5 },
};

function getUpgradePrice(tower){
  const base = TOWER_DEFS[tower.type].price;
  return Math.floor(base * 0.55 * tower.level);
}

function upgradeTower(tower){
  tower.level++;
  tower.damage = Math.floor(tower.damage * 1.28);
  tower.range = Math.floor(tower.range * 1.1);
  tower.maxCooldown = Math.max(8, Math.floor(tower.maxCooldown * 0.93));
}

// =========================
// 游戏状态
// =========================
let state = {
  lives: 25,
  money: 180,
  wave: 1,
  level: 1,
  gameOver: false,
  victory: false,
  enemies: [],
  towers: [],
  projectiles: [],
  particles: [],
  waveInProgress: false,
  spawnTimer: 0,
  enemiesToSpawn: 0,
  spawnInterval: 50,
  selectedTower: 'basic',
  selectedTowerIndex: -1,
  difficulty: 'normal',
};

// =========================
// 绘制工具
// =========================
function drawPixelRect(x,y,w,h,color){
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), Math.floor(w), Math.floor(h));
}
function drawPixelCircle(cx,cy,r,color){
  ctx.fillStyle = color;
  for(let y=-r;y<=r;y++){
    for(let x=-r;x<=r;x++){
      if(x*x+y*y<=r*r+1) ctx.fillRect(Math.floor(cx+x), Math.floor(cy+y), 1, 1);
    }
  }
}
function drawCircleOutline(cx, cy, r, color){
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI*2);
  ctx.stroke();
}

// =========================
// 粒子
// =========================
class Particle {
  constructor(x,y,color,size=randRange(2,4)){
    this.x=x; this.y=y;
    this.vx=randRange(-1.5,1.5); this.vy=randRange(-1.5,1.5);
    this.life=20+Math.random()*10;
    this.color=color; this.size=size;
  }
  update(){ this.x+=this.vx; this.y+=this.vy; this.life--; }
  draw(){ drawPixelRect(this.x, this.y, this.size, this.size, this.color); }
}
function createParticles(x,y,color,count,size){
  for(let i=0;i<count;i++) state.particles.push(new Particle(x,y,color,size));
}

// =========================
// 敌人
// =========================
class Enemy {
  constructor(wave, level, difficulty, isBoss=false){
    this.pathIndex = 0;
    const path = getCurrentPath();
    const start = tileToPx(path[0]);
    this.x = start.x + TILE/2;
    this.y = start.y + TILE/2;

    const diff = DIFFICULTY[difficulty];
    let baseHp = 10 + wave * 4 + (level - 1) * 12;
    let baseSpeed = 1.0 + wave * 0.05 + (level - 1) * 0.12;

    if(isBoss){
      baseHp *= 7;
      baseSpeed *= 0.5;
    }

    this.baseSpeed = baseSpeed * diff.speedMul;
    this.speed = this.baseSpeed;
    this.hpMax = Math.floor(baseHp * diff.hpMul);
    this.hp = this.hpMax;
    this.radius = isBoss ? 14 : 8;
    this.reward = (5 + Math.floor(wave/2) + (level-1)) * (isBoss ? 10 : 1);
    this.dead = false;
    this.reached = false;
    this.slowTimer = 0;
    this.isBoss = isBoss;

    const hues = [0, 30, 120, 180, 240, 280, 60, 300];
    const hue = hues[((level-1)*3 + (wave-1)) % hues.length];
    this.colorBody = `hsl(${hue}, ${isBoss?80:70}%, ${isBoss?45:50}%)`;
    this.colorDark = `hsl(${hue}, ${isBoss?90:80}%, 30%)`;
  }

  applySlow(frames=100){ this.slowTimer = Math.max(this.slowTimer, frames); }

  update(){
    if(this.dead || this.reached) return;
    if(this.slowTimer > 0){ this.speed = this.baseSpeed * 0.5; this.slowTimer--; }
    else { this.speed = this.baseSpeed; }

    const path = getCurrentPath();
    const targetTile = path[this.pathIndex+1];
    if(!targetTile){ this.reached=true; state.lives--; updateUI(); return; }
    const target = tileToPx(targetTile);
    const tx = target.x + TILE/2;
    const ty = target.y + TILE/2;
    const dx = tx - this.x;
    const dy = ty - this.y;
    const d = Math.hypot(dx, dy);
    if(d <= this.speed){ this.x=tx; this.y=ty; this.pathIndex++; }
    else { this.x += (dx/d)*this.speed; this.y += (dy/d)*this.speed; }
  }

  draw(){
    if(this.dead) return;
    if(this.slowTimer > 0) drawPixelRect(this.x-10, this.y-10, 20, 20, 'rgba(0,255,255,0.25)');

    if(this.isBoss){
      drawPixelRect(this.x-12, this.y-12, 24, 22, this.colorBody);
      drawPixelRect(this.x-12, this.y+4, 24, 6, this.colorDark);
      drawPixelRect(this.x-5, this.y-6, 3, 3, '#fff');
      drawPixelRect(this.x+2, this.y-6, 3, 3, '#fff');
      drawPixelRect(this.x-8, this.y-16, 16, 4, '#ffd700');
      drawPixelRect(this.x-6, this.y-18, 4, 2, '#ffd700');
      drawPixelRect(this.x+2, this.y-18, 4, 2, '#ffd700');
      drawPixelRect(this.x-14, this.y-20, 28, 3, '#333');
      drawPixelRect(this.x-14, this.y-20, Math.ceil(28*(this.hp/this.hpMax)), 3, '#f0f');
    } else {
      drawPixelRect(this.x-8, this.y-8, 16, 14, this.colorBody);
      drawPixelRect(this.x-8, this.y+2, 16, 4, this.colorDark);
      drawPixelRect(this.x-4, this.y-4, 2, 2, '#fff');
      drawPixelRect(this.x+2, this.y-4, 2, 2, '#fff');
      drawPixelRect(this.x-10, this.y-12, 20, 3, '#333');
      drawPixelRect(this.x-10, this.y-12, Math.ceil(20*(this.hp/this.hpMax)), 3, this.hp/this.hpMax > 0.5 ? '#0f0' : this.hp/this.hpMax > 0.25 ? '#ff0' : '#f00');
    }
  }

  takeDamage(amount){
    this.hp -= amount;
    if(this.hp <= 0 && !this.dead){
      this.dead = true;
      state.money += this.reward;
      updateUI();
      createParticles(this.x, this.y, this.colorBody, this.isBoss ? 16 : 6, this.isBoss ? 5 : undefined);
    }
  }
}

// =========================
// 塔
// =========================
class Tower {
  constructor(cx, cy, type){
    this.cx = cx; this.cy = cy;
    const def = TOWER_DEFS[type];
    this.type = type;
    this.range = def.range;
    this.damage = def.damage;
    this.maxCooldown = def.cooldown;
    this.cooldown = 0;
    this.color = def.color;
    this.angle = 0;
    this.level = 1;
  }

  update(){
    if(this.cooldown > 0) this.cooldown--;
    let target = null, bestD = Infinity;
    for(const e of state.enemies){
      if(e.dead || e.reached) continue;
      const d = dist({x:this.cx, y:this.cy}, e);
      if(d <= this.range && d < bestD){ bestD = d; target = e; }
    }
    if(target){
      this.angle = Math.atan2(target.y - this.cy, target.x - this.cx);
      if(this.cooldown <= 0){ this.shoot(target); this.cooldown = this.maxCooldown; }
    }
  }

  shoot(target){
    const def = TOWER_DEFS[this.type];
    state.projectiles.push(new Projectile(this.cx, this.cy, target, this.damage, this.type, def.projectileSpeed));
    audio.sfxShoot(this.type);
  }

  draw(){
    drawPixelRect(this.cx-12, this.cy-12, 24, 24, '#555');
    drawPixelRect(this.cx-10, this.cy-10, 20, 20, '#777');
    ctx.save();
    ctx.translate(this.cx, this.cy);
    ctx.rotate(this.angle);
    if(this.type === 'basic'){
      drawPixelRect(-4, -4, 18, 8, this.color);
      drawPixelRect(4, -6, 8, 12, '#b02a40');
    } else if(this.type === 'sniper'){
      drawPixelRect(-4, -3, 26, 6, this.color);
      drawPixelRect(10, -5, 10, 10, '#0077aa');
    } else if(this.type === 'slow'){
      drawPixelRect(-4, -4, 14, 8, this.color);
      ctx.beginPath(); ctx.arc(6, 0, 5, 0, Math.PI*2); ctx.fillStyle = '#00cccc'; ctx.fill();
    } else if(this.type === 'splash'){
      drawPixelRect(-4, -5, 16, 10, this.color);
      drawPixelRect(6, -7, 8, 14, '#cc5500');
    }
    ctx.restore();
    drawPixelRect(this.cx-3, this.cy-3, 6, 6, '#fff');

    // 等级小标记
    if(this.level > 1){
      ctx.fillStyle = '#ffd700';
      ctx.font = 'bold 9px "Courier New"';
      ctx.textAlign = 'center';
      ctx.fillText('+'+(this.level-1), this.cx+8, this.cy-6);
    }
  }
}

// =========================
// 子弹
// =========================
class Projectile {
  constructor(x, y, target, damage, type, speed){
    this.x=x; this.y=y; this.target=target; this.damage=damage; this.type=type; this.speed=speed;
    this.dead=false;
  }
  update(){
    if(this.dead) return;
    if(this.target.dead || this.target.reached){ this.dead=true; return; }
    const dx = this.target.x - this.x;
    const dy = this.target.y - this.y;
    const d = Math.hypot(dx, dy);
    if(d <= this.speed){ this.hit(this.target); this.dead = true; }
    else { this.x += (dx/d)*this.speed; this.y += (dy/d)*this.speed; }
  }
  hit(enemy){
    if(this.type === 'splash'){
      audio.sfxExplode();
      createParticles(enemy.x, enemy.y, '#ff8c00', 10, 4);
      const radius = 48;
      for(const e of state.enemies){
        if(e.dead || e.reached) continue;
        if(dist({x:enemy.x, y:enemy.y}, e) <= radius) e.takeDamage(Math.floor(this.damage * 0.6));
      }
    } else if(this.type === 'slow'){
      enemy.applySlow(100);
      enemy.takeDamage(this.damage);
      createParticles(enemy.x, enemy.y, '#00ffff', 4);
    } else {
      enemy.takeDamage(this.damage);
      createParticles(enemy.x, enemy.y, '#ffeeaa', 3);
      if(this.type === 'sniper') createParticles(enemy.x, enemy.y, '#00bfff', 4);
    }
  }
  draw(){
    const colors = {basic:'#ffeeaa', sniper:'#00bfff', slow:'#aaffff', splash:'#ffaa00'};
    const r = this.type==='sniper'?3:2;
    drawPixelCircle(this.x, this.y, r, colors[this.type] || '#fff');
  }
}

// =========================
// 地图
// =========================
function drawMap(){
  drawPixelRect(0, 0, canvas.width, canvas.height, '#1e3a2f');
  const path = getCurrentPath();
  for(const t of path){
    const p = tileToPx(t);
    drawPixelRect(p.x, p.y, TILE, TILE, '#2a5298');
    drawPixelRect(p.x+2, p.y+2, TILE-4, TILE-4, '#366ab5');
  }
  const s = tileToPx(path[0]);
  drawPixelRect(s.x+4, s.y+4, TILE-8, TILE-8, '#0f0');
  const e = tileToPx(path[path.length-1]);
  drawPixelRect(e.x+4, e.y+4, TILE-8, TILE-8, '#f00');
}

// =========================
// 塔选中UI
// =========================
function drawSelectedTowerUI(){
  if(state.selectedTowerIndex < 0) return;
  const t = state.towers[state.selectedTowerIndex];
  if(!t) return;

  // 范围圈
  drawCircleOutline(t.cx, t.cy, t.range, '#fff');

  // 左上角拆塔按钮
  const sellX = t.cx - 22;
  const sellY = t.cy - 22;
  drawPixelRect(sellX, sellY, 16, 16, '#e94560');
  drawPixelRect(sellX+2, sellY+2, 2, 2, '#fff');
  drawPixelRect(sellX+4, sellY+4, 2, 2, '#fff');
  drawPixelRect(sellX+6, sellY+6, 2, 2, '#fff');
  drawPixelRect(sellX+8, sellY+8, 2, 2, '#fff');
  drawPixelRect(sellX+10, sellY+10, 2, 2, '#fff');
  drawPixelRect(sellX+12, sellY+12, 2, 2, '#fff');
  drawPixelRect(sellX+12, sellY+2, 2, 2, '#fff');
  drawPixelRect(sellX+10, sellY+4, 2, 2, '#fff');
  drawPixelRect(sellX+8, sellY+6, 2, 2, '#fff');
  drawPixelRect(sellX+4, sellY+8, 2, 2, '#fff');
  drawPixelRect(sellX+2, sellY+10, 2, 2, '#fff');

  // 右上角升级按钮
  const upX = t.cx + 6;
  const upY = t.cy - 22;
  drawPixelRect(upX, upY, 16, 16, '#ffd700');
  // 箭头
  const ax = upX + 8;
  const ay = upY + 4;
  drawPixelRect(ax-1, ay, 2, 6, '#222');
  drawPixelRect(ax-2, ay+1, 4, 1, '#222');
  drawPixelRect(ax-3, ay+2, 6, 1, '#222');
  drawPixelRect(ax-4, ay+3, 8, 1, '#222');

  // 升级价格提示
  const upPrice = getUpgradePrice(t);
  ctx.fillStyle = '#ffd700';
  ctx.font = '10px "Courier New"';
  ctx.textAlign = 'center';
  ctx.fillText(upPrice + '🪙', t.cx + 14, t.cy - 26);
}

// =========================
// 交互
// =========================
function getTileFromEvent(ev){
  const rect = canvas.getBoundingClientRect();
  const mx = ev.clientX - rect.left;
  const my = ev.clientY - rect.top;
  return { tx: Math.floor(mx/TILE), ty: Math.floor(my/TILE), mx, my };
}

function getTowerAtTile(tx, ty){
  return state.towers.findIndex(t=>{
    const tcx = Math.floor(t.cx/TILE);
    const tcy = Math.floor(t.cy/TILE);
    return tcx===tx && tcy===ty;
  });
}

function isPath(tx, ty){ return getCurrentPath().some(p=>p.x===tx && p.y===ty); }

canvas.addEventListener('click', e=>{
  if(state.gameOver || state.victory) return;
  const {tx, ty, mx, my} = getTileFromEvent(e);

  // 如果有选中塔，先检查是否点了按钮
  if(state.selectedTowerIndex >= 0){
    const t = state.towers[state.selectedTowerIndex];
    if(t){
      // 拆塔按钮
      if(isPointInRect(mx, my, t.cx - 22, t.cy - 22, 16, 16)){
        const refund = Math.floor(TOWER_DEFS[t.type].price * 0.5);
        state.money += refund;
        state.towers.splice(state.selectedTowerIndex, 1);
        state.selectedTowerIndex = -1;
        createParticles(t.cx, t.cy, '#aaa', 8);
        audio.sfxSell();
        updateUI();
        return;
      }
      // 升级按钮
      if(isPointInRect(mx, my, t.cx + 6, t.cy - 22, 16, 16)){
        const price = getUpgradePrice(t);
        if(state.money >= price){
          state.money -= price;
          upgradeTower(t);
          createParticles(t.cx, t.cy, '#ffd700', 10, 4);
          audio.sfxUpgrade();
          updateUI();
        }
        return;
      }
    }
  }

  // 点击空地或另一座塔 -> 切换/取消选中
  const towerIdx = getTowerAtTile(tx, ty);
  if(towerIdx >= 0){
    state.selectedTowerIndex = towerIdx;
    return;
  }

  // 取消选中
  state.selectedTowerIndex = -1;

  if(isPath(tx, ty)) return;

  // 建塔
  const type = state.selectedTower;
  const price = TOWER_DEFS[type].price;
  const diff = DIFFICULTY[state.difficulty];
  if(diff.maxTowers < 900 && state.towers.length >= diff.maxTowers) return;

  if(state.money >= price){
    state.money -= price;
    state.towers.push(new Tower(tx*TILE + TILE/2, ty*TILE + TILE/2, type));
    updateUI();
    audio.sfxBuild();
    createParticles(tx*TILE + TILE/2, ty*TILE + TILE/2, '#e94560', 8);
  }
});

// 塔选择栏
document.querySelectorAll('.tower-card').forEach(card=>{
  card.addEventListener('click', ()=>{
    document.querySelectorAll('.tower-card').forEach(c=>c.classList.remove('selected'));
    card.classList.add('selected');
    state.selectedTower = card.dataset.type;
    state.selectedTowerIndex = -1;
  });
});

// =========================
// 设置面板
// =========================
const settingsModal = document.getElementById('settings-modal');
const volumeSlider = document.getElementById('volume-slider');
const volumeValue = document.getElementById('volume-value');
const diffDesc = document.getElementById('diff-desc');

document.getElementById('settings-btn').addEventListener('click', ()=>{
  settingsModal.classList.remove('hidden');
});
document.getElementById('close-settings').addEventListener('click', ()=>{
  settingsModal.classList.add('hidden');
});

volumeSlider.addEventListener('input', ()=>{
  const val = parseInt(volumeSlider.value, 10);
  volumeValue.textContent = val + '%';
  audio.setVolume(val / 100);
});

document.querySelectorAll('.diff-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.diff-btn').forEach(b=>b.classList.remove('selected'));
    btn.classList.add('selected');
    state.difficulty = btn.dataset.diff;
    diffDesc.textContent = DIFFICULTY[state.difficulty].desc;
    updateUI();
  });
});

// =========================
// 游戏主逻辑
// =========================
function startNextWave(){
  if(state.waveInProgress || state.gameOver || state.victory) return;
  state.waveInProgress = true;
  state.enemiesToSpawn = 5 + state.wave * 2 + state.level;
  state.spawnTimer = 0;
  state.spawnInterval = Math.max(16, 50 - state.wave * 1.1 - state.level * 0.7);
  document.getElementById('start-wave').disabled = true;
  audio.sfxWaveStart();
}

function resetGame(){
  state = {
    lives: 25, money: 180, wave: 1, level: 1,
    gameOver: false, victory: false,
    enemies: [], towers: [], projectiles: [], particles: [],
    waveInProgress: false, spawnTimer: 0, enemiesToSpawn: 0, spawnInterval: 50,
    selectedTower: state.selectedTower || 'basic',
    selectedTowerIndex: -1,
    difficulty: state.difficulty || 'normal',
  };
  updateUI();
  document.getElementById('start-wave').disabled = false;
}

function updateUI(){
  document.getElementById('lives').textContent = state.lives;
  document.getElementById('money').textContent = state.money;
  document.getElementById('wave').textContent = state.wave;
  document.getElementById('level').textContent = state.level;
  const diff = DIFFICULTY[state.difficulty];
  const max = diff.maxTowers >= 900 ? '∞' : diff.maxTowers;
  document.getElementById('tower-count').textContent = state.towers.length;
  document.getElementById('tower-max').textContent = max;
  if(state.lives <= 0 && !state.gameOver){ state.gameOver = true; state.waveInProgress = false; audio.sfxGameOver(); }
}

function endWave(){
  state.waveInProgress = false;
  state.wave++;
  state.money += 35;

  if(state.wave > MAX_WAVES){
    state.level++;
    if(state.level > MAX_LEVELS){
      state.victory = true;
      state.waveInProgress = false;
      audio.sfxVictory();
      updateUI();
      return;
    }
    state.wave = 1;
    state.money += 200;
    state.towers = []; // 进入新关卡清空塔，增加策略性
    state.selectedTowerIndex = -1;
    audio.sfxLevelUp();
  }
  updateUI();
  document.getElementById('start-wave').disabled = false;
}

function spawnLogic(){
  if(!state.waveInProgress) return;
  if(state.enemiesToSpawn > 0){
    state.spawnTimer++;
    if(state.spawnTimer >= state.spawnInterval){
      state.spawnTimer = 0;
      const isBoss = (state.wave % 5 === 0) && (state.enemiesToSpawn === 1);
      state.enemies.push(new Enemy(state.wave, state.level, state.difficulty, isBoss));
      state.enemiesToSpawn--;
    }
  } else if(state.enemies.length === 0){
    endWave();
  }
}

function update(){
  if(state.gameOver || state.victory) return;
  spawnLogic();
  for(const e of state.enemies) e.update();
  state.enemies = state.enemies.filter(e=>!e.dead && !e.reached);
  for(const t of state.towers) t.update();
  for(const p of state.projectiles) p.update();
  state.projectiles = state.projectiles.filter(p=>!p.dead);
  for(const p of state.particles) p.update();
  state.particles = state.particles.filter(p=>p.life > 0);
  if(state.lives <= 0 && !state.gameOver){ state.gameOver = true; state.waveInProgress = false; audio.sfxGameOver(); }
}

function draw(){
  drawMap();
  for(const t of state.towers) t.draw();
  for(const e of state.enemies) e.draw();
  for(const p of state.projectiles) p.draw();
  for(const p of state.particles) p.draw();
  drawSelectedTowerUI();

  if(state.gameOver){
    drawPixelRect(0, 0, canvas.width, canvas.height, 'rgba(0,0,0,0.7)');
    ctx.fillStyle = '#e94560';
    ctx.font = 'bold 44px "Courier New"';
    ctx.textAlign = 'center';
    ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2);
    ctx.font = '16px "Courier New"';
    ctx.fillStyle = '#fff';
    ctx.fillText(`您坚持到了 关卡 ${state.level} - 波次 ${state.wave}`, canvas.width/2, canvas.height/2 + 36);
    ctx.fillText('点击 "重置游戏" 再战江湖', canvas.width/2, canvas.height/2 + 62);
  } else if(state.victory){
    drawPixelRect(0, 0, canvas.width, canvas.height, 'rgba(0,0,0,0.7)');
    ctx.fillStyle = '#ffd700';
    ctx.font = 'bold 44px "Courier New"';
    ctx.textAlign = 'center';
    ctx.fillText('VICTORY!', canvas.width/2, canvas.height/2);
    ctx.font = '16px "Courier New"';
    ctx.fillStyle = '#fff';
    ctx.fillText('恭喜通关全部10个关卡！', canvas.width/2, canvas.height/2 + 36);
    ctx.fillText('像素塔防大师！', canvas.width/2, canvas.height/2 + 62);
  }
}

function loop(){
  update();
  draw();
  requestAnimationFrame(loop);
}

// =========================
// 按钮事件
// =========================
document.getElementById('start-wave').addEventListener('click', startNextWave);
document.getElementById('reset').addEventListener('click', resetGame);

resetGame();
loop();
