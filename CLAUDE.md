# Sound Sigils — Project Specification

## What This Is
Audio representations of N'Ko sigils. Each of 10 N'Ko Unicode characters is mapped to a distinctive sonic signature that reflects its semantic meaning through frequency, rhythm, spatial audio, and timbre.

## Architecture
```
sound_sigils/           # Python package
├── __init__.py         # Public API exports
├── models.py           # SigilDefinition (frozen data) + SigilSound (runtime)
├── definitions.py      # The 10 canonical sigil definitions
├── generators.py       # Sample generators — one per sigil
├── audio.py            # WAV rendering and encoding
├── engine.py           # SoundSigils high-level API
└── cli.py              # CLI entry point

tests/                  # pytest suite (112 tests)
├── test_models.py
├── test_definitions.py
├── test_generators.py
├── test_audio.py
├── test_engine.py
└── test_cli.py

scripts/sigils.py       # Legacy standalone script (preserved for compat)
web/index.html          # Browser-based player with Web Audio API
audio/                  # Pre-generated WAV files
```

## Key Design Decisions
- **Pure stdlib** — no external deps. Audio synthesis uses `math`, `struct`, `wave`.
- **Separation of concerns** — definitions (data) vs generators (synthesis) vs audio (encoding) vs engine (orchestration).
- **Frozen definitions** — `SigilDefinition` is immutable. Generator functions are registered separately.
- **All N'Ko chars in U+07C0–U+07FF** — validated by tests.

## Commands
```bash
# Run tests
uv run python -m pytest tests/ -v

# CLI
uv run sound-sigils list
uv run sound-sigils info ߛ
uv run sound-sigils play ߛ
uv run sound-sigils waveform ߛ
uv run sound-sigils export ߛ -o out.wav
uv run sound-sigils export-all -o audio/

# Python API
from sound_sigils import SoundSigils
ss = SoundSigils()
ss.generate("ߛ")  # → WAV bytes
```

## Conventions
- Conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`)
- Generator functions: `gen_{name}(t, duration, freq) -> (left, right)`
- All samples clipped to [-1.0, 1.0] before encoding
- 44100 Hz, 16-bit, stereo WAV output
