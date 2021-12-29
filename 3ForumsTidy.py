import requests
from requests.exceptions import HTTPError
import re
from bs4 import BeautifulSoup
import webbrowser
# from pytube import extract

def FindYoutubes(url, page):

    r = requests.get(url) ## Get Url
    r_html = r.content ##Get HTML
    soup = BeautifulSoup(r_html, 'html.parser')
    allhtml = str(soup.find_all('a'))
    spans = str(soup.find_all('span'))
    divs = str(soup.find_all('div'))
    
    
    
    Link_Type_1_Index = [m.start() for m in re.finditer('youtu.be/', allhtml)]
    Link_Type_2_Index = [m.start() for m in re.finditer('youtube.com/watch\?v', allhtml)]
    Link_Type_3_Index = [m.start() for m in re.finditer('data-youtube-id=', divs)]
    Link_Type_4_Index = [m.start() for m in re.finditer('youtube.com', spans)]
    
    YtLinkList = []
    
    for i in range(0, len(Link_Type_1_Index)):
        YtLinkList.append('>>>>> ')##Create Seperator for Splitting   9 20
        for c in range(Link_Type_1_Index[i]+9, Link_Type_1_Index[i]+20):    
            YtLinkList.append(allhtml[c])
    
    for i in range(0, len(Link_Type_2_Index)):
        YtLinkList.append('>>>>> ')##Create Seperator for Splitting   20 31
        for c in range(Link_Type_2_Index[i]+20, Link_Type_2_Index[i]+31):    
            YtLinkList.append(allhtml[c])
    
    for i in range(0, len(Link_Type_3_Index)): 
        YtLinkList.append('>>>>> ')##Create Seperator for Splitting   20 31
        for c in range(Link_Type_3_Index[i]+17, Link_Type_3_Index[i]+28):    
            YtLinkList.append(divs[c]) #data-youtube-id="kNv3lcNRhi8"
        
    for i in range(0, len(Link_Type_4_Index)):
        YtLinkList.append('>>>>> ')##Create Seperator for Splitting  20 31
        for c in range(Link_Type_4_Index[i]+20, Link_Type_4_Index[i]+31):  
            YtLinkList.append(spans[c])
    
    YtLinkListSorted = (''.join(YtLinkList)).split('>>>>> ')
   
    del YtLinkListSorted[0]
     
#     print("page : " + str(page))
#     print(YtLinkListSorted)#debugging
    
#     return list(dict.fromkeys(YtLinkListSorted))
    return YtLinkListSorted
    
def CheckURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
            
    except HTTPError as http_err:
            
        print(f'HTTP error occurred: {http_err}\n')
        return False
                    # Python 3.6
    except Exception as err:
            
        print(f'error occurred: {err}\n')
        return False# Python 3.6
    else:
        if url.find("dissensus.com") != -1:
            return 1
        elif url.find("ilxor.com") != -1:
            return 2
        elif url.find("555-5555.org") != -1:
            return 3
        else:
            print("This website is not currently supported")
            return False

def CleanUnreadables(PlayListOut): ##!!!!!!!!!!!!!!!!Unused Function
            
    PlayListOut = re.sub(",....\.\.\.....|,me_continue|,.....\.\.\....|,...\.\.\......|,...\.\.\......", "", PlayListOut) #del timecontinue, sdfds...sdff = shortened links
    
    return PlayListOut #sdffg...eat (feature)

def OpenLinksorNot(PlayListOut, Open):
        if Open == 'Y' or Open == 'y':
            webbrowser.open(PlayListOut + '&disable_polymer=true', new=1)
    

def PlaylistOutputBelow50(Links_Count_Down, Counter, Links_Num, PlayListOut, PlayList, Open):
    
    while Links_Count_Down > 0:    

        if Counter < Links_Num:
            
            PlayListOut += PlayList[Links_Num - Links_Count_Down]
            Links_Count_Down -= 1
            Counter += 1
        
        if Links_Count_Down == 0:
                
#             PlayListOut = CleanUnreadables(PlayListOut)  #Rough cut from unknown error in parsing time linked YTs....
            print(PlayListOut + '&disable_polymer=true')
            OpenLinksorNot(PlayListOut, Open)
    
