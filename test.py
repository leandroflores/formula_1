from tkinter import *

class Application:
    
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()
        self.msg = Label(self.widget1, text="Primeiro widget")
        self.msg["font"] = ("Verdana", "10", "italic", "bold")
        self.msg.pack ()
        self.sair = Button(self.widget1)
        self.sair["text"] = "Sair"
        self.sair["font"] = ("Calibri", "10")
        self.sair["width"] = 5
        self.sair["command"] = self.widget1.quit
        self.sair.pack()

window = Tk()
window.title("Teste")

header = Label(window, text="Clique aqui")
header.grid(column=0, row=0)
# Application(root)

text_2 = Label(window, text="Teste")
text_2.grid(column=1, row=0)

window.mainloop()