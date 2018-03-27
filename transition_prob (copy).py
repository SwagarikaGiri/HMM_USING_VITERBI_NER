from sklearn.model_selection import train_test_split
train_data = open('train_3_.txt','r')
train_data_line = train_data.readlines()
train, test = train_test_split(train_data_line, train_size = 0.6,test_size = 0.4)
""" lexixon has"""
lexicon_tag_count = dict()
lexicon_tag_c = dict()
lexicon_tag_prob = dict()
lexical_count=dict()
""" transition count gives number of tag-tag pair"""
def transition_count(train):
	for line in train:
		list_ = []
		line = line.strip("\n")
		print line
		words = line.split(" ")
		for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			list_.append(i_split[1])
		list_.append("^")
		print list_
		for j in range(0,len(list_)-1):
			print list_[j],list_[j+1]
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
	print lexicon_tag_c
	for key,value in lexicon.iteritems():
		if key not in lexicon_tag_prob:
			lexicon_tag_prob[key]=float(value)/float((lexicon_tag_c[key[0]]))
	return lexicon_tag_prob


# transition_prob(transition_count(train))
""" missing pairs like there can be no BB pair hence they should also be considered"""
def missing_prob(lexicon):
	# print lexicon
	list1=["B","I","O"]
	# print type(list1)
	list2 =["B","I","0","^"]
	for i in range(len(list1)):
		for j in range(len(list2)):
			pass
			if (list1[i],list2[j]) not in lexicon:
				lexicon[list1[i],list2[j]]=float(0.000001)
	return lexicon
# print missing_prob(transition_prob(transition_count(train)))
""" now we start with the lexical probablity in the same way"""
def lexical_count(train):
	for line in train:
		list_ = []
		line = line.strip("\n")
		print line
		words = line.split(" ")
		for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			if(i_split[0],i_split[1]) not in lexical_count:
				lexical_count[i_split[0],i_split[1]=1
			else:
				lexical_count[i_split[0],i_split[1]=lexical_count[i_split[0],i_split[1]+1
	return lexical_count
lexical_count(train)

			