from bs4 import BeautifulSoup 
import requests as rq
import regex as re

## This code: 
# a) Collects debates' website addresses by year beteween 1990-2005: metadata of debates;
# b) Filters xml web addresses where debates speeches are available;
# c) Filters xml addresses, mentioning 'housing crisis' expression;
# d) Counts debate sites by year;
# e) Repors result between 1990-2025 , where 2025 is a part year: 11 months;
# f) Generated chart of results.  

def WebRead02(WebAddr):#Reads a website content and returns it in text format
    x= rq.get(WebAddr)
    return(x.text)# returns results in text format


## Please replace folders with your folder names##
yearNb=[]
c03=0 # counter
for i in range (1990,2025+1):
    yearNb.append([int(i),0,0])# year, number of xml files; number of xml files containing ' housing crisis'
#print(yearNb)#test

ApiBased=True
if ApiBased:
    
    relev_sites=[]# list of relevant sites

    #quarter_nb=[0]*(36*4+1)# number of debate summaries in the given quarter between[01/Jan/1990; 2025 q4]; (nb: 2025 q4 is only a part of the quarter year; nb2: 1990 q0 does not exist)
    year_nb=[0]*(36+1)# number of summaries in the given quarter between[01/Jan/1990; 2025];



    n=1
    m=1
    for j in range(2006,2025+1):# (1990,2025+1)collection by year

        # Import API results from Oireachtas
        WebAddr=r'https://api.oireachtas.ie/v1/debates?&date_start=' +format(j)+r'-01-01&date_end='+format(j)+r'-12-31&skip=0&limit=100000'
        #WebAddr=r'https://api.oireachtas.ie/v1/debates?&date_start=2025-01-01&date_end=2025-12-01&skip=0&limit=100000'
        #print(WebRead02(WebAddr))# test

        #parsed_data01=BeautifulSoup(WebRead02(WebAddr),"html.parser")
        #https://api.oireachtas.ie/v1/debates?&date_start=2025-01-01&date_end=2025-12-01&skip=0&limit=100000

        # replace backslash in web addresses
        slashReplace = re.sub(r"\\/", "/", WebRead02(WebAddr)) 

        # find .xml website pointers
        pattern = r"https://data\.oireachtas\.ie[^\s\"']*\.xml" 
        matches = re.findall(pattern, slashReplace)
        #print(matches)
        c01=0
        c02=0
        for m in matches: 
            #print(c01, m)
            c01+=1
            yearNb[j-1990][1]+=1            
            if "housing crisis" in WebRead02(m).lower():
                c02+=1
                c03+=1
                yearNb[j-1990][2]+=1
                relev_sites.append(m)#save relevant site address
                print(c02, m)
                
        
        print(j, yearNb[j-1990][0], yearNb[j-1990][1],yearNb[j-1990][2])
        #print(c01, c02)
        #print(len(matches))

for j in range(2006, 2025+1):
    print(yearNb[j-1990][2])
# number of web sites
with open(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\Result_API_XML_NumResults_d1v2.txt', "w", encoding="utf-8") as f01:
    f01.write("Year, NbXMLFiles, NbXMLHousingCrisisFiles\n")
    for j in range(2006, 2025+1):
        f01.write(f"{yearNb[j-1990][0]},{yearNb[j-1990][1]},{yearNb[j-1990][2]}\n")
        #f01.write(yearNb[j-1990][0],yearNb[j-1990][1],yearNb[j-1990][2]  + "\n")

# web sites
with open(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\Result_API_XML_SiteResults_d1v2.txt', "w", encoding="utf-8") as f02:
    f02.write("Number, RelevantSiteMentioningHousingCrisis\n")
    for  value in enumerate(relev_sites):
       f02.write(f" {value}\n")
