list1 = []
for i in range(1, 4):
    list1.append(i)

list1.append("sdf")

str_list = str(list1)
print(str_list.replace('[','').replace("'sdf'","sdf"))
