————Program 1————
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

————Program 2————
To run:
  python similarity.py file1.txt file2.txt

