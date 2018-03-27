
from sklearn.model_selection import train_test_split
train_data = open('train_3.txt','r')
train_data_line = train_data.readlines()
print train_data_line
print type(train_data_line)
train, test = train_test_split(train_data_line, train_size = 0.6,test_size = 0.4)
print len(train)
print len(test)