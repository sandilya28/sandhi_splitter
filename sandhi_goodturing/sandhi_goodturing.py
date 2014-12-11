allSPLeftTokens = []
allSPRightTokens = []
allNSPLeftTokens = []
allNSPRightTokens = []

lftSPCount = {}
rgtSPCount = {}
lftNSPCount = {}
rgtNSPCount = {}

els = {}
ers = {}
eln = {}
ern = {}

selectedCorrectTP = []
selectedNOTCorrectFP = []
notSelected = []
notSelectedCorrectFN = []
notSelectedNOTCorrectTN = []

CONST_K = 6
SKIP = 3
THRESHOLD = 0.0

def getRightTokenNSPPBT(sfx):
    prob = 0.0
    prev = ""
    stri = ""
    i = 0
    for c in sfx :
        token = prev + str(c)
        i+=1
        if (i< SKIP ):
            prev = token
            continue

        nsp = getRgtNSPCount(token)
        sp = getRgtSPCount(token)

        tot = sp + nsp

        if(tot!=0):
            prob = prob + (nsp*1.0/tot)*1.0
        prev = prev + str(c)
    return prob

def getLeftTokenNSPPBT(pfx):

    prob = 0.0
    prev = ""
    i = 0
    for c in pfx :
        token = str(c) + prev
        i+=1
        if (i<SKIP):
            prev = token
            continue
        nsp = getLftNSPCount(token)
        sp = getLftSPCount(token)

        tot = sp + nsp
        if (tot!=0):
            prob = prob + (nsp*1.0/tot)*1.0
        prev = token
        
    return prob

def getRightTokenPBT(sfx):
    prob = 0.0
    prev = ""
    i = 0
    for c in sfx:
        token = prev + str(c)
        i+=1
        if (i<SKIP):
            prev = token
            continue

        nsp = getRgtNSPCount(token)
        sp = getRgtSPCount(token)
        
        tot = sp + nsp

        if (tot!=0):
            prob = prob + (sp*1.0/tot)*1.0
        prev = prev + str(c)
    return prob

def getLeftTokenPBT(pfx):
    prob = 0.0
    prev = ""
    i = 0
    for c in pfx :
        token = str(c)+prev
        i += 1
        if (i<SKIP):
            prev = token
            continue
        nsp = getLftNSPCount(token)
        sp = getLftSPCount(token)

        tot = sp + nsp
        if(tot!=0):
            prob = prob + (sp*1.0/tot)*1.0
        prev = token
    return prob

def getLftSPCount(stri):
    try:
        a = lftSPCount[stri]
        return goodTuring(lftSPCount[stri],0)
    except:
        return goodTuring(1,0)
def getRgtSPCount(stri):
    try:
        a = rgtSPCount[stri]
        return goodTuring(rgtSPCount[stri],1)
    except:
        return goodTuring(1,1)
def getLftNSPCount(stri):
    try:
        a = lftNSPCount[stri]
        return goodTuring(lftNSPCount[stri],2)
    except:
        return goodTuring(1,2)
def getRgtNSPCount(stri):
    try:
        a = rgtNSPCount[stri]
        return goodTuring(rgtNSPCount[stri],3)
    except:
        return goodTuring(1,3)

def goodTuring(num,flag):
    r = num + 1
    while(True):
        if flag==0:
            if(r==num+100):
                ans = (num+1)*1.0*(5/els[num]*1.0)
                return ans
                break
            else :
                try :
                    ans = (num+1)*1.0*(els[r]/els[num]*1.0)
                    return ans
                    break
                except:
                    r+=1
        if flag==1:
            if(r==num+100):
                ans = (num+1)*1.0*(5/ers[num]*1.0)
                return ans
                break
            else:
                try:
                    ans = (num+1)*1.0*(ers[r]/ers[num]*1.0)
                    return ans
                    break
                except:
                    r+=1
        if flag==2:
            if(r==num+100):
                ans = (num+1)*1.0*(5/eln[num]*1.0)
                return ans
                break
            else:
                try:
                    ans = (num+1)*1.0*(eln[r]/eln[num]*1.0)
                    return ans
                    break
                except:
                    r+=1
        if flag==3:
            if(r==num+100):
                ans = (num+1)*1.0*(5/ern[num]*1.0)
                return ans
                break
            else:
                try:
                    ans = (num+1)*1.0*(ern[r]/ern[num]*1.0)
                    return ans
                    break
                except:
                    r+=1

