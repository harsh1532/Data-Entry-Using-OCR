# Importing Libraries and Dependencies
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import pytesseract
import cv2
import numpy
import pickle
import os
import AlignImage
from ttkthemes import themed_tk as tk

# Connecting Tesseract Engine to the python file
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
root=tk.ThemedTk()
root.get_themes()
root.set_theme("clearlooks")

root.title("panned window")
root.geometry("1600x1600+0+0")

photo = PhotoImage(file = "Default.png")
root.iconphoto(False, photo)

rect = 0
img_list = []
pts_1 = []
pts_2 = []
OldForm_label = []
OldForm_entry = []
template = []
field = []
points = []
EntryVar = []
L = 0
number_attribute = 1
btn_temp = 0
flag_lbl_old = 0
flag_lbl_new = 0
old_open = False
new_open = False
mouse_down = False
global TempAndPoints

######################################################################################################################

def create_atribute(my_atribute):
    H=1
    W=10
    global attribute_entry, attribute_label
    attribute_label=[]
    attribute_entry=[]
    # Appending the FieldNames to field list
    field.append(my_atribute)
    
    attribute_label.append(Label(right_frame,text=my_atribute,padx=5,pady=5,height=H,width=W))
    attribute_label[-1].grid(row=number_attribute,column=0,pady=2)
    
    attribute_entry.append(Entry(right_frame, font=("Helvetica", 13)))
    attribute_entry[-1].grid(row=number_attribute,column=1,pady=2)
    pop.destroy()

def popup_ok():
    global string1, number_attribute
    string1=popup_entry.get()
    if string1 == "":
        messagebox.showwarning("showwarning", "Please Enter Attribute Name First!!")
        return

    number_attribute +=1
    create_atribute(string1)

def pop_cancel():
    my_canvas.delete(rect)
    global pts_1,pts_2
    pts_1.pop()
    pts_2.pop()
    pop.destroy()

def popup_window():
    global  pop,popup_entry
    pop=Toplevel(root)
    pop.title("Window:"+ str(rect))

    pop.wm_attributes("-topmost", 1)

    pop.title(" Add Attribute Name")
    pop.geometry("250x250")

    name=Label(pop,text="Enter selected attribute name")
    name.pack(padx=5,pady=5)

    popup_entry=Entry(pop,width=30)
    popup_entry.pack(padx=5,pady=5)

    ok_btn=ttk.Button(pop,text="OK",command=popup_ok)
    ok_btn.pack(pady=1)

    cancel_btn=ttk.Button(pop,text="Cancel",command=pop_cancel)
    cancel_btn.pack(pady=1)

######################################################################################################################

def on_button_press(event):
    if FormName.get() == "":
        messagebox.showwarning("showwarning", "Please Enter Form Name First!!")
        return
    global mouse_down
    mouse_down = True
    # save mouse drag start position
    global start_x, start_y
    start_x = event.x
    start_y = event.y
    pts_1.append((start_x,start_y))
    
    # create rectangle to represent Region of Interest(ROI)
    global rect
    rect = my_canvas.create_rectangle(x,y, 1, 1,outline="black")
    
def on_move_press(event):
    if mouse_down==False:
        return
    curX, curY = (event.x, event.y)

    # Expand rectangle as you drag the mouse
    my_canvas.coords(rect, start_x, start_y, curX, curY)
    
def on_button_release(event):
    if mouse_down==False:
        return
    curX, curY = (event.x, event.y)
    pts_2.append((curX,curY))
    popup_window()

def get_data():
    global lbl_formsave
    if FormName.get()=="":
        messagebox.showwarning("showwarning", "Please Enter Form Name First!!")
        return
    if len(field)==0 and len(pts_2)==0:
        messagebox.showwarning("showwarning", "Please Select atleast 1 attribute!!")
        return
    global points
    points = [(tl + br) for tl, br in zip(pts_1, pts_2)]

    try:
        TempAndPoints = pickle.load( open( "SavedData.p", "rb" ) )
    except:
        TempAndPoints = {}
    
    TempAndPoints[FormName.get()] = [template, field, points]
    pickle.dump(TempAndPoints, open( "SavedData.p", "wb" ) ) # Saving data relating to form into Binary file
    
    
    f_name = FormName.get()
    with open(f'Data Files\{f_name}.csv','a+') as f:
        for i in range(len(field)):
            f.write((str(field[i])+','))
        f.write('\n')
    
    lbl_formsave=Label(right_frame, text="Form Saved!!",font= ('Helvetica', 18, 'bold') , fg="#00ff00")
    lbl_formsave.grid(row=0,column=5,padx=5, pady=10)
    
