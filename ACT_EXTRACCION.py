import pandas as pd
import re
import time
from IPython.display import FileLink

def cargar_archivos_ios(files):
    data_list = []
    for f in files:
        try:
            data = pd.read_csv(f, encoding='ISO-8859-1', delimiter=';', on_bad_lines='skip')
            data_list.append(data)
            print(f"Archivo {f} cargado correctamente con {len(data)} filas.")
        except Exception as e:
            print(f"Error al cargar el archivo {f}: {e}")
    return pd.concat(data_list, ignore_index=True) if data_list else pd.DataFrame()

def cargar_archivo_matriz(file):
    try:
        return pd.read_csv(file, encoding='UTF-8', delimiter=',')
    except Exception as e:
        print(f"Error al cargar el archivo MATRIZ: {e}")
        return pd.DataFrame()

def cargar_excepciones(file):
    try:
        with open(file, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error al cargar el archivo EXCEPCIONES.txt: {e}")
        return []

def filtrar_ios_data(data, modulos_validos, excepciones_patron):
    data = data[data['Nombre del módulo'].isin(modulos_validos) &
                data['Descripción'].str.contains("Inicio de falla", case=False, na=False)]
    data = data[data['Descripción'] != '#N/D']
    data = data[~data['Nombre de objeto'].str.contains(excepciones_patron, na=False)]
    data = data[data['Nombre de objeto'].str.match(r'^[0-9=]', na=False)]
    return data

def agregar_area_desde_matriz(descripcion, matriz_data):
    for tag in matriz_data['TAG']:
        if tag in descripcion:
            return matriz_data[matriz_data['TAG'] == tag]['AREA'].values[0]
    return None

def convertir_line_protocol(data):
    lines = []
    for _, row in data.iterrows():
        line = (
            f"fallas,Planta={escape_spaces(row['Planta'])},Area={escape_spaces(row['Area'])},"
            f"Subarea={escape_spaces(row['Subarea'])},PLC={escape_spaces(row['PLC'])},"
            f"Group={escape_spaces(row['Group'])} "
            f"Tag=\"{row['Tag']}\",Objeto=\"{row['Objeto']}\",Receta=\"{row['Receta']}\" "
            f"{int(time.mktime(time.strptime(row['Fecha'], '%d.%m.%Y %H:%M:%S'))) * 1_000_000_000}"
        )
        lines.append(line)
    return lines

def ajustar_timestamps(lines):
    timestamp_count = {}
    adjusted_lines = []
    for line in lines:
        line_data, timestamp_str = line.rsplit(' ', 1)
        timestamp = int(timestamp_str)
        if timestamp in timestamp_count:
            timestamp_count[timestamp] += 1
            adjusted_timestamp = timestamp + timestamp_count[timestamp]
        else:
            timestamp_count[timestamp] = 0
            adjusted_timestamp = timestamp
        adjusted_lines.append(f"{line_data} {adjusted_timestamp}")
    return adjusted_lines

def escape_spaces(name):
    return str(name).replace(" ", "\\ ")

# Configuración de archivos
ios_files = ['IOS01.csv', 'IOS03.csv', 'IOS05.csv', 'IOS07.csv', 'IOS09.csv']
matriz_file = 'MATRIZ.csv'
excepciones_file = 'EXCEPCIONES.txt'

# Cargar y procesar datos
ios_data = cargar_archivos_ios(ios_files)
matriz_data = cargar_archivo_matriz(matriz_file)
excepciones = cargar_excepciones(excepciones_file)
excepciones_patron = '|'.join(re.escape(excepcion) for excepcion in excepciones)

print("Procesando...")

# Filtrar datos IOS
ios_data.columns = ios_data.columns.str.strip()
ios_data = filtrar_ios_data(ios_data, ['ICM1', 'ICM2', 'ICM3', 'ICM4', 'AIN'], excepciones_patron)

# Agregar columnas constantes
ios_data['Planta'] = 'Tuxtepec'
ios_data['Area'] = 'Brewing'

# Integrar datos MATRIZ
ios_data['AREA_MATRIZ'] = ios_data['Nombre de objeto'].apply(lambda x: agregar_area_desde_matriz(x, matriz_data))

# Ordenar los datos por "Fecha y Hora" de manera descendente sin convertir la columna
ios_data = ios_data.sort_values('Fecha y Hora', ascending=False)

# Reemplazar NaN con 'Desconocido'
ios_data = ios_data.fillna('Desconocido')

# Renombrar y reordenar columnas
ios_data = ios_data.rename(columns={
    'Número PCU': 'PLC',
    'Nombre de objeto': 'Tag',
    'Nombre de Unidad': 'Group',
    'Nombre de categoría de receta maestra': 'Receta',
    'Nombre del módulo': 'Objeto',
    'AREA_MATRIZ': 'Subarea',
    'Descripción': 'Descripcion',
    'Fecha y Hora' : 'Fecha'
})
ios_data = ios_data[['Planta', 'Area', 'Subarea', 'PLC', 'Tag', 'Group', 'Receta', 'Objeto', 'Fecha', 'Descripcion']]
ios_data = ios_data.dropna(subset=['Subarea'])

# Guardar resultados
ios_data.to_csv('resultado_filtrado_final.csv', encoding='UTF-8', index=False)

# Generar Line Protocol
lines = convertir_line_protocol(ios_data)
with open('TablaFallas_line_protocol.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

# Ajustar timestamps
adjusted_lines = ajustar_timestamps(lines)
with open('Fallas.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(adjusted_lines))

print("Proceso completado. Archivos generados: 'resultado_filtrado_final.csv', 'TablaFallas_line_protocol.txt', 'Fallas.txt'")
print("Cargue el archivo 'Fallas.txt' a la base de datos.")
display(FileLink('Fallas.txt'))