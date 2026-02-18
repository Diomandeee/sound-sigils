"""Sample generators for each N'Ko sigil.

Every generator has the same signature::

    def gen_NAME(t: float, duration: float, freq: float) -> tuple[float, float]

Where *t* is the current time in seconds, *duration* is the total length,
*freq* is the base frequency, and the return is ``(left, right)`` in [-1, 1].
"""

from __future__ import annotations

import math
from typing import Callable, Tuple

GeneratorFn = Callable[[float, float, float], Tuple[float, float]]


# ── Stability Group ───────────────────────────────────────────────


def gen_stabilization(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Descending tone settling to steady hum."""
    progress = t / duration
    current_freq = freq * (1.5 - 0.5 * progress)
    amp = min(1.0, t * 10) * 0.7
    val = amp * math.sin(2 * math.pi * current_freq * t)
    val += 0.2 * amp * math.sin(2 * math.pi * current_freq * 2 * t)
    return (val, val)


def gen_dispersion(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Expanding stereo, rising harmonics."""
    progress = t / duration
    current_freq = freq * (1 + 0.3 * progress)
    amp = 0.6 * math.sin(math.pi * progress)
    val = amp * math.sin(2 * math.pi * current_freq * t)
    for i in range(2, 5):
        val += (amp * 0.3 / i) * math.sin(2 * math.pi * current_freq * i * t)
    pan = progress * 0.8
    left = val * (1 - pan)
    right = val * (1 + pan)
    return (left, right)


# ── Change Group ──────────────────────────────────────────────────


def gen_transition(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Sharp frequency shift with brief silence."""
    progress = t / duration
    if progress < 0.4:
        val = 0.7 * math.sin(2 * math.pi * freq * t)
    elif progress < 0.5:
        val = 0.0
    else:
        val = 0.7 * math.sin(2 * math.pi * freq * 1.414 * t)
    return (val, val)


def gen_return(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Melodic resolution, home note return (V → I)."""
    progress = t / duration
    if progress < 0.4:
        current_freq = freq * 1.5
    elif progress < 0.6:
        current_freq = freq * 1.25
    else:
        current_freq = freq
    amp = 0.6 * (1 - 0.3 * progress)
    val = amp * math.sin(2 * math.pi * current_freq * t)
    val += 0.2 * amp * math.sin(2 * math.pi * current_freq * 2 * t)
    return (val, val)


def gen_dwell(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Long sustained tone with subtle warmth and vibrato."""
    progress = t / duration
    amp = 0.5 * math.sin(math.pi * progress)
    val = amp * math.sin(2 * math.pi * freq * t)
    val += 0.15 * amp * math.sin(2 * math.pi * freq * 2 * t)
    val += 0.08 * amp * math.sin(2 * math.pi * freq * 3 * t)
    vibrato = 1 + 0.003 * math.sin(2 * math.pi * 5 * t)
    val *= vibrato
    return (val, val)


def gen_oscillation(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Tremolo and rapid frequency modulation."""
    progress = t / duration
    tremolo = 0.5 + 0.5 * math.sin(2 * math.pi * 12 * t)
    fm = 1 + 0.1 * math.sin(2 * math.pi * 8 * t)
    amp = 0.6 * tremolo * math.sin(math.pi * progress)
    val = amp * math.sin(2 * math.pi * freq * fm * t)
    return (val, val)


# ── Spatial Group ─────────────────────────────────────────────────


def gen_recovery(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Slow fade-in, gradual stabilization."""
    progress = t / duration
    amp = 0.6 * (1 - math.exp(-3 * progress))
    wobble = 1 + 0.05 * math.sin(2 * math.pi * 3 * t) * (1 - progress)
    val = amp * math.sin(2 * math.pi * freq * wobble * t)
    val += 0.15 * amp * math.sin(2 * math.pi * freq * 2 * t)
    return (val, val)


def gen_novelty(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Surprising interval, new timbre via ring modulation."""
    progress = t / duration
    intervals = [1.0, 1.26, 0.84, 1.12]
    segment = min(int(progress * len(intervals)), len(intervals) - 1)
    current_freq = freq * intervals[segment]
    amp = 0.6 * (1 - 0.5 * progress)
    mod = math.sin(2 * math.pi * 73 * t)
    val = amp * math.sin(2 * math.pi * current_freq * t) * (0.7 + 0.3 * mod)
    return (val, val)


def gen_place_shift(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Spatial panning with Doppler effect."""
    progress = t / duration
    doppler = 1 + 0.15 * math.sin(2 * math.pi * progress)
    amp = 0.6 * math.sin(math.pi * progress)
    val = amp * math.sin(2 * math.pi * freq * doppler * t)
    pan = math.sin(2 * math.pi * progress)
    left = val * (0.5 - 0.5 * pan)
    right = val * (0.5 + 0.5 * pan)
    return (left, right)


# ── Temporal Group ────────────────────────────────────────────────


def gen_echo(t: float, duration: float, freq: float) -> tuple[float, float]:
    """Delayed repetition with reverb tail."""
    progress = t / duration
    amp = 0.6 * math.exp(-2 * progress)
    val = amp * math.sin(2 * math.pi * freq * t)
    delays = [0.15, 0.3, 0.45, 0.6]
    for i, delay in enumerate(delays):
        if t > delay:
            echo_amp = amp * 0.5 ** (i + 1)
            val += echo_amp * math.sin(2 * math.pi * freq * (t - delay))
    return (val * 0.9, val * 1.1)


# ── Registry ──────────────────────────────────────────────────────

GENERATOR_REGISTRY: dict[str, GeneratorFn] = {
    "stabilization": gen_stabilization,
    "dispersion": gen_dispersion,
    "transition": gen_transition,
    "return": gen_return,
    "dwell": gen_dwell,
    "oscillation": gen_oscillation,
    "recovery": gen_recovery,
    "novelty": gen_novelty,
    "place_shift": gen_place_shift,
    "echo": gen_echo,
}
