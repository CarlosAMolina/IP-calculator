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

def bits2cero(numeroConvertir,numBits2cero):
    # converts to 0 x number of bits of numeroConvertir starting at rigth (x=numBits2cero)
    for i in range(numBits2cero):
        numeroConvertir=numeroConvertir&(255<<(i+1)) # 255=11111111->not elimiate left numbers of numeroConvertir
    return numeroConvertir

def bits2one(numeroConvertir,numBits2one):
    # converts to 1 x number of bits of numeroConvertir starting at rigth (x=numBits2one)
    for i in range(numBits2one):
        numeroConvertir=numeroConvertir|1<<i # all ones
    return numeroConvertir

def makeBase(ip, bits4hosts): # ip[=]list
    ipBase=list(ip)
    if bits4hosts<=8:
        ipBase[3]=bits2cero(ip[3],bits4hosts)
    elif bits4hosts<=16:
        ipBase[3]=bits2cero(ip[3],8)
        ipBase[2]=bits2cero(ip[2],bits4hosts-8)
    elif bits4hosts<=24:
        ipBase[3]=bits2cero(ip[3],8)
        ipBase[2]=bits2cero(ip[2],8)
        ipBase[1]=bits2cero(ip[1],bits4hosts-16)
    else:
        ipBase[3]=bits2cero(ip[3],8)
        ipBase[2]=bits2cero(ip[2],8)
        ipBase[1]=bits2cero(ip[1],8)
        ipBase[0]=bits2cero(ip[0],bits4hosts-24)
    return ipBase

def makeBroadcast(ip, bits4hosts): # ip[=]list
    ipBroadcast=list(ip)
    if bits4hosts<=8:
        ipBroadcast[3]=bits2one(ip[3],bits4hosts)
    elif bits4hosts<=16:
        ipBroadcast[3]=bits2one(ip[3],8)
        ipBroadcast[2]=bits2one(ip[2],bits4hosts-8)
    elif bits4hosts<=24:
        ipBroadcast[3]=bits2one(ip[3],8)
        ipBroadcast[2]=bits2one(ip[2],8)
        ipBroadcast[1]=bits2one(ip[1],bits4hosts-16)
    else:
        ipBroadcast[3]=bits2one(ip[3],8)
        ipBroadcast[2]=bits2one(ip[2],8)
        ipBroadcast[1]=bits2one(ip[1],8)
        ipBroadcast[0]=bits2one(ip[0],bits4hosts-24)
    return ipBroadcast

def bits4hostsInAPart(maskPart):    # maskPart = 8bits
    # searchs number of 0's, started at rigth
    hostsBits = 0
    multi = 1    # searchs 0's at mask
    while (len(bin(multi))-2)<=8:    # bin(multi)='0b..'
        if maskPart&multi==0:
            hostsBits += 1
        else:
            return hostsBits
        multi = multi << 1
    return hostsBits

def bits4hosts(maskList):     #mask=part0.part1.part2.part3, each part = 8bits
    maskPart = 3
    hostsBits = bits4hostsInAPart(maskList[maskPart])
    while hostsBits%8 == 0 and maskPart>0:
        maskPart -= 1
        hostsBits += bits4hostsInAPart(maskList[maskPart])
    return hostsBits

def calculate_ip(ip_mask):
    try:
        ip = ip_mask.split('/')[0]    # ip = '0.1.2.3'
        mask = ip_mask.split('/')[1]    # mask = '24', string
        ipList = str2list(ip)
        if len(mask)<=2: # mask as CIDR
            bits4Hosts = 32-int(mask)
        else: # mask at decimal notation
            maskList = str2list(mask)
            bits4Hosts = bits4hosts(maskList)
            mask = 32-bits4Hosts
        ipBaseList = makeBase(ipList,bits4Hosts)
        ipBroadcastList = makeBroadcast(ipList,bits4Hosts)
        ipBase = list2string(ipBaseList)
        ipBroadcast = list2string(ipBroadcastList)
        return [ipBase, ipBroadcast, mask]
    except:
        print color('rojo', 'Invalid syntax')


ip_mask = raw_input('Write your ipv4/mask (e.g. 192.168.1.5/255.255.255.0 or 192.168.1.5/24): ')
while ip_mask == "":
    ip_mask = raw_input('Write your ipv4/mask (e.g. 192.168.1.5/255.255.255.0 or 192.168.1.5/24): ')
[ipBase, ipBroadcast, mask]=calculate_ip(ip_mask)
print 'ip_broadcast: '+ str(ipBase)+'/'+str(mask)
print 'ip_broadcast: '+ str(ipBroadcast)