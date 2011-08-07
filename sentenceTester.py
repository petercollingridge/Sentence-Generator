#! /usr/bin/env python

import os
import random
import Tkinter
import tkFont
import codecs
import sentenceMaker

class SentenceApp(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)

    #   Set formating options
        self.englishFont = ("Arial", 12)
        self.hanziFont = tkFont.Font(family="HDZB_36", size=24)

        self.patterns = sentenceMaker.getPatternsFromFile(os.path.join('data', 'patterns.txt'))

        self._createLabel()
        self._createButton()
        self.grid()

    def _createLabel(self):
        self.label1 = Tkinter.StringVar()
        self.label1.set("Test String")
        
        Label1 = Tkinter.Label(self, bg='white', relief=Tkinter.GROOVE, font=self.englishFont, textvariable=self.label1)        
        Label1.grid(row=0, column=0, columnspan=4, padx=25, pady=25, sticky=Tkinter.EW)

        self.nextSentence()

    def _createButton(self):
        nextButton = Tkinter.Button(self, text="Next", command=self.nextSentence)
        nextButton.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky=Tkinter.NSEW)

    def nextSentence(self):
        random_pattern = random.choice(self.patterns)
        english, chinese = random_pattern.generateSentence()
        self.label1.set(" ".join(english))
        self.answer = chinese

app = SentenceApp()
app.master.title("Chinese Grammar Quiz")
app.mainloop()
