# file = open('pos.txt','r')
# outfile = open('pos_file.txt','a')
# lines = file.readlines()
# # print lines
# for li in lines:
# 	string=""
# 	line = li.strip("\n")
# 	words = line.split(" ")
# 	for i in range(0,len(words)):
# 		i_split = words[i].split("_")
# 		string=string+i_split[0]+"_"+i_split[1]+" "
# 	print string
# 	outfile.write(string)
# 	outfile.write("\n")
file1=open('pos_file.txt','r')
lines =file1.readlines()
print lines


