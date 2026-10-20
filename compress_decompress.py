import json
import os
from collections import Counter

from huffman_core import huffman_codes


def compress(in_path, out_path, p_min):
    data = open(in_path, "rb").read()
    total = len(data)
    counts = Counter(data)

    probs = {}
    rare = 0
    for byte, c in counts.items():
        if c / total >= p_min:
            probs[byte] = c / total
        else:
            rare += c / total
    if rare > 0:
        probs["ESC"] = rare

    codes = huffman_codes(probs) if probs else {}
    esc = codes.get("ESC")

    bits = ""
    for byte in data:
        if byte in codes:
            bits += codes[byte]
        else:
            bits += esc + format(byte, "08b")

    pad = (8 - len(bits) % 8) % 8
    bits += "0" * pad
    packed = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))

    header = {
        "total": total,
        "pad": pad,
        "esc": esc,
        "codes": {str(b): c for b, c in codes.items() if b != "ESC"},
    }
    with open(out_path, "wb") as f:
        f.write(json.dumps(header).encode() + b"\n")
        f.write(packed)

    size = os.path.getsize(out_path)
    print("Original size  :", total, "bytes")
    print("Compressed size:", size, "bytes")
    if size:
        print("Compression ratio:", round(total / size, 3))


def decompress(in_path, out_path):
    with open(in_path, "rb") as f:
        header = json.loads(f.readline().decode())
        packed = f.read()

    bits = "".join(format(b, "08b") for b in packed)
    if header["pad"]:
        bits = bits[:-header["pad"]]

    lookup = {c: int(b) for b, c in header["codes"].items()}
    esc = header["esc"]

    result = bytearray()
    code = ""
    i = 0
    while len(result) < header["total"]:
        code += bits[i]
        i += 1
        if code in lookup:
            result.append(lookup[code])
            code = ""
        elif code == esc:
            result.append(int(bits[i:i + 8], 2))
            i += 8
            code = ""

    open(out_path, "wb").write(result)
    print("Decompressed", len(result), "bytes")