import clips
from tkinter import Tk, Button, Label, Canvas, messagebox
from PIL import Image, ImageTk
#clipspy
#pillow

ventana_semaforo = Tk()
ventana_semaforo.minsize(width=600, height=600)
ventana_semaforo.config(padx=35, pady=20)
ventana_semaforo.title("Sistema experto - vehículo")


btnIniciar = Button(ventana_semaforo, text="Iniciar", font=("Arial", 14))
btnIniciar.grid(row=0, column=0, ipadx=40)
btnDetener = Button(ventana_semaforo, text="Detener", font=("Arial", 14), state="disabled")
btnDetener.grid(row=0, column=1, ipadx=40)
btnInformacion = Button(ventana_semaforo, text="Información", font=("Arial", 14), bg="lightBlue")
btnInformacion.grid(row=0, column=2, ipadx=40)

btnHeight = 1
btnWidth = 6

lblSemaforo = Label(text="Semaforo", font=("Arial", 14))
lblSemaforo.grid(row=1, column=0)
lblSemaforo = Label(text="Acciones", font=("Arial", 14))
lblSemaforo.grid(row=2, column=0, pady=20)
btnAvanzarVehiculo = Button(ventana_semaforo, text="Avanzar", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnAvanzarVehiculo.grid(row=3, column=0, ipadx=40)
btnDetenerVehiculo = Button(ventana_semaforo, text="Detener", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnDetenerVehiculo.grid(row=3, column=1, ipadx=40)
btnGirarDerecha = Button(ventana_semaforo, text="Girar Derecha", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnGirarDerecha.grid(row=4, column=0, ipadx=40)
btnGirarIzquierda = Button(ventana_semaforo, text="Girar Izquierda", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnGirarIzquierda.grid(row=4, column=1, ipadx=40)
ventana_semaforo.rowconfigure(5, minsize=20)
btnProcesar = Button(ventana_semaforo, text="Procesar", font=("Arial", 14), height=btnHeight, width=btnWidth, bg="lightblue")
btnProcesar.grid(row=6, column=0, ipadx=40)
ventana_semaforo.rowconfigure(7, minsize=40)
lblResultado = Label(text="Resultado", font=("Arial", 14))
lblResultado.grid(row=8, column=0)
ventana_semaforo.rowconfigure(9, minsize=20)
btnDireccionalDerecha = Button(ventana_semaforo, text="DR", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnDireccionalDerecha.grid(row=10, column=0, ipadx=40)
btnEstadoVehiculo = Button(ventana_semaforo, text="Estado vehículo", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnEstadoVehiculo.grid(row=10, column=1, ipadx=40)
btnDireccionalIzquierda = Button(ventana_semaforo, text="DI", font=("Arial", 14), height=btnHeight, width=btnWidth)
btnDireccionalIzquierda.grid(row=10 , column=2, ipadx=40)

sistemaExperto = clips.Environment()
sistemaExperto.clear()

def definir_reglas():
    sistemaExperto.build("(deftemplate vehiculo (slot estado_vehiculo (type STRING)))")
    sistemaExperto.build("(deftemplate direccional (slot estado_direccional (type STRING)))")
    sistemaExperto.build("(deftemplate semaforo (slot estado_semaforo (type STRING)))")

    sistemaExperto.build('(defrule regla1(iniciar) => (assert(vehiculo (estado_vehiculo "avanzar"))))')
    sistemaExperto.build('(defrule regla2(and (vehiculo (estado_vehiculo "avanzar"))(semaforo (estado_semaforo "rojo"))) => (assert(vehiculo (estado_vehiculo "detener"))))')
    sistemaExperto.build('(defrule regla3(and (vehiculo (estado_vehiculo "avanzar"))(semaforo (estado_semaforo "amarillo"))) => (assert(vehiculo (estado_vehiculo "disminuir velocidad"))))')
    sistemaExperto.build('(defrule regla4(semaforo (estado_semaforo "verde")) => (assert(vehiculo (estado_vehiculo "avanzar"))))')
    sistemaExperto.build('(defrule regla5(girarDerecha) => (assert(direccional (estado_direccional "encender derecha"))) (assert(vehiculo (estado_vehiculo "Girando derecha"))))')
    sistemaExperto.build('(defrule regla6(girarIzquierda) => (assert(direccional (estado_direccional "encender izquierda"))) (assert(vehiculo (estado_vehiculo "Girando izquierda"))))')
    sistemaExperto.build('(defrule regla7(and (vehiculo (estado_vehiculo "avanzar"))(direccional (estado_direccional "encender derecha"))) => (assert(vehiculo (estado_vehiculo "Girando derecha"))))')
    sistemaExperto.build('(defrule regla8(and (vehiculo (estado_vehiculo "avanzar"))(direccional (estado_direccional "encender izquierda"))) => (assert(vehiculo (estado_vehiculo "Girando izquierda"))))')
    sistemaExperto.build('(defrule regla9(detener) => (assert(vehiculo (estado_vehiculo "detener"))))')
    sistemaExperto.build('(defrule regla10(vehiculo (estado_vehiculo "detener")) => (assert(direccional (estado_direccional "intermitente"))))')

def ver_reglas():
    for ac in sistemaExperto.activations():
        print(ac)

btnVer = Button(ventana_semaforo, text="Ver Reglas", font=("Arial", 14), height=btnHeight, width=btnWidth, bg="lightblue", command=ver_reglas)
btnVer.grid(row=6, column=1, ipadx=40)

def procesar_facts():
    sistemaExperto.run()
    btnDireccionalDerecha.config(bg="SystemButtonFace")
    btnDireccionalIzquierda.config(bg="SystemButtonFace")
    btnEstadoVehiculo.config(bg="SystemButtonFace")
    btnDireccionalDerecha.config(bg="SystemButtonFace")
    btnDireccionalIzquierda.config(bg="SystemButtonFace")
    for fact in sistemaExperto.facts():
        if fact.template.name == "vehiculo":            
            if fact['estado_vehiculo'] == "avanzar":
                btnEstadoVehiculo.config(bg="green", text="Avanzando")
            elif fact['estado_vehiculo'] == "detener":
                btnEstadoVehiculo.config(bg="red", text="Detenido")
            elif fact['estado_vehiculo'] == "disminuir velocidad":
                btnEstadoVehiculo.config(bg="yellow", text="Disminuyendo velocidad")
            elif fact['estado_vehiculo'] == "Girando derecha":
                btnEstadoVehiculo.config(bg="blue", text="Girando derecha")
                sistemaExperto.assert_string('(iniciar)')
            elif fact['estado_vehiculo'] == "Girando izquierda":
                btnEstadoVehiculo.config(bg="blue", text="Girando izquierda")
                sistemaExperto.assert_string('(iniciar)')
        elif fact.template.name == "semaforo":
            print(f"Semaforo: {fact['estado_semaforo']}")
        elif fact.template.name == "direccional":            
            if fact['estado_direccional'] == "encender derecha":
                btnDireccionalDerecha.config(bg="yellow")
                print("El direccional derecho está encendido")
            elif fact['estado_direccional'] == "encender izquierda":
                btnDireccionalIzquierda.config(bg="yellow")
                print("El direccional izquierdo está encendido")
            elif fact['estado_direccional'] == "intermitente":
                btnDireccionalDerecha.config(bg="yellow")
                btnDireccionalIzquierda.config(bg="yellow")
                print("El direccional está en intermitente")
    sistemaExperto.reset()

def iniciar():
    btnIniciar.config(state="disabled")
    btnDetener.config(state="normal")
    sistemaExperto.assert_string('(iniciar)')
    procesar_facts()
    print("Sistema iniciado")

def detener():
    btnIniciar.config(state="normal")
    btnDetener.config(state="disabled")
    btnEstadoVehiculo.config(bg="SystemButtonFace", text="Estado vehículo")
    btnDireccionalDerecha.config(bg="SystemButtonFace")
    btnDireccionalIzquierda.config(bg="SystemButtonFace")
    procesar_facts()
    print("Sistema detenido")

def semaforo_evento(event):
    canvas_widget = event.widget
    items_clicados = canvas_widget.find_withtag("current")
    if items_clicados:
        etiquetas = canvas_widget.gettags(items_clicados[0])
        sistemaExperto.assert_string(f'(semaforo (estado_semaforo "{etiquetas[0]}")))')

def vehiculo_estado(estado):
    sistemaExperto.assert_string(f'(vehiculo (estado_vehiculo "{estado}")))')

def funcion_assert(comando):
    sistemaExperto.assert_string(f'({comando})')

def mensaje_informacion():
    messagebox.showinfo("Información proyecto vehículo", "Para el desarrollo del juego es necesario que indique la acción a realizar, luego indicar el semaforo si lo requiere y luego dar clic en procesar.")

canvas = Canvas(ventana_semaforo, width=300, height=100)
canvas.grid(row=1, column=1)
# Dimensiones del círculo
diametro = 50
separacion_horizontal = 60
# Coordenadas círculo rojo
x1_rojo = 15
y1_rojo = 15
x2_rojo = x1_rojo + diametro
y2_rojo = y1_rojo + diametro
# Coordenadas círculo amarillo
x1_amarillo = x1_rojo + separacion_horizontal
y1_amarillo = y1_rojo
x2_amarillo = x2_rojo + separacion_horizontal
y2_amarillo = y2_rojo
# Coordenadas círculo verde
x1_verde = x1_rojo + 2 * separacion_horizontal
y1_verde = y1_rojo
x2_verde = x2_rojo + 2 * separacion_horizontal
y2_verde = y2_rojo
circulo_rojo = canvas.create_oval(x1_rojo, y1_rojo, x2_rojo, y2_rojo, fill="red", outline="", tags="rojo")
circulo_amarillo = canvas.create_oval(x1_amarillo, y1_amarillo, x2_amarillo, y2_amarillo, fill="yellow", outline="", tags="amarillo")
circulo_verde = canvas.create_oval(x1_verde, y1_verde, x2_verde, y2_verde, fill="green", outline="", tags="verde")

canvas.tag_bind("all", "<Button-1>", semaforo_evento)
btnIniciar.config(command=iniciar)
btnDetener.config(command=detener)
btnProcesar.config(command=procesar_facts)
btnAvanzarVehiculo.config(command=lambda:vehiculo_estado("avanzar"))
btnDetenerVehiculo.config(command=lambda: vehiculo_estado("detener"))
btnGirarDerecha.config(command=lambda: funcion_assert("girarDerecha"))
btnGirarIzquierda.config(command=lambda: funcion_assert("girarIzquierda"))
btnInformacion.config(command=mensaje_informacion)

definir_reglas()

ventana_semaforo.mainloop()