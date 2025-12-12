import os
from .huffman_tree import build_frequency_table, build_huffman_tree, generate_codes
from .bitstream import BitStreamWriter


def get_code_lengths(code_map):
    """Return {char: length_of_code} dictionary."""
    return {ch: len(code) for ch, code in code_map.items()}


def canonical_from_lengths(length_map):
    """
    Build canonical Huffman codes from {char: length}.
    Returns {char: canonical_code_as_string}.
    """
    # Sort by (length, lexicographically)
    symbols = sorted(length_map.items(), key=lambda x: (x[1], x[0]))

    canonical_codes = {}
    current_code = 0
    current_len = symbols[0][1]

    for ch, length in symbols:
        if length > current_len:
            # Shift left when code length increases
            current_code <<= (length - current_len)
            current_len = length

        canonical_codes[ch] = format(current_code, f'0{length}b')
        current_code += 1

    return canonical_codes


def compress_file(input_path, output_path):
    """Canonical Huffman compression."""

    # Read text
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Build tree + normal Huffman codes
    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    raw_codes = generate_codes(root)

    # Convert to canonical version
    length_map = get_code_lengths(raw_codes)
    canonical_codes = canonical_from_lengths(length_map)

    # Write compressed bitstream
    writer = BitStreamWriter()
    for ch in text:
        writer.write_bits(canonical_codes[ch])

    bitstream_bytes = writer.to_bytes()

    # ---- WRITE HEADER ----
    with open(output_path, "wb") as f:
        # Number of symbols (1 byte)
        f.write(bytes([len(length_map)]))

        # Write (char, length) pairs
        for ch, length in length_map.items():
            f.write(bytes([ord(ch), length]))

        # Write compressed data
        f.write(bitstream_bytes)

    stats = {
        "original_size": os.path.getsize(input_path),
        "compressed_size": os.path.getsize(output_path),
        "compression_ratio": round(os.path.getsize(output_path) / os.path.getsize(input_path), 3)
    }

    return stats, root  # keep root for visualization
