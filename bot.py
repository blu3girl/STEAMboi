from bs4 import BeautifulSoup
import requests as reqs
def getInfo(url):
    if "https://store.steampowered.com/app/" not in url:
        return find(url)
    site = reqs.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    prices=soup.findAll("div", {"class": "game_area_purchase_game_wrapper"})
    products={}
    products['url']=url

    gameDict={}
    for price in prices:
        text=price.get_text().replace('\t',"").split('\n')
        text = [t.strip() for t in text if t.strip()!='']
        cost=''
        for x in text:
            if '$' in x:
                cost=x.split('$')
                break
        val = text[0][4:]
        gameDict[val]=cost
        if(gameDict[val]==""):
            continue
        gameDict[val][0]=gameDict[val][0].split('-')[-1]
        tempDict={}
        tempDict['Discount']=gameDict[val][0]
        if(len(gameDict[val])>=3):
            tempDict['Discount']=gameDict[val][0]
            tempDict['Original Price']=gameDict[val][1]
            tempDict['Current Price']=gameDict[val][2]
        elif(len(gameDict[val])==2):
            tempDict['Discount']=gameDict[val][0]
            tempDict['Current Price']=gameDict[val][1]
        else:
            tempDict['Current Price']=gameDict[val][0]
        gameDict[val]=tempDict
    products['game_options']=gameDict

    dlcs=soup.find('div', {'class': 'game_area_dlc_section'})
    if dlcs == None:
        return products
    dlcs = dlcs.find('div', {'class': 'tableView'})
    if dlcs == None:
        return products
    dlDicts={}
    text = dlcs.get_text().replace('\t',"").split('\n')
    text = [t.strip() for t in text if t.strip()!='']
    for i in range(0,len(text)-2,2):
        val = text[i+1]
        dlDicts[val]=text[i].split('$')
        dlDicts[val][0]= dlDicts[val][0].split('-')[-1]
        tempDict={}
       
        if(len(dlDicts[val])>=3):
            tempDict['Discount']=dlDicts[val][0]
            tempDict['Original Price']=dlDicts[val][1]
            tempDict['Current Price']=dlDicts[val][2]
        elif(len(dlDicts[val])==2):
            tempDict['Discount']=dlDicts[val][0]
            tempDict['Current Price']=dlDicts[val][1]
        else:
            tempDict['Current Price']=dlDicts[val][0]
        dlDicts[val]=tempDict
    products['dlc']=dlDicts
    return products
    
def find(string):
    search="https://store.steampowered.com/search/?term="+string
    site = reqs.get(search)
    soup = BeautifulSoup(site.content, 'html.parser')
    urls = soup.findAll('a')
    for url in urls:
        if 'https://store.steampowered.com/app' in url['href']:
            print(url['href'])
            return getInfo(url['href'])
    return None
