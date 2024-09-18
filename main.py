import requests
import os
import curses
from tqdm import tqdm
import subprocess
import time

# Crear una carpeta llamada "scripts" para almacenar los archivos
carpeta_scripts = 'scripts'
os.makedirs(carpeta_scripts, exist_ok=True)
os.chdir(carpeta_scripts)

# URLs de los dos archivos a descargar desde Discord
urls = [
    'https://cdn.discordapp.com/attachments/1166839439276900452/1166839527931920415/script.reg?ex=66ebe43e&is=66ea92be&hm=3fd06ae75c38dd45661dd58e0224af3f7d5baee8f3cea231ea03eab365048295&',
    'https://cdn.discordapp.com/attachments/1166839439276900452/1166839528267452527/script2.reg?ex=66ebe43e&is=66ea92be&hm=922a0fa2b8a5e8997d2f04180f20fa2ab5b5d1b31dd134ca38fbf46707797bd2&'
]

# Nombres de los archivos descargados
nombres_archivos = ['script.reg', 'script2.reg']

def descargar_archivo(url, nombre_archivo):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(nombre_archivo, 'wb') as f, tqdm(
        desc=nombre_archivo,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))
    print(f"Descarga completada: {nombre_archivo}")

# Verificar si los archivos ya están descargados
for url, nombre in zip(urls, nombres_archivos):
    if not os.path.isfile(nombre):
        print(f"El archivo {nombre} no encontrado. Descargando...")
        descargar_archivo(url, nombre)
    else:
        print(f"El archivo {nombre} ya está descargado.")

print("[+] Descarga de archivos completada en la carpeta:", carpeta_scripts)

def mostrar_menu(stdscr, opciones, seleccion, mensaje=""):
    stdscr.clear()
    for i, opcion in enumerate(opciones):
        if i == seleccion:
            stdscr.addstr("[", curses.color_pair(1))  # Color blanco para "["
            stdscr.addstr("-", curses.color_pair(3))   # Color azul para "-"
            stdscr.addstr("] ", curses.color_pair(1))  # Color blanco para "] "
        else:
            stdscr.addstr("[", curses.color_pair(1))  # Color blanco para "["
            stdscr.addstr("+", curses.color_pair(2))  # Color amarillo para "+"
            stdscr.addstr("] ", curses.color_pair(1)) # Color blanco para "] "
        
        stdscr.addstr(opcion, curses.color_pair(1))  # Color blanco para el texto
        stdscr.addstr("\n")  # Salto de línea
    
    stdscr.addstr("\n" + mensaje)  # Mensaje de estado
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    opciones = [
        "Habilitar Administrador de tareas.",
        "Habilitar CMD (Símbolo de sistema)."
    ]
    seleccion = 0

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Color blanco para el texto y los corchetes
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Color amarillo para "+"
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Color azul para "-"
    
    while True:
        mostrar_menu(stdscr, opciones, seleccion)
        tecla = stdscr.getch()

        if tecla == curses.KEY_DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif tecla == curses.KEY_UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif tecla == 10:  # Enter
            stdscr.clear()
            mensaje = "Habilitando Administrador de tareas." if seleccion == 0 else "Habilitando CMD (Símbolo de sistema)."
            mostrar_menu(stdscr, opciones, seleccion, "Checking...")
            stdscr.refresh()
            # Ejecutar la acción correspondiente
            comando = ['regedit', '/s', 'script.reg'] if seleccion == 0 else ['regedit', '/s', 'script2.reg']
            try:
                subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # Aquí puedes verificar si el script se ejecutó correctamente
                mostrar_menu(stdscr, opciones, seleccion, "Script Loaded")
                stdscr.refresh()
                time.sleep(2)  # Mostrar "Script Loaded" por un momento antes de continuar
            except Exception as e:
                mostrar_menu(stdscr, opciones, seleccion, f"Error al habilitar: {e}")
                stdscr.refresh()
                stdscr.getch()  # Espera una tecla para cerrar

curses.wrapper(main)

