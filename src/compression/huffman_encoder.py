import os
from .huffman_tree import build_frequency_table, build_huffman_tree, generate_codes
from .bitstream import BitStreamWriter
from ..utils.tree_serializer import serialize_tree


def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    freq = build_frequency_table(text)
    root = build_huffman_tree(freq)
    codes = generate_codes(root)

    # Write compressed bits
    writer = BitStreamWriter()
    for ch in text:
        writer.write_bits(codes[ch])

    compressed_bits = writer.to_bytes()

    # Serialize tree
    tree_bytes = serialize_tree(root)
    tree_size = len(tree_bytes)

    with open(output_path, "wb") as f:
        f.write(tree_size.to_bytes(4, "big"))
        f.write(tree_bytes)
        f.write(compressed_bits)

    return {
        "original_size": os.path.getsize(input_path),
        "compressed_size": os.path.getsize(output_path),
        "compression_ratio": round(os.path.getsize(input_path) / os.path.getsize(output_path), 3)
    }, root
