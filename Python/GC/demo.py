from Encoder import *
from Decoder import *
import time
import random

def main():
    #bits=[128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
    bits=[16]
    for mlen in bits:
        Simulation(n=1, mlen=mlen, numDel=2, numChecker=1, f=1, lengthExtension=1)
        print('Ended', mlen)
        print()
def Simulation(n=1, mlen=16, numDel=1, numChecker=2, f=10, lengthExtension=0):
    """
     Decodes a large amount of sequences using GC algorithms.

    Args:
        n: Number of sequence to run GC on. If n is None, run on all possible one deletion cases of all numbers of mlen length.
        mlen: The length of each sequence.
        numDel: Number of deletions obviously.
        numPro: Number of decoding processes assisting the simulation.
        f: The frequency of priting out the result to the command line.

    Returns:
        The total elapsed time of the simulation.

    Raises:
        None
    """
    def sequential():
        de=Decoder(mlen, numDel, numChecker, lengthExtension)

        ttime = 0
        count=0
        for num in orange:
            for dels in irange:
                orgdata= Encoder.genMsg(num,mlen) # converts the integer num to its binary string representation.
                deldata=Encoder.pop(orgdata,dels) # pop one or more bits out to create a deleted sequence.
                parity=en.paritize(orgdata) # Compute the parity integers in based on the original sequence (encoder's end).
                print(parity)
                t1=time.time()
                r = de.decode(deldata, parity)
                ttime+=(time.time()-t1)
                record(orgdata, r, True)
                count+=1
        print('Average time: ',ttime/count*1000,'ms')
        print('Failure rate:',(stat['f']+stat['u'])/count*100,'%')
    def getRanges():
        """
        Generates sequences and deletions to run the simulation on.

        Args:
            n: Number of sequence to run GC on. If n is None, run on all possible one deletion cases of all numbers of mlen length.
            mlen: The length of each sequence.
            numDel: Number of deletions obviously.
            numPro: Number of decoding processes assisting the simulation.
            f: The frequency of priting out the result to the command line.

        Returns:
            Return 2 ranges/generators:
            orange: a collection of integers representing original sequences to decode.
            irange: the indeces of the deletions on the original sequences.

        Raises:
            None
        """
        if n != None:#random
            def genO():
                for _ in range(n):
                    yield random.randrange(2**mlen)
            def genI():
                for _ in range(n):
                    yield random.sample(range(mlen), numDel)
            orange=genO()
            irange = genI()
        else:
            orange=range(2**mlen)
            irange=range(mlen)
        return orange, irange
    def record(org, rec, valid):
        if valid:
            if rec==None:
                r='f'
            elif org==rec:
                r='s'
            else:
                r='u'
                #print('org',org)
                #print('rec',rec)
            stat[r]+=1
        else:
            r='f'
        if (sum(stat.values()))%f == 0: #display the results every f sequences.
            print(stat)
    print('Testing with', 'n=', n, ' mlen=', mlen, ' numDel=', numDel,' f=', f, ' lengthExtension=', lengthExtension)
    stat = {'s':0, 'f':0, 'u':0} #number of success, failure and unknown decoding.
    en=Encoder(mlen, numDel + numChecker, lengthExtension)
    orange, irange = getRanges() # get sequences and indices of deletions to run the simulation on.
    sequential()
if __name__ == '__main__':
    main()
