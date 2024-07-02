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
import logging
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
import shutil
from lcms import *
from benfeld import *
from codebrim import *
from rdg import *
from ufr import *
from deepCrack import *
from grandMare import *
from annotation import *
from newdb import *
from ttkthemes import ThemedTk
import webbrowser
import math
#import nbformat
#from nbconvert.preprocessors import ExecutePreprocessor

#from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QLineEdit, QPushButton, QLabel, QComboBox, QHBoxLayout, QFileDialog, QMessageBox
#from PyQt5.QtOpenGL import QGLWidget
#from OpenGL.GL import *
#from OpenGL.GLUT import *

buffer = io.StringIO()
sys.stdout = sys.stderr = buffer 

class CrackBase(Tk):

    def restart_application(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Fonction pour exécuter le script d'annotation
    def executer(self):
        chemin_annotation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "annotation.py")
        subprocess.run(["python", "annotation.py"])    
    
    # Fonction pour exécuter SAM
    def executer2(self):
        chemin_annotator = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sam\\annotator.py")
        subprocess.run(["python", "sam\\annotator.py"])     

    # Fonction pour exécuter npz_img
    def run_npz_img(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "npz-img.py")
        subprocess.run(["python", "npz-img.py"])

    # Fonction pour exécuter fusion_img
    def run_fusion_img(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fusion.py")
        subprocess.run(["python", "fusion.py"])
    
    # Fonction pour exécuter mat2img
    def run_mat2img(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mat2img\\mat2img.py")
        subprocess.run(["python", "mat2img\\mat2img.py"])

    # Fonctions pour exécuter les fichiers "coco-format"
    def execute_program2(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco\\mask2coco.py")
        subprocess.run(["python", "mask2coco\\mask2coco.py"])

    #def execute_program3(self):
    #    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco\\visualize_mask2points.py")
    #    subprocess.run(["python", "mask2coco\\visualize_mask2points.py"])

    #def execute_program4(self):
    #    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco\\analysis.py")
    #    subprocess.run(["python", "mask2coco\\analysis.py"])

    def execute_program5(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask2coco\\dir_masks.py")
        subprocess.run(["python", "mask2coco\\dir_masks.py"])

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

        # Style sombre pour ttk
        style = ttk.Style(self)
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        # Ajouter la barre de menu
        menu = Menu(self)
        self.config(menu=menu)

        # Ajouter le bouton du menu burger à la barre de menu
        menu.add_command(label="Menu", command=self.toggle_sidebar)

        file = Menu(menu, tearoff=0) 
        # Ajouter un bouton Actualiser à la barre de menu
        file.add_command(label="Redémarrer", command=self.restart_application)
        file.add_separator()
        file.add_command(label="Fermer", command=self.destroy)
        menu.add_cascade(label="File", menu=file)

        convert = Menu(menu, tearoff=0) 
        convert = tk.Menu(menu, tearoff=0)
        convert.add_command(label="Mask2COCO", command=self.execute_program2)
        convert.add_separator()
        convert.add_command(label="Copie les masques", command=self.execute_program5)
        convert.add_separator()
        convert.add_command(label="Npz2png", command=self.run_npz_img)
        menu.add_cascade(label="Converter", menu=convert)

        fusion_img = Menu(menu, tearoff=0) 
        fusion_img = tk.Menu(menu, tearoff=0)
        fusion_img.add_command(label="fusion capteurs", command=self.run_fusion_img)
        fusion_img.add_separator()
        fusion_img.add_command(label="mat2img", command=self.run_mat2img)
        menu.add_cascade(label="Fusion", menu=fusion_img)

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

        contact.add_command(label="Github", command=lambda: open_new("https://github.com/Zoubir78/Crack-Base/tree/master"))
        contact.add_separator()
        contact.add_command(label="Questions", command=lambda: open_new("https://stackoverflow.com/questions"))
        help_menu.add_cascade(label="Contact", menu=contact)
        menu.add_cascade(label="Help", menu=help_menu)

        a_propos = Menu(menu, tearoff=0)
        menu.add_cascade(label="A propos", command=lambda: self.show_page("a_propos"))

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
        sidebutton0 = Button(self.sidebar, text="Accueil", bg="#525659", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("Accueil"), font=("Arial", 9, "bold"))
        sidebutton0.grid(row=0, pady=3, padx=5)

        sidebutton1 = Button(self.sidebar, text="Images", bg="#525659", relief=SUNKEN, width=15, height=7, command=self.toggle_side_button, font=("Arial", 9, "bold"))
        sidebutton1.grid(row=1, pady=2, padx=5)

        # Sous-boutons
        self.side_button_lcms = Button(self.sidebar, text="LCMS", bg="black", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("LCMS"), font=("FontAwesome", 9, "bold"))
        self.side_button_lcms.grid(row=1, column=1, pady=(0, 70), padx=6)
        self.side_button_lcms.grid_remove()  # Caché initialement

        self.side_button_2d = Button(self.sidebar, text="Images 2D", bg="black", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("2d"), font=("FontAwesome", 9, "bold"))
        self.side_button_2d.grid(row=1, column=1, pady=(4, 4), padx=6)
        self.side_button_2d.grid_remove()  # Caché initialement

        self.side_button_NB = Button(self.sidebar, text="+", bg="black", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("nouvelle_BDD"), font=("FontAwesome", 9, "bold"))
        self.side_button_NB.grid(row=1, column=1, pady=(70, 0), padx=6)
        self.side_button_NB.grid_remove()  # Caché initialement

        sidebutton2 = Button(self.sidebar, text="Désordres", bg="#525659", relief=SUNKEN, width=15, height=7, command=self.toggle_side_button2, font=("Arial", 9, "bold"))
        sidebutton2.grid(row=2, pady=2, padx=5)

        # Sous-boutons
        self.side_button_fa = Button(self.sidebar, text="Fer apparent", bg="black", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("fer apparent"), font=("FontAwesome", 9, "bold"))
        self.side_button_fa.grid(row=2, column=1, pady=(0, 70), padx=6)
        self.side_button_fa.grid_remove()  # Caché initialement

        self.side_button_fes = Button(self.sidebar, text="Fissures", bg="black", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("fissures"), font=("FontAwesome", 9, "bold"))
        self.side_button_fes.grid(row=2, column=1, pady=(4, 4), padx=6)
        self.side_button_fes.grid_remove()  # Caché initialement

        self.side_button_NB1 = Button(self.sidebar, text="+", bg="black", relief=tk.SUNKEN, width=10, height=2, command=lambda: self.show_page("nouvelle_cat"), font=("FontAwesome", 9, "bold"))
        self.side_button_NB1.grid(row=2, column=1, pady=(70, 0), padx=6)
        self.side_button_NB1.grid_remove()  # Caché initialement

        sidebutton4 = Button(self.sidebar, text="Equipements", bg="#525659", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("equipements"), font=("Arial", 9, "bold"))
        sidebutton4.grid(row=3, pady=2, padx=5)

        sidebutton3 = Button(self.sidebar, text="Sites", bg="#525659", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("sites"), font=("Arial", 9, "bold"))
        sidebutton3.grid(row=4, pady=2, padx=5)

        sidebutton5 = Button(self.sidebar, text="View", bg="#525659", relief=SUNKEN, width=15, height=7, command=lambda: self.show_page("view"), font=("Arial", 9, "bold"))
        sidebutton5.grid(row=5, pady=2, padx=5)

        # Créer les différents Frames ; La classe Frames prend les arguments du parent, de la catégorie et du chemin d'accès au fichier de l'image.
        self.frames = {"Accueil": Home(body, image_paths, mask_paths), "LCMS": Frames(body, "LCMS", "images\\LCMS.png"), 
                        "2d": Frames2(body, "Images 2D", "images\\image-2d.jpg"),
                        "fer apparent": Frames3(body, "Fer apparent", image_paths2, mask_paths2),
                        "fissures": Frames4(body, "Fissures", image_paths1, mask_paths1), 
                        "nouvelle_BDD": Frames5(body, "Nouvelle BDD", "images\\database.png"),
                        "a_propos": Frames6(body, "A propos", "images\\VT.png"),
                        "sites": Frames7(body, "Sites", "images\\VT.png"),
                        "equipements": Frames8(body, "Equipements", "images\\detect.png"),
                        "nouvelle_cat": Frames9(body, "Nouvelle CAT", "images\\database.png"),
                        "view": View(body)}

        self.make_frame("Accueil")
        self.show_page("Accueil")  # Augmente la page d'accueil vers le haut.
        
        # Les threads sont utilisés pour charger simultanément les autres images en arrière-plan
        for x in ("LCMS", "2d", "fer apparent", "fissures", "equipements", "sites", "nouvelle_BDD", "nouvelle_cat", "a_propos", "view"):
            thread = Thread(target=self.make_frame, args=(x,)) 
            thread.start()

    def toggle_sidebar(self):
        if self.sidebar.winfo_viewable():
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side=LEFT, fill=Y)

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

class Home(Frame):
    def __init__(self, parent, image_paths, mask_paths):
        Frame.__init__(self, parent)
        self.image_paths = image_paths
        self.mask_paths = mask_paths
        self.image_objects = []
        self.mask_objects = []

        self.canvas = Canvas(self, width=1050, height=800)
        self.canvas.pack(fill=BOTH, expand=True)

        # Ajout du texte de bienvenue
        self.canvas_text1 = self.canvas.create_text(580, 30, text="""Bienvenue sur Crack Base - ENDSUM""", 
                                                    font=("Castellar", 20, "italic", "bold"), fill="white")

        self.load_images()
        self.create_image_grid()

    def load_images(self):
        for img_path, mask_path in zip(self.image_paths, self.mask_paths):
            img = Image.open(img_path).resize((200, 200))  # Redimensionner les images pour qu'elles s'adaptent à la grille
            mask = Image.open(mask_path).resize((200, 200))
            self.image_objects.append(ImageTk.PhotoImage(img))
            self.mask_objects.append(ImageTk.PhotoImage(mask))

    def create_image_grid(self):
        for i, (img_obj, mask_obj) in enumerate(zip(self.image_objects, self.mask_objects)):
            x = (i % 5) * 210 + 60  # Calculer la position x pour la grille (5 images par ligne, espacement de 210 pixels)
            y = (i // 5) * 210 + 60  # Calculer la position y pour la grille (espacement de 210 pixels)
            image_id = self.canvas.create_image(x, y, image=img_obj, anchor=NW)
            self.canvas.tag_bind(image_id, "<Enter>", lambda e, mask=mask_obj, img_id=image_id: self.on_hover(mask, img_id))
            self.canvas.tag_bind(image_id, "<Leave>", lambda e, img=img_obj, img_id=image_id: self.on_leave(img, img_id))

    def on_hover(self, mask_image, image_id):
        self.canvas.itemconfig(image_id, image=mask_image)

    def on_leave(self, original_image, image_id):
        self.canvas.itemconfig(image_id, image=original_image)

# Chemins des images et des masques
image_paths = ["images/11129.jpg", "images/11142-1.jpg", "images/11142-2.jpg", "images/11169-1.jpg", "images/11169-2.jpg", "images/11215-1.jpg", "images/11215-2.jpg", "images/11215-3.jpg", "images/11215-4.jpg", "images/11215-5.jpg", "images/11215-6.jpg", "images/11215-7.jpg", "images/11215-8.jpg", "images/11215-9.jpg", "images/11215-10.jpg"]
mask_paths = ["images/11129.png", "images/11142-1.png", "images/11142-2.png", "images/11169-1.png", "images/11169-2.png", "images/11215-1.png", "images/11215-2.png", "images/11215-3.png", "images/11215-4.png", "images/11215-5.png", "images/11215-6.png", "images/11215-7.png", "images/11215-8.png", "images/11215-9.png", "images/11215-10.png"]


class Frames(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(20, 50, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(790, 40, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(790, 75, text=f"(Images, profondeur, VT)", font=("Castellar", 13), fill="white")
        self.canvas_text3 = self.canvas.create_text(800, 180,
                                                    text=f"Le capteur LCMS analyse la projection d'une ligne laser \nsur la paroi du tunnel,"
                                                    "fournissant à chaque acquisition \nun profil de profondeur et un profil"
                                                    "d'intensité.\nCelles-ci sont progressivement agrégées au fur et à mesure \nque le"
                                                    "véhicule avance pour former des images \net des cartes de profondeur, avec une"
                                                    "résolution spatiale \nde 1 × 2 mm et une résolution de profondeur submillimétrique.",
                                                    font=("times new roman", 12, "italic", "normal"), fill="white")

        self.canvas_text4 = self.canvas.create_text(780, 350,
                                                    text=f"Nomenclature d'un dossier de données LCMS :\n - Un dossier par séquence\n "
                                                    "- Nom de dossier : “TE_D_18062_H1870_A0” \n TE : Tube Est (TE) ou Tube Ouest (TO) \n "
                                                    "D (ou C) : sens de prise (sens décroissant ou croissant) \n 18062 : numéro séquence (incrémental) \n "
                                                    "H (hauteur à partir du sol en mm) \n A (angle en degrés des capteurs , 0 = à l’horizontal)",
                                                    font=("times new roman", 12, "normal"), fill="white")
        
        self.entry_var = StringVar()
        self.check_var = BooleanVar()
        self.check_var.set(True)

        self.check_var2 = BooleanVar()
        self.check_var2.set(True)

        self.progress1 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress2 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        export_button1 = ttk.Button(self, text=f"Exporter", command=self.export_images_data)
        export_button2 = ttk.Button(self, text=f"Exporter", command=self.export_depth_data)
        export_button22 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data)

        button1 = ttk.Button(self, text=f"Ajouter des données (intensité)", width=40, command=lambda: upload_lcms(self, category))
        button01 = ttk.Button(self, text=f"Ajouter des données .mat (intensité)", width=40, command=lambda: upload_lcms_mat(self, category))
        button2 = ttk.Button(self, text=f"Ajouter des données (profondeur)", width=40, command=lambda: upload_depths(self, category))
        button02 = ttk.Button(self, text=f"Ajouter des données .mat (profondeur)", width=40, command=lambda: upload_depths_mat(self, category))
        button22 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=40, command=lambda: upload_masques(self, category))

        self.canvas_button1 = self.canvas.create_window(750, 470, window=button1)
        self.canvas_export_button1 = self.canvas.create_window(950, 470, window=export_button1)
        self.canvas_progress1 = self.canvas.create_window(750, 500, window=self.progress1)
        self.canvas_button01 = self.canvas.create_window(750, 530, window=button01)
        self.canvas_button2 = self.canvas.create_window(750, 570, window=button2)
        self.canvas_export_button2 = self.canvas.create_window(950, 570, window=export_button2)
        self.canvas_progress2 = self.canvas.create_window(750, 600, window=self.progress2)
        self.canvas_button02 = self.canvas.create_window(750, 630, window=button02)
        self.canvas_button22 = self.canvas.create_window(750, 670, window=button22)
        self.canvas_export_button22 = self.canvas.create_window(950, 670, window=export_button22)

    def add(self, table):
        site, tube, sens = select_site_details(self)
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

    def export_data(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\lcms_database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"tube": row[3],
                #"sens": row[4],
                "nom_image": row[1]
                #"image_json": row[6]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_images_data(self):
        self.export_data('images', 'images_data.json')

    def export_depth_data(self):
        self.export_data('profondeur', 'depth_data.json')

    def export_masques_data(self):
        self.export_data('masques', 'masques_data.json')
class Frames2(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=tk.TRUE)
        
        self.canvas_text1 = self.canvas.create_text(500, 40, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(500, 75, text=f"(Images visibles, VT, pas de profondeur)", font=("Castellar", 13), fill="white")
        self.canvas_text3 = self.canvas.create_text(340, 120, text=f"- Tunnel Rive-de-Gier (RDG)", font=("times new roman", 12, "normal", "bold"), fill="white")
        self.canvas_text4 = self.canvas.create_text(340, 220, text=f"→ Acquisition par un véhicule, sous forme de séquences, par bande (par passage) \n"
                                                                    "2 images par mètre, tunnel 80 m environ, total entre 160 et 180 images \n"
                                                                    "Nomenclature :\n 1 dossier  par passage. 2 types de caméras : \nles caméras de relevés sont indiqués dans le nom du dossier avec le mot “Voute”. \n"
                                                                    "Les autres dossiers sont des images pour la localisation odométrique, il n’y a pas d’indication “Voute” \n"
                                                                    "Nom : VT_RDG_Voute_0deg_sens_moins. \n"
                                                                    "1 sous-dossier numéroté contient l’image originale et l’image binaire (VT)",
                                                               font=("times new roman", 12, "normal"), fill="white")
        
        self.progress1 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        export_button003 = ttk.Button(self, text=f"Exporter", command=self.export_images_data03)
        export_button004 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data03)

        button03 = ttk.Button(self, text=f"Ajouter des données Images à la base 'RDG'", width=45, command=lambda: upload_images_rdg(self, category))
        button03.pack(pady=10)
        button003 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=45, command=lambda: upload_masques_rdg(self, category))
        button003.pack(pady=10)

        self.canvas_button = self.canvas.create_window(760, 160, window=button03)
        self.canvas_export_button1 = self.canvas.create_window(980, 160, window=export_button003)
        self.canvas_button = self.canvas.create_window(760, 200, window=button003)
        self.canvas_export_button1 = self.canvas.create_window(980, 200, window=export_button004)
        self.canvas_progress1 = self.canvas.create_window(800, 240, window=self.progress1)

        self.canvas_text3 = self.canvas.create_text(340, 320, text=f"- Tunnel piéton (Benfeld)", font=("times new roman", 12, "normal", "bold"), fill="white")
        self.canvas_text5 = self.canvas.create_text(260, 390, text=f"→ Acquisition “à la volée” par un smartphone \n"
                                                                    "4 sous dossiers CC-S, CC-C, CS-C, CS-S \n"
                                                                    "CC = coté centre ou ; CS = côté station \n"
                                                                    "- C ou -S = Cloudy , ou Sunny \n"
                                                                    "1 sous-dossier numéroté contient l’image originale et l’image binaire (VT)",
                                                               font=("times new roman", 12, "normal"), fill="white")
        
        self.progress01 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        export_button001 = ttk.Button(self, text=f"Exporter", command=self.export_images_data01)
        export_button002 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data01)

        button01 = ttk.Button(self, text=f"Ajouter des données Images à la base 'BENFELD'", width=45, command=lambda: upload_images_benfeld(self, category))
        button01.pack(pady=10)

        button001 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=45, command=lambda: upload_masques_benfeld(self, category))
        button001.pack(pady=10)

        self.canvas_button = self.canvas.create_window(760, 350, window=button01)
        self.canvas_export_button1 = self.canvas.create_window(980, 350, window=export_button001)
        self.canvas_button = self.canvas.create_window(760, 390, window=button001)
        self.canvas_export_button1 = self.canvas.create_window(980, 390, window=export_button002)
        self.canvas_progress01 = self.canvas.create_window(800, 430, window=self.progress01)

        self.canvas_text3 = self.canvas.create_text(340, 470, text=f"- Base CODEBRIM", font=("times new roman", 12, "normal", "bold"), fill="white")
        self.canvas_text6 = self.canvas.create_text(260, 520, text=f"→ Images à la volée, tailles différentes \n"
                                                                    "Récupéré d’un papier avec base d’images désordres sur OA \n"
                                                                    "Ajout de la VT en segmentation \n"
                                                                    "1 sous-dossier numéroté contient l’image originale et l’image binaire (VT)",
                                                               font=("times new roman", 12, "normal"), fill="white")
        
        self.progress02 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        export_button005 = ttk.Button(self, text=f"Exporter", command=self.export_images_data02)
        export_button006 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data02)

        button02 = ttk.Button(self, text=f"Ajouter des données Images à la base 'CODEBRIM'", width=45, command=lambda: upload_images_codebrim(self, category))
        button02.pack(pady=10)

        button002 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=45, command=lambda: upload_masques_codebrim(self, category))
        button002.pack(pady=10)

        self.canvas_button = self.canvas.create_window(760, 480, window=button02)
        self.canvas_export_button1 = self.canvas.create_window(980, 480, window=export_button005)
        self.canvas_button = self.canvas.create_window(760, 520, window=button002)
        self.canvas_export_button1 = self.canvas.create_window(980, 520, window=export_button006)
        self.canvas_progress02 = self.canvas.create_window(800, 550, window=self.progress02)

        self.canvas_text3 = self.canvas.create_text(340, 580, text=f"- Base UFR", font=("times new roman", 12, "normal", "bold"), fill="white")
        self.canvas_text7 = self.canvas.create_text(280, 620, text=f"→ Images à la volée, 2 capteurs (Apple ou Samsung) \n"
                                                                    "2 types de VT (à l’objet , comme autres bases, et sous forme de bande ou mask)",
                                                               font=("times new roman", 12, "normal"), fill="white")
        
        self.progress03 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        export_button007 = ttk.Button(self, text=f"Exporter", command=self.export_images_data04)
        export_button008 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data04)

        button04 = ttk.Button(self, text=f"Ajouter des données Images à la base 'UFR'", width=45, command=lambda: upload_images_ufr(self, category))
        button04.pack(pady=10)

        button004 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=45, command=lambda: upload_masques_ufr(self, category))
        button004.pack(pady=10)

        self.canvas_button = self.canvas.create_window(760, 600, window=button04)
        self.canvas_export_button1 = self.canvas.create_window(980, 600, window=export_button007)
        self.canvas_button = self.canvas.create_window(760, 640, window=button004)
        self.canvas_export_button1 = self.canvas.create_window(980, 640, window=export_button008)
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

    def export_data1(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\benfeld.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"cote": row[3],
                #"meteo": row[4],
                "nom_image": row[1]
                #"image_json": row[6]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_data2(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\rdg.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"camera": row[3],
                #"sens": row[4],
                "nom_image": row[1]
                #"image_json": row[6]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_data3(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\codebrim.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"type": row[3],
                "nom_image": row[1]
                #"image_json": row[5]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_data4(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\ufr.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"capteur": row[3],
                "nom_image": row[1]
                #"image_json": row[5]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_images_data01(self):
        self.export_data1('images_benfeld', 'images_data_benfeld.json')

    def export_masques_data01(self):
        self.export_data1('masques_benfeld', 'masques_data_benfeld.json')

    def export_images_data03(self):
        self.export_data2('images_rdg', 'images_data_rdg.json')

    def export_masques_data03(self):
        self.export_data2('masques_rdg', 'masques_data_rdg.json')

    def export_images_data02(self):
        self.export_data3('images_codebrim', 'images_data_codebrim.json')

    def export_masques_data02(self):
        self.export_data3('masques_codebrim', 'masques_data_codebrim.json')

    def export_images_data04(self):
        self.export_data4('images_ufr', 'images_data_ufr.json')

    def export_masques_data04(self):
        self.export_data4('masques_ufr', 'masques_data_ufr.json')

class Frames3(Frame):
    selected_tables = []
    def __init__(self, parent, category, image_paths2, mask_paths2):
        Frame.__init__(self, parent, bg="gray")
        self.image_paths2 = image_paths2
        self.mask_paths2 = mask_paths2
        self.image_objects2 = []
        self.mask_objects2 = []
        self.category = category
        self.canvas = Canvas(self, width=1050, height=800)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas_text1 = self.canvas.create_text(700, 30, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        #self.canvas_text2 = self.canvas.create_text(160, 500,
        #                                            text=f"Pour afficher vos données enregistrées \n'{category.lower()}', cliquez sur le menu View \n "
        #                                                 f"de la barre de menu et sélectionnez \n'View {category}'.", font=("times new roman", 12, "normal"), fill="white")

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
        self.canvas_button = self.canvas.create_window(180, 180, window=button01)
        self.canvas_button = self.canvas.create_window(180, 220, window=self.table_choice_button)
        self.canvas_button = self.canvas.create_window(180, 280, window=button02)
        self.canvas_button = self.canvas.create_window(180, 320, window=self.table_choice_button2)
        self.canvas_button = self.canvas.create_window(180, 380, window=button03)
        self.canvas_button = self.canvas.create_window(180, 420, window=self.table_choice_button3)
        self.canvas_button = self.canvas.create_window(180, 480, window=button04)
        self.canvas_button = self.canvas.create_window(180, 520, window=self.table_choice_button4)

        self.load_images2()
        self.create_image_grid2()

    def load_images2(self):
        for img_path, mask_path in zip(self.image_paths2, self.mask_paths2):
            img = Image.open(img_path).resize((200, 200))  # Redimensionner les images pour qu'elles s'adaptent à la grille
            mask = Image.open(mask_path).resize((200, 200))
            self.image_objects2.append(ImageTk.PhotoImage(img))
            self.mask_objects2.append(ImageTk.PhotoImage(mask))

    def create_image_grid2(self):
        for i, (img_obj, mask_obj) in enumerate(zip(self.image_objects2, self.mask_objects2)):
            x = (i % 3) * 210 + 370  # Calculer la position x pour la grille (3 images par ligne, espacement de 210 pixels)
            y = (i // 3) * 210 + 70  # Calculer la position y pour la grille (espacement de 210 pixels)
            image_id = self.canvas.create_image(x, y, image=img_obj, anchor=NW)
            self.canvas.tag_bind(image_id, "<Enter>", lambda e, mask=mask_obj, img_id=image_id: self.on_hover(mask, img_id))
            self.canvas.tag_bind(image_id, "<Leave>", lambda e, img=img_obj, img_id=image_id: self.on_leave(img, img_id))

    def on_hover(self, mask_image, image_id):
        self.canvas.itemconfig(image_id, image=mask_image)

    def on_leave(self, original_image, image_id):
        self.canvas.itemconfig(image_id, image=original_image)

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

image_paths2 = ["images/input_0.png", "images/input_1.png", "images/input_2.png", "images/input_3.png", "images/input_4.png", "images/input_5.png", "images/input_6.png", "images/input_7.png", "images/input_8.png"]
mask_paths2 = ["images/0.png", "images/1.png", "images/2.png", "images/3.png", "images/4.png", "images/5.png", "images/6.png", "images/7.png", "images/8.png"]

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
    def __init__(self, parent, category, image_paths1, mask_paths1):
        Frame.__init__(self, parent, bg="gray")
        self.image_paths1 = image_paths1
        self.mask_paths1 = mask_paths1
        self.image_objects1 = []
        self.mask_objects1 = []
        self.category = category
        self.canvas = Canvas(self, width=1050, height=800)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas_text1 = self.canvas.create_text(800, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        #self.canvas_text2 = self.canvas.create_text(800, 180,
        #                                            text=f"Pour afficher vos données enregistrées '{category.lower()}',\ncliquez sur le menu View "
        #                                                 f"de la barre de menu \net sélectionnez 'View {category}'.", font=("times new roman", 12, "normal"), fill="white")

        self.load_images1()
        self.create_image_grid1()

        self.progress001 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress002 = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')

        export_button00 = ttk.Button(self, text=f"Exporter", command=self.export_images_data00)
        export_button11 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data01)
        export_button22 = ttk.Button(self, text=f"Exporter", command=self.export_images_data02)
        export_button33 = ttk.Button(self, text=f"Exporter", command=self.export_masques_data03)

        button3 = ttk.Button(self, text=f"Ajouter des données Images à la base 'deepCrack'", width=45, command=lambda: upload_images_deep(self, category))
        button3.pack(pady=10)

        button4 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=45, command=lambda: upload_masques_deep(self, category))
        button4.pack(pady=10)

        button5 = ttk.Button(self, text=f"Ajouter des données Images à la base 'grandMare'", width=45, command=lambda: upload_images_grand(self, category))
        button5.pack(pady=10)

        button6 = ttk.Button(self, text=f"Ajouter des données VT (format COCO)", width=45, command=lambda: upload_masques_grand(self, category))
        button6.pack(pady=10)

        self.canvas_button = self.canvas.create_window(760, 160, window=button3)
        self.canvas_export_button00 = self.canvas.create_window(980, 160, window=export_button00)
        self.canvas_button = self.canvas.create_window(760, 200, window=button4)
        self.canvas_export_button11 = self.canvas.create_window(980, 200, window=export_button11)
        self.canvas_progress001 = self.canvas.create_window(760, 240, window=self.progress001)
        self.canvas_button = self.canvas.create_window(760, 280, window=button5)
        self.canvas_export_button22 = self.canvas.create_window(980, 280, window=export_button22)
        self.canvas_button = self.canvas.create_window(760, 320, window=button6)
        self.canvas_export_button33 = self.canvas.create_window(980, 320, window=export_button33)
        self.canvas_progress002 = self.canvas.create_window(760, 360, window=self.progress002)

        self.entry_var = StringVar()

    def load_images1(self):
        for img_path, mask_path in zip(self.image_paths1, self.mask_paths1):
            img = Image.open(img_path).resize((200, 200))  # Redimensionner les images pour qu'elles s'adaptent à la grille
            mask = Image.open(mask_path).resize((200, 200))
            self.image_objects1.append(ImageTk.PhotoImage(img))
            self.mask_objects1.append(ImageTk.PhotoImage(mask))

    def create_image_grid1(self):
        for i, (img_obj, mask_obj) in enumerate(zip(self.image_objects1, self.mask_objects1)):
            x = (i % 2) * 210 + 60  # Calculer la position x pour la grille (2 images par ligne, espacement de 210 pixels)
            y = (i // 2) * 210 + 60  # Calculer la position y pour la grille (espacement de 210 pixels)
            image_id = self.canvas.create_image(x, y, image=img_obj, anchor=NW)
            self.canvas.tag_bind(image_id, "<Enter>", lambda e, mask=mask_obj, img_id=image_id: self.on_hover(mask, img_id))
            self.canvas.tag_bind(image_id, "<Leave>", lambda e, img=img_obj, img_id=image_id: self.on_leave(img, img_id))

    def on_hover(self, mask_image, image_id):
        self.canvas.itemconfig(image_id, image=mask_image)

    def on_leave(self, original_image, image_id):
        self.canvas.itemconfig(image_id, image=original_image)
    
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

    def export_data0(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\deepCrack.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"type": row[3],
                "nom_image": row[1]
                #"image_json": row[5]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_data1(self, table_name, json_filename):
        conn = sqlite3.connect('DB\\grandMare.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, nom_image FROM {table_name}")
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                #"category": row[1],
                #"site": row[2],
                #"tube": row[3],
                "nom_image": row[1]
                #"image_json": row[5]
            })
        
        os.makedirs('export', exist_ok=True)
        file_path = os.path.join('export', json_filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        conn.close()
        messagebox.showinfo("Exportation réussie", f"Les données de la table '{table_name}' ont été exportées avec succès dans {file_path}.")

    def export_images_data00(self):
        self.export_data0('images_deep', 'images_data_deep.json')

    def export_masques_data01(self):
        self.export_data0('masques_deep', 'masques_data_deep.json')

    def export_images_data02(self):
        self.export_data1('images_grand', 'images_data_grand.json')

    def export_masques_data03(self):
        self.export_data1('masques_grand', 'masques_data_grand.json')

# Chemins des images et des masques
image_paths1 = ["images/11129.jpg", "images/11142-1.jpg", "images/11142-2.jpg", "images/11169-1.jpg", "images/11169-2.jpg", "images/11215-1.jpg"]
mask_paths1 = ["images/11129.png", "images/11142-1.png", "images/11142-2.png", "images/11169-1.png", "images/11169-2.png", "images/11215-1.png"]

import subprocess  # Ajoutez ceci en haut de votre fichier

class DatabaseManager:
    def __init__(self, db_path="DB"):
        self.db_path = db_path
        self.connection = self.connect()

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        print(f"Connecté à la base de données '{self.db_path}'")
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                site TEXT NOT NULL,
                tube TEXT NOT NULL,
                sens TEXT NOT NULL,
                hauteur INTEGER NOT NULL,
                angle INTEGER NOT NULL,
                nom_image TEXT NOT NULL,
                image_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("Table 'images' créée avec succès.")

        connection.commit()
        return connection

    def create_new_db(self, new_db_path):
        new_connection = sqlite3.connect(new_db_path)
        new_cursor = new_connection.cursor()

        new_cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                site TEXT NOT NULL,
                tube TEXT NOT NULL,
                sens TEXT NOT NULL,
                hauteur INTEGER NOT NULL,
                angle INTEGER NOT NULL,
                nom_image TEXT NOT NULL,
                image_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("Table 'images' dans la nouvelle base de données créée avec succès.")
        new_connection.commit()
        new_connection.close()

    def insert_image_data(self, db_path, data, progress_callback=None):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            placeholders = ", ".join(["?"] * len(data))
            columns = ", ".join(data.keys())
            cursor.execute(f'''
                INSERT INTO images ({columns})
                VALUES ({placeholders})
            ''', list(data.values()))
            connection.commit()
            connection.close()
            
            if progress_callback:
                progress_callback()

        except sqlite3.Error as e:
            print(e)

    def close(self):
        self.connection.close()
        print("Connexion à la base de données fermée.")

class Frames5(tk.Frame):
    def __init__(self, parent, category, image_path):
        tk.Frame.__init__(self, parent, bg="gray")
        self.category = category
        self.db_manager = None

        image = Image.open(image_path)
        self.image = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas_image = self.canvas.create_image(10, 50, image=self.image, anchor=tk.NW)
        self.canvas_text1 = self.canvas.create_text(900, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(900, 180,
                                                    text=f"Pour créer une nouvelle catégorie d'images,\n cliquez sur le bouton 'Nouvelle BDD'\n ci-dessous.\n Vous pouvez également importer vos données\n dans cette nouvelle base de données\n en cliquant sur 'Ajouter des données'.", font=("times new roman", 12, "normal"), fill="white")

        self.progress = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.canvas_progress = self.canvas.create_window(900, 380, window=self.progress)

        button5 = ttk.Button(self, text=f"Nouvelle BDD", width=40, command=self.nouvelle_bdd)
        button6 = ttk.Button(self, text=f"Ajouter des Données", width=40, command=self.ajouter_donnees)

        self.canvas_button1 = self.canvas.create_window(900, 300, window=button5)
        self.canvas_button2 = self.canvas.create_window(900, 340, window=button6)

    def nouvelle_bdd(self):
        new_db_name = simpledialog.askstring("Nom de la Nouvelle Base de Données", "Entrez le nom de la nouvelle base de données:")
        if new_db_name:
            new_db_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

            if new_db_path:
                self.db_manager = DatabaseManager(new_db_path)
                self.db_manager.create_new_db(new_db_path)
                messagebox.showinfo("Succès", "Nouvelle base de données créée avec succès!")

    def ajouter_donnees(self):
        if not self.db_manager:
            messagebox.showwarning("Attention", "Veuillez d'abord créer une nouvelle base de données.")
            return

        db_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])
        if not db_path:
            return

        category = simpledialog.askstring("Catégorie", "Entrez la catégorie:")
        site = simpledialog.askstring("Site", "Entrez le nom du site:")
        tube = simpledialog.askstring("Tube", "Entrez le tube:")
        sens = simpledialog.askstring("Sens de prise", "Entrez le sens de prise:")
        hauteur = simpledialog.askinteger("Hauteur", "Entrez la hauteur:")
        angle = simpledialog.askinteger("Angle", "Entrez l'angle:")

        if None in [category, site, tube, sens, hauteur, angle]:
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return

        folder_path = filedialog.askdirectory(title="Sélectionner un dossier d'images")
        if not folder_path:
            return

        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
        total_files = len(image_files)
        self.progress["maximum"] = total_files
        self.progress["value"] = 0

        def update_progress():
            self.progress["value"] += 1
            percent = int((self.progress["value"] / total_files) * 100)
            self.canvas.itemconfigure(self.canvas_text2, text=f"Importation en cours... {percent}%")
            self.update_idletasks()

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            with open(image_path, 'rb') as file:
                image_data = file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            data = {
                "category": category,
                "site": site,
                "tube": tube,
                "sens": sens,
                "hauteur": hauteur,
                "angle": angle,
                "nom_image": image_file,
                "image_json": json.dumps({"image": image_base64}),
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            self.db_manager.insert_image_data(db_path, data, update_progress)
        
        messagebox.showinfo("Succès", "Données ajoutées avec succès!")

class Frames6(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(10, 50, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(900, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(920, 230,
                                                    text=f"Bienvenue sur Crack Base! \nVotre solution complète de gestion de bases de données. \nConçue pour répondre aux besoins des \npassionnés de données, Crack Base offre une expérience \nintuitive et puissante pour gérer efficacement \ntoutes vos données.", font=("times new roman", 13, "italic"), fill="white")

        self.canvas_text3 = self.canvas.create_text(380, 480,
                                                    text=f"Avec Crack Base, vous pouvez créer, modifier et interroger des bases de données avec facilité. \nNotre interface conviviale vous permet de naviguer sans effort à travers vos ensembles de données, \nde créer des rapports personnalisés et d'analyser vos informations pour des insights précieux.", font=("times new roman", 13, "italic"), fill="white")

        self.canvas_text4 = self.canvas.create_text(400, 580,
                                                    text=f"Que vous soyez un développeur cherchant à gérer des données volumineuses, un analyste de données \nexplorant des tendances complexes ou un étudiant apprenant les bases de la gestion de bases de données, \nCrack Base est l'outil idéal pour vos besoins.", font=("times new roman", 13, "italic"), fill="white")
      
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
        self.canvas_image = self.canvas.create_image(30, 30, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(380, 420, text=f"{category}", font=("Castellar", 20, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(400, 520,
                                                    text=f"Avec notre application, vous avez la liberté d'ajouter autant de sites que vous le souhaitez. \nEn quelques clics, vous pouvez créer un nouveau site en utilisant le bouton <Nouveau site>. \nDe là, vous avez le choix : \nvous pouvez intégrer ce site à une base de données existante pour une gestion centralisée et organisée, \nou bien créer une toute nouvelle base de données dédiée à ce site spécifique. \nCette flexibilité vous permet de personnaliser votre expérience selon vos besoins \net de structurer vos données de la manière qui vous convient le mieux.", font=("times new roman", 13, "italic"), fill="white")
        
        self.entry_var = StringVar()
        self.sites = []  # Attribut pour stocker la liste des sites

        button5 = ttk.Button(self, text=f"Nouveau site", width=40, command=self.add_new_site)
        button4 = ttk.Button(self, text=f"Choisir une BDD", width=40, command=self.choose_database_for_site)
        button6 = ttk.Button(self, text=f"BDD existante", width=40, command=self.add_site_to_existing_database)
        button7 = ttk.Button(self, text=f"Nouvelle BDD", width=40, command=self.nouvelle_bdd)
        button8 = ttk.Button(self, text=f"Nouvelle Table", width=40, command=self.table_nouvelle_bdd)
        button9 = ttk.Button(self, text=f"Ajouter des données", width=40, command=self.donnees_nouvelle_bdd)
        button10 = ttk.Button(self, text=f"Liste des sites", width=40, command=self.show_sites_list)
        button11 = ttk.Button(self, text=f"Modifier/Supprimer un site", width=40, command=self.modify_or_delete_site)

        self.canvas_button = self.canvas.create_window(900, 50, window=button5)
        self.canvas_button = self.canvas.create_window(900, 90, window=button4)
        self.canvas_button = self.canvas.create_window(900, 130, window=button6)
        self.canvas_button = self.canvas.create_window(900, 170, window=button7)
        self.canvas_button = self.canvas.create_window(900, 210, window=button8)
        self.canvas_button = self.canvas.create_window(900, 250, window=button9)
        self.canvas_button = self.canvas.create_window(900, 290, window=button10)
        self.canvas_button = self.canvas.create_window(900, 330, window=button11)

    def add_new_site(self):
        site_name = simpledialog.askstring("Nouveau site", "Entrez le nom du nouveau site:")
        if site_name:
            self.sites.append(site_name)  # Ajouter le site à la liste
            self.choose_database_for_site(site_name)
            messagebox.showinfo("Site ajouté", f"Le site {site_name} a été ajouté avec succès.")

    def show_sites_list(self):
        sites_str = "\n".join(self.sites)
        messagebox.showinfo("Liste des sites", f"Sites existants:\n{sites_str}")

    def add_site_to_existing_database(self):
        site_name = simpledialog.askstring("Nouveau site", "Entrez le nom du nouveau site:")
        if site_name:
            self.sites.append(site_name)
            self.choose_database_for_site(site_name)

    def choose_database_for_site(self, site_name):
        existing_databases = self.get_existing_databases()
        if existing_databases:
            # Afficher une fenêtre avec les bases de données existantes
            database_window = Toplevel(self)
            database_window.title("Bases de données existantes")
            database_window.geometry("400x200")

            # Créer une liste déroulante pour afficher les bases de données existantes
            chosen_database = StringVar(database_window)
            chosen_database.set(existing_databases[0])  # Valeur initiale

            database_label = Label(database_window, text="Choisissez une base de données existante:")
            database_label.pack(pady=10)

            database_menu = OptionMenu(database_window, chosen_database, *existing_databases)
            database_menu.pack(pady=10)

            # Bouton pour confirmer le choix de la base de données
            confirm_button = Button(database_window, text="Confirmer", command=lambda: self.add_site_to_existing(chosen_database.get(), site_name))
            confirm_button.pack(pady=10)
        else:
            messagebox.showinfo("Aucune Base de Données", "Aucune base de données existante n'a été trouvée. Création d'une nouvelle base de données.")
            self.create_new_database_and_add_site(site_name)

    def get_existing_databases(self):
        # Cette fonction retourne une liste de bases de données existantes
        # Pour simplifier, nous allons supposer qu'elles se trouvent dans le répertoire 'DB'
        db_folder = 'DB'
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        databases = [f for f in os.listdir(db_folder) if f.endswith('.db')]
        return databases

    def add_site_to_existing(self, chosen_database, site_name):
        # Ajouter le site à la base de données existante choisie
        try:
            db_path = os.path.join('DB', chosen_database)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO images VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (site_name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", f"Le site {site_name} a été ajouté à la base de données {chosen_database}.")
        except Error as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def nouvelle_bdd(self):
        # Fonction pour créer une nouvelle base de données
        new_db_name = simpledialog.askstring("Nom de la Nouvelle Base de Données", "Entrez le nom de la nouvelle base de données:")
        if new_db_name:
            new_db_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

            if new_db_path:
                # Créer une connexion à la nouvelle base de données
                new_connection = sqlite3.connect(new_db_path)
                new_cursor = new_connection.cursor()

                # Enregistrez les modifications et fermez la connexion à la nouvelle base de données
                new_connection.commit()
                new_connection.close()

    def table_nouvelle_bdd(self):
        # Fonction pour créer une nouvelle table dans la base de données existante
        db_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

        if db_path:
            # Créer une connexion à la base de données existante
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Demander le nom de la nouvelle table
            table_name = simpledialog.askstring("Nom de la Table", "Entrez le nom de la nouvelle table:")

            if table_name:
                # Demander les champs de la nouvelle table
                fields = simpledialog.askstring("Champs de la Table", "Entrez les champs de la nouvelle table (séparés par des virgules):")

                if fields:
                    # Créer la nouvelle table
                    create_table_query = f'''
                        CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            {fields}
                        );
                    '''
                    cursor.execute(create_table_query)

                    # Enregistrez les modifications et fermez la connexion à la base de données
                    connection.commit()
                    connection.close()

    def donnees_nouvelle_bdd(self):
        # Fonction pour ajouter des données à la base de données
        db_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

        if db_path:
            # Créer une connexion à la base de données existante
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Demander à l'utilisateur les données à ajouter
            data_to_add = simpledialog.askstring("Ajouter des Données", "Entrez les données à ajouter (séparées par des virgules):")

            if data_to_add:
                # Diviser les données en une liste
                data_list = data_to_add.split(',')

                # Créer une requête d'insertion en fonction du nombre de données fournies
                placeholders = ', '.join(['?' for _ in data_list])
                insert_query = f'INSERT INTO votre_table ({", ".join(data_list)}) VALUES ({placeholders})'

                # Demander à l'utilisateur de confirmer l'ajout
                confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment ajouter les données suivantes ?\n{data_list}")

                if confirmation:
                    # Exécuter la requête d'insertion
                    cursor.execute(insert_query, data_list)

                    # Enregistrez les modifications et fermez la connexion à la base de données
                    connection.commit()
                    connection.close()

    def modify_or_delete_site(self):
        site_name = simpledialog.askstring("Modifier/Supprimer un Site", "Entrez le nom du site à modifier ou supprimer:")
        if site_name in self.sites:
            action = simpledialog.askstring("Action", "Voulez-vous 'modifier' ou 'supprimer' le site?")
            if action == 'modifier':
                new_site_name = simpledialog.askstring("Nouveau nom du site", "Entrez le nouveau nom du site:")
                if new_site_name:
                    index = self.sites.index(site_name)
                    self.sites[index] = new_site_name
                    self.update_site_in_database(site_name, new_site_name)
                    messagebox.showinfo("Succès", f"Le site {site_name} a été modifié en {new_site_name}.")
            elif action == 'supprimer':
                self.sites.remove(site_name)
                self.delete_site_from_database(site_name)
                messagebox.showinfo("Succès", f"Le site {site_name} a été supprimé.")
        else:
            messagebox.showinfo("Erreur", f"Le site {site_name} n'existe pas dans la liste.")

    def update_site_in_database(self, old_name, new_name):
        # Met à jour le nom du site dans toutes les bases de données existantes
        databases = self.get_existing_databases()
        for db in databases:
            db_path = os.path.join('DB', db)
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("UPDATE sites SET name = ? WHERE name = ?", (new_name, old_name))
                conn.commit()
                conn.close()
            except Error as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la mise à jour de {old_name} dans {db}: {e}")

    def delete_site_from_database(self, site_name):
        # Supprime le site de toutes les bases de données existantes
        databases = self.get_existing_databases()
        for db in databases:
            db_path = os.path.join('DB', db)
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sites WHERE name = ?", (site_name,))
                conn.commit()
                conn.close()
            except Error as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la suppression de {site_name} dans {db}: {e}")

# Configuration du système de log
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Créer un handler pour écrire les logs dans un fichier avec l'encodage UTF-8
file_handler = logging.FileHandler(os.path.join(log_directory, 'equipements.log'), encoding='utf-8')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Configurer le logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

class Frames8(Frame):
    def __init__(self, parent, category, image_path):
        logging.info('Initialisation de Frames8 avec category: %s et image_path: %s', category, image_path)
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(80, 10, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(380, 500, text=f"{category}", font=("Castellar", 20, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(400, 600,
                                                    text=f"La première étape consiste à modifier le fichier de configuration du modèle de détection. \nCe fichier contient tous les paramètres nécessaires à l'entraînement du modèle, \ntels que la structure du réseau neuronal, les hyperparamètres de l'entraînement, \nles chemins des jeux de données, et les prétraitements des images. \nPour notre projet, nous avons adapté ce fichier pour inclure des informations spécifiques \nsur les types d'équipements à détecter et les annotations correspondantes. \nCela permet au modèle d'apprendre à distinguer entre différents équipements \navec une grande précision.", font=("times new roman", 13, "italic"), fill="white")
      
        self.entry_var = StringVar()
        button5 = ttk.Button(self, text=f"COCO Viewer", width=30, command=self.run_cocoviewer)
        button6 = ttk.Button(self, text=f"Options Config", width=30, command=self.execute_program)
        button7 = ttk.Button(self, text=f"Voir les logs", width=30, command=self.open_log_files) 
        button8 = ttk.Button(self, text=f"Lancer l'entraînement", width=30, command=self.executer3)
        button9 = ttk.Button(self, text=f"Afficher le résultat", width=30, command=self.executer2)
        button10 = ttk.Button(self, text=f"Choix Epoch", width=30, command=self.executer1)
      
        self.canvas_button = self.canvas.create_window(860, 490, window=button5)
        self.canvas_button = self.canvas.create_window(860, 525, window=button6)
        self.canvas_button = self.canvas.create_window(860, 560, window=button7)
        self.canvas_button = self.canvas.create_window(860, 595, window=button8)
        self.canvas_button = self.canvas.create_window(860, 630, window=button9)
        self.canvas_button = self.canvas.create_window(860, 665, window=button10)

    def execute_program(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "option-config.py")
        logging.info('Exécution du programme option-config.py avec chemin: %s', chemin)
        subprocess.run(["python", chemin])

    def open_log_files(self):
        logging.info('Ouverture des fichiers de logs')
        root = ThemedTk(theme="breeze")
        root.title("Logs")
        root.geometry("1000x800")

        # Récupérer la liste des fichiers logs dans le premier dossier
        log_files1 = [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))]

        # Récupérer la liste des fichiers logs dans le deuxième dossier et filtrer les fichiers .log
        log_directory2 = r"C:\Users\z.marouf-araibi\Desktop\Crack-Base\work_dirs\my_custom_config"
        log_files2 = [f for f in os.listdir(log_directory2) if os.path.isfile(os.path.join(log_directory2, f)) and f.endswith(".log")]

        # Fonction pour afficher le contenu du fichier log correspondant au fichier sélectionné dans la liste déroulante
        def show_selected_log(event, log_combobox):
            selected_log = log_combobox.get()
            log_directory_selected = log_directory if log_combobox == log_combobox1 else log_directory2
            with open(os.path.join(log_directory_selected, selected_log), 'r') as f:
                log_content = f.read()
            log_text.delete("1.0", tk.END)  # Effacer le texte précédent
            log_text.insert(tk.END, log_content)

        # Créer une frame pour placer les listes déroulantes côte à côte
        combobox_frame = tk.Frame(root)
        combobox_frame.pack(side="top", pady=10)

        # Ajouter une étiquette pour le premier répertoire
        label1 = tk.Label(combobox_frame, text="Equipements logs")
        label1.pack(side="left", padx=10)

        # Créer une liste déroulante pour sélectionner les fichiers de log du premier répertoire
        log_combobox1 = ttk.Combobox(combobox_frame, values=log_files1, width=50)
        log_combobox1.pack(side="left", padx=10)
        log_combobox1.bind("<<ComboboxSelected>>", lambda event: show_selected_log(event, log_combobox1))  # Passer log_combobox1 comme argument

        # Ajouter une étiquette pour le deuxième répertoire
        label2 = tk.Label(combobox_frame, text="Train logs")
        label2.pack(side="left", padx=10)

        # Créer une liste déroulante pour sélectionner les fichiers de log filtrés du deuxième répertoire
        log_combobox2 = ttk.Combobox(combobox_frame, values=log_files2, width=50)
        log_combobox2.pack(side="left", padx=10)
        log_combobox2.bind("<<ComboboxSelected>>", lambda event: show_selected_log(event, log_combobox2))  # Passer log_combobox2 comme argument

        # Ajoutez un widget Text pour afficher le contenu du fichier log sélectionné
        log_text = tk.Text(root, wrap="word", bg="black", fg="white", font=("Arial", 10))
        log_text.pack(expand=True, fill="both")

        root.mainloop()

    #def run_cocoviewer(self):
    #    logging.info('Exécution de COCO Viewer')
    #    chemin_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coco-viewer", "cocoviewer.py")
    #    logging.info('Lancement du script COCO Viewer avec images_dir: %s et annotations_file: %s')
    #    subprocess.run(["python", chemin_script]) 

    def run_cocoviewer(self):
        logging.info('Exécution de COCO Viewer')
        chemin_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coco-viewer", "coco-view.py")
        logging.info('Lancement du script COCO Viewer avec images_dir: %s et annotations_file: %s')
        subprocess.run(["python", chemin_script]) 

    def executer3(self):
        chemin_batch = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_train.bat")
        logging.info('Exécution du batch pour l\'entraînement: %s', chemin_batch)
        subprocess.run(['start', 'cmd', '/k', chemin_batch], shell=True)

    def executer2(self):
        chemin_batch = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_resultat.bat")
        logging.info('Exécution du batch pour afficher le résultat: %s', chemin_batch)
        subprocess.run(['start', 'cmd', '/k', chemin_batch], shell=True)

    def executer1(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mmdetection", "choix-epoch.py")
        logging.info('Exécution du script choix-epoch.py: %s', chemin)
        subprocess.run(["python", chemin])

    def add(self, event):
        entry = self.entry_var.get()
        logging.info('Ajout de l\'entrée: %s', entry)
        if len(entry.strip()) > 2:
            messagebox.showinfo("Ajouté avec succès", f"{entry.title().strip()} a été ajouté avec succès")
            insert(entry.title().strip(), self.category)
        elif len(entry.strip()) < 1:
            logging.warning('Aucune entrée fournie')
            pass
        else:
            messagebox.showinfo("Doit contenir plus de 2 caractères","Les caractères saisis sont trop courts.")
        self.entry_var.set("")

    @staticmethod
    def lire_fichier(filepath):
        logging.info('Lecture du fichier: %s', filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                contenu = file.read()
            return contenu
        except FileNotFoundError:
            logging.error('Le fichier n\'existe pas: %s', filepath)
            return "Le fichier n'existe pas."
        except Exception as e:
            logging.error('Erreur lors de la lecture du fichier: %s', e)
            return f"Une erreur s'est produite : {e}"
        
class DbManager:
    def __init__(self, db_path="DB"):
        self.db_path = db_path
        self.connection = self.connect()

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        print(f"Connecté à la base de données '{self.db_path}'")
        return connection

    def create_new_db(self, new_db_path, disorder_type):
        new_connection = sqlite3.connect(new_db_path)
        new_cursor = new_connection.cursor()

        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {disorder_type} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                site TEXT NOT NULL,
                nom_image TEXT NOT NULL,
                image_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        '''
        new_cursor.execute(create_table_query)
        print(f"Table '{disorder_type}' dans la nouvelle base de données créée avec succès.")
        new_connection.commit()
        new_connection.close()

    def insert_image_data(self, db_path, table_name, data, progress_callback=None):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            placeholders = ", ".join(["?"] * 5)  # 5 placeholders for category, site, nom_image, image_json, created_at
            columns = ", ".join(data.keys())
            cursor.execute(f'''
                INSERT INTO {table_name} (category, site, nom_image, image_json, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (data["category"], data["site"], data["nom_image"], data["image_json"], data["created_at"]))
            connection.commit()
            connection.close()
            
            if progress_callback:
                progress_callback()

        except sqlite3.Error as e:
            print(e)

    def close(self):
        self.connection.close()
        print("Connexion à la base de données fermée.")

class Frames9(tk.Frame):
    def __init__(self, parent, category, image_path):
        tk.Frame.__init__(self, parent, bg="gray")
        self.category = category
        self.db_manager = None

        image = Image.open(image_path)
        self.image = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas_image = self.canvas.create_image(10, 50, image=self.image, anchor=tk.NW)
        self.canvas_text1 = self.canvas.create_text(900, 80, text=f"{category}", font=("Castellar", 30, "italic"), fill="white")
        self.canvas_text2 = self.canvas.create_text(900, 180,
                                                    text=f"Pour créer une nouvelle catégorie de désordre,\n cliquez sur le bouton 'Nouvelle BDD/Table'\n ci-dessous.\n Vous pouvez également importer vos données\n dans cette nouvelle base de données\n en cliquant sur 'Ajouter des données'.", font=("times new roman", 12, "normal"), fill="white")
        
        self.progress = Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.canvas_progress = self.canvas.create_window(900, 380, window=self.progress)

        button5 = ttk.Button(self, text=f"Nouvelle BDD/Table", width=40, command=self.nouvelle_bdd)
        button6 = ttk.Button(self, text=f"Ajouter des Données", width=40, command=self.ajouter_donnees)

        self.canvas_button1 = self.canvas.create_window(900, 300, window=button5)
        self.canvas_button2 = self.canvas.create_window(900, 340, window=button6)

    def nouvelle_bdd(self):
        new_db_name = simpledialog.askstring("Nom de la Nouvelle Base de Données", "Entrez le nom de la nouvelle base de données:")
        if new_db_name:
            new_db_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])
            if new_db_path:
                self.db_manager = DbManager(new_db_path)
                disorder_type = simpledialog.askstring("Type de Désordre", "Entrez le type de désordre:")
                if disorder_type:
                    self.db_manager.create_new_db(new_db_path, disorder_type.replace(" ", "_").lower())
                    messagebox.showinfo("Succès", "Nouvelle base de données créée avec succès!")

    def ajouter_donnees(self):
        if not self.db_manager:
            messagebox.showwarning("Attention", "Veuillez d'abord créer une nouvelle base de données.")
            return

        db_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])
        if not db_path:
            return

        category = simpledialog.askstring("Nouvelle Catégorie", "Entrez le nom de la nouvelle catégorie:")
        site = simpledialog.askstring("Nouveau site", "Entrez le nom du nouveau site:")
        disorder_type = simpledialog.askstring("Type de Désordre", "Entrez le type de désordre:")

        if not category or not disorder_type:
            messagebox.showerror("Erreur", "La catégorie et le type de désordre sont requis.")
            return

        table_name = disorder_type.replace(" ", "_").lower()
        folder_path = filedialog.askdirectory(title="Sélectionner un dossier d'images")
        if not folder_path:
            return

        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
        total_files = len(image_files)
        self.progress["maximum"] = total_files
        self.progress["value"] = 0

        def update_progress():
            self.progress["value"] += 1
            percent = int((self.progress["value"] / total_files) * 100)
            self.canvas.itemconfigure(self.canvas_text2, text=f"Importation en cours... {percent}%")
            self.update_idletasks()

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            with open(image_path, 'rb') as file:
                image_data = file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            data = {
                "category": category,
                "site": site,
                "nom_image": image_file,
                "image_json": json.dumps({"image": image_base64}),
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            self.db_manager.insert_image_data(db_path, table_name, data, update_progress)
        
        messagebox.showinfo("Succès", "Données ajoutées avec succès!")

#class OpenGLWidget(QGLWidget):
#    def __init__(self, parent=None):
#        super(OpenGLWidget, self).__init__(parent)
#        self.width = self.size().width()
#        self.height = self.size().height()
#
#    def initializeGL(self):
#        glEnable(GL_DEPTH_TEST)
#
#    def resizeGL(self, width, height):
#        self.width = width
#        self.height = height
#        glViewport(0, 0, self.width, self.height)
#        glMatrixMode(GL_PROJECTION)
#        glLoadIdentity()
#        #gluOrtho2D(0, self.width, 0, self.height)
#        glMatrixMode(GL_MODELVIEW)
#        glLoadIdentity()
#
#    def paintGL(self):
#        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#        glBegin(GL_TRIANGLES)
#        glVertex2f(0, 0)
#        glVertex2f(self.width, 0)
#        glVertex2f(self.width / 2, self.height)
#        glEnd()
#        self.swapBuffers()
class View(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Cadre principal pour contenir l'image et les contrôles
        main_frame = Frame(self.canvas)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cadre pour l'image du tunnel
        self.image_frame = Frame(main_frame)
        self.image_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)

        # Chargement de l'image du tunnel
        self.tunnel_image_path = 'images/tunnel.png'
        self.tunnel_canvas = Canvas(self.image_frame, width=500, height=350)
        self.tunnel_canvas.pack()
        self.load_tunnel_image()

        # Cadre pour les contrôles (boutons, champ de recherche)
        control_frame = Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Cadre pour les boutons, placé par paires
        button_frame = Frame(control_frame)
        button_frame.pack(fill=tk.X)

        # Cadre pour la première paire de boutons
        button_pair1 = Frame(button_frame)
        button_pair1.pack(fill=tk.X)
        ttk.Button(button_pair1, text="Voir le dossier des BDD", width=40, command=self.explorer).pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
        ttk.Button(button_pair1, text="Voir toutes les données", width=40, command=self.view_all_data).pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        # Cadre pour la deuxième paire de boutons
        button_pair2 = Frame(button_frame)
        button_pair2.pack(fill=tk.X)
        ttk.Button(button_pair2, text="Données LCMS", width=40, command=self.view_lcms_data).pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
        ttk.Button(button_pair2, text="Données Fers apparents", width=40, command=self.view_fers_apparents_data).pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        # Cadre pour la troisième paire de boutons
        button_pair3 = Frame(button_frame)
        button_pair3.pack(fill=tk.X)
        ttk.Button(button_pair3, text="Données Fissures", width=40, command=self.view_fissures_data).pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
        ttk.Button(button_pair3, text="Supprimer", width=40, command=self.delete_item).pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        # Cadre pour l'entrée de recherche et le bouton de recherche
        search_frame = Frame(control_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        # Entrée de saisie
        self.entryvar = tk.StringVar()
        entry = ttk.Entry(search_frame, textvariable=self.entryvar, width=40, font=("Helvetica", 12, "normal"))
        entry.pack(side=tk.LEFT, padx=5, pady=5)
        entry.bind("<Return>", self.search_box)

        # Bouton de recherche
        search_button = ttk.Button(search_frame, text="Recherche", command=lambda: self.search_box(None))
        search_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Bouton de la carte LCMS
        map_button = ttk.Button(search_frame, text="Carte LCMS", command=self.run_lcms_map)
        map_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Cadre pour la sélection de la base de données et de la table
        select_frame = Frame(control_frame)
        select_frame.pack(fill=tk.X, padx=5, pady=5)

        # Sélection de la base de données
        self.database_label = ttk.Label(select_frame, text="Base de données:")
        self.database_label.grid(row=0, column=0, padx=5, pady=5)
        self.database_combobox = ttk.Combobox(select_frame, width=30)
        self.database_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.database_combobox.bind("<<ComboboxSelected>>", self.load_tables)

        # Sélection de la table
        self.table_label = ttk.Label(select_frame, text="Table:")
        self.table_label.grid(row=1, column=0, padx=5, pady=5)
        self.table_combobox = ttk.Combobox(select_frame, width=30)
        self.table_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.table_combobox.bind("<<ComboboxSelected>>", self.display_selected_table)

        # Cadre pour le tableau avec barre de défilement
        self.table_frame = Frame(self.canvas)
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Ajout d'une fenêtre défilante pour le tableau
        scrollbar = Scrollbar(self.table_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.table_frame, columns=(), show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        # Pagination
        pagination_frame = Frame(control_frame)
        pagination_frame.pack(fill=tk.X, padx=5, pady=5)

        self.previous_button = ttk.Button(pagination_frame, text="Précédent", command=self.previous_page)
        self.previous_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.page_label = ttk.Label(pagination_frame, text="Page 1")
        self.page_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = ttk.Button(pagination_frame, text="Suivant", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.goto_page_var = tk.StringVar()
        self.goto_page_entry = ttk.Entry(pagination_frame, textvariable=self.goto_page_var, width=5)
        self.goto_page_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.goto_page_entry.bind("<Return>", self.goto_page)

        self.goto_page_button = ttk.Button(pagination_frame, text="Aller à la page", command=self.goto_page)
        self.goto_page_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Chargement des bases de données au démarrage
        self.db_directory = "DB"
        self.load_databases()

        # Binding de l'événement de sélection du TreeView
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Variables de pagination
        self.current_page = 1
        self.items_per_page = 20
        self.total_items = 0
        self.total_pages = 1
        self.data = []  # Contient les données à afficher

    def load_tunnel_image(self):
        self.tunnel_image = Image.open(self.tunnel_image_path)
        self.tunnel_photo = ImageTk.PhotoImage(self.tunnel_image)
        self.tunnel_canvas.create_image(0, 0, anchor=tk.NW, image=self.tunnel_photo)

    def load_databases(self):
        db_files = [f for f in os.listdir(self.db_directory) if f.endswith('.db')]
        self.database_combobox['values'] = db_files

    def load_tables(self, event):
        database_name = self.database_combobox.get()
        if not database_name:
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
            connection.close()
            self.table_combobox['values'] = tables
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors du chargement des tables : {e}")

    def run_lcms_map(self):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carte-folium.py")
        subprocess.run(["python", chemin])

    def explorer(self):
        dossier_db = os.path.abspath(self.db_directory)
        if os.name == 'nt':  # Windows
            subprocess.run(["explorer", dossier_db], shell=True)
        else:  # macOS ou Linux
            subprocess.run(["open", dossier_db], shell=True)

    def display_data(self, title, columns, data):
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.data = data
        self.total_items = len(data)
        self.total_pages = math.ceil(self.total_items / self.items_per_page)
        self.current_page = 1
        self.update_page_label()
        self.show_page_data()

    def show_page_data(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_data = self.data[start_index:end_index]

        self.tree.delete(*self.tree.get_children())
        for row in page_data:
            self.tree.insert('', 'end', values=row)

    def update_page_label(self):
        self.page_label.config(text=f"Page {self.current_page}/{self.total_pages}")

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_page_label()
            self.show_page_data()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_page_label()
            self.show_page_data()

    def goto_page(self, event=None):
        try:
            page = int(self.goto_page_var.get())
            if 1 <= page <= self.total_pages:
                self.current_page = page
                self.update_page_label()
                self.show_page_data()
            else:
                messagebox.showwarning("Avertissement", "Numéro de page invalide.")
        except ValueError:
            messagebox.showwarning("Avertissement", "Veuillez saisir un numéro de page valide.")

    def view_all_data(self):
        database_name = self.database_combobox.get()
        table_name = self.table_combobox.get()
        if not database_name or not table_name:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une base de données et une table.")
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            connection.close()
            self.display_data(f"Données de la table {table_name}", columns, data)
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données : {e}")

    def view_lcms_data(self):
        database_name = self.database_combobox.get()
        table_names = ["images", "profondeur"]  # Liste des tables à afficher
        if not database_name:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une base de données.")
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            for table_name in table_names:
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                self.display_data(f"Données LCMS - {table_name}", columns, data)
            
            connection.close()
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données LCMS : {e}")

    def view_fers_apparents_data(self):
        database_name = self.database_combobox.get()
        table_names = ["images_rdg", "images_benfeld", "images_codebrim", "images_ufr"]  # Liste des tables à afficher
        if not database_name:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une base de données.")
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            for table_name in table_names:
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                self.display_data(f"Données Fers apparents - {table_name}", columns, data)
            
            connection.close()
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données Fers apparents : {e}")

    def view_fissures_data(self):
        database_name = self.database_combobox.get()
        table_names = ["images_deep", "images_grand"]  # Liste des tables à afficher
        if not database_name:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une base de données.")
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            
            for table_name in table_names:
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                self.display_data(f"Données Fissures - {table_name}", columns, data)
            
            connection.close()
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données Fissures : {e}")

    def display_selected_table(self, event):
        self.view_all_data()

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un élément à supprimer.")
            return

        item_values = self.tree.item(selected_item, 'values')
        item_id = item_values[0]  # Supposons que le premier champ soit l'ID

        database_name = self.database_combobox.get()
        table_name = self.table_combobox.get()
        if not database_name or not table_name:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une base de données et une table.")
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (item_id,))
            connection.commit()
            connection.close()

            self.view_all_data()
            messagebox.showinfo("Info", "L'élément a été supprimé avec succès.")
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la suppression de l'élément : {e}")

    def search_box(self, event):
        search_term = self.entryvar.get().strip()
        if not search_term:
            messagebox.showwarning("Avertissement", "Veuillez saisir un terme de recherche.")
            return

        database_name = self.database_combobox.get()
        table_name = self.table_combobox.get()
        if not database_name or not table_name:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une base de données et une table.")
            return

        db_path = os.path.join(self.db_directory, database_name)
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Parsing the search term
            if '=' in search_term:
                column, value = search_term.split('=', 1)
                column = column.strip()
                value = value.strip()
                
                # Handle specific cases for 'sens' and 'angle'
                if column.lower() == 'sens':
                    query = f"SELECT * FROM {table_name} WHERE {column} = ?"
                    params = (value,)
                elif column.lower() == 'angle':
                    try:
                        angle_value = int(value)
                        if 0 <= angle_value <= 90:
                            query = f"SELECT * FROM {table_name} WHERE {column} = ?"
                            params = (angle_value,)
                        else:
                            messagebox.showwarning("Avertissement", "L'angle doit être compris entre 0 et 90.")
                            connection.close()
                            return
                    except ValueError:
                        messagebox.showwarning("Avertissement", "L'angle doit être un nombre entier.")
                        connection.close()
                        return
                else:
                    query = f"SELECT * FROM {table_name} WHERE {column} LIKE ?"
                    params = (f"%{value}%",)
            else:
                # General search for all columns if no specific column is mentioned
                query = f"SELECT * FROM {table_name} WHERE " + " OR ".join([f"{col} LIKE ?" for col in self.tree['columns']])
                params = [f"%{search_term}%"] * len(self.tree['columns'])

            cursor.execute(query, params)
            data = cursor.fetchall()
            connection.close()

            self.display_data(f"Résultats de recherche pour '{search_term}'", self.tree['columns'], data)
        except sqlite3.Error as e:
            print(f"Une erreur s'est produite : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la recherche : {e}")

    def on_treeview_select(self, event):
        # Récupère la ligne sélectionnée
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        values = item['values']

        # Trouver les indices des colonnes 'sens' et 'angle' 
        columns = self.tree["columns"]
        try:
            sens_index = columns.index('sens')
            angle_index = columns.index('angle')
        except ValueError:
            return

        sens = values[sens_index]
        angle = values[angle_index]

        self.highlight_tunnel_section(sens, angle)

    def highlight_tunnel_section(self, sens, angle):
        # Effacer tous les highlights précédents  
        self.tunnel_canvas.delete("highlight")

        # En bas au centre de l'image
        x0 = self.tunnel_photo.width() // 2
        y0 = self.tunnel_photo.height() - 15
        length = 200 
        arrow_width = 20
        arrow_length = 30

        # Ajuster l'angle en fonction du 'sens'
        if sens == 'D':  # Côté gauche de l'image
            if angle == 0:
                adjusted_angle = 180
            elif angle == 30:
                adjusted_angle = 150
            elif angle == 60:
                adjusted_angle = 125
            elif angle == 90:
                adjusted_angle = 90
            else:
                return  
        elif sens == 'C':  # Côté droit de l'image
            if angle == 0:
                adjusted_angle = 0
            elif angle == 30:
                adjusted_angle = 30
            elif angle == 60:
                adjusted_angle = 55
            elif angle == 90:
                adjusted_angle = 90
            else:
                return  
        else:
            return  

        # Calculer les points de la flèche en fonction de l'angle ajusté
        x1 = x0 + length * math.cos(math.radians(adjusted_angle))
        y1 = y0 - length * math.sin(math.radians(adjusted_angle))  

        left_wing_angle = math.radians(adjusted_angle + 150)
        right_wing_angle = math.radians(adjusted_angle - 150)

        left_wing_x = x1 + arrow_length * math.cos(left_wing_angle)
        left_wing_y = y1 - arrow_length * math.sin(left_wing_angle)

        right_wing_x = x1 + arrow_length * math.cos(right_wing_angle)
        right_wing_y = y1 - arrow_length * math.sin(right_wing_angle)

        # Dessiner la flèche sur le canvas
        self.tunnel_canvas.create_line(x0, y0, x1, y1, fill="black", width=6, tags="highlight")
        self.tunnel_canvas.create_polygon(
            x1, y1,
            left_wing_x, left_wing_y,
            right_wing_x, right_wing_y,
            fill="black", tags="highlight"
        )


        # Ajouter un footer
        footer = tk.Label(text="© Crack Base 2024 - ENDSUM", relief=tk.SUNKEN, anchor=tk.W, font=("Castellar", 12, "italic"), bg="black", fg="white")
        footer.grid(row=0, column=0, sticky="ew")

if __name__ == "__main__":
    app = CrackBase()
    app.title("Crack Base 2.0 - ENDSUM")
    app.iconbitmap("images/app.ico")
    app.maxsize(1300,800)
    app.minsize(1300,800)
    app.mainloop()

