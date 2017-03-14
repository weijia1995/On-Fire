# On-Fire
CS project for Zhuo Leng, Weijia Li, Xinzhu Sun, and Xingyun Wu


## Scripts for our program
  1. module.py is our main script
  2. review1.py is one of our modules that contains functions to crawl and analyse reviews
  3. crawling.py is another module to crawl all product information and generate csvs
  
  
## For Natural Language Process

### Program 1

Before run:
  1. install pip (in case you don't have it)
  2. command: [sudo] pip install textblob
  3. command: python -m textblob.download_corpora

To run:
  python freq.py folder/

Please note if you want to add words that you don't want to ignore during analysis,
simply add it into ignorelist at line 40, but make it uppercase as the others.

If you only want the frequency of a word in the current doc, it means you just want the
value of TF instead of TF * IDF, go to line 21, replace it with sentence "return tf(word, doc) * 1.0"

### Program 2

To run:
  python similarity.py file1.txt file2.txt


To run:
  python simliarity_2.py
  
### User Interface


Before run:
    go to the folder named "user_interface"
To run:
    python3 manage.py runserver
  
  
### All results are saved to shorten runing time
