# -*- coding: utf-8 -*-
'''
Created on 20 févr. 2024
@author: Zoubeir Marouf
'''
import os
import sys, io
import cv2
import subprocess
import json
from tkinter import *
from tkinter import simpledialog
from tkinter import Checkbutton, BooleanVar
from tkinter.ttk import Progressbar
from tkinter import ttk, messagebox, filedialog, StringVar, Menu, Frame, Canvas, Scrollbar, Listbox, BOTH, END, VERTICAL, RIGHT, Y, LEFT, NW
from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread
from webbrowser import open_new
from datetime import datetime
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from lcms import *
from benfeld import *
from codebrim import *
from rdg import *
from ufr import *
from deepCrack import *
from grandMare import *
from annotation import *
from newdb import *

buffer = io.StringIO()
sys.stdout = sys.stderr = buffer 

class CrackBase(Tk):

    # Fonction pour exécuter le script d'annotation
    def executer(self):
        chemin_annotation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "annotation.py")
        subprocess.run(["python", "annotation.py"])

        # Créer le contenu du notebook
        notebook_content = nbformat.v4.new_notebook()

        code_cell_source = """
        import os
        import cv2
        from tkinter import *
        from tkinter import ttk, messagebox
        from tkinter import simpledialog
        from tkinter import filedialog
        from PIL import Image, ImageTk
        from io import BytesIO
        from threading import Thread
        from webbrowser import open_new
        from datetime import datetime
        from backend import *
        from backend2 import *
        from backend3 import *
        from annotation import *
        os.chdir('{os.path.dirname(os.path.abspath(__file__))}')
        exec(open('annotation.py').read())
        """

        code_cell = nbformat.v4.new_code_cell(source=code_cell_source)
        notebook_content['cells'] = [code_cell]

        # Save the notebook content to a file or use it as needed
        with open('notebook_annotation.ipynb', 'w') as f:
            nbformat.write(notebook_content, f, version=nbformat.NO_CONVERT)

            #messagebox.showinfo("Script exécuté", "Le script d'annotation a été exécuté avec succès.")
    
    # Fonction pour exécuter SAM
    def executer2(self):
        chemin_annotator = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sam\\annotator.py")
        subprocess.run(["python", "sam\\annotator.py"])

        # Créer le contenu du notebook
        notebook_content = nbformat.v4.new_notebook()

        code_cell_source = """
        import os
        import cv2
        from tkinter import *
        from tkinter import ttk, messagebox
        from tkinter import simpledialog
        from tkinter import filedialog
        from PIL import Image, ImageTk
        from io import BytesIO
        from threading import Thread
        from webbrowser import open_new
        from datetime import datetime
        from backend import *
        from backend2 import *
        from backend3 import *
        from annotation import *
        os.chdir('{os.path.dirname(os.path.abspath(__file__))}')
        exec(open('annotation.py').read())
        """

        code_cell = nbformat.v4.new_code_cell(source=code_cell_source)
        notebook_content['cells'] = [code_cell]

        # Save the notebook content to a file or use it as needed
        with open('notebook_annotation.ipynb', 'w') as f:
            nbformat.write(notebook_content, f, version=nbformat.NO_CONVERT)

            #messagebox.showinfo("Script exécuté", "Le script SAM a été exécuté avec succès.")

    # Fonction pour exécuter Labelme
    def executer_executable(self):
        try:
            subprocess.run(["Labelme.exe"])
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Impossible de trouver l'exécutable.")     

    # Fonction pour exécuter npz_img
    def run_npz_img(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "npz-img.py")
        subprocess.run(["python", "npz-img.py"])

    # Fonction pour exécuter fusion_img
    def run_fusion_img(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fusion-img.py")
        subprocess.run(["python", "fusion-img.py"])

        messagebox.showinfo("Script exécuté", "La fusion des images a été exécutée avec succès.")

    # Fonctions pour exécuter les fichiers "coco-format"
    def execute_program2(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco-converter\\mask2coco.py")
        subprocess.run(["python", "mask2coco-converter\\mask2coco.py"])

    def execute_program3(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco-converter\\visualize_mask2points.py")
        subprocess.run(["python", "mask2coco-converter\\visualize_mask2points.py"])

    def execute_program4(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco-converter\\analysis.py")
        subprocess.run(["python", "mask2coco-converter\\analysis.py"])

    def execute_program5(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco-converter\\dir_masks.py")
        subprocess.run(["python", "mask2coco-converter\\dir_masks.py"])

    # Fonction pour afficher le fichier généré   
    def afficher_fichier_genere(self):
        try:
            with open("fichier_annoté.json", "r") as fp:
                content = json.load(fp)

            # Créer une nouvelle fenêtre pour afficher le contenu du fichier JSON
            window = Toplevel(self)
            window.title("Contenu du fichier généré")

            text_widget = Text(window, wrap="word", width=80, height=30)
            text_widget.insert(END, json.dumps(content, indent=4))

            text_widget.pack(expand=True, fill="both")

        except FileNotFoundError:
            messagebox.showinfo("Fichier non trouvé", "Le fichier généré n'a pas été trouvé.")
    
    def exporter_json(self):
        # Générer ou récupérer vos données au format Python dictionary
        data_to_export = {"key1": "value1", "key2": "value2"}

        # Demander à l'utilisateur où enregistrer le fichier JSON
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Fichiers JSON", "*.json")])

        # Vérifier si l'utilisateur a annulé la boîte de dialogue
        if file_path:
            # Exporter les données au format JSON dans le fichier spécifié
            with open(file_path, 'w') as json_file:
                json.dump(data_to_export, json_file)

            # Afficher un message de réussite (vous pouvez personnaliser ceci selon vos besoins)
            tk.messagebox.showinfo("Exportation réussie", "Le fichier JSON a été exporté avec succès.")

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Ajouter la barre de menu
        menu = Menu(self)
        self.config(menu=menu)

        # Ajouter le bouton du menu burger à la barre de menu
        menu.add_command(label="Menu", command=self.toggle_sidebar)

        file = Menu(menu, tearoff=0) 
        file.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=file)

        npz_img = Menu(menu, tearoff=0) 
        npz_img = tk.Menu(menu, tearoff=0)
        npz_img.add_command(label="Exécuter", command=self.run_npz_img)
        menu.add_cascade(label="npz-png", menu=npz_img)

        fusion_img = Menu(menu, tearoff=0) 
        fusion_img = tk.Menu(menu, tearoff=0)
        fusion_img.add_command(label="Exécuter", command=self.run_fusion_img)
        menu.add_cascade(label="Fusion-img", menu=fusion_img)

        view = Menu(self)
        view.add_command(label="Voir le dossier des BDD", command=self.explorer)
        view.add_separator()
        view.add_command(label="Voir les tables de la BDD", command=self.view_tables)
        view.add_separator()
        view.add_command(label="Voir toutes les données", command=self.view_all_data)
        view.add_separator()
        view.add_command(label="Voir les données LCMS", command=lambda: self.view_lcms_data)
        view.add_separator()
        view.add_command(label="Voir les données Fers apparents", command=lambda: self.view_other_table_data("fer_apparents"))
        view.add_separator()
        view.add_command(label="Voir les données Fissures", command=lambda: self.view_other_table_data("fissures"))
        view.add_separator()
        view.add_command(label="Voir les données Nouvelle BDD", command=lambda: self.view_other_table_data("nouvelle_bdd"))
        view.add_separator()
        view.add_command(label="Supprimer des données", command=lambda: self.delete_data("nom_de_l_image.jpg"))
        menu.add_cascade(label="View", menu=view)

        help_menu = Menu(self, tearoff=0)
        contact = Menu(self, tearoff=0)

        label = Menu(menu, tearoff=0) 
        exe_menu = tk.Menu(label, tearoff=0)
        exe_menu.add_command(label="Exécuter le script", command=self.executer)
        label.add_cascade(label="Annoter les images", menu=exe_menu)
        label.add_separator()
        label.add_command(label="Afficher le fichier JSON", command=self.afficher_fichier_genere)
        export_menu = tk.Menu(label, tearoff=0)
        export_menu.add_command(label="Exporter JSON", command=self.exporter_json)
        label.add_cascade(label="Exporter", menu=export_menu)
        menu.add_cascade(label="Label", menu=label)

        sam = Menu(menu, tearoff=0) 
        sam = tk.Menu(menu, tearoff=0)
        sam.add_command(label="Exécuter SAM", command=self.executer2)
        menu.add_cascade(label="SAM", menu=sam)

        labelme = Menu(menu, tearoff=0) 
        labelme = tk.Menu(menu, tearoff=0)
        labelme.add_command(label="Exécuter", command=self.executer_executable)
        menu.add_cascade(label="Labelme", menu=labelme)

        coco = Menu(menu, tearoff=0) 
        coco.add_command(label="Copie les masques", command=self.execute_program5)
        coco.add_separator()
        coco.add_command(label="Convertir en COCO", command=self.execute_program2)
        coco.add_separator()
        coco.add_command(label="Visualiser les masques", command=self.execute_program3)
        coco.add_separator()
        coco.add_command(label="Analyser", command=self.execute_program4)
        menu.add_cascade(label="COCO", menu=coco)
        #coco.add_separator()

        contact.add_command(label="Github", command=lambda: open_new("https://github.com/Zoubir78/"))
        contact.add_separator()
        contact.add_command(label="Questions", command=lambda: open_new("https://stackoverflow.com/questions"))
        help_menu.add_cascade(label="Contact", menu=contact)
        menu.add_cascade(label="Help", menu=help_menu)

        # Sidebar
        self.sidebar = Frame(self, width=100, bg="#484D7A")
        self.sidebar.pack(side=LEFT, fill=Y)

        # Body
        body = Frame(self, bg="black")
        body.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.body = body

        # Ajouter des bouttons à la barre latérale
        sidebutton0 = Button(self.sidebar, text="Accueil", bg="gray", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("Accueil"), font=("Arial", 9, "bold"))
        sidebutton0.grid(row=0, pady=3, padx=5)

        sidebutton1 = Button(self.sidebar, text="Type d\'image", bg="gray", relief=SUNKEN, width=15, height=7, command=self.toggle_side_button, font=("Arial", 9, "bold"))
        sidebutton1.grid(row=1, pady=2, padx=5)

        # Sous-boutons
        self.side_button_lcms = Button(self.sidebar, text="LCMS", bg="white", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("LCMS"), font=("FontAwesome", 9, "bold"))
        self.side_button_lcms.grid(row=1, column=1, pady=(0, 70), padx=6)
        self.side_button_lcms.grid_remove()  # Caché initialement

        self.side_button_2d = Button(self.sidebar, text="Images 2D", bg="white", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("2d"), font=("FontAwesome", 9, "bold"))
        self.side_button_2d.grid(row=1, column=1, pady=(4, 4), padx=6)
        self.side_button_2d.grid_remove()  # Caché initialement

        self.side_button_NB = Button(self.sidebar, text="\uf067", bg="white", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("nouvelle_BDD"), font=("FontAwesome", 9, "bold"))
        self.side_button_NB.grid(row=1, column=1, pady=(70, 0), padx=6)
        self.side_button_NB.grid_remove()  # Caché initialement

        sidebutton2 = Button(self.sidebar, text="Type de désordre", bg="gray", relief=SUNKEN, width=15, height=7, command=self.toggle_side_button2, font=("Arial", 9, "bold"))
        sidebutton2.grid(row=2, pady=2, padx=5)

        # Sous-boutons
        self.side_button_fa = Button(self.sidebar, text="Fer apparent", bg="white", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("fer apparent"), font=("FontAwesome", 9, "bold"))
        self.side_button_fa.grid(row=2, column=1, pady=(0, 70), padx=6)
        self.side_button_fa.grid_remove()  # Caché initialement

        self.side_button_fes = Button(self.sidebar, text="Fissures", bg="white", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("fissures"), font=("FontAwesome", 9, "bold"))
        self.side_button_fes.grid(row=2, column=1, pady=(4, 4), padx=6)
        self.side_button_fes.grid_remove()  # Caché initialement

        self.side_button_NB1 = Button(self.sidebar, text="\uf067", bg="white", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("nouvelle_BDD"), font=("FontAwesome", 9, "bold"))
        self.side_button_NB1.grid(row=2, column=1, pady=(70, 0), padx=6)
        self.side_button_NB1.grid_remove()  # Caché initialement

        sidebutton4 = Button(self.sidebar, text="Equipements", bg="gray", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("equipements"), font=("Arial", 9, "bold"))
        sidebutton4.grid(row=3, pady=2, padx=5)

        sidebutton3 = Button(self.sidebar, text="Sites", bg="gray", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("sites"), font=("Arial", 9, "bold"))
        sidebutton3.grid(row=4, pady=2, padx=5)

        sidebutton5 = Button(self.sidebar, text="A propos", bg="gray", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("a_propos"), font=("Arial", 9, "bold"))
        sidebutton5.grid(row=5, pady=2, padx=5)

        # Créer les différents Frames ; La classe Frames prend les arguments du parent, de la catégorie et du chemin d'accès au fichier de l'image.
        self.frames = {"Accueil": Home(body), "LCMS": Frames(body, "LCMS", "images\\LCMS.png"), 
                        "2d": Frames2(body, "Images 2D", "images\\image-2d.jpg"),
                        "fer apparent": Frames3(body, "Fer apparent", "images\\fer-apparent.png"),
                        "fissures": Frames4(body, "Fissures", "images\\fissures.jpg"), 
                        "sites": Frames7(body, "Sites", "images\\VT.png"),
                        "nouvelle_BDD": Frames5(body, "Nouvelle BDD", "images\\database.png"),
                        "equipements": Frames8(body, "Equipements", "images\\detect.png"),
                        "a_propos": Frames6(body, "A propos", "images\\VT.png"),
                        "view": View(body)}

        self.make_frame("Accueil")
        self.show_page("Accueil")  # Augmente la page d'accueil vers le haut.
        
        # Les threads sont utilisés pour charger simultanément les autres images en arrière-plan
        for x in ("LCMS", "2d", "fer apparent", "fissures", "equipements", "sites", "nouvelle_BDD", "a_propos", "view"):
            thread = Thread(target=self.make_frame, args=(x,)) #Remember the args argument takes a tuple, hence the comma.
            thread.start()

    def toggle_side_button(self):
        if self.side_button_lcms.winfo_ismapped():
            self.side_button_lcms.grid_remove()  # Masquer le sous-bouton LCMS s'il est affiché
            self.side_button_2d.grid_remove()  # Masquer le sous-bouton 2D s'il est affiché
            self.side_button_NB.grid_remove()
        else:
            self.side_button_lcms.grid()  # Afficher le sous-bouton LCMS s'il est masqué
            self.side_button_2d.grid()  # Afficher le sous-bouton 2D s'il est masqué
            self.side_button_NB.grid()

    def toggle_side_button2(self):
        if self.side_button_fa.winfo_ismapped():
            self.side_button_fa.grid_remove()  
            self.side_button_fes.grid_remove() 
            self.side_button_NB1.grid_remove()
        else:
            self.side_button_fa.grid()  
            self.side_button_fes.grid() 
            self.side_button_NB1.grid()

    def explorer(self):
        dossier_db = r'C:\Users\z.marouf-araibi\Desktop\crack-base-project\DB'
        os.name == 'nt'  # Windows
        subprocess.run(["explorer", dossier_db], shell=True)
        
    def toggle_sidebar(self):
        if self.sidebar.winfo_viewable():
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side=LEFT, fill=Y)

    def make_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.grid(row=0, sticky=NSEW)

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def view_menu(self):
        global listbox
        listbox.delete(0, END)
        self.show_page("view")
        #listbox.insert(END, f"           ")
        number = 1
        for i in view(): # Cette fonction d'affichage provient du fichier backend.py.
            listbox.insert(END, f"{number})  {{{i[2]}}}")
            number += 1

    def view_all_menu(self):
        global listbox
        listbox.delete(0, END)
        self.show_page("view")
        number = 1
        for i in view_all():
            listbox.insert(END, f"{number})  {i[1]} {{{i[2]}}}")
            number += 1

    def view_all_data(self):
        view = View(self)
        view.pack(fill=BOTH, expand=True)
        view.view_all_data()

    def view_other_table_data(self, table_name):
        view = View(self)
        view.pack(fill=BOTH, expand=True)
        view.view_other_table_data(table_name)

    def view_all_data(self):
        # Afficher toutes les données de la base de données
        all_data = view_all(connect())
        for data in all_data:
            print(data)

    def view_tables(self):
        # Afficher les tables de la base de données
        tables = get_tables()
        for table in tables:
            print(table[0])

    def view_lcms_data(self):
        # Afficher les données de la table 'images' (LCMS)
        lcms_data = view("images")
        for data in lcms_data:
            print(data)

    def delete_data(self, image_name):
        # Supprimer les données en fonction du nom de l'image
        delete(image_name)
        print(f"Data with image name '{image_name}' deleted successfully")

            

class Home(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        image = Image.open("images\\cracks-seg-1.png")
        self.main = ImageTk.PhotoImage(image)

        self.canvas = Canvas(self, width=1050)
        self.canvas.pack(fill=BOTH, expand=TRUE)

        # Ajout de l'image de fond et des textes au Canvas.
        self.canvas_image = self.canvas.create_image(60, 60, image=self.main, anchor=NW)

        self.canvas_text1 = self.canvas.create_text(520, 30, text="""Bienvenue sur Crack Base - ENDSUM""", font=("Castellar", 20, "italic", "bold"), fill="#2C3054")


class Frames(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(10, 10, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(790, 40, text=f"{category}", font=("Castellar", 30, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(790, 75, text=f"(Images, profondeur, VT)", font=("Castellar", 13), fill="#2C3054")
        self.canvas_text3 = self.canvas.create_text(800, 180,
                                                    text=f"Le capteur LCMS analyse la projection d'une ligne laser \nsur la paroi du tunnel,"
                                                    "fournissant à chaque acquisition \nun profil de profondeur et un profil"
                                                    "d'intensité.\nCelles-ci sont progressivement agrégées au fur et à mesure \nque le"
                                                    "véhicule avance pour former des images \net des cartes de profondeur, avec une"
                                                    "résolution spatiale \nde 1 × 2 mm et une résolution de profondeur submillimétrique.",
                                                    font=("times new roman", 12, "italic", "normal"), fill="black")

        self.canvas_text4 = self.canvas.create_text(780, 350,
                                                    text=f"Nomenclature de nommage '{category.lower()}' :\n - Un dossier par séquence\n "
                                                    "- Nom de dossier : “TE_D_18062_H1870_A0” → \n TE : Tube Est (TE) ou Tube Ouest (TO) \n "
                                                    "D (ou C) : sens de prise (sens décroissant ou croissant) \n 18062 : numéro séquence (incrémental) \n "
                                                    "H (Hauteur à partir du sol du gerbeur en mm) \n A (angle en degrés des capteurs , 0 = à l’horizontal)",
                                                    font=("times new roman", 12, "normal"), fill="black")
        
        self.entry_var = StringVar()
        self.check_var = BooleanVar()  # Variable to store the checkbox state
        self.check_var.set(True)  # Default to intensity

        self.check_var2 = BooleanVar()  # Variable to store the checkbox state
        self.check_var2.set(True)  # Default to intensity

        # Créer un widget Progressbar pour la barre de progression
        self.progress1 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress2 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        button1 = ttk.Button(self, text=f"Ajouter des données (intensité)", width=50, command=lambda: upload_lcms(self, category))
        button2 = ttk.Button(self, text=f"Ajouter des données (profondeur)", width=50, command=lambda: upload_depths(self, category))

        self.canvas_button1 = self.canvas.create_window(750, 510, window=button1)
        self.canvas_progress1 = self.canvas.create_window(750, 540, window=self.progress1)
        self.canvas_button2 = self.canvas.create_window(750, 570, window=button2)
        self.canvas_progress2 = self.canvas.create_window(750, 600, window=self.progress2)

    def add(self, table):
        site, tube, sens = select_site_details(self)  # Demander à l'utilisateur de saisir les détails
        if site and tube and sens:
            entry = self.entry_var.get()  
            display_intensity = self.check_var.get()
            if len(entry.strip()) > 2:
                messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
                insert(entry.title().strip(), self.category, site, tube, sens, display_intensity, table=table)
            elif len(entry.strip()) < 1:
                pass
            else:
                messagebox.showinfo("Doit contenir plus de 2 caractères", "Les caractères saisis sont trop courts.")
            self.entry_var.set("")

class Frames2(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=tk.TRUE)
        
        self.canvas_text1 = self.canvas.create_text(500, 40, text=f"{category}", font=("Castellar", 30, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(500, 75, text=f"(Images visibles, VT, pas de profondeur)", font=("Castellar", 13), fill="#2C3054")
        self.canvas_text3 = self.canvas.create_text(340, 120, text=f"- Tunnel Rive-de-Gier (RDG)", font=("times new roman", 12, "normal", "bold"), fill="black")
        self.canvas_text4 = self.canvas.create_text(340, 220, text=f"→ Acquisition par un véhicule, sous forme de séquences, par bande (par passage) \n"
                                                                    "2 images par mètre, tunnel 80 m environ, total entre 160 et 180 images \n"
                                                                    "Nomenclature :\n 1 dossier  par passage. 2 types de caméras : \nles caméras de relevés sont indiqués dans le nom du dossier avec le mot “Voute”. \n"
                                                                    "Les autres dossiers sont des images pour la localisation odométrique, il n’y a pas d’indication “Voute” \n"
                                                                    "Nom : VT_RDG_Voute_0deg_sens_moins. \n"
                                                                    "1 sous-dossier numéroté contient l’image originale et l’image binaire (VT)",
                                                               font=("times new roman", 12, "normal"), fill="black")
        
        self.progress1 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        button03 = ttk.Button(self, text=f"Ajouter des données Images à la base 'RDG'", width=40, command=lambda: upload_images_rdg(self, category))
        button03.pack(pady=10)
        button003 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=40, command=lambda: upload_masques_rdg(self, category))
        button003.pack(pady=10)

        self.canvas_button = self.canvas.create_window(800, 160, window=button03)
        self.canvas_button = self.canvas.create_window(800, 200, window=button003)
        self.canvas_progress1 = self.canvas.create_window(800, 240, window=self.progress1)

        self.canvas_text3 = self.canvas.create_text(340, 320, text=f"- Tunnel piéton (Benfeld)", font=("times new roman", 12, "normal", "bold"), fill="black")
        self.canvas_text5 = self.canvas.create_text(260, 390, text=f"→ Acquisition “à la volée” par un smartphone \n"
                                                                    "4 sous dossiers CC-S, CC-C, CS-C, CS-S \n"
                                                                    "CC = coté centre ou ; CS = côté station \n"
                                                                    "- C ou -S = Cloudy , ou Sunny \n"
                                                                    "1 sous-dossier numéroté contient l’image originale et l’image binaire (VT)",
                                                               font=("times new roman", 12, "normal"), fill="black")
        
        self.progress01 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        button01 = ttk.Button(self, text=f"Ajouter des données Images à la base 'BENFELD'", width=40, command=lambda: upload_images_benfeld(self, category))
        button01.pack(pady=10)

        button001 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=40, command=lambda: upload_masques_benfeld(self, category))
        button001.pack(pady=10)

        self.canvas_button = self.canvas.create_window(800, 350, window=button01)
        self.canvas_button = self.canvas.create_window(800, 390, window=button001)
        self.canvas_progress01 = self.canvas.create_window(800, 430, window=self.progress01)

        self.canvas_text3 = self.canvas.create_text(340, 470, text=f"- Base CODEBRIM", font=("times new roman", 12, "normal", "bold"), fill="black")
        self.canvas_text6 = self.canvas.create_text(260, 520, text=f"→ Images à la volée, tailles différentes \n"
                                                                    "Récupéré d’un papier avec base d’images désordres sur OA \n"
                                                                    "Ajout de la VT en segmentation \n"
                                                                    "1 sous-dossier numéroté contient l’image originale et l’image binaire (VT)",
                                                               font=("times new roman", 12, "normal"), fill="black")
        
        self.progress02 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        button02 = ttk.Button(self, text=f"Ajouter des données Images à la base 'CODEBRIM'", width=40, command=lambda: upload_images_codebrim(self, category))
        button02.pack(pady=10)

        button002 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=40, command=lambda: upload_masques_codebrim(self, category))
        button002.pack(pady=10)

        self.canvas_button = self.canvas.create_window(800, 480, window=button02)
        self.canvas_button = self.canvas.create_window(800, 520, window=button002)
        self.canvas_progress02 = self.canvas.create_window(800, 550, window=self.progress02)

        self.canvas_text3 = self.canvas.create_text(340, 580, text=f"- Base UFR", font=("times new roman", 12, "normal", "bold"), fill="black")
        self.canvas_text7 = self.canvas.create_text(280, 620, text=f"→ Images à la volée, 2 capteurs (Apple ou Samsung) \n"
                                                                    "2 types de VT (à l’obejt , comme autres bases, et sous forme de bande ou mask)",
                                                               font=("times new roman", 12, "normal"), fill="black")
        
        self.progress03 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        button04 = ttk.Button(self, text=f"Ajouter des données Images à la base 'UFR'", width=40, command=lambda: upload_images_ufr(self, category))
        button04.pack(pady=10)

        button004 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=40, command=lambda: upload_masques_ufr(self, category))
        button004.pack(pady=10)

        self.canvas_button = self.canvas.create_window(800, 600, window=button04)
        self.canvas_button = self.canvas.create_window(800, 640, window=button004)
        self.canvas_progress03 = self.canvas.create_window(800, 670, window=self.progress03)
        
        self.entry_var = StringVar()
        self.check_var = BooleanVar()
        self.check_var.set(True)

    def add(self, event=None):
        entry = self.entry_var.get()
        display_intensity = self.check_var.get()

        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category, display_intensity)
        elif len(entry.strip()) < 1:
            pass
        else:
            messagebox.showinfo("Doit contenir plus de 2 caractères", "Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class Frames3(Frame):
    selected_tables = []
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        #self.selected_tables = []  # Default table
        self.canvas_image = self.canvas.create_image(280, 20, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(700, 70, text=f"{category}", font=("Castellar", 30, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(160, 500,
                                                    text=f"Pour afficher vos données enregistrées \n'{category.lower()}', cliquez sur le menu View \n "
                                                         f"de la barre de menu et sélectionnez \n'View {category}'.", font=("times new roman", 12, "normal"), fill="black")

        self.entry_var = StringVar()
        #entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        button01 = ttk.Button(self, text=f"Ajouter des données à la base 'BENFELD'", width=40, command=lambda: self.choose_table_and_upload('BENFELD'))
        button01.pack(pady=10)
        self.table_choice_button = ttk.Button(self, text="Choisir une table", width=40, command=self.open_table_selection)
        self.table_choice_button.pack(pady=10)

        button02 = ttk.Button(self, text=f"Ajouter des données à la base 'CODEBRIM'", width=40, command=lambda: self.choose_table_and_upload2('CODEBRIM'))
        button02.pack(pady=10)
        self.table_choice_button2 = ttk.Button(self, text="Choisir une table", width=40, command=self.open_table_selection)
        self.table_choice_button2.pack(pady=10)

        button03 = ttk.Button(self, text=f"Ajouter des données à la base 'RDG'", width=40, command=lambda: self.choose_table_and_upload3('RDG'))
        button03.pack(pady=10)
        self.table_choice_button3 = ttk.Button(self, text="Choisir une table", width=40, command=self.open_table_selection)
        self.table_choice_button3.pack(pady=10)

        button04 = ttk.Button(self, text=f"Ajouter des données à la base 'UFR'", width=40, command=lambda: self.choose_table_and_upload4('UFR'))
        button04.pack(pady=10)
        self.table_choice_button4 = ttk.Button(self, text="Choisir une table", width=40, command=self.open_table_selection)
        self.table_choice_button4.pack(pady=10)

        #entry.bind("<Return>", self.add)
        button01.bind("<Return>", self.add)
        self.table_choice_button.bind("<Return>", self.add)
        button02.bind("<Return>", self.add)
        self.table_choice_button2.bind("<Return>", self.add)
        button03.bind("<Return>", self.add)
        self.table_choice_button3.bind("<Return>", self.add)
        button04.bind("<Return>", self.add)
        self.table_choice_button4.bind("<Return>", self.add)
        #self.canvas_entry = self.canvas.create_window(600, 700, window=entry)
        self.canvas_button = self.canvas.create_window(140, 180, window=button01)
        self.canvas_button = self.canvas.create_window(140, 200, window=self.table_choice_button)
        self.canvas_button = self.canvas.create_window(140, 240, window=button02)
        self.canvas_button = self.canvas.create_window(140, 260, window=self.table_choice_button2)
        self.canvas_button = self.canvas.create_window(140, 300, window=button03)
        self.canvas_button = self.canvas.create_window(140, 320, window=self.table_choice_button3)
        self.canvas_button = self.canvas.create_window(140, 360, window=button04)
        self.canvas_button = self.canvas.create_window(140, 380, window=self.table_choice_button4)

    def choose_table_and_upload(self, category):
        self.open_table_selection()
        upload_images_benfeld(category, self.selected_tables)

    def choose_table_and_upload2(self, category):
        self.open_table_selection()
        upload_images_codebrim(category, self.selected_tables)

    def choose_table_and_upload3(self, category):
        self.open_table_selection()
        upload_images_rdg(category, self.selected_tables)

    def choose_table_and_upload4(self, category):
        self.open_table_selection()
        upload_images_ufr(category, self.selected_tables)
    
    def open_table_selection(self):
        table_selection_window = TableSelectionWindow(self)
        self.wait_window(table_selection_window)
        selected_tables = table_selection_window.selected_tables
        if selected_tables:
            self.selected_tables = selected_tables
            print(f"Tables sélectionnées : {selected_tables}")

    def add(self, event):
        entry = self.entry_var.get()  # Obtient le contenu de la zone d'entrée saisie par l'utilisateur.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class TableSelectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Choisir une ou plusieurs tables")

        self.selected_tables = []

        self.label = tk.Label(self, text="Sélectionnez une table:")
        self.label.pack(pady=10)

        self.table_var = tk.StringVar()

        table_options = get_tables()  # You need to implement the 'get_tables' function

        if table_options:
            self.table_var.set(table_options[0])  # Set default value

            self.table_menu = ttk.Combobox(self, textvariable=self.table_var, values=table_options)
            self.table_menu.pack(pady=10)

            self.button_add = ttk.Button(self, text="Ajouter", command=self.add_table)
            self.button_add.pack(pady=10)

            self.button_ok = ttk.Button(self, text="OK", command=self.on_ok)
            self.button_ok.pack(pady=10)

        else:
            tk.Label(self, text="Aucune table trouvée dans la base de données.").pack(pady=10)

    def add_table(self):
        selected_table = self.table_var.get()
        if selected_table not in self.selected_tables:
            self.selected_tables.append(selected_table)
            tk.Label(self, text=f"Table ajoutée : {selected_table}").pack()

    def on_ok(self):
        self.destroy()

class Frames4(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(50, 50, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(800, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(800, 180,
                                                    text=f"Pour afficher vos données enregistrées '{category.lower()}',\ncliquez sur le menu View "
                                                         f"de la barre de menu \net sélectionnez 'View {category}'.", font=("times new roman", 12, "normal"), fill="black")
      
        self.entry_var = StringVar()
        #entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        button3 = ttk.Button(self, text=f"Ajouter des données à la base 'DeepCrack'", width=40, command=lambda: upload_images_deepCrack(category, 'tables'))
        button4 = ttk.Button(self, text=f"Ajouter des données à la base 'GrandMare'", width=40, command=lambda: upload_images_grandMare(category, 'tables'))
        #entry.bind("<Return>", self.add)
        button3.bind("<Return>", self.add)
        button4.bind("<Return>", self.add)
        #self.canvas_entry = self.canvas.create_window(880, 500, window=entry)
        self.canvas_button = self.canvas.create_window(800, 300, window=button3)
        self.canvas_button = self.canvas.create_window(800, 340, window=button4)
    
    def add(self, event):
        entry = self.entry_var.get()  # Obtient le contenu de la zone d'entrée saisie par l'utilisateur.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class Frames5(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(10, 50, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(900, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(900, 180,
                                                    text=f"Pour créer une nouvelle base de données,\ncliquez sur le boutton "
                                                         f"'{category.lower()}' ci-dessous.\nVous-pouvez aussi configurer la nouvelle table \nen cliquant sur 'Nouvelle Table'", font=("times new roman", 12, "normal"), fill="black")
      
        self.entry_var = StringVar()
        #entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        button5 = ttk.Button(self, text=f"Nouvelle BDD", width=40, command=create_new_database)
        button6 = ttk.Button(self, text=f"Nouvelle Table", width=40, command=create_table_in_database)
        button7 = ttk.Button(self, text=f"Ajouter des Données", width=40, command=add_data_to_database)

        #entry.bind("<Return>", self.add)
        button5.bind("<Return>", self.add)
        button6.bind("<Return>", self.add)
        button7.bind("<Return>", self.add)

        #self.canvas_entry = self.canvas.create_window(880, 500, window=entry)
        self.canvas_button = self.canvas.create_window(900, 300, window=button5)
        self.canvas_button = self.canvas.create_window(900, 340, window=button6)
        self.canvas_button = self.canvas.create_window(900, 380, window=button7)
    
    def add(self, event):
        entry = self.entry_var.get()  # Obtient le contenu de la zone d'entrée saisie par l'utilisateur.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class Frames6(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(10, 50, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(900, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(920, 230,
                                                    text=f"Bienvenue sur Crack Base! \nVotre solution complète de gestion de bases de données. \nConçue pour répondre aux besoins des \npassionnés de données, Crack Base offre une expérience \nintuitive et puissante pour gérer efficacement \ntoutes vos données.", font=("times new roman", 13, "italic"), fill="black")

        self.canvas_text3 = self.canvas.create_text(380, 480,
                                                    text=f"Avec Crack Base, vous pouvez créer, modifier et interroger des bases de données avec facilité. \nNotre interface conviviale vous permet de naviguer sans effort à travers vos ensembles de données, \nde créer des rapports personnalisés et d'analyser vos informations pour des insights précieux.", font=("times new roman", 13, "italic"), fill="black")

        self.canvas_text4 = self.canvas.create_text(400, 580,
                                                    text=f"Que vous soyez un développeur cherchant à gérer des données volumineuses, un analyste de données \nexplorant des tendances complexes ou un étudiant apprenant les bases de la gestion de bases de données, \nCrack Base est l'outil idéal pour vos besoins.", font=("times new roman", 13, "italic"), fill="black")
      
        self.entry_var = StringVar()
    
    def add(self, event):
        entry = self.entry_var.get()  # Obtient le contenu de la zone d'entrée saisie par l'utilisateur.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class Frames7(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(180, 30, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(380, 420, text=f"{category}", font=("Castellar", 20, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(400, 520,
                                                    text=f"Avec notre application, vous avez la liberté d'ajouter autant de sites que vous le souhaitez. \nEn quelques clics, vous pouvez créer un nouveau site en utilisant le bouton <Nouveau site>. \nDe là, vous avez le choix : \nvous pouvez intégrer ce site à une base de données existante pour une gestion centralisée et organisée, \nou bien créer une toute nouvelle base de données dédiée à ce site spécifique. \nCette flexibilité vous permet de personnaliser votre expérience selon vos besoins \net de structurer vos données de la manière qui vous convient le mieux.", font=("times new roman", 13, "italic"), fill="black")
      
        self.entry_var = StringVar()
        #entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        button5 = ttk.Button(self, text=f"Nouveau site", width=40, command=add_new_site)
        button6 = ttk.Button(self, text=f"BDD existante", width=40, command=add_site_to_existing_database)
        button7 = ttk.Button(self, text=f"Nouvelle BDD", width=40, command=create_new_database)
        button8 = ttk.Button(self, text=f"Nouvelle Table", width=40, command=create_table_in_database)
        button9 = ttk.Button(self, text=f"Ajouter des Données", width=40, command=add_data_to_database)

        self.canvas_button = self.canvas.create_window(920, 440, window=button5)
        self.canvas_button = self.canvas.create_window(920, 480, window=button6)
        self.canvas_button = self.canvas.create_window(920, 520, window=button7)
        self.canvas_button = self.canvas.create_window(920, 560, window=button8)
        self.canvas_button = self.canvas.create_window(920, 600, window=button9)
    
    def add(self, event):
        entry = self.entry_var.get()  # Obtient le contenu de la zone d'entrée saisie par l'utilisateur.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class Frames8(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(80, 10, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(380, 500, text=f"{category}", font=("Castellar", 20, "italic"), fill="#2C3054")
        self.canvas_text2 = self.canvas.create_text(400, 600,
                                                    text=f"La première étape consiste à modifier le fichier de configuration du modèle de détection. \nCe fichier contient tous les paramètres nécessaires à l'entraînement du modèle, \ntels que la structure du réseau neuronal, les hyperparamètres de l'entraînement, \nles chemins des jeux de données, et les prétraitements des images. \nPour notre projet, nous avons adapté ce fichier pour inclure des informations spécifiques \nsur les types d'équipements à détecter et les annotations correspondantes. \nCela permet au modèle d'apprendre à distinguer entre différents équipements \navec une grande précision.", font=("times new roman", 13, "italic"), fill="black")
      
        self.entry_var = StringVar()
        #entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        button5 = ttk.Button(self, text=f"Modifier le fichier Config", width=40, command=self.execute_program)
        button6 = ttk.Button(self, text=f"Afficher le fichier Config", width=40, command=self.open_config_file)
        button7 = ttk.Button(self, text=f"Help Config", width=40, command=self.lire_fichier)
        button8 = ttk.Button(self, text=f"Exécuter COCO Viewer", width=40, command=self.run_cocoviewer)
        button9 = ttk.Button(self, text=f"Entraîner le modèle", width=40, command=self.executer3)
        button10 = ttk.Button(self, text=f"Tester le modèle", width=40, command=self.executer2)
      
        self.canvas_button = self.canvas.create_window(920, 500, window=button5)
        self.canvas_button = self.canvas.create_window(920, 530, window=button6)
        self.canvas_button = self.canvas.create_window(920, 560, window=button7)
        self.canvas_button = self.canvas.create_window(920, 590, window=button8)
        self.canvas_button = self.canvas.create_window(920, 620, window=button9)
        self.canvas_button = self.canvas.create_window(920, 650, window=button10)

        # Fonction pour exécutez le fichier "Configs"
    def execute_program(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "option-config.py")
        subprocess.run(["python", "option-config.py"])
        #messagebox.showinfo("Script exécuté!", "Le script a été exécuté avec succès.")
    
    def open_config_file(self):
    # Créer une fenêtre Tkinter
        root = tk.Tk()
        root.title("Fichier de Configuration")
        root.geometry("1000x800")

        # Ouvrir une boîte de dialogue pour sélectionner le fichier de configuration
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers de configuration", "*.py"), ("Tous les fichiers", "*.*")])
        if file_path:
            # Ouvrir et lire le contenu du fichier de configuration
            with open(file_path, 'r') as f:
                config_content = f.read()
            
            # Créer une zone de texte pour afficher le contenu du fichier
            config_text = tk.Text(root, wrap="word")
            config_text.pack(expand=True, fill="both")
            
            # Afficher le contenu du fichier de configuration dans la zone de texte
            config_text.insert(tk.END, config_content)

        # Lancer la boucle principale de l'interface graphique
        root.mainloop()

    def lire_fichier(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                contenu = file.read()
            return contenu
        except FileNotFoundError:
            return "Le fichier n'existe pas."
        except Exception as e:
            return f"Une erreur s'est produite : {e}"

        # Utilisation
        filepath = 'C:/Users/z.marouf-araibi/Desktop/crack-base-project/mmdetection/configs/my_custom/doc-my_custom_config.txt'
        contenu = lire_fichier(filepath)
        print(contenu)

    def run_cocoviewer(self):
        # Demander à l'utilisateur de sélectionner le répertoire des images
        images_dir = filedialog.askdirectory(title="Sélectionner le répertoire des images")
        if not images_dir:  # L'utilisateur a annulé la sélection
            return

        # Demander à l'utilisateur de sélectionner le fichier d'annotations
        annotations_file = filedialog.askopenfilename(title="Sélectionner le fichier d'annotations", filetypes=[("Fichiers JSON", "*.json")])
        if not annotations_file:  # L'utilisateur a annulé la sélection
            return
        
        chemin_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coco-viewer", "cocoviewer.py")
        subprocess.run(["python", chemin_script, "-i", images_dir, "-a", annotations_file]) 

    # Fonction pour exécuter tools/train
    def executer3(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mmdetection\\tools\\train_final.py")
        subprocess.run(["python", "mmdetection\\tools\\train_final.py"])

    # Fonction pour exécuter tools/test
    def executer2(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mmdetection\\tools\\test.py")
        subprocess.run(["python", "mmdetection\\tools\\test.py"])
    
    def add(self, event):
        entry = self.entry_var.get()  # Obtient le contenu de la zone d'entrée saisie par l'utilisateur.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

class View(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=True)

        # Ajout d'une fenêtre défilante pour la liste
        scrollbar = Scrollbar(self.canvas, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.canvas, width=100, height=20, font=("comic sans ms", 13, "normal"), yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Ajout de l'entrée et du bouton de recherche
        self.entryvar = StringVar()
        entry = ttk.Entry(self, textvariable=self.entryvar, width=100, font=("Helvetica", 12, "normal"))
        entry.bind("<Return>", self.search_box)
        search_button = ttk.Button(self, text="Search", command=lambda: self.search_box(None))
        search_button.bind("<Return>", self.search_box)

        self.canvas_entry = self.canvas.create_window(520, 120, window=entry)
        self.canvas_button = self.canvas.create_window(1030, 120, window=search_button)

        # Ajout du bouton de suppression
        del_button = ttk.Button(self, text="Delete", width=20, command=self.delete_item)
        self.del_button = self.canvas.create_window(1010, 680, window=del_button)

    def search_box(self, event):
        if len(self.entryvar.get().strip()) > 0:
            number = 1
            search_results = self.search(self.entryvar.get().strip().title())
            if len(search_results) > 0:
                self.listbox.delete(0, END)  # Effacer la liste actuelle
                for x in search_results:
                    self.listbox.insert(END, f"{number})  {x[1]}   {{{x[2]}}}")
                    number += 1
                self.entryvar.set("")  # Effacer l'entrée de recherche
            else:
                messagebox.showinfo("Aucun résultat trouvé", "Désolé, vous n'avez pas trouvé ce que vous cherchiez.")

    def delete_item(self):
        try:
            index = self.listbox.curselection()[0]  # Obtient l'index de la ligne active dans la listbox
            selected_row = self.listbox.get(index)  # Récupère le contenu de la ligne active
            name = selected_row.split(" {")[0]  # Récupère le nom avant le premier "{"
            ask = messagebox.askyesno("Supprimer?", f"Etes-vous sûr que vous voulez supprimer {name}?")
            if ask:
                # Supprimer l'élément de la base de données ou de toute autre source
                self.listbox.delete(index)

        except IndexError:
            pass
        except ValueError:
            pass

    def display_data(self, data):
        self.listbox.delete(0, END)  # Effacer la liste actuelle
        for index, row in enumerate(data):
            self.listbox.insert(END, f"{index + 1}) {row[1]} - {row[2]} - {row[3]} - {row[4]}")

    def view_all_data(self):
        try:
            connection = sqlite3.connect("DB\\lcms_database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM images")
            data = cursor.fetchall()
            connection.close()
            self.display_data(data)
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données : {e}")

    def view_other_table_data(self, table_name):
        try:
            connection = sqlite3.connect("DB\\lcms_database.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            connection.close()
            self.display_data(data)
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données : {e}")

    def search(self, name):
        connection = sqlite3.connect("DB\\lcms_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM images WHERE nom_image LIKE ?", (f"%{name}%",))
        output = cursor.fetchall()
        connection.close()
        return output

    def delete_data(self, name):
        connection = sqlite3.connect("DB\\lcms_database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM images WHERE nom_image = ?", (name,))
        connection.commit()
        connection.close()

    # Ajouter un footer
        footer = tk.Label(self, text="© Crack Base 2024 - ENDSUM", relief=tk.SUNKEN, anchor=tk.W, font=("Castellar", 12, "italic"), bg="black", fg="white")
        footer.grid(row=6, column=0, sticky="ew")


app = CrackBase()
app.title("Crack Base 2.0 - ENDSUM")
app.iconbitmap("Images\\app.png")
app.maxsize(1300,800)
app.minsize(1300,800)
app.mainloop()