"""Generate a deterministic original 17.6-second percussive soundtrack.

All tones and rhythm are mathematically synthesized from sine waves and noise.
No sampled recordings, music libraries, third-party music, or OS system voices.
"""
import math, random, struct, wave
from pathlib import Path
RATE=44100
DURATION=17.6
BPM=96
BEAT=60/BPM
NOTES=(261.63,329.63,392.00,329.63,293.66,349.23,440.00,349.23)
CHORDS=((130.81,164.81,196.00),(98.00,146.83,196.00),(110.00,130.81,164.81),(87.31,130.81,174.61))
R=random.Random(9102026)
WAV=Path(__file__).with_name('original-soundtrack.wav')
with wave.open(str(WAV),'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    block=bytearray()
    for n in range(round(DURATION*RATE)):
        t=n/RATE
        beat_i=int(t/BEAT)
        phase=t%BEAT
        chord=CHORDS[(beat_i//4)%4]
        chord_phase=t%(4*BEAT)
        pad_envelope=min(1.0, chord_phase/0.16)*min(1.0,(4*BEAT-chord_phase)/0.18)
        pad=sum(math.sin(2*math.pi*f*t) for f in chord)/3*0.095*pad_envelope
        tone=math.sin(2*math.pi*NOTES[beat_i%8]*t)*0.17*math.exp(-5.5*phase)
        kick=0.17*math.sin(2*math.pi*(70*phase-24*phase*phase))*math.exp(-23*phase)
        hat=(2*R.random()-1)*0.034*math.exp(-105*phase)
        envelope=min(1.0,t/0.5)*min(1.0,(DURATION-t)/1.0)
        sample=max(-0.96,min(0.96,(pad+tone+kick+hat)*envelope))
        block.extend(struct.pack('<h',round(sample*32767)))
        if len(block)>=131072:
            w.writeframes(block)
            block.clear()
    if block:
        w.writeframes(block)
print('original_soundtrack_ready',WAV.stat().st_size)
