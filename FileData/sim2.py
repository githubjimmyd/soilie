################################################
#
#  SIM2 MODULE
# -------------
#
# Description:  * Main Simulation Module *
#               Runs simulation -> Creates a
#               Concept from a visualization
#               phrase.
#
# Author:   Jonathan Gagne
#           Institute of Cognitive Science
#           Carleton University
#           jgagne2@connect.carleton.ca
#
# For:      Undergraduate Thesis
# Supervisor: Dr. Jim Davies
#
################################################
from __future__ import division
#import pdb
#from nltk.wordnet import * #Sterling
from nltk.corpus import wordnet #Sterling
from utilities import *
from parse import *
#from size import *
from attribute_v2 import *                                              #Added _v2 Vinc
from modifier_v2 import *
import cPickle
#import IPython
import time
#ic = nltk.wordnet.load_ic('ic-bnc-resnik.dat')#Sterling
p = [syn.lemma_names for syn in list(wordnet.all_synsets('n'))]
N = []
for x in p:
    for t in x:
        N.append(t)
N = set(N)
N = list(N)

p = [syn.lemma_names for syn in list(wordnet.all_synsets('s'))]
ADJ = []
for x in p:
    for t in x:
        ADJ.append(t)

p = [syn.lemma_names for syn in list(wordnet.all_synsets('v'))]
V = []
for x in p:
    for t in x:
        V.append(t)
p = [syn.lemma_names for syn in list(wordnet.all_synsets('r'))]
ADV= []
for x in p:
    for t in x:
        ADV.append(t)


#EXAMPLE_FILE = "examples.txt"
#EXAMPLE_FILE = "example (from paper).txt"

VERBOSE_LEVEL = -1                   # -1 = print nothing
DEBUGGING = False       # also must uncomment import pdb on line 22

#-------------------------------------
# Preposition init

PREP = []                       # list of prepositions

f = open("prepositions.txt")
for line in f.xreadlines():
    if '#' in line:
        line = line[:line.find('#')]
    line = line.strip()
    if line:
        PREP.append(line)

#-------------------------------------

def output(data, verbose_level=0):
    if VERBOSE_LEVEL >= verbose_level:
        if isinstance(data, (list, dict, tuple)):
            for datum in data:
                print datum,
            print
        else:
            print data


# visualizes a concept
def build_concept(tree):
    return combine_concept(split_concept(tree))


# splits appart a concept
def split_concept(tree):
    output(("split ", tree), 1)

    # if there is a prototype with the same name as the tree structure, return that prototype
    if Prototype.has(tree.get_name()):
        return [Prototype.get(tree.get_name())]

    subconcept = [child for child in tree.get_children()]	# list of all subconcepts
    split_list = []                                             # list of split concepts

    # if the tree is not found and the subconcept list is empty, this means the concept cannot be visualized
    if not subconcept:
        raise "Concept not found and cannot be broken down any further!\nConcept '" + tree.get_name() + "' not found"
    else:
        # iterates through subconcepts
        for c in subconcept:
            # if c is found, add it to split_list
            if Prototype.has(c.get_name()):
                split_list.append(Prototype.get(c.get_name()))

            # if c is not found, attempt to split it and merge what is split
            else:
                split_list.append(combine_concept(split_concept(c)))

        return split_list


# combines a list of concepts
def combine_concept(concepts):
    if not isinstance(concepts, (list, tuple)):
        raise "Invalid 'combine_concept' argument\n" + str(concepts) + " given"

    output(("combine ", concepts),1)
    count = len(concepts)
    if count < 1:
        raise "No concepts to merge"
    elif count == 1:
        output("comb1", 2)
        return concepts[0]
    elif count == 2:
        output("comb2", 2)
        if   (concepts[0].lexical_category == "noun") and (concepts[1].lexical_category != "noun"):
            return merge_concepts2(concepts[0], concepts[1], concepts[0].name + " " + concepts[1].name)
        elif (concepts[0].lexical_category != "noun") and (concepts[1].lexical_category == "noun"):
            return merge_concepts2(concepts[1], concepts[0], concepts[0].name + " " + concepts[1].name)
        else:
            print concepts
            error = "Cannot determine root\n     concept1 = " + concepts[0].lexical_category + "   &   concept2 = " + concepts[1].lexical_category
            ##raise error
    elif count == 3:
        output("comb3", 2)

        if concepts[1].lexical_category == "preposition":
            return merge_concepts3(concepts[0], concepts[1], concepts[2])
        else:
            print concepts[0].lexical_category, concepts[1].lexical_category, concepts[2].lexical_category
            ##raise "Cannot combine a group of tree concepts if concepts are not a noun, preposition, noun respectively"
    else:
        # TODO: Everything for the > 3 case
        raise "Cannot combine concepts of greater then 3"


# merges two concepts together  (c1 = concept1, c2 = concept2)
def merge_concepts2(c1, c2, new_concept_name):

    def modify_or_transform(c1, c2):
        # TODO: implement tranformation detection
        return "modify"

    output(("merge:", c1,c2),1)

    # figures out if the change should be a modification or a transformation
    if modify_or_transform(c1, c2) == "modify":
        return modify(c1, c2, new_concept_name)
    else:
        raise "transform not implemented"