def loadFrequencies():
    for i in lftSPCount.keys():
        try:
            ans = els[lftSPCount[i]]
            els[lftSPCount[i]] += 1
        except:
            els[lftSPCount[i]] = 1
    for i in rgtSPCount.keys():
        try:
            ans = ers[rgtSPCount[i]]
            ers[rgtSPCount[i]] += 1
        except:
            ers[rgtSPCount[i]] = 1

    for i in lftNSPCount.keys():
        try:
            ans = eln[lftNSPCount[i]]
            eln[lftNSPCount[i]] += 1
        except:
            eln[lftNSPCount[i]] = 1
    for i in rgtNSPCount.keys():
        try:
            ans = ern[rgtNSPCount[i]]
            ern[rgtNSPCount[i]] += 1
        except:
            ern[rgtNSPCount[i]] = 1

def main():
    inpfile = "train1.txt"
    fp = open(inpfile,"r",encoding="utf8")
    entryArr = []
    for line in fp :
        line = line.split("\n")
        entryArr.append(line[0])
    loadTrainingData(entryArr)
    loadFrequencies()
    testfile = "test1.txt"
    filep = open(testfile,"r",encoding="utf8")
    inputArr = []
    for line in filep :
        line = line.split("\n")
        inputArr.append(line[0])
    process(inputArr)

def getLeftToken(word,idx):
    leftToken = ""
#    print word
    if (idx - CONST_K > 0):
        leftToken = str(word[idx-CONST_K:idx+1])
    elif (idx <= CONST_K):
        leftToken = str(word[0:idx+1])
    return leftToken

def getRightToken(word,idx):
    rightToken = ""
    if(idx + CONST_K < len(word)):
        rightToken = str(word[idx:idx+CONST_K+1])
    elif(idx+CONST_K >= len(word)):
        rightToken = str(word[idx:len(word)])
    return rightToken

def addSPCount(leftToken,rightToken):
    for i in range(len(leftToken)):
        thisToken = leftToken[i:len(leftToken)]
        presentCount = matchCount(allSPLeftTokens,thisToken)
        lftSPCount[thisToken] = presentCount
    for i in range(len(rightToken)):
        thisToken = rightToken[0:i+1]
        presentCount = matchCount(allSPRightTokens,thisToken)
        rgtSPCount[thisToken] = presentCount

def addNSPCount(leftToken,rightToken):
    for i in range(len(leftToken)):
        thisToken = leftToken[i:len(leftToken)]
        presentCount = matchCount(allNSPLeftTokens,thisToken)
        lftNSPCount[thisToken] = presentCount
    for i in range(len(rightToken)):
        thisToken = rightToken[0:i+1]
        presentCount = matchCount(allNSPRightTokens,thisToken)
        rgtNSPCount[thisToken] = presentCount

def loadTrainingData(entryArr):
    for entry in entryArr :
        if(len(entry) > 2):
            entryTokens = entry.split("=")
            compoundWord = entryTokens[0]
            split = entryTokens[1].split('|')[1].split(",")
            #split = split.split(" ")[1]
            intArr = []
            for j in split :
                intArr.append(int(j))
            i = 0
            for thisChar in compoundWord :
                if (i!=0 and i!=len(compoundWord)):
                    leftToken = getLeftToken(compoundWord,i)
                    rightToken = getRightToken(compoundWord,i)

                    if i in intArr :
                        allSPLeftTokens.append(leftToken)
                        allSPRightTokens.append(rightToken)
                        addSPCount(leftToken,rightToken)
                    else:
                        allNSPLeftTokens.append(leftToken)
                        allNSPRightTokens.append(rightToken)
                        addNSPCount(leftToken,rightToken)
                i += 1
