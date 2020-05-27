f = open("/Users/sean/Library/CloudStorage/iCloud Drive/Documents/MyProjects/Python/mafengwo/Proxies/proxies.txt")
fw = open("/Users/sean/Library/CloudStorage/iCloud Drive/Documents/MyProjects/Python/mafengwo/Proxies/new_proxies.txt","w")
line = f.readline()

while line:
    print(line[7:])
    new_line=line[7:]
    new_line=new_line[:len(new_line)-2]
    print(new_line)
    fw.write( "     '"+new_line+"',\n")
    line = f.readline()


f.close()
fw.close()