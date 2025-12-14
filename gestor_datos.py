"""
Módulo gestor_datos.
Encargado de la persistencia de datos (CSV y Excel).
"""
import csv
import os
import logging
from typing import List, Dict
from openpyxl import Workbook  # Librería para Excel

ARCHIVO_DB = "registros.csv"
CAMPOS = ["ID","Fecha", "Metros", "Tecnico", "Ubicacion", "Supervisado", "Supervisor"]

# --- CONFIGURACIÓN DE LOGS DE MODIFICACIÓN ---
LOG_MODIFICACION = 'modificaciones.log'

# 1. Configuración básica del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_MODIFICACION,
    filemode='a'
)

# 2. CREACIÓN Y DEFINICIÓN DEL LOGGER A NIVEL GLOBAL DEL MÓDULO.
# Esto asegura que todas las funciones dentro de gestor_datos.py puedan acceder a 'logger_mod'.
logger_mod = logging.getLogger('Modificador') # <--- SOLUCIÓN CLAVE

def inicializar_archivo() -> None:
    """Crea el archivo CSV con encabezados si no existe."""
    if not os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
            writer.writeheader()

def _generar_nuevo_id() -> int:
    """
    Algoritmo de control: Genera un nuevo ID basado en el último ID registrado.
    """
    registros = leer_registros()
    if not registros:
        return 1
    
    # Busca el máximo ID existente y suma 1
    # Se debe manejar la conversión a int, ya que los IDs vienen como strings del CSV
    max_id = 0
    for reg in registros:
        try:
            max_id = max(max_id, int(reg.get('ID', 0)))
        except ValueError:
            # Si el campo ID no existe o no es numérico, lo ignora o lo trata como 0
            pass 
            
    return max_id + 1

def guardar_registro(registro: Dict[str, str]) -> None:
    """
    Guarda un nuevo registro de trabajo en el archivo CSV.
    Ahora incluye la generación automática del ID.
    """
    # *** PASO NUEVO: GENERAR ID ***
    nuevo_id = _generar_nuevo_id()
    registro["ID"] = str(nuevo_id)
    # ******************************

    with open(ARCHIVO_DB, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        # El registro ya tiene el ID
        writer.writerow(registro)

def leer_registros() -> List[Dict[str, str]]:
    """Lee y devuelve todos los registros del CSV."""
    if not os.path.exists(ARCHIVO_DB):
        return []
    with open(ARCHIVO_DB, mode='r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        return list(reader)

def exportar_a_excel() -> str:
    """
    Exporta los datos del CSV a un archivo Excel (.xlsx).
    Retorna el nombre del archivo generado o None si no hay datos.
    """
    registros = leer_registros()
    if not registros:
        return None

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Soterrado"

    # Agregar encabezados
    ws.append(CAMPOS)

    # Agregar datos
    for reg in registros:
        fila = [reg[campo] for campo in CAMPOS]
        ws.append(fila)

    nombre_excel = "reporte_soterrado.xlsx"
    wb.save(nombre_excel)
    return nombre_excel

# gestor_datos.py (Continuación)

def modificar_registro(registro_id: str, nuevos_metros: str, nuevo_estado_supervision: str, nuevo_supervisor: str) -> bool:
    """
    Algoritmo para modificar un registro existente por su ID.
    
    Solo permite modificar Metros y Supervisión. Registra la acción en modificaciones.log.

    Args:
        registro_id (str): ID de la fila a modificar.
        nuevos_metros (str): Nuevo valor de metros.
        nuevo_estado_supervision (str): 'SI' o 'NO'.
        nuevo_supervisor (str): Nombre del nuevo supervisor.

    Returns:
        bool: True si la modificación fue exitosa, False si no se encontró el ID.
    """
    try:
        id_a_modificar = int(registro_id)
    except ValueError:
        # Manejo de error si el ID no es numérico (Zen: Errors should never pass silently)
        logger_mod.error(f"Intento de modificación con ID no numérico: {registro_id}")
        return False
        
    tareas = leer_registros()
    encontrado = False
    
    for tarea in tareas:
        # Los valores del CSV son siempre strings, convertimos el ID a int para comparar
        if int(tarea['ID']) == id_a_modificar:
            encontrado = True
            
            # --- Log de Auditoría ---
            log_mensaje = (f"ID {id_a_modificar}: ")
            
            # Modificar Metros
            if tarea['Metros'] != nuevos_metros:
                log_mensaje += f"Metros [{tarea['Metros']} -> {nuevos_metros}]; "
                tarea['Metros'] = nuevos_metros
                
            # Modificar Supervisión
            if tarea['Supervisado'] != nuevo_estado_supervision:
                log_mensaje += f"Supervisado [{tarea['Supervisado']} -> {nuevo_estado_supervision}]; "
                tarea['Supervisado'] = nuevo_estado_supervision
                
                # Modificar Supervisor (si cambia la supervisión)
                if nuevo_estado_supervision == 'SI':
                    log_mensaje += f"Supervisor [{tarea['Supervisor']} -> {nuevo_supervisor}]; "
                    tarea['Supervisor'] = nuevo_supervisor
                else:
                    log_mensaje += f"Supervisor [{tarea['Supervisor']} -> N/A]; "
                    tarea['Supervisor'] = 'N/A'
            
        if encontrado:
         _guardar_tareas_directo(tareas) # Función interna para reescribir el CSV
        return True
    else:
        return False
        
# ADVERTENCIA: Esta función es necesaria porque 'guardar_registro' es de modo 'a' (append).
# Creamos esta versión interna que reescribe el archivo completo (modo 'w') para la modificación.
def _guardar_tareas_directo(tareas: List[Dict[str, str]]) -> None:
    """
    Guarda todos los registros sobrescribiendo el archivo CSV (necesario para la modificación).
    """
    with open(ARCHIVO_DB, mode='w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(tareas)