# merges three concepts together
def merge_concepts3(c1, c2, c3):

    def modify_or_transform(c1, c2, c3):
        # TODO: implement tranformation detection
        return "modify"

    output(("merge:", c1,c2,c3),1)

    # figures out if the change should be a modification or a transformation
    if modify_or_transform(c1, c2, c3) == "modify":
        return modify_relation(c1, c2, c3)
    else:
        raise "transform not implemented"



# creates a concept modifier and a new concept from the concept modifier
def modify(c1, c2, new_concept_name):

    # searches for concept candidates
    candidates = search_candidates(c1, c2)

    # finds general source concepts
    sourceHyper = candidates[0][1]

    # finds specific source concept
    sourceHypo  = candidates[0][2]

    # finds general target concept
    targetHyper = c1

    # stores a dictionary of the attributes
    attributes = {}

    # list of potential aattributes
    potential_attributes = []

    output(("\nsource hypernym attributes\n", sourceHyper.attributes, '\n' ), 0)

    # all attributes that are contained in all three concepts are added to the list of potential concepts
    for attrib in sourceHyper.attributes:
        if (attrib in sourceHypo.attributes) and (attrib in targetHyper.attributes):
            potential_attributes.append(attrib)

    # if no potential attributes where found, the concept cannot be created
    if not potential_attributes:
        global concept1
        global concept2
        global cand
        concept1 = c1
        concept2 = c2
        cand = candidates
        ##raise "Cannot compare"

    # creates all the new attributes for the target general concept
    for attrib in potential_attributes:
        targetHypo_attribute  = modify_attribute(sourceHyper.attributes[attrib], sourceHypo.attributes[attrib], targetHyper.attributes[attrib])
        attributes[attrib] = targetHypo_attribute

    #targetHypo_attribute  = modify_attribute(sourceHyper.attributes['size'], sourceHypo.attributes['size'], targetHyper.attributes['size'])
    #attributes['size'] = targetHypo_attribute

    # creates an new exemplar out of the n
    new_exemplar = Exemplar(name=new_concept_name, attributes=attributes, lexical_category='noun', WordNetName=targetHyper.WordNetName, mental_image=True)

    #return Prototype.add(Prototype(new_concept_name))
    return new_exemplar

# finds the appropriate concepts to use as analogies for modify
def search_candidates(c1, c2):
    # makes sure the c1 concept is a noun
    if c1.lexical_category != 'noun':
        raise str("Concept '" + c1.name + "' is of type '" + c1.lexical_category + "'\n Should be type 'noun'")

    # gets the sense fo the word from word net
    if c1.WordNetName.lower() in N:
        ##sense1 = N[c1.WordNetName.lower()][0] #Sterling
        sense1 = wordnet.synsets(c1.WordNetName.lower())[0] #Sterling
    else:
        raise str("Concept '" + c1.name + "' is not a word in wordNet")

    # list of candidates
    candidates = []

    # gets list of nouns
    concepts = Prototype.get_all('noun')

    # runs through each concept
    for c in concepts:
        output(("search -- c2", c2, "c.hypernyms", c.hypernyms),1)
        # checks if c2 is a hypernym of concept c
        if c2 in c.hypernyms and c != c1:
            output(("hypernym ->", c2), 1)
            # checks if any of c's hypernyms are in N
            #cHypernymsWords = [(N[h.name.lower()],h) for h in c.hypernyms if h.lexical_category == 'noun' and h.name.lower() in N]
            cHypernymsWords = [(wordnet.synsets(h.name.lower()),h) for h in c.hypernyms if h.lexical_category == 'noun' and h.name.lower() in N]
            for hypWord, hypConcept in cHypernymsWords:
                # uses the first correct sense
                sense2 = hypWord[0]
                # calculates the similarity and adds it to candidates list
                # NOTE: wup similarity is used, except that it is squared to give extra preference towards similar objects
                candidates.append((pow(sense1.wup_similarity(sense2),2), hypConcept, c))

    # sorts list of candidates
    candidates.sort(reverse=True)

    return candidates
##From here
# in place shift
def step_shift(source, step):
    for i in range(step):
        source.append(source.pop(0))

# in place shift
def substep_shift(source, substep):
    if substep >= 0:
        t0 = source[0]
        for i in range(0, len(source)-1):
            source[i] = source[i]*(1-substep) + source[i+1]*substep
        source[-1] = source[-1]*(1-substep) + t0*substep
    else:
        substep *= -1
        tf = source[-1]
        for i in range(len(source)-1, 0, -1):
            source[i] = source[i]*(1-substep) + source[i-1]*substep
        source[0] = source[0]*(1-substep) + tf*substep


