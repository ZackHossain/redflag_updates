import requests
import json
from bs4 import BeautifulSoup
from sender import notify


# Define the base URL
base_url = "https://redflag.org.au"

# Find all article titles
def get_titles(bs):
    anchors = bs.find_all('a')

    found = []
    
    articles = []
    for anchor in anchors:
        href = anchor.get('href')
        if href in found:
            continue
        else:
            found.append(href)
        
        if 'marxistleftreview' in href:
            continue
        
        if 'article' in href:   # href for articles is structured as /article/{article_id}
            title = anchor.get_text(strip=True)
            new_article = {
                'title': title,
                'href': base_url + href
            }
            if new_article not in articles:
                articles.append(new_article)
    
    return articles

def get_old_articles():
    old_articles = None
    with open('articles.json', 'r') as fd:
        return json.load(fd)

# checks if articles are different
# returns list of new articles if there is a difference
# otherwise returns None
def compare_articles(old, new):
    new_articles = []
    for article in new:
        if article not in old:
            new_articles.append(article)
    
    if new_articles == []:
        return None
    
    return new_articles

def save_new_articles(articles):
    with open('articles.json', 'w') as fd:
        json.dump(articles, fd, ensure_ascii=False, indent=4)
    
    print('saved articles')

def new_articles_notification(articles):
    msg = 'New article(s) on Red Flag! @everyone\n'
    i = 0
    for article in articles:
        # limits notification to 5 articles
        if i > 4:
            msg = msg + "[AND MORE!](https://redflag.org.au)"
            break
        
        title = article['title']
        href = article['href']
        
        if title == "":
            title = href[31:]
        msg = msg + f'* [\"{title}\"]({href})\n'
        i = i + 1 
    notify(msg)
    

if __name__ == '__main__':
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    updated_articles = get_titles(soup)
    old_articles = get_old_articles()
    
    new_articles = updated_articles
    if len(old_articles) != 0:
        new_articles = compare_articles(old_articles, updated_articles)
        if new_articles is not None:
            new_articles_notification(new_articles)
    else:
        new_articles_notification(new_articles)
    
    save_new_articles(updated_articles)