import os
from .huffman_tree import build_frequency_table, build_huffman_tree, generate_codes
from ..utils.tree_serializer import serialize_tree

def compress_file(input_path, output_path, progress_callback=None):
    """
    Compress a file using Huffman coding with optional progress updates.
    
    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to save the compressed file.
        progress_callback (callable, optional): Function accepting a float (0.0-1.0) to indicate progress.
    
    Returns:
        tuple: (dict with original_size, compressed_size, compression_ratio, Huffman tree root)
    """
    # 1️⃣ Read input file once
    with open(input_path, "rb") as f:
        data = f.read()

    # 2️⃣ Build frequency table, Huffman tree, and codes
    freq = build_frequency_table(data)
    root_node = build_huffman_tree(freq)
    codes = generate_codes(root_node)  # byte -> bitstring mapping

    # 3️⃣ Encode data using buffered bits
    bit_buffer = 0
    bit_count = 0
    output_bytes = bytearray()

    total_bytes = len(data)
    processed = 0

    for byte in data:
        code = codes[byte]  # e.g., '1010'
        for bit in code:
            bit_buffer = (bit_buffer << 1) | int(bit)
            bit_count += 1
            if bit_count == 8:
                output_bytes.append(bit_buffer)
                bit_buffer = 0
                bit_count = 0

        # Update progress
        processed += 1
        if progress_callback and processed % 1000 == 0:
            progress_callback(processed / total_bytes)  # fraction 0.0-1.0

    # Handle remaining bits
    if bit_count > 0:
        bit_buffer <<= (8 - bit_count)  # pad with zeros
        output_bytes.append(bit_buffer)

    # 4️⃣ Serialize Huffman tree
    tree_bytes = serialize_tree(root_node)
    tree_size = len(tree_bytes)

    # 5️⃣ Write output file in one go
    with open(output_path, "wb") as f:
        f.write(tree_size.to_bytes(4, "big"))
        f.write(tree_bytes)
        f.write(output_bytes)

    # Final progress update
    if progress_callback:
        progress_callback(1.0)

    return {
        "original_size": os.path.getsize(input_path),
        "compressed_size": os.path.getsize(output_path),
        "compression_ratio": round(os.path.getsize(input_path) / os.path.getsize(output_path), 3)
    }, root_node
