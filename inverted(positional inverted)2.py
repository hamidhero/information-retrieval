from os import *
from os.path import isfile, join
import io
import re
import pickle
import my_porter
#import time

hash_map = {}
file_name_map={}


stop_words=frozenset(['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before',
            'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
            'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's",
            'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't",
            'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
            'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so',
            'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll",
            "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've",
            'were', "weren't", 'what', "what's",'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't",
            'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'])

mypath = "."
files = [ f for f in listdir(mypath) if (isfile(join(mypath,f)) and f!= path.basename(__file__)) ]

number_of_files=0
#start_time = time.time()




for dirs in files:
    number_of_files += 1
    file_name_map[dirs] = number_of_files
    file = io.open(dirs, 'r+b')
    mybytes = file.read()
    a = str(mybytes)
    b = a.lower()
    file.close()

    mainArray = re.split("\\W+|_+", b)
    
        
    position_counter = 0

    for k in mainArray:

        if k not in stop_words and len(k)>=2 and not(re.match("^\d+?",k)):
            position_counter += 1
            
            k = my_porter.stem(k)
    
            try:
                if hash_map[k][-1][0] == file_name_map[dirs]:
                    hash_map[k][-1][1] += 1
                    hash_map[k][-1][2].append(position_counter)
                    
                    
                else:
                    hash_map[k].append([file_name_map[dirs], 1, [position_counter]])

            except Exception :
                hash_map[k] = [[file_name_map[dirs], 1, [position_counter]]]                                 


#print("before writing to file and after 'FOR' : ",time.time() - start_time)

hash_map['num_of_files'] = number_of_files

with io.open("../sorted_inverted.txt", "wb") as handle:
    pickle.dump(hash_map, handle)


#print("---seconds---",time.time() - start_time)
