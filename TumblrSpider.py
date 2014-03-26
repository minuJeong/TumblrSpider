import os
import urllib2
from bs4 import BeautifulSoup

PAGE_UNIT = 3
SEED_BLOG = "globalmonsterhunters"
SEARCH_SEED = "monster"

def main() :
    # getTumblrFromID(SEED_BLOG, PAGE_UNIT )
    getTumblrFromSearch(SEARCH_SEED)

def getTumblrFromSearch(SEARCH_SEED) :
    src = "http://www.tumblr.com/search/" + SEARCH_SEED
    bs = BeautifulSoup(urllib2.urlopen(src).read())
    for a in bs.findAll("a") :
        href = a.get("href")

        # exceptions
        if not href :
            continue
        if not href[:4] == "http" :
            continue
        if href.find(".tumblr.com") == -1 :
            continue

        ID = href[ 7 : href.find(".tumblr.com") ]
        getTumblrFromID(ID, PAGE_UNIT)

def getTumblrFromID(ID, pageRange) :
    scriptDirName = os.path.dirname(__file__)
    for dirName in os.listdir(scriptDirName) :
        if dirName == ID :
            return

    if not os.path.exists( ID ) :
        os.makedirs( ID )

    for page in range(1, pageRange) :
        try :
            src = "http://%s.tumblr.com/page/%d" % (ID, page)
            print ID, page, src
            bs = BeautifulSoup (urllib2.urlopen(src).read())
        except :
            print "ERROR"
            return

        imgs = bs.findAll("img")
        links = bs.findAll("a")
        blogs = []
        for link in links :
            href = link.get("href")
            if not href.find(".tumblr.com/") == -1 :
                blog = href[ 7 : href.find(".tumblr.com/") ]
                blogs.append(blog)

        if imgs : saveImgtagsToFolder(imgs, ID + "/images_%s_%d" % (ID, page))

    if blogs: spiderToAnotherBlog(blogs)

def saveImgtagsToFolder( imgs, folder ) :
    if not os.path.exists( folder ) :
        os.makedirs( folder )

    imageNumber = 0
    for img in imgs :
        imageNumber += 1
        src = img.get("src")
        print "image source: ", src
        if not src[:4] == "http" :
            continue

        extension = src[-3:]
        if not (extension == "jpg" or extension == "gif" or extension == "png") :
            continue

        image = urllib2.urlopen( src ).read()

        file = open( folder + "/image_%d.%s" % ( imageNumber, extension ), "w" )
        file.write(image)
        file.close()

def spiderToAnotherBlog(blogs) :
    for blog in blogs :
        print "blog: ", blog
        getTumblrFromID( blog, PAGE_UNIT )

# if main, go main()
if __name__ == "__main__" :
    main()
