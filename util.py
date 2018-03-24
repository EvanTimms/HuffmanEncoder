# The functions in this file are to be implemented by students.

import bitio
import huffman


def read_tree(bitreader):
    '''Read a description of a Huffman tree from the given bit reader,
    and construct and return the tree. When this function returns, the
    bit reader should be ready to read the next bit immediately
    following the tree description.

    Huffman trees are stored in the following format:
      * TreeLeaf is represented by the two bits 01, followed by 8 bits
          for the symbol at that leaf.
      * TreeLeaf that is None (the special "end of message" character) 
          is represented by the two bits 00.
      * TreeBranch is represented by the single bit 1, followed by a
          description of the left subtree and then the right subtree.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.

    Returns:
      A Huffman tree constructed according to the given description.
      

    implementation: read each bit, and sort depending on what value it makes up
    '''     
    #pass the input of the bitreader(the opened file) and construct
    #the frequency table from the stream
    table = huffman.make_freq_table(bitreader.input)

    return huffman.make_tree(table)
        

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.
    
    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.

    Starting from the root, traverse the Huffman tree. Each bit from
    the input sequence tells you when to go left or right.
    """
    
    bit = bitreader.readbit()
    
    if bit == 1:
        #traverse left
        tree = tree[tree._lchild]
        return decode_byte(tree, bitreader)
    elif bit == 0:
        #traverse right
        tree = tree[tree._rchild]
        return decode_byte(tree, bitreader)
    elif isInstance(tree, huffman.TreeLeaf()):
        return tree[0][0].value
    


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.

    '''
    reader = bitio.BitReader(compressed)
    writer = bitio.BitWriter(uncompressed)

    tree = read_tree(reader)

    while(True):
        try:
            byte = decode_byte(tree, reader)
            writer.writebits(byte,8)
        except EOFError:
            break

    
    


def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    pass    


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    pass


