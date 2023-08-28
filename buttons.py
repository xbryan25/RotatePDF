import customtkinter as ctk
import easygui
from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import os


class Buttons:
    def __init__(self, window):
        self.window = window

        # Initializing the buttons
        self.insert_button = ctk.CTkButton(self.window, text="Open .pdf", command=lambda: self.button_event(),
                                           hover_color='blue')
        self.insert_button.place(x=50, y=40)

        self.right_button = ctk.CTkButton(self.window, text="Rotate right", command=lambda: self.rotate_photo('right'),
                                          hover_color='blue', width=50)
        self.right_button.place(x=320, y=40)

        self.left_button = ctk.CTkButton(self.window, text="Rotate left", command=lambda: self.rotate_photo('left'),
                                         hover_color='blue', width=50)
        self.left_button.place(x=230, y=40)

        self.save_button = ctk.CTkButton(self.window, text="Save orientation", command=lambda: self.save_pdf(),
                                         hover_color='blue', width=50)
        self.save_button.place(x=260, y=195)

        # Initial states of buttons
        self.left_button.configure(state='disabled')
        self.right_button.configure(state='disabled')
        self.save_button.configure(state='disabled')

        # Initialization of entry widget
        self.entry = ctk.CTkEntry(self.window, state='disabled')
        self.entry.bind("<Button-1>", lambda e: self.entry.delete(0, 'end'))
        self.entry.place(x=50, y=195)

        # Initialization of label widget
        self.pdf_label = ctk.CTkLabel(self.window, text='No file loaded')
        self.pdf_label.place(x=83, y=10)

        # Loading of pictures using PIL
        self.pic_1 = ctk.CTkImage(
            Image.open(r"Assets\Pic1.png"),
            size=(125, 100))
        self.pic_1_label = ctk.CTkLabel(master=self.window, image=self.pic_1, text="")

        self.pic_2 = ctk.CTkImage(
            Image.open(r"Assets\Pic2.png"),
            size=(110, 100))
        self.pic_2_label = ctk.CTkLabel(master=self.window, image=self.pic_2, text="")

        self.pic_3 = ctk.CTkImage(
            Image.open(r"Assets\Pic3.png"),
            size=(125, 100))
        self.pic_3_label = ctk.CTkLabel(master=self.window, image=self.pic_3, text="")

        self.pic_4 = ctk.CTkImage(
            Image.open(r"Assets\Pic4.png"),
            size=(110, 100))
        self.pic_4_label = ctk.CTkLabel(master=self.window, image=self.pic_4, text="")

        # Initialization of variables
        self.old_pdf_angle = 0
        self.new_pdf_angle = 0

        self.file_path = ''

    def rotate_photo(self, direction):
        # State of entry widget once a rotate button is clicked
        self.entry.configure(state='normal')
        self.entry.delete(0, 'end')

        if direction == 'left':
            self.new_pdf_angle -= 90
            if self.new_pdf_angle < 0:
                self.new_pdf_angle = 270

        if direction == 'right':
            self.new_pdf_angle += 90
            if self.new_pdf_angle >= 360:
                self.new_pdf_angle = 0

        if self.new_pdf_angle == 90:
            self.pic_1_label.place_forget()
            self.pic_2_label.place_forget()
            self.pic_4_label.place_forget()

            self.pic_3_label.place(x=250, y=80)

        elif self.new_pdf_angle == 180:
            self.pic_1_label.place_forget()
            self.pic_3_label.place_forget()
            self.pic_4_label.place_forget()

            self.pic_2_label.place(x=258, y=80)

        elif self.new_pdf_angle == 270:
            self.pic_2_label.place_forget()
            self.pic_3_label.place_forget()
            self.pic_4_label.place_forget()

            self.pic_1_label.place(x=250, y=80)

        elif self.new_pdf_angle == 0 or self.new_pdf_angle == 360:
            self.pic_1_label.place_forget()
            self.pic_2_label.place_forget()
            self.pic_3_label.place_forget()

            self.pic_4_label.place(x=258, y=80)

    def button_event(self):
        # Enables the option to only view .pdf files
        file_path = easygui.fileopenbox(msg='Please locate the PDF', filetypes=["*.pdf", "All files"])

        # If prompt screen is left without choosing a .pdf file
        if not file_path:
            self.entry.configure(state='normal')
            self.entry.delete(0, 'end')
            self.entry.insert(0, 'Choose a .pdf file')
            self.entry.configure(state='disabled')

        # If a .pdf file is chosen
        elif file_path.endswith(".pdf"):
            self.entry.configure(state='normal')
            self.entry.delete(0, 'end')
            self.entry.insert(0, 'File found!')
            self.entry.configure(state='disabled')
            self.file_path = file_path

            pdf = PdfReader(open(file_path, 'rb'))

            if not pdf.pages[0].get('/Rotate'):
                self.new_pdf_angle = 0
                self.old_pdf_angle = 0
            else:
                self.new_pdf_angle = (pdf.pages[0].get('/Rotate'))
                self.old_pdf_angle = (pdf.pages[0].get('/Rotate'))

            if self.new_pdf_angle == 360 or self.old_pdf_angle == 360:
                self.new_pdf_angle = 0
                self.old_pdf_angle = 0

            self.left_button.configure(state='normal')
            self.right_button.configure(state='normal')
            self.save_button.configure(state='normal')

            self.pdf_label.configure(text=f'You are editing: {os.path.basename(file_path)}')
            self.pdf_initial_view()

        # If a file is chosen but not a .pdf file
        else:
            self.entry.configure(state='normal')
            self.entry.delete(0, 'end')
            self.entry.insert(0, 'Choose a .pdf file')
            self.entry.configure(state='disabled')

    def save_pdf(self):
        # Gets name from entry widget
        new_name = self.entry.get()

        # Cant' save when no name is inputted
        if not new_name:
            self.entry.delete(0, 'end')
            self.entry.configure(placeholder_text='Input name for file.')

        else:
            reader = PdfReader(self.file_path)
            writer = PdfWriter()

            # Rotates every page
            for i in range(len(reader.pages)):
                writer.add_page(reader.pages[i])

                if self.new_pdf_angle == 0:
                    self.new_pdf_angle = 360

                writer.pages[i].rotate(self.new_pdf_angle - self.old_pdf_angle)

            # Saves the edited .pdf file at the same directory of the original file
            with open(os.path.join(os.path.dirname(self.file_path), f"{new_name}.pdf"), "wb") as fp:
                writer.write(fp)

            self.entry.delete(0, 'end')
            self.entry.configure(placeholder_text='Process done!')
            self.entry.configure(state="disabled")

            self.save_button.configure(state="disabled")

            # Makes the pdf picture stand upright

            self.pic_1_label.place_forget()
            self.pic_2_label.place_forget()
            self.pic_3_label.place_forget()

            self.pic_4_label.place(x=258, y=80)
            self.new_pdf_angle = 0

            self.pdf_label.configure(text="Select a new .pdf to rotate")

    def pdf_initial_view(self):
        # This method provides the functionality of being able to view the orientation of the .pdf once it is loaded
        if self.old_pdf_angle == 90:
            self.pic_1_label.place_forget()
            self.pic_2_label.place_forget()
            self.pic_4_label.place_forget()

            self.pic_3_label.place(x=250, y=80)

        elif self.old_pdf_angle == 180:
            self.pic_1_label.place_forget()
            self.pic_3_label.place_forget()
            self.pic_4_label.place_forget()

            self.pic_2_label.place(x=258, y=80)

        elif self.old_pdf_angle == 270:
            self.pic_2_label.place_forget()
            self.pic_3_label.place_forget()
            self.pic_4_label.place_forget()

            self.pic_1_label.place(x=250, y=80)

        elif self.old_pdf_angle == 0 or self.new_pdf_angle == 360:
            self.pic_1_label.place_forget()
            self.pic_2_label.place_forget()
            self.pic_3_label.place_forget()

            self.pic_4_label.place(x=258, y=80)
