import datetime
import json
import glob
from msilib.schema import File
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     #py -m pip install matplotlib
from matplotlib.figure import Figure



class List: 
    def __init__(self,listname,filename):
        self.listname = str(listname)
        self.filename = str(filename)   #data this user
        self.detail = None
        self.notificate = None
        self.checkbox = False 
        self.priority = None
    
    def __str__(self):
        return self.listname

    def setlistname(self,listname):
        self.listname = str(listname)
        return self

    def getlistname(self):
        #return self.listname
        return self

    def getdetail(self,subjname):
        with open(self.filename,'r') as data_json:
            dt = json.load(data_json)
            self.detail = dt[subjname][self.listname]["detail"]
        return self.detail

    def getpriority(self,subjname):
        with open(self.filename,'r') as data_json:
            dt = json.load(data_json)
            self.priority = dt[subjname][self.listname]["priority"]
        return self.priority

    def getcheckbox(self,subjname):
        with open(self.filename,'r') as data_json:
            dt = json.load(data_json)
            self.checkbox = dt[subjname][self.listname]["checkbox"]
        return self.checkbox

    def getnotificate(self,subjname):
        with open(self.filename,'r') as data_json:
            dt = json.load(data_json)
            self.notificate = dt[subjname][self.listname]["notificate"]
        return self.notificate

class Subject: 
    def __init__(self,subjname,filename):
        self.filename = str(filename)   #data this user
        self.subjname = str(subjname)
        self.alllist = {}               # key is listname ,value is listobject
    
    def __str__(self):
        return self.subjname

    def setSubj(self,subjname):     #setSubj when change subject name
        self.subjname = str(subjname)
        return self
    
    def getSubj(self):

        return self     #return object
    
    def addlist(self,listname):
        l = List(listname,self.filename)
        self.alllist[str(listname)] = l
        tmp = {}
        tmp[listname] = {
            "detail":"",
            "notificate":"",
            "checkbox":'False',
            "priority":0
            }
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[self.subjname].update(tmp)              
        
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
        return listname

    def dellist(self,listname):

        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[self.subjname].pop(listname)
            self.alllist.pop(str(listname))

        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
        return listname
    
    def setdetail(self,listname,detail):
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[self.subjname][listname]["detail"] = detail
        
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
    
    def setnotificate(self,listname,noti):
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[self.subjname][listname]["notificate"] = noti
        
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
    
    def setcheckbox(self,listname,cb):
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[self.subjname][listname]["checkbox"] = cb
        
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
    
    def setpriority(self,listname,priority):
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[self.subjname][listname]["priority"] = priority
        
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)

    def editlistname(self,oldlistname,newlistname):
        tmpO = {}   #Object
        tmpN = {}   #Name
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            tmpN = dt[self.subjname][oldlistname].copy()
            tmpO[newlistname] = self.alllist[oldlistname]
            dt[self.subjname].pop(oldlistname)
            self.alllist.pop(oldlistname)
            dt[self.subjname][newlistname] = tmpN
            self.alllist[newlistname] = tmpO[newlistname]

            self.alllist[newlistname].setlistname(newlistname)

        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
        return newlistname
    
    def getallListN(self):  #get all string List name that subject 
        listname = []
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            for ln in dt[self.subjname]:

                listname.append(ln)

        return listname
    
    def getallListO(self):  #get all object List name that subject 

        return self.alllist

class Reminder:
    def __init__(self,filename):

        self.filename = str(filename)       #data this user
        self.allsubjname = {}               #key is subject name , value is subject obj
    
    def getSubjOforList(self,listname):     #get Subject for that list name
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            for subj in self.getallSubjN():
                if str(listname) in str(dt[subj]):
                    return subj  

    def addSubjname(self,subjname):
        s = Subject(subjname,self.filename)
        self.allsubjname[str(subjname)] = s
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt[subjname] = {}          
        
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
        
        return s

    def editSubject(self,oldsubjname,newsubjname):
        self.checkSubj(oldsubjname)
        tmpO = {}
        tmpN = {}
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            tmpN = dt[oldsubjname].copy()
            tmpO[newsubjname] = self.allsubjname[oldsubjname] #create new key buy old value
            dt.pop(oldsubjname)
            self.allsubjname.pop(oldsubjname)
            dt[newsubjname] = tmpN
            self.allsubjname[newsubjname] = tmpO[newsubjname]

            self.allsubjname[newsubjname].setSubj(newsubjname)

        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
        return newsubjname

    def delSubject(self,subjname):
        self.checkSubj(subjname)
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            dt.pop(str(subjname))
            self.allsubjname.pop(str(subjname))
        with open(self.filename, mode = 'w', encoding = 'utf8') as data_json:
            json.dump(dt,data_json)
        
    def gettodayN(self):    #get list name today
        listname = []
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            for subj in dt:
                for lis in dt[subj]:
                    if dt[subj][lis]["notificate"] == str(datetime.datetime.today().strftime('%Y-%m-%d')) and dt[subj][lis]['checkbox'] == 'False':
                        listname.append(lis)
        return listname
    
    def getallN(self): #get all list (not complete)
        listname = []
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            for subj in dt:
                for lis in dt[subj]:
                    if dt[subj][lis]['checkbox'] == 'False':
                        listname.append(lis)
        return listname
    
    def getallNComp(self): #listname with complete and notcomplete
        listname = []
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            for subj in dt:
                for lis in dt[subj]:
                    listname.append(lis)
        return listname

    def getallSubjN(self):  #get all Subject Name
        Subjname = []
        with open(self.filename) as data_json:
            dt = json.load(data_json)
            for subj in dt:
                Subjname.append(subj)
        return Subjname

    def getallSubjO(self):  #get all Subject Object

        for subj in self.getallSubjN():
            self.checkSubj(str(subj))

        return self.allsubjname

    def checkSubj(self,subjname):   #Check if this Subject has an Object. 
        if subjname in self.allsubjname:
            return True             #this subject has object
        else:
            s = Subject(subjname,self.filename)     #create Object
            self.allsubjname[str(subjname)] = s
            with open(self.filename) as data_json:
                dt = json.load(data_json)
                if subjname not in dt:
                    return False
                tmpN = dt[subjname].copy() #data in subj (list and detail)

                for l in tmpN:
                    s.addlist(str(l))
                    s.setdetail(str(l),tmpN[l]["detail"])
                    s.setnotificate(str(l),tmpN[l]["notificate"])
                    s.setcheckbox(str(l),tmpN[l]["checkbox"])
                    s.setpriority(str(l),tmpN[l]["priority"])

            return self.allsubjname[subjname]


