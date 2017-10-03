import numpy as np
from math import fabs
from Encoder import *
class Decoder(Encoder):
    def __init__(self, mlen, numDel, numChecker, lengthExtension):
        """
         Initialization of each deleted sequence.

        Args:
            s: The binary string of the deleted sequence.
            p: A list of parity integers.
            mlen: The bit length of the original sequences.
        """
        super().__init__(mlen, numDel + numChecker,  lengthExtension)
        self.numDel = numDel
        self.maxVal = pow(2, self.blockLength)
    def caseGen(self, reverse = False):
        """
         Return a GENERATOR of all possible indices where deletions might occur. Example, [[0], [1], [2], [3]] is the result of calling case(numBlock=4, numDel=1).
         Notice this call does not use too much time and memory because it returns a generator instead of a actual list deletion cases.

        Args:
            reverse: if true, generates cases in a reverse order.

        Returns:
            A generator of all possible indices where deletions might occur. 

        Raises:
            None
        """
        numBlock, numDel = self.numBlock, self.numDel
        def case_rec(numDel, first, last, root=list()):
            """
             A recursive method assiting the generation of deletion cases.

            Args:
                numDel: Number of deletions.
                start: The first deletion index of the remaining deletion.
                root: The base indices for each each guess.

            Returns:
                A generator of all possible indices where deletions might occur. 

            Raises:
                None
            """
            if numDel==1:
                for current in range(first, last, change):
                    root.append(current)
                    yield root
                    del root[-1]
            else:
                for current in range(first, last, change):
                    root.append(current)
                    yield from case_rec(numDel-1, current , last, root)
                    del root[-1]
        if reverse == False:
            change=1
            return case_rec(numDel, 0, numBlock) 
        else:
            change=-1
            return case_rec(numDel, numBlock-1, 0-1)
    def caseGenFast(self,s ,p ,reverse = False):
        """
         Return a GENERATOR of all possible indices where deletions might occur. Example, [[0], [1], [2], [3]] is the result of calling case(numBlock=4, numDel=1).
         Notice this call does not use too much memory because it return a generator instead of a actual list. It is also less time consumming.
         In addition, this also maintains P', which is a array of Parity minus known quantities on the left when solving the systems of equations.
        
        Args:
            s: the deleted binary string
            p: the parities
            reverse: if true, generates cases in the reverse order (not tested)
        Returns:
            root: a list of deletion indices 
            pprime: p'
        Raises:
            None
        """
        numBlock, numDel = self.numBlock, self.mlen-len(s)
        def baseCase():
            dels=[self.numBlock-1]*self.numDel
            lst = []
            lst.append(self.bin2int(self.breakString(s, dels))) # convert each block in b into an equivalent integer.
            lst[-1][self.numBlock-1]=0
            for i in range(self.numDel):
                dels[i]=0
                lst.append(self.bin2int(self.breakString(s, dels)))
                for j in set(dels):
                    lst[-1][j]=0
            return lst
        def case_rec(first, last, idx=0, pprime=0):
            """
             A recursive method assiting the generation of deletion cases.

            Args:
                numDel: Number of deletions.
                start: The first deletion index of the remaining deletion.
                root: The base indices for each each guess.

            Returns:
                A generator of all possible indices where deletions might occur. 

            Raises:
                None
            """
            if idx != numDel-1:
                for current in range(first, last, change):
                    if current > first:
                        pprime+=d[-1][current]*self.enVec[current,:]
                    root[idx] = current
                    yield from case_rec(current, last, idx + 1, np.array(pprime))
                    if idx==0 or current > first:
                        pprime-=d[idx][current]*self.enVec[current,:]
            else:
                for current in range(first, last, change):
                    root[idx] = current
                    if current != first:
                        pprime+=d[-1][current]*self.enVec[current,:]
                    yield root, pprime
                    if idx==0 or current != first:
                        pprime-=d[idx][current]*self.enVec[current,:]
        d= baseCase()
        root=[0]*numDel
        pprime=(p - np.dot(d[-1], self.enVec))
        if reverse == False:
            change=1
            return case_rec(0, numBlock, pprime=pprime) 
        else:
            change=-1
            return case_rec(numBlock-1, -1, pprime=pprime)
    def rcaseGen(self, sidx, number=None):
        """
         Return a GENERATOR of all possible indices where deletions might occur. Example, [[0], [1], [2], [3]] is the result of calling case(numBlock=4, numDel=1).
         Notice this call does not use too much memory because it return a generator instead of a actual list. It is also less time consumming.
         This is used to distribute cases in multiprocessing.

        Args:
            sidx: the index of the first case a process is taking care of.
            number: the number of cases from the first index.

        Returns:
            A generator of all possible indices where deletions might occur. 

        Raises:
            None
        """
        def numCase():
            return table[self.numDel][self.numBlock]
        def getTable():
            '''Table of number of cases vs number of deletions, used to split the task for multitple processes.'''
            l=self.numBlock+1
            t = []
            d1 = [1]*l
            d1[0]=0
            t.append(d1)
            for n in range(self.numDel):
                t.append([sum(t[-1][:i+1]) for i in range(l)])
            return t
        def case_rec(numDel, last=0, root=list()):
            """
             A recursive method assiting the generation of deletion cases.

            Args:
                numDel: Number of deletions.
                last: The last deletion index of the remaining deletion.
                root: The base indices for each each guess.

            Returns:
                A generator of all possible indices where deletions might occur. 

            Raises:
                None
            """
            if numDel==1:
                for loc in range(numBlock - sidx[0], last -1 , -1):
                    if count[0] >= number: break
                    else:
                        root.append(loc)
                        yield root
                        del root[-1]
                    count[0]+=1
            else:
                idx = 0
                for i in range(len(table[numDel])):
                    if table[numDel][i]>=sidx[0]:
                        idx = i
                        break
                sidx[0] = sidx[0] - table[numDel][idx - 1]
                for d in range(numBlock - idx, last -1 , -1):
                    if count[0] >= number: break
                    root.append(d)
                    yield from case_rec(numDel-1, d, root)
                    del root[-1]
        numBlock, numDel = self.numBlock, self.mlen-len(s)
        table = getTable() # make this class variable if used so it will not get a new table each run
        sidx=[sidx+1]
        if number == None: number = self.numCase()
        count=[0]
        return case_rec(numDel)
    @staticmethod
    def levCheck(r, b, dels):
        """
         Check the posibility of each recovered deleted binary string using Lavenshtein distance algorithms.

        Args:
            r: a list of recovered deleted binary string.
            dels: indices of the deletions.

        Returns:
            True if all recovery pass the Lev test.
            False if any one them fails.
        """
        def lev(strX, strY):
                '''Check the Lavenshtein distance of the two strings strX and strY.

                Args:
                    strX: the first string.
                    strY: the second string.

                Returns:
                    True if distance is greater than number of deletions.
                    False otherwise.
                '''
                if len(strX) > len(strY):
                    strX, strY = strY, strX
                dels=int(fabs(len(strX)-len(strY)))
                strX=' '+strX
                strY=' '+strY
                m=len(strX)
                n=len(strY)
                t=[[None for _ in range(m)] for _ in range(n)]
                for j in range(m):
                    t[0][j]=j
                for i in range(n):
                    t[i][0]=i
                for i in range(1, n):
                    donotreturn=False
                    for j in range(1, m):
                        if strX[j]==strY[i]:
                            t[i][j]=t[i-1][j-1]
                        else:
                            minVal=min(t[i][j-1],t[i-1][j])
                            t[i][j]=minVal+1  
                        if t[i][j]<=dels: donotreturn=True
                    if donotreturn==False and t[i][0]>dels: return False
                return True
        for i in range(len(r)):
            if lev(b[dels[i]],r[i]):
                b[dels[i]]=r[i]
            else:
                return False
        return True

    def olddecode(self, dels):
        """
         A recursive method assiting the generation of deletion cases. This is not memory and time efficient.

        Args:
            dels: A list of deltion indices.
            de: A decoder that has a decode method.

        Returns:
            A binary string of the recovered sequence.
        """
        def decoder(self, data, parity, dels):
            dels=list(sorted(set(dels)))
            numDel=len(dels)
            if numDel==1: return self.onedel(data, parity, dels)
            if numDel==2: return self.twodels(data, parity,dels)
            if numDel==3: return self.twodels(data, parity,dels)
        b = self.breakString(s, dels) # Bring the deleted sequence in to blocks of smaller binary strings with the deleted bits removed.
        i = self.bin2int(b) # convert each block in b into an equivalent integer.
        for d in dels: i[d]=0 # set the blocks that contain the deletion to zeros.
        r, valid =self.decoder(i, p, dels) # decode using a decoder, r is a list of candidates for the deleted value.
        if not valid: return None# valid means it has passed the parity check.
        r = self.int2bin(r) # converts the recovered deleted values to binary strings.
        #for i in range(len(r)):
        #    b[dels[i]]=r[i]
        if not self.levCheck(r, b, dels):
            print('failed Lev')
            return None #Do the Levanshtein Distance check of the recovered deleted binary strings.
        lastLen=self.mlen%self.blockLength
        b[-1]=b[-1][-lastLen:] # re-adjust the length of the last block in case of awkward mlen (not 2^x).
        return ''.join(b) # return the sequence if all tests are passed.
    def decode(self, s, p):
        """
            A decoding manager, which calls the appropriate functions based on the number of distinct deletions.

        Args:
            s: the deleted binary sequence
            p: the parities

        Returns:
            A binary string of the recovered sequence.

        Raises:
            DecodingError: no valid case -> there must be somehthinf wrong witht the decoder.
        """
        cases = self.caseGenFast(s, p)
        if self.numDel == 1: solver = self._solve1
        elif self.numDel == 2: solver = self._solve2
        for case in cases:
            dels = case[0]
            #ddels = dels
            #ddels = sorted(list(set(dels)))
            pprime = case[1]
            #if len(ddels) == 1:
            #    X, valid = self._solve1(pprime,ddels[0])
            #else:
            #    X, valid = self._solve2(pprime, ddels)
            X, valid = solver(pprime, dels)
            if valid:
                cdels = {d:dels.count(d) for d in dels}
                X = self.int2bin(X) # converts the recovered deleted values to binary strings. 
                count = 0
                for d in cdels.keys():
                    left = d*self.blockLength
                    right = (d+1)*self.blockLength-cdels[d]
                    if d == self.numBlock-1:
                        lastLen=self.mlen%self.blockLength
                        X[count] =  X[count][-lastLen:]
                    s = s[:left] + X[count] + s[right:] # return the sequence if all tests are passed.
                    count+=1
                return s
        raise DecodingError

    def solve1(self, data , parity, dels):
        """
            Preperation of one deletion solver.

        Args:
            data: a list if integers representing a guess.
            parity: the parities
            dels: a list of deletion indices, received from a case generator.

        Returns:
            [X]: A list of integers representing recover sub-sequence.
            valid: whether the recover integer has passed the parity check.

        """
        pprime = parity - np.dot(data,self.enVec)
        return _solve1(pprime, dels[0])
    def _solve1(self, pprime, dels):
        '''
            One deletion solver (Cramer's rules)
            cX + sumknown = p0
            X = (p0-sumknown)*gfinv(c)
            X = pprime*gfinv(c)

        Args:
            pprime: a list of parity - known quantities on the left.
            dels: a list of deletion indices, received from a case generator.

        Returns:
            [X]: A list of integers representing recover sub-sequence.
            valid: whether the recovered integer has passed the parity check.
            
        '''
        def isvalid():
            '''Check the validity of the result against the checker parities.'''
            for i in range(1, len(pprime)):
                valid = ((self.enVec[dels][i] * float(X)) - pprime[i])%self.gf == 0
                if not valid: break
            return valid
        dels=dels[0]
        X = self.gfdiv(self.enVec[dels][0], pprime[0])
        #print(pprime, dels, X, self.gfdiv(self.enVec[dels][0]))
        if isvalid():
            
            return [X], True
        else:
            return None, False
    def solve2(self, data, parity, dels):
        """
            Preperation of two deletion solver.

        Args:
            data: a list if integers representing a guess.
            parity: the parities
            dels: a list of deletion indices, received from a case generator.

        Returns:
            [X1, X2]: A list of integers representing recover sub-sequence.
            valid: whether the recover integer has passed the parity check.

        """
        pprime = parity - np.dot(data,self.enVec)
        return _solve2(pprime, dels)
    def _solve2(self, pprime, dels):
        '''
            Two deletion solver (Cramer's rules)
            cX + sumknown = p0
            X = (p0-sumknown)*gfinv(c)
            X = pprime*gfinv(c)

        Args:
            pprime: a list of parity - known quantities on the left.
            dels: a list of deletion indices, received from a case generator.

        Returns:
            [X1, X2]: A list of integers representing recover sub-sequence.
            valid: whether the recovered integer has passed the parity check.
            
        '''
        def isvalid():
            '''Check the validity of the result against the checker parities.'''
            for i in range(2, self.numVec):
                valid = ((self.enVec[dels[0]][i] * X1 + self.enVec[dels[1]][i]*X2) - pprime[i])%self.gf == 0
                if not valid: break
            return valid
        # detA = ad - bc
        detA = ((self.enVec[dels[0]][0]*self.enVec[dels[1]][1])-(self.enVec[dels[1]][0]*self.enVec[dels[0]][1]))
        idetA = self.gfdiv(detA)
        detX1 = (pprime[0]*self.enVec[dels[1]][1])-(pprime[1]*self.enVec[dels[1]][0])
        X1 = detX1*idetA%self.gf
        #if X1 >= self.maxVal: return None, False
        detX2 = (pprime[1]*self.enVec[dels[0]][0])-(pprime[0]*self.enVec[dels[0]][1])
        X2 = detX2*idetA%self.gf
        #if X2 >= self.maxVal: return None, False
        if isvalid():
            return [X1, X2], True
        else:
            return None, False
