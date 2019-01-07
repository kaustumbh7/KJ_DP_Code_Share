import pickle 

with open ('ner_data_corpus_260', 'rb') as fp:
    itemlist = pickle.load(fp)

print(itemlist[0])