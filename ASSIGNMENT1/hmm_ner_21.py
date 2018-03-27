from sklearn.model_selection import train_test_split
train_data = open('train_10_.txt','r')
train_data_line = train_data.readlines()
train, test = train_test_split(train_data_line, train_size = 0.7,test_size = 0.3)
test2 = test[0:1]
result_file = open('result_file_10.txt','a')


"""tag_pair_count counts all pair on the list  and transition count counts all the pair"""
tag_pair_count = dict()
tag_pair_prob = dict()
tag_count = dict()
transition = dict()
emission =dict()
word_tag_pair=dict()
start=dict()
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
			if(list_[j],list_[j+1]) not in tag_pair_count:
				tag_pair_count[list_[j],list_[j+1]]=1
			else:
				tag_pair_count[list_[j],list_[j+1]]=tag_pair_count[list_[j],list_[j+1]]+1
	return tag_pair_count
# print tag_pair_count

""" divide tag pair with the probablity of the tag """
def transition_prob(lexicon):
	for key, value in lexicon.iteritems():
		if key[0] not in tag_count:
			tag_count[key[0]] = value 
		else:
			tag_count[key[0]] = tag_count[key[0]]+value
	for key,value in lexicon.iteritems():
		if key not in tag_pair_prob:
			tag_pair_prob[key]=float(value)/float((tag_count[key[0]]))
	return tag_pair_prob
""" it is used to find the unique tag and unique vocabulary so that nothing is hardcoded"""
def find_unique_tag(train):
	states = []
	for line in train:
		line = line.strip("\n")
		words = line.split(" ")
		for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			if i_split[1] not in states:
				states.append(i_split[1])
	return states


def missing_prob(lexicon,list1,list2):
	for i in range(len(list1)):
		for j in range(len(list2)):
			if (list1[i],list2[j]) not in lexicon:
				transition[list1[i],list2[j]]=float(0.000001)
			else:
				transition[list1[i],list2[j]]=float(lexicon[list1[i],list2[j]])
	return transition

def calculate_transition_table():
	transition_count(train)
	transition_prob(tag_pair_count)
	states=find_unique_tag(train_data_line)
	transition=missing_prob(tag_pair_prob,states,states)
	# print transition


def word_tag_count(train):
	for line in train:
		line = line.strip("\n")
		words = line.split(" ")
		for i in range(0,len(words)-1):
			i_split = words[i].split("^")
			if(i_split[0],i_split[1]) not in word_tag_pair:
				word_tag_pair[i_split[0],i_split[1]]=1
			else:
				word_tag_pair[i_split[0],i_split[1]]=word_tag_pair[i_split[0],i_split[1]]+1
	return word_tag_pair

def word_tag_prob_fn(lexicon):
	for key,value in lexicon.iteritems():
		word_tag_pair[key]=float(value)/float(tag_count[key[1]])
	return word_tag_pair
def unique_vocab_training(lexicon):
	list_=[]
	for key,value in lexicon.iteritems():
		if key[0] not in list_:
			list_.append(key[0])
	return list_


def emission_table():
	list2=find_unique_tag(train_data_line)
	list1=unique_vocab_training(word_tag_pair)
	for i in range(len(list1)):
		for j in range(len(list2)):
			if(list1[i],list2[j]) not in word_tag_pair:
				emission[list1[i],list2[j]]=float(0.00001)
			else:
				emission[list1[i],list2[j]]=word_tag_pair[list1[i],list2[j]]
	return emission
def calculate_emission_probablity():
	word_tag_count(train)
	word_tag_prob_fn(word_tag_pair)
	emission_table()
states=find_unique_tag(train_data_line)
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
def round_prob_5_digit(transition,emission):
	for key,value in transition.iteritems():
		transition[key]=round(value,7)
	for key,value in emission.iteritems():
		emission[key] = round(value,7)
	return transition,emission
""" final 2 function"""
calculate_transition_table()
calculate_emission_probablity()
round_prob_5_digit(transition,emission)
calculate_start_prob(train,states)
print start
def write_file(wordlist,taglist,opt):
	for i in range(len(wordlist)):
		string=wordlist[i]+"\t"+taglist[i]+"\t"+opt[i]
		print string
		result_file.write(string)
		result_file.write("\n")
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
		return (float(0.00001))
	else:
		if(emission[word,tag])>float(0.0):
			return round(emission[word,tag],7)
		else:
			return float(0.00001)


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