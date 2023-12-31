import customtkinter as ctk
import ctypes as ct
import buttons


def main():
    app = ctk.CTk()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app.geometry("440x260")
    app.iconbitmap(r'Assets/icon.ico')
    app.resizable(False, False)
    app.title("RotatePDF v1.0 by xbryan")

    # Set icon in taskbar
    myappid = u'mycompany.myproduct.subproduct.version'
    ct.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app.eval("tk::PlaceWindow . center")

    buttons.Buttons(app)

    app.mainloop()


if __name__ == '__main__':
    main()
