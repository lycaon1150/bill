# import class functionall
import functionall
from tika import parser

#global var
limitAccountNo = 5
limitServiceNo = 5
limitLocation = 10

#import pdf
file = 'Pages-from-maxtot10.pdf'

#pdf to text
print("import pdf name : "+file)
file_data = parser.from_file(file)
text = file_data['content']

#check Alian
try:
    s=text.encode('iso-8859-1').decode('tis-620')
    print("string is not UTF-8, length %d bytes" % len(s))
except UnicodeError:
    s=text
    print("string is UTF-8, length %d bytes" % len(s))

#remove whitespace
s = s.replace(",", "")
listData = s.split()

#Using for loop cleanData
count = 0
for i in listData:
    dataClean = (functionall.cleanData(i))
    if dataClean: #not equal ""
        listData[count] = i.replace(dataClean,'')
        listData.insert(count+1,dataClean)
    count +=1


# Using for loop checkType
listType = [None] * len(listData)
count = 0
for i in listData:
    listType[count] = (functionall.checkType(i))
    count += 1


#check AccountNo + ServiceNo + Everything
count = 0
for i in listData:
    if "Account" in listData[count] :
        for i in range(count, count+limitAccountNo):
            if(listType[i]) == 3:
                listType[i] = 11
                #print( listType[i])
                break
    elif "หมายเลข"in listData[count] :
         for i in range(count, count+limitServiceNo):
            if(listType[i]) == 3:
                listType[i] = 22
                #print( listType[i])
                break
    elif listType[count] == 3 and listType[count+1] == 2 and listType[count+2] == 1: #check Location type , and Category Type
        for i in range(count+2,count+2+limitLocation):
            if(listType[i]==3 and listType[i+1]==4 ): 
                if len(listData[i-1]) == 2 and listType[i-1] != 222:
                    listType[i-1] = "222" #type category
                else:
                    listData.insert(i,"NO")
                    listType.insert(i,"222")
                for i in range(count+3,i):
                    listType[i] = "111"  #type Location
                break       
    count += 1

result = functionall.formatCdr(listData,listType,'TOT')

print(len(listData))
print(len(listType))
with open("new.txt", "w", encoding="utf-8") as f:
    f.write(str(result))
    f.close