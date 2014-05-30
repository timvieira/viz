from Tkinter import Tk, Entry, Label, Frame, Button, LEFT, RIGHT, CENTER


def quickentry(labels, callback, title=''):
    "Simple dialog from grabbing parameters from the user."

    root = Tk()

    root.title(title)
    root['padx'] = 20
    root['pady'] = 10

    widgets = {}
    for label in labels:

        # Create a text frame to hold the text Label and the Entry widget
        f = Frame(root)

        #Create a Label in textFrame
        l = Label(f)
        l['text'] = label
        l['width'] = 10
        l.pack(side=LEFT)

        w = Entry(f)
        w['width'] = 20
        w.pack(side=LEFT)

        widgets[label] = w

        f.pack()

    def cb():
        callback({label: widgets[label].get().strip() for label in labels})

    Button(root, text="Quit", command=lambda root=root: root.destroy()).pack(side=RIGHT)
    Button(root, text='Submit', command=cb).pack(side=RIGHT)


    root.protocol("WM_DELETE_WINDOW", lambda root=root: root.destroy())

    print '[quickentry] running'
    root.bind("<Return>", lambda e: cb())
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()
    print '[quickentry] done'
    return root


if __name__ == '__main__':
    import tkMessageBox
    quickentry(['one', 'two', 'three'],
               lambda vs: tkMessageBox.showinfo("Values", str(vs)))
