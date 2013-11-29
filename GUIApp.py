from AgentJBaseClass import *
#GUI Packages-- Tkinker
from Tkinter import *
import Tkinter

   
class App(Tkinter.Tk):

    def __init__(self,master):
        #*note*- pack_propagate(0) used to change default behavior of
        #frames to NOT size to fit child widgets.

        Tkinter.Tk.__init__(self,master)
        self.initialize(master)


    def initialize(self,master):
        main=Frame(master)
        main.pack()
        
        #configure i/o pane's
        paneOut=Frame(main,width=900, height=600,background="green")
        paneIn=Frame(main,width=800, height=100,background="red")
        paneIn.pack_propagate(0)
        #contents will NOT resize, note--changing default behavior of Tkinker
        
        #PaneOut sub-panes (AGENT OUTPUT, WORLD OUTPUT)
        paneWorld = LabelFrame(paneOut,text="World Output",width=450,height=600,background="white")
        paneWorld.pack(side=LEFT,fill=BOTH, expand=1,padx=10, pady=10)
        paneWorld.pack_propagate(0)

        paneAgent = LabelFrame(paneOut,text="Agent Output",width=450,height=600,background="white")
        paneAgent.pack(side=LEFT,fill=BOTH, expand=1,padx=10, pady=10)
        paneAgent.pack_propagate(0)

        global worldMessage
        global agentMessage
        worldMessage = Tkinter.StringVar()
        agentMessage = Tkinter.StringVar()
        #add text box's to Agent output and World Output
        self.w_out = Message(paneWorld,textvariable=worldMessage,width=400,anchor=NW)
        self.a_out = Message(paneAgent,textvariable=agentMessage,width=400,anchor=NW)

        self.w_out.pack(fill=BOTH, expand=1)
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
        display =  eval(i)
        agentMessage.set(display)


######################## MAIN ##########################

if __name__ == "__main__":
    app = App(None)
    app.title('Agent in Blocks World')
    
    #initialize Agent and blocksWorld
    Agent = AgentJBase()

    app.mainloop()





    
