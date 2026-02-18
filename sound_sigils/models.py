"""Data models for Sound Sigils."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Tuple


@dataclass(frozen=True)
class SigilDefinition:
    """Static definition of a sigil's identity and audio parameters.

    Attributes:
        char: The N'Ko Unicode character (e.g. ``"ߛ"``).
        name: Machine-readable name (e.g. ``"stabilization"``).
        description: Human-readable meaning (e.g. ``"Dispersion decreased"``).
        sound_description: How the sigil *sounds* (e.g. ``"Descending tone settling to steady hum"``).
        base_freq: Base frequency in Hz.
        duration: Default duration in seconds.
    """

    char: str
    name: str
    description: str
    sound_description: str
    base_freq: float
    duration: float


@dataclass
class SigilSound:
    """Runtime-ready sigil that pairs a definition with its generator function.

    Attributes:
        definition: The static sigil definition.
        generator: ``(t, duration, freq) -> (left, right)`` sample generator.
    """

    definition: SigilDefinition
    generator: Callable[[float, float, float], Tuple[float, float]]

    # Convenience accessors ------------------------------------------------

    @property
    def char(self) -> str:
        return self.definition.char

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def description(self) -> str:
        return self.definition.description

    @property
    def sound_description(self) -> str:
        return self.definition.sound_description

    @property
    def base_freq(self) -> float:
        return self.definition.base_freq

    @property
    def duration(self) -> float:
        return self.definition.duration
