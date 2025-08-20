REM -----------------------------
REM Script para generar .exe con ícono para Conversion_Sistemas_Numericos.py
REM -----------------------------

REM 1️⃣ Cambiar a la carpeta del proyecto
cd "D:\Familia\Diego\ITECSUR\Tareas Itecsur\Deberes Electronica\Examen_Convesion_Sistemas_Numericos"

REM 2️⃣ Renombrar archivo para quitar espacios
rename "Conversion_Sistemas Numericos.py" Conversion_Sistemas_Numericos.py

REM 3️⃣ Verificar que el ícono existe
if not exist "mi_icono.ico" (
    echo ⚠️ No se encontró el archivo mi_icono.ico
    echo El .exe se generará sin ícono.
    pyinstaller --onefile --windowed "Conversion_Sistemas_Numericos.py"
) else (
    REM 4️⃣ Generar ejecutable con PyInstaller y el ícono
    pyinstaller --onefile --windowed --icon=mi_icono.ico "Conversion_Sistemas_Numericos.py"
)

REM 5️⃣ Mensaje de finalización
echo ===============================
echo .exe generado correctamente en la carpeta dist\
echo ===============================
pause