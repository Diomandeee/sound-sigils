#!/usr/bin/env python3
"""
Sound Sigils - Audio representations of N'Ko sigils
HEF Instance: inst_20260131082127_609 | Generation: 5
"""

import argparse
import wave
import struct
import math
import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Callable
import subprocess
import tempfile

# Constants
SAMPLE_RATE = 44100
CHANNELS = 2  # Stereo for spatial effects

@dataclass
class SigilSound:
    """Audio characteristics for a sigil"""
    name: str
    sigil: str
    description: str
    base_freq: float
    duration: float
    generator: Callable  # Function to generate samples

class SoundSigils:
    """Generate and play N'Ko sigil sounds"""
    
    def __init__(self):
        self.sigils = self._define_sigils()
    
    def _define_sigils(self) -> dict:
        """Define the 10 N'Ko sigils with their audio characteristics"""
        return {
            # ߛ - Stabilization: Descending tone settling to steady hum
            'ߛ': SigilSound(
                name='stabilization',
                sigil='ߛ',
                description='Dispersion decreased',
                base_freq=440,
                duration=1.5,
                generator=self._gen_stabilization
            ),
            # ߜ - Dispersion: Expanding stereo, rising harmonics
            'ߜ': SigilSound(
                name='dispersion',
                sigil='ߜ',
                description='Spread increased',
                base_freq=330,
                duration=1.5,
                generator=self._gen_dispersion
            ),
            # ߕ - Transition: Sharp frequency shift, brief silence
            'ߕ': SigilSound(
                name='transition',
                sigil='ߕ',
                description='Change point',
                base_freq=523,
                duration=0.8,
                generator=self._gen_transition
            ),
            # ߙ - Return: Melodic resolution, home note return
            'ߙ': SigilSound(
                name='return',
                sigil='ߙ',
                description='Re-entry to basin',
                base_freq=392,
                duration=1.2,
                generator=self._gen_return
            ),
            # ߡ - Dwell: Long sustained tone, subtle warmth
            'ߡ': SigilSound(
                name='dwell',
                sigil='ߡ',
                description='Sustained stay',
                base_freq=349,
                duration=2.0,
                generator=self._gen_dwell
            ),
            # ߚ - Oscillation: Tremolo, rapid frequency modulation
            'ߚ': SigilSound(
                name='oscillation',
                sigil='ߚ',
                description='Rapid alternation',
                base_freq=466,
                duration=1.0,
                generator=self._gen_oscillation
            ),
            # ߞ - Recovery: Slow fade-in, gradual stabilization
            'ߞ': SigilSound(
                name='recovery',
                sigil='ߞ',
                description='Return latency',
                base_freq=294,
                duration=1.8,
                generator=self._gen_recovery
            ),
            # ߣ - Novelty: Surprising interval, new timbre
            'ߣ': SigilSound(
                name='novelty',
                sigil='ߣ',
                description='New basin',
                base_freq=587,
                duration=1.0,
                generator=self._gen_novelty
            ),
            # ߠ - Place-Shift: Spatial panning, Doppler effect
            'ߠ': SigilSound(
                name='place_shift',
                sigil='ߠ',
                description='Location change',
                base_freq=415,
                duration=1.3,
                generator=self._gen_place_shift
            ),
            # ߥ - Echo: Delayed repetition, reverb tail
            'ߥ': SigilSound(
                name='echo',
                sigil='ߥ',
                description='Pattern match',
                base_freq=370,
                duration=2.0,
                generator=self._gen_echo
            ),
        }
    
    def _lookup(self, key: str) -> Optional[SigilSound]:
        """Look up sigil by character or name"""
        if key in self.sigils:
            return self.sigils[key]
        # Search by name
        for sigil in self.sigils.values():
            if sigil.name == key.lower().replace('-', '_'):
                return sigil
        return None
    
    # =========== Sound Generators ===========
    
    def _gen_stabilization(self, t: float, duration: float, freq: float) -> tuple:
        """Descending tone settling to steady hum"""
        progress = t / duration
        # Frequency descends from 1.5x to 1x
        current_freq = freq * (1.5 - 0.5 * progress)
        # Amplitude envelope: attack then steady
        amp = min(1.0, t * 10) * 0.7
        val = amp * math.sin(2 * math.pi * current_freq * t)
        # Add warmth harmonic
        val += 0.2 * amp * math.sin(2 * math.pi * current_freq * 2 * t)
        return (val, val)  # Centered stereo
    
    def _gen_dispersion(self, t: float, duration: float, freq: float) -> tuple:
        """Expanding stereo, rising harmonics"""
        progress = t / duration
        # Rising frequency
        current_freq = freq * (1 + 0.3 * progress)
        amp = 0.6 * math.sin(math.pi * progress)  # Swell envelope
        val = amp * math.sin(2 * math.pi * current_freq * t)
        # Add expanding harmonics
        for i in range(2, 5):
            val += (amp * 0.3 / i) * math.sin(2 * math.pi * current_freq * i * t)
        # Stereo expansion
        pan = progress * 0.8
        left = val * (1 - pan)
        right = val * (1 + pan)
        return (left, right)
    
    def _gen_transition(self, t: float, duration: float, freq: float) -> tuple:
        """Sharp frequency shift with brief silence"""
        progress = t / duration
        if progress < 0.4:
            # First tone
            val = 0.7 * math.sin(2 * math.pi * freq * t)
        elif progress < 0.5:
            # Silence gap
            val = 0.0
        else:
            # Second tone (tritone away - dissonant shift)
            val = 0.7 * math.sin(2 * math.pi * freq * 1.414 * t)
        return (val, val)
    
    def _gen_return(self, t: float, duration: float, freq: float) -> tuple:
        """Melodic resolution, home note return"""
        progress = t / duration
        # V-I resolution: starts at dominant, resolves to tonic
        if progress < 0.4:
            current_freq = freq * 1.5  # Perfect fifth above
        elif progress < 0.6:
            current_freq = freq * 1.25  # Passing tone
        else:
            current_freq = freq  # Home
        amp = 0.6 * (1 - 0.3 * progress)  # Gentle decay
        val = amp * math.sin(2 * math.pi * current_freq * t)
        val += 0.2 * amp * math.sin(2 * math.pi * current_freq * 2 * t)
        return (val, val)
    
    def _gen_dwell(self, t: float, duration: float, freq: float) -> tuple:
        """Long sustained tone with subtle warmth"""
        progress = t / duration
        # Smooth envelope
        amp = 0.5 * math.sin(math.pi * progress)
        val = amp * math.sin(2 * math.pi * freq * t)
        # Warm harmonics
        val += 0.15 * amp * math.sin(2 * math.pi * freq * 2 * t)
        val += 0.08 * amp * math.sin(2 * math.pi * freq * 3 * t)
        # Subtle vibrato
        vibrato = 1 + 0.003 * math.sin(2 * math.pi * 5 * t)
        val *= vibrato
        return (val, val)
    
    def _gen_oscillation(self, t: float, duration: float, freq: float) -> tuple:
        """Tremolo and rapid frequency modulation"""
        progress = t / duration
        # Rapid tremolo (12Hz)
        tremolo = 0.5 + 0.5 * math.sin(2 * math.pi * 12 * t)
        # Frequency modulation
        fm = 1 + 0.1 * math.sin(2 * math.pi * 8 * t)
        amp = 0.6 * tremolo * math.sin(math.pi * progress)
        val = amp * math.sin(2 * math.pi * freq * fm * t)
        return (val, val)
    
    def _gen_recovery(self, t: float, duration: float, freq: float) -> tuple:
        """Slow fade-in, gradual stabilization"""
        progress = t / duration
        # Slow logarithmic fade-in
        amp = 0.6 * (1 - math.exp(-3 * progress))
        # Frequency wobbles then stabilizes
        wobble = 1 + 0.05 * math.sin(2 * math.pi * 3 * t) * (1 - progress)
        val = amp * math.sin(2 * math.pi * freq * wobble * t)
        val += 0.15 * amp * math.sin(2 * math.pi * freq * 2 * t)
        return (val, val)
    
    def _gen_novelty(self, t: float, duration: float, freq: float) -> tuple:
        """Surprising interval, new timbre"""
        progress = t / duration
        # Unexpected intervals
        intervals = [1.0, 1.26, 0.84, 1.12]  # Unusual ratios
        segment = int(progress * len(intervals))
        segment = min(segment, len(intervals) - 1)
        current_freq = freq * intervals[segment]
        amp = 0.6 * (1 - 0.5 * progress)
        # Ring modulation for alien timbre
        mod = math.sin(2 * math.pi * 73 * t)
        val = amp * math.sin(2 * math.pi * current_freq * t) * (0.7 + 0.3 * mod)
        return (val, val)
    
    def _gen_place_shift(self, t: float, duration: float, freq: float) -> tuple:
        """Spatial panning with Doppler effect"""
        progress = t / duration
        # Doppler: frequency shifts as "object" passes
        doppler = 1 + 0.15 * math.sin(2 * math.pi * progress)
        amp = 0.6 * math.sin(math.pi * progress)
        val = amp * math.sin(2 * math.pi * freq * doppler * t)
        # Panning sweeps across stereo field
        pan = math.sin(2 * math.pi * progress)
        left = val * (0.5 - 0.5 * pan)
        right = val * (0.5 + 0.5 * pan)
        return (left, right)
    
    def _gen_echo(self, t: float, duration: float, freq: float) -> tuple:
        """Delayed repetition with reverb tail"""
        progress = t / duration
        # Primary tone with decay
        amp = 0.6 * math.exp(-2 * progress)
        val = amp * math.sin(2 * math.pi * freq * t)
        # Echo delays
        delays = [0.15, 0.3, 0.45, 0.6]
        for i, delay in enumerate(delays):
            if t > delay:
                echo_amp = amp * 0.5 ** (i + 1)
                val += echo_amp * math.sin(2 * math.pi * freq * (t - delay))
        return (val * 0.9, val * 1.1)  # Slight stereo spread
    
    # =========== Audio Generation ===========
    
    def generate(self, key: str) -> bytes:
        """Generate WAV data for a sigil"""
        sigil = self._lookup(key)
        if not sigil:
            raise ValueError(f"Unknown sigil: {key}")
        
        samples = []
        num_samples = int(sigil.duration * SAMPLE_RATE)
        
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            left, right = sigil.generator(t, sigil.duration, sigil.base_freq)
            # Clip and convert to 16-bit
            left = max(-1, min(1, left))
            right = max(-1, min(1, right))
            samples.append(struct.pack('<hh',
                int(left * 32767),
                int(right * 32767)
            ))
        
        return self._create_wav(b''.join(samples))
    
    def _create_wav(self, audio_data: bytes) -> bytes:
        """Wrap raw audio in WAV format"""
        import io
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(CHANNELS)
            wav.setsampwidth(2)  # 16-bit
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes(audio_data)
        return buffer.getvalue()
    
    def export(self, key: str, output_path: str):
        """Export sigil to WAV file"""
        wav_data = self.generate(key)
        with open(output_path, 'wb') as f:
            f.write(wav_data)
        print(f"✓ Exported {key} to {output_path}")
    
    def export_all(self, output_dir: str):
        """Export all sigils to directory"""
        os.makedirs(output_dir, exist_ok=True)
        for sigil in self.sigils.values():
            path = os.path.join(output_dir, f"{sigil.name}.wav")
            self.export(sigil.sigil, path)
    
    def play(self, key: str, async_: bool = False):
        """Play sigil audio using system audio"""
        sigil = self._lookup(key)
        if not sigil:
            raise ValueError(f"Unknown sigil: {key}")
        
        wav_data = self.generate(key)
        
        # Write to temp file and play with afplay (macOS)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(wav_data)
            temp_path = f.name
        
        try:
            if sys.platform == 'darwin':
                cmd = ['afplay', temp_path]
            elif sys.platform.startswith('linux'):
                cmd = ['aplay', temp_path]
            else:
                cmd = ['powershell', '-c', f'(New-Object Media.SoundPlayer "{temp_path}").PlaySync()']
            
            print(f"🔊 Playing {sigil.sigil} ({sigil.name}): {sigil.description}")
            
            if async_:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(cmd, check=True)
        finally:
            if not async_:
                os.unlink(temp_path)
    
    def sequence(self, keys: List[str], gap: float = 0.1):
        """Play a sequence of sigils"""
        for key in keys:
            self.play(key)
    
    def list_sigils(self):
        """Print all available sigils"""
        print("\n🎵 Sound Sigils - N'Ko Audio Signatures\n")
        print(f"{'Sigil':<6} {'Name':<15} {'Description':<25} {'Freq':<8} {'Duration'}")
        print("-" * 70)
        for s in self.sigils.values():
            print(f"{s.sigil:<6} {s.name:<15} {s.description:<25} {s.base_freq:<8.0f} {s.duration}s")
        print()

