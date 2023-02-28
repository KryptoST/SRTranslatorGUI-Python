import glob
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from srtranslator import SrtFile
from srtranslator.translators.deepl import DeeplTranslator

def open_folder():
    folder_path = filedialog.askdirectory(
        title="Open Folder"
    )
    print("Selected folder path:", folder_path)
    clear_data()
    file_paths = glob.glob(os.path.join(folder_path, "**/*.srt"), recursive=True)
    add_file_to_list(file_paths)

def open_file():
    file_path = filedialog.askopenfilenames(
        title="Open Files",
        filetypes=[("Srt files", "*.srt")]
    )
    print("Selected file path:", file_path)
    add_file_to_list(file_path)
    #print(languages.get(combo_box1.get()))
    

def translate_files():
    

    for index, name, status, progress in file_list:
        print(index)
        filepath = f"{name}"
        max_retries = 3
        num_retries = 0
        while num_retries < max_retries:
            try:
                translator = DeeplTranslator()
                srt = SrtFile(filepath)
                srt.translate(translator, languages_source.get(combo_box1.get()), languages_dest.get(combo_box2.get()))
                srt.wrap_lines()
                srt.save(f"{os.path.splitext(filepath)[0]}[{languages_dest.get(combo_box2.get()).upper()}].srt")
                translator.quit()
                # Actualizar el estado del archivo en la lista y en la tabla
                status = "Traducido"
                progress = 100
                update_file_status(index, status)
                update_file_progress(index, progress)

                break # Salir del bucle while si la traducción fue exitosa
            except Exception as e:
                # Actualizar el estado del archivo en la lista y en la tabla
                status = "Error"
                update_file_status(index, status)
                print(f"Error al traducir el archivo {name}: {str(e)}")

                num_retries += 1
                if num_retries == max_retries:
                    print(f"No se pudo traducir el archivo {name} después de {max_retries} intentos.")

    

root = tk.Tk()
root.title("SRTranslatorGUI")
root.geometry("800x600")
root.minsize(800, 600)
root.maxsize(800, 600)
# Set the initial theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

# Crear un menú desplegable
file_menu = tk.Menu(root, tearoff=0)

# Agregar opciones al menú desplegable
file_menu.add_command(label="Open Folder", command=open_folder)
file_menu.add_command(label="Open File", command=open_file)

# Agregar el menú desplegable a la barra de menú
menu_bar = tk.Menu(root)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Crear una lista de archivos abiertos
file_list = []
# Crear un frame horizontal para agrupar los widgets
frame = ttk.Frame(root)
# Crear los widgets
combo_box1 = ttk.Combobox(frame, values=["Any language (detect)", "Bulgarian","Chinese","Czech","Danish","Dutch","English",
 "Estonian","Finnish","French","German","Greek","Hungarian","Indonesian","Italian","Japanese","Latvian","Lithuanian","Polish",   
  "Portuguese","Romanian","Russian","Slovak","Slovenian","Spanish","Swedish","Turkish","Ukrainian"])
combo_box1.set("Any language (detect)")
combo_box2 = ttk.Combobox(frame, values=["Bulgarian","Chinese","Czech","Danish","Dutch","English (American)","English (British)",
 "Estonian","Finnish","French","German","Greek","Hungarian","Indonesian","Italian","Japanese","Latvian","Lithuanian","Polish",   
  "Portuguese","Portuguese (Brazilian)","Romanian","Russian","Slovak","Slovenian","Spanish","Swedish","Turkish","Ukrainian"])
combo_box1.set("Any language (detect)")
combo_box2.set("Spanish")
button = tk.Button(frame, text="Translate",command=translate_files)
# Colocar los widgets en la ventana
combo_box1.pack(side="left")
combo_box2.pack(side="left", padx=10)
button.pack(side="left", padx=10)
# Empaquetar el frame dentro de la ventana principal
frame.pack(pady=10)



