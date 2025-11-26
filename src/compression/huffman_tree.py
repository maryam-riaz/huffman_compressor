import heapq


class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    # Required for priority queue comparisons
    def __lt__(self, other):
        return self.freq < other.freq


def build_frequency_table(text: str) -> dict:
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq_table: dict) -> HuffmanNode:
    pq = []

    for char, freq in freq_table.items():
        heapq.heappush(pq, HuffmanNode(char, freq))

    if len(pq) == 1:
        # Edge case: text has only 1 unique character
        only_node = heapq.heappop(pq)
        return HuffmanNode(None, only_node.freq, left=only_node)

    while len(pq) > 1:
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)

        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(pq, merged)

    return heapq.heappop(pq)


def generate_codes(root: HuffmanNode) -> dict:
    codes = {}

    def traverse(node, current_code):
        if node is None:
            return

        if node.char is not None:
            codes[node.char] = current_code
            return

        traverse(node.left, current_code + "0")
        traverse(node.right, current_code + "1")

    traverse(root, "")
    return codes
