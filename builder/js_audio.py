# -*- coding: utf-8 -*-

JS_AUDIO = """
    /*************************************************************************
     * 3. PROCEDURAL WEB AUDIO SYNTHESIZER (MUSIC & SFX - ZERO EXTERNAL ASSETS)
     *************************************************************************/
    class ProceduralAudioEngine {
      constructor() {
        this.ctx = null;
        this.masterGain = null;
        this.musicGain = null;
        this.sfxGain = null;
        this.bgmTimer = null;
        this.isPlayingBgm = false;
        this.stepIndex = 0;
      }

      init() {
        if (this.ctx) return;
        try {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioContext();

          this.masterGain = this.ctx.createGain();
          this.masterGain.gain.value = 1.0;
          this.masterGain.connect(this.ctx.destination);

          this.musicGain = this.ctx.createGain();
          this.musicGain.gain.value = (state.settings.musicVol || 70) / 100;
          this.musicGain.connect(this.masterGain);

          this.sfxGain = this.ctx.createGain();
          this.sfxGain.gain.value = (state.settings.sfxVol || 85) / 100;
          this.sfxGain.connect(this.masterGain);

          this.startBgmLoop();
        } catch (e) {
          console.warn('Web Audio not supported or blocked:', e);
        }
      }

      ensureContext() {
        if (!this.ctx) {
          this.init();
        } else if (this.ctx.state === 'suspended') {
          this.ctx.resume();
        }
      }

      setMusicVol(pct) {
        if (this.musicGain && this.ctx) {
          this.musicGain.gain.setValueAtTime(pct / 100, this.ctx.currentTime);
        }
      }

      setSfxVol(pct) {
        if (this.sfxGain && this.ctx) {
          this.sfxGain.gain.setValueAtTime(pct / 100, this.ctx.currentTime);
        }
      }

      // Procedural Upbeat Roblox BGM Synthesizer Loop (124 BPM)
      startBgmLoop() {
        if (this.isPlayingBgm || !this.ctx) return;
        this.isPlayingBgm = true;

        const melody = [
          523.25, 659.25, 783.99, 1046.50, // C5, E5, G5, C6
          587.33, 698.46, 880.00, 1046.50, // D5, F5, A5, C6
          659.25, 783.99, 987.77, 1174.66, // E5, G5, B5, D6
          783.99, 659.25, 523.25, 392.00   // G5, E5, C5, G4
        ];
        const bass = [
          130.81, 130.81, 164.81, 196.00, // C3, C3, E3, G3
          146.83, 146.83, 174.61, 220.00, // D3, D3, F3, A3
          164.81, 164.81, 196.00, 246.94, // E3, E3, G3, B3
          196.00, 196.00, 164.81, 130.81  // G3, G3, E3, C3
        ];

        const stepDuration = 0.24; // ~124 BPM sixteenth notes

        const scheduleNote = () => {
          if (!this.isPlayingBgm || !this.ctx) return;
          const now = this.ctx.currentTime;
          const mFreq = melody[this.stepIndex % melody.length];
          const bFreq = bass[this.stepIndex % bass.length];

          // Lead synth note
          if (mFreq) {
            const osc = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            const filter = this.ctx.createBiquadFilter();

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(mFreq, now);

            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(1400, now);

            g.gain.setValueAtTime(0.06, now);
            g.gain.exponentialRampToValueAtTime(0.001, now + stepDuration * 0.9);

            osc.connect(filter);
            filter.connect(g);
            g.connect(this.musicGain);

            osc.start(now);
            osc.stop(now + stepDuration);
          }

          // Bass groove
          if (this.stepIndex % 2 === 0) {
            const bOsc = this.ctx.createOscillator();
            const bG = this.ctx.createGain();
            bOsc.type = 'sine';
            bOsc.frequency.setValueAtTime(bFreq, now);
            bG.gain.setValueAtTime(0.08, now);
            bG.gain.exponentialRampToValueAtTime(0.001, now + stepDuration * 1.8);
            bOsc.connect(bG);
            bG.connect(this.musicGain);
            bOsc.start(now);
            bOsc.stop(now + stepDuration * 1.8);
          }

          this.stepIndex++;
          this.bgmTimer = setTimeout(scheduleNote, stepDuration * 1000);
        };

        scheduleNote();
      }

      playClickSound() {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(400, now + 0.05);
        g.gain.setValueAtTime(0.2, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
        osc.connect(g);
        g.connect(this.sfxGain);
        osc.start(now);
        osc.stop(now + 0.05);
      }

      playThrowSound(isSurge, isCritical) {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;

        // Base Whoosh
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.exponentialRampToValueAtTime(isSurge ? 1100 : 660, now + 0.28);
        g.gain.setValueAtTime(0.35, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.connect(g);
        g.connect(this.sfxGain);
        osc.start(now);
        osc.stop(now + 0.3);

        // Max Surge Sonic Boom
        if (isSurge) {
          const boom = this.ctx.createOscillator();
          const boomG = this.ctx.createGain();
          boom.type = 'sawtooth';
          boom.frequency.setValueAtTime(140, now);
          boom.frequency.exponentialRampToValueAtTime(40, now + 0.4);
          boomG.gain.setValueAtTime(0.4, now);
          boomG.gain.exponentialRampToValueAtTime(0.001, now + 0.42);
          boom.connect(boomG);
          boomG.connect(this.sfxGain);
          boom.start(now);
          boom.stop(now + 0.42);
        }

        // Critical Point Sparkle Chime
        if (isCritical) {
          [1200, 1600, 2400].forEach((freq, idx) => {
            const ch = this.ctx.createOscillator();
            const chG = this.ctx.createGain();
            ch.type = 'sine';
            ch.frequency.setValueAtTime(freq, now + idx * 0.06);
            chG.gain.setValueAtTime(0.25, now + idx * 0.06);
            chG.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.25);
            ch.connect(chG);
            chG.connect(this.sfxGain);
            ch.start(now + idx * 0.06);
            ch.stop(now + idx * 0.06 + 0.25);
          });
        }
      }

      playCatchSound(isNew, rarity) {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const notes = isNew ? [523.25, 659.25, 783.99, 1046.50, 1318.51] : [587.33, 783.99, 1046.50];
        notes.forEach((freq, i) => {
          const osc = this.ctx.createOscillator();
          const g = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + i * 0.08);
          g.gain.setValueAtTime(0.3, now + i * 0.08);
          g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.35);
          osc.connect(g);
          g.connect(this.sfxGain);
          osc.start(now + i * 0.08);
          osc.stop(now + i * 0.08 + 0.35);
        });
      }

      playPullUpSound(isPerfect) {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = isPerfect ? 'triangle' : 'sine';
        osc.frequency.setValueAtTime(isPerfect ? 880 : 440, now);
        osc.frequency.exponentialRampToValueAtTime(isPerfect ? 1320 : 660, now + 0.12);
        g.gain.setValueAtTime(0.28, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
        osc.connect(g);
        g.connect(this.sfxGain);
        osc.start(now);
        osc.stop(now + 0.14);
      }

      playCoinSound() {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc1 = this.ctx.createOscillator();
        const osc2 = this.ctx.createOscillator();
        const g = this.ctx.createGain();

        osc1.type = 'sine';
        osc2.type = 'sine';
        osc1.frequency.setValueAtTime(987.77, now); // B5
        osc2.frequency.setValueAtTime(1318.51, now + 0.07); // E6

        g.gain.setValueAtTime(0.2, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.25);

        osc1.connect(g);
        osc2.connect(g);
        g.connect(this.sfxGain);

        osc1.start(now);
        osc1.stop(now + 0.08);
        osc2.start(now + 0.07);
        osc2.stop(now + 0.25);
      }

      playLevelUpSound() {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const chords = [523.25, 659.25, 783.99, 1046.50];
        chords.forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const g = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.05);
          g.gain.setValueAtTime(0.25, now + idx * 0.05);
          g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.05 + 0.4);
          osc.connect(g);
          g.connect(this.sfxGain);
          osc.start(now + idx * 0.05);
          osc.stop(now + idx * 0.05 + 0.4);
        });
      }

      playUnlockSound() {
        this.ensureContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        [440, 554.37, 659.25, 880, 1108.73].forEach((f, idx) => {
          const osc = this.ctx.createOscillator();
          const g = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(f, now + idx * 0.06);
          g.gain.setValueAtTime(0.25, now + idx * 0.06);
          g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.3);
          osc.connect(g);
          g.connect(this.sfxGain);
          osc.start(now + idx * 0.06);
          osc.stop(now + idx * 0.06 + 0.3);
        });
      }
    }

    const audio = new ProceduralAudioEngine();
    // Wake up audio on first interaction
    ['click', 'keydown', 'touchstart'].forEach(ev => {
      window.addEventListener(ev, () => audio.ensureContext(), { once: true });
    });
"""

