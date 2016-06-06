from os import *
from os.path import isfile, join
import io
import math
#from nltk import PorterStemmer
import re

import my_porter

import time
start_time = time.time()

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

for dirs in files:
    number_of_files += 1
    file_name_map[dirs] = number_of_files
    file = io.open(dirs, 'r+b')
    mybytes = file.read()
    a = str(mybytes)
    b = a.lower()
    file.close()
    

    
        
    position_counter = 0
    for k in mainArray:
        #if k in stop_words or len(k) < 2 or re.match("^\d+?", k):
            #mainArray.remove(k)
            #pass
        #elif re.match("^\d+?", k):
            #mainArray.remove(k)

        
        #else:
        if k not in stop_words and len(k)>=2 and not(re.match("^\d+?",k)):
            position_counter += 1
            #k = PorterStemmer().stem_word(k)
            #k = my_porter.stem(k)
            if k not in hash_map.keys():
                hash_map[k] = [[file_name_map[dirs], 1, [position_counter]]]             
                
            
            else:
                
                if hash_map[k][-1][0] == file_name_map[dirs]:
                    hash_map[k][-1][1] += 1
                    hash_map[k][-1][2].append(position_counter)
                    
                    
                else:
                    hash_map[k].append([file_name_map[dirs], 1, [position_counter]])

f = io.open("../sorted_inverted.txt", "w")
f.write(str(number_of_files))
f.write("\n")
for key in sorted(hash_map):
    f.write(key)
    f.write("$")
    f.write(str(hash_map[key]))
    f.write("\n")

    
f.close()

print("---seconds---",time.time() - start_time)



##def search(word):
##   
##    tempArray = []
##    wordArray = re.split("\\W+|_", word)
##    test = 0
##    for j in range(len(wordArray)):
##        wordArray[j] = wordArray[j].lower()
##        wordArray[j] = PorterStemmer().stem_word(wordArray[j])
##    for term in wordArray:
##        if term not in hash_map.keys():
##            test += 1
##            
##
##    if len(wordArray) == 1:
##        if term not in hash_map.keys():
##            return "Not Found !"
##        print(term,' => [ Document ID , TF , [Positions] ] => ', hash_map[term], '\tDF => ', len(hash_map[term]))
##
##        for i in range(len(hash_map[term])):
##            print("Weight in document ", hash_map[term][i][0], " : ", hash_map[term][i][1]*math.log(number_of_files/len(hash_map[term])))
##    
##    elif len(wordArray) > 1 and test == len(wordArray):
##        return "Phrase Not Found !"
##
##    
##    elif len(wordArray) > 1 and test == 0:
##        for k in range(len(wordArray)-1):
##            c1 = c2 = 0
##            result = 0
##            same_doc_counter = 0
##            
##            while c1 < len(hash_map[wordArray[k]]) and c2 < len(hash_map[wordArray[k+1]]):
##                
##                if hash_map[wordArray[k]][c1][0] > hash_map[wordArray[k+1]][c2][0]:
##                    c2 += 1
##                    
##
##                elif hash_map[wordArray[k]][c1][0] < hash_map[wordArray[k+1]][c2][0]:
##                    c1 += 1
##                    
##                    
##                elif hash_map[wordArray[k]][c1][0] == hash_map[wordArray[k+1]][c2][0]:
##                    same_doc_counter += 1
##                    same_doc_id = hash_map[wordArray[k]][c1][0]
##                    
##                                        
##                    p1 = p2 = 0
##                    
##                    while p1 < len(hash_map[wordArray[k]][c1][2]) and p2 < len(hash_map[wordArray[k+1]][c2][2]):
##                        if hash_map[wordArray[k]][c1][2][p1] +1 > hash_map[wordArray[k+1]][c2][2][p2]:
##                            p2 += 1
##                            
##                        elif hash_map[wordArray[k]][c1][2][p1] +1 < hash_map[wordArray[k+1]][c2][2][p2]:
##                            p1 += 1
##                            
####################### for phrases which are in sequential positions ####################################################
##                        
##                        elif hash_map[wordArray[k]][c1][2][p1] +1 == hash_map[wordArray[k+1]][c2][2][p2]:
##                            tempArray.append([[wordArray[k], wordArray[k+1]], hash_map[wordArray[k]][c1][0], [hash_map[wordArray[k]][c1][2][p1], hash_map[wordArray[k+1]][c2][2][p2]]])
##                            
##                            result += 1
##                            p1 += 1
##
##                            
##                    c1+=1
##                    c2+=1
##                
############################################################################################################################                
##                    
####################### for phrases which are not in the same document at all ##############################################
##                
##            if same_doc_counter == 0:
##                for item in wordArray:
##                    search(item)
##                    print('\n')
##                    
############################################################################################################################
##                    
##
##                    
######################## for phrases which are in the same documents but not sequential positions ##########################
##                    
##            sameArray=[]
##            k1=k2=0
##            if same_doc_counter > 0 and result == 0:
##                for i in range(len(hash_map[wordArray[k]])):
##                    for j in range(len(hash_map[wordArray[k+1]])):
##                        if hash_map[wordArray[k]][i][0] > hash_map[wordArray[k+1]][j][0]:
##                            k1 += 1
##                        elif hash_map[wordArray[k]][i][0] < hash_map[wordArray[k+1]][j][0]:
##                            k2 += 1
##                        else:
##                            sameArray.append(hash_map[wordArray[k]][i][0])
##        
##                print(wordArray[k] ,' , ', wordArray[k+1], '  are both in document(s) ', sameArray)
##                #search(wordArray[k])
##                #print('\n')
##                #search(wordArray[k+1])
##                
###############################################################################################################################
##            
######################## when some words in input are not in inverted index ###################################################
##                
##    elif len(wordArray) > 1 and test > 0 and test < len(wordArray):
##        for term in wordArray:
##            if term not in hash_map.keys():
##                wordArray.remove(term)
##        search(' '.join(wordArray))
##        
###############################################################################################################################
##
##
##    
##    
##
##
##    if len(wordArray) >= 1:
##        individual = []
##        def get_key(item):
##            return item[2][0]
##        
##        sort=(sorted(tempArray, key = get_key))
##        counter=0
##        while len(sort) > 1 and counter < len(sort)-1:
##            if sort[counter][2][-1] == sort[counter+1][2][0]:
##                for i in range(1, len(sort[counter+1][0])):
##                    sort[counter][0].append(sort[counter+1][0][i])
##                    sort[counter][2].append(sort[counter+1][2][i])
##                sort.remove(sort[counter+1])
##            else:
##                counter += 1
##
##        def get_size(item):
##            return len(item[0])
##        final_sorted = sorted(sort, key = get_size, reverse =  True)
##                
##        for item in final_sorted:
##            print(item[0])
##            print('Document :', item[1])
##            print('Positions :',item[2],'\n')
##
##            for i in item[0]:
##                if i not in individual:
##                    individual.append(i)
##        print('--------------------------------------------------------------------------------')
##        for term in individual:
##            print(term,' => [ Document ID , TF , [Positions] ] => ', hash_map[term], '\tDF => ', len(hash_map[term]), '\n')
##            
##            
##    
##
##
##def inverted():
##    for item in hash_map:
##        print(item, " => ", hash_map[item])
##
##
##def find(no, pos):
##    for item in hash_map:
##        for i in range(len(hash_map[item])):
##            if hash_map[item][i][0] == no:
##                if pos in hash_map[item][i][2]:
##                    return(item)
##                
