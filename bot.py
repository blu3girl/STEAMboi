from bs4 import BeautifulSoup
import requests as reqs
def foo(url):
    site = reqs.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    prices=soup.findAll("div", {"class": "game_area_purchase_game_wrapper"})
    products={}
    for price in prices:
        text=price.get_text().replace('\t',"").split('\n')
        text = [t.strip() for t in text if t.strip()!='']
        cost=''
        for x in text:
            if '$' in x:
                cost=x.split('$')
                break
        val = text[0][4:]
        products[val]=cost
        products[val][0]=products[val][0].split('-')[-1]
        tempDict={}
        tempDict['Discount']=products[val][0]
        if(len(products[val])>=3):
            tempDict['Original Price']=products[val][1]
            tempDict['Current Price']=products[val][2]
        else:
            tempDict['Current Price']=products[val][1]
        products[val]=tempDict
    dlcs=soup.find('div', {'class': 'game_area_dlc_section'}).find('div', {'class': 'tableView'})
    dlDicts={}
    text = dlcs.get_text().replace('\t',"").split('\n')
    text = [t.strip() for t in text if t.strip()!='']
    for i in range(0,len(text)-2,2):
        val = text[i+1]
        dlDicts[val]=text[i].split('$')
        dlDicts[val][0]= dlDicts[val][0].split('-')[-1]
        tempDict={}
        tempDict['Discount']=dlDicts[val][0]
        if(len(dlDicts[val])>=3):
            tempDict['Original Price']=dlDicts[val][1]
            tempDict['Current Price']=dlDicts[val][2]
        else:
            tempDict['Current Price']=dlDicts[val][1]
        dlDicts[val]=tempDict
    products['dlc']=dlDicts
    return products
    
# foo("https://store.steampowered.com/app/578650/The_Outer_Worlds/")
# foo("https://store.steampowered.com/app/625960/Stoneshard/")
print(foo("https://store.steampowered.com/app/678960/CODE_VEIN/"))
