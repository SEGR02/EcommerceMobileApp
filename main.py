from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen, SwapTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
import os
import sys
from kivymd.toast import toast
from kivy.logger import Logger
from kivymd.uix.datatables import MDDataTable
from datetime import datetime
from controlador import Login, Registro
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.factory import Factory
#from PIL import Image
from kivy.app import App
import kivy
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ColorProperty, ListProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
import pymongo
from kivy.metrics import dp, sp
#img = Image.open('assets/luis.png')
kivy.require('2.1.0')

Window.size = (310, 580)
MONGO_HOST="localhost"
MONGO_PUERTO= "27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
try:
    cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    cliente.server_info()
    #print("Conexion a Mongo Exitosa")
    

except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print ("Tiempo excedido"+errorTiempo)
except pymongo.errors.ConnectionFailure as errorConexion:
    print ("Error al conectarse a MongoDB"+errorConexion)

dbs = cliente.list_database_names()
db = cliente.App
coleccion = db.usuarios
cursor = db.productos

class VentanaPop(Screen,BoxLayout):
    nombre = StringProperty()
    tipo = StringProperty()
    source = StringProperty()
    desc = StringProperty()
    precio = NumericProperty(0.0)
    back = StringProperty()
       
    def home(self,*args):
        app = App.get_running_app()
        app.manager.current = 'home'
    pass


