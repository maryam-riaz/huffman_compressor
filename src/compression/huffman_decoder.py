from ..utils.tree_serializer import deserialize_tree
from .bitstream import BitStreamReader


def decompress_file(input_path, output_path):
    with open(input_path, "rb") as f:
        tree_size = int.from_bytes(f.read(4), "big")
        tree_data = f.read(tree_size)
        bitstream = f.read()

    root = deserialize_tree(tree_data)

    reader = BitStreamReader(bitstream)
    bits = reader.read_bits()

    node = root
    result = []

    for b in bits:
        node = node.left if b == "0" else node.right
        if node.char is not None:
            result.append(node.char)
            node = root

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(result))

    return True
