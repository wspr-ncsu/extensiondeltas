import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

def extract_dates(inPath):
    categories = ['7_productivity', '38_search_tools', '11_web_development']
    with open(inPath) as f:
        lines = f.read().splitlines()
    days_list = []
    descriptions_list = []
    path_not_exist = 0 
    for l in lines:
        fields = l.split('_')
        hid = fields[0]
        y =  fields[9]
        m =  fields[10]
        d =  fields[11]
        path = "/home/kapravel/crawl_metadata/chrome-extensions-archive/crawled/pages/" + hid
        path0 = y + '-' + m + '-' + d 
        print(path0)
        if not os.path.isdir(path):
            path_not_exist += 1
            continue
        # for malicious extensions first
        prefixed = list(os.listdir(path))[0]
        print(prefixed)

        # check if string or list
        # if not isinstance(prefixed, basestring):
        #     prefixed = prefixed[0]

        #check for specific date
        # prefixed = [filename for filename in os.listdir(path) if filename.startswith(path0)]
        if not len(prefixed):
            continue
        with open(path + '/' + prefixed) as json_file:
            desc = json.load(json_file)['full_description']
            # print(desc)
            descriptions_list.append(desc)
    print(len(descriptions_list))
    descriptions_list = removeUnicodeErrors(descriptions_list)
    print("Path not found out of 143 malicious: " + str(path_not_exist))
    
    # add rest of descriptions non-malicious
    progress_counter = 0
    descriptions_list_benign = []
    path_not_exist_benign = 0
    base_path = "/home/kapravel/crawl_metadata/chrome-extensions-archive/crawled/pages/"  
    length = len(os.listdir(base_path))
    print(length)
    for hid in os.listdir(base_path)[:50000]:
        print(str(progress_counter) + " out of " + str(length))
        progress_counter += 1
        prefixed = list(os.listdir(base_path+hid))[0]
        # print(prefixed)
        if not os.path.isdir(path):
            path_not_exist_benign += 1
            continue
        if not len(prefixed):
            continue
        # initialize category in case not found afterwards
        extension_category = "not_found"
        with open(base_path + hid + '/' + prefixed) as json_file:
            try:
                extension_category = json.load(json_file)['category']
            except:
                pass
        if extension_category in categories:
            with open(base_path + hid + '/' + prefixed) as json_file:
                desc = json.load(json_file)['full_description']
                descriptions_list_benign.append(desc + 'putthecategoryafterhere' + extension_category)
        if not path_not_exist_benign % 100:
            print(len(descriptions_list_benign))
    # print(len(descriptions_list_benign))
    descriptions_list = removeUnicodeErrors(descriptions_list_benign)
    print("Path not found out of ~200k non-malicious: " + str(path_not_exist_benign))
    return (descriptions_list, descriptions_list_benign)


def removeUnicodeErrors(descriptions_list):
    for d in descriptions_list:
        try:
            print(str(d))
            print('\n\n')
        except UnicodeEncodeError:
            descriptions_list.remove(d)
    print(len(descriptions_list))
    return descriptions_list

def idf_implementation(descriptions_list):
    stopwords = {"after","all","also","an","a","and","any","ve","was","want","wants",
        "about", "way", "we", "well","were","what", "when", "where", "whether",
    "which", "while", "why", "with","will", "you", "your", "yakkyofy", "without"}
    vectorizer = TfidfVectorizer( max_features=100, stop_words=stopwords)
    vectors = vectorizer.fit_transform(descriptions_list)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    with open("idf_out.txt", 'w') as f:
        f.write(str(df.mean()))
    print(df.mean())

def writeToFiles(descriptions_list, starting_letter):
    resultPath = "/home/npantel/scripts/test/major_revision_experiments/results/"
    try:
        os.makedirs(resultPath)
    except OSError:
        pass
    cnt = 0
    for l in descriptions_list:
        # get category encoded at the end
        actual_description = l.split('putthecategoryafterhere')[0]
        category = l.split('putthecategoryafterhere')[1]
        with open(resultPath + starting_letter + str(cnt) + '_' + category + ".txt", 'w') as f:
            f.write(actual_description.encode('utf-8'))
        cnt += 1

def descriptionLengthComparison():
    mal_lengths = []
    nonmal_lengths = []
    for each in os.listdir('results'):
        fileName = 'results/' + each
        if len(each.split('_')) < 2:
            with open(fileName) as f: 
                mal_lengths.append(len(f.read().splitlines()))
        else:
            with open(fileName) as f: 
                nonmal_lengths.append(len(f.read().splitlines())) 
    print(len(mal_lengths))
    print(len(nonmal_lengths))
    print("Malicious documents had an average length of %d lines" % (sum(mal_lengths)/len(mal_lengths)))
    print("Non malicious documents had an average length of %d lines" % (sum(nonmal_lengths)/len(nonmal_lengths)))


def idfImplementNew():
    stopwords = {"after","all","also","an","a","and","any","ve","was","want","wants",
        "about", "way", "we", "well","were","what", "when", "where", "whether",
    "which", "while", "why", "with","will", "you", "your", "yakkyofy", "without"}
    file_list = sorted(os.listdir('results'))
    full_path_file_list = []
    for f in file_list:
        full_path_file_list.append('results/' + f)
    vectorizer = TfidfVectorizer(input='filename', max_features=10000, stop_words=stopwords)
    vectors = vectorizer.fit_transform(full_path_file_list)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    # print(denselist)
    print(denselist[0])
    # df = pd.DataFrame(denselist, columns=feature_names)
    result_list = {}
    for i in range(76):
        df = pd.DataFrame(np.array(denselist[i]).reshape(1, 8855), columns=feature_names, index=['a'])
        df2 = df.sort_values(by='a', axis=1, ascending=False)
        # outputLine = sorted(denselist[i], reverse=True)
        # print(df2.iloc[0,0:20])
        with open("idf_out.txt", 'a') as f:
            f.write(str(df2.iloc[0,0:20]))
        # for each in df2.iloc[0,0:30]:
        #     print(each)
        #     print('\n')
    # with open("idf_out.txt", 'w') as f:
    #     f.write(str(df.mean()))
    # print(df.mean())

def analyzeIdfResults():
    with open("idf_out.txt") as f:
        lines = f.read().splitlines()
    dictionary = {}
    for l in lines:
        if 'dtype' in l:
            continue
        split = l.split('    ')
        if(dictionary.has_key(split[0])) and dictionary[split[0]] and split[1]:
            dictionary[split[0]] = float(dictionary[split[0]]) + float(split[1])
        elif split[1]:
            dictionary[split[0]] = float(split[1])
    sort_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    # print(sort_dictionary)
    for k,v in sort_dictionary:
        print(k + '\t' + str(v))


def main():
    # extract descriptions from all
    # inPath = "text_files/found_clusters_results_2020_08_04.txt"
    # (malicious_list,non_malicious_list) = extract_dates(inPath)
    # writeToFiles(malicious_list, 'a')
    # writeToFiles(non_malicious_list, 'b')

    # length comparison between malicious and non malicious
    # descriptionLengthComparison()

    # idf implementation on 3k files (141 malicious)
    # idfImplementNew()
    analyzeIdfResults()


    # previous idf implementation
    # idf_implementation(descriptions_list)
    # with open('idtf_results.txt') as f:
    #     lines = f.read().splitlines()
    # for l in lines:
        
if __name__ == '__main__':
    main()