def Open_dialog_new():
    H=1
    W=20
    global btn_temp
    btn_temp=0

    old_open = False
    new_open = True

    for i in range(rect+1):
        # Remove rectangle on screen when we transit from new to old form
        my_canvas.delete(i+2)


    my_canvas.bind("<ButtonPress-1>", on_button_press)
    my_canvas.bind("<B1-Motion>", on_move_press)
    my_canvas.bind("<ButtonRelease-1>", on_button_release)  
    left_frame.filename=askopenfilename(title="select",filetypes=(("jpeg files","*.jpeg "), ("jpg files","*.jpg "),("png files","*.png "),("all files","*.*")))
    if left_frame.filename == "":
        return
    root.title("new form window")
    global template, FormName, field, pts_1, pts_2, points, mouse_down

    # Delete right frame 
    global right_frame
    right_frame.destroy()

    if (len(OldForm_label)!=0):
        OldForm_label.clear()
        OldForm_entry.clear()
    
    right_frame=Frame(panel_1)
    panel_1.add(right_frame)
    template=cv2.imread(left_frame.filename)

    image = Image.open(left_frame.filename)
    image = image.resize((650, 700), Image.ANTIALIAS)
    img_list.append(ImageTk.PhotoImage(image))

    #Update image by getting link from user selection
    my_canvas.itemconfig(image_id,image = img_list[-1])

    # Intializations
    mouse_down = False
    FormName.set("")
    field.clear()
    pts_1.clear()
    pts_2.clear()
    points.clear()

    # On right frame for new user or new form
    form_name=Label(right_frame,text="Enter form name",padx=5,pady=5,height=H,width=W)
    form_name.grid(row=0,column=0,pady=10)

    entry_name=Entry(right_frame,textvariable = FormName, font=("Helvetica", 13))
    entry_name.grid(row=0,column=1,padx=10)
    entry_name.insert(0,"")

    save_btn_new = ttk.Button(right_frame,text="Save",command=get_data)
    save_btn_new.grid(row=0,column=2, padx=50)

    user_menu.entryconfig("Old Form",state=NORMAL)
    user_menu.entryconfig("New Form",state=NORMAL)

######################################################################################################################

def form_delete():
    global TempAndPoints, my_combo,btn_temp, flag_lbl_old
    h = messagebox.askquestion("Form","Are you sure you want to Delete")
    if flag_lbl_old==1:         # Remove the "Data Saved!!" label from the frame
        lbl_succ.grid_remove()
        flag_lbl_old=0

    if  (h=='yes'):
        _ = TempAndPoints.pop(my_combo.get())

        file_name = f'Data Files\{str(my_combo.get())}.csv'
        
        pickle.dump(TempAndPoints, open( "SavedData.p", "wb" ) )
        my_combo.destroy()
        
        try:
            TempAndPoints = pickle.load( open( "SavedData.p", "rb" ) )
        except:
            TempAndPoints = {}
        
        List = ["None"]
        key = list(TempAndPoints.keys())
        List = List + key
        
        my_combo=ttk.Combobox(right_frame,value=List)
        my_combo.current(0)
        my_combo.bind('<<ComboboxSelected>>',combo_reply)
        my_combo.grid(row=1,column=1,padx=25,pady=50)
        my_canvas.itemconfig(image_id,image = img_list[0])

        for i in range(len(OldForm_label)):
            OldForm_label[i].grid_remove() 
            OldForm_entry[i].grid_remove()

        if (len(OldForm_label)!=0):
            OldForm_label.clear()
            OldForm_entry.clear()

        if btn_temp!=0:
            btn_scan.grid_forget()
            btn_save.grid_forget()
            btn_temp=1

        btn1.configure(state=DISABLED)
        btn_view.configure(state=DISABLED)
        btn_delete.configure(state=DISABLED)

        
        if(os.path.exists(file_name) and os.path.isfile(file_name)):
            os.remove(file_name)
            print("file deleted")
        else:
            print("file not found")
         
