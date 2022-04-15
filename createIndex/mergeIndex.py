#!/usr/bin/python3
import os, sys
import heapq                                                                    
import contextlib 

# Open a file
path = sys.argv[1]
inFiles = os.listdir( path )                                                                                


with contextlib.ExitStack() as stack:
    files = [open(os.path.join(path,fn)) for fn in inFiles]                                            
    with open(sys.argv[2], 'w') as f:
        f.writelines(heapq.merge(*files))