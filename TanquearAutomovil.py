import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Frame, Spinbox, Entry
from PIL import Image, ImageTk

#Creando ventana
ventana_tanquear = Tk()
ventana_tanquear.minsize(width=600, height=500)
ventana_tanquear.config(padx=35, pady=20)
ventana_tanquear.title("Logíca difusa - Tanquear vehículo")

btnHeight = 1
btnWidth = 15

lblTitulo = Label(text="Tanqueo de Vehículo", font=("Arial", 14))
lblTitulo.pack(pady=10)
#lblTitulo.grid(row=0, column=1)
lblVerGraficas = Label(text="Visualizar gráficas de las variables", font=("Arial", 14))
lblVerGraficas.pack(pady=10)

frame_botones = Label(ventana_tanquear)
frame_botones.pack(pady=5)

btnVerGraficaCombustible = Button(frame_botones, text="Nivel Combustible", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnVerGraficaCombustible.grid(row=0, column=0, padx=5)
btnVerGraficaGasolinera = Button(frame_botones, text="Dist. Gasolinera", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnVerGraficaGasolinera.grid(row=0, column=1, padx=5)
btnVerGraficaResultado = Button(frame_botones, text="Resultado", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnVerGraficaResultado.grid(row=0, column=2, padx=5)

# Frame para agrupar imagen y controles
contenedor_nivel_gasolina = Frame(ventana_tanquear)
contenedor_nivel_gasolina.pack(pady=20)

# Imagen
img_pil = Image.open("recursos/medidor.avif")
img_pil = img_pil.resize((100, 100))
img_tk = ImageTk.PhotoImage(img_pil)
label_imagen = Label(contenedor_nivel_gasolina, image=img_tk, bd=1, relief="solid")
label_imagen.grid(row=0, column=0, rowspan=2, padx=10)
label_imagen.image = img_tk

lblSelecciona = Label(contenedor_nivel_gasolina, text="Selecciona el nivel de combustible", font=("Arial", 14))
lblSelecciona.grid(row=0, column=1, sticky="w", pady=(40,0))
nivel_gasolina = Spinbox(contenedor_nivel_gasolina, from_=0, to=11, font=("Arial", 14), width=15)
nivel_gasolina.grid(row=1, column=1, sticky="w", pady=(5,0))

nivel_combustible = ctrl.Antecedent(np.arange(0, 11, 1), 'nivel_combustible')
distancia_gasolinera = ctrl.Antecedent(np.arange(0, 500, 1), 'distancia_gasolinera')
resultado = ctrl.Consequent(np.arange(0, 10, 1), 'resultado')


label_kilometros = Label(ventana_tanquear, text="Distancia a la gasolinera (km)", font=("Arial", 14))
label_kilometros.pack(pady=(10, 0))
campo_distancia = Entry(ventana_tanquear, font=("Arial", 14), width=btnWidth)
campo_distancia.pack(pady=(10, 0))

btnProcesar = Button(ventana_tanquear, text="Procesar", font=("Arial", 14), bg="green", height=btnHeight, width=btnWidth)
btnProcesar.pack(pady=(20, 0))

def iniciar_tanqueo():
    nivel_combustible['bajo'] = fuzz.trapmf(nivel_combustible.universe, [0, 0, 2, 3])
    nivel_combustible['medio'] = fuzz.trapmf(nivel_combustible.universe, [2.5, 3.5, 8, 9])
    nivel_combustible['alto'] = fuzz.trapmf(nivel_combustible.universe, [8.5, 9.5, 11, 11])

    distancia_gasolinera['muy_cerca'] = fuzz.trapmf(distancia_gasolinera.universe, [0, 0, 5, 15])
    distancia_gasolinera['cerca'] = fuzz.trapmf(distancia_gasolinera.universe, [13, 18, 80, 100])
    distancia_gasolinera['media'] = fuzz.trapmf(distancia_gasolinera.universe, [90, 110, 220, 220])
    distancia_gasolinera['lejos'] = fuzz.trapmf(distancia_gasolinera.universe, [210, 230, 310, 350])
    distancia_gasolinera['muy_lejos'] = fuzz.trapmf(distancia_gasolinera.universe, [340, 360, 500, 500])

    resultado['grua'] = fuzz.trimf(resultado.universe, [0, 0, 3])
    resultado['llega'] = fuzz.trimf(resultado.universe, [2, 5, 8])
    resultado['llega_sin_problema'] = fuzz.trimf(resultado.universe, [7, 10, 10])
    print("Iniciando el sistema de tanques de automóviles...")

def visualizar_graficas(tipo):
    if tipo == 1:
        nivel_combustible.view()
    elif tipo == 2:
        distancia_gasolinera.view()
    elif tipo == 3:
        resultado.view()

def procesar_tanqueo():
    distancia = float(campo_distancia.get())
    nivel = float(nivel_gasolina.get())
    tanquear_sim.input['nivel_combustible'] = nivel
    tanquear_sim.input['distancia_gasolinera'] = distancia
    tanquear_sim.compute()
    resultado_final = tanquear_sim.output['resultado']
    print(f"Resultado del tanquero: {resultado_final}")
    resultado.view(sim=tanquear_sim)
    plt.show()

iniciar_tanqueo()

regla1 = ctrl.Rule(nivel_combustible['bajo'] & distancia_gasolinera['muy_cerca'], resultado['llega_sin_problema'])
regla2 = ctrl.Rule(nivel_combustible['bajo'] & distancia_gasolinera['cerca'], resultado['llega'])
regla3 = ctrl.Rule(nivel_combustible['bajo'] & distancia_gasolinera['media'], resultado['grua'])
regla4 = ctrl.Rule(nivel_combustible['bajo'] & distancia_gasolinera['lejos'], resultado['grua'])
regla5 = ctrl.Rule(nivel_combustible['bajo'] & distancia_gasolinera['muy_lejos'], resultado['grua'])
regla6 = ctrl.Rule(nivel_combustible['medio'] & distancia_gasolinera['muy_cerca'], resultado['llega_sin_problema'])
regla7 = ctrl.Rule(nivel_combustible['medio'] & distancia_gasolinera['cerca'], resultado['llega_sin_problema'])
regla8 = ctrl.Rule(nivel_combustible['medio'] & distancia_gasolinera['media'], resultado['llega'])
regla9 = ctrl.Rule(nivel_combustible['medio'] & distancia_gasolinera['lejos'], resultado['llega'])
regla10 = ctrl.Rule(nivel_combustible['medio'] & distancia_gasolinera['muy_lejos'], resultado['grua'])
regla11 = ctrl.Rule(nivel_combustible['alto'] & distancia_gasolinera['muy_cerca'], resultado['llega_sin_problema'])
regla12 = ctrl.Rule(nivel_combustible['alto'] & distancia_gasolinera['cerca'], resultado['llega_sin_problema'])
regla13 = ctrl.Rule(nivel_combustible['alto'] & distancia_gasolinera['media'], resultado['llega'])
regla14 = ctrl.Rule(nivel_combustible['alto'] & distancia_gasolinera['lejos'], resultado['llega'])
regla15 = ctrl.Rule(nivel_combustible['alto'] & distancia_gasolinera['muy_lejos'], resultado['grua'])

tanquear_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10, regla11, regla12, regla13, regla14, regla15])
tanquear_sim = ctrl.ControlSystemSimulation(tanquear_ctrl)

btnVerGraficaCombustible.config(command=lambda: visualizar_graficas(1))
btnVerGraficaGasolinera.config(command=lambda: visualizar_graficas(2))
btnVerGraficaResultado.config(command=lambda: visualizar_graficas(3))
btnProcesar.config(command=procesar_tanqueo)

ventana_tanquear.mainloop()