'''
Created on Sep 8, 2017

@author: Story
'''
from nltk import *
from nltk.corpus import brown
from numpy import *
from tkinter import *
import pickle
import operator
#from nltk.book import *

class boxItems():
    def __init__(self, workspace, refbox):
        self.UserText = StringVar()
        self.RobotOutput = ''
        self.refbox = refbox
        self.workspace = workspace
        self.freqcounter = 0
        self.ngrams = []
    
    def moveText(self):
        self.refbox.delete(0, END)
        L = Label(self.workspace, text=self.UserText)
        L.grid(column=2, columnspan=1)
        
    def getNGrams(self, text):
        self.ngrams=[{},{},{},{},{},{},{},{},{}]
        for i in range(1,10):
            tokenizeMachine = RegexpTokenizer(r'\w+')
            tokens = tokenizeMachine.tokenize(text)
            trash = ngrams(tokens, i)
            for token in trash:
                if token in self.ngrams[i-1]:
                    self.ngrams[i-1][token] += 1
                else:
                    self.ngrams[i-1][token] = 1
            temp = sorted(self.ngrams[i-1].items(), key=operator.itemgetter(1))
            temp.reverse()
            print(str(i)+"grams: "+str(temp))
    
    def writeVariables(self):
        brains = [{},{},{},{},{},{},{},{},{}]
        with open('/Users/Story/Desktop/Word_Data/brains.pickle', 'rb') as handle:
#             for i in range(0,9):
            brains = pickle.load(handle)
                #print(brains[i])
        with open('/Users/Story/Desktop/Word_Data/brains.pickle', 'wb') as handle:
            dumpthis = [{k: brains[i].get(k,0)+self.ngrams[i].get(k,0) for k in list(brains[i].keys())+list(self.ngrams[i].keys())} for i in range(0,9)]
                
            pickle.dump(dumpthis, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.ngrams=[{},{},{},{},{},{},{},{},{}]
        
    def populateBrains(self, corpus):
        self.UserText = corpus
        self.getNGrams(self.UserText)
        self.writeVariables()
    
    def updateText(self, event):
        self.UserText = self.refbox.get()
        self.UserText = self.UserText.lower()
        print(self.UserText)
        self.moveText()
        self.getNGrams(self.UserText)
        self.writeVariables()
        
    def CheckClose(self, win):
        win.getMouse()
        win.close()

class generatedAnswer():
    def __init__(self):
        #USE THIS CLASS AS A POTENTIAL CHILDCLASS OF BOXITEMS
        #GRAB ALL THE INFO FROM BOXITEMS AND USE IT TO GENERATE AN ANSWER
        self.response = ''
        self.smarts = ''
    
    def textGenerator(self,numwords):
        print('--------------------GENERATED TEXT-------------------------')
        #do transmission
        #do blah
        words = ["poundcake"]
        weights = [.1,.1,.2,.7,.5,.4,.2,.1,.1]
        #weights = [.11,.13,.16,.22,.26,.09,.07,.03,.01]
        bweight = .6
        procbuffer = []#[{k[:-1]:(k[-1],v) for k,v in dic.items()} for dic in self.smarts]
        for dic in self.smarts:
            construct = {}
            for k,v in dic.items():
                if k[:-1] in construct.keys():
                    construct[k[:-1]].append((k[-1],v))
                else:
                    construct[k[:-1]] = [(k[-1],v)]
            procbuffer.append(construct)
        for i in range(0,numwords):
            freq = {}
            for n in range(0,9):
                if len(words) < n: 
                    break
                lastn = tuple(words[len(words)-n:])
#                 print(words[len(words)-n:len(words)])
                if lastn in procbuffer[n].keys():
                    sum=0.0
                    for pair in procbuffer[n][lastn]:
                        sum+=pair[1]
                    for pair in procbuffer[n][lastn]:
                        if (pair[0] not in freq.keys()): 
                            freq[pair[0]] = 0
                        freq[pair[0]]+=weights[n]*pair[1]/sum
#             mx=0;
#             chosenword = "FAILURE"
#             for k,v in freq.items():
#                 if v>mx: 
#                     mx=v
#                     chosenword = k
            mx=0;
            acceptable = []
            selected = sorted(freq.values())[0]
            for k,v in freq.items():
                mx+=v;
            rand = random.random()*mx*bweight;
            for v in sorted(freq.values()):
                mx-=v;
                if mx<=0:
                    selected = v;
            for k,v in freq.items():
                if v==selected:
                    acceptable.append(k)
            chosenword = random.choice(acceptable);
            words.append(chosenword)
        print("\t"+" ".join(words))
    
    def loadBrains(self, event):
        print('------------------LOAD BRAINS--------------------')
        #smarts = [{},{},{},{},{},{},{},{},{}]
        with open('/Users/Story/Desktop/Word_Data/brains.pickle', 'rb') as handle:
            self.smarts = pickle.load(handle)
            print(("\n").join(map(str,self.smarts)))
        self.textGenerator(500)
    
def main():
    win = Tk()
    win.title("P.A.U.L.L")
    win.geometry('{}x{}'.format(400, 600))
    win.resizable(width=False, height=False)
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    
    textFrame = Frame(win, width=400, height=480, background="blue")
    textFrame.columnconfigure(1, weight=1)
    textFrame.grid(sticky="new")
    entryFrame = Frame(win, height=40, pady=40,bg="green")
    entryFrame.grid(sticky="sew")
    entryFrame.columnconfigure(1,weight=1)
    
    e = Entry(entryFrame, width=40)
    e.grid(row=0, column=1)
    e.focus_set()
    
    UserGUI = boxItems(textFrame, e)
    e.bind("<Return>", UserGUI.updateText)

    
    Alyce = generatedAnswer()
    win.bind("-", Alyce.loadBrains)
    
    #Initial populatin of brains
    #with open('/Users/Story/Desktop/Word_Data/food.txt', 'r') as handle:
        #text = handle.read()
    #UserGUI.populateBrains(text)
    
    win.mainloop()
    
if __name__ == '__main__':
    main()