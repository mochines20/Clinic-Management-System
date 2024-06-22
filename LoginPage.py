import mysql.connector
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import subprocess

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(host="localhost", user="root", password="", database="mydatabase")
        self.cursor = self.connection.cursor()

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1450x600+0+0')
        self.window.resizable(True, True)
        self.window.title('Login Page')
        self.db = Database()

        # ============================background image============================
        self.bg_frame = Image.open('background1.jpeg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='lightblue', width=1050, height=600)
        self.lgn_frame.place(x=200, y=70)

        # ========================================================================

        self.txt = "WELCOME TO CLINIC MANAGEMENT SYSTEM"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 28, "bold"), bg="lightblue",
                    fg='Darkblue', bd=5, relief=FLAT, anchor='w', justify=CENTER)
        self.heading.place(x=130, y=35, relwidth=1, height=30)
        
        # ============================ Canvas with line ================================================
        
        self.canvas = Canvas(self.lgn_frame, bg="Darkblue", height=2, highlightthickness=0)
        canvas_width = self.lgn_frame.winfo_width()  
        self.canvas.create_line(0, 90, canvas_width, 90, width=20, fill="darkblue")  
        self.canvas.place(x=0, y=100, relwidth=1)

        # ============ Left Side Image ================================================
        self.side_image = Image.open('logobg.png')
        self.side_image = self.side_image.convert("RGBA")  
        self.side_image_with_transparency = Image.new("RGBA", self.side_image.size, (255, 255, 255, 0))  
        self.side_image_with_transparency.paste(self.side_image, (0, 0), self.side_image)  
        photo = ImageTk.PhotoImage(self.side_image_with_transparency)  
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='lightblue')
        self.side_image_label.image = photo
        self.side_image_label.place(x=10, y=105)

        # ============================username====================================

        self.username_label = Label(self.lgn_frame, text="Username", bg="lightblue", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=200)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=230, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=253)
        # ===== Username icon =========
        self.username_icon = Image.open('username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='lightblue')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=225)

        # ============================login button================================

        self.login = Button(self.lgn_frame, text='LOGIN', font=("yu gothic ui", 13, "bold"), 
        width=25, bd=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.login_user)
        self.login.place(x=585, y=330)

        # ============================Forgot password=============================

        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?", font=("yu gothic ui", 13, "bold underline"), fg="darkblue", relief=FLAT,
                                    activebackground="lightblue", borderwidth=0, background="lightblue", cursor="hand2", command=self.forgot_password)
        self.forgot_button.place(x=630, y=380)
        
        # ============================password====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="lightblue", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=260)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=290, width=270)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=315)
        
        # ======== Password icon ================
        self.password_icon = Image.open('password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='lightblue')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=290)
        
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT, activebackground="white", borderwidth=0, background="white",cursor="hand2")
        self.show_button.place(x=860, y=295)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=295)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=295)
        self.password_entry.config(show='*')

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        query = "SELECT password FROM users WHERE username = %s"
        self.db.cursor.execute(query, (username,))
        result = self.db.cursor.fetchone()

        if result and result[0] == password:
            messagebox.showinfo("Login Successful", "You have logged in successfully!")
            subprocess.run(["python", "Clinic Management.py"])
            self.window.destroy()
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")


    def forgot_password(self):
        def send_reset_link():
            email = email_entry.get()
            if email:
                messagebox.showinfo("Reset Link Sent", f"Reset link sent to: {email}")
                forgot_password_window.destroy()  
            else:
                messagebox.showerror("Error", "Please enter your email.")

        forgot_password_window = Toplevel(self.window)
        forgot_password_window.title("Forgot Password")

        email_label = Label(forgot_password_window, text="Enter your email:", font=("yu gothic ui", 12))
        email_label.pack()
        email_entry = Entry(forgot_password_window, font=("yu gothic ui", 12))
        email_entry.pack()

        send_link_button = Button(forgot_password_window, text="Send Reset Link", font=("yu gothic ui", 12), command=send_reset_link)
        send_link_button.pack()
        
def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    page()
