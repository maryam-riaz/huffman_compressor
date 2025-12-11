class BitStreamWriter:
    def __init__(self):
        self.bits = ""

    def write_bits(self, bitstring: str):
        self.bits += bitstring

    def to_bytes(self) -> bytes:
        padding = 8 - (len(self.bits) % 8)
        if padding == 8:
            padding = 0

        self.bits += "0" * padding

        byte_arr = bytearray()
        for i in range(0, len(self.bits), 8):
            byte_arr.append(int(self.bits[i:i+8], 2))

        return bytes([padding]) + bytes(byte_arr)


class BitStreamReader:
    def __init__(self, data: bytes):
        self.padding = data[0]
        bits = ""

        for byte in data[1:]:
            bits += f"{byte:08b}"

        if self.padding > 0:
            self.bits = bits[:-self.padding]
        else:
            self.bits = bits

    def read_bits(self):
        return self.bits
