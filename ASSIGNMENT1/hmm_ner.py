from sklearn.model_selection import train_test_split
train_data = open('train_3_.txt','r')
train_data_line = train_data.readlines()
train, test = train_test_split(train_data_line, train_size = 0.6,test_size = 0.4)
test2 = test[0:1]
print test2
result_file = open('result_file.txt','a')
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
transition = dict()
emission = dict()
start = dict()
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
	list2 =["B","I","O","^"]
	for i in range(len(list1)):
		for j in range(len(list2)):
			pass
			if (list1[i],list2[j]) not in lexicon_tag_prob:
				lexicon_tag_prob[list1[i],list2[j]]=float(0.00001)
	return lexicon_tag_prob


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

""" exi"""
def lexical_table():
	list2=["B","I","O"]
	list1=unique_vocab_training()
	for i in range(len(list1)):
		for j in range(len(list2)):
			if(list1[i],list2[j]) not in lexical_probablity:
				lexical_prob_table[list1[i],list2[j]]=float(0.0)
			else:
				lexical_prob_table[list1[i],list2[j]]=lexical_probablity[list1[i],list2[j]]
	return lexical_prob_table


states=('B','I','O')
def calculate_start_prob(train,states):
	count =0
	for line in train:
		count = count+1
		line = line.strip("\n")
		words = line.split(" ")
		i_split = words[0].split("^")
		if (i_split[1]) not in start:
			start[i_split[1]]=1
		else:
			start[i_split[1]]=start[i_split[1]]+1
	for key,value in start.iteritems():
		start[key]=float(value)/float(count)
	for i in range(len(states)):
		if (states[i]) not in start:
			start[states[i]]=0.000001
	return start
def calculate_transmision_emission_start():
	transition_prob(transition_count(train))
	transition=missing_prob()
	# print transition
	count_tag()
	lexical_prob()
	emission=lexical_table()
	# print emission
	calculate_start_prob(train,states)
	return transition,emission
def seperate_tag_word(line):
	wordlist=[]
	taglist=[]
	line = line.strip("\n")
	words = line.split(" ")
	for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			wordlist.append(i_split[0])
			taglist.append(i_split[1])
	return wordlist,taglist
def emission_prob(emission,word,tag):
	# print emission
	if(word,tag) not in emission:
		return (float(0.0001))
	else:
		if(emission[word,tag])>float(0.0):
			return round(emission[word,tag],5)
		else:
			return float(0.00001)

	


def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%f: " % state + " ".join("%f" % ("%f" % v[state]["prob"]) for v in V)
def round_prob_5_digit(transition,emission):
	for key,value in transition.iteritems():
		transition[key]=round(value,7)
	for key,value in emission.iteritems():
		emission[key] = round(value,5)
	return transition,emission
def transition_prob_value(transition,prev_st,st):
	if (prev_st,st) not in transition:
		return float(0.0001)
	else:
		return transition[prev_st,st]
# def write_file(wordlist,taglist,opt):


transition,emission=calculate_transmision_emission_start()
def write_file(wordlist,taglist,opt):
	for i in range(len(wordlist)):
		string=wordlist[i]+"\t"+taglist[i]+"\t"+opt[i]
		print string
		result_file.write(string)
		result_file.write("\n")

def viterbi(test,states,emission,transition,start):
	# print transition
	V = [{}]
	count =0
	for line in test:
		V = [{}]
		count = count + 1
		wordlist,taglist=seperate_tag_word(line)
		for st in states:
			value =float(emission_prob(emission,wordlist[0],st))
			V[0][st] = {"prob": start[st] * value, "prev": None}
		for t in range(1, len(wordlist)):
			V.append({})
			for st in states:
				max_tr_prob = max(V[t-1][prev_st]["prob"]*transition[prev_st,st] for prev_st in states)
				for prev_st in states:
					if V[t-1][prev_st]["prob"] * transition[prev_st,st] == max_tr_prob:
						value =float(emission_prob(emission,wordlist[t],st))
						max_prob = max_tr_prob * value
						V[t][st] = {"prob": max_prob, "prev": prev_st}
						break

		opt = []
		max_prob = max(value["prob"] for value in V[-1].values())
		previous = None
		print max_prob
		for st, data in V[-1].items():
			if data["prob"] == max_prob:
				opt.append(st)
				previous = st
				break
		for t in range(len(V) - 2, -1, -1):
			opt.insert(0, V[t + 1][previous]["prev"])
			previous = V[t + 1][previous]["prev"]
		print opt
		print len(opt)
		print len(wordlist)
		print len(taglist)
		write_file(wordlist,taglist,opt)


viterbi(test,states,emission,transition,start)
