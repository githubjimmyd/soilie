import random, pickle, numpy

class Coherencer(object):
  def __init__(self):
    self.db = self.loadDB()
    self.reset()
    self.termsToProc = []

  def loadDB(self, path='pkb_matrix_sept2013-2'):
    with open(path, 'rb') as f:
      db = pickle.load(f)
    return db

  def reset(self):
    self.queries = []
    self.numTerms = 0
    self.threshold = 0.0
    self.sThreshold = 0.0
    self.coTerms = []
    self.selTerms = []
    self.totals = []
    self.sTotals = []
    self.filterType = None

  def buildPool(self, queries):
    pool = set(queries)
    #iterating the algorithm below increases the edge depth for search
    pool |= set([x for y in pool for x in self.db[y].keys()])
    #pool |= set([x for y in pool for x in self.db[y].keys()])
    pool = [x for x in pool if x not in queries]
    return pool

  def selectTerms(self, seed):
    if seed:
      sample = self.topN(self.queries, self.numTerms)
    else:
      sample = random.sample(self.coTerms, self.numTerms-len(self.queries))
    self.coTerms = [x for x in self.coTerms if x not in sample]
    return sample



  def setParams(self, queries=['party'], numTerms=5, threshold=0.23,
                sThreshold=10, seed=True):
    self.queries = queries
    self.selTerms.extend(queries)
    self.numTerms = numTerms
    self.threshold = threshold
    self.sThreshold = sThreshold
    self.coTerms = self.buildPool(self.queries)
    self.selTerms.extend(self.selectTerms(seed))
    self.fill()


  def fill(self):
    self.matrix = numpy.zeros([self.numTerms, self.numTerms])
    for i, term in enumerate(self.selTerms):
      for i2, term2 in enumerate(self.selTerms):
        try:
          val = self.db[term][term2]
        except KeyError:
          pass
        else:
          self.matrix[i][i2] = val
        try:
          val = self.db[term2][term]
        except KeyError:
          pass
        else:
          self.matrix[i2][i] = val
    self.matrix = numpy.ma.masked_equal(self.matrix, -1)

  #generic of above function:
  def mat(self, terms):
    matrix = numpy.zeros([len(terms), len(terms)])
    for i, term in enumerate(terms):
      for i2, term2 in enumerate(terms):
        try:
          val = self.db[term][term2]
        except KeyError:
          pass
        else:
          matrix[i][i2] = val
        try:
          val = self.db[term2][term]
        except KeyError:
          pass
        else:
          matrix[i2][i] = val
    matrix = numpy.ma.masked_equal(matrix, -1)
    return matrix

  def assess(self):
    self.totals = numpy.sum(self.matrix, 0) + numpy.sum(self.matrix, 1)
    total = numpy.mean(self.matrix)
    if total > self.threshold:
      self.sTotals = numpy.std(self.matrix, 0) + numpy.std(self.matrix, 1)
      total2 = numpy.std(self.matrix)
      if total2 < self.sThreshold:
        return True
      else:
        self.filterType = 'std'
        return False
    else:
      self.filterType = 'avg'
      return False



  def filter_(self):
    if self.filterType == 'avg':
      vals = [x for x in self.totals]
      r = False
    else:
      vals = [x for x in self.sTotals]
      r = True
    vals = zip(self.selTerms, vals)
    vals = sorted(vals, key=lambda x: x[1], reverse=r)
    self.selTerms.remove(vals[0][0])
    try:
      sel = random.choice(self.coTerms)
    except IndexError:
      return False
    else:
      self.coTerms.remove(sel)
      self.selTerms.append(sel)
      return True

  def ask(self, default=True):
    if default:
      self.reset()
      self.setParams()
    for x in xrange(5000):
      if self.assess():
        return self.selTerms
      else:
        if self.filter_():
          self.fill()
        else:
          return False

  def runLoop(self, num, query, t):
    self.reset()
    self.setParams([query], num, t)
    terms = self.ask(False)
    return terms

  def buildTermsToProc(self, num):
    self.termsToProc = [x for x in random.sample(self.db.keys(), num)]

  def askCycle(self, numTerms=5, threshold=0.23, sThreshold=10,
               seed=True, num=False):
    if num:
      self.buildTermsToProc(num)
    results = []
    for term in self.termsToProc:
      if len(self.db[term].keys()) < numTerms-1:
        temp = [term]
        temp.extend(self.db[term].keys())
        results.append(temp)
      else:
        self.setParams([term], numTerms, threshold, sThreshold, seed)
        results.append(self.ask(False))
      self.reset()
    return results

  def topN(self, terms, numTerms):
    """Calculates top co-occurring terms and returns them.

    Keyword arguments:
    term (str) -- query or term that's being associated to
    nTerms (int) -- number of associated terms INCLUDING query
    
    """
    store = []
    for term in terms:
      temp = self.db[term]
      ls = sorted(temp, key=lambda label: temp[label],
                  reverse=True)[:numTerms-1]
      store.append(ls)
    if len(store) > 1:
      #Tries to take common terms and if that fails adds with random selection
      #Might be better to go with topN of highest common co-occurring terms
      #Better to sum co-occurrence with each query for each coTerm
      temp = set(store[0])
      for x in store[1:]:
        temp &= set(x)
      temp |= set(random.sample([x for y in store for x in y],
                                numTerms-len(temp)))
      store[0] = [x for x in temp]
    return store[0]

  def calcTopN(self, numTerms=5, num=False):
    if num:
      self.buildTermsToProc(num)
    results2 = []
    for term in self.termsToProc:
      ls = self.topN([term], numTerms)
      ls.append(term)
      results2.append(ls)
    return results2