def form_view():
    img1=TempAndPoints[my_combo.get()][0]
    resized_window = cv2.resize(img1, (700, 700))
    cv2.imshow("View Template", resized_window)
    cv2.waitKey(0)
    
def form_save():
    global flag_lbl_old, lbl_succ
    
    f_name = my_combo.get()
    with open(f'Data Files\{f_name}.csv','a+') as f:
        for i in range(len(OldForm_label)):
            y = OldForm_entry[i].get()
            f.write((str(y)+','))
        f.write('\n')

    btn_save.configure(state=DISABLED)
    btn_scan.configure(state=DISABLED)

    lbl_succ=Label(right_frame, text=f"Saved to {f_name}.csv",font= ('Helvetica', 18, 'bold') , fg="#00ff00")
    lbl_succ.grid(row=0,column=2,padx=5, pady=10)
    flag_lbl_old=1

def attribute_onscreen(att):
    global OldForm_entry, EntryVar,template, field, points, TempAndPoints
    H=1
    W=10

    # Code for removing Labels
    for i in range(len(OldForm_label)):
        OldForm_label[i].grid_remove() 
        OldForm_entry[i].grid_remove()
        
    if (len(OldForm_label)!=0):
        OldForm_label.clear()
        OldForm_entry.clear()
    
    for i in range(len(TempAndPoints[att][1])):
        EntryVar.append(StringVar())
        EntryVar[i].set("")

    for i in range(len(TempAndPoints[att][1])):
        OldForm_label.append(Label(right_frame,text=TempAndPoints[att][1][i],padx=5,pady=5,height=H,width=W))
        OldForm_label[i].grid(row=i+2,column=0,pady=2)
   
    for i in range(len(TempAndPoints[att][1])):
        OldForm_entry.append(ttk.Entry(right_frame, textvariable=EntryVar[i] , font=("Helvetica", 13)))
        OldForm_entry[i].grid(row=i+2,column=1,pady=2)
    
    global btn_scan,btn_temp, btn_save

    if btn_temp!=0:
        btn_scan.grid_forget()
        btn_save.grid_forget()
    btn_scan=ttk.Button(right_frame,text="Scan",command = Scan_OCR)
    btn_scan.grid(row=len(TempAndPoints[att][1])+3,column=1,pady=10)
    btn_temp=1

    
    btn_save=ttk.Button(right_frame,text="Save",state=NORMAL,command=form_save)
    btn_save.grid(row=len(TempAndPoints[att][1])+4,column=1,pady=10)

    template = TempAndPoints[att][0]
    field = TempAndPoints[att][1]
    points = TempAndPoints[att][2]

    my_canvas.itemconfig(image_id,image = img_list[0])
    
def combo_reply(event):
    global flag_lbl_old
    if flag_lbl_old==1:
        lbl_succ.grid_remove()
        flag_lbl_old=0
    if my_combo.get()!="None":
        btn1.configure(state=NORMAL)
        btn_view.configure(state=NORMAL)
        btn_delete.configure(state=NORMAL)
        attribute_onscreen(my_combo.get())

    else:
        btn1.configure(state=DISABLED)
        btn_view.configure(state=DISABLED)
        btn_delete.configure(state=DISABLED)
        for i in range(len(OldForm_label)):
            OldForm_label[i].grid_remove()
            OldForm_entry[i].grid_remove()
        if btn_temp!=0:
            btn_scan.grid_remove()
            btn_save.grid_remove()

