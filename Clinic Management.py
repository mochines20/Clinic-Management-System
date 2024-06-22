from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import random
from tkinter import Scrollbar
from tkinter import Text
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
        self.cursor = self.conn.cursor()

    def __del__(self)
        self.conn.close()

    def insert_data(self, data):
        try:
            patient_id = str(random.randint(10000, 99999))
            self.cursor.execute("""
                INSERT INTO users (PatientId, PatientName, Age, Sex, Sr_code, Block, Course, Department, Medicine_name, Quantity, Doctor_name, Reason, doctor_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    patient_id,
                    data['PatientName'],
                    data['Age'],
                    data['Sex'],
                    data['Sr_code'],
                    data['Block'],
                    data['Course'],
                    data['Department'],
                    data['Medicine_name'],
                    data['Quantity'],
                    data['Doctor_name'],
                    data['Reason'],
                    data['doctor_number']
                ))
            self.conn.commit()
            return True, "Prescription data inserted successfully!"
        except mysql.connector.Error as err:
            return False, f"Error: {err}"

    def update_data(self, data):
        try:
            self.cursor.execute("""
                UPDATE users
                SET PatientName = %s, Age = %s, Sex = %s, Sr_code = %s,
                    Block = %s, Course = %s, Department = %s,
                    Medicine_name = %s, Quantity = %s, Doctor_name = %s, Reason = %s, doctor_number = %s
                WHERE PatientId = %s""",
                (
                    data['PatientName'],
                    data['Age'],
                    data['Sex'],
                    data['Sr_code'],
                    data['Block'],
                    data['Course'],
                    data['Department'],
                    data['Medicine_name'],
                    data['Quantity'],
                    data['Doctor_name'],
                    data['Reason'],
                    data['doctor_number'],
                    data['PatientId']
                ))
            self.conn.commit()
            return True, "Record updated successfully!"
        except mysql.connector.Error as err:
            return False, f"Error: {err}"

    def delete_data(self, patient_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE PatientId = %s", (patient_id,))
            self.conn.commit()
            return True, "Record deleted successfully!"
        except mysql.connector.Error as err:
            return False, f"Error: {err}"

    def fetch_data(self):
        try:
            self.cursor.execute("""SELECT PatientId, PatientName, Age, Sex, Sr_code, Block, Course, Department, Medicine_name, Quantity, Doctor_name, Reason , doctor_number, Timestamp FROM users""")
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            return None, f"Error fetching data: {err}"

class Clinic:  
    def __init__(self, root):

        self.root = root
        self.root.title("Clinic Management System")
        self.root.geometry("1450x600+0+0")
        self.root.resizable(True,True)

        self.PatientId=StringVar()
        self.PatientName=StringVar()
        self.Age=StringVar()
        self.Sex=StringVar()
        self.Sr_code=StringVar()
        self.Block=StringVar()
        self.Course=StringVar()
        self.Department=StringVar()
        self.MedicineName=StringVar()
        self.Quantity=StringVar()
        self.Doctor_name=StringVar()
        self.Reason = StringVar()
        self.doctor_number=StringVar()

        self.logo = PhotoImage(file="logo.png").subsample(5)  
        lbltitle = Label(self.root, bd=20, relief=RIDGE, text="Clinic Management System", fg="blue", bg="white", font=("times new roman", 50, "bold"), compound=LEFT, image=self.logo)
        lbltitle.config(borderwidth=0, highlightbackground="black")
        lbltitle.pack(side=TOP, fill=X)

        # ===============Dataframe=============================
        Dataframe=Frame(self.root,bd=20,relief=RIDGE)
        Dataframe.place(x=0,y=130,width=1530,height=400)

        DataframeLeft=LabelFrame(Dataframe,bd=10,relief=RIDGE,padx=10,
        font=("times new roman", 12, "bold") ,text="Patient record")
        DataframeLeft.place(x=0,y=5,width=500,height=350)

        DataframeMid=LabelFrame(Dataframe,bd=10,relief=RIDGE,padx=10,
        font=("times new roman", 12, "bold") ,text="Prescription")
        DataframeMid.place(x=500,y=5,width=500,height=350)

        DataframeRight=LabelFrame(Dataframe,bd=10,relief=RIDGE,padx=10,
        font=("times new roman", 12, "bold") ,text="Medical Records")
        DataframeRight.place(x=1000,y=5,width=460,height=350)

        # =================Buttonsframe ====================

        Buttonframe=Frame(self.root,bd=20,relief=RIDGE)
        Buttonframe.place(x=0,y=530,width=1530,height=70)

        # =================Details frame ====================

        Detailsframe=Frame(self.root,bd=20,relief=RIDGE)
        Detailsframe.place(x=0,y=600,width=1530,height=190)

        # =====================DataframeLeft===================
        patient_id = str(random.randint(10000, 99999))

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Patient ID:", padx=2)
        lblref.grid(row=0, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.PatientId, width=35)
        txtref.insert(0, patient_id)  
        txtref.config(state='readonly')  
        txtref.grid(row=0, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Patient Name:", padx=2)
        lblref.grid(row=1, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.PatientName, width=35)
        txtref.grid(row=1, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Age:", padx=2)
        lblref.grid(row=2, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.Age,  width=35)
        txtref.grid(row=2, column=1)
        
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"), textvariable=self.Age,  width=35)
        txtref.config(validate='key', validatecommand=(self.root.register(self.validate_numeric_input), '%d', '%P'))
        txtref.grid(row=2, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Sex:", padx=2)
        lblref.grid(row=3, column=0, sticky=W)
        comNametablet = ttk.Combobox(DataframeLeft,textvariable=self.Sex, font=("times new roman", 12, "bold"), width=35)
        comNametablet["values"] = ("Male", "Female")
        comNametablet.grid(row=3, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Sr_code:", padx=2)
        lblref.grid(row=4, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.Sr_code,  width=35)
        txtref.grid(row=4, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Course:", padx=2)
        lblref.grid(row=5, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.Course,  width=35)
        txtref.grid(row=5, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Department:", padx=2)
        lblref.grid(row=6, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.Department,  width=35)
        txtref.grid(row=6, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Block:", padx=2)
        lblref.grid(row=7, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.Block,  width=35)
        txtref.grid(row=7, column=1)
        
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"), textvariable=self.Block,  width=35)
        txtref.config(validate='key', validatecommand=(self.root.register(self.validate_numeric_input), '%d', '%P'))
        txtref.grid(row=7, column=1)
        
        # =====================DataframeMid===================

        lblref = Label(DataframeMid, font=("arial", 12, "bold"), text="Medicine Name:", padx=2)
        lblref.grid(row=0, column=2, sticky=W)
        txtref = Entry(DataframeMid, font=("arial", 12, "bold"), textvariable=self.MedicineName,  width=35)
        txtref.grid(row=0, column=3)

        lblref = Label(DataframeMid, font=("arial", 12, "bold"), text="Quantity:", padx=2)
        lblref.grid(row=1, column=2, sticky=W)
        txtref = Entry(DataframeMid, font=("arial", 12, "bold"), textvariable=self.Quantity, width=35)
        txtref.grid(row=1, column = 3)
        
        txtref = Entry(DataframeMid, font=("arial", 12, "bold"), textvariable=self.Quantity,  width=35)
        txtref.config(validate='key', validatecommand=(self.root.register(self.validate_numeric_input), '%d', '%P'))
        txtref.grid(row=1, column=3)
        
        lbldoc = Label(DataframeMid, font=("arial", 12, "bold"), text="Doctor Name:", padx=2)
        lbldoc.grid(row=2, column=2, sticky=W)
        comDoctor = ttk.Combobox(DataframeMid, textvariable=self.Doctor_name, font=("times new roman", 12, "bold"), width=35)
        comDoctor["values"] = ("Dr Bondoc", "Dr Esplanada", "Rn Evangelio")
        comDoctor.grid(row=2, column=3)

        lblref = Label(DataframeMid, font=("arial", 12, "bold"), text="Reason:", padx=2)
        lblref.grid(row=3, column=2, sticky=W)
        txtref = Entry(DataframeMid, font=("arial", 12, "bold"), textvariable=self.Reason, width=35)
        txtref.grid(row=3, column=3)
        
        lblref = Label(DataframeMid, font=("arial", 12, "bold"), text="Doctor Number:", padx=2)
        lblref.grid(row=4, column=2, sticky=W)
        txtref = Entry(DataframeMid, font=("arial", 12, "bold"), textvariable=self.doctor_number, width=35)
        txtref.grid(row=4, column=3)

        # =================DataframeRight====================
        self.txtPrescription = Text(DataframeRight, font=("arial", 12, "bold"), width=45, height=12, padx=2, pady=6)
        self.txtPrescription.grid(row=0, column=0)
        
        self.txtSearch = Entry(DataframeRight, font=("arial", 12, "bold"), width=35)
        self.txtSearch.grid(row=4, column=0)
        
        btnSearch = Button(DataframeRight, command=self.search_data, text="Search", bg="green", fg="white", font=("arial", 12, "bold"), width=15, height=1, padx=2, pady=7)
        btnSearch.grid(row=5, column=0)
        
        # =================Button====================
        btnPrescription = Button(Buttonframe,command=self.iPrescriptionData, text="Prescription", bg="green", fg="white", font=("arial", 12, "bold"), width=24, height=2, padx=2, pady=6)
        btnPrescription.grid(row=0, column=0)

        btnPrescriptionData = Button(Buttonframe, command=self.displayPrescriptionData, text="Prescription Data", bg="green", fg="white", font=("arial", 12, "bold"), width=24, height=2, padx=3, pady=7)
        btnPrescriptionData.grid(row=0, column=1)

        btnUpdate = Button(Buttonframe,command=self.update_data, text="Update", bg="green", fg="white", font=("arial", 12, "bold"), width=24, height=2, padx=2, pady=6)
        btnUpdate.grid(row=0, column=2)

        btnDelete = Button(Buttonframe,command=self.delete, text="Delete", bg="green", fg="white", font=("arial", 12, "bold"), width=24, height=2, padx=2, pady=7)
        btnDelete.grid(row=0, column=3)

        btnClear = Button(Buttonframe,command=self.clear ,text="Clear", bg="green", fg="white", font=("arial", 12, "bold"), width=24, height=2, padx=2, pady=7)
        btnClear.grid(row=0, column=4)

        btnExit = Button(Buttonframe,command=self.iExit ,text="Exit", bg="green", fg="white", font=("arial", 12, "bold"), width=24, height=2, padx=2, pady=7)
        btnExit.grid(row=0, column=5)
        
        # =================Table====================
        # =================Scrollbar====================
        scroll_x = ttk.Scrollbar(Detailsframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Detailsframe, orient=VERTICAL)
        self.Clinic_table = ttk.Treeview(Detailsframe, columns=("PatientId", "PatientName", "Age", "Sex", "Sr_code", "Block", "Course", "Department", "Medicine_name", "Quantity", "Doctor_name","Reason" , "doctor_number"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.config(command=self.Clinic_table.xview)
        scroll_y.config(command=self.Clinic_table.yview)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.Clinic_table.heading("PatientId",text="Patient ID")
        self.Clinic_table.heading("PatientName",text="Patient Name")
        self.Clinic_table.heading("Age",text="Age")
        self.Clinic_table.heading("Sex",text="Sex")
        self.Clinic_table.heading("Sr_code",text="Sr_code")
        self.Clinic_table.heading("Block",text="Block")
        self.Clinic_table.heading("Course",text="Course")
        self.Clinic_table.heading("Department", text="Department")  
        self.Clinic_table.heading("Medicine_name",text="Medicine_name")
        self.Clinic_table.heading("Quantity",text="Quantity")
        self.Clinic_table.heading("Doctor_name",text="Doctor_name")
        self.Clinic_table.heading("Reason",text="Reason")
        self.Clinic_table.heading("doctor_number",text="Doctor_number")

        self.Clinic_table["show"]="headings"

        self.Clinic_table.pack(fill=BOTH,expand=1)
        self.Clinic_table.column("PatientId",width=100)
        self.Clinic_table.column("PatientName",width=100)
        self.Clinic_table.column("Age",width=100)
        self.Clinic_table.column("Sex",width=100)
        self.Clinic_table.column("Sr_code",width=100)
        self.Clinic_table.column("Block",width=100)
        self.Clinic_table.column("Course",width=100)
        self.Clinic_table.column("Department",width=100)
        self.Clinic_table.column("Medicine_name",width=100)
        self.Clinic_table.column("Quantity",width=100)
        self.Clinic_table.column("Doctor_name",width=100)
        self.Clinic_table.column("Reason",width=100)
        self.Clinic_table.column("doctor_number",width=100)
        self.Clinic_table.pack(fill=BOTH,expand=1)
        self.fetch_data()
        self.Clinic_table.bind("<ButtonRelease-1>",self.get_cursor)
        
    # ==========database=========
    
    def iPrescriptionData(self):
        if self.PatientName.get() == "":
            messagebox.showerror("Error", "Patient Name is required")
        else:
            try:
                patient_id = self.PatientId.get()
                if patient_id == "":
                    while True:
                        new_patient_id = str(random.randint(10000, 99999))
                        if not self.check_patient_id_exists(new_patient_id):
                            patient_id = new_patient_id
                            break
                    self.PatientId.set(patient_id)
                    
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
                my_cursor = conn.cursor()
                my_cursor.execute("""
                        INSERT INTO users (PatientId, PatientName, Age, Sex, Sr_code, Block, Course, Department, Medicine_name, Quantity, Doctor_name, Reason, doctor_number, Timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            patient_id, 
                            self.PatientName.get(),
                            self.Age.get(),
                            self.Sex.get(),
                            self.Sr_code.get(),
                            self.Block.get(),
                            self.Course.get(),
                            self.Department.get(),
                            self.MedicineName.get(),
                            self.Quantity.get(),
                            self.Doctor_name.get(),
                            self.Reason.get(),
                            self.doctor_number.get(),
                            current_timestamp  
                        ))
                conn.commit()
                conn.close()
                self.fetch_data()
                self.PatientName.set("")
                self.Age.set("")
                self.Sex.set("")
                self.Sr_code.set("")
                self.Block.set("")
                self.Course.set("")
                self.Department.set("")
                self.MedicineName.set("")
                self.Quantity.set("")
                self.Doctor_name.set("")
                self.Reason.set("") 
                self.doctor_number.set("") 
                messagebox.showinfo("Success", "Prescription data inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

    def check_patient_id_exists(self, patient_id):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT PatientId FROM users WHERE PatientId = %s", (patient_id,))
            row = my_cursor.fetchone()
            conn.close()
            return row is not None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error checking PatientId existence: {err}")
            return True 

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                SELECT PatientId, PatientName, Age, Sex, Sr_code, Block, Course, Department, Medicine_name, Quantity, Doctor_name, Reason, doctor_number, Timestamp
                FROM users
                ORDER BY Timestamp ASC""")
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.Clinic_table.delete(*self.Clinic_table.get_children())
                for i in rows:
                    self.Clinic_table.insert("", END, values=i[:13])
                conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching data: {err}")

    def update_data(self):
        selected_item = self.Clinic_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update.")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                UPDATE users
                SET PatientName = %s, Age = %s, Sex = %s, Sr_code = %s,
                    Block = %s, Course = %s, Department = %s,
                    Medicine_name = %s, Quantity = %s, Doctor_name = %s, Reason = %s, doctor_number = %s
                WHERE PatientId = %s""",
                (
                    self.PatientName.get(),
                    self.Age.get(),
                    self.Sex.get(),
                    self.Sr_code.get(),
                    self.Block.get(),
                    self.Course.get(),
                    self.Department.get(),
                    self.MedicineName.get(),
                    self.Quantity.get(),
                    self.Doctor_name.get(),
                    self.Reason.get(),
                    self.doctor_number.get(),
                    self.PatientId.get()
                ))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Record updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def delete(self):
        selected_item = self.Clinic_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.")
            return
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
        if confirmation:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
                my_cursor = conn.cursor()
                cursor_row = self.Clinic_table.focus()
                contents = self.Clinic_table.item(cursor_row)
                patient_id = contents['values'][0]  
                my_cursor.execute("DELETE FROM users WHERE PatientId = %s", (patient_id,))
                conn.commit()
                conn.close()
                
                self.auto_refresh()
                messagebox.showinfo("Success", "Record deleted successfully!")
                
                self.clear_prescription_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

    def auto_refresh(self):
        self.fetch_data()
        self.clear()

    def clear(self):
        patient_id = str(random.randint(10000, 99999))
        self.PatientId.set(patient_id)
        self.PatientName.set("")
        self.Age.set("")
        self.Sex.set("")
        self.Sr_code.set("")
        self.Block.set("")
        self.Course.set("")
        self.Department.set("")
        self.MedicineName.set("")
        self.Quantity.set("")
        self.Doctor_name.set("")
        self.Reason.set("")
        self.doctor_number.set("")

        self.txtSearch.delete(0, END)
        self.clear_prescription_data()

    def clear_prescription_data(self):
        self.txtPrescription.delete(1.0, END)

    def iExit(self):
        iExit=messagebox.askyesno("Clinic Management System","Confirm you want to exit")
        if iExit>0:
            root.destroy()
            return
        
    def validate_numeric_input(self, action, value_if_allowed):
        if action == '1':  
            if value_if_allowed.isdigit():
                return True
            else:
                self.root.bell()  
                return False
        return True
    
    def search_data(self):
        search_term = self.txtSearch.get().strip()
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term.")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                SELECT PatientId, PatientName, Age, Sex, Sr_code, Block, Course, Department, Medicine_name, Quantity, Doctor_name, Reason, Doctor_number ,Timestamp
                FROM users
                WHERE PatientId = %s OR Sr_code = %s OR doctor_number = %s
                ORDER BY Timestamp ASC""", (search_term, search_term, search_term))
            rows = my_cursor.fetchall()
            if rows:
                messagebox.showinfo("Prescription Data", f"Found {len(rows)} record(s) with Patient ID, Sr_code, or Doctor Number: {search_term}:")
                self.displayPrescriptionData()  
                sorted_rows = sorted(rows, key=lambda x: x[12])
                for row in sorted_rows:
                    messagebox.showinfo("Prescription Data", 
                        f"Patient ID: {row[0]}\n"
                        f"Patient Name: {row[1]}\n"
                        f"Age: {row[2]}\n"
                        f"Sex: {row[3]}\n"
                        f"Sr_code: {row[4]}\n"
                        f"Block: {row[5]}\n"
                        f"Course: {row[6]}\n"
                        f"Department: {row[7]}\n"
                        f"Medicine Name: {row[8]}\n"
                        f"Quantity: {row[9]}\n"
                        f"Doctor Name: {row[10]}\n"
                        f"Reason: {row[11]}\n"
                        f"Doctor_number: {row[12]}\n"
                        f"Timestamp: {row[13]}\n")    
                self.display_similar_patient_data(search_term)
            else:
                messagebox.showinfo("Info", "No records found with the specified Patient ID, Sr_code, or Doctor Number.")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error searching data: {err}")

    def display_similar_patient_data(self, search_term):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="clinic_management")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                SELECT * FROM users WHERE PatientId = %s OR Sr_code = %s OR doctor_number = %s""", (search_term, search_term, search_term))
            rows = my_cursor.fetchall()
            if rows:
                similar_data = ""
                for row in rows:
                    similar_data += f"Patient ID: {row[0]}\n"
                    similar_data += f"Patient Name: {row[1]}\n"
                    similar_data += f"Age: {row[2]}\n"
                    similar_data += f"Sex: {row[3]}\n"
                    similar_data += f"Sr_code: {row[4]}\n"
                    similar_data += f"Block: {row[5]}\n"
                    similar_data += f"Course: {row[6]}\n"
                    similar_data += f"Department: {row[7]}\n"
                    similar_data += f"Medicine Name: {row[8]}\n"
                    similar_data += f"Quantity: {row[9]}\n"
                    similar_data += f"Doctor Name: {row[10]}\n"
                    similar_data += f"Reason: {row[11]}\n"
                    similar_data += f"Doctor_number: {row[12]}\n"
                    similar_data += f"Timestamp: {row[13]}\n\n"
                self.txtPrescription.delete('1.0', END)
                self.txtPrescription.insert(END, similar_data)
            else:
                messagebox.showinfo("Info", "No similar records found.")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error retrieving similar data: {err}")

    def display_patient_data(self, rows):
        self.patient_data_textbox.config(state='normal')
        self.patient_data_textbox.delete('1.0', 'end')
        for row in rows:
            self.patient_data_textbox.insert('end', f"Patient ID: {row[0]}\n"
                                                    f"Patient Name: {row[1]}\n"
                                                    f"Age: {row[2]}\n"
                                                    f"Sex: {row[3]}\n"
                                                    f"Sr_code: {row[4]}\n"
                                                    f"Block: {row[5]}\n"
                                                    f"Course: {row[6]}\n"
                                                    f"Department: {row[7]}\n"
                                                    f"Medicine Name: {row[8]}\n"
                                                    f"Quantity: {row[9]}\n"
                                                    f"Doctor Name: {row[10]}\n"
                                                    f"Reason: {row[11]}\n"
                                                    f"Doctor_number: {row[12]}\n"
                                                    f"Timestamp: {row[13]}\n\n")
        self.patient_data_textbox.config(state='disabled')
        
    def add_scrollbar(self):
            scrollbar = Scrollbar(self)
            scrollbar.pack(side='right', fill='y')
            self.prescription_data_textbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.prescription_data_textbox.yview)
            
    def displayPrescriptionData(self):
        self.clear_prescription_data() 
        prescription_data = f"PatientID:\t{self.PatientId.get()}\n"
        prescription_data += f"PatientName:\t{self.PatientName.get()}\n"
        prescription_data += f"Age:\t{self.Age.get()}\n"
        prescription_data += f"Sex:\t{self.Sex.get()}\n"
        prescription_data += f"Sr_code:\t{self.Sr_code.get()}\n"
        prescription_data += f"Block:\t{self.Block.get()}\n"
        prescription_data += f"Course:\t{self.Course.get()}\n"
        prescription_data += f"Department:\t{self.Department.get()}\n"
        prescription_data += f"MedicineName:\t{self.MedicineName.get()}\n"
        prescription_data += f"Quantity:\t{self.Quantity.get()}\n"
        prescription_data += f"Doctor_name:\t{self.Doctor_name.get()}\n"
        prescription_data += f"Reason:\t{self.Reason.get()}\n"
        prescription_data += f"Doctor_number:\t{self.doctor_number.get()}\n"
        prescription_data += f"Timestamp:\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"  
        self.txtPrescription.insert(END, prescription_data)

    def get_cursor(self, event):
            cursor_row = self.Clinic_table.focus()
            contents = self.Clinic_table.item(cursor_row)
            row = contents['values']
            if row:
                self.PatientId.set(row[0])
                self.PatientName.set(row[1])
                self.Age.set(row[2])
                self.Sex.set(row[3])
                self.Sr_code.set(row[4])
                self.Block.set(row[5])
                self.Course.set(row[6])
                self.Department.set(row[7])
                self.MedicineName.set(row[8])
                self.Quantity.set(row[9])
                self.Doctor_name.set(row[10])
                self.Reason.set(row[11])
                self.doctor_number.set(row[12])
                self.Timestamp.set(row[13])
            else:
                messagebox.showerror("Error", "Please select a record to update.")

root = Tk()
ob = Clinic(root)
root.mainloop()