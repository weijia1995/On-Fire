from collections import Counter
from textblob import TextBlob as tb
import codecs
import math
import sys
import time
import glob

# Get cosine similarity of two vectors
def getCos(vec1, vec2):
    all_values = set(vec1.keys()) & (set(vec2.keys()))
    numerator = sum([vec1[key] * vec2[key] for key in all_values])
    sum1 = sum([vec1[key] ** 2 for key in vec1.keys()])
    sum2 = sum([vec2[key] ** 2 for key in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# convert word list to vectors
def text_to_vector(text):
    return Counter(text.words)


if __name__ == '__main__':
    files_des=[]
    files_rev=[]
    files_des = glob.glob("/Users/admin/Desktop/CS/NLPK/dataset/*_des.txt")
    files_rev = glob.glob("/Users/admin/Desktop/CS/NLPK/dataset/*_rev.txt")
    text1=[]
    text2=[]

    for i in  range (0, 5):
        des = codecs.open(files_des[i], 'r', encoding='utf-8',
                    errors='ignore').read()
        text1.append(des)
        rev = codecs.open(files_rev[i], 'r', encoding='utf-8',
                    errors='ignore').read()
        text2.append(rev)
        vector1 = text_to_vector(tb(text1[i]))
        vector2 = text_to_vector(tb(text2[i]))
        cos = getCos(vector1, vector2)
        print(cos)




