# import regular expresstion
import re
import functions
def formatCdr(data,type,filename,provider):
    stage1=0
    stage2=0
    # stage3=0
    stage4=0
    stage1Pos = 0
    stage2Pos = 0
    stage3Pos = 0
    stage4Pos = 0
    result=[]
    dataStage1 =""
    dataStage2 =""
    dataStage3 =""
    dataStage4 =""
    accountNo ="xx"
    serviceNo =""
    limitLoop =10
    limitLoopStage1 =8
    if provider == 'TOT':
        for i in range(0,len(data)):
            try:
                if(type[i] == 11 and not accountNo):
                    accountNo = data[i]
                if(type[i]== 22):
                    serviceNo=data[i]
                if type[i] == 3 and type[i+1] ==2 and type[i+2] ==1 :
                    stage1 = 1 
                    stage1Pos = i
                    dataStage1 = '\t'.join(data[stage1Pos:stage1Pos+3])
                if stage1 == 1:   
                    for j in range(stage1Pos+2,stage1Pos+2+limitLoopStage1):
                        if(type[j]==3 and type[j+1]==4):
                            stage2=1
                            stage2Pos=j
                            dataStage2 = '\t'.join(data[stage2Pos-1:stage2Pos+2])
                            break
                        if stage1 == 1 and stage2 == 1 :
                            location = ""
                            for k in range(stage1Pos+2,stage2Pos): #checkType Location key =111
                                if type[k] == "111":
                                    location = location+" "+data[k]
                            my_lst_str = accountNo +"\t"+ serviceNo+"\t"+filename +"\t"+ dataStage1 +"\t"+ location+"\t" + dataStage2 #concat 2 stage and location
                            result.append(my_lst_str)
                            stage1Pos=0
                            stage2Pos=0
                            stage2=0
                            stage1=0
                            break
            except IndexError:
                pass
        return "\n".join(result)

    elif provider == 'AIS':
        filenameSplit = filename.split('_') 
        billCycle=""
        for i in range(0,len(data)):
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
                # print(accountNo)
            if(type[i]== 22):
                serviceNo=data[i]
                # print(serviceNo)
            elif(len(filenameSplit) == 4):
                serviceNo = filenameSplit[2]
                monthYear = filenameSplit[3]
                billCycle = functions.monthtxt(monthYear[:2]) + '_20' + monthYear[2:]
            if type[i] == 1 and type[i+1] ==2 and type[i+2] ==3 and type[i+3] == 0 :
                stage1Pos = i
                dataStage1 = '\t'.join(data[stage1Pos:stage1Pos+4])
                stage2pos = stage1Pos+4
                stage1 = 1
                # print(dataStage1)
                if(stage1 == 1):
                    for j in range(stage1Pos+4,stage1Pos+4+limitLoop):
                        if type[j] != 33 :
                            dataStage2 = ' '.join(data[stage2pos:j])
                            stage2=1
                            stage3Pos = j
                            # print(dataStage2)
                            break
                if(stage1==1 and stage2==1):
                    for k in range(stage3Pos,stage3Pos+limitLoop):
                        if(type[k] == 5 and type[k+1] == 4 and type[k+2] == 4):
                            dataStage4 = '\t'.join(data[k:k+3])
                            stage4=1
                            stage4Pos = k
                            # print(dataStage4)
                            break
                if(stage1==1 and stage2==1 and stage4==1):
                    dataStage3 = ' '.join(data[stage3Pos:stage4Pos])
                    # print(dataStage3)
                
                my_lst_str = accountNo +"\t"+ serviceNo+"\t"+billCycle+"\t"+filename+"\t"+ dataStage1 +"\t"+ dataStage2+"\t" + dataStage3 +"\t" + dataStage4 
                result.append(my_lst_str)
                stage1=0
                stage2=0
                stage4=0
                stage1Pos=0
                stage2pos=0
                stage3Pos=0
                stage4Pos=0
                # stage3=0
        result.append("")        
        return "\n".join(result)
   

