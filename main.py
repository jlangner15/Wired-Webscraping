from bs4 import BeautifulSoup as soup
import requests

def contentcreator(pagenum):
    if pagenum > 1:
        url = 'https://www.wired.com/most-recent/page/' + str(pagenum) + '/' #use passed args to find wired correct url
    else:
        url = 'https://www.wired.com/most-recent/page/'
    response = requests.get(url, timeout=5)
    content = soup(response.content, "html.parser")
    return content

def containerGenerator(pagenum):
    return contentcreator(pagenum).findAll("a", {"class": "byline-component__link"}) #Returns container with indidivual articles

def getLink(pagenum,index):
    siteArticle = contentcreator(pagenum).findAll("li", {"class": "archive-item-component"})
    link = siteArticle[index].a['href'] #return article url linked to name
    return link

def getTitle(pagenum,index):
    titles = contentcreator(pagenum).findAll("h2", {"class": "archive-item-component__title"})
    return titles[index].text

def authorFinder(name,pages):
    numArticles = 0

    filename = name + "_wiredWS"".txt"
    f = open(filename, 'w')

    for j in range(1,pages + 1):
        containers = containerGenerator(j)
        for i in range(len(containers)):
            if containers[i].text == name:
                numArticles += 1

                f.write("Page: "+ str(j) + " Link: " + 'https://www.wired.com' + str(getLink(j,i)) + "\n")

    f.close()
    print("completed")

#authorFinder("Andy Greenberg",5)

def keywordAdjustor(keyword):
    list = [keyword]
    if 65 <= ord(keyword[0]) <= 90:
        list.append(chr(ord(keyword[0])+32) + keyword[1:])
    else:
        list.append(chr(ord(keyword[0])-32) + keyword[1:])
    return list

def titleKeyword(keyword, pages):
    numArticles = 0
    k1 = keywordAdjustor(keyword)[0]
    k2 = keywordAdjustor(keyword)[1]
    filename = "articles_with_" + keyword + ".txt"
    f = open(filename, 'w')

    for page in range(2, pages + 1):
        containers = containerGenerator(page)

        for i in range(10):
            listTitleSplit = getTitle(page,i).split(" ")

            for j in range(len(listTitleSplit)):
                if listTitleSplit[j] == k1 or listTitleSplit[j] == k2:
                    numArticles += 1
                    f.write("Link: " + "https://www.wired.com" + getLink(page,j) + "\n")
    print("Number articles with '" + str(keyword) + "' is "+ str(numArticles) + " articles")
    f.close()
    print("completed")

#titleKeyword("The",4)

def main():
    print("This is a personal webscraping project using BeautifulSoup\ndesigned to search Wired's recentarticles by any author or title keyword\n"
          "If you would like to search by author please enter:\n'author' or 'keyword' or 'both' without the quotation marks to specify your decision")

    decision = input("Please enter your decision \n")

    if decision == 'author':
        author = input('Please enter the author case sensitive Ex. Elon Musk NOT elon musk \n')
        pages = int(input("Please enter how many most recent pages you would like to search for " + author + "\n"))
        print("running...")
        authorFinder(author,pages)
    elif decision == 'keyword':
        keyword = input('Please enter the keyword \n')
        pages = int(input("Please enter how many most recent pages you would like to search for " + keyword + "\n"))
        print("running...")
        titleKeyword(keyword,pages)
    elif decision == 'both':
        author = input('Please enter the author case sensitive Ex. Elon Musk NOT elon musk \n')
        pages = int(input("Please enter how many most recent pages you would like to search for " + author + "\n"))
        authorFinder(author, pages)
        keyword = input('Please enter the keyword \n')
        pages = int(input("Please enter how many most recent pages you would like to search for " + keyword + "\n"))
        titleKeyword(keyword, pages)

    else:
        print("Please try again")
        main()
main()