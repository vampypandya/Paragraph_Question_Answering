import os
import sys
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import nltk.tag.stanford as st
import os.path
from sklearn.feature_extraction.text import TfidfVectorizer

tagger = st.StanfordNERTagger('Dependency/english.muc.7class.distsim.crf.ser.gz','Dependency/stanford-ner.jar')

fil=sys.argv[1]
det=open(fil,'r').read()
vectorizer = TfidfVectorizer(stop_words='english')



def cosine_sim(text1, text2):
    #print text1,text2
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def findSimilarity(sentences,question):
    cos_scores=[]
    for sentence in sentences:
        cos_scores.append(cosine_sim(question,sentence))
    max_cos=max(cos_scores)
    cos_index=cos_scores.index(max_cos)
    req_sent=sentences[cos_index]
    an_file=open('input_answer.txt','w')
    an_file.write(req_sent)
    an_file.close()
    qq=os.popen("java -mx600m -cp '*:lib/*' edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier Dependency/english.muc.7class.distsim.crf.+ser.gz -textFile input_answer.txt -outputFormat slashTags 2> /dev/null").read()
    
    
    arr=str(qq).split(" ")
    del arr[-1]
    
	
    ar=[]
    for tt in arr:
        wt=tt.split("/")
        ar.append([wt[0],wt[1]])
 	#print question.split(" ")[0]
    if(question.split(" ")[0]=='When'):
        for aa in ar:
            if(aa[1]=="DATE" or aa[1]=="TIME"):
                aw=aa[0]
                print "Required duration is",aw
                break
    elif(question.split(" ")[0]=='Where'):
        for aa in ar:
            #print "asd",ar
            if(aa[1]=='LOCATION'):
                aw=aa[0]
                print "Required location is",aw
                break
    elif(question.split(" ")[0]=='How' and question[4]=='m'):
        for aa in ar:
            if(aa[1]=='MONEY' or aa[1]=='PERCENT'):
                aw=aa[0]
                print "Required value is",aw
                break
    else:
		print req_sent

	
	
    
	
path = '/opt/lampp/htdocs/yutzii/nayawala.txt' 
if os.path.exists(path) == []: 
    fils="default.txt"
else: 
    fils="nayawala.txt"
    
para=open(fils,'r').read()
listy=[]
for line in sent_tokenize(para):
	listy.append(line)
	
findSimilarity(listy,det)