# aligns circular attributes (e.g. angles)
def align_curcular_attribute(target, source):

    def find_substep(target, source, value, step_size, error):
        # recursive end condition
        if step_size < 0.0001:
            #new_source = source[:]
            #substep_shift(new_source, value)
            #return new_source
            return value

        # check plus shift
        source_plus = source[:]
        substep_shift(source_plus, value+step_size)
        p_error = 0
        for vals in zip(target, source_plus):
            p_error += pow(vals[0]-vals[1], 2)

        # check minus shift
        source_minus = source[:]
        substep_shift(source_minus, value-step_size)
        m_error = 0
        for vals in zip(target, source_minus):
            m_error += pow(vals[0]-vals[1], 2)

        # take best out of plus shift, minus shift, and no shift
        if p_error < m_error:
            if p_error < error:
                return find_substep(target, source, value+step_size, step_size/2, p_error)
            else:
                return find_substep(target, source, value, step_size/2, error)
        else:
            if m_error < error:
                return find_substep(target, source, value-step_size, step_size/2, m_error)
            else:
                return find_substep(target, source, value, step_size/2, error)

        ##raise "This line should never run"


    # approximate alignment (find integer number of steps)
    msource = source[:]
    step = 0
    length = len(msource)
    min_step = 0
    min_error = 1000000000

    while step < length:
        error = 0
        for vals in zip(target, msource):
            error += pow(vals[0]-vals[1], 2)
        if error < min_error:
            min_error = error
            min_step = step
        step += 1
        msource.append(msource.pop(0))

    min_source = source[:]
    step_shift(min_source, min_step)

    return (min_step, find_substep(target, min_source, 0, 0.5, min_error))



# creates an attribute from the general source concept, the specific source concept, and the general target concept
def modify_attribute(sourceHyper, sourceHypo, targetHyper, attribute_name=""):

    if (targetHyper.circular):
        (step_shift_val, substep_shift_val) = align_curcular_attribute(targetHyper.degrees_of_membership, sourceHyper.degrees_of_membership)
        sourceHypo_mod = sourceHypo.get_modifier(sourceHyper, step_shift_val, substep_shift_val)
    else:
        # creates an attribute modifier
        sourceHypo_mod = sourceHypo.get_modifier(sourceHyper)

    # creates the new attribute
    targetHypo = MODIFIER.modify(sourceHypo_mod, targetHyper)
    # targetHypo.write_membership_distribution("width&small.dist", "small width (Estimated)")

    return targetHypo

# creates an attribute from the general source concept, the specific source concept, and the general target concept
def modify_attribute(sourceHyper, sourceHypo, targetHyper, attribute_name=""):

    # creates an attribute modifier
    sourceHypo_mod = sourceHypo.get_modifier(sourceHyper)
    #print sourceHypo_mod

    # creates the new attribute
    targetHypo = MODIFIER.modify(sourceHypo_mod, targetHyper)
    # targetHypo.write_membership_distribution("width&small.dist", "small width (Estimated)")

    return targetHypo
##To here
# modifies relation concepts (eg noun, preposition, noun)
def modify_relation(c1, c2, c3):

    # gets list of candidates
    candidates = search_relation_candidates(c1, c2, c3)

    # creates the name of the new concept
    if len(c1.name.split()) > 1:
        name1 = '[' + c1.name + ']'
    else:
        name1 = c1.name
    if len(c2.name.split()) > 1:
        name2 = '[' + c2.name + ']'
    else:
        name2 = c2.name
    if len(c3.name.split()) > 1:
        name3 = '[' + c3.name + ']'
    else:
        name3 = c3.name

    new_concept_name = name1 + " " + name2 + " " + name3

    # selects the source preposition as most relevant candidate
    source = candidates[0][1]

    # creates a dictionary to store the targets attributes
    target_attributes = {}

    # copies attributes from the source to the will be target
    for attrib in source.attributes:
        target_attributes[attrib] = source.attributes[attrib].copy()

    print new_concept_name
    # creates a new exemplar with the attributes from the source
    new_exemplar = Exemplar(name=new_concept_name, attributes=target_attributes, lexical_category='preposition', mental_image=True)

    #return Prototype.add(Prototype(new_concept_name))
    return new_exemplar

# search appropriate relation concepts
def search_relation_candidates(left_concept, relation_concept, right_concept):

    # concept to the left of the preposition
    left = left_concept.WordNetName

    # the preposition
    rel_name = relation_concept.name

    # the concept to the right of the preposition
    right = right_concept.WordNetName

    # gets a list of all possible candidates
    candidates = []
    for c in Prototype.get_all('preposition'):
        score_left = 0
        score_right = 0

        # considers the same concepts in memory but does not need to have the same sense
        if rel_name == c.relation_name:

            # assigns a score to how close the left concept is to the potential left source concept
            # score of 1 if the concept is identical
            if c.relation_left == left: score_left = 1
            else:
                # finds it in the WordNet dictionary
                if left:
                    if left.lower() in N:
                        #sense1 = N[left.lower()][0]  #Sterling
                        sense1 = wordnet.synsets(left.lower(), pos=wordnet.NOUN)[0] #Sterling
                    # error if it cannot be found in the WordNet dictionary
                    else:
                        #IPython.embed()
                        error = "* " + left + " not found in wordnet noun dictionary. \nCannot compare."
                        ##raise error
                # score of 0 if there is no left concept
                else:
                    score_left = 0

                # score from 0 to 1 depending on how close it is semantically
                if c.relation_left.lower() in N and c.relation_left:

                    sense2 = wordnet.synsets(c.relation_left.lower(), pos=wordnet.NOUN)[0]

                    score_left = sense1.wup_similarity(sense2)
                else:
                    score_left = 0

            # assigns a score to how close the right concept is to the potential right source concept
            # score of 1 if the concept is identical
            if c.relation_right == right: score_right = 1
            else:

                # finds it in the WordNet dictionary
                if c.relation_right:
                    # error if it cannot be found in the WordNet dictionary
                    if right.lower() in N:
                        #sense1 = N[right.lower()][0]                    #sterling
                        sense1 = wordnet.synsets(right.lower(), pos=wordnet.NOUN)[0]#sterling

                    else:
                        error = "* " + right + " not found in wordnet noun dictionary. \nCannot compare."
                        ##raise error
                # score of 0 if there is no right concept
                else:
                    score_right = 0

                # score from 0 to 1 depending on how close it is semantically
                if c.relation_right.lower() in N and c.relation_right:
                    #sense2 = N[c.relation_right.lower()][0] #Sterling
                    sense2 = wordnet.synsets(c.relation_right.lower(), pos=wordnet.NOUN)[0] #Sterling
                    score_right = sense1.wup_similarity(sense2)
                else:
                    print str(c.relation_right) + "not found in wordnet noun dictionary. \nCannot compare."
                    score_right = 0

            # candidate score is the left score multiplied by the right score
            candidates.append((score_left*score_right, c))

    # sorts candidates based on score
    candidates.sort(reverse=True)

    # returns list of candidates
    return candidates


