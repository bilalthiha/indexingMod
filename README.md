# indexingMod
This package implements an indexing component of an information retrieval system using SPIMI algorithm.

==========DESCRIPTION=============

This python program (indexingMod) implements an indexing component of an information retrieval system using SPIMI algorithm. 

Inputs to the indexing program: 
1. Path to the dataset directory containing text files. (e.g "C:\Dataset")
2. Block size for SPMI algorithm. (e.g 50000)

Output of the indexing program:
1. A text file containing the inverted index, which is "out_SPIMI_Output.txt". This file is output in the same directory as the input dataset.

==========ENVIRONMENT SET-UP=============
1. Download this indexing package (indexingMod) from GitHub (easy as a zip file). Save and unzip it in a preferred directory in your machine (e.g "C:\Test\indexingMod")
Note: An example dataset is available in the package as "ExampleDataset.zip" for use.
2. Install Python 3.8.0 or above from https://www.python.org/downloads/.
3. Install Natural Language Toolkit from https://www.nltk.org/
Note: A reference tutorial of NLTK can be found in this YouTube video. https://www.youtube.com/watch?v=FLZvOKSCkxY


==========HOW TO RUN THE PROGRAM=============
1. Launch the command line. 
E.g For Windows, press Window Key + R on keyboard and then type 'cmd'

2. Locate the path of python executable in your machine. 
E.g. For Windows, it's usually located at "C:\Users\YourUserId\AppData\Local\Programs\Python\Python38-32". Replace "YourUserId" with your actual Windows user Id.

3. Change current directory in the command line to the python path above.
E.g For Windows, "cd C:\Users\YourUserId\AppData\Local\Programs\Python\Python38-32"

4. Get the path of the indexing program (indexingMain.py) in your machine.
E.g "C:\Test\indexingMod\indexingMain.py"

5. Get the path of the input dataset containing text files to index.
E.g "C:\Test\indexingMod\HillaryEmails"

6. Decide on a block size of SPIMI algorithm.
E.g 100000

7. Excecute the indexing program in the command line using data from 4, 5 and 6.
E.g "python C:\Test\indexingMod\indexingMain.py C:\Test\indexingMod\HillaryEmails 100000"

8. Wait for some time until the program ends. The program will respond on the command line when it ends. It could take up to a few minutes.

9. Find the program output file which contains the inverted index under the same directory as the input dataset.
E.g "C:\Test\indexingMod\HillaryEmails\out_SPIMI_Output.txt"

10. Find the timing statistics file which contains the related timing statistics under the same directory as the input dataset.
E.g "C:\Test\indexingMod\HillaryEmails\out_timeStats4BlkSz100000
