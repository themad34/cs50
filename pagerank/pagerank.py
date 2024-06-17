import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    res = {}
    x = 1 / len(corpus)
    y = len(corpus[page])
    if y>0:
    
        for k in corpus.keys():
            res[k] = (1 - damping_factor) * x

   
        y = 1 / len(corpus[page])
        for n in corpus[page]:
            res[n] += damping_factor * y

    else:
        for k in corpus.keys():
            res[k] = x
    
    return res



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res = {}
    

    for k in corpus.keys():
        res[k] = 0

    cur_page = random.choice(list(corpus.keys()))
    res[cur_page] += 1


    for i in range(1,n):
        next_pr = transition_model(corpus,cur_page,damping_factor)
        
        cur_page = random.choices(list(next_pr.keys()),[next_pr[pr] for pr in next_pr])[0]
      
        res[cur_page] += 1
        

    for k in res.keys():
        res[k] = res[k] / n

    return res


def links_to(corpus,page):
    res = []
    for p in corpus.items():
        if page in p[1]:
            res+=[p[0]]

    return res


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    res = {}
    N = len(corpus)

    corp = {}
    for i in corpus.items():
        if i[1]=={}:
            corp[i[0]]={x for x in corpus}
        else:
            corp[i[0]]=i[1]


    for k in corp.keys():
        res[k] = 1 / N

    update = True

    while update:
       
        update = False
        new = {}
        for i in res.items():
            p = i[0]
            sum = 0
            
            for l in links_to(corp,p):
                x = len(corp[l])
               
                sum += res[l] / x
            
            new[p] = (1 - damping_factor) / N + damping_factor * sum
        
            #check for update
            
            if abs(res[p]-new[p]) > 0.001:
                update = True
            
        res = new

    return res



if __name__ == "__main__":
    main()
