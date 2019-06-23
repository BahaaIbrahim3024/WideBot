from bs4 import BeautifulSoup
import urllib
import time
import requests


firstUrl = "https://en.wikipedia.org/wiki/Special:Random"
endURL = "https://en.wikipedia.org/wiki/Philosophy"
visitedUrls = [firstUrl]



def findLinks(url):
    sourceCode = requests.get(url)
    plainText = sourceCode.text
    soup = BeautifulSoup(plainText,"html.parser")

    # This div stars with the body of the article
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # if the link contains no links it remains None
    article_link = None

    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link

def spider_module(scraping_history, target_url, max_steps=30):

    if scraping_history[-1] == target_url:
        print("Target ('Philosphy') article reached!")
        return False

    elif len(scraping_history) > max_steps:
        print("Maximum (30) searches reached, interrupted.")
        return False

    elif scraping_history[-1] in scraping_history[:-1]:
        print("We are in a Loop , interrupted.")
        return False
    else:
        return True


while spider_module(visitedUrls, endURL):
    print(visitedUrls[-1])

    first_link = findLinks(visitedUrls[-1])
    # when arrive at an article with no links
    if not first_link:
        print("Arrived at an article with no links, search aborted.")
        break

    visitedUrls.append(first_link)

    time.sleep(0.5)  # Slow things down so as to not overload Wikipedia's servers
visited_urls=[firstUrl]