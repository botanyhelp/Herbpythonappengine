import sys, urllib2, urllib, codecs

#NOT THERE ANYMORE:
#sys.setdefaultencoding('utf8')

fieldlist = [];
fieldlist.append("ACCESSION")
fieldlist.append("TYPE")
fieldlist.append("COLLDATE")
fieldlist.append("FLOWER")
fieldlist.append("FRUIT")
fieldlist.append("STERILE")
fieldlist.append("OBJTYPE")
fieldlist.append("INST")
fieldlist.append("ANNCODE")
fieldlist.append("ANNDATE")
fieldlist.append("ANNSOURCE")
fieldlist.append("CITY")
fieldlist.append("SITENO")
fieldlist.append("CITYTYPE")
fieldlist.append("COLL2NAME")
fieldlist.append("COLL3NAME")
fieldlist.append("COLL1NAME")
fieldlist.append("COLLNO1")
fieldlist.append("COLLEVENT")
fieldlist.append("TAXCD")
fieldlist.append("CFS")
fieldlist.append("CFV")
fieldlist.append("CFVariety")
fieldlist.append("HABITAT_MISC")
fieldlist.append("HABITAT")
fieldlist.append("LONGX")
fieldlist.append("LAT")
fieldlist.append("ELEV")
fieldlist.append("LLGENER")
fieldlist.append("LONG2")
fieldlist.append("LAT2")
fieldlist.append("LTDEC")
fieldlist.append("LGDEC")
fieldlist.append("NOWLOC")
fieldlist.append("LOAN")
fieldlist.append("PAGES")
fieldlist.append("ORIGCD")
fieldlist.append("PUBCD")
fieldlist.append("LITCIT")
fieldlist.append("PUBDATE")
fieldlist.append("PUBDATEA")
fieldlist.append("VERPERS")
fieldlist.append("VERDATE")
fieldlist.append("EX")
fieldlist.append("ARTICLE")
fieldlist.append("PREC")
fieldlist.append("STATEL")
fieldlist.append("COUNTY")
fieldlist.append("COUNTRY")
fieldlist.append("T1")
fieldlist.append("R1")
fieldlist.append("S1")
fieldlist.append("NSEW_1")
fieldlist.append("TRSGENER")
fieldlist.append("T2")
fieldlist.append("R2")
fieldlist.append("S2")
fieldlist.append("NSEW_2")
fieldlist.append("PLACE")
fieldlist.append("scan")
fieldlist.append("MAPFILE")
fieldlist.append("username")
fieldlist.append("date_time")
fieldlist.append("DTRS")
fieldlist.append("PKID")



#datafile=codecs.open("spdetail_herbfortynine10-next5lines.txt", "r", encoding='utf-8')
#datafile=codecs.open("spdetail_herbfortynine11.txt", "r", encoding='utf-8')
datafile=codecs.open("specimen_herbfortynine1.txt", "r", encoding='utf-8')
for line in datafile:
    line.rstrip()
    valuelist = []
    items_in_line = line.split("|")
    for item in items_in_line:
        #valuelist.append(str(item))
        #valuelist.append(item.encode("utf-8"))
        #print("----------------------")
        #print(item.encode("utf-8"))
        #print("----------------------")
        valuelist.append(item.encode("utf-8"))

    print(len(fieldlist), len(valuelist));
    tuplelist=[]
    for i in range(len(valuelist)):
        #print(i)
        tuplelist.append((fieldlist[i], valuelist[i]));
    
    #url = 'http://localhost:8080/addspecies'
    url = 'http://localhost:8080/addspecimen'
    data = urllib.urlencode(tuplelist)
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req, data)
    while 1:
        data = fd.read(1024)
        if not len(data):
            break
        sys.stdout.write(data)


