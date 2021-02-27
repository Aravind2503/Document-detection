import shutil
import tkinter as tk
import os
import training
import testocr




x = []
docs=None

f = open('../resources/trainable.txt','r')
x = f.read().split(' ')

#has the list of unique docs that are to be trained
x = x[:-1]
x=list(set(x))

print(x)

 

cat = ''

def close():
    app.destroy()



OptionList = x

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

l = [x[1] for x in os.walk('../resources/ml/buffer/train')]
print(l)

# this means that its a new category.
if cat in l[0]:
    #move all the contents from buffer to ml directory
    #create a template
    target_test = '../resources/ml/test/'
    target_train = '../resources/ml/train/'
    
    # os.makedirs(target_test)
    # os.makedirs(target_train) 

    buffer_train = '../resources/ml/buffer/train/'+cat+'/'
    buffer_test = '../resources/ml/buffer/test/'+cat+'/'
    

    shutil.move(buffer_train,target_train)
    shutil.move(buffer_test,target_test)



    testocr.create_template()
    training.train_model()
    # import testocr
    x.remove(cat)
    for i in x:
        docs += i+' ' 


    f = open("../resources/trainable.txt", "w")
    f.write(docs)
    f.close()




else:
    training.train_model()
    