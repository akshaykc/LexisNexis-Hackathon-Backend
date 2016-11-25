import geocoder
import csv

firstLine = True
firstQuery = True


outFile = open('addWithLatLong.txt','wb')
queryCount = 0

with open('Addresses.csv', 'rb') as csvfile:
    for line in csvfile:
        line=line.replace('\x00', '')
        #line = line.replace("\r\n", "\t")
        if len(line.split("\t")) > 3:
            if firstLine:
                firstLine = False
                outFile.write(line[2:])
            else:
                elem = line.split("\t")
                line1Addr = elem[0]
                line2Addr = elem[1]
                city = elem[3]
                country = elem[6]
                address = ""
                #print line1Addr + ", " + city
                if firstQuery:
                    #firstQuery = False
                    if line1Addr.strip() != "NULL":
                        address = line1Addr + ", " + city + ", " + elem[5]
                        address = address.replace('"','')
                        g = geocoder.google(address)
                        queryCount += 1
                        
                    if not g.latlng or line1Addr.strip() == "NULL":
                        if line2Addr.strip() == "NULL":
                            address = city + ", " + elem[5]+ ", " + elem[6]
                            address = address.replace('"','')
                            g = geocoder.google(address)
                            queryCount += 1
                        else:
                            address = line2Addr + ", " + city + ", " + elem[5]
                            address = address.replace('"','')
                            g = geocoder.google(address)
                            queryCount += 1
                    
                    if g.latlng:
                        outFile.write(line[:-2]+"\t "+ str(g.latlng[0]) + "\t " + str(g.latlng[1]) + "\n")
                    print address
                    if queryCount == 30:
                        break
                    
    print "end"

outFile.close()



#g = geocoder.google('40 Berkeley Square, London')
#g = geocoder.google('Intuitive Surgical, Kifer Road, Sunnyvale, California')
#print g.latlng