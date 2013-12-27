from AgentClasses.AgentKen import *
#GUI Packages-- Tkinker
from Tkinter import *
import Tkinter
from naturalLanguageProcessing import *

   
class App(Tkinter.Tk):

    def __init__(self,master):
        Tkinter.Tk.__init__(self,master)
        self.initialize(master)
 
    def initialize(self,master):
        main=Frame(master)
        
        main.pack()
        
        #configure i/o pane's
        paneOut=Frame(main,width=800, height=600,background="green")
        paneIn=Frame(main,width=800, height=100,background="red")
        paneIn.pack_propagate(0)
        #contents will NOT resize, note--changing default behavior of Tkinker
        
        paneAgent = LabelFrame(paneOut,text="Agent Output",width=300,height=100,background="white")
        paneAgent.pack(side=LEFT,fill=BOTH, expand=1,padx=10, pady=10)
        paneAgent.pack_propagate(0)

        #global worldMessage
        global agentMessage
        agentMessage = Tkinter.StringVar()
        self.a_out = Message(paneAgent,textvariable=agentMessage,width=300,anchor=NW)

        self.a_out.pack(fill=BOTH, expand=1)

        #paneIn sub-panes/buttons/ect
        self.entry = Entry(paneIn,width=70)
        self.entry.pack()
        self.entry.focus_set()

        self.enter = Button(paneIn,text="Enter", command=self.onEnter)
        self.enter.pack()
        
        paneOut.pack(fill=BOTH, expand=1)
        paneIn.pack(fill=BOTH, expand=1)

    #called when enter button is clicked
    def onEnter(self):
        #get text from entry box, and eat CR
        global agentMessage
        i = self.entry.get()
        #convert input to function call list
        functionCallList = convertSpeechToFunction(i)
        display = ''
        for x in functionCallList:
            display =  display + eval(x)
            agentMessage.set(display)

        self.entry.delete(0, Tkinter.END)

    def EnterPressed(self,button):
        self.onEnter()
        return None


######################## MAIN ###########################

if __name__ == "__main__":
    app = App(None)
    app.title('Agent in Blocks World')
    app.bind("<Return>", app.EnterPressed)
    
    #initialize Agent and blocksWorld
    Agent = AgentKen()

    app.mainloop()




    
