import struct
class RLE():

    def __init__(self):
        self.iterations = 0
        self.a = bytearray(1000000000)
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
        self.iterations += 1
        rle = self.rle_encode(data)
        data = b''
        for i in range(len(rle)):
            data += struct.pack("<B", rle[i][1])
            data += rle[i][0]
        if len(data) < len(self.a):
            self.a = bytes(data)
            self.length = len(rle)
            return self.archive(data)
        else:
            ans = b''
            ans += struct.pack("<i", self.iterations-1)
            ans += struct.pack("<i", self.length)
            ans += self.a
            return ans
    def read_data(self, file):
        with open(file, "rb") as f:
            f.read(7)
            self.iterations = struct.unpack("<i", f.read(4))[0]
            data = []
            l = struct.unpack("<i", f.read(4))[0]
            for i in range(l):
                a = struct.unpack("<B", f.read(1))[0]
                data.append((f.read(1), a))
            return data

    def unarchive(self, archive_name):
        data = self.read_data(archive_name)
        data = bytes(self.rle_decode(data))
        for i in range(self.iterations-1):
            lst = []
            for i in range(0,len(data),2):
                lst.append((data[i], struct.unpack("<B", data[i+1])[0]))
            data = lst
            data = bytes(self.rle_decode(data))
        return data






