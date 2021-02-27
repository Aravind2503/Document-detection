import tkinter as tk
import os 

cat = ''

def close():
    app.destroy()

l = [x[1] for x in os.walk('../resources/')]
l[2].sort()

print(l)

lll = [x[1] for x in os.walk('../resources/ml/buffer/train')]
print()
print(lll)

#here l2 is the categories we already have and l6 is the buffer categories
ll= lll[0]+l[2]

OptionList = ll

app = tk.Tk()

app.geometry('300x150')


variable = tk.StringVar(app)
variable.set(OptionList[0])

opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=50, font=('Helvetica', 12))
opt.pack(side="top")

button  = tk.Button(app,text = "ok",command=close)
button.config(width=20, font=('Helvetica', 12))
button.pack(side="bottom")

labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
labelTest.pack(side="top")

def callback(*args):
    global cat
    labelTest.configure(text="The selected item is {}".format(variable.get()))
    cat = variable.get()

variable.trace("w", callback)

app.mainloop()

print(cat)

f = open("../resources/classification_output/out.txt", "w")
f.write(cat)
f.close()