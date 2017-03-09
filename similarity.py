from collections import Counter
from textblob import TextBlob as tb
import codecs
import math
import sys
import time

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
    if len(sys.argv) != 3:
        print('Usage: python similarity.py text.txt description.txt')
        sys.exit(1)

    text1 = codecs.open(sys.argv[1], 'r', encoding='utf-8',
                    errors='ignore').read()
    text2 = codecs.open(sys.argv[2], 'r', encoding='utf-8',
                    errors='ignore').read()

    start_time = time.time()

    vector1 = text_to_vector(tb(text1))
    vector2 = text_to_vector(tb(text2))
    cos = getCos(vector1, vector2)

    print("Cosine Similarity between %s and %s: %f" % (sys.argv[1], sys.argv[2], cos))
    print("Running time: %s seconds" % (time.time() - start_time))
