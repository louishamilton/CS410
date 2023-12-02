
import os
from tkinter import *
from collections import defaultdict




class Search:

    def __init__(self):# this function reads and indexes files


        self.invertedindex = invertedindex = defaultdict(list)
        self.list1 = list1 = []
        self.titlelist = titlelist= []

        #resturant folder in the same path as the script
        self.filelocations = os.path.join(os.path.dirname(__file__), "restaurants")
        if not os.path.exists(self.filelocations):
            messagebox.showerror("Error", "Restaurant folder does not exist")
            exit()

        os.chdir(self.filelocations) #make the program read files from the specified path

        for eachfile in os.listdir(): #for every file in the folder

            with open(eachfile, "r") as r: #open the file
                self.list1.append(r.read()) #append the contents of the file to list1

                    
        for eachdoccontent in list1: #for each batch of text in a file
            tokens = eachdoccontent.split() #split all text into tokens

            for eachtoken in tokens: #for each token in a file

                lowercasewords = eachtoken.lower() #lowercase each token before indexing
                removed_1 = lowercasewords.replace(".","") #remove "." before indexing
                removed_2 = removed_1.replace(",", "")  # remove "," before indexing
                removed_3 = removed_2.replace("and", "")  # remove "and" before indexing
                removed_4 = removed_3.replace("the", "")  # remove "the" before indexing

                if list1.index(eachdoccontent) not in invertedindex[removed_4]: #if a document number is not a value for a particular token
                    invertedindex[removed_4].append(list1.index(eachdoccontent)) #add that document number as a value for that token



    def searchindex(self,query,location): #this function queries the inverted index

        querylen = len(query.split())
        resultlist = []
        for eachqueryterm in query.split():#split all query terms

            lowercasequery = eachqueryterm.lower()#lowercase the user query
            query_remove_1 = lowercasequery.replace(".","")#remove "." from user query
            query_remove_2 = query_remove_1.replace(",", "") #remove "," from user query
            if eachqueryterm == "and": #remove "and" from user query
                querylen = querylen - 1
            if eachqueryterm == "the": #remove "the" from user query
                querylen = querylen - 1

            for item in self.invertedindex[query_remove_2]: #for every item in the inverted index for a query term
                resultlist.append(item) #append each item to result list

        rankdict = {}
        for item in resultlist:    #for each item in the result list
            if item in rankdict:    #if the item is in the rankdict
                rankdict[item] = rankdict[item] + 1 #increase the count by 1
            else:
                rankdict[item] = 1 #if not, then assign 1

        for item in rankdict:
            rankdict[item] = rankdict[item] / querylen #calculating the relavance score

        ranklist = (sorted(rankdict, key=rankdict.get, reverse = True))#this sorts the dictionary by value


        totalcounter = 1
        relloccounter = 0
        guilist = []
        # this is the output if at least 1 word of the query is in a document
        for item in ranklist:
            #print the first line in the file and the relevance score
            #print(self.list1[item].split("\n")[0],": relevance "+str(round(rankdict[item]*100,3)) + "%")
            if location != "":
                if self.list1[item].split("\n")[1] == location :
                    guilist.append("#"+ str(totalcounter) + " " +self.list1[item].split("\n")[0] + ", LOC: " + self.list1[item].split("\n")[1] + ", relevance: "+str(round(rankdict[item]*100,3)) + "%")
                    relloccounter = relloccounter + 1
                else:
                    guilist.append("Location Filter Applied")

            if location == "":
                guilist.append("#"+ str(totalcounter) + " "  +self.list1[item].split("\n")[0] + ", LOC: " + self.list1[item].split("\n")[1] + ", relevance: " + str(round(rankdict[item] * 100, 3)) + "%")
            totalcounter = totalcounter + 1
        # this is the output if no words of the query are in any documents
        if len(ranklist) == 0:
            #print("No words in any document matched your query.")

            guilist.append("No words in any document matched your query.")


        return guilist, totalcounter-1, relloccounter


gui = Tk()
gui.geometry("850x600")
gui.title('The Restaurant Selector')

titlelabel = Label(gui, text="What do you feel like eating today?",font=("Times", 21))
titlelabel.pack()

inputtxt = Text(gui, width=40,height=5)
inputtxt.pack()

filterlabel = Label(gui, text="(Optional) Please enter a city name and the first two letters of the state. eg. Urbana IL",font=("Times", 8))
filterlabel.pack()

filterlabel2 = Label(gui, text="NOTE: The format must exactly match the format of the example.",font=("Times", 8))
filterlabel2.pack()

locationtxt = Entry(gui, width=20)
locationtxt.pack()

resultslabel = Label(gui, text="Results",font=("Times", 12))
resultslabel.pack()

results = Text(gui, width=95,height=24)
results.pack()


def guifunction():

    location = locationtxt.get()

    gettext = inputtxt.get("1.0", "end")

    results.insert("1.0", "\nYour Query: "+gettext)

    for item in Search().searchindex(gettext,location)[0].__reversed__():
        results.insert("1.0", "\n" + str(item))

    results.insert("1.0", "\n" + str(Search().searchindex(gettext, location)[2]) + " relevant to your specified location")
    results.insert("1.0", "\n" + str(Search().searchindex(gettext, location)[1]) + " total results returned")



searchbutton = Button(gui, text ="Find Restaurants", command = guifunction)
searchbutton.place(x=70,y=60)


gui.mainloop()
