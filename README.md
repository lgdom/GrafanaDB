# README: Extracción de Fallas y Conversión a Line Protocol

## Instrucciones de Uso

Este repositorio contiene los elementos necesarios para que el código de extracción de fallas y conversión a Line Protocol funcione correctamente, permitiendo al usuario actualizar las extracciones en caso de continuar con el uso del Dashboard de Fallas de BRAUMAT.

### Requisitos Principales

#### 1. **Extracción de BRAUMAT**
Los datos descargados de BRAUMAT deben generarse como documentos CSV, obteniendo un archivo por cada host. Cada archivo debe seguir esta nomenclatura específica:

IOS01.csv, IOS03.csv, IOS05.csv, IOS07.csv, IOS09.csv


Es crucial respetar esta nomenclatura, ya que cualquier desviación impedirá que el código funcione correctamente.

#### 2. **Archivo: MATRIZ**
Este archivo en formato `.csv` contiene información que el código utiliza para organizar y complementar los datos de manera automática.

- **Ubicación**: Coloque el archivo `MATRIZ` en la misma ruta donde esté ejecutando el script Python (`.py`) o la libreta Jupyter (`.ipynb`).
- **Errores relacionados**: Si encuentra errores relacionados a este archivo, asegúrese de especificar correctamente la ruta.

#### 3. **Archivo: EXCEPCIONES**
Este archivo de texto contiene una lista de TAGs que no deben incluirse en la extracción. Algunas de las razones comunes para excluir ciertos TAGs son:

- TAGs con órdenes de mantenimiento inconclusas que se asumen como problemas mecánicos.
- Elementos obsoletos que permanecen en BRAUMAT pero ya no están en funcionamiento.

El script filtrará automáticamente los TAGs listados en este archivo.

### Recomendaciones

Se recomienda ejecutar este código en **Google Colab** para evitar la instalación de dependencias adicionales en su computadora. Si opta por esta opción, no olvide cargar los archivos necesarios antes de ejecutar el código. En caso de ejecutarlo localmente, asegúrese de:

1. Instalar todas las dependencias requeridas.
2. Ubicar correctamente los archivos `MATRIZ` y `EXCEPCIONES`.

### Notas Finales

Este repositorio está diseñado para optimizar y automatizar el manejo de datos en el Dashboard de Fallas de BRAUMAT. Asegúrese de seguir las instrucciones cuidadosamente para garantizar un funcionamiento óptimo del código.
