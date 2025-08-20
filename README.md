# Importamos tkinter y sus módulos necesarios
import tkinter as tk
from tkinter import ttk, messagebox

# ============================
# FUNCIONES PRINCIPALES
# ============================

# Función que ajusta el número según el sistema numérico elegido
def ajustar_valor(valor, base):
    if base == "Binario":
        # Rellenar con ceros a la izquierda para múltiplos de 4 bits
        return valor.zfill(((len(valor) + 3) // 4) * 4)
    elif base == "Octal":
        # Rellenar a múltiplos de 3 dígitos
        return valor.zfill(((len(valor) + 2) // 3) * 3)
    elif base == "Hexadecimal":
        # Rellenar a múltiplos de 2 dígitos
        return valor.zfill(((len(valor) + 1) // 2) * 2)
    return valor  # En decimal no se rellena


# Función para convertir el valor ingresado
def convertir(event=None):
    valor = entrada.get().strip()
    base_nombre = tipo_sistema.get()

    if not valor:
        messagebox.showwarning("Advertencia", "Ingrese un número.")
        return

    try:
        negativo = valor.startswith("-")
        if negativo:
            valor = valor[1:]  # Quitar el "-" temporalmente

        # Verificación y conversión según el sistema elegido
        if base_nombre == "Binario":
            if not all(c in "01" for c in valor):
                raise ValueError
            valor = ajustar_valor(valor, "Binario")
            decimal = int(valor, 2)

        elif base_nombre == "Octal":
            if not all(c in "01234567" for c in valor):
                raise ValueError
            valor = ajustar_valor(valor, "Octal")
            decimal = int(valor, 8)

        elif base_nombre == "Decimal":
            if not valor.isdigit():
                raise ValueError
            decimal = int(valor, 10)

        elif base_nombre == "Hexadecimal":
            if not all(c.upper() in "0123456789ABCDEF" for c in valor):
                raise ValueError
            valor = ajustar_valor(valor, "Hexadecimal")
            decimal = int(valor, 16)

        else:
            messagebox.showerror("Error", "Seleccione un sistema.")
            return

        # Si el número era negativo, se aplica el signo
        if negativo:
            decimal = -decimal
            valor = "-" + valor

        # Actualizamos la entrada con el valor ajustado
        entrada.delete(0, tk.END)
        entrada.insert(0, valor)

        # Mostramos resultados
        resultado.set(
            f"Binario: {bin(decimal)}\n"
            f"Octal: {oct(decimal)}\n"
            f"Decimal: {decimal}\n"
            f"Hexadecimal: {hex(decimal).upper()}"
        )

    except ValueError:
        messagebox.showerror("Error", f"El valor ingresado no es válido para {base_nombre}.")


# Función que borra entrada y resultados
def limpiar():
    entrada.delete(0, tk.END)
    resultado.set("")


# Función que copia el resultado al portapapeles
def copiar_resultado():
    ventana.clipboard_clear()
    ventana.clipboard_append(resultado.get())
    ventana.update()
    messagebox.showinfo("Copiado", "Resultado copiado al portapapeles.")


# ============================
# INTERFAZ GRÁFICA
# ============================

ventana = tk.Tk()
ventana.title("Conversión Numérica")
ventana.geometry("360x640")  # tamaño tipo app móvil
ventana.configure(bg="white")
ventana.resizable(False, False)

# Fuentes
fuente_label = ("Arial", 13)
fuente_boton = ("Consolas", 12)
fuente_resultado = ("Arial", 13, "bold")

# Entrada de número
lbl_entrada = tk.Label(ventana, text="Ingrese un número:", bg="white", font=fuente_label)
lbl_entrada.pack(anchor="w", padx=20, pady=(20, 5))

entrada = tk.Entry(ventana, font=("Arial", 14), relief="solid", bd=2, justify="center")
entrada.pack(fill="x", padx=20, pady=5, ipady=8)

# Selección de sistema
lbl_sistema = tk.Label(ventana, text="Seleccione el sistema:", bg="white", font=fuente_label)
lbl_sistema.pack(anchor="w", padx=20, pady=(20, 5))

tipo_sistema = ttk.Combobox(
    ventana,
    values=["Binario", "Octal", "Decimal", "Hexadecimal"],
    state="readonly",
    font=("Arial", 13),
    justify="center"
)
tipo_sistema.pack(padx=20, pady=5, fill="x", ipady=5)
tipo_sistema.set("Decimal")  # valor por defecto

# Botones
boton_calcular = tk.Button(
    ventana, text="Calcular", command=convertir,
    bg="#4CAF50", fg="white", font=fuente_boton, height=2
)
boton_calcular.pack(fill="x", padx=40, pady=10)

boton_limpiar = tk.Button(
    ventana, text="Limpiar", command=limpiar,
    bg="#f44336", fg="white", font=fuente_boton, height=2
)
boton_limpiar.pack(fill="x", padx=40, pady=10)

boton_copiar = tk.Button(
    ventana, text="Copiar", command=copiar_resultado,
    bg="#2196F3", fg="white", font=fuente_boton, height=2
)
boton_copiar.pack(fill="x", padx=40, pady=10)

boton_salir = tk.Button(
    ventana, text="Salir", command=ventana.destroy,
    bg="#9C27B0", fg="white", font=fuente_boton, height=2
)
boton_salir.pack(fill="x", padx=40, pady=10)

# Resultados
lbl_resultados = tk.Label(ventana, text="Resultados:", bg="white", font=fuente_label)
lbl_resultados.pack(anchor="w", padx=20, pady=(20, 5))

resultado = tk.StringVar()
txt_resultado = tk.Label(
    ventana, textvariable=resultado, justify="left",
    font=fuente_resultado, bg="#f9f9f9", relief="ridge",
    bd=2, anchor="nw", width=40, height=8
)
txt_resultado.pack(padx=20, pady=5, fill="both")

# Atajo de teclado
ventana.bind("<Return>", convertir)

# Iniciar aplicación
ventana.mainloop()
