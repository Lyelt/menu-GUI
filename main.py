#Program that organizes food choices
#Can read a file to organize into food and ingredients
#Can append items to the File
#Can display the whole menu, organize by categories, or filter
#Can enter ingredients on hand and filter items that have that ingredient

import sys
import tkinter
import tkinter.messagebox
from tkinter.constants import LEFT
from tkinter import *
from tkinter.font import Font
#-------------------------------------------------------------------------------
#---Ingredient: Has a name and a category
class ingredient :
    def __init__(self, name = "", category = "Miscellaneous") :
        self.name = name
        self.category = category
    
    def __str__(self) :
        return self.name.strip(" -\t")
    
    def printI(self) :
            print(self.name)

#-------------------------------------------------------------------------------
#---MenuItem: Has two parts, a name and a set of ingredients. Data struct
#---is dictionary.        
class menuItem :
    #Is made of a dictionary, where (name:set of ingredients) is (key:value)
    def __init__(self, name = "", ingredients = set()) :
        self.item = {}  #Dictionary itself
        self.name = name    #Name
        self.ingredients = ingredients #Set of ingredients
        self.item[name] = ingredients #Initialize dictionary
    
    def __str__(self) :
        result = ""
        for i in self.ingredients :
            result = result + str(i) + "\n"
        return (self.name + "\n" + result)
    
    def printItem(self) :
        print("Name: " + self.name)
        for i in self.ingredients :
            i.printI()
    
    #Return the name of the item
    def getItem(self) :
        return self.name

#-------------------------------------------------------------------------------
#---Menu: Name is a string, file is text file to read from  
class menu :
    #Consists of a name, ie. "Stephanie's Foods"
    #A filename to read from, ie. "menu.txt"
    #And a list of all of the menuItems
    def __init__(self, name = "Menu", file = "menu.txt") :
        #print("Name = " + name + " and file = " + file)
        self.name = name
        self.menuItems = []
        self.fileName = file
        self.readFile(file)
        
    #Create a menuItem object and add it to the master list
    def addMenuItem(self, name, ingSet) :
        item = menuItem(name, ingSet)
        self.menuItems.append(item)
        self.writeFile()
    
    def writeFile(self) :
        writeObj = open(self.fileName, "w")
        for item in self.menuItems :
            s = item.getItem()
            writeObj.write(s + "\n")
            for ing in item.ingredients :
                writeObj.write("\t- " + str(ing) + "\n")
            writeObj.write("=========================\n")
        writeObj.close()
    
    def makeMenu(self, file) :
        lineList = file.read().splitlines()
        ingSet = set()
        name = ""
        for line in lineList :
            # If the line is a separator "===", add the previously collected data
            if not str(line).find("===") == -1 :
                self.addMenuItem(name, ingSet)
                ingSet = set()
            # If the line has a "-", it is an ingredient. Add to set
            elif str(line).strip().startswith("-") :
                ing = ingredient(line.strip("- "))
                #print("Ingredient found: " + str(ing))
                ingSet.add(ing)
            # Otherwise, it's the name of the ingredient
            else :
                name = str(line)
                #print("Item found: " + name)
            
    #Open file for reading.8
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
#---Create the base window
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

#-------------------------------------------------------------------------------
#---Initialize top buttons
def showMainScreen (base, menu) :
    frame2 = tkinter.Frame(base, width = 25, height = 400, bg="white")
    frame2.grid(row = 0, column = 1)
    frame3 = tkinter.Frame(base, width = 25, height = 400, bg="white")
    frame3.grid(row = 0, column = 2)
    fullMenu = tkinter.Button(base, text="Full Menu", command = lambda: showMenu("full", fullMenu, frame2))
    fullMenu.grid(row=0, column=0, sticky="nwe")
    fullMenu.config(bg="white", padx = 5)
    enterIng = tkinter.Button(base, text="Enter Ingredients")
    enterIng.grid(row=0, column=1, sticky="nwe")
    enterIng.config(bg="white", padx = 5)
    addItem = tkinter.Button(base, text="Add Item", command = lambda: addMenuItem(menu, frame2))
    addItem.grid(row=0, column=2, sticky="nwe")
    addItem.config(bg="white", padx = 5)
    
    exitButton = tkinter.Button(base, text="Exit", command = lambda: sys.exit())
    exitButton.config(bg="white", padx = 5)
    exitButton.grid(row=3, column=2, sticky="se")

