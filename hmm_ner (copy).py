from sklearn.model_selection import train_test_split
train_data = open('train_3_.txt','r')
train_data_line = train_data.readlines()
train, test = train_test_split(train_data_line, train_size = 0.6,test_size = 0.4)
lexicon_tag_count = dict()
''' how many oo ,bo io etc present'''
lexicon_tag_c = dict()
""" tag count as count o i b"""
"""**************************"""
lexicon_tag_prob = dict()
"""*************************"""
""" final transition  probablity"""
lexical_count=dict()
lexical_tag_count=dict()
lexical_probablity =dict()
"""*****************"""
lexical_prob_table = dict()
"""*****************"""
def transition_count(train):
	for line in train:
		list_ = []
		line = line.strip("\n")
		words = line.split(" ")
		for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			list_.append(i_split[1])
		list_.append("^")
		for j in range(0,len(list_)-1):
			if(list_[j],list_[j+1]) not in lexicon_tag_count:
				lexicon_tag_count[list_[j],list_[j+1]]=1
			else:
				lexicon_tag_count[list_[j],list_[j+1]]=lexicon_tag_count[list_[j],list_[j+1]]+1
	return lexicon_tag_count
# print transition_count(train)
""" it gives the transition probablity i.e number(tag tag)/num tag """
def transition_prob(lexicon):
	for key, value in lexicon.iteritems():
		if key[0] not in lexicon_tag_c:
			lexicon_tag_c[key[0]] = value 
		else:
			lexicon_tag_c[key[0]] = lexicon_tag_c[key[0]]+value
	for key,value in lexicon.iteritems():
		if key not in lexicon_tag_prob:
			lexicon_tag_prob[key]=float(value)/float((lexicon_tag_c[key[0]]))
	return lexicon_tag_prob


# transition_prob(transition_count(train))
""" missing pairs like there can be no BB pair hence they should also be considered"""
def missing_prob():
	# print lexicon
	list1=["B","I","O"]
	# print type(list1)
	list2 =["B","I","0","^"]
	for i in range(len(list1)):
		for j in range(len(list2)):
			pass
			if (list1[i],list2[j]) not in lexicon_tag_prob:
				lexicon_tag_prob[list1[i],list2[j]]=float(0.000001)
	return lexicon_tag_prob
transition_prob(transition_count(train))
missing_prob()

""" now we start with the lexical probablity in the same way"""
def lexic_count(train):
	for line in train:
	
		line = line.strip("\n")
		words = line.split(" ")
		for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			if(i_split[0],i_split[1]) not in lexical_count:
				lexical_count[i_split[0],i_split[1]]=1
			else:
				lexical_count[i_split[0],i_split[1]]=lexical_count[i_split[0],i_split[1]]+1
	return lexical_count
lexic_count(train)
""" finding the y axis for the lexical table so we need all unique words"""
def unique_vocab_training():
	list_=[]
	for key,value in lexical_count.iteritems():
		if key[0] not in list_:
			list_.append(key[0])
	return list_
# print unique_vocab_training(lexic_count(train))
""" all occurrence of the particular tag"""
def count_tag():
	for key,value in lexical_count.iteritems():
		if key[1] not in lexical_tag_count:
			lexical_tag_count[key[1]]=value
		else:
			lexical_tag_count[key[1]]=lexical_tag_count[key[1]]+value
	return lexical_tag_count
count_tag()
# count_tag(lexic_count(train))
# print lexical_tag_count
# print lexical_count
""" it has the probablity of the words with corresponding tag"""
def lexical_prob():
	
	for key,value in lexical_count.iteritems():
		tag=key[1]
		tag_count = lexical_tag_count[tag] 
		lexical_probablity[key]=float(value)/float(tag_count)
	return lexical_probablity
lexical_prob()
""" exi"""
def lexical_table():
	list2=["B","I","O"]
	list1=unique_vocab_training()
	for i in range(len(list1)):
		for j in range(len(list2)):
			if(list1[i],list2[j]) not in lexical_probablity:
				lexical_prob_table[list1[i],list2[j]]=float(0.0000000001)
			else:
				lexical_prob_table[list1[i],list2[j]]=lexical_probablity[list1[i],list2[j]]
	return lexical_prob_table
lexical_table()