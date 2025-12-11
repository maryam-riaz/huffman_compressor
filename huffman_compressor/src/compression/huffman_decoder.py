from ..utils.tree_serializer import deserialize_tree

def decompress_file(input_path, output_path):
    with open(input_path, "rb") as f:
        tree_size = int.from_bytes(f.read(4), "big")
        tree_data = f.read(tree_size)
        compressed_data = f.read()  # remaining bytes

    # Reconstruct Huffman tree
    root = deserialize_tree(tree_data)

    # Decode bits directly
    result = bytearray()
    node = root

    for byte in compressed_data:
        for i in range(7, -1, -1):  # process bits from MSB to LSB
            bit = (byte >> i) & 1
            node = node.left if bit == 0 else node.right
            if node.char is not None:
                result.append(node.char)
                node = root

    # Write decoded bytes
    with open(output_path, "wb") as f:
        f.write(result)

    return True
