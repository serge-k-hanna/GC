# About This Simulation.
This is one of two implimentations that we wrote to simulate Guess & Check Algorithms. The other one was writen in Python (https://github.com/HieuNguyen202/GC), which is easy to code, but slow. In an attemp to optimize decoding speed using G & C algorithms, this implimentation was born. However, this is not a fully completed work. All we did was to translate what we had in Python to C++. We believe there is still a lot of room for optimization because of the C++'s control over lower level of computer's resources. Below are some of areas can be optimized:
1. The use of variables (try to reuse or maintain often used variable. don't make uneccessary copies when passing them to other fucnitons.)
2. NTL's Multithreading: NTL has its own multithreading library to speed up some matrix calculations.
3. Levanshtein Distance check (to minimized failure probability with an unnoticeable increase in run time): this is available in the Python implimentation.
# Guess and Check Algorithms 
This project was based upon the Guess &amp; Check Algorithms (GC) by Dr. Salim El Rouayheb and Serge Kashanna. The goal of this project was to simulate and optimize the decoding process to recover one or multiple deletions using GC algorithms (please help me on the section, Serge).
# Installation Guide
## Requirements
1. [Number Theory Library (NTL)](http://www.shoup.net/ntl/) by Victor Shoup: You must install this library to your machine and correctly add the include path to its header files.
2. Recomended OS: Unix (Mac or Linux).
3. Compiler: `g++` (because of NTL)
## Additional Library
This implimentation is so much easier thanks to the help of [Number Theory Library (NTL)](http://www.shoup.net/ntl/).
This is a wonderful library that effectively deals with calculations in finite field.
Some of the helpful features include performing basic mathematical calculations in finite field, simulating abitrary sized numbers, and performing matrix manipulations in finite field. 
Detailed installation guide can be found in Shoup's website. However, below are some tips and IDE settings that might be helpful to you.
## Tips
Here is one quick way to compile this project in terminal is (assuming you have install NTL in `/usr/local`).

In *Terminal*:
```
cd /to/your/project/folder
```
```
g++ -g -O2 main.cpp -o main -lntl -lgmp -lm
```
## Setup IDE
All of these settings are for your IDE to be able to compile NTL library.
1. Suggested IDE: CLion because this was done in CLion, but anything uses g++ compiler should work (with the right settings, see below).
2. Add additional linking flags to your linker setting: `-lntl` `-lgmp` `-lm`.
3. Add additional compiling flags to your compiler setting: `-g` `-O2`.
4. Change your default C++ compiler to `g++` (if it is not already in used). Check this folder `/usr/bin/g++` (although it could be at somewhere else depending on the Unix package manager you use.)

## Wanrning to Windows Users.
I have not been able to compile this project using Visual Studio's complier (MSVC). If you are testing this codes in a Windows machine, make sure you use g++ to compile this project. MinGW and Cygwin are the two tools could help you to get the g++ compiler and Unix like Terminal.
