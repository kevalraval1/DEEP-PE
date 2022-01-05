# DEEP-PE

This algorithm parses through the received results from http://deepcrispr.info/DeepPE/ along with an inputted FASTA sequence from the user to create a sorted list of the best spacer and extension sequences to try out first in a .txt file. 

To use the program, download the results from your DEEP-PE search, then run the program with the FASTA query you put into the DEEP-PE search, along with your desired mutation. For example:

CGATGCCAAGAACATGATGGCTGCCTGTGACCCCCGCCAC(G/A)GCCGATACCTCACCGTGGCTGCTGTCTTCCGTGGTCGGAT

This sequence will be used to search the DEEP-PE results and the mutation will be a G to A in the extension, with the A being lowercase. 