"""
AUTHOR:SYED ZUBIN HAFIZ
STUDENT ID: 32227671
VERSION:2.2
"""
from queue import Queue
from collections import deque
import math 

# ------------------------------------------------------------------------------------
#Question 1
class Vertex:
    def __init__(self,id):
        self.id = id
        self.edges = [] 
        self.edgeFromSource = None
        self.edgeToSink = None 
        self.isVisited = False 
        self.previous = None 
        self.demand = 0
    def setDemand(self,demand):
        self.demand = demand
        if(demand<0): # negative demand
            self.edgeFromSource.maxFlow = abs(demand)
            self.edgeToSink.maxFlow = 0
            self.edgeFromSource.residualEdge.maxFlow = abs(demand)
            self.edgeToSink.residualEdge.maxFlow = 0
        elif(demand>0): # positive demand
            self.edgeFromSource.maxFlow = 0
            self.edgeToSink.maxFlow = abs(demand)
            self.edgeFromSource.residualEdge.maxFlow = 0
            self.edgeToSink.residualEdge.maxFlow = abs(demand)
        else: # no demand
            self.edgeFromSource.maxFlow = 0
            self.edgeToSink.maxFlow = 0
            self.edgeFromSource.residualEdge.maxFlow = 0
            self.edgeToSink.residualEdge.maxFlow = 0
    

class Edge:
    def __init__(self,u,v,maxFlow=0,minFlow=0,flow=0,isResidual=False):
        self.u = u
        self.v = v
        self.maxFlow = maxFlow
        self.minFlow = minFlow
        self.flow = flow 
        self.isResidual = isResidual
        if(not isResidual): # handle residual edge
            self.residualEdge = Edge(v,u,maxFlow,minFlow,maxFlow-flow,True)
            self.residualEdge.residualEdge = self
            u.edges.append(self)
            v.edges.append(self.residualEdge)
        else:
            self.residualEdge = None 

class Graph:
    def __init__(self,graphSize):
        self.vertexes = []
        self.networkSource = Vertex(graphSize+1)
        self.networkSink = Vertex(graphSize)
        # connect source and sink to all vertices
        for id in range(graphSize):
            u = Vertex(id)
            self.vertexes.append(u)
            u.edgeFromSource = Edge(self.networkSource,u)
            u.edgeToSink = Edge(u,self.networkSink)
        self.vertexes.append(self.networkSink)
        self.vertexes.append(self.networkSource)
    def reduceMinFlows(self):
        for u in self.vertexes:
            for edge in u.edges:
                if(edge.minFlow!=0 and not edge.isResidual):
                    edge.maxFlow = edge.maxFlow-edge.minFlow
                    edge.residualEdge.maxFlow = edge.residualEdge.maxFlow-edge.residualEdge.minFlow
                    edge.u.setDemand(edge.u.demand+edge.minFlow)
                    edge.v.setDemand(edge.v.demand-edge.minFlow)
    def fordFulkersonIteration(self,source,sink):
        networkQueue = Queue(len(self.vertexes))
        data = (float('inf'),source)
        networkQueue.put(data)
        augment = 0
        source.isVisited = True
        source.previous = None 
        # loop until queue is empty
        while not networkQueue.empty():
            (throughput,u) = networkQueue.get()
            # handle situation where the sink is found
            if(u==sink):
                if(throughput != float('inf')):
                    augment = throughput
                else:
                    augment = 0 
                break 
            # check each adjacent edge and add to queue
            for edge in u.edges:
                if(not edge.v.isVisited and edge.maxFlow - edge.flow > 0):
                    edge.v.previous = edge
                    edge.v.isVisited = True
                    data = (min(throughput,edge.maxFlow - edge.flow),edge.v)
                    networkQueue.put(data)

        edge = sink.previous 
        return self.backtrackAndAugment(edge,augment)
    def backtrackAndAugment(self,edge,augment):
        while edge != None:
            edge.flow += augment 
            edge.residualEdge.flow = edge.maxFlow - edge.flow
            edge = edge.u.previous
        return augment
    def generateNetwork(self):
        self.reduceMinFlows()
        flowIncrease = 0.00001
        maxFlow = 0
        # iterate until iterations no longer increase the flow
        while flowIncrease != 0:
            for u in self.vertexes:
                u.previous = None
                u.isVisited = False 
            flowIncrease = self.fordFulkersonIteration(self.networkSource,self.networkSink)
            maxFlow += flowIncrease
        return maxFlow

