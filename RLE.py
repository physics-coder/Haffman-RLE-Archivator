import struct
class RLE():

    def __init__(self):
        self.iterations = 0
        self.a = bytes(1000000000)
        self.length = 0
    def rle_encode(self, data):
        data = bytearray(data)
        count = 1
        prev_byte = b''
        lst = []
        for byte in data:
            byte = bytes([byte])
            if byte != prev_byte:
                if prev_byte:
                    entry = (prev_byte, count)
                    lst.append(entry)
                count = 1
                prev_byte = byte
            else:
                if count < 255:
                    count += 1
                else:
                    entry = (prev_byte, count)
                    lst.append(entry)
                    count = 1
        entry = (byte, count)
        lst.append(entry)
        return lst

    def rle_decode(self, lst):
        data = b''
        for item in lst:
            char = item[0]
            count = item[1]
            data += char * count
        return data

    def archive(self, data):
        length = len(data)
        self.iterations += 1
        rle = self.rle_encode(data)
        data = b''
        if length > len(rle)*2:
            for i in range(len(rle)):
                data += struct.pack("<B", rle[i][1])
                data += rle[i][0]
            ans = b''
            ans += struct.pack("<i", len(rle))
            ans += data
            return ans
        else:
            return bytes(1000000000)
    def read_data(self, file):
        with open(file, "rb") as f:
            f.read(7)
            data = []
            l = struct.unpack("<i", f.read(4))[0]
            for i in range(l):
                a = struct.unpack("<B", f.read(1))[0]
                data.append((f.read(1), a))
            return data

    def unarchive(self, archive_name):
        data = self.read_data(archive_name)
        data = bytes(self.rle_decode(data))
        return data






