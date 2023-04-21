import binascii
import heapq
import pickle
import struct
from collections import defaultdict

class Huffman():
    def huffman_encode(self, data):
        freq = defaultdict(int)
        for byte in data:
            freq[byte] += 1

        heap = [[weight, [byte, '']] for byte, weight in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        huff = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))
        encoded_data = ''.join([huff[byte] for byte in data])
        return encoded_data, huff

    def read_data(self, file):
        with open(file, "rb") as f:
            f.read(7)
            a = struct.unpack("<i", f.read(4))[0]
            length = struct.unpack("<i", f.read(4))[0]
            binary_data_read = f.read(length)
            binary_data_read = ''.join(format(byte, '08b') for byte in binary_data_read)
            if a != 0:
                binary_data_read = binary_data_read[0:-8] + binary_data_read[-1 * a::]
            else:
                binary_data_read = binary_data_read
            while True:
                try:
                    chunk = pickle.load(f)

                    # Check if the chunk is a dictionary
                    if isinstance(chunk, dict):
                        # Use the dictionary found
                        my_dict = chunk
                        break
                except EOFError:
                    # End of file reached, no dictionary found
                    break
            huff = my_dict
            return binary_data_read, huff

    def huffman_decode(self, encoded_data, huff):
        inv_huff = {v: k for k, v in huff.items()}
        decoded_data = b''
        i = 0
        while i < len(encoded_data):
            for code in inv_huff:
                if encoded_data[i:].startswith(code):
                    decoded_data += bytes([inv_huff[code]])
                    i += len(code)
                    break
        return decoded_data

    def archive(self, data):
        huff = self.huffman_encode(data)
        my_dict = huff[1]
        binary_string = huff[0]
        binary_data = bytes([int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8)])
        a = len(binary_string) % 8
        data = b''
        data += struct.pack("<i", a)
        data += struct.pack("<i", len(binary_data))
        data += binary_data
        data += pickle.dumps(my_dict)
        return data

    def unarchive(self, archive_name):
        data = self.read_data(f"{archive_name}.ultarc")
        return self.huffman_decode(data[0], data[1])

