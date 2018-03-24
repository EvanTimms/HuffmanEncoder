
import bitio
import huffman
import util

with open('message.txt', mode='rb') as file:
    reader = bitio.BitReader(file)
    tree = util.read_tree(reader)