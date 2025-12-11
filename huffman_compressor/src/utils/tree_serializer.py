from ..compression.huffman_tree import HuffmanNode


def serialize_tree(root: HuffmanNode) -> bytes:
    data = bytearray()

    def dfs(node):
        if node.char is not None:
            data.append(1)
            data.append(ord(node.char))
        else:
            data.append(0)
            dfs(node.left)
            dfs(node.right)

    dfs(root)
    return bytes(data)


def deserialize_tree(data: bytes) -> HuffmanNode:
    index = 0

    def dfs():
        nonlocal index
        flag = data[index]
        index += 1

        if flag == 1:  # leaf
            ch = chr(data[index])
            index += 1
            return HuffmanNode(ch, 0)

        # internal
        left = dfs()
        right = dfs()
        return HuffmanNode(None, 0, left, right)

    return dfs()