def add_file_to_list(file_paths):
    # Agregar un nuevo archivo a la lista
    for file_path in file_paths:
        index = len(file_list) + 1
        name = file_path
        status = "Pending"
        progress = 0

        file_list.append((index, name, status, progress))

        # Agregar una nueva fila a la tabla
        treeview.insert('', 'end', values=(index, name, status, progress))

# Crear la tabla para mostrar los archivos abiertos
treeview = ttk.Treeview(root, columns=["Index", "Name", "Status", "Progress"], show="headings")
treeview.heading("Index", text="Index", anchor="center")
treeview.heading("Name", text="Name",anchor="center")
treeview.heading("Status", text="Status",anchor="center")
treeview.heading("Progress", text="Progress",anchor="center")
treeview.pack(side="left",fill="both", expand=True)

# Configurar el tamaño de las columnas
treeview.column("Index", width=50)
treeview.column("Name", width=200)
treeview.column("Status", width=100)
treeview.column("Progress", width=100)

# Crear una barra de desplazamiento vertical
scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbar.set)


# Agregar los archivos existentes a la tabla
for index, name, status, progress in file_list:
    treeview.insert('', 'end', values=(index, name, status, progress))

def update_file_status(index, status):
    file_tuple = file_list[index - 1]
    updated_tuple = (file_tuple[0], file_tuple[1], status, file_tuple[3])
    file_list[index - 1] = updated_tuple

    # Actualizar el estado del archivo en la tabla
    table_row = treeview.get_children()[index - 1]
    treeview.set(table_row, column=2, value=status)

def update_file_progress(index, progress):
    file_tuple = file_list[index - 1]
    updated_tuple = (file_tuple[0], file_tuple[1], file_tuple[2], progress)
    file_list[index - 1] = updated_tuple

    # Actualizar el estado del archivo en la tabla
    table_row = treeview.get_children()[index - 1]
    treeview.set(table_row, column=3, value=progress)
    
# Crea una función para limpiar el treeview y la file_list
def clear_data():
    # Borra todos los items del treeview
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Borra todos los elementos de la file_list
    file_list.clear()

languages_source={
    'Any language (detect)': 'auto', 
    'Bulgarian': 'bg', 
    'Chinese': 'zh', 
    'Czech': 'cs', 
    'Danish': 'da', 
    'Dutch': 'nl', 
    'English': 'en',
    'Estonian': 'et', 
    'Finnish': 'fi', 
    'French': 'fr', 
    'German': 'de', 
    'Greek': 'el', 
    'Hungarian': 'hu', 
    'Indonesian': 'id', 
    'Italian': 'it', 
    'Japanese': 'ja', 
    'Latvian': 'lv', 
    'Lithuanian': 'lt',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Slovak': 'sk', 
    'Slovenian': 'sl', 
    'Spanish': 'es', 
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Ukrainian': 'uk'
    }

languages_dest={
    'Bulgarian': 'bg', 
    'Chinese': 'zh', 
    'Czech': 'cs', 
    'Danish': 'da', 
    'Dutch': 'nl', 
    'English (American)': 'en-US',
    'English (British)': 'en-GB', 
    'Estonian': 'et', 
    'Finnish': 'fi', 
    'French': 'fr', 
    'German': 'de', 
    'Greek': 'el', 
    'Hungarian': 'hu', 
    'Indonesian': 'id', 
    'Italian': 'it', 
    'Japanese': 'ja', 
    'Latvian': 'lv', 
    'Lithuanian': 'lt',
    'Polish': 'pl',
    'Portuguese': 'pt-PT',
    'Portuguese (Brazilian)': 'pt-BR', 
    'Romanian': 'ro',
    'Russian': 'ru',
    'Slovak': 'sk', 
    'Slovenian': 'sl', 
    'Spanish': 'es', 
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Ukrainian': 'uk'
    }

root.mainloop()