def formatInventory(data,type,filename,provider):
    result=[]
    accountNo =""
    stage1 = 0
    billcycleFlag = 0
    startBill = ""
    endBill = ""
    no = 0 #no ServiceNo for check
    serviceNo=""
    companyName=""
    limitLoop =10
    stage1Pos= 0
    flagInternet = False
    flagDetectError = False
    if provider == 'TOT':
        for i in range(0,len(data)):    
            if("รอบค่าใช้บริการ" in data[i] or billcycleFlag == 1):
                billcycleFlag = 1
                if(type[i]==1):
                    startBill = data[i]
                    endBill = data[i+2]
                    billcycleFlag = 0
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
            if(type[i]== 22):
                no = data[i-2]
                for j in range(i,len(data)):
                    stage1 =j
                    if("โปรโมชั่น" in data[j]):
                        print("case : โปรโมชั่น")
                    elif("ค่า" in data[j]):
                        listStr1 = accountNo +"\t"+  data[i] +"\t"+filename+"\t"+ startBill +"\t"+ endBill +"\t"+ ' '.join(data[i+1:j])
                        for k in range(j,len(data)):
                            if(type[k]==4):
                                    typeOfService = ' '.join(data[stage1:k])
                                    amount = data[k]
                                    quantity = re.findall('\([0-9a-zA-Zก-๙\s^\)]+\)', typeOfService ) #ex. (1 ครั้ง)
                                    quantity = re.findall('\d+', str(quantity))
                                    if(len(quantity)>0):
                                        quantity = quantity[0]
                                    else:
                                        quantity = 1
                                    
                                    if(typeOfService.find("(")>0):
                                        print(typeOfService[:(typeOfService.find("("))])
                                        typeOfService = typeOfService[:(typeOfService.find("("))]
                                    listStr2 = no +"\t"+ typeOfService +"\t"+  str(quantity) +"\t"+ str(amount)
                                    result.append(listStr1+"\t"+listStr2)
                                    # print(listStr1+"\t"+listStr2)
                                    stage1 = k+1
                            if("รวม" in data[k]): #หยุดเมื่อเจอ รวม
                                break
                        break
        return "\n".join(result)
    elif provider == 'AIS':
        print("AIS")
        for i in range(0,len(data)):   
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
            if(type[i] == 22):
                serviceNo = data[i]
                # print(serviceNo)
            if(type[i]==1 and not startBill and not endBill):
                if(re.search('^-([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$',data[i+1])):
                   startBill = data[i]
                   endBill = data[i+1].replace('-', '') 
            if("ค่าบริการที่เรียกเก็บ" in data[i] and "Current" in data[i+1] and "จำนวนเงิน:" in data[i+3]):
                print("##################################")
                print(" ")
                stage1Pos = i+5
                listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ startBill +"\t"+ endBill
                for j in range(i+5,len(data)):
                    if "(ต่อ)" in data[j] and "จำนวนเงิน:" in data[j+1]:
                        print("HIIIIIIIIIIIIIIIIIIIIIII  "+data[j+3])
                        stage1Pos = j+3
                    if(type[j]==4 or re.search("\([+-]?\d+\.[0-9]*\)",data[j])): #(1.00)
                        if(type[j-1]==3 or type[j-1]==4): #case มีจำนวนครั้งกับราคา
                            print(" ")
                            print("11111111111111111111111111111")
                            # print(' '.join(data[stage1Pos:j-1]))
                            # print(data[j-1])
                            # print(data[j])
                            typeOfService=' '.join(data[stage1Pos:j-1])
                            quantity=data[j-1]
                            amount = data[j]
                            if(re.search("\([+-]?\d+\.[0-9]*\)",amount)):
                                    amount = amount.replace("(", "-")
                                    amount = amount.replace(")", "")
                            listStr2 =  typeOfService +"\t"+  str(quantity) +"\t"+ str(amount)
                            # print(listStr2)
                            result.append(listStr1+"\t"+ listStr2)
                            stage1Pos=j+1
                        elif type[j+1]==4:
                            pass
                        else:
                            print(" ")
                            print("222222222222222222222222222222")
                            mb=0
                            kb=0
                            for k in range(stage1Pos,j):
                                if("Internet" in data[k] and type[k+1] == 3):
                                    stage1Pos=k
                                    for l in range(k+1,j):
                                        if "MB" in data[l]:
                                            mb = data[l-1]
                                        elif "KB" in data[l]:
                                            kb = data[l-1]
                                            break
                                    flagInternet = True
                                elif("detectError01" in data[k]):
                                    flagDetectError = True
                            if flagDetectError is True :
                                # print("GU TRUE ERROR")
                                # print(data[stage1Pos]) #คาบริการตามโปรโมชั่น
                                # print(data[j]) #899.00
                                for l in range(j+1,len(data)):
                                    if "ค่าโทรส่วนเกินโปรโมชั่น" in data[l] or "รวม" in data[l] or "detectError01" in data[l] or "ค่าใช้บริการที่เรียกเก็บ" in data[l] :
                                        typeOfService = ' '.join(data[j+1:l])
                                        print(typeOfService)
                                        stage1Pos=l
                                        break
                                    elif "Internet" in data[l]:
                                        typeOfService = ' '.join(data[j+1:l-1])
                                        print(typeOfService)
                                        stage1Pos=l-1
                                        break
                                quantity = 1 
                                amount = data[j]
                                listStr2 =  typeOfService +"\t"+  str(quantity) +"\t"+ str(amount)
                                flagDetectError = False
                            elif flagInternet is False:
                                    # print(' '.join(data[stage1Pos:j]))
                                typeOfService = ' '.join(data[stage1Pos:j])
                                quantity = 1 
                                amount = data[j]
                                if(re.search("\([+-]?\d+\.[0-9]*\)",amount)):
                                    amount = amount.replace("(", "-")
                                    amount = amount.replace(")", "")
                                listStr2 =  typeOfService +"\t"+  str(quantity) +"\t"+ str(amount)
                                # print(listStr2)
                                stage1Pos=j+1
                            else :
                                print("INTERNET TRUEEEEEEEEEEEEE")
                                print(data[stage1Pos])
                                typeOfService = data[stage1Pos] #ONLY Internet
                                # typeOfService = ' '.join(data[stage1Pos:j])
                                quantity = ((int(mb)*1000)+int(kb))/1000
                                amount = data[j]
                                if(re.search("\([+-]?\d+\.[0-9]*\)",amount)):
                                    amount = amount.replace("(", "-")
                                    amount = amount.replace(")", "")
                                listStr2 =  typeOfService +"\t"+  str(quantity) +"\t"+ str(amount)
                                # print(listStr2)
                                stage1Pos=j+1
                            result.append(listStr1+"\t"+ listStr2)
                            flagInternet = False
                    if(type[j] == 22 or data[j]== "รายการโทรออกในต่างประเทศ" or data[j]=="ค่าบริการที่เรียกเก็บ" or "รวม" in data[j]): #เจอเบอร์ต่อไปหยุด #ดักเคสข้ามแดน
                        break
        result.append("")
        return "\n".join(result)
           
