#######################################################################
#
# parse.py
# --------
#
# Description:  Transforms a string representation of a concept into  
#               an actual concept object.
#
# Author:   Jonathan Gagne
#           Institute of Cognitive Science
#           Carleton University
#           jgagne2@connect.carleton.ca
#
# For:      Undergraduate Thesis
# Supervisor: Dr. Jim Davies
#
#######################################################################


#ALWAYS_ENCAP_IN_SIMAGE = True           # whether or not to always scene in an S-Image

class PARSER:

    class TREE:
        def __init__(self, name, parent=None, hasChildren=True):
            
            self.name = name
            self.parent = parent
            if hasChildren:
                self.children = PARSER.get_children(name, self)
            else:
                self.children = []

        # returns list of children
        def get_children(self):
            return self.children
        # returns whether tree has children
        def has_children(self):
            return len(self.children) > 0

        # returns the name of the tree
        def get_name(self):
            return self.name

        # returns parent
        def get_parent(self):
            return self.parent
        # returns whether tree has parent
        def has_parent(self):
            return self.parent != None
        def is_root(self):
            return self.parent == None
        

        # makes tree more compact
        def trim(self):
            # shortest unnecessarily long branches
            while(len(self.children) == 1):                
                if (self.children[0].children) > 0:
                    self.name = self.children[0].name
                    self.children = self.children[0].children

            # recursive call to trim children
            for child in self.children:
                child.trim()

            if self.is_root():
                self.update_name()

        # updates the name of tree
        def update_name(self):
            name = []
            if self.has_children():
                for child in self.children:
                    childname = child.update_name()
                    if childname != None:
                        name.append(childname)
                self.name = "[" + " ".join(name) + "]"

            return self.name
                

        def printtree(self, level=0):
            self.update_name()          # updates the names of the tree
            
            print ".   "*level + self.name
            if self.has_children:
                for child in self.children:
                    child.printtree(level+1)

        def covlan(self, level=0, indent=False):
            self.update_name()          # updates the names of the tree

            if not indent: level = 0
            
            print ".   "*level + self.name.replace(' ', '_')
            if self.has_children:
                for child in self.children:
                    print ".   "*level + self.name.replace(' ', '_') + " HAS-COMPONENT " + child.name.replace(' ', '_')
                    
                for child in self.children:
                    child.covlan(level+1, indent)

        def __str__(self):
            self.update_name()          # updates the names of the tree
            
            return self.name

    @staticmethod
    def build_tree(text):
        text2 = text
        text = PARSER.clean_parsed_text(text)        
        tree = PARSER.TREE(text)
        tree.trim()
        return tree
        

    @staticmethod
    def get_children(text, parent=None):

        ## !!!!!!!!!!  error in this case "[asdf] sdf [erer]"  ->  must be like [[asdf] sdf [erer]]"  !!!!!!!!

        if text[0] == "[" and text[-1] == "]":
            text = text[1:-1]

        children = []

        while(len(text) > 0):
            
            if text[0] == '[':
                pos = 1
                level = 1
                while(level > 0):
                    if text[pos] == '[':
                        level += 1
                    elif text[pos] == ']':
                        level -= 1
                    pos += 1
                children.append(PARSER.TREE(text[:pos], parent))
            else:
                pos = 0
                while(pos < len(text)):
                    if text[pos] == ' ' or text[pos] == '[':
                        break
                    elif text[pos] == ']':
                        break
                    else:
                        pos += 1
                pos += 1
                children.append(PARSER.TREE(text[:pos-1], parent, hasChildren=False))

            text = text[pos:].strip()

        return children


    @staticmethod
    def clean_parsed_text(text):

        # checks bracket structure.
        def check_brackets(text):

            # remove redundant bracketing
            stack = []
            
            level = 0               # current level of tree
            height =  0             # height of tree
            flag = False            # True: exterior brackets required
            
            # checks if brackets are inserted properly and determines height
            for char in text:
                if char == '[':
                    level += 1
                    if level > height: height = level
                elif char == ']':
                    level -= 1
                    if level < 0: raise "Parsing error: Brackets not matched"
                elif level == 0:
                    flag = True
                
                    
            if level != 0:
                print text
                raise "Parsing error: Brackets not matched"

            # adds external brackets if required
            if flag == True:
                text = '[' + text + ']'
                
            return text


        # cleans leading and trailing spaces
        text = text.strip()

        # if string is empty return        
        if len(text) == 0: return text

        # checks brackets
        text = check_brackets(text)

        # removes double spaces, spaces after open brackets and empty brackets (i.e. "[]")
        i = 0
        while(i<len(text)):
            if text[i] == " ":
                # removes spaces at the end
                if i+1 == len(text):
                    text = text[:-1]
                # removes double spaces
                elif text[i+1] == " ":
                    text = text[:i+1] + text[i+2:]
                    i -= 1
                    
            elif text[i] == "[":
                # insures there is a space before bracket (unless at location 0 or preceded by an open bracket)
                if i > 0:
                    if text[i-1] != ' ' and text[i-1] != '[':
                        text = text[:i] + " " + text[i:]
                        i += 1
                # checks if open bracket is that last in the text
                if i+1 >= len(text):
                    raise "Parsing error: Bracket not matched -> Open bracket at end of statement"
                # removes spaces after open brackets
                elif text[i+1] == " ":
                    text = text[:i+1] + text[i+2:]
                    i -= 1
                # removes empty brackets (i.e. "[]")
                elif text[i+1] == "]":
                    text = text[:i] + text[i+2:]
                    # go backwards 3 or 2 if possible, otherwise 1
                    if i > 1:
                        i -= 3
                    elif i > 0:
                        i -= 2
                    else:
                        i -= 1
                        
            elif text[i] == "]":
                # insures there is a space after a closed bracket (except if there is another closed bracket following)
                if i+1 < len(text):
                    if text[i+1] != "]" and text[i+1] != " ":
                        text = text[:i+1] + " " + text[i+1:]
                if i>0:
                    if text[i-1] == " ":
                        text = text[:i-1] + text[i:]
                    
            i +=1

        return text

# example:
# PARSER.clean_parsed_text(" [ big [tree [house ] ]] [above][  [   [ ]]][ small[] tree ]  ")
#
# tree = PARSER.build_tree(" [ big [tree [house ] ]] [above][  [   [ ]]][ small[] tree ]  ")
# tree.covlan()
# tree.printtree()



