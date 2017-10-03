import numpy as np
from math import ceil, log, sqrt
class GF(object):
    '''Contains variable, methods to calculate, converse numbers in a finite field'''
    def __init__(self, mlen, lengthExtension=1):
        """
         Initialize a finite field as a base for an encoder/decoder.

        Args:
            mlen: the bit length of a complete message,
            lengthExtension: the multitple of the base blocklength (increasing block length means faster decoding)
        """
        self.numBlock, self.blockLength = self.getDem(mlen, lengthExtension)
        self.gf = self.nextPrime(2**self.blockLength)
        self.gfMinus2 = self.gf-2 #to save calculation when finding gf division (inversion).
        self.mlen = mlen

    def nextPrime(self, num):
        """
        Returns the smallest prime number that is greater than or equal to num.

        Args:
            num: the input number.

        Returns:
            Returns the smallest prime number that is greater than or equal to num.
        """
        def isPrime():
            """
            Check whether a number is a prime number.

            Args:
                num: the input number

            Returns:
                True if num is a prime number.
                Flase if num is NOT a prime number.
            """
            if num < 2: return False
            for i in range(2, int(sqrt(num)) + 1):
                if num % i == 0:
                    return False
            return True
        while isPrime() is False: num+=1
        return num
    def gfdiv(self, den, num = 1):
        """
        Returns the  result of a devision (num/den) in GF.

        Args:
            num: the numerator, num is set to 1 by default, which is equivalent to an GF inversion.
            den: the denominator.

        Returns:
            Returns the  result of a devision (num/den) in GF.
        """
        inv = pow(int(den), self.gfMinus2, self.gf) #the first parameter of pow must a Python int. int64 type of Numpy does not work.
        if num == 1: return inv
        else: return (num*inv)%self.gf
    def getgfdict(self):#not in C
        """
        Returns a GF inversion table containing pairs of number and its inversion in a given GF.
        """
        d={}
        p = self.gf
        for x in range(1, self.gf):
            if x not in d:
                y = pow(x, p-2, p)
                d[x]=y
                d[y]=x
        d[0]=None
        return d
    @staticmethod
    def getDem(mlen, lengthExtension=1): #k == original message length
        """
         Return the number of blocks and the bit length of each block for a given total bit length k.

        Args:
            k: the total bit length of a sequence.
            lengthExtension: the multitple of the base blocklength (increasing block length means faster decoding)
        Returns:
            blockLength: the ceiling of log k based 2.
            numBlock: the ceiling of k devided by blockLength.
        """
        if lengthExtension <=0: raise InvalidBlockLength()
        blockLength=lengthExtension*int(ceil(log(mlen,2))) #round up
        if blockLength > mlen: raise TooLongBlocks
        numBlock=int(ceil(mlen/blockLength))#round up
        return numBlock, blockLength
    def __str__(self):
        return 'numBlock ({}), blockLength ({}), gf({})'.format(self.numBlock, self.blockLength,self.gf)

class Encoder(GF):
    def __init__(self, mlen, numVec, lengthExtension=1):
        super().__init__(mlen, lengthExtension)
        #self.gfinv = self.getgfdict()
        self.numVec=numVec
        self.enVec=self.getEnVec(numVec)
    def getEnVec(self, numVec, type='cauchy'):
        """
        Returns encoding/decoding matrix.

        Args:
            numVec: number of column = # decoding parities + # checker parities
            type: if type is 'cauchy', return a cauchy matrix; otherwise, return a 'all one' matrix.


        Returns:
            Returns encoding/decoding matrix.
        """
        def allone():
            '''the last rows are zeros'''
            length=self.numBlock
            vectors=list()
            vectors = np.reshape([i**x for i in range(1,numVec+1) for x in range(length)],(numVec,length))
            return np.transpose(vectors)%self.gf
        def inv(A):
            for e in np.nditer(A, op_flags=['readwrite']):
                e[...] = self.gfdiv(e)
        if type!='cauchy': return allone()
        x = np.array(range(self.numBlock), np.int64)
        y = np.array(range(self.numBlock,self.numBlock+numVec), np.int64) #number of rows is the same as the number of blocks
        A=(x.reshape((-1,1)) - y)%self.gf
        inv(A)
        #A[self.numBlock:,:]=[0]
        return A%self.gf
    def paritize(self, data):
        """
        Returns a list of parities (done in sender's side).

        Args:
            data: the original binary sequence or a list of integers representing the original binary sequence.

        Returns:
            Returns a list of parities.
        """
        if type(data) == str:
            data = np.array(self.bin2int(self.breakString(data)), dtype=np.int64)
        p= np.dot(data, self.enVec[:len(data),:])%self.gf
        return p
    def breakString(self, s, dels=[]):
        """
         Break a long binary string into blocks of smaller binary strings
         with each block has the length of self.blocklength - number of deletion in that block.

        Args:
            s: the binary string to break down.
            dels: indices of the deletion in the string s.
        Returns:
            A list of smaller binary strings.
        """
        lens=[self.blockLength]*self.numBlock #create an array and fill it with blockLengths integers.
        for d in dels: #decrement the length of each block that has one or more deletions
            lens[d]-=1
        output=[]
        idx=0
        for l in lens: #build a binary string list with each block's length specified by the lens list.
            output.append(s[idx:idx+l])
            idx+=l
        numZeros=lens[-1]-len(output[-1])
        output[-1]=output[-1].zfill(numZeros) #left fill zeros to the last block in case of awkward mlen.
        return output
    @staticmethod
    def bin2int(b):
        """
         Converts a binary string or a list of binary strings to integers.

        Args:
            b: a binary string or a list of binary strings.

        Returns:
            A integer or a list of integers.
        """
        if type(b) == str:
            return int(b,2)
        else:
            output=[]
            for _b in b:
                try:
                    output.append(int(_b,2))
                except:
                    output.append(None)
        return output 
    def int2bin(self, num):
        """
         Converts an integer or a list of integers to binary strings with zeros left filled to make them blockLength size.

        Args:
            num: an integer or a list of integers.

        Returns:
            A binary string or a list of binary strings with zeros left filled to make them blockLength size
        """
        if type(num) != list:
            return bin(int(num))[2:].zfill(self.blockLength)
        else:#list
            output=[]
            for n in num:
                output.append(bin(int(n))[2:].zfill(self.blockLength))
            return output
    @staticmethod
    def pop(inputString, idx):
        """
        Returns the input binary string with bits at indices specified by idx removed.
        Used to generate a deleted sequence to feed the simulation.

        Args:
            inputString: the input string.
            idx: indices of the deleted bits.

        Returns:
            Returns the input binary string with bits at indices specified by idx removed.
        """
        if type(idx)==int: idx=[idx]
        chars = [c for c in inputString]
        for i in sorted(idx, reverse=True):
            del chars[i]
        return ''.join(chars)
    @staticmethod
    def genMsg(dataInt, mLen):
        """
        Convert an a decimal number to its binary representation.

        Args:
            dataInt: the input decimal.
            mLen: the size of the result binary string.

        Returns:
            An equivalent binary representation of the input decimal.
        """
   
        if dataInt>2**mLen: raise TooShortLength
        orim = bin(dataInt)[2:].zfill(mLen)
        return orim
    def __str__(self):
        return ('Decoding matrix: \n'+str(self.enVec)+
                super().__str__())

