"""High-level API for Sound Sigils."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from typing import Sequence

from sound_sigils.audio import generate_sequence_wav, generate_wav
from sound_sigils.definitions import SIGIL_DEFINITIONS
from sound_sigils.generators import GENERATOR_REGISTRY
from sound_sigils.models import SigilDefinition, SigilSound


class SoundSigils:
    """Generate, play, and export N'Ko sigil sounds.

    Example::

        ss = SoundSigils()
        ss.play("ߛ")
        ss.export("stabilization", "out.wav")
        wav_bytes = ss.generate("ߛ")
    """

    def __init__(self) -> None:
        self._sigils: dict[str, SigilSound] = {}
        self._by_name: dict[str, SigilSound] = {}
        self._load_sigils()

    # ── Initialisation ────────────────────────────────────────────

    def _load_sigils(self) -> None:
        """Wire definitions to their generators."""
        for defn in SIGIL_DEFINITIONS:
            gen = GENERATOR_REGISTRY.get(defn.name)
            if gen is None:
                raise RuntimeError(
                    f"No generator registered for sigil {defn.name!r}"
                )
            sigil = SigilSound(definition=defn, generator=gen)
            self._sigils[defn.char] = sigil
            self._by_name[defn.name] = sigil

    # ── Lookup ────────────────────────────────────────────────────

    def lookup(self, key: str) -> SigilSound | None:
        """Look up a sigil by character or name.

        Args:
            key: N'Ko character (e.g. ``"ߛ"``) or English name
                 (e.g. ``"stabilization"``).

        Returns:
            The matching :class:`SigilSound`, or ``None``.
        """
        if key in self._sigils:
            return self._sigils[key]
        normalised = key.lower().replace("-", "_")
        return self._by_name.get(normalised)

    def _require(self, key: str) -> SigilSound:
        """Like :meth:`lookup` but raises on miss."""
        s = self.lookup(key)
        if s is None:
            raise ValueError(
                f"Unknown sigil: {key!r}. "
                f"Valid: {', '.join(self.names)}"
            )
        return s

    # ── Collection accessors ──────────────────────────────────────

    @property
    def all_sigils(self) -> list[SigilSound]:
        """All registered sigils in definition order."""
        return list(self._sigils.values())

    @property
    def chars(self) -> list[str]:
        """All sigil characters."""
        return list(self._sigils.keys())

    @property
    def names(self) -> list[str]:
        """All sigil names."""
        return list(self._by_name.keys())

    @property
    def definitions(self) -> list[SigilDefinition]:
        """All sigil definitions."""
        return [s.definition for s in self._sigils.values()]

    def __len__(self) -> int:
        return len(self._sigils)

    def __iter__(self):
        return iter(self._sigils.values())

    def __contains__(self, key: str) -> bool:
        return self.lookup(key) is not None

    # ── Generation ────────────────────────────────────────────────

    def generate(self, key: str, **kwargs) -> bytes:
        """Generate WAV data for a sigil.

        Args:
            key: Sigil character or name.
            **kwargs: Forwarded to :func:`~sound_sigils.audio.generate_wav`
                (e.g. ``duration_override``, ``freq_override``).

        Returns:
            WAV file bytes.
        """
        sigil = self._require(key)
        return generate_wav(sigil, **kwargs)

    def generate_sequence(
        self, keys: Sequence[str], *, gap: float = 0.1
    ) -> bytes:
        """Generate a WAV file containing a sequence of sigils.

        Args:
            keys: Ordered sigil characters or names.
            gap: Silence between sigils in seconds.

        Returns:
            WAV file bytes.
        """
        sigils = [self._require(k) for k in keys]
        return generate_sequence_wav(sigils, gap=gap)

    # ── Export ────────────────────────────────────────────────────

    def export(self, key: str, output_path: str, **kwargs) -> str:
        """Export a sigil to a WAV file.

        Args:
            key: Sigil character or name.
            output_path: Destination file path.
            **kwargs: Forwarded to :meth:`generate`.

        Returns:
            The absolute path written to.
        """
        wav_data = self.generate(key, **kwargs)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(wav_data)
        return os.path.abspath(output_path)

    def export_all(self, output_dir: str) -> list[str]:
        """Export all sigils to a directory.

        Args:
            output_dir: Target directory (created if needed).

        Returns:
            List of absolute paths written.
        """
        os.makedirs(output_dir, exist_ok=True)
        paths: list[str] = []
        for sigil in self._sigils.values():
            path = os.path.join(output_dir, f"{sigil.name}.wav")
            self.export(sigil.char, path)
            paths.append(os.path.abspath(path))
        return paths

    # ── Playback ──────────────────────────────────────────────────

    def play(self, key: str, *, blocking: bool = True) -> None:
        """Play a sigil through the system audio.

        Args:
            key: Sigil character or name.
            blocking: If ``True``, wait for playback to finish.
        """
        sigil = self._require(key)
        wav_data = self.generate(key)
        self._play_wav(wav_data, blocking=blocking)
        return None

    def play_sequence(
        self, keys: Sequence[str], *, gap: float = 0.1
    ) -> None:
        """Play a sequence of sigils.

        Args:
            keys: Ordered sigil characters or names.
            gap: Silence between sigils in seconds.
        """
        wav_data = self.generate_sequence(keys, gap=gap)
        self._play_wav(wav_data, blocking=True)

    @staticmethod
    def _play_wav(wav_data: bytes, *, blocking: bool = True) -> None:
        """Play WAV bytes using the platform audio player."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_data)
            temp_path = f.name

        try:
            if sys.platform == "darwin":
                cmd = ["afplay", temp_path]
            elif sys.platform.startswith("linux"):
                cmd = ["aplay", temp_path]
            elif sys.platform == "win32":
                cmd = [
                    "powershell",
                    "-c",
                    f'(New-Object Media.SoundPlayer "{temp_path}").PlaySync()',
                ]
            else:
                raise RuntimeError(f"Unsupported platform: {sys.platform}")

            if blocking:
                subprocess.run(cmd, check=True, capture_output=True)
            else:
                subprocess.Popen(
                    cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                return  # Don't delete temp file if async
        finally:
            if blocking:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

    # ── Display ───────────────────────────────────────────────────

    def list_sigils(self) -> str:
        """Return a formatted table of all sigils.

        Returns:
            Multi-line string suitable for terminal display.
        """
        lines = [
            "",
            "🎵 Sound Sigils — N'Ko Audio Signatures",
            "",
            f"{'Sigil':<6} {'Name':<15} {'Description':<25} {'Freq':<8} {'Duration'}",
            "-" * 70,
        ]
        for s in self._sigils.values():
            lines.append(
                f"{s.char:<6} {s.name:<15} {s.description:<25} "
                f"{s.base_freq:<8.0f} {s.duration}s"
            )
        lines.append("")
        return "\n".join(lines)

    def info(self, key: str) -> str:
        """Return detailed info about a single sigil.

        Args:
            key: Sigil character or name.

        Returns:
            Multi-line string with sigil details.
        """
        s = self._require(key)
        return (
            f"  Character : {s.char}\n"
            f"  Name      : {s.name}\n"
            f"  Meaning   : {s.description}\n"
            f"  Sound     : {s.sound_description}\n"
            f"  Frequency : {s.base_freq} Hz\n"
            f"  Duration  : {s.duration}s"
        )
