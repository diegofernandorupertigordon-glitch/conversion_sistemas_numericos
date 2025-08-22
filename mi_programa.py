import tkinter as tk
from tkinter import ttk, messagebox

# ============================
# FUNCIONES PRINCIPALES
# ============================

def ajustar_valor(valor, base):
    if base == "Binario":
        return valor.zfill(((len(valor) + 3) // 4) * 4)
    elif base == "Octal":
        return valor.zfill(((len(valor) + 2) // 3) * 3)
    elif base == "Hexadecimal":
        return valor.zfill(((len(valor) + 1) // 2) * 2)
    return valor

def convertir(event=None):
    valor = entrada.get().strip()
    base_nombre = tipo_sistema.get()

    if not valor:
        messagebox.showwarning("Advertencia", "Ingrese un número.")
        return

    try:
        negativo = valor.startswith("-")
        if negativo:
            valor = valor[1:]

        valor_original = valor  # Guardamos el valor original para comparar

        if base_nombre == "Binario":
            if not all(c in "01" for c in valor):
                raise ValueError
            valor = ajustar_valor(valor, "Binario")
            decimal = int(valor, 2)

        elif base_nombre == "Octal":
            # Si no es octal puro, intentar como decimal
            if not all(c in "01234567" for c in valor):
                decimal_temp = int(valor)
                valor = oct(decimal_temp)[2:]
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

        if negativo:
            decimal = -decimal
            valor = "-" + valor

        # Mensaje personalizado por sistema si hubo corrección
        if valor != valor_original:
            messagebox.showinfo(
                "Ajuste automático",
                f"El número en {base_nombre} fue corregido a: {valor}"
            )

        entrada.delete(0, tk.END)
        entrada.insert(0, valor)

        resultado.set(
            f"Binario: {bin(decimal)[2:]}\n"
            f"Octal: {oct(decimal)[2:]}\n"
            f"Decimal: {decimal}\n"
            f"Hexadecimal: {hex(decimal)[2:].upper()}"
        )

    except ValueError:
        messagebox.showerror("Error", f"El valor ingresado no es válido para {base_nombre}.")

def limpiar():
    entrada.delete(0, tk.END)
    resultado.set("")

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
ventana.geometry("360x640")
ventana.configure(bg="white")
ventana.resizable(False, False)

# 🎨 Estilos modernos con ttk.Style
style = ttk.Style(ventana)
style.theme_use("clam")

style.configure("TLabel", background="white", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=10)
style.map("TButton",
          background=[("active", "#1976D2")],
          foreground=[("active", "white")])

style.configure("TEntry", padding=5, relief="flat", font=("Segoe UI", 13))
style.configure("TCombobox", font=("Segoe UI", 12), padding=5)

# ============================
# WIDGETS
# ============================

lbl_entrada = ttk.Label(ventana, text="Ingrese un número:")
lbl_entrada.pack(anchor="w", padx=20, pady=(20, 5))

entrada = ttk.Entry(ventana, justify="center")
entrada.pack(fill="x", padx=20, pady=5, ipady=5)

lbl_sistema = ttk.Label(ventana, text="Seleccione el sistema:")
lbl_sistema.pack(anchor="w", padx=20, pady=(20, 5))

tipo_sistema = ttk.Combobox(
    ventana,
    values=["Binario", "Octal", "Decimal", "Hexadecimal"],
    state="readonly",
    justify="center"
)
tipo_sistema.pack(padx=20, pady=5, fill="x")
tipo_sistema.set("Decimal")

# 🔘 Botones con colores personalizados
btn_frame = tk.Frame(ventana, bg="white")
btn_frame.pack(pady=20, fill="x")

boton_calcular = ttk.Button(btn_frame, text="Calcular", command=convertir)
boton_calcular.pack(fill="x", padx=40, pady=5)

boton_limpiar = ttk.Button(btn_frame, text="Limpiar", command=limpiar)
boton_limpiar.pack(fill="x", padx=40, pady=5)

boton_copiar = ttk.Button(btn_frame, text="Copiar", command=copiar_resultado)
boton_copiar.pack(fill="x", padx=40, pady=5)

boton_salir = ttk.Button(btn_frame, text="Salir", command=ventana.destroy)
boton_salir.pack(fill="x", padx=40, pady=5)

lbl_resultados = ttk.Label(ventana, text="Resultados:")
lbl_resultados.pack(anchor="w", padx=20, pady=(20, 5))

resultado = tk.StringVar()
txt_resultado = tk.Text(
    ventana, font=("Consolas", 12), bg="#F4F6F7",
    relief="flat", height=10, wrap="word"
)
txt_resultado.pack(padx=20, pady=5, fill="both")

# Vincular StringVar al Text
def actualizar_resultado(*args):
    txt_resultado.delete("1.0", tk.END)
    txt_resultado.insert(tk.END, resultado.get())

resultado.trace_add("write", actualizar_resultado)

# Atajo de teclado
ventana.bind("<Return>", convertir)

ventana.mainloop()
