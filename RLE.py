import struct
class RLE():
    def rle_encode(self, data):
        count = 1
        prev_char = ''
        lst = []
        for char in data:
            if char != prev_char:
                if prev_char:
                    entry = (prev_char, count)
                    lst.append(entry)
                count = 1
                prev_char = char
            else:
                if count <= 255:
                    count += 1
                else:
                    entry = (prev_char, count)
                    lst.append(entry)
                    count = 1
        entry = (char, count)
        lst.append(entry)
        return lst

    def rle_decode(self, lst):
        data = ''
        for item in lst:
            char = item[0]
            count = item[1]
            data += char * count
        return data
    def text_archive(self, data, name):
        rle = self.rle_encode(data.read())
        with open(f"{name}.ultarc", "wb") as f:
            f.write(struct.pack("<i", len(rle)))
            for i in range(len(rle)):
                f.write(struct.pack("<b", rle[i][1]))
                f.write(struct.pack("<h", ord(rle[i][0])))
    def read_data(self, file):
        with open(f"{file}.ultarc", "rb") as f:
            data = []
            l = struct.unpack("<i", f.read(4))[0]
            for i in range(l):
                a = struct.unpack("<b", f.read(1))[0]
                data.append((chr(struct.unpack("<h", f.read(2))[0]), a))
            return data

    def text_unarchive(self, archive_name, output_name):
        with open(f"{output_name}.txt", "w") as f:
            f.write(self.rle_decode(self.read_data(archive_name)))






