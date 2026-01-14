# Huffman Text Compression Tool

A Python-based application that implements **lossless text compression and decompression** using **Huffman Coding**, with an optimized **canonical Huffman encoding strategy**, bit-level stream handling, and a graphical user interface for compression, decompression, and tree visualization.

---

## Overview

This project implements a **Huffman-based compression system** designed to explore practical considerations in real-world lossless compression, including **metadata overhead**, **bit-level encoding**, and **deterministic decoding**.

While the application exposes a single compression workflow to the user, the underlying implementation leverages **canonical Huffman coding** to optimize storage efficiency and decoding reliability.

---

## Key Concepts

- Huffman Coding  
- Canonical Huffman Codes  
- Prefix-free encoding  
- Bit-level compression and padding  
- Deterministic code reconstruction  
- Lossless text compression  

---

## Architecture

The system is structured into independent modules for compression, decoding, bitstream handling, visualization, and user interaction:
```
src/
│
├── compression/
│ ├── huffman_tree.py # Frequency analysis and tree construction
│ ├── canonical_encoder.py # Canonical Huffman encoder
│ ├── canonical_decoder.py # Canonical Huffman decoder
│ ├── bitstream.py # Bit-level I/O and padding handling
│
├── utils/
│ ├── tree_serializer.py # Tree serialization (used for visualization)
│
├── visualization/
│ ├── tree_visualizer.py # Huffman tree rendering
│
├── gui/
│ ├── home_page.py
│ ├── compress_page.py
│ ├── decompress_page.py
│ ├── visualizer_page.py
│
├── main_app.py # Application entry point
```

---

## Dependencies

This project uses external Python packages. All required dependencies are listed in `requirements.txt`.

Install dependencies using:
```
pip install -r requirements.txt
```

---

## Compression Strategy

The application uses **canonical Huffman coding** as its primary compression mechanism.

### Encoding Process

1. Build a Huffman tree from symbol frequencies  
2. Extract code lengths from the tree  
3. Generate canonical Huffman codes deterministically  
4. Encode the input text into a bitstream  
5. Store only `(symbol, code length)` metadata in the file header  
6. Append the compressed bitstream with padding information  

### Decoding Process

1. Read symbol–length pairs from the file header  
2. Reconstruct canonical Huffman codes deterministically  
3. Decode the bitstream bit-by-bit using prefix matching  
4. Restore the original input exactly  

The Huffman tree itself is **not stored in the compressed file** and is used only internally for code-length derivation and visualization.

---

## File Format
```
[Symbol Count (1 byte)]
[Symbol][Code Length] × N
[Padding Info + Compressed Bitstream]
```

This format minimizes metadata size while ensuring deterministic decoding.

---

## Bitstream Handling

- Encoded symbols are written as variable-length bit sequences  
- Padding is added to ensure byte alignment  
- Padding size is stored to allow safe removal during decoding  

This guarantees correctness regardless of input size.

---

## Time Complexity

| Stage | Complexity |
|------|-----------|
| Frequency Analysis | O(n) |
| Huffman Tree Construction | O(k log k) |
| Encoding / Decoding | O(n) |

Where:
- `n` = number of characters in the input  
- `k` = number of unique symbols  

Overall complexity: **O(n + k log k)**

---

## Compression Characteristics

- Compression efficiency improves as input size increases  
- Small files may show limited compression due to fixed metadata overhead  
- Observed behavior aligns with entropy-based compression theory  

---

## User Interface

The graphical interface provides:

- File selection for compression and decompression  
- Display of compression statistics  
- Huffman tree visualization  
- Multithreaded execution to maintain responsiveness  

The UI focuses on usability and correctness rather than algorithm comparison.

---

## Limitations

- Designed for text-based files  
- No runtime toggle between standard and canonical Huffman modes  
- Binary file compression is not currently supported  

---

## Future Enhancements

- Binary file support  
- Hybrid compression (e.g., dictionary-based preprocessing)  
- Adaptive Huffman coding  
- Error detection and integrity checks  
- Performance optimizations for large inputs  

---

## Summary

This project delivers a clean, modular implementation of **canonical Huffman compression**, emphasizing correctness, determinism, and practical file-format design. It demonstrates how classical algorithms are adapted for efficient real-world usage while maintaining a simple and accessible user interface.