class HomeScreen(Screen):

    def nav_drawer_open(self, *args):
        bar = self.manager.get_screen('prin')
        nav_drawer = bar.children[0].ids.nav_drawer
        nav_drawer.set_state("open")
    
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.llenar, .1)

    def llenar(self,*kw):
        
        ter = self.manager.get_screen('home')
        lista=list(cursor.find())
        ter.ids.products.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=1,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="4dp",
                    size_hint=(None, 1),
                    size=("200dp", "100dp"),
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.products.add_widget(card)
            
    
    def buscar(self):
        app = App.get_running_app()
        ter = self.manager.get_screen('grid')
        
        buscador = app.manager.get_screen('home').ids['buscador'].text
        lista=list(cursor.find({ "nom_prod": { "$regex": buscador, "$options" :'i' } }))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=1,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="4dp",
                    size_hint=(1, None),
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            

    def llenarpapeleria(self, *args):
        
        ter = self.manager.get_screen('grid')
        #print(ter.ids)
        lista=list(cursor.find({"tipo_prod":"papeleria"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
    
    def llenarferre(self, *args):
        
        ter = self.manager.get_screen('grid')
        lista=list(cursor.find({"tipo_prod":"ferreteria"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            

    def llenarjuguetes(self, *args):
        
        ter = self.manager.get_screen('grid')
        lista=list(cursor.find({"tipo_prod":"jugueteria"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            

    def llenarelect(self, *args):
        
        ter = self.manager.get_screen('grid')
        lista=list(cursor.find({"tipo_prod":"electronica"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            
    

    def ver_producto(self, elemento):
        ver = Factory.VentanaPop()
        ver.nombre = elemento.name
        ver.tipo = elemento.tipo
        ver.precio = elemento.precio
        ver.source = elemento.source
        ver.desc = elemento.desc
        self.ventanapop = Popup(title="",content=ver)
        self.ventanapop.open()
        self.manager.transition = SwapTransition()
        
       
    
    pass
        
class Menu(Screen):
    def desconectar(self):
        self.manager.current = "login"
    pass

class GridProductos(Screen):
    
    def buscar(self):
        app = App.get_running_app()
        ter = self.manager.get_screen('grid')
        #print(ter.ids)
        
        buscador = app.manager.get_screen('grid').ids['buscador'].text
        lista=list(cursor.find({ "nom_prod": { "$regex": buscador, "$options" :'i' } }))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=1,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="4dp",
                    size_hint=(1, None),
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)

    def llenarpapeleria(self, *args):
        
        ter = self.manager.get_screen('grid')
        #print(ter.ids)
        lista=list(cursor.find({"tipo_prod":"papeleria"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            
    
    def llenarferre(self, *args):
        
        ter = self.manager.get_screen('grid')
        #print(ter.ids)
        lista=list(cursor.find({"tipo_prod":"ferreteria"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            

    def llenarjuguetes(self, *args):
        
        ter = self.manager.get_screen('grid')
        #print(ter.ids)
        lista=list(cursor.find({"tipo_prod":"jugueteria"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
        
    def llenarelect(self, *args):
        
        ter = self.manager.get_screen('grid')
        #print(ter.ids)
        lista=list(cursor.find({"tipo_prod":"electronica"}))
        ter.ids.gridprincipal.clear_widgets()
        for elemento in lista:
            
            card=(
                MDCard(
                    
                    MDBoxLayout(
                        Image(
                            source=elemento['imagen_prod'],
                            pos_hint={"top": 1, "right": 1}
                            
                        ),
                        MDLabel(
                            text="$"+str(elemento['precio']),
							font_size=80,
                            #color="grey",
                            pos=("5dp", "5dp"),
                            size_hint= (1.5, 0.2),
                            bold=True,
                        ),
                        size_hint_x=1.5,
					    size_hint_y=3,
                    ),
                    
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="3dp",
                    size_hint=(1, None),
                    
                    orientation="vertical",
                    
                    
                )
            )
            card.precio = elemento['precio']
            card.name = elemento['nom_prod']
            card.tipo = elemento['tipo_prod']
            card.source = elemento['imagen_prod']
            card.desc = elemento['desc_prod']
            card.bind(on_release= self.ver_producto)
            ter.ids.gridprincipal.add_widget(card)
            
    

    def ver_producto(self, elemento):
        app = App.get_running_app()
        popp = app.manager.get_screen('popup')
        ver = Factory.VentanaPop()
        ver.nombre = elemento.name
        ver.tipo = elemento.tipo
        ver.precio = elemento.precio
        ver.source = elemento.source
        ver.desc = elemento.desc
        self.ventanapop = Popup(title="",content=ver)
        self.ventanapop.open()
    
    
    pass

class Administracion(Screen):

    def home(self,*args):
        app = App.get_running_app()
        app.manager.current = 'home'
    pass
    
    def llenardatatable(self,*args):
        app = App.get_running_app()
        box = app.manager.get_screen('elim_obj')
        objetos= list(cursor.find())
        box.ids.datatable.clear_widgets()
        box.ids.boton.clear_widgets()

        tabla = MDDataTable(
            pos_hint = {'center_x':0.5,'center_y':0.5},
            size_hint = (0.95, 0.6),
            use_pagination=True,
            check=True,
            column_data =[
                ("Producto",dp(50)),
                ("Categoria",dp(20)),
                ("Precio",dp(20)),
            ],
                row_data = [
                    (elemento['nom_prod'],elemento['tipo_prod'],elemento['precio']) for elemento in objetos
                    ]
        )
        tabla.bind(on_row_press=self.on_row_press)
        tabla.bind(on_check_press=self.check_borrar)
        box.ids.datatable.add_widget(tabla)
    pass
    def on_row_press(self, instance_table, instance_row):
        
        #print(instance_table, instance_row)
        index = instance_row.index
        cols_num = len(instance_table. column_data)
        row_num = int(index/cols_num)
        
        cell_row =instance_table.table_data.view_adapter.get_visible_view(row_num*cols_num)
        if cell_row.ids.check.state == 'normal':
            instance_table.table_data.select_all('normal')
            cell_row.ids.check.state = 'down'
        else:
            cell_row.ids.check.state = 'normal'
        instance_table.table_data.on_mouse_select(instance_row)
        if cell_row.ids.check.state == 'normal':
            app = App.get_running_app()
            box = app.manager.get_screen('elim_obj')
            box.ids.boton.clear_widgets()

    def check_borrar(self, instance_row, current_row):
        def borrar_producto(self, *args):
            eliminar_producto= cursor.delete_one({"nom_prod":current_row[0]})
            Logger.info("Producto Eliminado: {}".format(eliminar_producto.deleted_count))
            toast ("Producto Eliminado de Forma Exitosa!")
            app.manager.current = 'admin'
            pass
        def visualizar_producto(self):
            ver = Factory.VentanaActualizar()
            busq= cursor.find({"nom_prod":current_row[0]})
            for elemento in busq:
                desc=elemento['desc_prod']
                source=elemento['imagen_prod']

            ver.nombre = current_row[0]
            ver.tipo =current_row[1]
            ver.precio = current_row[2]
            ver.desc = desc
            ver.source = source
            self.ventanapop = Popup(title="Actualizar Producto",content=ver)
            self.ventanapop.open()
            


        app = App.get_running_app()
        box = app.manager.get_screen('elim_obj')
        box.ids.boton.clear_widgets()
        boton = MDBoxLayout(
            MDIconButton(
            icon='trash-can',
            on_release= borrar_producto,
        ),
            MDIconButton(
            icon='rename-box',
            on_release= visualizar_producto,
        ),
            
            orientation="horizontal"
        )
        box.ids.boton.add_widget(boton)
        
        
    
class AgregarObj(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            icon_color="orange",
            background_color_selection_button="orange",
            background_color_toolbar="orange",
            select_path=self.select_path
        )

    # Método para mostrar el administrador de archivos
    def show_file_manager(self):
        self.file_manager.show('/')

    # Método llamado al seleccionar una ruta de archivo
    def select_path(self, path):
        # Actualizar la vista previa de la imagen
        self.ids.imagen_preview.source = path
        self.guardar_imagen_confirmado()
        self.exit_file_manager()

    # Método para cerrar el administrador de archivos
    def exit_file_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
        
      

    # Método llamado al confirmar la acción de guardar la imagen
    def guardar_imagen_confirmado(self, *args):
        # Obtener la ruta de la imagen seleccionada
        self.ruta_imagen = self.ids.imagen_preview.source
        if self.ruta_imagen != "":
            dialog = MDDialog(
            title="Imagen Seleccionada!",
            text="La imagen ha sido seleccionada exitosamente.",
        )
        dialog.open()
        # Guardar la imagen en la ubicación deseada
        # Aquí puedes escribir tu código para guardar la imagen

        # Mostrar un mensaje para confirmar que se guardó la imagen
        #self.ids.imagen_preview.source = ''
        
        #print(ruta_imagen)
        
    
    def ingresar_producto(self, *args):
        try:
            agre_img= self.ruta_imagen
        except AttributeError:
            toast("Por favor selecciona una imagen")
            return
        app = App.get_running_app()
        agre_prod = app.manager.get_screen('agre_obj').ids['agre_prod'].text
        agre_precio = app.manager.get_screen('agre_obj').ids['agre_precio'].text
        agre_tipo = app.manager.get_screen('agre_obj').ids['agre_tipo'].text
        agre_desc = app.manager.get_screen('agre_obj').ids['agre_desc'].text
        agre_img = self.ruta_imagen
        try:
            agre_precio = int(agre_precio)
        except ValueError:
            toast("Ingresa el precio en valor numerico")
            return
        
        valida = cursor.find_one({"nom_prod": agre_prod})
        datosprod = {"nom_prod": agre_prod, "precio": agre_precio,"tipo_prod": agre_tipo,"desc_prod": agre_desc,"imagen_prod":agre_img}
        if valida != None:
            toast("Ya existe un producto con ese nombre, intenta nuevamente")
            return
        else:
            agregar_producto = cursor.insert_one(datosprod)
            Logger.info("Nuevo Producto insertado: {}".format(agregar_producto.inserted_id))
            toast ("Producto Ingresado de Forma Exitosa!")
            consulta = {"nom_prod": agre_prod}
            fecha_prod_agre = {"$set": {"fecha_producto_agregado": datetime.now()}}
            cursor.update_one(consulta, fecha_prod_agre)
            
        
    pass

class EliminarObj(Screen):
    pass

class Gestor(Screen):

    pass
class VentanaActualizar(Screen):
    
    nombre = StringProperty()
    tipo = StringProperty()
    source = StringProperty()
    desc = StringProperty()
    precio = NumericProperty(0.0)
    back = StringProperty()
    source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            icon_color="orange",
            background_color_selection_button="orange",
            background_color_toolbar="orange",
            select_path=self.select_path
        )

    # Método para mostrar el administrador de archivos
    def show_file_manager(self):
        self.file_manager.show('/')

    # Método llamado al seleccionar una ruta de archivo
    def select_path(self, path):
        # Actualizar la vista previa de la imagen
        self.ids.imagen_preview.source = path
        self.guardar_imagen_confirmado()
        self.exit_file_manager()

    # Método para cerrar el administrador de archivos
    def exit_file_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
        
      

    # Método llamado al confirmar la acción de guardar la imagen
    def guardar_imagen_confirmado(self, *args):
        # Obtener la ruta de la imagen seleccionada
        self.act1_imagen = self.ids.imagen_preview.source
        if self.act1_imagen != "":
            dialog = MDDialog(
            title="Imagen Seleccionada!",
            text="La imagen ha sido seleccionada exitosamente.",
        )
        dialog.open()
        # Guardar la imagen en la ubicación deseada
        # Aquí puedes escribir tu código para guardar la imagen

        # Mostrar un mensaje para confirmar que se guardó la imagen
        #self.ids.imagen_preview.source = ''
        
        #print(ruta_imagen)

    def actualizar_producto(self):
        try:
            act_imagen= self.act1_imagen
        except AttributeError:
            toast("Por favor selecciona una imagen")
            return
        app = App.get_running_app()
        prod = self.ids.act_prod.helper_text
        act_prod = self.ids.act_prod.text
        act_precio = self.ids.act_precio.text
        act_tipo = self.ids.act_tipo.text
        act_desc = self.ids.act_desc.text
        cambiar_imagen = self.act1_imagen
        try:
            act_precio = int(act_precio)
        except ValueError:
            toast("Ingresa el precio en valor numerico")
            return
        
        valida = cursor.find_one({"nom_prod": prod})
        datosprod = {"nom_prod": act_prod, "precio": act_precio,"tipo_prod": act_tipo,"desc_prod": act_desc}
        if valida == None:
            toast("No existe un producto con ese nombre, intenta nuevamente")
            return
        else:
            
            toast ("Producto Actualizado de Forma Exitosa!")
            consulta = {"nom_prod": prod}
            actualizar = {"$set": {"nom_prod": act_prod,"precio": act_precio,"tipo_prod": act_tipo,"desc_prod": act_desc,"imagen_desc":cambiar_imagen,"fecha_producto_actualizado": datetime.now()}}
            cursor.update_one(consulta, actualizar)
            app.manager.current = 'admin'
            
    pass

class NovedadesApp(MDApp):
    def build(self):
        #global screen_manager
        #screen_manager = ScreenManager()
        self.manager = ScreenManager(transition=SlideTransition())
        self.manager.add_widget(Builder.load_file("pre-splash.kv"))
        self.manager.add_widget(Login(name='login'))
        self.manager.add_widget(Menu(name='prin'))
        self.manager.add_widget(Registro(name='reg'))
        self.manager.add_widget(HomeScreen(name = 'home'))
        self.manager.add_widget(GridProductos(name = 'grid'))
        self.manager.add_widget(VentanaPop(name = 'popup'))
        self.manager.add_widget(Administracion(name='admin'))
        self.manager.add_widget(AgregarObj(name='agre_obj'))
        self.manager.add_widget(EliminarObj(name='elim_obj'))
        self.manager.add_widget(VentanaActualizar(name='popupact'))
        self.manager.add_widget(Gestor(name='gestor'))
        return self.manager

    def on_start(self):

        Clock.schedule_once(self.renderizar, 6)

    def renderizar(self, *args):
        
        self.manager.current = "home"
        
    def nav_drawer_open(self, *args):
        nav_drawer = self.root.children[0].ids.nav_drawer
        nav_drawer.set_state("open")

if __name__ == '__main__':
    NovedadesApp().run()
