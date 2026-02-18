"""Canonical definitions for the 10 N'Ko sound sigils.

Each sigil maps an N'Ko character to semantic meaning and audio parameters.
The generator functions live in :mod:`sound_sigils.generators`.
"""

from __future__ import annotations

from sound_sigils.models import SigilDefinition

# Ordered by conceptual grouping: stability → change → spatial → temporal

SIGIL_DEFINITIONS: list[SigilDefinition] = [
    SigilDefinition(
        char="ߛ",
        name="stabilization",
        description="Dispersion decreased",
        sound_description="Descending tone settling to steady hum",
        base_freq=440.0,
        duration=1.5,
    ),
    SigilDefinition(
        char="ߜ",
        name="dispersion",
        description="Spread increased",
        sound_description="Expanding stereo, rising harmonics",
        base_freq=330.0,
        duration=1.5,
    ),
    SigilDefinition(
        char="ߕ",
        name="transition",
        description="Change point",
        sound_description="Sharp frequency shift, brief silence",
        base_freq=523.0,
        duration=0.8,
    ),
    SigilDefinition(
        char="ߙ",
        name="return",
        description="Re-entry to basin",
        sound_description="Melodic resolution, home note return",
        base_freq=392.0,
        duration=1.2,
    ),
    SigilDefinition(
        char="ߡ",
        name="dwell",
        description="Sustained stay",
        sound_description="Long sustained tone, subtle warmth",
        base_freq=349.0,
        duration=2.0,
    ),
    SigilDefinition(
        char="ߚ",
        name="oscillation",
        description="Rapid alternation",
        sound_description="Tremolo, rapid frequency modulation",
        base_freq=466.0,
        duration=1.0,
    ),
    SigilDefinition(
        char="ߞ",
        name="recovery",
        description="Return latency",
        sound_description="Slow fade-in, gradual stabilization",
        base_freq=294.0,
        duration=1.8,
    ),
    SigilDefinition(
        char="ߣ",
        name="novelty",
        description="New basin",
        sound_description="Surprising interval, new timbre",
        base_freq=587.0,
        duration=1.0,
    ),
    SigilDefinition(
        char="ߠ",
        name="place_shift",
        description="Location change",
        sound_description="Spatial panning, Doppler effect",
        base_freq=415.0,
        duration=1.3,
    ),
    SigilDefinition(
        char="ߥ",
        name="echo",
        description="Pattern match",
        sound_description="Delayed repetition, reverb tail",
        base_freq=370.0,
        duration=2.0,
    ),
]


def get_definition_by_char(char: str) -> SigilDefinition | None:
    """Look up a sigil definition by its N'Ko character."""
    for defn in SIGIL_DEFINITIONS:
        if defn.char == char:
            return defn
    return None


def get_definition_by_name(name: str) -> SigilDefinition | None:
    """Look up a sigil definition by its machine name."""
    normalised = name.lower().replace("-", "_")
    for defn in SIGIL_DEFINITIONS:
        if defn.name == normalised:
            return defn
    return None