############-----------------  GUI function  -----------------############

def createGraph(a): #create graph Page1

    def create_charts(): #all list graph

        comp = 0
        late = 0
        for sub in a.getallSubjN():
            subj = a.getallSubjO()[sub]
            for l in subj.getallListN():
                ls = subj.getallListO()[l]
                if ls.getcheckbox(str(sub)) == "True":
                    comp += 1
                elif checktoday(str(ls.getnotificate(str(sub)))): #return true when late
                    late += 1

        notcomp = len(a.getallNComp())-comp-late
        if notcomp == 0:
            data = [late,comp]
            labels2 = 'Lated', 'Completed'  
            figure2 = Figure(figsize=(4,3), dpi=100) #Circle Area
            subplot2 = figure2.add_subplot(111) 

            pieSizes = data
            my_colors2 = ['lightblue','lightsteelblue']
            explode2 = (0, 0.1) #distance 
            subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True, startangle=90) 
            subplot2.axis('equal')  
            pie2 = FigureCanvasTkAgg(figure2, graphWin)
            pie2.get_tk_widget().pack()
        else:
            data = [late,comp,notcomp]
            labels2 = 'Lated', 'Completed', 'Uncompleted'   
            figure2 = Figure(figsize=(4,3), dpi=100) 
            subplot2 = figure2.add_subplot(111) 

            pieSizes = data
            my_colors2 = ['lightblue','lightsteelblue','silver']
            explode2 = (0, 0.1, 0) 
            subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True, startangle=90) 
            subplot2.axis('equal')  
            pie2 = FigureCanvasTkAgg(figure2, graphWin)
            pie2.get_tk_widget().pack()

    def graphSub(): #Subject Graph

        Nlist = []
        Subn = []
        for sub in a.getallSubjN():
            subj = a.getallSubjO()[sub]
            Nlist.append(len(subj.getallListN()))
            Subn.append(str(subj.getSubj()))

        tSub = tuple(Subn)  
        figure2 = Figure(figsize=(4,3), dpi=100)
        subplot2 = figure2.add_subplot(111) 

        pieSizes = Nlist
        #my_colors2 = ['lightblue','lightsteelblue','silver']
        explode2 = tuple([0]*len(Subn))
        subplot2.pie(pieSizes, explode=explode2, labels=tSub, autopct='%1.1f%%', shadow=True, startangle=90) 
        subplot2.axis('equal')  
        pie2 = FigureCanvasTkAgg(figure2, graphWin)
        pie2.get_tk_widget().pack()

    if len(a.getallSubjN()) <= 0:
        messagebox.showwarning('Subject Error', 'No Subject')
        return
    if len(a.getallNComp()) <= 0:
        messagebox.showwarning('List Error', 'No List')
        return
    graphWin= Tk()  
    graphWin.title('Overall summary graph')
    graphWin = Canvas(graphWin, width = 300, height = 300)
    graphWin.pack()
    create_charts()
    ttk.Button(graphWin, text = "List status",command=create_charts).pack()
    ttk.Button(graphWin, text = "Subject",command = graphSub).pack()
    
def checktoday(d):

    if d == "":
        return  
    Day = d.split('-')
    daytoday = int(str(datetime.datetime.today().strftime('%Y-%m-%d')).split('-')[2])
    monthtoday = int(str(datetime.datetime.today().strftime('%Y-%m-%d')).split('-')[1])
    yeartoday = int(str(datetime.datetime.today().strftime('%Y-%m-%d')).split('-')[0])
    Dday = int(Day[2])
    Dmonth = int(Day[1])
    Dyear = int(Day[0])

    #late == TRUE
    #not yet == FALSE
    
    if yeartoday < Dyear:
        return False
    elif yeartoday == Dyear:
        if monthtoday < Dmonth:
            return False
        elif monthtoday == Dmonth:
            if daytoday < Dday:
                return False
            elif daytoday == Dday:
                return False
            else:
                return True
        else:
            return True
    else:
        return True

