# importing the modules 
import cv2 
from tkinter import *
from tkinter import simpledialog
import json
import browse_file



points=[]
count =0;
ll = []
d={}


# function to find the regions to do ocr
def click_event(event, x, y, flags, params): 

    global count
    global points
    
    # img = params[0]
    
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
        points.append((x,y));
        count += 1
  
        
        if(count %2 ==0):
            #these 4 lines are for getting the coordinates for the cropping
            y = points[0][1]
            x = points[0][0]
            w = abs(points[1][0]-points[0][0]);
            h = abs(points[1][1]-points[0][1]);
            


            crop_img = img[y:y+h,x:w+x] #for cropping the image
            cv2.imshow("cropped", crop_img)
            # cv2.waitKey(0)

            
            

            enter_template() #giving a name for the extracted field

            
            
            


def enter_template():
    
    root = Tk()
    root.withdraw()
    # button_accept = Button(root,text=" enter field name",command=get_name)
    # button_accept.pack()
    # button_cancel = Button(root,text="cancel",command=cancel_operation)
    # button_cancel.pack()
    
    get_name()
    # root.geometry("300x300")
    # root.mainloop()
    # root.quit()
    # root.destroy()

def get_name():
    global d
    global points
    s = simpledialog.askstring("field name","enter field name")

    # ll.append(points.copy())
    d[s]=points.copy()
    # print("d: "+str(d))
    
    
    points.clear()
    
    





    

# def create_template():

#     path = browse_file.browse()
    
#     # reading the image 
#     img = cv2.imread(path, 1) 
  
#     # displaying the image 
#     cv2.imshow('image', img) 
  
#     # setting mouse hadler for the image 
#     # and calling the click_event() function 

    
#     cv2.setMouseCallback('image', click_event) 
    
#     # wait for a key to be pressed to exit 
#     cv2.waitKey(0) 
  
#     # close the window 
#     cv2.destroyAllWindows() 
#     print(d)

#     #storing the template in a template file as json





  
    
  
# driver function 
# if __name__=="__main__": 

def create_template():
    global img
  
    path = browse_file.browse()

    # reading the image 
    img = cv2.imread(path, 1) 

    # displaying the image 
    cv2.imshow('image', img) 

    # setting mouse hadler for the image 
    # and calling the click_event() function 


    cv2.setMouseCallback('image', click_event) 

    # wait for a key to be pressed to exit 
    cv2.waitKey(0) 

    # close the window 
    cv2.destroyAllWindows() 
    template_name = simpledialog.askstring("template name","enter name of the document")
    print(d)
    print(template_name)

    #add dimensions of the image also
    d['im_shape'] = (img.shape[0],img.shape[1])


    json_object = json.dumps(d, indent = 4)   
    print(json_object) 

    with open("../resources/templates/"+template_name+".json", "w") as outfile:
        json.dump(d, outfile)  

    # create_template()
    # print('hello this is d:' + str(d))

if __name__=='__main__':
    create_template()