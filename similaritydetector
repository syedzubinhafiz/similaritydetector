"""
AUTHOR:SYED ZUBIN HAFIZ
VERSION:2.2
"""
from queue import Queue
from collections import deque
import math 

# ------------------------------------------------------------------------------------
def charToIndex(char):
    # $ = 0, space = 1, a = 2, b = 3, c = 4, ..., z = 28
    if(char=='$'):
        return 0
    elif(char==' '):
        return 1
    else:
        return ord(char) - 97 + 2
def indexToChar(val):
    if(val==0):
        return '$'
    elif(val==1):
        return ' '
    else:
        return chr(val - 2 + 97)

#Node data structure
class Node:
    def __init__ (self,size=28,level=None, data=None):
        self.link = [None]*size
        self.data = data
        self.char = ""
        self.level = level
        self.visitedByStr1 = False 
        self.visitedByStr2 = False 
    
#The Trie data structure
class Trie:
    def __init__(self):
         self.root = Node(level = 0)
         
    def insert(self,key,data=None,currentStr=0):
        count_level = 0
        #begin from root
        current = self.root
        if(currentStr==1):
            current.visitedByStr1 = True 
        elif(currentStr==2):
            current.visitedByStr2 = True 
        #go through the key 1 by 1 
        for char in key:
            # print(current.level)
            #calculate index
            #$ = 0,a =1,b=2,c=3...
            index = charToIndex(char)
            
            #if path exists
            if current.link[index] is not None:
                current = current.link[index]
            #if path doesn't exist
            else:
                #create a new Node
                current.link[index] = Node(level=count_level)
                current = current.link[index]
                current.char = char 
            if(currentStr==1):
                current.visitedByStr1 = True 
            elif(currentStr==2):
                current.visitedByStr2 = True 
                
            count_level = count_level + 1
        
        #go through the terminal $,index = 0
        index = 0
        if current.link[index] is not None:
            current = current.link[index]
        #if path doesn't exist
        else:
                #create a new Node
                current.link[index] = Node(level=count_level)
                current = current.link[index]
                current.char = "$" 
        #add in the payload
        current.data = data
        if(currentStr==1):
            current.visitedByStr1 = True 
        elif(currentStr==2):
            current.visitedByStr2 = True 
             
        
    def search(self,key):
        #begin from root
        current = self.root
        #go through the key 1 by 1 
        for char in key:
            #calculate index
            #$ = 0,a =1,b=2,c=3...
            index = ord(char)-97+1
            #if path exists
            if current.link[index] is not None:
                current = current.link[index]
            #if path doesn't exist
            else:
                return None
        
        #go through the terminal $,index = 0
        index = 0
        if current.link[index] is not None:   
            current = current.link[index]
        #if path doesn't exist
        else:
            return Exception(str(key)+" doesn't exist")
        #at the leaf (terminal)
        return current.data
    def __str__(self):
        return self.strAux(self.root,"|")
    def strAux(self,node,char):
        result = "\n%s (%s,%s)" % (node.char,node.visitedByStr1,node.visitedByStr2)
        i = 0
        for child in node.link:
            if(child!=None):
                result += self.strAux(child,indexToChar(i)).replace("\n","\n  ")
            i += 1
        return result 

class SuffixTrie(Trie):
    def __init__(self,suffixStr1,suffixStr2):
        super().__init__()
        strVal = ""
        i = len(suffixStr1)
        while(i>=0):
            self.insert(strVal,currentStr=1)
            i -= 1
            strVal = suffixStr1[i] + strVal 
        strVal = ""
        i = len(suffixStr2)
        while(i>=0):
            self.insert(strVal,currentStr=2)
            i -= 1
            strVal = suffixStr2[i] + strVal 

class SuffixTree(SuffixTrie):
    "Time complexity & Space complexity: O(N+M^2) "
    def __init__(self,suffixStr1,suffixStr2):
        super().__init__(suffixStr1,suffixStr2)
        self.suffixTrieToTree()
    def suffixTrieToTree(self):
        treeRoot = Node()
        if(self.root.visitedByStr1): treeRoot.visitedByStr1 = True 
        if(self.root.visitedByStr2): treeRoot.visitedByStr2 = True
        q = deque()
        q.append((self.root,treeRoot))
        while(len(q)!=0):
            currentTrieNode, currentTreeNode = q.pop()
            currentTreeNode.char += currentTrieNode.char
            # calculate the number of non-null child nodes of the Trie node
            linkLen = sum([1 for child in currentTrieNode.link if child != None])
            if(linkLen==0):
                pass 
            elif(linkLen==1):
                childTrieNode = [child for child in currentTrieNode.link if child != None][0]
                q.append((childTrieNode,currentTreeNode))
            else:
                i = 0
                for childTrieNode in currentTrieNode.link:
                    if(childTrieNode!=None):
                        childTreeNode = Node()
                        if(childTrieNode.visitedByStr1): childTreeNode.visitedByStr1 = True 
                        if(childTrieNode.visitedByStr2): childTreeNode.visitedByStr2 = True 
                        currentTreeNode.link[i] = childTreeNode
                        q.append((childTrieNode,childTreeNode))
                    i += 1   
        self.root = treeRoot
    def longestSubstring(self):
        return self.longestSubstringAux(self.root).replace("$","")
    def longestSubstringAux(self,node):
        longestSubstr = ""
        for child in node.link:
            if(child!=None and child.visitedByStr1 and child.visitedByStr2):
                childStr = self.longestSubstringAux(child)
                if(len(longestSubstr)<len(childStr)):
                    longestSubstr = childStr
        return node.char + longestSubstr
             
def compare_subs(suffixStr1,suffixStr2):
    "Time and space complexity: O(N+M)"
    tree = SuffixTree(suffixStr1,suffixStr2)
    resultStr = tree.longestSubstring()
    percentStr1 = round(len(resultStr)/len(suffixStr1)*100)
    percentStr2 = round(len(resultStr)/len(suffixStr2)*100)
    return [resultStr,percentStr1,percentStr2]



if __name__ == "__main__":
    
    print(compare_subs("the quick brown fox jumped over the lazy dog","my lazy dog has eaten my homework"))
    print(compare_subs(
        "radix sort and counting sort are both non comparison sorting algorithms",
        "counting sort and radix sort are both non comparison sorting algorithms")) 
