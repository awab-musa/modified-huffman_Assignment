# Modified Huffman Coding

Compression and decompression of any file using **Modified Huffman coding**, written in Python.
Information Theory and Data Compression, Assignment 2.

## How it works

Standard Huffman gives every symbol its own code, so very rare symbols get very long codes.
Modified Huffman uses a minimum probability `p_min`:

- Symbols with probability **>= p_min** get their own Huffman code.
- Symbols with probability **< p_min** are merged into one **ESC** (escape) symbol.
- A rare symbol is written as **ESC code + its 8-bit raw value**.

The 0s and 1s are packed into real bits (8 per byte), not stored as text.

## Compressed file format

1. One JSON line (the header): original size, padding bits, ESC code, code table.
2. The packed bit stream.

## Project structure

| File | Purpose |
|---|---|
| `huffman_core.py` | Builds the Huffman codes |
| `compress_decompress.py` | `compress` and `decompress` functions |
| `main.py` | Menu: run this file |

## Requirements

- Python 3.8 or newer
- No external libraries

## Usage

```
python main.py
```

**Compress**
```
Choose (1/2): 1
Input file: test.txt
Output file: test.huf
Minimum probability p_min (e.g. 0.01): 0.01
```

**Decompress**
```
Choose (1/2): 2
Compressed file: test.huf
Output file: test_out.txt
```

## Example output

```
Original size  : 1704 bytes
Compressed size: 902 bytes
Compression ratio: 1.889
```

## Choosing p_min

| p_min | Effect |
|---|---|
| `0` | Standard Huffman (no ESC) |
| `0.001` to `0.01` | Good for most files |
| `0.1` or higher | Too many symbols go to ESC, so the file may get bigger |

Very small files can come out larger because of the header size.

## Team

- [Name 1] ([ID1])
- [Name 2] ([ID2])
- [Name 3] ([ID3])
