import binascii
import heapq
import pickle
import struct
from collections import defaultdict

class Huffman():
    def huffman_encode(self, data):
        freq = defaultdict(int)
        for char in data:
            freq[char] += 1

        heap = [[weight, [char, '']] for char, weight in freq.items()]
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
        encoded_data = ''.join([huff[char] for char in data])
        return encoded_data, huff

    def read_data(self, file):
        with open(file, "rb") as f:
            a = struct.unpack("<i", f.read(4))[0]
            b = struct.unpack("<i", f.read(4))[0]
            data = f.read(a)
            my_dict = 0
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
            return (bin(int(binascii.hexlify(data), 16))[2:].zfill(len(data) * 8))[:-1 * b], huff

    def huffman_decode(self, encoded_data, huff):
        inv_huff = {v: k for k, v in huff.items()}
        decoded_data = ''
        i = 0
        while i < len(encoded_data):
            for code in inv_huff:
                if encoded_data[i:].startswith(code):
                    decoded_data += inv_huff[code]
                    i += len(code)
                    break
        return decoded_data

    def text_archive(self, data, name):
        f = open(f"{name}.ultarc", "wb")
        huff = self.huffman_encode(data.read())
        my_dict = huff[1]
        if len(huff[0]) % 8 == 0:
            length = len(huff[0]) // 8
        else:
            length = len(huff[0]) // 8 + 1
        f.write(struct.pack("<i", length))
        f.write(struct.pack("<i", 8 - len(huff[0]) % 8))
        binary_string = huff[0]
        f.write(bytes(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8)))
        pickle.dump(my_dict, f)

    def text_unarchive(self, archive_name, output_name):
        with open(f"{output_name}.txt", "w") as f:
            f.write(self.huffman_decode(self.read_data(f"{archive_name}.ultarc")[0], self.read_data(f"{archive_name}.ultarc")[1]))