def showAllList(a,day,userfile,filename,user):

    def BackPage():
        pl.destroy()
        Page1(a,userfile,filename,user)

    def NextPage():
        select = listboxlist.get(listboxlist.curselection())
        subj = a.getallSubjO()[showlistSubj()]
        pl.destroy()
        if day == "today":
            Page3(a,subj,select,"ptoday",userfile,filename,user)
        elif day == "all":
            Page3(a,subj,select,"pall",userfile,filename,user)

    def showlistSubj():
        return a.getSubjOforList(str(listboxlist.get(listboxlist.curselection())))
   
    def showList():
        listboxlist.delete(0, 'end') #clear all data
        
        if day == "today":
            for l in a.gettodayN():
                subjn = a.getSubjOforList(str(l))
                subj = a.getallSubjO()[subjn]
                listboxlist.insert('end',str(l))
                listboxlist.itemconfig('end',fg= Color(subj,str(l)))
                
        elif day == "all":
            for l in a.getallN():
                subjn = a.getSubjOforList(str(l))
                subj = a.getallSubjO()[subjn]
                listO = subj.getallListO()[str(l)]
                listboxlist.insert('end',str(l))
                listboxlist.itemconfig('end',fg= Color(subj,str(l)))
                if checktoday(listO.getnotificate(str(subj))):
                    if listO.getcheckbox(str(subj)) != 'True':
                        listboxlist.itemconfig('end',bg='#FAA0A0')
                if listO.getnotificate(str(subj)) == str(datetime.datetime.today().strftime('%Y-%m-%d')):
                    if listO.getcheckbox(str(subj)) != 'True':
                        listboxlist.itemconfig('end',bg='#FFE7E5')
                
            
    def showcomp(): #show all list with complete
        listboxlist.delete(0, 'end')
        for l in a.getallNComp():
            subjn = a.getSubjOforList(str(l))
            subj = a.getallSubjO()[subjn]
            listO = subj.getallListO()[str(l)]
            listboxlist.insert('end',str(l))
            listboxlist.itemconfig('end',fg= Color(subj,str(l)))
            if checktoday(listO.getnotificate(str(subj))):
                if listO.getcheckbox(subjn) != 'True':
                    listboxlist.itemconfig('end',bg='#FAA0A0')
            if listO.getnotificate(str(subj)) == str(datetime.datetime.today().strftime('%Y-%m-%d')):
                if listO.getcheckbox(str(subj)) != 'True':
                    listboxlist.itemconfig('end',bg='#FFE7E5')
                
    def complete(): #set complete
        subj = a.getallSubjO()[showlistSubj()]
        subj.setcheckbox(str(listboxlist.get(listboxlist.curselection())),'True')
        pl.destroy()
        showAllList(a,day,userfile,filename,user)

    def update(data):
        # Clear the Combobox
        listboxlist.delete(0, END)
        # Add values to the combobox
        for value in data:
            subjn = a.getSubjOforList(str(value))
            subj = a.getallSubjO()[subjn]
            listO = subj.getallListO()[str(value)]
            listboxlist.insert(END,value)
            listboxlist.itemconfig('end',fg= Color(subj,str(value)))
            if checktoday(listO.getnotificate(str(subj))):
                if listO.getcheckbox(subjn) != 'True':
                    listboxlist.itemconfig('end',bg='#FAA0A0')
            if listO.getnotificate(str(subj)) == str(datetime.datetime.today().strftime('%Y-%m-%d')):
                if listO.getcheckbox(str(subj)) != 'True':
                    listboxlist.itemconfig('end',bg='#FFE7E5')
            
    def check(e): #Check for search list
        v= entry.get()
        alllist = a.getallNComp()
        if v=='':
            data = alllist
        else:
            data=[]
            for item in alllist:
                if v.lower() in item.lower():
                    data.append(item)
        update(data)

    def checkSelect(nextpage):

        if str(listboxlist.curselection()) == '()':
            messagebox.showwarning("Warning", "Please select List")
            return 
        if nextpage == "comp":
            complete()
        elif nextpage == "open":
            NextPage()

    pl = Tk()
    pl.geometry("400x250")
    pl.title("All List")
    if day == 'all':
        entry = Entry(pl,width = 30)
        entry.grid(row = 1, column= 1,columnspan= 4,pady=5)
        entry.bind('<KeyRelease>',check)
        ttk.Label(pl,text = "Search List").grid(row = 1, column= 0,pady=5)
        ttk.Label(pl, text = "All List").grid(row = 2, column= 0,padx=5)
    listboxlist = Listbox(pl,width = 30, height= 10)
    listboxlist.grid(row = 2, column = 1,columnspan= 4,rowspan= 4,padx = 10, pady = 20 )
    ttk.Button(pl,text = "Open",command = lambda:checkSelect('open')).grid(row =2,column=5)
    ttk.Button(pl,text = "Back",command = BackPage).grid(row = 0,column=0 )
    ttk.Button(pl,text = "Complete",command = lambda:checkSelect('comp')).grid(row = 3,column=5 )
    if day != "today":
        ttk.Button(pl,text = "All List",command = showcomp).grid(row = 4,column=5 )
    showList()
    pl.mainloop()

def Color(s,l): #set color in listbox

    ln = s.getallListO()[str(l)]
    pri = ln.getpriority(str(s))
    cb = ln.getcheckbox(str(s))

    if cb == 'True':
        return '#AEAEAE'
    else:
        if pri == 0:            
            return '#000000'
        elif pri == 1:
            return '#0400D1'    #Blue
        elif pri == 2:
            return '#B27300'    #Orange
        elif pri == 3:          
            return '#8940FA'    #Purple #imortant

