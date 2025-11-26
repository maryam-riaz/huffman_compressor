import networkx as nx
import matplotlib.pyplot as plt
from ..compression.huffman_tree import HuffmanNode
from PIL import Image
import io


def _build_graph(root):
    G = nx.DiGraph()
    counter = [0]  # ensures unique node IDs

    def walk(node):
        node_id = counter[0]
        counter[0] += 1

        # label includes character (if any)
        if node.char is None:
            label = f"•"
        else:
            ch = node.char
            if ch == " ":
                ch = "␣"
            if ch == "\n":
                ch = "\\n"
            label = f"'{ch}'"

        G.add_node(node_id, label=label)

        if node.left:
            left_id = walk(node.left)
            G.add_edge(node_id, left_id, label="0")

        if node.right:
            right_id = walk(node.right)
            G.add_edge(node_id, right_id, label="1")

        return node_id

    walk(root)
    return G


def _hierarchy_positions(G, root):
    """Return a layout dictionary for a tree."""
    def dfs(n, x=0, y=0, layer=1):
        pos[n] = (x, -y)
        children = list(G.successors(n))
        if len(children) == 0:
            return 1

        width = 0
        child_positions = []
        for c in children:
            w = dfs(c, x + width, y + 1, layer + 1)
            child_positions.append((c, w))
            width += w

        # center parent relative to children
        mid = (pos[child_positions[0][0]][0] + pos[child_positions[-1][0]][0]) / 2
        pos[n] = (mid, -y)

        return width

    pos = {}
    dfs(root)
    return pos


def visualize_tree(root: HuffmanNode, output_path: str):
    G = _build_graph(root)

    # find root (node whose indegree=0)
    roots = [n for n, d in G.in_degree() if d == 0]
    root_id = roots[0]

    pos = _hierarchy_positions(G, root_id)

    labels = nx.get_node_attributes(G, "label")
    edge_labels = nx.get_edge_attributes(G, "label")

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, arrows=False, node_size=1800)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(output_path, format="png", dpi=200)
    plt.close()

    return output_path