class Comparer(object):
  """Tests if image in 2nd database has matching terms to coherencer output.

  Public functions:
  ***Argument names are designed to be illustrative and may be different but
  similar in the actual function***
  loadDB(path)
  test(listOfResults)
  compare(singleResult)

  """

  def __init__(self):
    """Loads the database and stores the terms for quick access.

    """
    self.db = self.loadDB()
    self.terms = self.db.keys()

  def loadDB(self, path="pkb_by_lbl_filter5_sept2013"):
    """Loads database from the specified path defaulting to my location.

    """
    with open(path, 'r') as f:
      db = pickle.load(f)
    return db

  def test(self, results):
    """Takes output and returns total number of sets with corresponding image.

    Keyword arguments:
    results (list of lists) -- list of 'coherent' terms from one of the
    functions
    
    """
    c = self.compare
    total = 0
    for comb in results:
      if c(comb):
        total +=1
    return total

  def compare(self, comb):
    """Checks if there is are images that have this 'comb'ination of terms

    Keyword arguments:
    comb (list) -- a result set of terms for a particular query

    """
    if comb == False or comb == None:
      return False
    theSet = []
    for term in comb:
      if term not in self.terms:
        return False
    theSet.extend(self.db[comb[0]])
    comb = comb[1:]
    for term in comb:
      imgs = self.db[term]
      theSet = [t for t in theSet if t in imgs]
    if len(theSet) > 0:
      return True
    else:
      return False

class Main(object):
  """Runs all coherence algorithms and prints output.

  Public functions:
  run(numterms, numQueries, numTimes)

  """
  def __init__(self):
    """Initializes both classes.

    """
    self.coh = Coherencer()
    self.com = Comparer()

if __name__ == '__main__':
  m = Main()
##  m.run(4, 1000, 20)

##########
##For Testing purposes

  t = 0.19
  while t < 0.24:
    t2 = 0.1
    while t2 < 0.4:
      a = []
      for x in range(1):
        r = m.coh.askCycle(5, t, t2, True, 8372)
        a.append(m.com.test(r))
      print(t, t2, sum(a)) #/1, max(a), min(a)
      t2 += 0.1
    t += 0.01
##########