def formatUsage(data,type,filename,provider):
    result=[]
    resultInternet=[]
    accountNo=""
    serviceNo=""
    startBill = ""
    endBill = ""
    stageServiceNo= 0
    stage1Pos = 0
    if provider == 'AIS':
        for i in range(0,len(data)):   
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
            if(type[i]==1 and not startBill and not endBill):
                if(re.search('^-([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$',data[i+1])):
                   startBill = data[i]
                   endBill = data[i+1].replace('-', '') 
            if(type[i] == 22):
                # print(serviceNo)
                serviceNo = data[i]
                stageServiceNo = i
            if("ข้อมูลการใช้บริการโทรศัพท์" == data[i] and stageServiceNo > 0): #call usage
                listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ startBill +"\t"+ endBill
                # print(data[i])
                mb=0
                kb=0
                for j in range(i,len(data)):
                    if("(บาท)" in data[j]):
                        stage1Pos = j+1
                    if(type[j] == 5 ): #colon
                        for k in range(j+1,len(data)):
                            if(type[k]==4):
                                for l in range(k+1,len(data)):
                                    if(type[l]==4):
                                        typeOfService = ' '.join(data[stage1Pos:l-2])
                                        time = data[l-2]
                                        realUse = data[l-1] 
                                        amount = data[l]
                                        listStr2 =  typeOfService +"\t"+  str(time) +"\t"+ str(realUse)+"\t"+ str(amount)
                                        # print(listStr1+"\t"+ listStr2)
                                        stage1Pos=l+1
                                        result.append(listStr1+"\t"+ listStr2)
                                        break
                                    else:
                                        break
                            else:
                                break            
                    elif(type[j]==4): #float
                        if(type[j-1]!=5 and type[j-1]!=4):
                            # print("งง")
                            typeOfService = ' '.join(data[stage1Pos:j])
                            time = "xx"
                            realUse = data[j]
                            amount = "xx"
                            listStr2 =  typeOfService +"\t"+  str(time) +"\t"+ str(realUse)+"\t"+ str(amount)
                            # print(listStr1+"\t"+ listStr2)
                            result.append(listStr1+"\t"+ listStr2)
                            stage1Pos=j+1
                    elif("Internet" in data[j] and type[j+1] == 3):
                        # print("INTERNET IS HERE")
                        stage1Pos=j
                        for k in range(j+1,len(data)):
                            if "MB" in data[k]:
                                mb = data[k-1]
                            elif "KB" in data[k]:
                                kb = data[k-1]
                                amount = data[k+1]
                                break
                        typeOfService = data[stage1Pos] #ONLY Internet
                        realUse = ((int(mb)*1000)+int(kb))/1000
                        # amount = data[j]
                        amount = 0 if amount == '-'  else amount
                        listStr2 =  typeOfService +"\t"+  str(realUse) +"\t"+ str(amount)
                        # print(listStr1+"\t"+ listStr2)
                        resultInternet.append(listStr1+"\t"+ listStr2)
                        stage1Pos=j+1
                    if("รวม" in data[j] ): #เจอเบอร์ต่อไปหยุด 
                        break
            elif ("ข้อมูลการใช้บริการโทรศัพท์ที่ใช้จริง" == data[i] and stageServiceNo > 0): #actual usage:
                listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ startBill +"\t"+ endBill
                print(data[i])
                for j in range(i,len(data)):
                    if("นาที:วินาที" in data[j]):
                        stage1Pos = j+1
                    if("บาท" in data[j]):
                        stage1Pos = j+1
                    if(type[j] == 5 ): #colon
                        for k in range(j+1,len(data)):
                            if(type[k]==4):
                                typeOfService = ' '.join(data[stage1Pos:k-1])
                                time = data[k-1]
                                realUse = data[k] 
                                amount = "xx"
                                listStr2 =  typeOfService +"\t"+  str(time) +"\t"+ str(realUse)+"\t"+ str(amount)
                                # print(listStr1+"\t"+ listStr2)
                                stage1Pos=k+1
                                result.append(listStr1+"\t"+ listStr2)
                                break
                            else:
                                print("ONLY COLON")
                                typeOfService = ' '.join(data[stage1Pos:k-1])
                                time = data[k-1]
                                realUse = "xx"
                                amount = "xx"
                                listStr2 =  typeOfService +"\t"+  str(time) +"\t"+ str(realUse)+"\t"+ str(amount)
                                print(listStr1+"\t"+ listStr2)
                                stage1Pos=k+1
                                result.append(listStr1+"\t"+ listStr2)
                                break
                    elif(type[j]==4): #float
                        if(type[j-1]!=5 ):
                            typeOfService = ' '.join(data[stage1Pos:j])
                            time = "xx"
                            realUse = data[j]
                            amount = "xx"
                            listStr2 =  typeOfService +"\t"+  str(time) +"\t"+ str(realUse)+"\t"+ str(amount)
                            # print(listStr1+"\t"+ listStr2)
                            result.append(listStr1+"\t"+ listStr2)
                            stage1Pos=j+1
                    elif("Internet" in data[j] and type[j+1] == 3):
                        stage1Pos=j
                        mb=0
                        kb=0
                        for k in range(j+1,len(data)):
                            if "MB" in data[k]:
                                mb = data[k-1]
                            elif "KB" in data[k]:
                                kb = data[k-1]
                                amount = data[k+1]
                                break
                        typeOfService = data[stage1Pos] #ONLY Internet
                        realUse = ((int(mb)*1000)+int(kb))/1000
                        # amount = data[j]
                        amount = 0 if amount == '-'  else amount
                        listStr2 =  typeOfService +"\t"+  str(realUse) +"\t"+ str(amount)
                        # print(listStr1+"\t"+ listStr2)
                        resultInternet.append(listStr1+"\t"+ listStr2)
                        stage1Pos=j+1

                    if("รวม" in data[j] ): #เจอเบอร์ต่อไปหยุด 
                        break
    result.append("")
    resultInternet.append("")                        
    return "\n".join(result) , "\n".join(resultInternet)

    """
            if(("ข้อมูลการใช้บริการโทรศัพท์" == data[i] or "ข้อมูลการใช้บริการโทรศัพท์ที่ใช้จริง" == data[i]) and stageServiceNo > 0):
                print(serviceNo)
                for j in range(i,len(data)):
                    # print(data[j])
                    if("บาท" == data[j]): #case  Actual Usage
                        stagePos1 = j+1
                        print("IN STAGE 2 =========================")
                    elif("(บาท)" in data[j] and "(บาท)" in data[j+1] ): #case  Call Usage
                        stagePos1 = j+2
                        print("IN STAGE 1 =========================")
                        
                    if(type[j]==5 and type[j+1]==4 and type[j+2]==4):
                        print("THREE")
                        typeOfService=' '.join(data[stagePos1:j])
                        print(typeOfService)
                        stagePos1=j+3
                        # print(data[j] + " " + data[j+1] +" "+ data[j+2])
                    elif(type[j]==5 and type[j+1]==4):
                        print("TWO")
                        # print(data[j] + " " + data[j+1])
                    elif(type[j-1]==0 and type[j]==4 and type[j+1]==0 ):
                        print("ONE")
                        typeOfService=' '.join(data[stagePos1:j])
                        print(typeOfService)
                        stagePos1=j+2
                        # print(data[j])
                    elif("Internet" in data[j] and type[j+1] == 3):
                       print("INTERNET")
                       print(data[j])
                    if("รวม" in data[j] ): #เจอเบอร์ต่อไปหยุด 
                        break
                 print("####################")

                """
               