# mental representation of a prototype concept
class Prototype:

    concept_list = []                           # stores all created concepts

    # returns all concepts of lexical category.  Blank for all categories
    @staticmethod
    def get_all(category=""):
        if category:
            c_list = []
            for c in Prototype.concept_list:
                if c.lexical_category == category:
                    c_list.append(c)
            return c_list
        else:
            return Prototype.concept_list[:]

    # adds a concept to the concept list and returns prototype. "name" = name of concept to add to
    @staticmethod
    def add(c, name=None, preference=""):

        # if c is an exemplar, find its respective prototype and add it to it
        if isinstance(c, Exemplar):

            # determines name if not specified
            if not name:
                name = c.name

            # gets the respective prototype
            proto = Prototype.get(name)

            # adds exemplar to prototype
            if proto:
                proto.add_exemplar(c)
                return proto

            # if prototypes does not exist, create one and add exemplar to it
            else:
                if preference:
                    proto = Prototype.add(Prototype(name=name, preference=preference, WordNetName=c.WordNetName))      # creates a new prototype
                else:
                    proto = Prototype.add(Prototype(name=name, lexical_category=c.lexical_category, WordNetName=c.WordNetName))      # creates a new prototype
                proto.add_exemplar(c)
                return proto



        # if c is a prototype
        elif isinstance(c, Prototype):
            if Prototype.has(c.name):
                return Prototype.get(c.name)
            else:
                output(("adding prototype:", c),0)
                Prototype.concept_list.append(c)
                return c

        else:
            print c
            print getClass(c)
            ##raise "Invalid concept class in add() function"

    # checks if concept is in concept list
    @staticmethod
    def has(c):
        # if c is just the name of a concept (aka a string)
        if isinstance(c, str):
            found = None
            for concept in Prototype.concept_list:
                if concept.name == c.upper():
                    found = concept
                    break
            return found != None

        # if c is an exemplar
        elif isinstance(c, Exemplar):
            found = None
            for concept in Prototype.concept_list:
                if concept.name == c.name.upper():
                    found = concept
                    break
            return found != None

        # if c is a prototype
        elif isinstance(c, Prototype):
            for concept in Prototype.concept_list:
                if concept.name == c.name.upper():
                    return True
            return False

        else:
            raise "Invalid concept class in has() function"


    # gets a prototype from the concept list given an exemplar
    @staticmethod
    def get(c):
        # if c is just the name of a concept (aka a string)
        if isinstance(c, str):
            found = None
            for concept in Prototype.concept_list:
                if concept.name == c.upper():
                    found = concept
                    break
            return found

        # if c is an exemplar
        if isinstance(c, Exemplar):
            found = None
            for concept in Prototype.concept_list:
                if concept.name == c.name.upper():
                    found = concept
                    break
            return found

        else:
            global test
            test = c
            ##raise "Invalid concept class in get() function"

    def __init__(self, name, lexical_category="", preference=[], WordNetName="", LC_guess = True):
        output(("Building Prototype:", name),1)

        self.name = name.upper()                                # name of the concept
        self.lexical_category = lexical_category                # noun, adjective, etc
        self.attributes = {}
        self.relation_left = ""
        self.relation_name = ""
        self.relation_right = ""
        self._LC_guessed = LC_guess

        if WordNetName:
            self.WordNetName=WordNetName
        else:
            self.WordNetName=self.name

        self.hypernyms = []
        self.exemplars = []

        # creates list of names
        tree = PARSER.build_tree(self.name)
        if tree.has_children():
            names = [child.name.strip() for child in tree.get_children()]
        else:
            names = [self.name.strip()]

        # builds hypernym lists
        if len(names) == 2:
            self.hypernyms.append(Prototype.add(Prototype(name=names[0], preference=ADJ)))
            self.hypernyms.append(Prototype.add(Prototype(name=names[1], preference=N)))
        elif len(names) == 3:
            proto2 = Prototype.add(Prototype(name=names[1], preference=PREP))
            if proto2.lexical_category == "preposition":
                self.hypernyms.append(Prototype.add(Prototype(name=names[0], preference=N)))
                self.hypernyms.append(proto2)
                self.hypernyms.append(Prototype.add(Prototype(name=names[2], preference=N)))
            else:
                self.hypernyms.append(Prototype.add(Prototype(name=names[0], preference=ADJ)))
                self.hypernyms.append(proto2)
                self.hypernyms.append(Prototype.add(Prototype(name=names[2], preference=N)))
        elif len(names) > 3:
            for c_name in names:
                self.hypernyms.append(Prototype.add(Prototype(name=c_name)))

        if not self.lexical_category:
            if preference:
                if self.name.lower() in preference:
                    if preference == N: self.lexical_category = 'noun'
                    elif preference == ADJ: self.lexical_category = 'adjective'
                    elif preference == PREP: self.lexical_category = 'preposition'
                    elif preference == V: self.lexical_category = 'verb'
                    elif preference == ADV: self.lexical_category = 'adverb'
                    output(("Lexical category estimate (WordNet):", self.lexical_category), 1)

            if self.lexical_category: pass
            elif self.name.lower() in N:
                self.lexical_category = 'noun'
                output(("Lexical category estimate (WordNet):", self.lexical_category), 1)
            elif self.name.lower() in ADJ:
                self.lexical_category = 'adjective'
                output(("Lexical category estimate (WordNet):", self.lexical_category), 1)
            elif self.name in PREP:
                self.lexical_category = "preposition"
                output(("Lexical category found to be a preposition (list):", self.lexical_category),1)
            elif self.name.lower() in V:
                self.lexical_category = 'verb'
                #raise "verbs not supported, it is recommended that " + self.name + " is manually added"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                output(("Lexical category estimate (WordNet):", self.lexical_category),1)
            elif self.name.lower() in ADV:
                self.lexical_category = 'adverb'
                #raise "adverbs not supported, it is recommended that " + self.name + "'s lexical \ncategory be manually added\n"
                output(("Lexical category estimate (WordNet):", self.lexical_category),1)
            else:
                # creates list of names
                tree = PARSER.build_tree(self.name)

                if tree.has_children():
                    names = [child.name.strip().lower() for child in tree.get_children()]
                else:
                    names = [self.name.strip().lower()]

                for c_name in names:
                    # replaces best guess with the most recent guess, unless it was previously
                    # a noun - which has the highest priority
                    if c_name in N:
                        self.lexical_category = 'noun'
                    elif c_name in ADJ:
                        if self.lexical_category != 'noun':
                            self.lexical_category = 'adjective'
                    elif c_name in PREP:
                        if self.lexical_category != 'noun':
                            self.lexical_category = "preposition"
                    elif c_name in V:
                        if self.lexical_category != 'noun':
                            self.lexical_category = 'verb'
                    elif c_name in ADV:
                        if self.lexical_category != 'noun':
                            self.lexical_category = 'adverb'

                if self.lexical_category != 'preposition':
                    output(("Lexical category estimate by hypernym (WordNet):", self.lexical_category),1)
                else:
                    output(("Lexical category estimated by hypernym found as a preposition (list):", self.lexical_category),1)
                if self.lexical_category != 'noun':
                    output(("*** Note: there is likely an error here, it is recommended that " + self.name + "'s lexical \ncategory be manually added\n"),0)

        # creates list of names
        tree = PARSER.build_tree(self.name)
        if tree.has_children():
            split_names = [child.name.strip() for child in tree.get_children()]
        else:
            split_names = [self.name.strip()]
        #split_names = self.name.split()

        if self.lexical_category == "preposition":
            if len(split_names) == 1:
                self.relation_left = ""
                self.relation_name = split_names[0]
                self.relation_right = ""
            elif len(split_names) == 3:
                self.relation_left = split_names[0]
                self.relation_name = split_names[1]
                self.relation_right = split_names[2]
                self.hypernyms.append(Prototype.add(self, self.relation_name))
            else:
                raise self.name + "Not a valid relation"



    # adds an exemplar to prototype
    def add_exemplar(self, c):

        if self._LC_guessed and not c._LC_guessed:
            self.lexical_category = c.lexical_category
        elif not self.lexical_category:
            self.lexical_category = c.lexical_category
            self._LC_guessed = True

        if c not in self.exemplars:
            self.exemplars.append(c)

            output(("----------------------------------------------"), 0)
            output((self),0)
            for attrib_type in c.attributes:
                if attrib_type not in self.attributes:
                    #attrib_instance = eval(attrib_type.upper())()
                    attrib_instance = ATTRIBUTE(type=attrib_type.upper())
                    attrib_instance.add_attribute(c.attributes[attrib_type])
                    if VERBOSE_LEVEL > -1:
                        attrib_instance.output()
                    self.attributes[attrib_type] = attrib_instance
                else:
                    self.attributes[attrib_type].add_attribute(c.attributes[attrib_type])
                    if VERBOSE_LEVEL > -1:
                        print self.attributes[attrib_type].output()

    # prints string representation
    def __repr__(self):
        if self.lexical_category:
            return self.name + " (" + self.lexical_category + ")"
        else:
            return self.name + " (N/A)"

