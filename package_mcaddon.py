#!/usr/bin/env python3
"""Package the Hero Academy Bedrock packs as an importable .mcaddon archive."""

from pathlib import Path
from struct import pack
from zipfile import ZIP_DEFLATED, ZipFile
import zlib

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "HeroAcademy.mcaddon"
PACKS = (
    ("behavior_packs/HeroAcademy_BP", "HeroAcademy_BP", (32, 58, 105), (239, 190, 55)),
    ("resource_packs/HeroAcademy_RP", "HeroAcademy_RP", (105, 35, 65), (72, 205, 190)),
)


def png_chunk(kind, data):
    return pack(">I", len(data)) + kind + data + pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def make_icon(background, accent):
    """Create a small, dependency-free PNG badge for a pack icon."""
    size = 64
    rows = []
    center = size // 2
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            edge = min(x, y, size - 1 - x, size - 1 - y)
            diamond = abs(x - center) + abs(y - center) < 25
            border = edge < 4
            color = accent if diamond or border else background
            row.extend(color)
        rows.append(bytes(row))
    raw = b"".join(rows)
    header = pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", header) + png_chunk(b"IDAT", zlib.compress(raw, 9)) + png_chunk(b"IEND", b"")


def main():
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as archive:
        for source_name, archive_root, background, accent in PACKS:
            source = ROOT / source_name
            if not source.is_dir():
                raise FileNotFoundError(f"Required pack folder not found: {source}")
            files = sorted(path for path in source.rglob("*") if path.is_file())
            if not files:
                raise ValueError(f"Pack folder is empty: {source}")
            for path in files:
                archive.write(path, (Path(archive_root) / path.relative_to(source)).as_posix())
            archive.writestr(f"{archive_root}/pack_icon.png", make_icon(background, accent))
    print(f"Created {OUTPUT} with icons for both packs")


if __name__ == "__main__":
    main()