def formatPromotion(data,type,filename,provider):  
    accountNo=""
    serviceNo=""
    startBill = ""
    endBill = ""
    stageServiceNo= 0   
    result=[]
    billCycle=""
    stage1Pos = 0
    stage2Pos = 0
    promotion = ""
    print("FUCKING PROMOTION")  
    if provider == 'AIS':
        for i in range(0,len(data)):   
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
            if(type[i]==1 and not startBill and not endBill):
                if(re.search('^-([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$',data[i+1])):
                   startBill = data[i]
                   endBill = data[i+1].replace('-', '') 
            if(type[i] == 22):
                print(serviceNo)
                serviceNo = data[i]
                stageServiceNo = i   
            if("แพ็กเกจของคุณ" in data[i] and stageServiceNo > 0):
                stage1Pos = i+3
                for j in range(stage1Pos,len(data)):
                    if "(ต่อ)" in data[j]:
                        stage1Pos = j+1
                    if("สิ้นสุดวันที่" in data[j]):
                        # print(data[j])
                        listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ startBill +"\t"+ endBill
                        promotion = ' '.join(data[stage1Pos:j])
                        # print(listStr1)
                        # print(promotion)
                        if(type[j+1] == 1):
                            # print(' '.join(data[j:j+3]))
                            # print(data[j+1])
                            # print("AAAAAAAAAAAAAAAAAAAAAAAA")
                            stage1Pos = j+3
                            listStr2 =  promotion +"\t"+  data[j+1]
                            # print(listStr1+"\t"+ listStr2)
                            result.append(listStr1+"\t"+ listStr2)
                    # if(type[j]==1):
                        # print(''.join(data[stage1Pos:j+2]))
                        # stage1Pos = j+2
                    if(type[j] == 22 or "รวม" in data[j]): #เจอเบอร์ต่อไปหยุด #ดักเคสข้ามแดน
                        # print("##################################################################")
                        break
        result.append("")
        return "\n".join(result) 
    elif provider == 'TRUE':
        print("FUCKING PROMOTION TRUE")  
        for i in range(0,len(data)):
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
                # print(accountNo)
                # print(filename)
            if data[i] == "หมายเลขโทรศัพท์":
                if type[i+1] == 3 and type[i+2] == 3 and type[i+1] == 3:     
                    serviceNo = ''.join(data[i+1:i+4])
                    # print(serviceNo)
                elif type[i+2] == 3 and type[i+3] == 3 and type[i+4] == 3:  
                    serviceNo = ''.join(data[i+2:i+5])
            if "กำหนดชำระ" == data[i]: #JAN_2020
                month = functions.monthth(data[i+1])
                year = int(data[i+2]) - 543 # พศ to คศ
                billCycle =str(month)+"_"+str(year)
                # print(billCycle)
            if "ค่าบริการรายเดือนตามโปรโมชั่น" == data[i] and serviceNo:
                promotion = data[i]
                stage1Pos = i 
                listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ billCycle
                # print(listStr1)
                for j in range(i,len(data)):
                    if type[j] == 111 and serviceNo:
                        for k in range(stage1Pos,j+3):
                            if data[k] == "รวม" or data[k]=="ได้รับ":
                                break
                            if data[k] == "detectError01" :
                                if(data[k-1]=="-"):
                                    price = data[k-1]+""+data[k+1] # ex -0.99 
                                else:
                                    price = data[k+1]
                                promotionName = ' '.join(data[k+2:j])
                                promotionName = promotion+"\t"+promotionName
                                listStr2 = promotionName + "\t" + price
                                # print(listStr2)
                                stage1Pos = j+1
                                result.append(listStr1+"\t"+ listStr2)
                                break
                            elif type[k] == 4 :
                                # print(serviceNo+" "+data[k])
                                if data[k-1] == "-":
                                    price = ''.join(data[k-1:k+1])
                                    promotionName = ' '.join(data[stage1Pos:k-1])
                                    promotionName = promotion+"\t"+promotionName
                                    listStr2 = promotionName + "\t" + price
                                    print(listStr2)
                                    result.append(listStr1+"\t"+ listStr2)
                                else:
                                    print("normal")
                                stage1Pos = k+1
            elif "ค่าบริการเสริม" in data[i] and serviceNo:          
                promotion = data[i]
                stage1Pos = i 
                listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ billCycle      
                print(serviceNo)
                
                for j in range(stage1Pos,len(data)):
                    if data[j] == "detectError01" :
                        price = data[j+1]
                        stage1Pos = j+2 
                        for k in range(stage1Pos,stage1Pos+10) :
                            if data[k] == "detectError01" or data[k] =="ค่าใช้บริการส่วนเกิน"or data[k] =="รวม":
                                promotionName = ' '.join(data[stage1Pos:k-1])
                                promotionName = promotion+"\t"+promotionName
                                listStr2 = promotionName + "\t" + price
                                result.append(listStr1+"\t"+ listStr2)
                                break

                    if data[j] == "รวม" or data[j]== "ค่าใช้บริการส่วนเกิน":
                        # print("============================")
                        break


        result.append("")
        # print("\n".join(result))
        return "\n".join(result) 
         
