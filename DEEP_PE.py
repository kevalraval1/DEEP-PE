from tkinter import *
from tkinter import filedialog
import regex as re

window = Tk()
window.title("DEEP-PE Searching Tool")

def selectFile():
    global filename
    filename = filedialog.askopenfilename(initialdir='/',title='Select File',
    filetypes=(('Text File','*.txt'),('All Files', '*.*')))
    if(filename!=''):
        label = Label(frame, text=filename, bg = 'gray')
        spaceText.window_create("end", window=label)
        spaceText.insert('end', '\n')

def main():
    file = open("DeepPE_Scores.txt", "r")
    content = file.read()

    contentList = content.splitlines()
    del contentList[0]
    print (contentList[0])
    parsedList = []

    for line in contentList:
        tempSplit = line.split("\t")
        parsedList.append(tempSplit)

    print (parsedList[0])

    for line in parsedList:
        changeList = line[4].split(" ")
        if (len(changeList) == 10) and (changeList[2] == "to"):
            originalBase = changeList[3]
            originalBase2 = changeList[8]
        elif (len(changeList) == 4) and (changeList[2] == "to"):
            originalBase = changeList[3]
        RTTLength = int(line[5])
        extension = line[7]
        searchSeq = "".join(extension[0:RTTLength])
        tempList = list(searchSeq)
        baseCount = 0
        for count, base in enumerate(tempList):
            if base.islower() and baseCount == 0:
                tempList[count] = originalBase
                baseCount += 1
            elif base.islower() and baseCount > 0:
                tempList[count] = originalBase2
        searchSeq = "".join(tempList)
        result = re.search(searchSeq, inputFASTA.get(), re.IGNORECASE)
        print (result)

canvas = Canvas(window, height = 100, width = 600)
canvas.pack()

frame = Frame(window,relief = 'groove')
frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)

welcome = Label(frame, text = "Welcome to the DEEP-PE Searching and Analysis Tool", fg = "Black")
welcome.pack(side = "top")

inputFASTA = Entry(frame, width = 50)
inputFASTA.pack(side = "top")
inputFASTA.insert(0, "Please enter the inputted FASTA sequence")

spaceText = Text(frame,width=40,height=20, borderwidth=0)
spaceText.pack(side='right',fill='both' ,expand=True)

openFile = Button(window, text='Open DEEP-PE results .txt File', padx = 10, pady = 5, fg = 'black', bg = 'gray', command = selectFile)
openFile.pack()

enterButton = Button(window, text = "Start", padx = 10, pady = 5, fg = "Black", bg = "gray", command = main)
enterButton.pack()

window.mainloop()