def main():
    parser = argparse.ArgumentParser(description='Sound Sigils - N\'Ko Audio Representations')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    subparsers.add_parser('list', help='List all sigils')
    
    # Play command
    play_parser = subparsers.add_parser('play', help='Play a sigil')
    play_parser.add_argument('sigil', help='Sigil character or name')
    
    # Sequence command
    seq_parser = subparsers.add_parser('sequence', help='Play a sequence of sigils')
    seq_parser.add_argument('sigils', help='Space-separated sigils')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export sigil to WAV')
    export_parser.add_argument('sigil', help='Sigil character or name')
    export_parser.add_argument('--output', '-o', required=True, help='Output file path')
    
    # Export all command
    export_all_parser = subparsers.add_parser('export-all', help='Export all sigils')
    export_all_parser.add_argument('--output', '-o', required=True, help='Output directory')
    
    args = parser.parse_args()
    ss = SoundSigils()
    
    if args.command == 'list':
        ss.list_sigils()
    elif args.command == 'play':
        ss.play(args.sigil)
    elif args.command == 'sequence':
        sigils = args.sigils.split()
        ss.sequence(sigils)
    elif args.command == 'export':
        ss.export(args.sigil, args.output)
    elif args.command == 'export-all':
        ss.export_all(args.output)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