def loginWindow(userfile):

    def Importfile(): #data about user is name "data_json*.json" only

        def im(): #import process
            fn = str(fname.get())
            if fn in jsonfiles:
                if fn[:9] != "data_json":
                    ImportWin.destroy()
                    loginWin.destroy()
                    loginWindow(fn)
                else:
                    messagebox.showwarning('json file name', 'Please use User Json file')
                    return
            else:  
                messagebox.showwarning('file name error', 'This file does not exist')
                return

        jsonfiles = []
        for file in glob.glob("*.json"):
            jsonfiles.append(file)

        ImportWin = Toplevel()
        ImportWin.title("Import Json file")
        ImportWin.geometry("300x80")
        fname = StringVar()
        topLevelEntry = Entry(ImportWin,width= 35,textvariable=fname)
        topLevelEntry.grid(row = 2, column= 1,columnspan= 2, padx = 5,pady = 10) 
        ttk.Label(ImportWin,text = "Import").grid(row = 2, column= 0,padx = 10)
        ttk.Button(ImportWin,text = "Confirm",width=10,command = im).grid(row = 4, column= 1)  
        ttk.Button(ImportWin,text = "Cancel",width=10).grid(row = 4, column= 2)  

    def registerWindow():

        def newuser(): #register process
            usernew = str(emailname.get())
            file = None
            with open(userfile,mode = 'r') as user_json:
                us = json.load(user_json)
                if usernew in us:
                    messagebox.showerror('User Error', 'This user is already in use. ')
                    return
                else:    
                    num = len(us.keys()) + 1
                    file = str('data_json'+str(num)+'.json')
                    us[usernew] = {}
                    us[usernew]['filename'] = file
            with open(userfile, mode = 'w') as user_json:
                json.dump(us,user_json)

            newdata = {}
            data_json = json.dumps(newdata)
            jsonFile = open(file,"w")
            jsonFile.write(data_json)
            jsonFile.close()

            registerWin.destroy()

            

        registerWin = Toplevel()
        registerWin.title("Register")
        emailname = StringVar()
        registerWin.geometry("250x80")
        CreateUser = Entry(registerWin,width= 30,textvariable=emailname)
        CreateUser.grid(row = 2, column= 2,columnspan= 2, padx = 5,pady = 10)
        ttk.Label(registerWin,text = "Email").grid(row = 2, column= 0,columnspan= 2,padx = 10)
        ttk.Button(registerWin,text = "OK",width=10,command=newuser).grid(row = 5, column= 2)  
        ttk.Button(registerWin,text = "Cancel",width=10).grid(row = 5, column= 3)

    def checkuser():
        user = str(username.get())
        with open(userfile,mode = 'r') as user_json:
            us = json.load(user_json)
            if user in us:
                jsonfiles = []
                for file in glob.glob("*.json"):
                    jsonfiles.append(file)
                filename = us[user]['filename']
                if filename not in jsonfiles:
                    messagebox.showerror('File Error', 'User data file does not exist.')
                    return
                app = Reminder(filename)
                loginWin.destroy()
                Page1(app,userfile,filename,user)
                
            else:
                messagebox.showerror('User Error', 'This user does not exist.')

    loginWin = Tk()
    s = str('Login with '+str(userfile))
    loginWin.title(s)
    loginWin.geometry("350x80")
    username = StringVar()
    LoginEntry = Entry(loginWin,width= 45,textvariable=username)
    LoginEntry.grid(row = 2, column= 1,columnspan= 3, padx = 5,pady = 10)
    ttk.Label(loginWin,text = "Email").grid(row = 2, column= 0, padx = 10)
    ttk.Button(loginWin,text = "Register",width=10,command=registerWindow).grid(row = 4, column= 1)
    ttk.Button(loginWin,text = "Login",width=10,command = checkuser).grid(row = 4, column= 2)  
    ttk.Button(loginWin,text = "Import File",width=10,command=Importfile).grid(row = 4, column= 3)
    loginWin.mainloop()

