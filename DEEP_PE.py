from tkinter import *
from tkinter import filedialog
import regex as re
from Bio.Seq import Seq

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

def extensionFixer(edit, RTLength, extSeq, inputSeq):
    editSplit = edit.split(" ")
    if "insertion" in edit:
        tempSeq = ""
        for letter in extSeq:
            if letter.islower():
                continue
            else:
                tempSeq += letter
        return tempSeq
    elif "deletion" in edit:
        basepairAmt = int(editSplit[1])
        searchSeq = extSeq[int(RTLength):]
        match = re.search(searchSeq, inputSeq)
        if match == None:
            inputSeq = Seq(inputSeq).reverse_complement()._data
            match = re.search(searchSeq, inputSeq)
        start = match.start()
        return inputSeq[start - (int(RTLength) + basepairAmt):match.end()]
    lowerCase = 0
    for letter in extSeq:
        if letter.islower():
            lowerCase += 1
    if lowerCase == 1:
        for count, letter in enumerate(extSeq):
            if letter.islower():
                extSeq = extSeq[:count] + editSplit[3] + extSeq[count + 1:]
        return extSeq
    else:
        fixedCount = 0
        for count, letter in enumerate(extSeq):
            if letter.islower() and fixedCount == 0:
                extSeq = extSeq[:count] + editSplit[8] + extSeq[count + 1:]
                fixedCount += 1
            elif letter.islower():
                extSeq = extSeq[:count] + editSplit[3] + extSeq[count + 1:]
        return extSeq

def mutationChecker(RTLength, extSeq, inputSeq, mutationIndex, mutation):
    searchSeq = extSeq[:int(RTLength)]
    match = re.search(searchSeq, inputSeq)
    if match != None and (match.start() <= mutationIndex <= match.end()):
        return (True, "+", inputSeq[match.start():mutationIndex] + mutation.lower() + inputSeq[mutationIndex + 1:match.end()])
    revInputSeq = Seq(inputSeq).reverse_complement()
    match = re.search(searchSeq, revInputSeq._data)
    newMutationIndex = len(inputSeq) - 1 - mutationIndex
    newMutation = Seq(mutation).reverse_complement()._data
    if match != None and (match.start() <= newMutationIndex <= match.end()):
        return (True, "-", (revInputSeq[match.start():newMutationIndex] + newMutation.lower() + revInputSeq[newMutationIndex + 1:match.end()])._data)
    return (False, "")

def main():
    dataDict = {}
    inputFile = open(filename, "r")
    inputFile.readline()
    inputSeq = inputFASTA.get()
    for count, letter in enumerate(inputSeq):
        if letter == "(":
            mutationIndex = count + 1
            mutation = inputSeq[count + 3]
            break
    inputSeq = inputSeq[:mutationIndex - 1] + inputSeq[mutationIndex] + inputSeq[mutationIndex + 4:]
    mutationIndex -= 1
    for line in inputFile:
        line = line.split("\t")
        extSeq = extensionFixer(line[4], line[6], line[7], inputSeq)
        resultTup = mutationChecker(line[6], extSeq, inputSeq, mutationIndex, mutation)
        if (resultTup[0]):
            key = float(line[8])
            dataDict[key] = (line[3], line[5], line[6], resultTup[2], line[9].strip("\n"), resultTup[1])
    inputFile.close()
    dictItems = dataDict.items()
    dictItems = sorted(dictItems)
    outputFile = open("output.txt", "w")
    outputFile.write("Guide\tExtension\tPBS Length\tRT Length\tScore\tPrediction Model\tStrand of Extension\n")
    for item in reversed(dictItems):
        outputFile.write(f"{item[1][0]}\t{item[1][3]}\t{item[1][1]}\t{item[1][2]}\t{item[0]}\t{item[1][4]}\t{item[1][5]}\n")
    outputFile.close()

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


