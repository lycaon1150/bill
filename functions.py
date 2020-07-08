from tika import parser
from difflib import SequenceMatcher
import re
import constant
import os
from os import listdir

    #accountNo = 11
    #serviceNo = 22
    #Location = 111
    #Category = 222
def checkType(data):
    result = 0
    #Date
    if (re.search("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$", data) or re.search("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}$", data) ):
        result = 1

    #Time
    if (re.search("([0-9]{2}:[0-9]{2}:[0-9]{2})", data)):
        result = 2
        
     #Number
    if (re.search("(^[0-9]*$)", data)):
        result = 3   

     #Float
    if (re.search("[+-]?[0-9]+\.[0-9]+$", data)):
        result = 4  
    
    #Num:Num ex. 01:00
    if (re.search("^([0-9]*[0-9]):([0-9][0-9])$", data)):
        result = 5  

    return result


def cleanData(data):
    result = ""
    if (re.search("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}.+",data)): #ex 27/10/2558BKK
        result = data[10:]
       
    if (re.search("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}.+",data)): #ex 27/10/58BKK
        if not (re.search("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}",data)): #NOT DD/MM/YYYY
            result = data[8:]

    return result

def readPdf(fullpath):
    file = fullpath
    #pdf to text
    print("import pdf name : "+file)
    file_data = parser.from_file(file)
    text = file_data['content']
    return text

def checkUTF8(text):
    try:
        s=text.encode('iso-8859-1').decode('tis-620')
        print("string is not UTF-8, length %d bytes" % len(s))
        return s
    except UnicodeError:
        s=text
        print("string is UTF-8, length %d bytes" % len(s))
        return s

def removeWhiteSpace(text):
    s = text.replace(",", "")
    listData = s.split()
    return listData

def cleanData2(listData):
    count = 0
    for i in listData:
        dataClean = (cleanData(i))
        if dataClean: #not equal ""
            listData[count] = i.replace(dataClean,'')
            listData.insert(count+1,dataClean)
        count +=1
    return listData

def checkType2(listData):
    listType = [None] * len(listData)
    count = 0
    for i in listData:
        listType[count] = (checkType(i))
        count += 1
    return listType

def exportText(result,filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(result))
        f.close

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def changeword(listData):
    for w in range(0,len(listData)):
        percent = 0 
        value = ""
        for l in range(0,len(constant.CHANGEWORD)):
            num= similar(listData[w],constant.CHANGEWORD[l])
            if(num >= 0.6):
                if(num>percent):
                    percent = num
                    value = constant.CHANGEWORD[l]
        if(percent >= 0.8 or (len(value)<=3 and percent >= 0.6)):            
            listData[w] = value
            # print(value)
            # print(listData[w+1])
    return listData



def cleanDataAis(listData): #case 174.24 174.24176:00
    limit =5
    i=0
    loopCount = len(listData)
    # for i in range(0,len(listData)):
    while i < loopCount:
        if "ภายในเครือข่าย" in listData[i] or "นอกเครือข่าย" in listData[i]  :
            # print(listData[i+2])
            for j in range(i,i+limit):
                if(listData[j].find(".") > 0 and listData[j].find(":") > 0):
                    start = listData[j].find(".") + 3 # .00 position
                    dataOld = listData[j]
                    dataColon = dataOld[start:]
                    dataFloat = dataOld[:start]
                    listData[j] = dataFloat
                    listData.insert(j-1,dataColon) 
                    loopCount = loopCount+1
                    # print(listData[j-1])
                    # print(listData[j])
                    # print(listData[j+1])
        i += 1
    return listData

def wordCheck(checkText): #case 699.00เหมาจ่าย = 699.00 เหมาจ่าย
    newText = []

    for i in range(0,len(checkText)):
        a = re.search("(^[+-]?[0-9]+[.][0-9]{2}[a-zก-๙A-Z0-9])", checkText[i])
        b = re.search("([บ][.])", checkText[i])
        c = re.search("([Bb][aA][tT][hH])", checkText[i])
        d = re.search("([บ][า][ท])", checkText[i])
        x = re.search("(^[+-]?[0-9]+[.][0-9]{2})", checkText[i])

        if b != None:
            bb=b.start()
        else:
            bb=999

        if(a != None and bb > len(x.group()) and c == None and d == None):
            # print(x.start(),"  +  " , x.group())
            newText.append('detectError01')
            newText.append(x.group())
            newText.append(checkText[i][len(x.group()):]) 
       
        else:
            newText.append(checkText[i])
            
    return (newText)

def monthtxt(mm):
    switcher = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC"
    }
    return switcher.get(mm, "Please type only (1-12)")

def monthth(mm):
    switcher = {
        "มกราคม": "JAN",
        "กุมภาพันธ์": "FEB",
        "มีนาคม": "MAR",
        "เมษายน": "APR",
        "พฤษภาคม": "MAY",
        "มิถุนายน": "JUN",
        "กรกฎาคม": "JUL",
        "สิงหาคม": "AUG",
        "กันยายน": "SEP",
        "ตุลาคม": "OCT",
        "พฤศจิกายน": "NOV",
        "ธันวาคม": "DEC"
    }
    return switcher.get(mm, "Please type only (month TH)")

def deleteFile(directory):
    file_path = directory
    try:
        os.remove(file_path)
    except OSError as e:
        print("Error: %s : %s" % (file_path, e.strerror))

def deleteFileListDir(directory):
    file_path = directory
    try:
        for file_name in listdir(file_path):
            os.remove(file_path +"\\"+ file_name)
    except OSError as e:
        print("Error: %s : %s" % (file_path, e.strerror))