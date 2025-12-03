from .bitstream import BitStreamReader


def build_canonical_decoder(length_map):
    """
    Build canonical decoder tree from {char: length}.
    Returns dictionary: {bitstring: char}
    """
    # Sort by length, then alphabetically
    symbols = sorted(length_map.items(), key=lambda x: (x[1], x[0]))

    decoder = {}
    current_code = 0
    current_len = symbols[0][1]

    for ch, length in symbols:
        if length > current_len:
            current_code <<= (length - current_len)
            current_len = length

        bitstring = format(current_code, f'0{length}b')
        decoder[bitstring] = ch

        current_code += 1

    return decoder


def decompress_file(input_path, output_path):
    """Canonical Huffman decoder."""

    with open(input_path, "rb") as f:
        N = f.read(1)[0]  # number of symbols

        length_map = {}
        for _ in range(N):
            ch = chr(f.read(1)[0])
            length = f.read(1)[0]
            length_map[ch] = length

        bitstream = f.read()

    decoder_map = build_canonical_decoder(length_map)
    reader = BitStreamReader(bitstream)
    bits = reader.read_bits()

    # STREAM DECODING (bit-by-bit)
    decoded = []
    buffer = ""

    for b in bits:
        buffer += b
        if buffer in decoder_map:
            decoded.append(decoder_map[buffer])
            buffer = ""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(decoded))

    return True