def old_form():
    old_open = True
    new_open = False
    user_menu.entryconfig("Old Form",state=DISABLED)
    user_menu.entryconfig("New Form",state=NORMAL)

    root.title("Old form window")
    my_canvas.unbind('<ButtonPress-1>')
    my_canvas.unbind('<B1-Motion>')
    my_canvas.unbind('<ButtonRelease-1>')
   
    for i in range(rect+1):
        # Remove rectangle on screen when we transit from new to old form
        my_canvas.delete(i+2)

    my_canvas.itemconfig(image_id,image = img_list[0])
    global right_frame
    right_frame.destroy()
    
    right_frame=Frame(panel_1)
    panel_1.add(right_frame)

    lb1=Label(right_frame,text="Browse form to be scanned",font=("Arial", 15))
    lb1.grid(row=0,column=0,padx=5,pady=15)

    global btn1
    btn1=ttk.Button(right_frame,text="Browse",state=DISABLED,command=Open_dialog_old)
    btn1.grid(row=1,column=0,pady=20)

    global btn_view
    btn_view=ttk.Button(right_frame,text="View Form",state=DISABLED,command=form_view)
    btn_view.grid(row=1,column=2,padx=10,pady=20)

    global btn_delete
    btn_delete=ttk.Button(right_frame,text="Delete Form",state=DISABLED,command=form_delete)
    btn_delete.grid(row=1,column=3,padx=10,pady=20)

    global TempAndPoints
    try:
        TempAndPoints = pickle.load( open( "SavedData.p", "rb" ) )
    except:
        TempAndPoints = {}
    
    List = ["None"]
    key = list(TempAndPoints.keys())
    List = List + key
    
    global my_combo
    my_combo=ttk.Combobox(right_frame,value=List)
    my_combo.current(0)
    my_combo.bind('<<ComboboxSelected>>',combo_reply)
    my_combo.grid(row=1,column=1,padx=10,pady=50)

def Open_dialog_old():
    global image_old, img, flag_lbl_old
    left_frame.filename=askopenfilename(title="select",filetypes=(("jpeg files","*.jpeg "),("jpg files","*.jpg "),("png files","*.png "),("all files","*.*")))
    if left_frame.filename =="":
        return
    
    btn_save.configure(state=NORMAL) #To enable the buttons back to NORMAL when we click on Browse button
    btn_scan.configure(state=NORMAL) #To enable the buttons back to NORMAL when we click on Browse button
    if flag_lbl_old==1:
        lbl_succ.grid_remove()
        flag_lbl_old=0


    for i in range(len(OldForm_entry)):  # Setting it to empty string 
        EntryVar[i].set("")
    
    img = cv2.imread(left_frame.filename)

    aligned = AlignImage.align_images(img, template)
    aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
    
    image_old = Image.fromarray(aligned)

    image_old = image_old.resize((650, 700), Image.ANTIALIAS)
    img_list.append(ImageTk.PhotoImage(image_old))

    #Update image by getting link from user selection
    my_canvas.itemconfig(image_id,image = img_list[-1])

def Scan_OCR():
    global myData, image_old
    image_old = numpy.asarray(image_old)

    userImage = image_old.copy()
    myData = []
    for i,j in zip(field, points):
        imgCrop = userImage[j[1]:j[3], j[0]:j[2]]
        Result = pytesseract.image_to_string(imgCrop)
        myData.append(Result)

    global EntryVar
    for i,j in enumerate(myData):
        EntryVar[i].set(j)

#################################################################################################
panel_1=PanedWindow(bd=4,orient=HORIZONTAL,relief="raised",bg="black")
panel_1.pack(fill=BOTH,expand=1)

left_frame=Frame(panel_1)
panel_1.add(left_frame,width=700)

right_frame=Frame(panel_1)
panel_1.add(right_frame)

my_menu=Menu(root)
root.config(menu=my_menu)

user_menu=Menu(my_menu)
my_menu.add_cascade(label="User",menu=user_menu)
user_menu.add_command(label="New Form",command=Open_dialog_new)
user_menu.add_command(label="Old Form",command=old_form)

my_canvas=Canvas(left_frame,highlightbackground="black", height=700,width=650,cursor="cross",highlightthickness=2,background='#A9A9A9',bd= 0)
my_canvas.pack(side=LEFT,expand=1)

image1 = Image.open('Default.png')
# The (650, 700) is (width, height)
image1 = image1.resize((650, 700), Image.ANTIALIAS)

img_list.append(ImageTk.PhotoImage(image1))
image_id=my_canvas.create_image(0,0, image=img_list[0], anchor=NW)

FormName = StringVar()
x = y = 0
root.mainloop()