"""Generate minimal valid PNG icons for URLSentinel browser extension."""

import struct
import zlib
from pathlib import Path


def create_png(width: int, height: int, rgba_color: tuple) -> bytes:
    """Create a minimal RGBA PNG with given dimensions and color."""
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # filter type None
        for x in range(width):
            # Draw a shield-like bordered square with the accent color
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                # Border (indigo)
                raw_data.extend([99, 102, 241, 255])
            elif width // 4 <= x <= 3 * width // 4 and height // 4 <= y <= 3 * height // 4:
                # Center accent (emerald)
                raw_data.extend([16, 185, 129, 255])
            else:
                # Background (dark slate)
                raw_data.extend([15, 17, 23, 255])

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(bytes(raw_data)))
    iend = chunk(b"IEND", b"")

    return header + ihdr + idat + iend


def main():
    out_dir = Path("z:/URLSentinel/apps/extension/icons")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for size in (16, 48, 128):
        png_bytes = create_png(size, size, (99, 102, 241, 255))
        file_path = out_dir / f"icon-{size}.png"
        file_path.write_bytes(png_bytes)
        print(f"Generated: {file_path}")


if __name__ == "__main__":
    main()