def Page1(a,userfile,filename,user):    #filename = data about that user (data_json.json)
                                        #userfile = The file that stores the file name of the user data. (user.json)
                                        #user = username (Fair)

    def NextPage(page):

        if page == "p2":
            select = listbox1.get(listbox1.curselection())
            p1.destroy()
            Page2(a,select,userfile,filename,user)
        elif page == "pall":
            p1.destroy()
            showAllList(a,"all",userfile,filename,user)
        elif page == "ptoday":
            p1.destroy()
            showAllList(a,"today",userfile,filename,user)

    def showSubj():
        listbox1.delete(0, 'end') #clear all data
        for i in a.getallSubjN():
            listbox1.insert('end', str(i))

    def AddSubjWindow():

        def addsubj():
            a.addSubjname(str(newSubjname.get()))
            #print(str(newSubjname.get()))
            showSubj()
            AddSubjWin.destroy()

        AddSubjWin = Toplevel()
        AddSubjWin.geometry("300x80")
        AddSubjWin.title("Add Subject")
        newSubjname = StringVar()
        ttk.Entry(AddSubjWin,textvariable=newSubjname,width= 30).grid(column=2, row=0,columnspan= 2, padx=5, pady=5)
        ttk.Label(AddSubjWin, text = "Subject Name").grid(column=0, row=0,columnspan= 2,padx = 10)
        ttk.Button(AddSubjWin,text = "OK",command = addsubj).grid(column=2, row=3)
        ttk.Button(AddSubjWin,text = "Cancel",command = AddSubjWin.destroy).grid(column=3, row=3)
        AddSubjWin.mainloop()

    def editSubjWin():

        def editsubj(): #errorrrrr
            a.editSubject(str(listbox1.get(listbox1.curselection())),str(newSubjname.get()))
            showSubj()
            EditSubjWin.destroy()

        def delsubj():
            if messagebox.askokcancel("Delete Subject", "Are you sure?"):
                a.delSubject(str(listbox1.get(listbox1.curselection())))
                showSubj()
                EditSubjWin.destroy()
            else:
                pass

        newSubjname = StringVar()
        EditSubjWin = Toplevel()
        EditSubjWin.geometry("380x120")
        EditSubjWin.title(str("Edit "+str(listbox1.get(listbox1.curselection()))))
        ttk.Entry(EditSubjWin,textvariable=newSubjname,width= 40).grid(column=1, row=1,columnspan= 3, padx=5, pady=5)
        ttk.Label(EditSubjWin, text = str(listbox1.get(listbox1.curselection())), font='Helvetica 18 bold').grid(column=0, row=0, padx=5, pady=5)
        ttk.Label(EditSubjWin, text = "New Subject Name").grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(EditSubjWin,text = "OK",command = editsubj).grid(column=1, row=4, padx=5, pady=5)
        ttk.Button(EditSubjWin,text = "Cancel",command = EditSubjWin.destroy).grid(column=2, row=4, padx=5, pady=5)
        ttk.Button(EditSubjWin,text = "Delete",command = delsubj).grid(column=3, row=4, padx=5, pady=5)
        EditSubjWin.mainloop()

    def checkSelect(nextpage):
        if str(listbox1.curselection()) == '()':
            messagebox.showwarning("Warning", "Please select Subject")
            return 
        if nextpage == "edit":
            editSubjWin()
        elif nextpage == "open":
            NextPage('p2')

    def logout():
        p1.destroy()
        loginWindow(userfile)

    def export():

        def Exp(): #export file process
            s = str('Are You sure for export '+ str(CName.get())+' ?')
            special_characters = "!@#$%^&*-+?=,<>/."
            if any(c in special_characters for c in str(CName.get())[:-5]):
                messagebox.showwarning('filename error', 'file name cannot contain special characters. ')
                return 
            if str(CName.get())[-5:] != ".json":
                messagebox.showwarning('filename error', 'file name should be json file')
                return 
            if messagebox.askokcancel('Export', s):
                newfile = {}
                with open(str(filename)) as data_json:
                    currentfile = json.load(data_json)
                    newfile = currentfile
                    data = json.dumps(newfile)
                    jsonFile = open(str(CName.get()),"w")
                    jsonFile.write(data)
                    jsonFile.close()
                
                ExWin.destroy()
                p1.destroy()

        ExWin = Toplevel()
        ExWin.title("Export file")
        ExWin.geometry("300x100")
 
        CName = StringVar()
        CreateName = Entry(ExWin,width= 30,textvariable=CName)
        CreateName.grid(row = 3, column= 2,columnspan= 2, padx = 5,pady = 10) 
        ttk.Label(ExWin,text = str(userfile)).grid(row = 2, column= 0,columnspan= 2, padx = 10)
        ttk.Label(ExWin,text = "file name").grid(row = 3, column= 0,columnspan= 2, padx = 10)
        ttk.Button(ExWin,text = "OK",width=10,command=Exp).grid(row = 5, column= 2)  
        ttk.Button(ExWin,text = "Cancel",width=10,command=ExWin.destroy).grid(row = 5, column= 3)
    
    def importFile():

        def im(): #import file process

            fn = str(fname.get())
            
            if fn in jsonfiles:
                if fn[:9] == "data_json":
                    with open(userfile,mode = 'r') as user_json:
                        us = json.load(user_json)
                        us[user]['filename'] = fn

                    with open(userfile, mode = 'w') as user_json:
                        json.dump(us,user_json)
                    app = Reminder(fn)
                    ImportWin.destroy()
                    p1.destroy()
                    Page1(app,userfile,fn,user)
                else:
                    messagebox.showwarning('json file name', 'Please use User Json file')
                    return
            else:  
                messagebox.showwarning('file name error', 'This file does not exist')
                return

        jsonfiles = []      #json file in directory
        for file in glob.glob("*.json"):
            jsonfiles.append(file)
        s = str(str(user)+" with "+str(filename))
        ImportWin = Toplevel()
        ImportWin.title(s)
        ImportWin.geometry("300x80")
        fname = StringVar()
        topLevelEntry = Entry(ImportWin,width= 35,textvariable=fname)
        topLevelEntry.grid(row = 2, column= 1,columnspan= 2, padx = 5,pady = 10) 
        ttk.Label(ImportWin,text = "Import").grid(row = 2, column= 0,padx = 10)
        ttk.Button(ImportWin,text = "Confirm",width=10,command = im).grid(row = 4, column= 1)  
        ttk.Button(ImportWin,text = "Cancel",width=10,command=ImportWin.destroy).grid(row = 4, column= 2)  

    p1 = Tk()
    p1.title("To do list")
    p1.geometry("350x350")

    ttk.Label(p1, text = "Subject").grid(row = 5, column= 1,padx=10)
    listbox1 = Listbox(p1,width = 30)
    listbox1.grid(row = 5, column = 2,columnspan= 2,rowspan= 4,padx = 10, pady = 20 )
    
    ttk.Button(p1,text = "Add Subject" ,command = AddSubjWindow).grid(row = 6,column=4 )
    ttk.Button(p1,text = "Edit",command = lambda:checkSelect('edit')).grid(row =7,column=4 )
    ttk.Button(p1,text = "Open",command = lambda:checkSelect('open')).grid(row = 5, column = 4)
    ttk.Button(p1, text = "Today",command = lambda:NextPage('ptoday')).grid(row = 3, column = 2)
    ttk.Button(p1, text = "Graph",command = lambda:createGraph(a)).grid(row = 8, column = 4)
    ttk.Button(p1, text = "All",command = lambda:NextPage('pall')).grid(row = 3, column = 3)
    ttk.Button(p1, text = "Log out",command = logout).grid(row = 0, column = 4)
    ttk.Button(p1, text = "Export file",command = export).grid(row = 12, column = 3)
    ttk.Button(p1, text = "Import file",command = importFile).grid(row = 12, column = 2)
    ttk.Label(p1, text = str(len(a.gettodayN()))).grid(row = 4, column = 2,padx = 5)
    ttk.Label(p1, text = str(len(a.getallN()))).grid(row = 4, column = 3, padx = 5)
    showSubj()
    p1.mainloop()

