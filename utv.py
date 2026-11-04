"""Inspect and round-trip legacy UpdateLogic UTV containers offline."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

MAGIC = b"BDC\tCDB\tBDC\tCDB\t"
HEADER = struct.Struct("<16sBBBBIII")


def records(stream):
    """Yield record metadata and decoded header fields."""
    offset = 0
    end = stream.seek(0, 2)
    stream.seek(0)
    if not end:
        raise ValueError("Empty input")
    while offset < end:
        header = stream.read(HEADER.size)
        if len(header) != HEADER.size:
            raise ValueError(f"Truncated header at offset {offset}")
        fields = HEADER.unpack(header)
        magic, clear, key, kind, reserved, vendor, group, size = fields
        if magic != MAGIC:
            raise ValueError(f"Unrecognized legacy UTV magic at offset {offset}")
        if not HEADER.size <= size <= end - offset:
            raise ValueError(f"Invalid record size at offset {offset}: {size}")
        yield {
            "offset": offset, "size": size, "clear_version": clear,
            "key_version": key, "key_type": kind, "reserved": reserved,
            "vendor_id": f"0x{vendor:06x}", "model_group": f"0x{group:04x}",
        }, fields
        offset += size
        stream.seek(offset)


def inspect(path, verify_roundtrip=False):
    digest = hashlib.sha256()
    rebuilt = hashlib.sha256()
    rows = []
    with path.open("rb") as stream:
        for row, fields in records(stream):
            rows.append(row)
            stream.seek(row["offset"])
            original_header = stream.read(HEADER.size)
            digest.update(original_header)
            if verify_roundtrip:
                rebuilt.update(HEADER.pack(*fields))
            remaining = row["size"] - HEADER.size
            while remaining:
                data = stream.read(min(remaining, 1024 * 1024))
                if not data:
                    raise ValueError("Unexpected end of record")
                digest.update(data)
                if verify_roundtrip:
                    rebuilt.update(data)
                remaining -= len(data)
    result = {
        "format": "legacy-updatelogic-utv", "sha256": digest.hexdigest(),
        "record_count": len(rows), "records": rows,
    }
    if verify_roundtrip:
        result["reserialized_sha256"] = rebuilt.hexdigest()
        result["roundtrip_sha256_match"] = digest.digest() == rebuilt.digest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--verify-roundtrip", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.image, args.verify_roundtrip), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