def formatGetPackage(data,type,filename,provider):  
    accountNo=""
    serviceNo=""
    billCycle=""
    stage1Pos=0
    getPackageName=""
    result=[]
    if provider == 'TRUE':
        print("TRUE GET PACKAGE")
        for i in range(0,len(data)):
            if(type[i] == 11 and not accountNo):
                accountNo = data[i]
            if "กำหนดชำระ" == data[i]: #JAN_2020
                month = functions.monthth(data[i+1])
                year = int(data[i+2]) - 543 # พศ to คศ
                billCycle =str(month)+"_"+str(year)
            if data[i] == "หมายเลขโทรศัพท์":
                if type[i+1] == 3 and type[i+2] == 3 and type[i+1] == 3:     
                    serviceNo = ''.join(data[i+1:i+4])
                    print("TRUE = "+serviceNo)
                elif type[i+2] == 3 and type[i+3] == 3 and type[i+4] == 3:  
                    serviceNo = ''.join(data[i+2:i+5])
                    print("TRUE 1 = "+serviceNo)
            if "ใช้ไป" == data[i] and serviceNo:
                listStr1 =accountNo +"\t"+ serviceNo +"\t"+filename+"\t"+ billCycle 
                print("listStr1 = "+listStr1)
                if "(หน่วย)" == data[i+1]:
                    stage1Pos = i+2
                    for j in range(stage1Pos,len(data)):
                        if type[j] == 5 and type[j+2] == 5: #colon :
                            print("หลังหน่วย colon"+data[j])
                            getPackageName = ' '.join(data[stage1Pos:j])
                            dataReceive =  data[j]
                            typeReceive =data[j+1]
                            dataUse = data[j+2]
                            typeUse =data[j+3]
                            listStr2 = getPackageName + "\t" + dataReceive + "\t" + typeReceive + "\t" + dataUse + "\t" +typeUse
                            print(listStr1+"\t"+listStr2)
                            stage1Pos = j+4
                            result.append(listStr1+"\t"+ listStr2)
                        elif type[j] == 4 and type[j+2] == 4: #float
                            print("หลังหน่วย float"+data[j])
                            getPackageName = ' '.join(data[stage1Pos:j])
                            dataReceive =  data[j]
                            typeReceive =data[j+1]
                            dataUse = data[j+2]
                            typeUse =data[j+3]
                            listStr2 = getPackageName + "\t" + dataReceive + "\t" + typeReceive + "\t" + dataUse + "\t" +typeUse
                            print(listStr1+"\t"+listStr2)
                            stage1Pos = j+4
                            result.append(listStr1+"\t"+ listStr2)
                        elif type[j] == 3 and type[j+2] == 3: #number
                            print("หลังหน่วย number"+data[j])
                            getPackageName = ' '.join(data[stage1Pos:j])
                            dataReceive =  data[j]
                            typeReceive =data[j+1]
                            dataUse = data[j+2]
                            typeUse =data[j+3]
                            listStr2 = getPackageName + "\t" + dataReceive + "\t" + typeReceive + "\t" + dataUse + "\t" +typeUse
                            print(listStr1+"\t"+listStr2)
                            stage1Pos = j+4
                            result.append(listStr1+"\t"+ listStr2)
                        if "ค่าใช้บริการส่วนเกิน" == data[j] or "รวม" == data[j] and type[j+2]!=5 or "ค่าใช้บริการส่วนเกิน/ค่าใช้บริการอื่นๆ" == data[j] or "ค่าบริการเสริม" == data[j] or "ค่าโทรทางไกลระหว่างประเทศ" == data[j] :
                            break
                    print("________________________________________")
        result.append("")
        return "\n".join(result) 

