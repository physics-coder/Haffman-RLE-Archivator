import struct
class RLE():
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
                if count <= 255:
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
        a = data
        rle = self.rle_encode(a)
        data = b''
        data+=struct.pack("<i", len(rle))
        for i in range(len(rle)):
            data+=struct.pack("<b", rle[i][1])
            data+=rle[i][0]
        return data
    def read_data(self, file):
        with open(f"{file}.ultarc", "rb") as f:
            f.read(7)
            data = []
            l = struct.unpack("<i", f.read(4))[0]
            for i in range(l):
                a = struct.unpack("<b", f.read(1))[0]
                data.append((f.read(1), a))
            return data

    def unarchive(self, archive_name):
        return self.rle_decode(self.read_data(archive_name))






