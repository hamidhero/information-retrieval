import re
import io
from math import log
import my_porter
import pickle


with io.open("../sorted_inverted.txt", "rb") as handle:
    hash_map = pickle.loads(handle.read())

number_of_files = hash_map['num_of_files']
##f = io.open("..\sorted_inverted.txt", "r")
##hash_map = {}
##hash_file_number = {}
##number_of_files = f.readline()
##
##for line in f:
##    split = "a = re.split('\$', line)"
##    exec(split)
##
##    a[1] = "temp = " + a[1]
##    exec(a[1])
##   
##    hash_map[a[0]] = temp
##
##    
##f.close()


def search(word):
   
    tempArray = []
    wordArray = re.split("\\W+|_+", word)
    test = 0
    for j in range(len(wordArray)):
        wordArray[j] = wordArray[j].lower()
        wordArray[j] = my_porter.stem(wordArray[j])
    for term in wordArray:
        if term not in hash_map.keys():
            test += 1

    if len(wordArray) >= 1 and test == len(wordArray):
        return "Word or Phrase Not Found !"
            

    elif len(wordArray) == 1 and test == 0:
        
        print(term,' => [ Document ID , TF , [Positions] ] => ', hash_map[term], '\tDF => ', len(hash_map[term]))

        for i in range(len(hash_map[term])):
            print("Weight of document ", hash_map[term][i][0], " : ", hash_map[term][i][1]*log((number_of_files)/len(hash_map[term])))

    
    elif len(wordArray) > 1 and test == 0:
        for k in range(len(wordArray)-1):
            c1 = c2 = 0
            result = 0
            same_doc_counter = 0
            
            while c1 < len(hash_map[wordArray[k]]) and c2 < len(hash_map[wordArray[k+1]]):
                
                if hash_map[wordArray[k]][c1][0] > hash_map[wordArray[k+1]][c2][0]:
                    c2 += 1
                    

                elif hash_map[wordArray[k]][c1][0] < hash_map[wordArray[k+1]][c2][0]:
                    c1 += 1
                    
                    
                elif hash_map[wordArray[k]][c1][0] == hash_map[wordArray[k+1]][c2][0]:
                    same_doc_counter += 1
                    same_doc_id = hash_map[wordArray[k]][c1][0]
                    
                                        
                    p1 = p2 = 0
                    
                    while p1 < len(hash_map[wordArray[k]][c1][2]) and p2 < len(hash_map[wordArray[k+1]][c2][2]):
                        if hash_map[wordArray[k]][c1][2][p1] +1 > hash_map[wordArray[k+1]][c2][2][p2]:
                            p2 += 1
                            
                        elif hash_map[wordArray[k]][c1][2][p1] +1 < hash_map[wordArray[k+1]][c2][2][p2]:
                            p1 += 1
                            
##################### for phrases which are in sequential positions ####################################################
                        
                        elif hash_map[wordArray[k]][c1][2][p1] +1 == hash_map[wordArray[k+1]][c2][2][p2]:
                            tempArray.append([[wordArray[k], wordArray[k+1]], hash_map[wordArray[k]][c1][0], [hash_map[wordArray[k]][c1][2][p1], hash_map[wordArray[k+1]][c2][2][p2]]])
                            
                            result += 1
                            p1 += 1

                            
                    c1+=1
                    c2+=1
                
##########################################################################################################################                
                    
##################### for phrases which are not in the same document at all ##############################################
                
            if same_doc_counter == 0:
                for item in wordArray:
                    search(item)
                    print('\n')
                    
##########################################################################################################################
                    

                    
###################### for phrases which are in the same documents but not sequential positions ##########################
                    
            sameArray = []
            k1 = k2 = 0
            if same_doc_counter > 0 and result == 0:
                for i in range(len(hash_map[wordArray[k]])):
                    for j in range(len(hash_map[wordArray[k+1]])):
                        if hash_map[wordArray[k]][i][0] > hash_map[wordArray[k+1]][j][0]:
                            k1 += 1
                        elif hash_map[wordArray[k]][i][0] < hash_map[wordArray[k+1]][j][0]:
                            k2 += 1
                        else:
                            sameArray.append(hash_map[wordArray[k]][i][0])
        
                print(wordArray[k] ,' , ', wordArray[k+1], '  are both in document(s) ', sameArray)

                for i in range(len(sameArray)):
                    w1 = w2 = 0
                    for j in range(len(hash_map[wordArray[k]])):
                        if hash_map[wordArray[k]][j][0] == sameArray[i]:
                            w1 = hash_map[wordArray[k]][j][1]*log((number_of_files)/len(hash_map[wordArray[k]]))
                    for q in range(len(hash_map[wordArray[k+1]])):
                        if hash_map[wordArray[k+1]][q][0] == sameArray[i]:
                            w2 = hash_map[wordArray[k+1]][q][1]*log((number_of_files)/len(hash_map[wordArray[k+1]]))
                            
                    print("weight of document ", sameArray[i], " is : ", w1 + w2)
                #search(wordArray[k])
                #print('\n')
                #search(wordArray[k+1])
                
#############################################################################################################################
            
###################### when some words in input are not in inverted index ###################################################
                
    elif len(wordArray) > 1 and test > 0 and test < len(wordArray):
        for term in wordArray:
            if term not in hash_map.keys():
                wordArray.remove(term)
        search(' '.join(wordArray))
        
#############################################################################################################################


    
    


    if len(tempArray) >= 1:
        individual = []
        def get_key(item):
            return item[2][0]
        
        sort=(sorted(tempArray, key = get_key))
        counter=0
        while len(sort) > 1 and counter < len(sort)-1:
            if sort[counter][2][-1] == sort[counter+1][2][0]:
                for i in range(1, len(sort[counter+1][0])):
                    sort[counter][0].append(sort[counter+1][0][i])
                    sort[counter][2].append(sort[counter+1][2][i])
                sort.remove(sort[counter+1])
            else:
                counter += 1

        def get_size(item):
            return len(item[0])
        final_sorted = sorted(sort, key = get_size, reverse =  True)

        terms=[]
        
        for item in final_sorted:
            print(item[0])
            terms = item[0]
            print('Document :', item[1])
            doc = item[1]
            w = 0
            for x in range(len(terms)):
                for y in range(len(hash_map[terms[x]])):
                    if hash_map[terms[x]][y][0] == doc:
                        w += hash_map[terms[x]][y][1]*log((number_of_files)/len(hash_map[terms[x]]))
            print('Positions :',item[2])

            print("### weight of document ", item[1], " is : ",w, " ###",'\n')

            for i in item[0]:
                if i not in individual:
                    individual.append(i)
        print('--------------------------------------------------------------------------------')
        for term in individual:
            print(term,' => [ Document ID , TF , [Positions] ] => ', hash_map[term], '\tDF => ', len(hash_map[term]), '\n')


    


def inverted():
    for item in hash_map:
        print(item, " => ", hash_map[item])


def find(no, pos):
    for item in hash_map:
        for i in range(len(hash_map[item])):
            if hash_map[item][i][0] == no:
                if pos in hash_map[item][i][2]:
                    return(item)
                
