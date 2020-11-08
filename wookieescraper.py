import requests
from bs4 import BeautifulSoup


def get_wikia_contents(url):
    """
    scrapes given webpage
    returns a tuple (title, description)
    """
    
    if url is None:
        return (None, None)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find(id='firstHeading')

    description = soup.find("meta", {"name": "description", "content": True})['content']
    for i in range(10):
        description = description.replace(f"{i}", "")
    
    return (title.string, description)

def get_wikia_article(search_term):
    """
    returns the url of the first wookieepedia article
    that matches the given search term
    """
    googlified_search_term = '+'.join(term for term in search_term.split(' '))
    
    google_query = f"https://www.google.com/search?sxsrf=ALeKk036ntSwXkae4YOGp5Vz1pV7dujP_w%3A1604704208905&ei=0NelX_npNt-Y4-EPkeaf0AI&q={googlified_search_term}%3Astarwars.fandom.com/wiki"
    
    r = requests.get(google_query)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    for link in soup.find_all('a'):
        url = link.get('href')
        #print(url)
        #and search_term.lower() in url.lower()
        if url and '/url?q=' in url and 'Main_Page' not in url:
            stop_index = -1
            for i, c in enumerate(url):
                if i > 7 and not (c.isalpha() or c == '/' or c == '.' or c == ':'):
                    stop_index = i
                    #print(f"c == {c}")
                    break
                
            #stop_index = min(url.find('&', 7), url.find('%', 7))
            #print(stop_index)
            return url[7:stop_index]
            #print(url[7:url.find('&')])
        #if '/url?q=' in link.text:
        #    return link.text[17:link.text.find('&')]
        #print(link)  
    
    #print(soup)
    #return soup.find('cite').text    
 
    

url = get_wikia_article("sarlacc")
print(url)
title, description = get_wikia_contents(url)
print(title)
print(description + "...")