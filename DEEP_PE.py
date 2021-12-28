from tkinter import *
from tkinter import filedialog
import regex as re
from Bio.seq import seq

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


def extensionFixer(edit, extSeq, RTLength, inputSeq):
    if "insertion" in edit:
        tempSeq = ""
        for letter in extSeq:
            if letter.islower():
                continue
            else:
                tempSeq += letter
        return tempSeq
    elif "deletion" in edit:
        basepairAmt = edit[3]
        searchSeq = extSeq[RTLength:]
        match = re.search(searchSeq, inputSeq)
        start = match.start()
        return inputSeq[start - (RTLength + basepairAmt):match.end()]
    elif len(edit) == 10:
        for count, letter in enumerate(extSeq):
            if letter.islower():
                extSeq[count] = edit[9]
            return extSeq
    else:
        fixedCount = 0
        for count, letter in enumerate(extSeq):
            if letter.islower() and fixedCount == 0:
                extSeq[count] = edit[22]
                fixedCount += 1
            elif letter.islower():
                extSeq[count] = edit[9]
        return extSeq

def mutationChecker(RTLength, extSeq, inputSeq, mutationIndex):
    searchSeq = extSeq[:RTLength]
    match = re.search(searchSeq, inputSeq)
    if match != None and (match.start() <= mutationIndex <= match.end()):
        return (True, "+")
    revInputSeq = Seq(inputSeq).reverse_complement()
    match = re.search(searchSeq, revInputSeq)
    if match != None and (match.start() <= mutationIndex <= match.end()):
        return (True, "-")
    return (False, "")

def main():
    dataDict = {}
    inputFile = open(filename, "r")
    inputFile.readline()
    inputSeq = inputFASTA.get()
    for line in inputFile:
        line = line.split("\t")
        #filter bad data here, skip and don't add to dictionary
        key = line[8]
        dataDict[key] = (line[2], line[3], line[4], line[5], line[6], line[7], line[9].strip("\n"))

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


