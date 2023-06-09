import pickle
import struct

# Node tree for the Huffman algorithm


class Nodes:
    def __init__(self, probability, symbol, left=None, right=None):
        # probability of the symbol
        self.probability = probability

        # the symbol
        self.symbol = symbol

        # the left node
        self.left = left

        # the right node
        self.right = right

        # the tree direction (0 or 1)
        self.code = ''


# A supporting function in order to calculate the probabilities of symbols
# in specified data
def CalculateProbability(the_data):
    the_symbols = dict()
    for item in the_data:
        if the_symbols.get(item) is None:
            the_symbols[item] = 1
        else:
            the_symbols[item] += 1
    return the_symbols


# A supporting function in order to print the codes of symbols by
# travelling a Huffman Tree
the_codes = dict()


def CalculateCodes(node, value=''):
    # a huffman code for current node
    newValue = value + str(node.code)

    if (node.left):
        CalculateCodes(node.left, newValue)
    if (node.right):
        CalculateCodes(node.right, newValue)

    if (not node.left and not node.right):
        the_codes[node.symbol] = newValue

    return the_codes


# A supporting function in order to get the encoded result
def OutputEncoded(the_data, coding):
    encodingOutput = []
    for element in the_data:
        encodingOutput.append(coding[element])

    the_string = ''.join([str(item) for item in encodingOutput])
    return the_string


# A supporting function in order to calculate the space difference between
# compressed and non-compressed data


def TotalGain(the_data, coding):
    # total bit space to store the data before compression
    beforeCompression = len(the_data) * 8
    afterCompression = 0
    the_symbols = coding.keys()
    for symbol in the_symbols:
        the_count = the_data.count(symbol)
        # calculating how many bit is required for that symbol in total
        afterCompression += the_count * len(coding[symbol])

# Function for encoding data using the Huffman algorithm that returns a
# node tree and the encoded output


def HuffmanEncoding(the_data):
    symbolWithProbs = CalculateProbability(the_data)
    the_symbols = symbolWithProbs.keys()
    the_probabilities = symbolWithProbs.values()
    the_nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for symbol in the_symbols:
        the_nodes.append(Nodes(symbolWithProbs.get(symbol), symbol))

    while len(the_nodes) > 1:
        # sorting all the nodes in ascending order based on their probability
        the_nodes = sorted(the_nodes, key=lambda x: x.probability)
        # for node in nodes:
        #      print(node.symbol, node.prob)

        # picking two smallest nodes
        right = the_nodes[0]
        left = the_nodes[1]

        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create new node
        newNode = Nodes(
            left.probability +
            right.probability,
            left.symbol +
            right.symbol,
            left,
            right)

        the_nodes.remove(left)
        the_nodes.remove(right)
        the_nodes.append(newNode)

    huffmanEncoding = CalculateCodes(the_nodes[0])
    TotalGain(the_data, huffmanEncoding)
    encodedOutput = OutputEncoded(the_data, huffmanEncoding)
    return encodedOutput, the_nodes[0]

# Function for decoding encoded data using the Huffman node tree


def HuffmanDecoding(encodedData, huffmanTree):
    treeHead = huffmanTree
    decodedOutput = []
    for x in encodedData:
        if x == '1':
            huffmanTree = huffmanTree.right
        elif x == '0':
            huffmanTree = huffmanTree.left
        try:
            if huffmanTree.left.symbol is None and huffmanTree.right.symbol is None:
                pass
        except AttributeError:
            decodedOutput.append(huffmanTree.symbol)
            huffmanTree = treeHead
    bytess = bytes()
    for i in decodedOutput:
        bytess += bytes([i])

    return bytess


# Class for Huffman file archivation
class Huffman():
    # Function for reading data from a Huffman archive
    def read_data(self, file):
        with open(file, "rb") as f:
            f.read(7)
            a = struct.unpack("<l", f.read(4))[0]
            length = struct.unpack("<l", f.read(4))[0]
            binary_data_read = f.read(length)
            binary_data_read = ''.join(format(byte, '08b')
                                       for byte in binary_data_read)
            if a != 0:
                binary_data_read = binary_data_read[0:-
                                                    8] + binary_data_read[-1 * a::]
            else:
                binary_data_read = binary_data_read
            while True:
                try:
                    chunk = pickle.load(f)

                    # Check if the chunk is a dictionary
                    if isinstance(chunk, Nodes):
                        # Use the dictionary found
                        my_tree = chunk
                        break
                except EOFError:
                    # End of file reached, no dictionary found
                    break
            huff = my_tree
            return binary_data_read, huff
    # Function for archiving files using the Huffman algorithm

    def archive(self, data):
        encoding, the_tree = HuffmanEncoding(data)
        binary_string = encoding
        binary_data = bytes([int(binary_string[i:i + 8], 2)
                            for i in range(0, len(binary_string), 8)])
        a = len(binary_string) % 8
        data = b''
        data += struct.pack("<l", a)
        data += struct.pack("<l", len(binary_data))
        data += binary_data
        data += pickle.dumps(the_tree)
        return data
    # Function for unarchiving Huffman archives

    def unarchive(self, archive_name):
        data = self.read_data(archive_name)
        return HuffmanDecoding(data[0], data[1])