# mental representation of an exemplar concept
class Exemplar:

    exemplar_list = []

    # constructor
    def __init__(self, name="", secondary_names=[], attributes = {}, lexical_category="", example_attributes={}, WordNetName="", preference="", LC_guess = True, mental_image=False):

        self.name = name.lower()                                # name of the concept
        if WordNetName:
            self.WordNetName = WordNetName
        else:
            self.WordNetName = self.name
        self.secondary_names = secondary_names                  # alternative names for the concept
        self.lexical_category = lexical_category                # noun, adjective, etc
        self.temp_attributes = example_attributes.copy()               # just for implementation
        self.relation_name = ""
        self.relation_left = ""
        self.relation_right = ""
        self.attributes = attributes.copy()
        self._LC_guessed = LC_guess
        for attrib_type in self.temp_attributes:
            # TEMP SOLUTION: NEXT LINE COMMENTED OUT AND REPLACE WITH A SIZE INSTANCE
            #attrib_instance = eval(attrib_type.upper())()
            attrib_instance = ATTRIBUTE(type=attrib_type.upper())
            attrib_instance.fuzzify(self.temp_attributes[attrib_type])
            #attrib_instance.output()
            self.attributes[attrib_type] = attrib_instance

        # if a mental image is being created and a prototype of the examplar exists,
        # copy properties from prototype to the exemplar that do not currently exist in the exemplar
        if mental_image:
            print "Mental image being created"
            if Prototype.has(self.WordNetName):
                proto = Prototype.get(self.WordNetName)
                for attrib in proto.attributes:
                    if attrib not in self.attributes:
                        print attrib + "  copied from <" + proto.name + "> prototype to <" + self.name + "> exemplar"
                        self.attributes[attrib] = proto.attributes[attrib].copy()
                    else:
                        print attrib + "  not copied from <" + proto.name + "> prototype  to <" + self.name + "> exemplar"



        self.hypernyms = []                  # hypernym concepts links  *note: name must be split by spaces, if not, change this line

        # if a lexical category is not provided, attempt to automatically determine it
        if not lexical_category:
            #self._determine_lexical_category(preference)
            pass

        if Prototype.has(self.name):
            proto = Prototype.get(self.name)
            self.lexical_category = proto.lexical_category
            if not proto._LC_guessed:
                self._LC_guessed = False
                output(("Lexical category found (Prototype):", self.lexical_category),1)
            else:
                output(("Lexical category estimate (Prototype):", self.lexical_category),1)

        # creates list of names
        #split_names = self.name.split()
        tree = PARSER.build_tree(self.name)
        if tree.has_children():
            split_names = [child.name.strip() for child in tree.get_children()]
        else:
            split_names = [self.name]

        if self.lexical_category == "preposition":
            if len(split_names) == 1:
                self.relation_left = ""
                self.relation_name = split_names[0]
                self.relation_right = ""
                self.hypernyms.append(Prototype.add(self, self.relation_name))
            elif len(split_names) == 3:
                self.relation_left = split_names[0]
                self.relation_name = split_names[1]
                self.relation_right = split_names[2]
                self.hypernyms.append(Prototype.add(self, self.relation_name))
                self.hypernyms.append(Prototype.add(self))
            else:
                raise self.name + " Not a valid relation"

        # builds hypernym lists
        self.hypernyms.append(Prototype.add(self))
        # only splits it up if it is not a relation
        if self.lexical_category != "preposition":
            if len(split_names) > 1:
                for (c_name, c_cat) in zip(split_names, get_category_list(split_names)) :
                    self.hypernyms.append(Prototype.add(self, c_name, preference=c_cat))

        # builds hypernym list from secondary names
        for sec_name in self.secondary_names:
            self.hypernyms.append(Prototype.add(self, sec_name))
            # only splits it up if it is not a relation
            if self.lexical_category != "preposition":
                # creates list of names
                tree = PARSER.build_tree(self.name)
                if tree.has_children():
                    sec_names = [child.name.strip() for child in tree.get_children()]
                else:
                    sec_names = [self.name.strip()]
                #split_names = sec_name.split()
                if len(split_names) > 1:
                    for (c_name, c_cat) in zip(split_names, get_category_list(split_names)) :
                        self.hypernyms.append(Prototype.add(self, c_name, preference=c_cat))

        # precise attributes decay
        self.temp_attributes = []

        # adds exemplar to list of all exemplars
        Exemplar.exemplar_list.append(self)


    #def add_attribute(self, name, attribute):
    #    self.attributes[name] = attribute

    def _determine_lexical_category(self):

        #split_name = self.name.split()
        # creates list of names
        tree = PARSER.build_tree(self.name)
        if tree.has_children():
            split_names = [child.name.strip() for child in tree.get_children()]
        else:
            split_names = [self.name.strip()]

        if len(split_names) == 3:
            if split_name[1] in PREP:
                self.lexical_category = "preposition"
                output(("Lexical category found as a preposition (list):", self.lexical_category),0)

        if Prototype.has(self.name):
            proto = Prototype.get(self.name)
            self.lexical_category = proto.lexical_category
            if not proto._LC_guessed:
                self._LC_guessed = False
                output(("Lexical category found (Prototype):", self.lexical_category),1)
            else:
                output(("Lexical category estimate (Prototype):", self.lexical_category),1)
        else:
            # creates list of names
            tree = PARSER.build_tree(self.name)
            if tree.has_children():
                names = [child.name.strip() for child in tree.get_children()]
            else:
                names = [self.name.strip()]

            #if len(names) == 1:
            #    if preference:


            for c_name in names:
                if Prototype.has(c_name):
                    # gets the category of the word
                    category = Prototype.get(c_name).lexical_category

                    # replaces best guess with the most recent guess, unless it was previously
                    # a noun - which has the highest priority
                    if self.lexical_category != 'noun':
                        self.lexical_category = category
                    if category == 'noun':
                        self.lexical_category = category
                        self._LC_guessed = False
            output(("Lexical category estimate (Hypernym Prototype):", self.lexical_category),1)


        if not self.lexical_category:
            if self.name.lower() in N:
                self.lexical_category = 'noun'
                output(("Lexical category estimate (WordNet):", self.lexical_category),1)
            elif self.name.lower() in ADJ:
                self.lexical_category = 'adjective'
                output(("Lexical category estimate (WordNet):", self.lexical_category),1)
            elif self.name in PREP:
                self.lexical_category = "preposition"
                output(("Lexical category found to be a preposition (list):", self.lexical_category),1)
            elif self.name.lower() in V:
                self.lexical_category = 'verb'
                ##raise "verbs not supported, it is recommended that " + self.name + " is manually added"
                output(("Lexical category estimate (WordNet):", self.lexical_category),1)
            elif self.name.lower() in ADV:
                self.lexical_category = 'adverb'
                ##raise "adverbs not supported, it is recommended that " + self.name + "'s lexical \ncategory be manually added\n"
                output(("Lexical category estimate (WordNet):", self.lexical_category),1)
            else:
                # creates list of names
                tree = PARSER.build_tree(self.name)
                if tree.has_children():
                    names = [child.name.strip().lower() for child in tree.get_children()]
                else:
                    names = [self.name.strip().lower()]
                #names = [n.lower() for n in self.name.split()]
                for c_name in names:
                    # replaces best guess with the most recent guess, unless it was previously
                    # a noun - which has the highest priority
                    if c_name in N:
                        self.lexical_category = 'noun'
                    elif c_name in ADJ:
                        if self.lexical_category != 'noun':
                            self.lexical_category = 'adjective'
                    elif c_name in PREP:
                        if self.lexical_category != 'noun':
                            self.lexical_category = "preposition"
                    elif c_name in V:
                        if self.lexical_category != 'noun':
                            self.lexical_category = 'verb'
                    elif c_name in ADV:
                        if self.lexical_category != 'noun':
                            self.lexical_category = 'adverb'

                if self.lexical_category != 'preposition':
                    output(("Lexical category estimate by hypernym (WordNet):", self.lexical_category),1)
                else:
                    output(("Lexical category estimated by hypernym found as a preposition (list):", self.lexical_category),1)
                if self.lexical_category != 'noun':
                    output(("*** Note: there is likely an error here, it is recommended that " + self.name + "'s lexical \ncategory be manually added\n"),0)

        if not self.lexical_category:
            if self.name in PREP:
                self.lexical_category = "preposition"
                output(("Lexical category found as a preposition (list):", self.lexical_category),0)

    # prints string representation
    def __repr__(self):
        if self.lexical_category:
            return self.name + " (" + self.lexical_category + ")"
        else:
            return self.name + " (N/A)"

