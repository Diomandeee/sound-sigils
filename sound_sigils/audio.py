"""Audio generation and WAV encoding for Sound Sigils."""

from __future__ import annotations

import io
import struct
import wave
from typing import Sequence

from sound_sigils.models import SigilSound

SAMPLE_RATE: int = 44100
CHANNELS: int = 2  # Stereo
BIT_DEPTH: int = 16
MAX_AMPLITUDE: int = 32767


def render_samples(
    sigil: SigilSound,
    *,
    sample_rate: int = SAMPLE_RATE,
    duration_override: float | None = None,
    freq_override: float | None = None,
) -> list[tuple[float, float]]:
    """Render a sigil to a list of ``(left, right)`` float sample pairs.

    Args:
        sigil: The sigil to render.
        sample_rate: Output sample rate in Hz.
        duration_override: Override the sigil's default duration.
        freq_override: Override the sigil's base frequency.

    Returns:
        List of (left, right) tuples with values in [-1.0, 1.0].
    """
    duration = duration_override if duration_override is not None else sigil.duration
    freq = freq_override if freq_override is not None else sigil.base_freq
    num_samples = int(duration * sample_rate)

    samples: list[tuple[float, float]] = []
    for i in range(num_samples):
        t = i / sample_rate
        left, right = sigil.generator(t, duration, freq)
        left = max(-1.0, min(1.0, left))
        right = max(-1.0, min(1.0, right))
        samples.append((left, right))

    return samples


def samples_to_wav(
    samples: Sequence[tuple[float, float]],
    *,
    sample_rate: int = SAMPLE_RATE,
) -> bytes:
    """Encode ``(left, right)`` float samples into WAV bytes.

    Args:
        samples: Iterable of (left, right) in [-1.0, 1.0].
        sample_rate: Output sample rate in Hz.

    Returns:
        Complete WAV file as bytes.
    """
    packed = b"".join(
        struct.pack("<hh", int(l * MAX_AMPLITUDE), int(r * MAX_AMPLITUDE))
        for l, r in samples
    )

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(CHANNELS)
        wav.setsampwidth(BIT_DEPTH // 8)
        wav.setframerate(sample_rate)
        wav.writeframes(packed)
    return buf.getvalue()


def generate_wav(
    sigil: SigilSound,
    *,
    sample_rate: int = SAMPLE_RATE,
    duration_override: float | None = None,
    freq_override: float | None = None,
) -> bytes:
    """One-shot: render a sigil directly to WAV bytes."""
    samples = render_samples(
        sigil,
        sample_rate=sample_rate,
        duration_override=duration_override,
        freq_override=freq_override,
    )
    return samples_to_wav(samples, sample_rate=sample_rate)


def generate_sequence_wav(
    sigils: Sequence[SigilSound],
    *,
    gap: float = 0.1,
    sample_rate: int = SAMPLE_RATE,
) -> bytes:
    """Render a sequence of sigils into a single WAV file.

    Args:
        sigils: Ordered list of sigils to play.
        gap: Silence gap in seconds between each sigil.
        sample_rate: Output sample rate in Hz.

    Returns:
        Complete WAV file as bytes.
    """
    all_samples: list[tuple[float, float]] = []
    gap_samples = int(gap * sample_rate)
    silence = [(0.0, 0.0)] * gap_samples

    for i, sigil in enumerate(sigils):
        all_samples.extend(render_samples(sigil, sample_rate=sample_rate))
        if i < len(sigils) - 1:
            all_samples.extend(silence)

    return samples_to_wav(all_samples, sample_rate=sample_rate)
