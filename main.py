"""
Programa Principal - Documentación de Soterrado.
Interfaz de consola con Rich, Art y OpenPyXL.
"""
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from art import tprint
import gestor_datos

console = Console()

def mostrar_encabezado():
    """Limpia pantalla y muestra el logo."""
    console.clear()
    console.print("[bold cyan]SISTEMA DE INFRAESTRUCTURA[/bold cyan]")
    tprint("SOTERRADO", font="block")
    console.print("[italic dim]v1.1 - Con exportación a Excel[/italic dim]\n")

def solicitar_datos():
    """Pide datos al usuario y los guarda."""
    console.print("[bold yellow]--- Nuevo Registro de Tarea ---[/bold yellow]")
    
    while True:
        try:
            metros_str = Prompt.ask("Cantidad de metros soterrados")
            metros = float(metros_str)
            if metros <= 0:
                raise ValueError("Debe ser positivo")
            break
        except ValueError:
            console.print("[red]Error: Ingrese un número válido mayor a 0.[/red]")

    tecnico = Prompt.ask("Nombre del Técnico")
    ubicacion = Prompt.ask("Barrio-Lote")
    es_supervisado = Confirm.ask("¿La tarea fue supervisada?")
    
    nombre_supervisor = "N/A"
    if es_supervisado:
        nombre_supervisor = Prompt.ask("Nombre del Supervisor")

    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    nuevo_registro = {
        "Fecha": fecha_hoy,
        "Metros": str(metros),
        "Tecnico": tecnico,
        "Ubicacion": ubicacion,
        "Supervisado": "SI" if es_supervisado else "NO",
        "Supervisor": nombre_supervisor
    }

    gestor_datos.guardar_registro(nuevo_registro)
    console.print(f"\n[bold green]✔ Registro guardado exitosamente.[/bold green]")

def ver_tabla():
    """
    Visualiza los datos cargados utilizando una tabla de Rich.
    """
    registros = gestor_datos.leer_registros()
    
    if not registros:
        console.print("\n[red]No hay registros cargados aún.[/red]")
        return

    # Creación de tabla con Rich (Librería externa 2)
    tabla = Table(title="Historial de Soterrado")

    # [NUEVA LÍNEA] AGREGAMOS LA COLUMNA ID AL PRINCIPIO
    tabla.add_column("ID", style="bold yellow", no_wrap=True)
    
    tabla.add_column("Fecha", style="cyan", no_wrap=True)
    tabla.add_column("Metros", justify="right", style="magenta")
    tabla.add_column("Técnico", style="green")
    tabla.add_column("Ubicación", style="white")
    tabla.add_column("Supervisado", justify="center")
    tabla.add_column("Supervisor", style="blue")

    for reg in registros:
        # Colorear condicionalmente si está supervisado o no
        color_sup = "green" if reg.get("Supervisado") == "SI" else "red"
        
        # [MODIFICACIÓN CLAVE] AHORA LEEMOS reg["ID"]
        tabla.add_row(
            reg.get("ID", "?"),  # Obtenemos el ID
            reg.get("Fecha", "N/A"),
            f"{reg.get('Metros', '0')} m",
            reg.get("Tecnico", "N/A"),
            reg.get("Ubicacion", "N/A"),
            f"[{color_sup}]{reg.get('Supervisado', 'NO')}[/{color_sup}]",
            reg.get("Supervisor", "N/A")
        )

    console.print(tabla)

def exportar_datos():
    """Maneja la exportación a Excel desde el menú."""
    console.print("[yellow]Generando archivo Excel...[/yellow]")
    try:
        archivo = gestor_datos.exportar_a_excel()
        if archivo:
            console.print(f"[bold green]¡Éxito! Datos exportados a: {archivo}[/bold green]")
        else:
            console.print("[red]No hay datos para exportar. Cargue tareas primero.[/red]")
    except Exception as e:
        console.print(f"[bold red]Error al exportar:[/bold red] {e}")


def modificar_datos():
    """Solicita el ID y los nuevos datos para modificar una tarea."""
    console.print(f"\n[bold yellow]--- MODIFICAR REGISTRO ---[/bold yellow]")
    
    ver_tabla()
    
    registro_id = Prompt.ask("Ingrese el ID del registro a modificar")
    
    # 1. Validación de Metros
    while True:
        try:
            nuevos_metros_str = Prompt.ask("Nuevos metros soterrados")
            nuevos_metros = float(nuevos_metros_str)
            if nuevos_metros <= 0:
                raise ValueError("Debe ser mayor a 0")
            break
        except ValueError:
            console.print("[red]Error: Ingrese un número válido positivo para metros.[/red]")
            
    # 2. Validación de Supervisión
    es_supervisado = Confirm.ask("¿La tarea fue supervisada (SI/NO)?")
    nuevo_estado_supervision = "SI" if es_supervisado else "NO"
    
    nombre_supervisor = "N/A"
    if es_supervisado:
        nombre_supervisor = Prompt.ask("Nombre del nuevo Supervisor")
    
    # Llamamos al algoritmo de modificación
    exito = gestor_datos.modificar_registro(
        registro_id, 
        str(nuevos_metros), 
        nuevo_estado_supervision, 
        nombre_supervisor
    )
    
    if exito:
        console.print(f"\n[bold green]El registro ID {registro_id} ha sido modificado.[/bold green]")
        console.print(f"[bold magenta]Revise el archivo 'modificaciones.log' para la auditoría.[/bold magenta]")
    else:
        console.print(f"\n[bold red]ERROR: No se encontró el registro ID {registro_id}.[/bold red]")

def main():
    """Bucle principal del programa."""
    gestor_datos.inicializar_archivo()
    
    while True:
        mostrar_encabezado()
        console.print("1. [bold green]Agregar[/bold green] tarea de soterrado")
        console.print("2. [bold blue]Ver[/bold blue] tabla de registros")
        console.print("3. [bold yellow]Modificar[/bold yellow] registro")
        console.print("4. [bold magenta]Exportar[/bold magenta] a Excel (.xlsx)")
        console.print("5. [bold red]Salir[/bold red]") 
        
        
        opcion = Prompt.ask("\nSeleccione una opción", choices=["1", "2", "3", "4", "5"])

        if opcion == "1":
            solicitar_datos()
            Prompt.ask("\nPresione Enter para continuar...")
        elif opcion == "2":
            ver_tabla()
            Prompt.ask("\nPresione Enter para continuar...")
        elif opcion == "3": 
            modificar_datos()
            Prompt.ask("\nPresione Enter para continuar...")
        elif opcion == "4":
            exportar_datos()
            Prompt.ask("\nPresione Enter para continuar...")
        elif opcion == "5":
            console.print("[bold]¡Hasta luego! Mantén la infraestructura segura.[/bold] 👋")
            break

if __name__ == "__main__":
    main()