def get_category_list(split_names):
    category_list = []     # list of lexical categories for each word in the phrase
    if len(split_names) == 1:
        category_list.append(self.lexical_category)
    elif len(split_names) == 2:
        leftN = False
        leftA = False
        rightN = False
        rightA = False

        if split_names[0] in N:
            leftN = True
        if split_names[0] in ADJ:
            leftA = True
        if split_names[1] in N:
            rightN = True
        if split_names[1] in ADJ:
            rightA = True

        if (not leftN and not leftA):
            print split_names
            ##raise "Cannot determine left concept"
        elif (not rightN and not rightA):
            print split_names
            ##raise "Cannot determine right concept"
        elif (not leftN and not rightN):
            print split_names
            ##raise "One concept needs to be a noun"
        elif (not leftA and not rightA):
            print split_names
            ##raise "Once concept needs to be an adjective"
        elif (leftN and leftA and rightN and rightA):
            category_list.append(ADJ)
            category_list.append(N)
        elif (leftN and not leftA and rightN and rightA):
            category_list.append(N)
            category_list.append(ADJ)
        elif (not leftN and leftA and rightN and rightA):
            category_list.append(ADJ)
            category_list.append(N)
        elif (leftN and leftA and not rightN and rightA):
            category_list.append(N)
            category_list.append(ADJ)
        elif (leftN and leftA and rightN and not rightA):
            category_list.append(ADJ)
            category_list.append(N)
        elif (leftA and rightN):
            category_list.append(ADJ)
            category_list.append(N)
        elif (leftN and rightA):
            category_list.append(N)
            category_list.append(ADJ)
        else:
            print leftN, leftA, rightN, rightA
            print split_names
            ##raise "check print out"
    elif len(split_names) == 3 and split_names[1].lower() in PREP:
        category_list.append(N)
        category_list.append(PREP)
        category_list.append(N)
    elif len(split_names) < 1 :
        ##raise "Invalid phrase: phrase less then 1"
        print split_names
    else:
        print split_names
        for name in split_names[:-1]:
            category_list.append(ADJ)
        category_list.append(N)
    print split_names

    return category_list

