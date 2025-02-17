#project_test.py

import nltk
from nltk.tokenize import sent_tokenize
import spacy

textfile = "data/set4/a7.txt"


text = []
with open(textfile, "r") as f:
    for line in f:
        line = line.split('. ')
        if len(line) != 0:
        	temp = line[0].strip('\n')
        	if len(temp) != 0:
       			text.append(temp)

# tokens = []
# for line in text:
# 	token = nltk.pos_tag(line)
# 	tokens.append(token)
# print(tokens[1:10])

# freq_dist = nltk.FreqDist(tokens[0])
# freq_dist.plot()

text1 = str(open(textfile, "rb").read())
newtext = sent_tokenize(text1)

nlp = spacy.load('en_core_web_sm')

NER_tag_dict = dict()
POS_tag_dict = dict()

def tag1(text1):
	tags = []
	doc = nlp(text1)
	for ent in doc.ents:
	# print(ent.text +'-' + ent.label_ + '\n')
		NER_tags.append(ent.text +'-' + ent.label_)
	

def tag2(text):
	for i,line in enumerate(text):
		tags = []
		doc = nlp(str(line))

		for ent in doc.ents:
			# print(ent.text +'-' + ent.label_ + '\n')
			tags.append(ent.text +'-' + ent.label_)
		if len(tags) != 0:
			NER_tag_dict[i] = tags


def pos_tag(text):
	for i,line in enumerate(text):
		tags = []
		doc = nlp(str(line))
		for token in doc:
		    tags.append((token.text, token.pos_, token.tag_, token.dep_, token.is_stop))
		if len(tags) != 0:
			POS_tag_dict[i] = tags


doc1 = nlp("Autonomous cars shift insurance liability toward manufacturers")
for token in doc1:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])

# print(tag2(text))
# pos_tag(text)
# print(POS_tag_dict[1])




