Sistema de Documentación de Soterrado (Infraestructura IT)

Este proyecto es un software desarrollado en Python, diseñado para gestionar de manera profesional el registro de tareas de tendido de cableado de fibra óptica soterrado.

------ Fundamentos teóricos aplicados --------------

El desarrollo se basa en los conceptos fundamentales de la Unidad 1 del programa:

Naturaleza del Lenguaje: Se utiliza Python, un lenguaje de Alto Nivel que permite enfocarse en la lógica del problema en lugar de los detalles técnicos del hardware. Es un lenguaje interpretado, lo que facilitó la depuración y pruebas inmediatas del código.
Estructura de Algoritmos: Cada funcionalidad (Carga, Modificación, Exportación) sigue la estructura esencial de un algoritmo:
                         Entrada: Recolección de datos del técnico y metros vía consola.
			 Proceso: Validación de datos, actualización de archivos y cálculo de IDs.
			 Salida: Generación de tablas visuales, registros de logs y archivos Excel.

--------- Funciones principales ------------------

1.  Gestión de Tareas: Carga de metros soterrados, técnicos responsables y estado de supervisión.
2.  Modificación con Auditoría: Permite corregir registros existentes, guardando un historial de cambios en un archivo de logs.
3.  Visualización Profesional: Uso de la librería `rich` para mostrar tablas formateadas en consola.
4.  Exportación de Datos: Generación de reportes en formato Excel (`.xlsx`) mediante la librería `openpyxl`.

--------- Estructura ------------------
 - Módulos de código:
main.py - Interfaz de Usuario (CLI): Es el punto de entrada y el Algoritmo de Control. Su única responsabilidad es interactuar con el usuario, mostrar el menú y orquestar las llamadas a las funciones lógicas.

gestor_datos.py - Lógica del Negocio y Persistencia: Módulo propio que gestiona cómo se guardan, leen, modifican y exportan los datos. No tiene interacción directa con el usuario. Contiene los algoritmos clave:_generar_nuevo_id(), guardar_registro(), y el algoritmo de auditoría en modificar_registro().

 - Archivos de Persistencia y ReportesArchivo
registros.csv: Almacenamiento de datos en texto plano. Se eligió CSV por su simplicidad (Zen de Python: "Simple es mejor que complejo") y legibilidad, ideal para un proyecto de este alcance.

reporte_soterrado.xlsx: Archivo de reporte generado bajo demanda por la función exportar_a_excel(). Demuestra la interoperabilidad de Python con herramientas externas.

modificaciones.log: esencial para la trazabilidad y la Integridad de Datos. Registra quién, cuándo y qué se modificó en el sistema (metros y supervisión), cumpliendo con estándares profesionales de seguridad de la información

------- Instalación y Uso ----------

1.  Preparar el entorno virtual:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
2.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ejecutar el programa:
    ```bash
    python main.py
    ```

Estándares de Calidad
PEP 8: Código limpio y legible siguiendo las guías de estilo de Python.
PEP 257: Documentación completa de todas las funciones mediante docstrings.
Modularización: Separación de la lógica de datos (`gestor_datos.py`) de la interfaz de usuario (`main.py`).

---
Desarrollado como Proyecto Final para la materia Programación I - Tecnicatura en Soporte de Infraestructura IT - ISTEA 2025