def Page2(a,s,userfile,filename,user):

    def BackPage():
        p2.destroy()
        Page1(a,userfile,filename,user)

    def NextPage():
        select = listbox2.get(listbox2.curselection())
        p2.destroy()
        Page3(a,subj,select,"p2",userfile,filename,user)

    def showList(stat):
        listbox2.delete(0, 'end') #clear all data
        for i in subj.getallListN():
            listO = subj.getallListO()[i]
            if stat == "all": 
                listbox2.insert('end', str(i))
                listbox2.itemconfig('end',fg= Color(subj,str(i)))
                if checktoday(listO.getnotificate(str(subj))):
                    if listO.getcheckbox(str(subj)) != 'True':
                        listbox2.itemconfig('end',bg='#FAA0A0')
                if listO.getnotificate(str(subj)) == str(datetime.datetime.today().strftime('%Y-%m-%d')):
                    if listO.getcheckbox(str(subj)) != 'True':
                        listbox2.itemconfig('end',bg='#FFE7E5')
            else:
                if listO.getcheckbox(str(subj)) == 'False':
                    listbox2.insert('end', str(i))
                    listbox2.itemconfig('end',fg= Color(subj,str(i)))
                    if checktoday(listO.getnotificate(str(subj))):
                        listbox2.itemconfig('end',bg='#FAA0A0')
                    if listO.getnotificate(str(subj)) == str(datetime.datetime.today().strftime('%Y-%m-%d')):
                        listbox2.itemconfig('end',bg='#FFE7E5')

    def addlistWin(): #Subject Object
        
        def setdata():
            l = str(name.get('1.0','end')).splitlines()[0]
            subj.addlist(l)
            Edate = str(noti.get('1.0','end')).splitlines()[0]
            Ecb = str(cb.get('1.0','end')).splitlines()[0]
            Ep = str((pri.get('1.0','end')).splitlines()[0])
            priority = ['0','1','2','3']
            if Ecb == 'True' or Ecb == 'False':
                if Ep in priority:
                    if Edate == "":
                        subj.setdetail(str(l),str(detail.get('1.0','end')).splitlines()[0])
                        subj.setnotificate(str(l),Edate)
                        subj.setpriority(str(l),int(str((pri.get('1.0','end')).splitlines()[0])))
                        subj.setcheckbox(str(l),Ecb)
                        EditdataWin.destroy()
                        #p2.destroy()
                        showList(0)
                        return 
                    if Edate[4] == '-' and Edate[7] == '-' and len(Edate) == 10:
                        ed = Edate.split('-')
                        if ed[0].isnumeric() and ed[1].isnumeric() and ed[2].isnumeric():
                                subj.setdetail(str(l),str(detail.get('1.0','end')).splitlines()[0])
                                subj.setnotificate(str(l),Edate)
                                subj.setpriority(str(l),int(str((pri.get('1.0','end')).splitlines()[0])))
                                subj.setcheckbox(str(l),Ecb)
                                EditdataWin.destroy()
                                #p2.destroy()
                                showList(0)
                        else:
                            messagebox.showerror('Date error', 'Date should be Number')
                    else:
                        messagebox.showerror('Date error', 'Date should be YYYY-MM-DD')
                else:
                    messagebox.showerror('Priority error', 'Priority should be around 0 - 3 and be integer')
            else:
                messagebox.showerror('Checkbox error', 'Check Box should be True or False')

        EditdataWin = Tk()
        EditdataWin.geometry("400x250")
        EditdataWin.title("Edit data")
        ttk.Label(EditdataWin,text = "Name").grid(row=1,column=0,columnspan=2,pady=5)
        name = Text(EditdataWin,height=1,width=20)
        name.grid(row=1,column=2,columnspan=3,pady=5)
        ttk.Label(EditdataWin,text = "detail").grid(row=2,column=0,columnspan=2,pady=5)
        detail = Text(EditdataWin,height=1,width=20)
        detail.grid(row=2,column=2,columnspan=3,pady=5)
        ttk.Label(EditdataWin,text = "Due Date (YYYY-MM-DD)").grid(row=3,column=0,columnspan=2,pady=5)
        noti = Text(EditdataWin,height=1,width=20)
        noti.grid(row=3,column=2,columnspan=3,pady=5)
        ttk.Label(EditdataWin,text = "Priority").grid(row=4,column=0,columnspan=2,pady=5)
        pri = Text(EditdataWin,height=1,width=20,pady=5)
        pri.insert('end',str(0))
        pri.grid(row=4,column=2,columnspan=3)
        ttk.Label(EditdataWin,text = "Checkbox").grid(row=5,column=0,columnspan=2,pady=5)
        cb = Text(EditdataWin,height=1,width=20)
        cb.insert('end','False')
        cb.grid(row=5,column=2,columnspan=3,pady=5)
        cb.configure(state='disabled')
        ttk.Button(EditdataWin,text = "Ok",command = setdata).grid(row=6,column=2,padx = 5)
        ttk.Button(EditdataWin,text = "Back",command = EditdataWin.destroy).grid(row=0,column=0,padx = 5)
        ttk.Button(EditdataWin,text = "Cancel",command = EditdataWin.destroy).grid(row=6,column=3,padx = 5)

    def complete(): #set complete
        subj.setcheckbox(str(listbox2.get(listbox2.curselection())),'True')
        showList(0)
    
    def Dellist():
        if messagebox.askokcancel("Delete List", "Are you sure?"):
            subj.dellist(str(listbox2.get(listbox2.curselection())))
            showList(0)
        else:
            showList(0)
    
    def checkSelect(nextpage):
        if str(listbox2.curselection()) == '()':
            messagebox.showwarning("Warning", "Please select List")
            return 
        if nextpage == "delete":
            Dellist()
        elif nextpage == "open":
            NextPage()
        elif nextpage == "complete":
            complete()
    
    def createGraph():

        def create_charts():
        
            if notcomp == 0:
                data = [late,comp]
                labels2 = 'Lated', 'Completed'  
                figure2 = Figure(figsize=(4,3), dpi=100)
                subplot2 = figure2.add_subplot(111) 

                pieSizes = data
                my_colors2 = ['lightblue','lightsteelblue']
                explode2 = (0, 0.1)  
                subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True, startangle=90) 
                subplot2.axis('equal')  
                pie2 = FigureCanvasTkAgg(figure2, graphWin)
                pie2.get_tk_widget().pack()
            else:
                data = [late,comp,notcomp]
                labels2 = 'Lated', 'Completed', 'Uncompleted'   
                figure2 = Figure(figsize=(4,3), dpi=100) 
                subplot2 = figure2.add_subplot(111) 

                pieSizes = data
                my_colors2 = ['lightblue','lightsteelblue','silver']
                explode2 = (0, 0.1, 0)   
                subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True, startangle=90) 
                subplot2.axis('equal')  
                pie2 = FigureCanvasTkAgg(figure2, graphWin)
                pie2.get_tk_widget().pack()

        if len(a.getallSubjN()) <= 0:
            messagebox.showwarning('Subject Error', 'No Subject')
            return
        if len(a.getallNComp()) <= 0:
            messagebox.showwarning('List Error', 'No List')
            return
        comp = 0
        late = 0
        for l in subj.getallListN():
            ls = subj.getallListO()[l]
            if ls.getcheckbox(str(s)) == "True":
                comp += 1
            elif checktoday(str(ls.getnotificate(str(subj)))): #return true when late
                late += 1

        notcomp = len(subj.getallListN()) - comp - late

        graphWin= Toplevel()
        tt = str("Overall smmary "+ str(s))  
        graphWin.title(tt)
        graphWin = Canvas(graphWin, width = 300, height = 300)
        graphWin.pack()
        create_charts()

 
    subj = a.getallSubjO()[str(s)]
    p2 = Tk()
    p2.geometry("400x300")
    p2.title(str(subj))
    ttk.Label(p2, text = str(subj), font='Helvetica 18 bold').grid(row = 9, column = 2)
    listbox2 = Listbox(p2,width = 30, height= 10)
    listbox2.grid(row = 10, column = 2,columnspan= 2,rowspan= 4,padx = 10, pady = 20 )
    ttk.Button(p2,text = "Add List",command= addlistWin).grid(row = 11,column=4 )
    ttk.Button(p2,text = "Delete",command = lambda:checkSelect("delete")).grid(row = 13,column=4 )
    ttk.Button(p2,text = "Open",command = lambda:checkSelect("open")).grid(row = 10, column = 4)
    ttk.Button(p2,text = "Back",command = BackPage).grid(row = 0, column = 0)
    ttk.Button(p2,text = "Complete",command = lambda:checkSelect("complete")).grid(row = 12,column=4 )
    ttk.Button(p2,text = "ShowAll",command = lambda:showList('all')).grid(row = 15,column=3 )
    ttk.Button(p2,text = "Graph",command = createGraph).grid(row = 15,column=2 )
    showList(0)
    p2.mainloop()

