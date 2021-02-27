from tkinter import *
from tkinter import simpledialog
import os


root = Tk()
root.withdraw()
template_name = simpledialog.askstring('template creation','enter the name of the template')

print('temp_naem:'+template_name)

train_path  = '../resources/ml/buffer/train/'+template_name
test_path  = '../resources/ml/buffer/test/'+template_name

os.makedirs(train_path)
os.makedirs(test_path)

f = open('../resources/classification_output/out.txt','w')
f.write(template_name)
f.close()



