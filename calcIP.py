def str2list(STRing):    # each element separed by dot
    parts = STRing.split('.')    # parts=['0','1','2','3']
    List = []
    List.append(int(parts[0]))
    List.append(int(parts[1]))
    List.append(int(parts[2]))
    List.append(int(parts[3]))
    return List        #  list=[0,1,10,11], int elements

def list2string(List):
    return '%s.%s.%s.%s' %(List[0],List[1],List[2],List[3])

def bits2cero4Base(numeroConvertir,numBits2cero):
    # converts to 0 x number of bits of numeroConvertir starting at rigth (x=numBits2cero)
    for i in range(numBits2cero):
        numeroConvertir=numeroConvertir&(255<<(i+1)) # 255=11111111->not elimiate left numbers of numeroConvertir
    # takes as 0 only x bits starting at the rigth (x=numBits2cero)
    numeroConvertir=bin(numeroConvertir)[-numBits2cero:] # example: 255and5=5 but if numBits2cero=1 must to be 255and5=1
    numeroConvertir = int(str(numeroConvertir),2) # from binary to decimal
    return numeroConvertir

def bits2one4Broadcast(numeroConvertir,numBits2one):
    # converts to 1 x number of bits of numeroConvertir starting at rigth (x=numBits2one)
    for i in range(numBits2one):
        numeroConvertir=numeroConvertir|1<<i # all ones
    # takes as 1 only x bits starting at the rigth (x=numBits2one)
    numeroConvertir=bin(numeroConvertir)[-numBits2one:] # example: numBits2one=1, then 5 or 1 = 5, but must to be 1
    numeroConvertir = int(str(numeroConvertir),2) # from binary to decimal
    return numeroConvertir

def makeBase(ip, bits4hosts): # ip[=]list
    ipBase=list(ip)
    if bits4hosts<=8:
        ipBase[3]=bits2cero4Base(ip[3],bits4hosts)
    elif bits4hosts<=16:
        ipBase[3]=bits2cero4Base(ip[3],8)
        ipBase[2]=bits2cero4Base(ip[2],bits4hosts-8)
    elif bits4hosts<=24:
        ipBase[3]=bits2cero4Base(ip[3],8)
        ipBase[2]=bits2cero4Base(ip[2],8)
        ipBase[1]=bits2cero4Base(ip[1],bits4hosts-16)
    else:
        ipBase[3]=bits2cero4Base(ip[3],8)
        ipBase[2]=bits2cero4Base(ip[2],8)
        ipBase[1]=bits2cero4Base(ip[1],8)
        ipBase[0]=bits2cero4Base(ip[0],bits4hosts-24)
    return ipBase

def makeBroadcast(ip, bits4hosts): # ip[=]list
    ipBroadcast=list(ip)
    if bits4hosts<=8:
        ipBroadcast[3]=bits2one4Broadcast(ip[3],bits4hosts)
    elif bits4hosts<=16:
        ipBroadcast[3]=bits2one4Broadcast(ip[3],8)
        ipBroadcast[2]=bits2one4Broadcast(ip[2],bits4hosts-8)
    elif bits4hosts<=24:
        ipBroadcast[3]=bits2one4Broadcast(ip[3],8)
        ipBroadcast[2]=bits2one4Broadcast(ip[2],8)
        ipBroadcast[1]=bits2one4Broadcast(ip[1],bits4hosts-16)
    else:
        ipBroadcast[3]=bits2one(ip[3],8)
        ipBroadcast[2]=bits2one(ip[2],8)
        ipBroadcast[1]=bits2one(ip[1],8)
        ipBroadcast[0]=bits2one(ip[0],bits4hosts-24)
    return ipBroadcast

def bits4hostsInAPart(mascPart):    #masc=part0.part1.part2.part3, each part = 8bits
    hostsBits = 0
    multi = 1    # searchs 0's at masc
    while (len(bin(multi))-2)<=8:    # bin(multi)='0b..'
        if mascPart&multi==0:
            hostsBits += 1
        else:
            return hostsBits
        multi = multi << 1
    return hostsBits

def bits4hosts(mascList):     #masc=part0.part1.part2.part3, each part = 8bits
    mascPart = 3
    hostsBits = bits4hostsInAPart(mascList[mascPart])
    while hostsBits%8 == 0 and mascPart>0:
        mascPart -= 1
        hostsBits += bits4hostsInAPart(mascList[mascPart])
    return hostsBits



import sys
sintaxisOK = False
while sintaxisOK == False:
    ipMasc = raw_input('Escriba ip/mascara (ejm 192.168.1.5/255.255.255.0): ')
    # if len(ipMasc) == 0:
    #     ipMasc = '192.168.1.5/255.255.255.0'
    #     # ipMasc = '192.168.1.5/128.0.0.0'
    try:
        ip = ipMasc.split('/')[0]    # ip = '0.1.2.3'
        masc = ipMasc.split('/')[1]    # masc = 24
        sintaxisOK = True
    except:
        print 'sintaxis incorrecta'
ipList = str2list(ip)
mascList = str2list(masc)

bits4Hosts = bits4hosts(mascList)
masc = 32-bits4Hosts
ipBaseList = makeBase(ipList,bits4Hosts) #ipBaseList = ipANDmasc(ipList,mascList)
ipBroadcastList = makeBroadcast(ipList,bits4Hosts) 
ipBase = list2string(ipBaseList)
ipBroadcast = list2string(ipBroadcastList)
# print 'ip: ' + str(ip)
# print 'masc: ' + str(masc)
# print 'ip base: '+str(ipBase)
# print 'bits4Hosts :' + str(bits4Hosts)
print 'ip_base/masc: '+ str(ipBase) +'/'+str(masc)
print 'ip_broadcast: '+ str(ipBroadcast)

# webs 4 help
#http://www.tutorialspoint.com/python/bitwise_operators_example.htm