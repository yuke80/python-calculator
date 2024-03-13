import tkinter as tk
 
root = tk.Tk()
 
def key(event):
    print( "pressed", repr(event.char)) #repr
    print("PRESSED", repr(event.keysym))
 
frame = tk.Frame(root, width=100, height=100) #main windown frame
frame.bind("<Key>", key) #press a key to execute key function
frame.focus_set() #send the pressed key value to the frame, not else.
frame.pack()
 
root.mainloop()