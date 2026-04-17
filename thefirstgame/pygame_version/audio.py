import numpy as np
import pygame
import threading
import time

class AudioEngine:
    def __init__(self):
        # channels=2, buffer=1024 兼容性更好，部分声卡不支持单声道小buffer
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.initialized = False
        self.volume = 0.35
        self.muted = False
        self.bgm_thread = None
        self.bgm_stop = threading.Event()
        self.next_note_time = 0.0
        self.beat_index = 0
        self.tempo = 0.18

    def init(self):
        if self.initialized:
            return
        # 如果 mixer 已经被默认参数初始化，先退出再用指定参数重开
        if pygame.mixer.get_init() is not None:
            pygame.mixer.quit()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.initialized = True
        self.start_bgm()

    def set_volume(self, v):
        self.volume = v

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted

    def _generate_wave(self, freq, duration, wave_type='square', gain=0.1, slide_to=None):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        if slide_to is not None:
            freqs = np.linspace(freq, slide_to, len(t))
        else:
            freqs = np.full_like(t, freq)
        phase = np.cumsum(2 * np.pi * freqs / sample_rate)
        if wave_type == 'sine':
            wave = np.sin(phase)
        elif wave_type == 'sawtooth':
            wave = 2 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5))
        elif wave_type == 'triangle':
            wave = 2 * np.abs(2 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5))) - 1
        else:  # square
            wave = np.sign(np.sin(phase))
        env = np.ones_like(t)
        attack = int(0.01 * sample_rate)
        release = int(0.1 * sample_rate)
        if attack > 0:
            env[:attack] = np.linspace(0, 1, attack)
        if release > 0 and len(env) > release:
            env[-release:] = np.linspace(1, 0, release)
        wave = wave * env * gain * 32767
        wave = wave.astype(np.int16)
        # 如果 mixer 初始化为立体声，需要二维数组 (N, 2)
        if pygame.mixer.get_init() is not None and pygame.mixer.get_init()[2] == 2:
            wave = np.column_stack((wave, wave))
        return wave

    def _play_array(self, arr):
        if not self.initialized or self.muted or self.volume <= 0.001:
            return
        try:
            sound = pygame.sndarray.make_sound(np.ascontiguousarray(arr))
            sound.set_volume(self.volume)
            sound.play()
        except Exception:
            pass

    def play_tone(self, freq=440, wave_type='square', duration=0.1, gain=0.1, slide_to=None):
        arr = self._generate_wave(freq, duration, wave_type, gain, slide_to)
        self._play_array(arr)

    def play_noise(self, duration=0.15, gain=0.15):
        if not self.initialized or self.muted or self.volume <= 0.001:
            return
        sample_rate = 44100
        samples = np.random.uniform(-1, 1, int(sample_rate * duration))
        env = np.ones_like(samples)
        release = int(0.1 * sample_rate)
        if release > 0 and len(env) > release:
            env[-release:] = np.linspace(1, 0, release)
        samples = samples * env * gain * 32767
        samples = samples.astype(np.int16)
        if pygame.mixer.get_init() is not None and pygame.mixer.get_init()[2] == 2:
            samples = np.column_stack((samples, samples))
        self._play_array(samples)

    def _play_seq(self, seq):
        for note in seq:
            self.play_tone(*note)
            time.sleep(note[2] if len(note) > 2 else 0.1)

    def sfx_shoot(self, t='basic'):
        if t == 'sniper':
            self.play_tone(600, 'sawtooth', 0.25, 0.12, 150)
        elif t == 'slow':
            self.play_tone(900, 'sine', 0.15, 0.1, 400)
        elif t == 'splash':
            self.play_tone(300, 'square', 0.18, 0.12, 80)
        else:
            self.play_tone(700, 'square', 0.1, 0.1, 300)

    def sfx_build(self):
        seq = [(400,'square',0.08,0.1,None),(600,'square',0.08,0.1,None),(800,'square',0.15,0.1,None)]
        def runner():
            for s in seq:
                self.play_tone(s[0], s[1], s[2], s[3], s[4])
                time.sleep(s[2]+0.02)
        threading.Thread(target=runner, daemon=True).start()

    def sfx_upgrade(self):
        seq = [(523,'square',0.1,0.1,None),(659,'square',0.1,0.1,None),(783,'square',0.1,0.1,None),(1046,'square',0.2,0.1,None)]
        def runner():
            for s in seq:
                self.play_tone(s[0], s[1], s[2], s[3], s[4])
                time.sleep(s[2]+0.02)
        threading.Thread(target=runner, daemon=True).start()

    def sfx_sell(self):
        def runner():
            self.play_tone(800, 'square', 0.08, 0.1)
            time.sleep(0.1)
            self.play_tone(500, 'square', 0.12, 0.1)
        threading.Thread(target=runner, daemon=True).start()

    def sfx_explode(self):
        self.play_noise(0.2, 0.2)
        self.play_tone(150, 'sawtooth', 0.25, 0.15, 50)

    def sfx_wave_start(self):
        notes = [330, 392, 494, 659]
        def runner():
            for f in notes:
                self.play_tone(f, 'square', 0.15, 0.1)
                time.sleep(0.12)
        threading.Thread(target=runner, daemon=True).start()

    def sfx_level_up(self):
        notes = [523, 659, 783, 1046]
        def runner():
            for f in notes:
                self.play_tone(f, 'square', 0.2, 0.12)
                time.sleep(0.12)
        threading.Thread(target=runner, daemon=True).start()

    def sfx_victory(self):
        notes = [392, 523, 659, 783, 1046, 1318]
        def runner():
            for f in notes:
                self.play_tone(f, 'square', 0.25, 0.12)
                time.sleep(0.12)
        threading.Thread(target=runner, daemon=True).start()

    def sfx_game_over(self):
        notes = [523, 494, 466, 440, 415, 392, 370, 349]
        def runner():
            for f in notes:
                self.play_tone(f, 'sawtooth', 0.25, 0.12)
                time.sleep(0.15)
        threading.Thread(target=runner, daemon=True).start()

    def start_bgm(self):
        self.bgm_stop.clear()
        self.bgm_thread = threading.Thread(target=self._bgm_loop, daemon=True)
        self.bgm_thread.start()

    def stop_bgm(self):
        self.bgm_stop.set()

    def _bgm_loop(self):
        base = [220, 261.63, 329.63, 392]
        pattern = [0, 2, 1, 3, 2, 1, 3, 2, 0, 2, 1, 3, 2, 0, 3, 1]
        beat = 0
        while not self.bgm_stop.is_set():
            if not self.muted and self.volume > 0.001 and self.initialized:
                try:
                    idx = pattern[beat % 16]
                    freq = base[idx] * (2 if (beat % 16 == 7 or beat % 16 == 15) and np.random.rand() > 0.7 else 1)
                    arr = self._generate_wave(freq, 0.14, 'triangle', 0.06)
                    sound = pygame.sndarray.make_sound(np.ascontiguousarray(arr))
                    sound.set_volume(self.volume)
                    sound.play()
                except Exception:
                    pass
            beat += 1
            time.sleep(self.tempo)

audio = AudioEngine()