def matchCount(list1,token):
    count = 0
    for i in list1:
        if i==token:
            count += 1
    return count



def process(stringArr):
    correctCount = 0
    for inputString in stringArr :
        splitPointsArr = inputString.split("=")[1].split("|")[1].split(",")
        correctSplitPoints = []
        for stri in splitPointsArr:
            correctSplitPoints.append(int(stri))
        inputString = inputString.split("=")[0]
        i = 0
        probList = []
        probNSPList = []
        print("*"*100)
        print(inputString)
        for c in inputString:
            probNSP = 0.0
            if (i!=0 and i!=len(inputString)):
                 pfx = getLeftToken(inputString,i)
                 sfx = getRightToken(inputString,i)
                 #print(pfx)
                 #print(sfx)
                 #print ("")
                 lftPBT = getLeftTokenPBT(pfx[::-1])*1.0
                 lftNSPPBT = getLeftTokenNSPPBT(pfx[::-1])*1.0
                
                 rgtPBT = getRightTokenPBT(sfx)*1.0
                 rgtNSPPBT = getLeftTokenNSPPBT(pfx[::-1])*1.0
                 newlftPBT = 0.0
                 newrgtPBT = 0.0
                 newlftNSPPBT = 0.0
                 newrgtNSPPBT = 0.0
                 if (lftPBT!=0.0 and lftNSPPBT!=0.0):
                     newlftPBT = lftPBT*1.0 / (lftPBT + lftNSPPBT)
                     newlftNSPPBT = lftNSPPBT*1.0 / (lftPBT + lftNSPPBT)
                 if (rgtPBT!=0.0 and rgtNSPPBT!=0.0):
                     newrgtPBT = rgtPBT*1.0 / (rgtPBT + rgtNSPPBT)*1.0
                     newrgtNSPPBT = rgtNSPPBT*1.0 / (rgtPBT + rgtNSPPBT)*1.0
                 
                 prob = newlftPBT * newrgtPBT
                 probNSP = newlftNSPPBT * newrgtNSPPBT
                 print ("split "+str(i))
                 print (pfx+" : "+str(lftPBT))
                 print (sfx+" : "+str(rgtPBT))
                 print ("prob : "+str(prob))
                 print("")

                 probList.append(str(prob)+"_"+str(i))
            probNSPList.append(probNSP)
            i += 1
        probList.sort()
        print (probList)

        idxStr = probList[-1]
        maxProb = float(idxStr.split("_")[0])
        splitPntStr = idxStr.split("_")[1]
        splitPnt = int(splitPntStr)
        print ("Maximum Probability : "+str(maxProb))
        if maxProb > THRESHOLD :
            if splitPnt in correctSplitPoints :
                selectedCorrectTP.append(inputString)
            else:
                selectedNOTCorrectFP.append(inputString)
        else:
            if splitPnt in correctSplitPoints :
                notSelectedCorrectFN.append(inputString)
            else:
                notSelectedNOTCorrectTN.append(inputString)

    print ("Total Input Data : "+str(len(stringArr)))
    print ("selectedCorrectTP : "+ str(len(selectedCorrectTP)))
    print ("selectedNOTCorrectFP : "+ str(len(selectedNOTCorrectFP)))
    print ("notselectedCorrectFN : "+ str(len(notSelectedCorrectFN)))
    print ("notselectedNOTCorrectTN : "+ str(len(notSelectedNOTCorrectTN)))
    
    print (selectedCorrectTP)
    print (selectedNOTCorrectFP)
    print (notSelectedCorrectFN)
    print (notSelectedNOTCorrectTN)
    



if __name__=="__main__":
    main() 