def Page3(a,s,l,bp,userfile,filename,user):

    def showdata():
        def BackPage():
            p3.destroy()
            if bp == "p2":
                Page2(a,s,userfile,filename,user)
            elif bp == "pall":
                showAllList(a,"all",userfile,filename,user)
            elif bp == "ptoday":
                showAllList(a,"today",userfile,filename,user)

        def editlist():

            def setdata():
                Edate = str(noti.get('1.0','end')).splitlines()[0]
                Ecb = str(cb.get('1.0','end')).splitlines()[0]
                Ep = str((pri.get('1.0','end')).splitlines()[0])
                priority = ['0','1','2','3']
                if Ecb == 'True' or Ecb == 'False':
                    if Ep in priority:
                        if Edate == "":
                            s.setdetail(str(l),str(detail.get('1.0','end')).splitlines()[0])
                            s.setnotificate(str(l),Edate)
                            s.setpriority(str(l),int(str((pri.get('1.0','end')).splitlines()[0])))
                            s.setcheckbox(str(l),Ecb)
                            newln = str(name.get('1.0','end')).splitlines()[0]
                            s.editlistname(str(l),newln)
                            EditdataWin.destroy()
                            p3.destroy()
                            showdata()
                            return 
                        if len(Edate) < 10:
                            messagebox.showerror('Date error', 'Date should be YYYY-MM-DD')
                            return
                        if Edate[4] == '-' and Edate[7] == '-' and len(Edate) == 10:
                            ed = Edate.split('-')
                            if ed[0].isnumeric() and ed[1].isnumeric() and ed[2].isnumeric() and ed[1] != "00" and ed[2] != "00" and ed[0] != "0000" and int(ed[1]) <= 12 and int(ed[2]) <= 31:
                                    s.setdetail(str(l),str(detail.get('1.0','end')).splitlines()[0])
                                    s.setnotificate(str(l),Edate)
                                    s.setpriority(str(l),int(str((pri.get('1.0','end')).splitlines()[0])))
                                    s.setcheckbox(str(l),Ecb)
                                    newln = str(name.get('1.0','end')).splitlines()[0]
                                    s.editlistname(str(l),newln)
                                    EditdataWin.destroy()
                                    p3.destroy()
                                    showdata()
                            else:
                                messagebox.showerror('Date error', 'Date error')
                        else:
                            messagebox.showerror('Date error', 'Date should be YYYY-MM-DD')
                    else:
                        messagebox.showerror('Priority error', 'Priority should be around 0 - 3 and be integer')
                else:
                    messagebox.showerror('Checkbox error', 'Check Box should be True or False')
                
            
            def dellist():
                if messagebox.askokcancel("Delete List", "Are you sure?"):
                    s.dellist(str(l))
                    EditdataWin.destroy()
                    BackPage()
                else:
                    EditdataWin.destroy()
                    BackPage()
                
            EditdataWin = Tk()
            EditdataWin.geometry("400x220")
            EditdataWin.title("Edit data")
            ttk.Label(EditdataWin,text = "Name").grid(row = 1, column= 0,columnspan=2,pady = 5)
            name = Text(EditdataWin,height=1,width=30)
            name.insert('end',str(ln.getlistname()))
            name.grid(row = 1, column= 2,columnspan=3,pady = 5)
            ttk.Label(EditdataWin,text = "detail").grid(row = 2, column= 0,columnspan=2,pady = 5)
            detail = Text(EditdataWin,height=1,width=30)
            detail.insert('end',str(ln.getdetail(str(s))))
            detail.grid(row = 2, column= 2,columnspan=3,pady = 5)
            ttk.Label(EditdataWin,text = "Due Date (YYYY-MM-DD)").grid(row = 3, column= 0,columnspan=2,pady = 5)
            noti = Text(EditdataWin,height=1,width=30)
            noti.insert('end',str(ln.getnotificate(str(s))))
            noti.grid(row = 3, column= 2,columnspan=3,pady = 5)
            ttk.Label(EditdataWin,text = "Priority").grid(row = 4, column= 0,columnspan=2,pady = 5)
            pri = Text(EditdataWin,height=1,width=30)
            pri.insert('end',str(ln.getpriority(str(s))))
            pri.grid(row = 4, column= 2,columnspan=3,pady = 5)
            ttk.Label(EditdataWin,text = "Checkbox").grid(row = 5, column= 0,columnspan=2,pady = 5)
            cb = Text(EditdataWin,height=1,width=30)
            cb.insert('end',str(ln.getcheckbox(str(s))))
            cb.grid(row = 5, column= 2,columnspan=3,pady = 5)
            ttk.Button(EditdataWin,text = "Ok",command = setdata).grid(row = 6, column= 2,padx = 5)
            ttk.Button(EditdataWin,text = "Back",command = EditdataWin.destroy).grid(row = 0, column= 0)
            ttk.Button(EditdataWin,text = "Delete",command = dellist).grid(row = 6, column= 4,padx = 5)
            ttk.Button(EditdataWin,text = "Cancle",command = EditdataWin.destroy).grid(row = 6, column= 3,padx = 5)

        p3 = Tk()
        p3.geometry("400x250")
        p3.title(str(l))
        ttk.Label(p3,text = "Name").grid(column=0, row=1, padx=5, pady=5)
        name = Text(p3,height=1,width=30)
        name.insert('end',str(ln.getlistname()))
        name.grid(column=1, row=1,columnspan=3, padx=5, pady=5)
        name.configure(state='disabled')
        ttk.Label(p3,text = "detail").grid(column=0, row=2, padx=5, pady=5)
        detail = Text(p3,height=1,width=30)
        detail.insert('end',str(ln.getdetail(str(s))))
        detail.grid(column=1, row=2,columnspan=3, padx=5, pady=5)
        detail.configure(state='disabled')
        ttk.Label(p3,text = "Due Date").grid(column=0, row=3, padx=5, pady=5)
        noti = Text(p3,height=1,width=30)
        noti.insert('end',str(ln.getnotificate(str(s))))
        noti.grid(column=1, row=3,columnspan=3, padx=5, pady=5)
        noti.configure(state='disabled')
        ttk.Label(p3,text = "Priority").grid(column=0, row=4, padx=5, pady=5)
        pri = Text(p3,height=1,width=30)
        pri.insert('end',str(ln.getpriority(str(s))))
        pri.grid(column=1, row=4,columnspan=3, padx=5, pady=5)
        pri.configure(state='disabled')
        ttk.Label(p3,text = "Checkbox").grid(column=0, row=5, padx=5, pady=5)
        cb = Text(p3,height=1,width=30)
        cb.insert('end',str(ln.getcheckbox(str(s))))
        cb.grid(column=1, row=5,columnspan=3, padx=5, pady=5)
        cb.configure(state='disabled')
        ttk.Button(p3,text = "Edit",command = editlist).grid(column=2, row=6, padx=5, pady=5)
        ttk.Button(p3,text = "Back",command = BackPage).grid(column=0, row=0, padx=5, pady=5)
        p3.mainloop()

    ln = s.getallListO()[str(l)]
    showdata()
       


############-----------------  Create GUI  -----------------############

loginWindow('user.json')
