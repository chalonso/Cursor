import tkinter as tk

from tkinter import filedialog, messagebox

 

class EditorNotas(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Editor de Notas")

        self.geometry("600x400")

        # Crear área de texto

        self.text_area = tk.Text(self)

        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Crear menú

        self.crear_menu()

   

    def crear_menu(self):

        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label="Abrir", command=self.abrir_archivo)

        filemenu.add_command(label="Guardar", command=self.guardar_archivo)

        filemenu.add_separator()

        filemenu.add_command(label="Salir", command=self.quit)

        menubar.add_cascade(label="Archivo", menu=filemenu)

        self.config(menu=menubar)

   

    def abrir_archivo(self):

        filepath = filedialog.askopenfilename(

            filetypes=[("Archivos de texto","*.txt"), ("Todos los archivos","*.*")]

        )

        if not filepath:

            return

        try:

            with open(filepath, "r", encoding="utf-8") as file:

                contenido = file.read()

            self.text_area.delete(1.0, tk.END)

            self.text_area.insert(tk.END, contenido)

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

   

    def guardar_archivo(self):

        filepath = filedialog.asksaveasfilename(

            defaultextension=".txt",

            filetypes=[("Archivos de texto","*.txt"), ("Todos los archivos","*.*")]

        )

        if not filepath:

            return

        try:

            contenido = self.text_area.get(1.0, tk.END)

            with open(filepath, "w", encoding="utf-8") as file:

                file.write(contenido)

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

 

if __name__ == "__main__":

    app = EditorNotas()

    app.mainloop()