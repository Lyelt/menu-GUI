#Program that organizes food choices
#Can read a file to organize into food and ingredients
#Can append items to the File
#Can display the whole menu, organize by categories, or filter
#Can enter ingredients on hand and filter items that have that ingredient
import sys
import tkinter
import tkinter.messagebox
from tkinter.constants import LEFT
#-------------------------------------------------------------------------------
class ingredient :
    def __init__(self, name = "", category = "Miscellaneous") :
        self.name = name
        self.category = category
    
    def __str__(self) :
        return self.name
    
    def printI(self) :
            print(self.name)

#-------------------------------------------------------------------------------        
class menuItem :
    #Is made of a dictionary, where (name:set of ingredients) is (key:value)
    def __init__(self, name = "", ingredients = set()) :
        self.item = {}
        self.name = name
        self.ingredients = ingredients
        self.item[name] = ingredients
    
    def __str__(self) :
        result = ""
        for i in self.ingredients :
            result = result + str(i) + "\n"
        return (self.name + "\n" + result)
    
    def printItem(self) :
        print("Name: " + self.name)
        for i in self.ingredients :
            i.printI()
    
    def getItem(self) :
        return self.name
    
#-------------------------------------------------------------------------------  
class menu :
    #Consists of a name, ie. "Stephanie's Foods"
    #A filename to read from, ie. "menu.txt"
    #And a list of all of the menuItems
    def __init__(self, name, file) :
        #print("Name = " + name + " and file = " + file)
        self.name = name
        self.menuItems = []
        self.readFile(file)
        
    #Create a menuItem object and add it to the master list
    def addMenuItem(self, name, ingSet) :
        menuitem = menuItem(name, ingSet)
        self.menuItems.append(menuitem)
    
    def makeMenu(self, file) :
        lineList = file.read().splitlines()
        ingSet = set()
        name = ""
        for line in lineList :
            if not str(line).find("===") == -1 :
                self.addMenuItem(name, ingSet)
                ingSet = set()
            elif str(line).strip().startswith("-") :
                ing = ingredient(line.strip("- "))
                ingSet.add(ing)
            else :
                index = line.find("(")
                name = str(line[0:index])
            
    #Open file for reading.
    def readFile(self, file) :
        try :
            fileObj = open(file, "r")
        except FileNotFoundError :
            print(file + " not found.")
        
        self.makeMenu(fileObj)
        fileObj.close()
        
    def printMenu(self, filt = "none") :
        if filt == "none" :
            result = ""
            for item in self.menuItems :
                result = result + str(item) + "\n"
                print(result)
        
    def getNames(self, filt = "full") :
        result = ""
        results = []
        if filt == "full" :
            for item in self.menuItems :
                result = item.getItem()
                results.append(str(result))
            return results
        
#-------------------------------------------------------------------------------          

def baseWindow (title = "Menu") :
    base = tkinter.Tk()
    base.title(title)
    base.lift()
    base.rowconfigure(0, weight=1)
    base.rowconfigure(1, weight=2)
    base.columnconfigure(0, weight=1)
    base.columnconfigure(1, weight=1)
    base.columnconfigure(2, weight=1)
    base.config(height=500, width = 700, bg = "white")
    base.minsize(width = 700, height = 500)
    return base

def showMainScreen (base, menu) :
    fullMenu = tkinter.Button(base, text="Full Menu", command = lambda: showMenu("full", fullMenu))
    fullMenu.grid(row=0, column=0, sticky="nwe")
    fullMenu.config(bg="white", padx = 5)
    enterIng = tkinter.Button(base, text="Enter Ingredients")
    enterIng.grid(row=0, column=1, sticky="nwe")
    enterIng.config(bg="white", padx = 5)
    addItem = tkinter.Button(base, text="Add Item", command = lambda: addMenuItem())
    addItem.grid(row=0, column=2, sticky="nwe")
    addItem.config(bg="white", padx = 5)
    
def showMenu(filt, parent) :
    menuWindow = tkinter.Listbox(base, bg = "white")
    menuWindow.grid(row=0, column = 0)
    
    nameList = newMenu.getNames(filt)
    for name in nameList :
        menuWindow.insert(len(nameList), name)

def addMenuItem() :
    #item = tkinter.StringVar()
    addItemField = tkinter.Entry(base, width = 20)
    addItemField.grid(row=0, column=1)
    addItemField2 = tkinter.Entry(base, width = 20)
    addItemField2.grid(row=1, column=1)

newMenu = menu("For Stephanie", "menu.txt")
base = baseWindow()
showMainScreen(base, menu)
base.mainloop()