class Example_code:
    def __init__(self, name):
        self.name = name
        self.secondary_names = []
        self.lexical_category = ""
        self.attributes = {}

    def output(self):
        print "================="
        print self.name
        print self.secondary_names
        print self.lexical_category
        print "attributes:"
        for attrib in self.attributes:
            print attrib
        print "-----------------"


    # builds exemplar
    def create_exemplar(self):
        secondary_names = [e.lower() for e in self.secondary_names]
        if self.lexical_category:
            LC_guess = False
        else:
            LC_guess = True
        Exemplar(name=self.name, secondary_names=secondary_names, example_attributes=self.attributes, lexical_category=self.lexical_category, LC_guess=LC_guess)


def create_examples(filename):
    global examples
    f = open(filename, 'r')
    current_example = None
    examples = []
    print time.clock()#Here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    for line in f.xreadlines():

        if "#" in line: line = line[:line.find('#')]
        line = line.strip()
        if line:
            if '=' in line:
                left  = line[:line.find('=')].strip().lower()
                right = line[line.find('=')+1:].strip()
                if not left or not right:
                    raise "Invalid example"

                #print left
                if left == 'name':
                    exec(line)
                    current_example = Example_code(name)
                    examples.append(current_example)
                elif current_example:
                    if left == "secondary_names":
                        current_example.secondary_names = eval(right)
                    elif left == "lexical_category":
                        current_example.lexical_category = eval(right)
                    else:
                        current_example.attributes[left] = eval(right)

    print("Done examples. We have "+ str(len(examples)) + " examples.")
    x = 0
    for example in examples:
        example.create_exemplar()
        #print time.clock()#Here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print plu
        if (x % int(len(examples) / 10)) == 0:
            print int(100-(float(x)/len(examples)*100))
            print time.clock()
        #failSafe.write(Prototype.name)
        x = x+1
    print("Done examplar. We have " + str(len(Exemplar.exemplar_list)) + " exemplar and "+ str(len(Prototype.concept_list))+ " prototypes.")
    print("This took "+str(time.clock())+" seconds.")
    #picklingfile = open("savefile_ultimate.txt", "wb")
    #cPickle.dump(Prototype.concept_list, picklingfile)#fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    #picklingfile.close()
