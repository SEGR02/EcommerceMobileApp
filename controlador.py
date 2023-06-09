from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from datetime import datetime
from kivy.uix.screenmanager import Screen, SwapTransition, ScreenManager
import pymongo
from pymongo import MongoClient
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ColorProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.image import Image


MONGO_HOST="localhost"
MONGO_PUERTO= "27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
try:
    cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    cliente.server_info()
    print("Conexion a Mongo Exitosa")
    

except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print ("Tiempo excedido"+errorTiempo)
except pymongo.errors.ConnectionFailure as errorConexion:
    print ("Error al conectarse a MongoDB"+errorConexion)

dbs = cliente.list_database_names()
db = cliente.App
coleccion = db.usuarios
cursor = db.productos


def ingresar_datos(reg_correo, reg_contraseña):
        datosreg = {"input_correo": reg_correo, "input_contraseña": reg_contraseña} 
        registro = coleccion.insert_one(datosreg)
        Logger.info("Nuevo Usuario insertado: {}".format(registro.inserted_id))


class Login(Screen):       

    def regg(self):
        self.manager.current = "reg"

    def home(self):
        self.manager.current = "home"
    
    def connect(self):
        
        app = App.get_running_app()
        input_correo = app.manager.get_screen('login').ids['input_correo'].text
        input_contraseña = app.manager.get_screen('login').ids['input_contraseña'].text
        Datos = coleccion.find_one({"input_correo": input_correo, "input_contraseña": input_contraseña })          
        if (Datos is None):
            toast("Datos Incorrectos, intentalo de nuevo")
            return
        else:
            toast("Inicio de Sesion Exitoso")
            #print(input_correo)
            rueda = coleccion.find({"input_correo":input_correo},{"_id":0,"tipo_usuario":1})
            for usuario in rueda:
                tipo = usuario['tipo_usuario']
            if tipo == "administrador":
                consulta = {"input_correo": input_correo}
                fecha_ini_ses = {"$set": {"ultima_sesion": datetime.now()}}
                coleccion.update_one(consulta, fecha_ini_ses)
                cliente.commit
                self.manager.current = "admin"
            elif tipo == "gestor":
                consulta = {"input_correo": input_correo}
                fecha_ini_ses = {"$set": {"ultima_sesion": datetime.now()}}
                coleccion.update_one(consulta, fecha_ini_ses)
                cliente.commit
                self.manager.current = "gestor"
            elif tipo == "cliente":
                consulta = {"input_correo": input_correo}
                fecha_ini_ses = {"$set": {"ultima_sesion": datetime.now()}}
                coleccion.update_one(consulta, fecha_ini_ses)
                cliente.commit
                self.manager.current = "home"
                app = App.get_running_app()
                bott = app.manager.get_screen('home')
                nav_drawer = bott.ids.nav_drawer
                boton = bott.ids.abrirsidebar
                

    
        

    pass

class Registro(Screen):
        
    def registrar(self):
        
        app = App.get_running_app()
        reg_correo = app.manager.get_screen('reg').ids['reg_correo'].text
        reg_contraseña = app.manager.get_screen('reg').ids['reg_contraseña'].text
        val_contraseña = app.manager.get_screen('reg').ids['val_contraseña'].text
        valida = coleccion.find_one({"input_correo": reg_correo})
        if reg_contraseña != val_contraseña:
            toast("No coinciden las contraseñas, intenta de nuevo")
            return
        if valida != None:
            toast("Ya existe un usuario registrado con ese nombre, intenta nuevamente")
            return
        else:
            
            if reg_contraseña and reg_correo:
                ingresar_datos(reg_correo, reg_contraseña)
                toast ("Registro exitoso, ingresa con tus credenciales")
                consulta = {"input_correo": reg_correo}
                fecha_reg_ses = {"$set": {"reg_sesion": datetime.now()}}
                coleccion.update_one(consulta, fecha_reg_ses)
                self.manager.current = "login"
            else:
                toast ("Fallo al registrar sus credenciales, intentelo nuevamente") 
                return
            
    

    pass



class VentanaPop(Screen):
    nombre = StringProperty()
    tipo = StringProperty()
    source = StringProperty()
    desc = StringProperty()
    precio = NumericProperty(0.0)
    back = StringProperty()
       
    def home(self):
        self.manager.current = "home"
    pass        

    


    

        

    