#-------------------------------------------------------------------------------
#---Show a third listbox with details about the ingredient
def showDetails(text) :
    detailFrame = tkinter.Frame(base, width = 25, height = 400, bg="white")
    detailFrame.grid(row = 0, column = 2)
    
    detailWindow = tkinter.Listbox(detailFrame, bg="white")
    detailWindow.pack(side=TOP)
    
#-------------------------------------------------------------------------------
#---Show the button to see ingredient details
def showBut2(ingWindow, frame) :
    okButton = tkinter.Button(frame, bg ="white", text="Ingredient Details", command = lambda: showDetails(ingWindow.get(ingWindow.curselection())))
    okButton.pack(side=BOTTOM)
    ingWindow.bind('<<ListboxSelect>>', lambda x: doNothing())
    def doNothing() :
        pass
#-------------------------------------------------------------------------------
#---Show the ingredients of the currently selected menu item
def showIngredients(text, frame2) :
    frame2.pack_forget()
    frame2 = tkinter.Frame(base, width = 25, height = 400, bg="white")
    frame2.grid(row = 0, column = 1)
    for i in range(0, len(newMenu.menuItems)) :
        if newMenu.menuItems[i].getItem() == text :
            ingWindow = tkinter.Listbox(frame2, bg = "white")
            ingWindow.pack(side=TOP)
            for ing in newMenu.menuItems[i].ingredients :
                ingWindow.insert(0, ing)
    ingWindow.bind('<<ListboxSelect>>', lambda x: showBut2(ingWindow, frame2))

#-------------------------------------------------------------------------------
#---Show the button to "Show Ingredients"
def showBut(menuWindow, frame, frame2) :
    okButton = tkinter.Button(frame, bg ="white", text="Show Ingredients", command = lambda: showIngredients(menuWindow.get(menuWindow.curselection()), frame2))
    okButton.pack(side=BOTTOM)
    menuWindow.bind('<<ListboxSelect>>', lambda x: doNothing())
    def doNothing() :
        pass
    
#-------------------------------------------------------------------------------
#---Show the current menu
def showMenu(filt, parent, frame2) :
    menuFrame = tkinter.Frame(base, width = 25, height = 400, bg="white")
    menuFrame.grid(row = 0, column = 0)
    menuWindow = tkinter.Listbox(menuFrame, bg = "white")
    menuWindow.pack(side=TOP)
    
    nameList = newMenu.getNames(filt)
    # Show the menu
    for name in nameList :
        menuWindow.insert(len(nameList), name)
        
    # Show ingredients of whatever menu item is selected
    menuWindow.bind('<<ListboxSelect>>', lambda x: showBut(menuWindow, menuFrame, frame2))
    menuWindow.bind('<Double-1>', lambda x: showIngredients(menuWindow.get(menuWindow.curselection()), frame2))

#-------------------------------------------------------------------------------
#---Add another ingredient field
def anotherEntry(frame, ingList) :
    addItemField = tkinter.Entry(frame, width = 20)
    addItemField.pack()
    ingList.append(addItemField)

#-------------------------------------------------------------------------------
#---Add the menu items to the menu
def saveEntries(name, ingList, menu, frame2) :
    ingSet = set()
    for i in ingList :
        ingSet.add(i.get())
    menu.addMenuItem(name, ingSet)
    showMenu("full", base, frame2)

#-------------------------------------------------------------------------------
#---Add a menu item and its ingredients
def addMenuItem(menu, frame2) :
    ingList = []
    # Entry fields for adding a menu item
    addItemField = tkinter.Entry(frame2, width = 20)    
    addItemField2 = tkinter.Entry(frame2, width = 20)
    addItemField3 = tkinter.Entry(frame2, width = 20)
    l1 = tkinter.Label(frame2, text="Name of Menu Item", bg="white")
    l1.pack(side=TOP)
    addItemField.pack()
    l2 = tkinter.Label(frame2, text="Ingredients", bg="white")
    l2.pack(side=TOP)
    addItemField2.pack()
    addItemField3.pack()
    
    ingList.append(addItemField2)
    ingList.append(addItemField3)
        
    saveButton = tkinter.Button(frame2, text="Save Item", bg = "white", command = lambda: saveEntries(addItemField.get(), ingList, menu, frame2))
    addButton = tkinter.Button(frame2, text="Add Ingredient", bg = "white", command = lambda: anotherEntry(frame2, ingList))
    saveButton.pack(side=BOTTOM)
    addButton.pack(side=BOTTOM)

newMenu = menu("For Stephanie", "menu.txt")
base = baseWindow()
showMainScreen(base, newMenu)
base.mainloop()
