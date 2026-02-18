"""Command-line interface for Sound Sigils.

Usage::

    sound-sigils list
    sound-sigils info ߛ
    sound-sigils play ߛ
    sound-sigils play stabilization
    sound-sigils sequence "ߛ ߕ ߙ"
    sound-sigils export ߛ -o out.wav
    sound-sigils export-all -o audio/
    sound-sigils waveform ߛ
"""

from __future__ import annotations

import argparse
import sys

from sound_sigils import __version__
from sound_sigils.engine import SoundSigils


def _waveform_ascii(sigil_key: str, ss: SoundSigils, width: int = 60) -> str:
    """Render a mini ASCII waveform of a sigil.

    Shows a simplified amplitude envelope using block characters.
    """
    from sound_sigils.audio import render_samples

    sigil = ss._require(sigil_key)
    samples = render_samples(sigil)

    if not samples:
        return "(empty)"

    # Downsample to `width` buckets
    bucket_size = max(1, len(samples) // width)
    buckets: list[float] = []
    for i in range(0, len(samples), bucket_size):
        chunk = samples[i : i + bucket_size]
        peak = max(abs(l) + abs(r) for l, r in chunk) / 2
        buckets.append(peak)

    if not buckets:
        return "(empty)"

    max_peak = max(buckets) or 1.0
    height = 8
    blocks = " ▁▂▃▄▅▆▇█"

    lines = [f"  {sigil.char} {sigil.name} — {sigil.duration}s @ {sigil.base_freq}Hz"]
    lines.append("  " + "".join(
        blocks[min(int(b / max_peak * (len(blocks) - 1)), len(blocks) - 1)]
        for b in buckets[:width]
    ))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``sound-sigils`` CLI."""
    parser = argparse.ArgumentParser(
        prog="sound-sigils",
        description="Sound Sigils — Audio representations of N'Ko sigils",
    )
    parser.add_argument(
        "--version", action="version", version=f"sound-sigils {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # list ──────────────────────────────────────────────────────────
    subparsers.add_parser("list", help="List all sigils")

    # info ──────────────────────────────────────────────────────────
    info_p = subparsers.add_parser("info", help="Show detailed info for a sigil")
    info_p.add_argument("sigil", help="Sigil character or name")

    # play ──────────────────────────────────────────────────────────
    play_p = subparsers.add_parser("play", help="Play a sigil through speakers")
    play_p.add_argument("sigil", help="Sigil character or name")

    # sequence ─────────────────────────────────────────────────────
    seq_p = subparsers.add_parser("sequence", help="Play a sequence of sigils")
    seq_p.add_argument("sigils", help="Space-separated sigil characters or names")
    seq_p.add_argument(
        "--gap", type=float, default=0.1, help="Gap between sigils in seconds"
    )

    # export ────────────────────────────────────────────────────────
    exp_p = subparsers.add_parser("export", help="Export a sigil to WAV")
    exp_p.add_argument("sigil", help="Sigil character or name")
    exp_p.add_argument("--output", "-o", required=True, help="Output file path")

    # export-all ───────────────────────────────────────────────────
    expa_p = subparsers.add_parser("export-all", help="Export all sigils to a directory")
    expa_p.add_argument("--output", "-o", required=True, help="Output directory")

    # waveform ─────────────────────────────────────────────────────
    wav_p = subparsers.add_parser("waveform", help="Show ASCII waveform of a sigil")
    wav_p.add_argument("sigil", help="Sigil character or name")
    wav_p.add_argument("--width", "-w", type=int, default=60, help="Display width")

    args = parser.parse_args(argv)
    ss = SoundSigils()

    if args.command == "list":
        print(ss.list_sigils())

    elif args.command == "info":
        try:
            print(ss.info(args.sigil))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "play":
        try:
            sigil = ss._require(args.sigil)
            print(f"🔊 Playing {sigil.char} ({sigil.name}): {sigil.description}")
            ss.play(args.sigil)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "sequence":
        keys = args.sigils.split()
        try:
            print(f"🎼 Playing sequence: {' '.join(keys)}")
            ss.play_sequence(keys, gap=args.gap)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "export":
        try:
            path = ss.export(args.sigil, args.output)
            print(f"✓ Exported to {path}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "export-all":
        paths = ss.export_all(args.output)
        for p in paths:
            print(f"✓ {p}")
        print(f"\nExported {len(paths)} sigils.")

    elif args.command == "waveform":
        try:
            print(_waveform_ascii(args.sigil, ss, width=args.width))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    else:
        parser.print_help()
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
