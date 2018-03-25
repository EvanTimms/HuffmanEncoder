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
    #recursive function that constructs the tree by reading in bytes
    def construct_tree(bitreader):
        bit = bitreader.readbit()
        if bit == 1:
            #need a branch, construct a new one and its branchs
            new_branch = huffman.TreeBranch(None,None)
            new_branch.left = construct_tree(bitreader)
            new_branch.right = construct_tree(bitreader)
            return new_branch
        elif bit == 0:
            bit2 = bitreader.readbit()
            if bit2 == 0:
                #eof file character
                return huffman.TreeLeaf(None)
            else:
                #return the value of the next 8 bits corresponding to the leaf
                val = bitreader.readbits(8)
                return huffman.TreeLeaf(val)
        
    #initalize tree branch    
    tree = huffman.TreeBranch(None,None)
    #since the first bit is always one, we can ignore it since the first branch
    #has already been constructed.
    bitreader.readbit()
    #contruct the left and right portions of the tree respectivlty.
    tree.left = construct_tree(bitreader)
    tree.right = construct_tree(bitreader)

    return tree



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
    if isinstance(tree, huffman.TreeBranch):
        #if the node is a branch, read the next bit and traverse left or right
        bit = bitreader.readbit()
        if bit == 0:
            #traverse left
            tree = tree.left
            return decode_byte(tree, bitreader)
        elif bit == 1:
            #traverse right
            tree = tree.right
            return decode_byte(tree, bitreader)  
    elif isinstance(tree, huffman.TreeLeaf):
        #return value of tree leaf
        return tree.value 
    


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
    #set up reader and writer 
    reader = bitio.BitReader(compressed)
    writer = bitio.BitWriter(uncompressed)
    #read in and construct tree
    tree = read_tree(reader)

    while(True):    
        byte = decode_byte(tree, reader)
        #if the byte is the eof char, break you are done
        if byte == None:
            break
        else:
            #write bits to uncompressed file
            writer.writebits(byte,8)
            


def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    if isinstance(tree, huffman.TreeLeaf):
        #check the leafs value, if its the eof(represented by none) write 00
        #else, write the chars ascii num representation 
        if tree.value == None:
            bitwriter.writebit(False)
            bitwriter.writebit(False)
        else:
            bitwriter.writebit(False)
            bitwriter.writebit(True)
            
            bitwriter.writebits(tree.value, 8)

    elif isinstance(tree, huffman.TreeBranch):
        #write a 1 representing the branch and write the left and write of the
        #branch
        bitwriter.writebit(True)
        write_tree(tree.left, bitwriter)
        write_tree(tree.right, bitwriter)


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
    #set up reader and writer 
    reader = bitio.BitReader(uncompressed)
    writer = bitio.BitWriter(compressed)

    #write tree to output file
    write_tree(tree, writer)
    #construct encoding table from tree
    encoder = huffman.make_encoding_table(tree)

    while(True):
        try:
            #read in a byte and find its bit representation using the 
            #encoding table
            byte = reader.readbits(8)
            sequence = encoder[byte]
            #write out the sequence of bits
            for bit in sequence:
                writer.writebit(bit)
        #when eof occurs, break from loop you are done writing the file
        except EOFError:
            break

