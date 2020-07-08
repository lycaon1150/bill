import re
import constant
#global var
limitAccountNo = 5
limitServiceNo = 3
limitLocation = 10

def tot(listData,listType):
    count = 0
    for i in listData:
        try:
            if "Account" in listData[count] :
                for i in range(count, count+limitAccountNo):
                    if(listType[i]) == 3:
                        listType[i] = 11
                        #print( listType[i])
                        break
            elif "หมายเลข"in listData[count] :
                for i in range(count, count+limitServiceNo):
                    if(listType[i]) == 3 or (re.search("^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{8,}$", listData[i])): #ex 02286A430
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
        except IndexError:
            pass   
        count += 1
    return listData,listType #return 2 type



def ais(listData,listType):
    stage1=0
    stage2=0
    stage1Pos = 0
    stage2Pos = 0
    count = 0
    for i in listData:
        if("เลขที่ลูกค้า" in i):
            for i in range(count, count+limitAccountNo):
                if(listType[i]) == 3:
                    listType[i] = 11
                    break
        elif("หมายเลขโทรศัพท์" in i or "หมายเลขผู้ใช้อินเทอร์เน็ต" in i):
            for i in range(count, count+limitServiceNo):
                if(listType[i]) == 3: 
                    listType[i] = 22
                    break
        if(listType[count] == 1 and listType[count+1] == 2 and listType[count+2] == 3):
            stage1=1
            stage1Pos = count+3
            # print(str(listData[count]) + " "+str(listData[count+1])+ " "+str(listData[count+2]))
            if(stage1==1):
                for j in range(stage1Pos,stage1Pos+limitLocation):
                    if((listType[j] == 5 or listType[j]==3) and listType[j+1] == 4 and listType[j+2] == 4):
                        if(listType[j]==3):
                            listType[j]=5
                        stage2=1
                        stage2Pos = j
                        # print(str(listData[j]) + " "+str(listData[j+1])+ " "+str(listData[j+2]))
                        break
                if(stage1==1 and stage2==1):
                    for i in range(stage1Pos,stage2Pos):
                        if ' '.join(listData[stage1Pos:i+1])in constant.PROVIDER:
                            for k in range(stage1Pos,i+1):
                                listType[k] = 33  #ต้นทาง
                            break
                        elif ' '.join(listData[stage1Pos+1:i+1])in constant.PROVIDER:
                            for k in range(stage1Pos+1,i+1):
                                listType[k] = 33  #ต้นทาง
                            break   
                   
                    
                    if(listData[stage1Pos] == listData[stage1Pos+1] and listData[stage1Pos] == listData[stage1Pos+2] ):
                            listType[stage1Pos+1] = 33
                            

                    if(listType[stage1Pos] == 33 and listType[stage1Pos-1]==3 ):
                            # print(listData[stage1Pos])
                            listData.insert(stage1Pos,"NO")
                            listType.insert(stage1Pos,0)

                stage2=0
                stage1=0
                stage1Pos=0
                stage2Pos=0
       
        count += 1
    return listData,listType 

def true(listData,listType):
    for i in range(0,len(listData)):
        if "รหัสลูกค้า" == listData[i]:
            for j in range(i, i+limitServiceNo):
                if(listType[j]) == 3: 
                    listType[j] = 11
                    break
        #02/01/2562-02/01/2562
        if (re.search("^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}-([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$", listData[i])):
            listType[i] = 111
    return listData,listType 

