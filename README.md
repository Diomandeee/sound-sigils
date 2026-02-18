# Sound Sigils ߛ🔊

**Audio representations of N'Ko sigils that convey meaning through tone**

## Overview

Sound Sigils translates the 10 N'Ko inscription sigils into distinctive audio signatures. Each sigil's sonic characteristics reflect its semantic meaning, creating an auditory language that can be perceived, learned, and used alongside the visual glyphs.

## The 10 Sound Sigils

| Sigil | Name | Meaning | Sound Characteristics |
|-------|------|---------|----------------------|
| ߛ | Stabilization | Dispersion decreased | Descending tone settling to steady hum |
| ߜ | Dispersion | Spread increased | Expanding stereo, rising harmonics |
| ߕ | Transition | Change point | Sharp frequency shift, brief silence |
| ߙ | Return | Re-entry to basin | Melodic resolution, home note return |
| ߡ | Dwell | Sustained stay | Long sustained tone, subtle warmth |
| ߚ | Oscillation | Rapid alternation | Tremolo, rapid frequency modulation |
| ߞ | Recovery | Return latency | Slow fade-in, gradual stabilization |
| ߣ | Novelty | New basin | Surprising interval, new timbre |
| ߠ | Place-Shift | Location change | Spatial panning, Doppler effect |
| ߥ | Echo | Pattern match | Delayed repetition, reverb tail |

## Installation

```bash
# Install from source
pip install -e .

# Or run directly with uv
uv run sound-sigils list
```

## Usage

### CLI

```bash
# List all sigils
sound-sigils list

# Show detailed info
sound-sigils info ߛ

# Play a sigil
sound-sigils play ߛ
sound-sigils play stabilization

# Play a sequence
sound-sigils sequence "ߛ ߕ ߙ"

# View ASCII waveform
sound-sigils waveform ߛ

# Export to WAV
sound-sigils export ߛ -o audio/stabilization.wav

# Export all sigils
sound-sigils export-all -o audio/
```

### Python API

```python
from sound_sigils import SoundSigils

ss = SoundSigils()

# Lookup
sigil = ss.lookup("ߛ")           # by character
sigil = ss.lookup("stabilization")  # by name

# Generate WAV bytes
wav_data = ss.generate("ߛ")

# Play through speakers
ss.play("ߛ")

# Play a sequence
ss.play_sequence(["ߛ", "ߕ", "ߙ"])

# Export
ss.export("ߛ", "output.wav")
ss.export_all("audio/")

# Iterate
for sigil in ss:
    print(f"{sigil.char} — {sigil.name}")
```

### Web Interface

```bash
python -m http.server 8080 -d web
# Open http://localhost:8080
```

The web interface uses the Web Audio API to synthesize sounds in the browser. Click any sigil card to hear it and build sequences.

## Sound Design Philosophy

Each sigil's audio is designed around three principles:

1. **Semantic Mapping** — The sound behavior mirrors the sigil's meaning
2. **Distinctiveness** — Each sigil is immediately recognizable
3. **Combinability** — Sigils can be sequenced into "sound sentences"

## Audio Specifications

- **Sample Rate**: 44,100 Hz
- **Bit Depth**: 16-bit
- **Channels**: Stereo
- **Format**: WAV (uncompressed)
- **Duration**: 0.8–2.0 seconds per sigil

## Project Structure

```
sound_sigils/           # Python package
├── __init__.py         # Public API
├── models.py           # Data models
├── definitions.py      # Sigil definitions
├── generators.py       # Audio synthesis functions
├── audio.py            # WAV rendering
├── engine.py           # High-level API
└── cli.py              # Command-line interface

tests/                  # Test suite (112 tests)
scripts/sigils.py       # Legacy standalone script
web/index.html          # Browser player
audio/                  # Pre-generated WAV files
```

## Development

```bash
# Run tests
uv run python -m pytest tests/ -v

# Run with coverage
uv run python -m pytest tests/ -v --cov=sound_sigils
```

## Applications

1. **Accessibility** — Audio cues for visual N'Ko annotations
2. **Learning** — Sound-symbol association for N'Ko learners
3. **Monitoring** — Audio alerts for system events
4. **Composition** — Generative music from attention basin trajectories
5. **Meditation** — Ambient soundscapes from consciousness maps

## License

MIT License