def PrintLinks(Link, Pages, Open, PlayListsOrLinks, LinkType):
    
    ErrorStrings = "....\.\.\.....|me_continue|.....\.\.\....|...\.\.\......|...\.\.\......" #time continue, shortened link text
    Links = []
    PlayList = []
    Links_Num = 0
    Counter = 0
    Playlist_Count = 0
    StartLinks = ["5CDRfNSV1Mk,","CWGDJ1pdAug,","ySsp9-mjJKM,","WmaTAYtCs8E,","fXEjBHxVZR8,","cg5ImAawzd8,","G5JlIRRh2cs,","aaw_H_2VbAE,","DVSQDzWJOpY,","2OYRbNZTsRs,"]
    
    
    if PlayListsOrLinks == 1:
        PlayListOut = 'https://www.youtube.com/watch_videos?video_ids=' + StartLinks[Playlist_Count]  ##reset link value
  
    Links.append(FindYoutubes(Link,1)) ##Get Codes for first page.
   
    if Pages > 1: ## if more than 1 page cycle through to specified page number.
        if LinkType == 1:
            for z in range(2, Pages+1):
                Links.append(FindYoutubes(Link + 'page-' + str(z),z)) ###Save to list
        if LinkType == 3:
            for z in range(1, Pages, 10):
                Links.append(FindYoutubes(Link + '/' + str(z),z))   
   
    
    for x in Links:
        for y in x:
            if len(re.findall(ErrorStrings, y)) == 0:
                if PlayListsOrLinks == 1:
                    PlayList.append(y + ",")
                        
                elif PlayListsOrLinks == 0:   
                    Links_Num += 1
                    PlayList.append('https://www.youtube.com/watch?v=' + y)
    
    PlayList = list(dict.fromkeys(PlayList))
    Links_Num = len(PlayList)
    
    if PlayListsOrLinks == 0:
        for i in PlayList:
            print(i)
      
    print("\n Found " + str(Links_Num) + " Links") ##print Number of Links
    
    if PlayListsOrLinks == 1:
        
        Links_Count_Down = Links_Num ## Counter for Links
        
        if Links_Num > 49:  ##If More than 50 videos.
            while Links_Count_Down >= 49:
                while Counter < 49: ##Cycle through groups of 50 and output playlist.
                    PlayListOut += PlayList[Links_Num - Links_Count_Down]
                    Links_Count_Down -= 1
                    Counter += 1
                
                PlayListOut += PlayList[Links_Num - 1]##Add final item
                
                Playlist_Count += 1
#                 PlayListOut = CleanUnreadables(PlayListOut)
                                                            #Rough cut from unknown error in parsing time linked YTs....
                print(PlayListOut + '&disable_polymer=true')
                
                OpenLinksorNot(PlayListOut, Open)
               
                print("\n")
               
                if PlayListsOrLinks == 1:
                    PlayListOut = 'https://www.youtube.com/watch_videos?video_ids=' + StartLinks[Playlist_Count] ##reset link value
              
                Counter = 0
                
#             print(Links_Count_Down)
            PlayListOut = 'https://www.youtube.com/watch_videos?video_ids=' + StartLinks[Playlist_Count]
            PlaylistOutputBelow50(Links_Count_Down, Counter, Links_Num, PlayListOut, PlayList, Open) ##when Links are less than 50.
                    
        else: ##If Links are less than 50.
            
            PlaylistOutputBelow50(Links_Count_Down, Counter, Links_Num, PlayListOut, PlayList, Open)
        
        print("\n ------------------------- \n finished")

iLink = input("Copy Your Link Here: ")
LinkType = CheckURL(iLink)
iPages = 0
Open = 'n'
PlayListsOrLinks = 0

if LinkType != False:
    
    if LinkType == 1:
        print("Parsing From Dissensus.com")
        iPages = input("Enter the number of pages: \n")
    
    elif LinkType == 2:
        print("Parsing From ilxor.com")
        IlxMusicPattern = "https://www.ilxor.com/ILX/ThreadSelectedControllerServlet?boardid=41&threadid="
        IlxMusicShowAllPattern = "https://www.ilxor.com/ILX/ThreadSelectedControllerServlet?action=showall&boardid=41&threadid="
        iLink = iLink.replace(IlxMusicPattern, IlxMusicShowAllPattern).strip('#unread')

    elif LinkType == 3:
        print("Parsing From 555-5555.com")
        iPages = input("Enter the number of posts: \n")
    
    if int(input("Press 0 for List of Links and 1 for Playlists: \n")) == 1:
    
        PlayListsOrLinks = 1
        Open = input("Open Playlists in Browser? Y/N \n")
    
    print("\n.....Searching \n")
    PrintLinks(iLink, int(iPages), Open, PlayListsOrLinks, LinkType) 
    

    


