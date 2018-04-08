import matplotlib.pyplot as plt
import matplotlib.animation as anim
import tkinter as tk
from time import gmtime, strftime
import serial as ser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = plt.figure()
ax = fig.add_subplot(111)
temp=0

def animate(k):
    global xs
    global yx
    with ser.Serial("com14", baudrate=9600, timeout=1) as seri:

        line = seri.readline().strip()#.decode('unicode_escape')
        data=list(line)
        len_d=len(data)
        if(len_d>0):
            temp=(data[len_d-2]*300/1024)-32
            print(temp)
            x = strftime("%H:%M:%S", gmtime())
            xs.append(x)
            ys.append(temp)


    ax.clear()
    ax.plot(xs,ys)
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Main, Visualize):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
class Main(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            tk.Label(self, text="COM PORT").grid(row=0)

            self.com_port = tk.Entry(self)

            self.com_port.grid(row=0, column=1)
            self.error_label = tk.Label(self, fg="red", text="")
            self.error_label.grid(row=2)

            tk.Button(self, text='visualize', command=self.go_visualize).grid(row=3, column=1,  pady=4)

        def go_visualize(self):
            port = str(self.com_port.get())
            err = False
            if len(port) > 0:

                try:
                    s = ser.Serial(port, baudrate=9600, timeout=1)
                    
                except:
                    err = True
                    self.error_label.config(text="Port is already open!!")

                s.close()
            else:
                err=True
                self.error_label.config(text="Empty Port!!")
            if (not err):
                self.controller.show_frame("Visualize")

            pass
class Visualize(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Button(self, text='back Home', command=self.goHome).grid(row=0, column=2, pady=4)
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.show()
        canvas.get_tk_widget().grid(row=1)
    def goHome(self):
        plt.close()
        self.controller.show_frame("Main")

if __name__=="__main__":
    xs=[]
    ys=[]
    app = App()
    ani=anim.FuncAnimation(fig,func=animate,interval=3000)
    #plt.show()

    app.mainloop()