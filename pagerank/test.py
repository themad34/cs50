import random

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
    size = len(corpus)

    for k in corpus.keys():
        res[k] = 0

    cur_page = random.choice(list(corpus.keys()))
    res[cur_page] += 1


    for i in range(1,n):
        next_pr = transition_model(corpus,cur_page,damping_factor)
        print(list(next_pr.keys()))
        print([next_pr[pr] for pr in next_pr])
        cur_page = random.choices(list(next_pr.keys()),[next_pr[pr] for pr in next_pr])[0]
        print(next_pr.keys())
        print(cur_page)
        res[cur_page] += 1
        

    for k in res.keys():
        res[k] = res[k] / n

    return res


def links_to(corpus,page):
    res = []
    for p in corpus.items():
        if page in p[1] or p[1] == {}:
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

    for k in corpus.keys():
        res[k] = 1 / N

    update = True

    while update:
        print(1)
        update = False
        new = {}
        for i in res.items():
            p = i[0]
            sum = 0
            for l in links_to(corpus,p[0]):
                sum += res[l] / len(corpus[l])
            new[p] = (1 - damping_factor) / N + damping_factor * sum
        
            #check for update
            if abs(res[p]-new[p]) > 0.001:
                update = True
        res = new

    return res

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}, "4.html": {}}


page = '1.html'

d = 0.85

#print(links_to(corpus,'2.html'))


corp = {}

for i in corpus.items():
    if i[1]=={}:
        corp[i[0]]={x for x in corpus}
    else:
        corp[i[0]]=i[1]

print(corpus)
print(corp)