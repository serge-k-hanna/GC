/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: hn
 *
 * Created on August 10, 2017, 11:50 AM
 */

#include <stdio.h>
#include <stdlib.h>
#include <NTL/ZZ_p.h>
#include <iostream>
#include "GF.h"
#include "Encoder.h"
#include "Decoder.h"
#include <bitset>
#include <vector>
#include <iterator>
#include <ctime>
#include <array>




using namespace std;
using namespace NTL;


void demo(long mlen, int numDels, int numChecker, int lengthExtension, int number=1){//a
        double elapsed_secs;
        long success = 0;
        long total = 0;
        Decoder de(mlen, numDels, numChecker, lengthExtension);
        for (int i = 0; i < number; ++i) {
            //generate deleted bit locations
            vector<long> dels(numDels,0);
            long idx = 0;
            while(idx<numDels){
                long temp = rand() % mlen;
                if(!(find(dels.begin(), dels.end(), temp) != dels.end())) {//is temp not in dels?
                    dels[idx]=temp;
                    idx++;
                }
            }

            //generate org and del sequence
            string orgdata = de.randBin();
            string deldata = de.erase(orgdata, dels);
            Vec<ZZ_p> parity = de.paritize(orgdata);
            //decode
            clock_t begin = clock();
            de.decode(deldata, parity);
            clock_t end = clock();
            elapsed_secs += double(end - begin) / CLOCKS_PER_SEC;

            //confirm
            if (deldata.compare(orgdata) == 0) {
                success++;
            }
            total++;
        }
        //print
        double aveTime = elapsed_secs / total * 1000;
        double failRate = (double) (total - success) / total * 100;
        cout<<mlen<<"\t"<<success<<"\t"<<total<<"\t"<<aveTime<<"\t"<<failRate<<"\t"<<numDels<<"\t"<<numChecker<<"\t"<<lengthExtension<<endl;
}

int main(int xargc, char **argv) {
    cout<<"mlen"<<"\t"<<"success"<<"\t"<<"total"<<"\t"<<"aveTime"<<"\t"<<"failRate"<<"\t"<<"numDels"<<"\t"<<"numChecker"<<"\t"<<"lengthExtension"<<endl;
//    array<long,11> mlens = {128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072};
    array<long,11> mlens = {128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072};
    array<long,1> numCheckers = {2};
    array<long,1> numDels = {1};
    array<long,1> lengthExtensions = {1};
    for ( auto lengthExtension = lengthExtensions.begin(); lengthExtension != lengthExtensions.end(); ++lengthExtension )
    {
        for ( auto numDel = numDels.begin(); numDel != numDels.end(); ++numDel )
        {
            for ( auto numChecker = numCheckers.begin(); numChecker != numCheckers.end(); ++numChecker )
            {
                for ( auto mlen = mlens.begin(); mlen != mlens.end(); ++mlen )
                {
                        demo(*mlen, *numDel, *numChecker, *lengthExtension, 1000);
                }
            }
        }
    }
}


