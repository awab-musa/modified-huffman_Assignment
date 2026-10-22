import os

FOLDER = os.path.dirname(os.path.abspath(__file__))


def in_folder(name):
    return os.path.join(FOLDER, name)


# Count how many times each byte appears
def count_symbols(data):
    counts = {}
    for byte in data:
        if byte in counts:
            counts[byte] = counts[byte] + 1
        else:
            counts[byte] = 1
    return counts


def find_smallest(groups):
    smallest = 0
    for i in range(len(groups)):
        if groups[i][0] < groups[smallest][0]:
            smallest = i
    return smallest


# Build Huffman codes: always merge the two smallest groups
def build_huffman_codes(probs):
    codes = {}
    groups = []
    for symbol in probs:
        codes[symbol] = ""
        groups.append([probs[symbol], [symbol]])

    if len(groups) == 1:
        codes[groups[0][1][0]] = "0"
        return codes

    while len(groups) > 1:
        group1 = groups.pop(find_smallest(groups))
        group2 = groups.pop(find_smallest(groups))
        for symbol in group1[1]:
            codes[symbol] = "0" + codes[symbol]
        for symbol in group2[1]:
            codes[symbol] = "1" + codes[symbol]
        groups.append([group1[0] + group2[0], group1[1] + group2[1]])

    return codes


def to_8_bits(number):
    return format(number, "08b")


# Compression: symbols with probability <= p_min are grouped into "Others"
def compress(in_path, out_path, p_min):
    file = open(in_path, "rb")
    data = file.read()
    file.close()

    total = len(data)
    counts = count_symbols(data)

    probs = {}
    others_prob = 0
    for byte in counts:
        p = counts[byte] / total
        if p > p_min:
            probs[byte] = p
        else:
            others_prob = others_prob + p
    if others_prob > 0:
        probs["Others"] = others_prob

    codes = {}
    if len(probs) > 0:
        codes = build_huffman_codes(probs)

    bits = ""
    for byte in data:
        if byte in codes:
            bits = bits + codes[byte]
        else:
            bits = bits + codes["Others"] + to_8_bits(byte)

    pad = 0
    while len(bits) % 8 != 0:
        bits = bits + "0"
        pad = pad + 1

    packed = bytearray()
    for i in range(0, len(bits), 8):
        packed.append(int(bits[i:i + 8], 2))

    file = open(out_path, "wb")
    file.write((str(total) + "\n").encode())
    file.write((str(pad) + "\n").encode())
    file.write((str(len(codes)) + "\n").encode())
    for symbol in codes:
        file.write((str(symbol) + " " + codes[symbol] + "\n").encode())
    file.write(packed)
    file.close()


# Decompression: read bit by bit until the buffer matches a code
def decompress(in_path, out_path):
    file = open(in_path, "rb")
    total = int(file.readline().decode())
    pad = int(file.readline().decode())
    count = int(file.readline().decode())

    lookup = {}
    others_code = "none"
    for i in range(count):
        line = file.readline().decode().split()
        if line[0] == "Others":
            others_code = line[1]
        else:
            lookup[line[1]] = int(line[0])

    packed = file.read()
    file.close()

    bits = ""
    for byte in packed:
        bits = bits + to_8_bits(byte)
    if pad > 0:
        bits = bits[:-pad]

    result = bytearray()
    buffer = ""
    i = 0
    while len(result) < total:
        buffer = buffer + bits[i]
        i = i + 1
        if buffer in lookup:
            result.append(lookup[buffer])
            buffer = ""
        elif buffer == others_code:
            result.append(int(bits[i:i + 8], 2))
            i = i + 8
            buffer = ""

    file = open(out_path, "wb")
    file.write(result)
    file.close()


def main():
    while True:
        choice = input("1) Compress  2) Decompress  3) Exit: ")
        if choice == "1":
            name = input("File name: ")
            p_min = float(input("Minimum probability: "))
            compress(in_folder(name), in_folder("comp.txt"), p_min)
            print("Done: comp.txt")
        elif choice == "2":
            decompress(in_folder("comp.txt"), in_folder("decomp.txt"))
            print("Done: decomp.txt")
        elif choice == "3":
            break


if __name__ == "__main__":
    main()