class BipartiteDay:
    def __init__(self,dayData,start,people,restaurant,meals,extra,end):
        self.start = start
        self.start.setDemand(-10)
        self.people = people 
        self.restaurant = restaurant 
        self.meals = meals 
        self.extra = extra 
        self.end = end  
        self.breakfastConnections = []
        self.dinnerConnections = []

        # connect people/restaurants to their respective extras
        for i in range(len(self.people)):
            Edge(self.people[i],self.extra[i],2,minFlow=1)
        Edge(self.restaurant,self.extra[-1],2)
        # start to people + restaurant
        for u in self.people:
            Edge(self.start,u,2) 
        Edge(self.start,self.restaurant,2)
        # connect people to meals based on their availability
        for i in range(len(self.people)):
            if(dayData[i] == 1 or dayData[i] == 3):
                edge = Edge(self.people[i],self.meals[0],1) 
                self.breakfastConnections.append((i,edge))
            if(dayData[i] == 2 or dayData[i] == 3):
                edge = Edge(self.people[i],self.meals[1],1)  
                self.dinnerConnections.append((i,edge))
        # allow the possibility of eating out for breakfast and dinner
        self.breakfastConnections.append((5,Edge(self.restaurant,self.meals[0],1)))
        self.dinnerConnections.append((5,Edge(self.restaurant,self.meals[1],1)))
        # connect meals to the end
        for meal in self.meals:
            Edge(meal,self.end,1)


    def breakfastID(self):
        breakfastID = -1
        for (id,edge) in self.breakfastConnections:
            if(edge.flow==1):
                breakfastID = id 
        return breakfastID
    def dinnerID(self):
        dinnerID = -1
        for (id,edge) in self.dinnerConnections:
            if(edge.flow==1):
                dinnerID = id 
        return dinnerID

def allocate(availability):
    "Time complexity : O(n^2)"
    days = len(availability)
    if(days==0):
        return ([],[]) 
    g = Graph(4+16*days)
    # setup the start/end vertex positions, along wih their associated demands
    # 0: start
    # 1: extra start
    # 2: end
    # 3: extra end
    topStart = g.vertexes[0]
    bottomStart = g.vertexes[1]
    topEnd = g.vertexes[2]
    bottomEnd = g.vertexes[3]
    bottomEnd.setDemand(10*days)
    topStart.setDemand(-2)
    topEnd.setDemand(2)

    # create Days 
    dayList = []
    j = 0
    for i in range(4,4+16*days,16):
        #0: start
        #1 - 5: people
        #6: restaurant
        #7 - 8: meals
        #9 - 14: extra
        #15: end
        dayList.append(BipartiteDay(availability[j],g.vertexes[i+0],g.vertexes[i+1:i+6],g.vertexes[i+6],g.vertexes[i+7:i+9],g.vertexes[i+9:i+15],g.vertexes[i+15]))
        j += 1
    
    # connect days
    Edge(topStart,dayList[0].start,2)
    for i in range(days-1):
        Edge(dayList[i].end,dayList[i+1].start,2,2)
    Edge(dayList[-1].end,topEnd,2,2)

    # connect bottom
    for u in dayList[0].extra:
        Edge(bottomStart,u,2*days)
    for i in range(days-1):
        for j in range(6):
            Edge(dayList[i].extra[j],dayList[i+1].extra[j],2*days)


    # calc constraints
    doubleDays = 2*days
    lastDay = dayList[-1]
    for i in range(5):
        Edge(lastDay.extra[i],bottomEnd,doubleDays - math.floor(0.36 * days),doubleDays - math.ceil(0.44 * days))
    Edge(lastDay.extra[5],bottomEnd,doubleDays,doubleDays - math.floor(0.1 * days))

    # run network flow
    g.generateNetwork()
    # check for invalidity
    for edge in g.networkSource.edges:
        if(edge.flow<edge.maxFlow):
            return None 
    # return result
    breakfast = [day.breakfastID() for day in dayList]
    dinner = [day.dinnerID() for day in dayList]
    return (breakfast,dinner)

# ------------------------------------------------------------------------------------
#Question 2 
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



if __name__ == "__main__": # ,[3,2,0,2,2],[0,3,0,3,2]
    availability = [[2, 0, 2, 1, 2], [3, 3, 1, 0, 0],
                    [0, 1, 0, 3, 0], [0, 0, 2, 0, 3],
                    [1, 0, 0, 2, 1], [0, 0, 3, 0, 2],
                    [0, 2, 0, 1, 0], [1, 3, 3, 2, 0],
                    [0, 0, 1, 2, 1], [2, 0, 0, 3, 0]]
    results = allocate(availability)
    print(results)
    
    print(compare_subs("the quick brown fox jumped over the lazy dog","my lazy dog has eaten my homework"))
    print(compare_subs(
        "radix sort and counting sort are both non comparison sorting algorithms",
        "counting sort and radix sort are both non comparison sorting algorithms")) 