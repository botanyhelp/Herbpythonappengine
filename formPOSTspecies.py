import sys, urllib2, urllib, codecs

#NOT THERE ANYMORE:
#sys.setdefaultencoding('utf8')

fieldlist = [];
fieldlist.append("Taxcd")
fieldlist.append("Syncd")
fieldlist.append("family_code")
fieldlist.append("genus")
fieldlist.append("species")
fieldlist.append("authority")
fieldlist.append("subsp")
fieldlist.append("variety")
fieldlist.append("forma")
fieldlist.append("subsp_auth")
fieldlist.append("var_auth")
fieldlist.append("forma_auth")
fieldlist.append("sub_family")
fieldlist.append("tribe")
fieldlist.append("common")
fieldlist.append("Wisc_found")
fieldlist.append("ssp")
fieldlist.append("var")
fieldlist.append("f")
fieldlist.append("hybrids")
fieldlist.append("status_code")
fieldlist.append("hide")
fieldlist.append("USDA")
fieldlist.append("COFC")
fieldlist.append("WETINDICAT")
fieldlist.append("FAM_NAME")
fieldlist.append("FAMILY")
fieldlist.append("GC")
fieldlist.append("FAMILY_COMMON")
fieldlist.append("SYNWisc_found")
fieldlist.append("SYNS_STATUS")
fieldlist.append("SYNV_STATUS")
fieldlist.append("SYNF_STATUS")
fieldlist.append("SYNHYBRIDS_STATUS")
fieldlist.append("SYNW_STATUS")
fieldlist.append("speciesweb_Taxcd")
fieldlist.append("Status")
fieldlist.append("Photo")
fieldlist.append("Photographer")
fieldlist.append("Thumbmaps")
fieldlist.append("Accgenus")
fieldlist.append("SORTOR")
fieldlist.append("Hand")
fieldlist.append("growth_habit_bck")
fieldlist.append("blooming_dt_bck")
fieldlist.append("origin_bck")
fieldlist.append("Thumbphoto")
fieldlist.append("date_time")
fieldlist.append("growth_habit")
fieldlist.append("blooming_dt")
fieldlist.append("origin")
fieldlist.append("Taxa")

#datafile=codecs.open("spdetail_herbfortynine10-next5lines.txt", "r", encoding='utf-8')
#datafile=codecs.open("spdetail_herbfortynine11.txt", "r", encoding='utf-8')
datafile=codecs.open("spdetail_herbfortynine13.txt", "r", encoding='utf-8')
for line in datafile:
    line.rstrip()
    valuelist = []
    items_in_line = line.split("|")
    #Get taxcd from species record, then use it to query for Specimen list
    #taxcd = items_in_line[0]
    #PROBLEM--this doesn't have DS connection to query for Specimen
    
    for item in items_in_line:
        #valuelist.append(str(item))
        #valuelist.append(item.encode("utf-8"))
        valuelist.append(item.encode("utf-8"))

    tuplelist=[]
    for i in range(len(valuelist)):
        tuplelist.append((fieldlist[i], valuelist[i]));
    
    url = 'http://localhost:8080/addspecies'
    data = urllib.urlencode(tuplelist)
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req, data)
    while 1:
        data = fd.read(1024)
        if not len(data):
            break
        sys.stdout.write(data)
