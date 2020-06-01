
from nltk.corpus import wordnet as wn
from nltk.metrics.distance import edit_distance as ed
from pickle import load, dump
from utils.fuzzfunc import defuzz
from utils.parsers import fuzzparsetrainfiles, parsetraindata
import numpy as np

class NoWordnetMatchError(Exception):
  def __init__(self, word):
    self.word=word
  def __str__(self):
    return repr(self.word)

class NoDatabaseError(Exception):
  def __init__(self, msg):
    self.msg=msg
  def __str__(self):
    return repr(self.msg)

class VisuoBeta(object):
  """Builds a database of fuzzy magnitudes for angles and distances in an image.

  Public Functions:
  __init__(db, parsed, totrain, fparser, tparser) - Initializes Visuo.
        Requires either a path to a visuo database, a parsed database
        of the training files, or the training files themselves.
  getangledist(db, ktosyns, query, obj) - Returns the angle and distance.
  calcanglesdists(db, ktosyns, query, objs) - Makes a file for a set of angles
        and distances.
  savedb(db, filename) - Saves the visuo database.

  """
  DIST = np.array(range(-7, 1), np.float16)
  ANGL = np.array([-157.5, -135., -112.5, -90., -67.5, -45., -22.5, 0., 22.5,
                   45., 67.5, 90., 112.5, 135., 157.5, 180.], np.float16)
  ANGL2 = np.array([22.5, 45., 67.5, 90., 112.5, 135., 157.5, 180., 202.5, 225.,
                   247.5, 270., 292.5, 315., 337.5, 360.], np.float16)

  def getallobjs(self, db):
    k=db.keys()
    for k1 in db:
      k.extend(db[k1].keys())
    return list(set(k))

  def cleanoutput(self, db):
    todeletepairs=[]
    a=todeletepairs.append
    kbase=set(db.keys())
    k=self.getallobjs(db)
    notk=set.difference(set(k), set([_ for _ in k if len(wn.synsets(_))>0]))
    todeletesingles=set.intersection(notk, kbase)
    for k1 in list(kbase-todeletesingles):
      vals=list(set.intersection(set(db[k1].keys()), notk))
      for k2 in vals:
        a((k1, k2))
    return todeletesingles, todeletepairs

  def getclosestname(self, obj):
    syns=wn.synsets(obj)
    if len(syns)==0:
      raise NoWordnetMatchError(obj)
    sets=[(ed(obj, s.name.split('.')[0]), s) for s in syns]
    sets=sorted(sets, key=lambda x: x[0])
    return sets[0][1].name, sets[0][1]

  def getclosestsyns(self, db):
    k=self.getallobjs(db)
    ktosyns=dict([(k1, None) for k1 in k])
    try:
      for k1 in ktosyns:
        ktosyns[k1], _=self.getclosestname(k1)
    except NoWordnetMatchError:
      print 'ERROR: Run cleanoutput() before getting synsets.'
      ktosyns=False
    return ktosyns
  
  def __init__(self, db=None, parsed=None, totrain=None,
               fparser=fuzzparsetrainfiles, tparser=parsetraindata):
    """Initializes Visuo.

    Keyword Arguments:
    Requires one of...
    db -- string, path to the visuo database made by this class
    parsed -- string, path to parsed database of training files
    totrain -- string, path to folder of training files

    fparser -- function, a parser of the parsed training files database
    tparser -- function, a parser of the training files

    """
    if type(db) == str:
      with open(db, 'rb') as f:
        self.db=load(f)
      print 'Database Loaded'
    else:
      if type(parsed) == str:
        with open(parsed, 'rb') as f:
          train=load(f)
      elif type(totrain) == str:
        train=parsetraindata(totrain)
      else:
        raise NoDatabaseError("""Either a database, parsed training file, or
                                 training files path must be present.""")
      self.db=fuzzparsetrainfiles(train, self.__class__.DIST,
                                  self.__class__.ANGL)
      print 'Database Loaded'
      singles, pairs=self.cleanoutput(self.db)
      for k in singles:
        del self.db[k]
      for k1, k2 in pairs:
        del self.db[k1][k2]
      print 'Database Cleaned'
      
    self.ktosyns=self.getclosestsyns(self.db)

  def getclosestobj(self, ktosyns, obj):
    name, syn=self.getclosestname(obj)
    vals=[(syn.path_similarity(wn.synset(s)), k) for k, s in ktosyns.items()]
    vals=sorted(vals, key=lambda x: x[0], reverse=True)
    return vals[0][1]

  def getangledist(self, db, ktosyns, query, obj):
    """Returns the angle and distance between the query and object.

    Keyword Arguments:
    db -- self.db, the visuo database
    ktosyns -- self.ktosyns, a dictionary of labels to synset names
    query -- string, the query label
    obj -- string, the other object label

    """
    if query in ktosyns:
      q=query
    else:
      q=self.getclosestobj(ktosyns, query)
    if obj in db[query]:
      o=obj
    else:
      ktosyns2=dict([(k, ktosyns[k]) for k in db[query]])
      o=self.getclosestobj(ktosyns2, obj)
    out=db[q][o]
    return defuzz(self.__class__.ANGL, out['angl']), \
           2**defuzz(self.__class__.DIST, out['dist'])


  def calcanglesdists(self, db, ktosyns, query, objs):
    """Makes local file of angles and distances between query and objects.

    Keyword Arguments:
    db -- self.db, the visuo database
    ktosyns -- self.ktosyns, a dictionary of labels to synset names
    query -- string, the query label
    objs -- list, a list of object labels

    """
    f=open(''.join(['FromVisuoToDisplay', query, '.txt']), 'wb')
    f.write(''.join(['#', query, '\n']))
    for obj in objs:
      try:
        angl, dist=self.getangledist(db, ktosyns, query, obj)
      except NoWordnetMatchError as e:
        print 'ERROR:', e.word, 'could not be found in WordNet.'
      else:
        f.write(''.join([query, '-', obj, ' ', str(angl), ' ',
                         str(dist), '\n']))
    f.close()

  def savedb(self, db, filename):
    """Saves visuo database.

    Keyword Arguments:
    db -- self.db, the visuo database
    filename -- string, the path to save the database

    Note: the database only needs to be saved once unless changed.

    """
    with open(filename, 'wb') as f:
      dump(db, f)
  
  