if __name__ == '__main__':

    if DEBUGGING:
        pdb.set_trace()
    #failSafe = open("failSafe.txt", "wb")
    print('Load a file?')
    #loadOrNot = input()
    loadOrNot = "n"
    if loadOrNot == "y":
        print('Name of the file')
        picklingfile = open("savefile_take5.txt", "rb")
        Prototype.concept_list = cPickle.load(picklingfile)
        picklingfile.close()
##    else:
##        print("Please chose a name for the savefile")
##        picklingfile = input()
    print("Are we training anything?")
    TRAINING = "y"
    if TRAINING == "y":
        print("Please input examplefile name.")
        EXAMPLE_FILE = "newfiletake5.txt"
        print('Would you like to get the output?')
        OUTPUT = "y"
        create_examples(EXAMPLE_FILE)
    else:
        OUTPUT = "y"

    # tree = parsed statement as a tree representation
    # concept_dict = dictionary of all concept names and concepts

    # searches tree to find all concept and then excites them
    # take into consideration context

    # excite_all_found_concepts(tree)

    #tree = PARSER.build_tree("[big square] above tree")
    #tree = PARSER.build_tree("large square")
    #tree = PARSER.build_tree("raven above tree")
    #tree = PARSER.build_tree("large city")
    #tree = PARSER.build_tree("[bright [large [large raven]]] above [dark [small tree]]")
    #tree = PARSER.build_tree("[bright [large [large raven]]]")
    #tree = PARSER.build_tree("[bright [long [large raven]]]")
    #tree = PARSER.build_tree("[large raven] above [small tree]")
    #tree = PARSER.build_tree("large [large [large raven]]" )
    #tree = PARSER.build_tree("[large raven]" )
    #

    # one from conference paper
    if OUTPUT == "y":
        tree = PARSER.build_tree("[[an] above sky]")

        complete_concept = build_concept(tree)
        print "------------------------------------------------------------"
        print
        print "Concepts:"
        #print Prototype.concept_list
        print
        print "Build concept of: ", tree
        print complete_concept
        for attrib in complete_concept.attributes:
            print complete_concept.attributes[attrib].output()
            print "Defuzz value:", complete_concept.attributes[attrib].defuzzify()
            print
    #print complete_concept.attributes['size'].output()
    #print "Defuzz value:", complete_concept.attributes['size'].defuzzify()


### TODO: complete_concept.name is a bunch of word with no bracketing
###       e.g. BIG SQUARE ABOVE TREE
###       Make it so it works with brackets
