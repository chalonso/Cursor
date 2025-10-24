#analisis_ventas
#Cargar librerias
import pandas as pd
import matplotlib.pyplot as plt
import os

#Cargar datos de CSV
CSV_PATH = r"C:\Users\Rentas 25481\Documents\Cursor\proyecto_git\ventas.csv"
def cargar_y_validar(csv_path):
    #1) Cargar intentando parsear la columna 'fecha'
    df = pd.read_csv(csv_path, parse_dates=['fecha'], dayfirst=True)

    print("----Primeras filas---")
    print(df.head(),'\n')

    print("---Tipos originales---")
    print(df.dtypes, "\n")

    #2) Normalizar nombres de columna: quitar espacios y pasar a minusculas
    df.columns = [c.strip().lower() for c in df.columns]
    print("Columnas despues de normalizar: ", df.columns.tolist())

    #3) Renombrar si hay nombres distintos
    rename_map = {}
    if 'cantidad_vendida' in df.columns:
        rename_map['cantidad_vendida'] = 'cantidad'
    if 'precio unitario' in df.columns:
        rename_map['precio unitario'] = 'precio'
    if rename_map:
        df = df.rename(columns = rename_map)
        print("Se renombraron columnas: ", rename_map)
    
    #4) Asegurar que columnas necesarias existen
    needed = {'fecha', 'producto', 'cantidad', 'precio'}

    miss = needed - set(df.columns)
    if miss:
        raise ValueError(f"Faltan columnas en el CSV: {miss}")
    
    # 5) Limpiar la columna 'producto' (quitar espacios, normalizar mayúsculas)
    df['producto'] = df['producto'].astype(str).str.strip().str.lower()

    #6) convertir cantidad y precio a numéricos (forzar errores a NaN)
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors = 'coerce')
    df['precio'] = pd.to_numeric(df['precio'], errors = 'coerce')
    
    # # 7) Mostrar filas con problemas (NaN) para que puedas corregir
    problemas = df[df[['cantidad','precio','fecha','producto']].isnull().any(axis=1)]
    if not problemas.empty:
        print("\n--- Filas con datos inválidos (revisa o limpia) ---")
        print(problemas)
        # aquí puedes decidir: quitar filas con NaN o imputar
        # por ahora vamos a eliminar filas con datos críticos faltantes:
        df = df.dropna(subset=['cantidad','precio','fecha','producto']).copy()
        print(f"\nSe eliminaron {len(problemas)} filas inválidas.\n")
    
    #8) Asegurar tipos definitivos
    df['cantidad'] = df['cantidad'].astype(int)
    df['precio'] = df['precio'].astype(float)

    print("---Tipos finales--")
    print(df.dtypes, "\n")

    return df

# Test de carga cuando se llama desde la línea de comandos
if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encontró {CSV_PATH}. Crea el CSV o ajusta la variable CSV_PATH.")

    df = cargar_y_validar(CSV_PATH)
    print("Datos cargados y validados. Filas:", len(df))


#Calcular ventas totales por mes
def calcular_ventas_mes(df):
    #Agreagamos columna 'total por fila
    df['total'] = df['cantidad']*df['precio']
    #Extraemos periodo mes-año
    df['mes'] = pd.to_datetime(df['fecha'], errors='coerce').dt.to_period('M').astype(str)
    ventas_mes = df.groupby('mes')['total'].sum()
    return ventas_mes

#Determinar producto más vendido con mayor ingreso
def producto_mas_vendido(df):
    #Por cantidad
    por_cantidad = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    top_producto = por_cantidad.idxmax()
    return top_producto, por_cantidad
def producto_mayor_ingreso(df):
    por_ingreso = df.groupby('producto')['total'].sum().sort_values(ascending=False)
    top_ingreso = por_ingreso.idxmax()
    return top_ingreso, por_ingreso

#Graficar ventas por mes
def graficar_ventas_mes(ventas_mes, output="ventas_por_mes.png"):
    ventas_mes.plot(kind='bar',figsize=(10,5))
    plt.title("Ventas totales por mes")
    plt.xlabel("Mes")
    plt.ylabel("Ventas ($)")
    plt.tight_layout()
    plt.savefig(output)
    plt.show()
#Graficar top 5 productos por ingresos
def graficar_top5_productos_por_ingreso(por_ingreso, output="top5_productos.png"):
    top5 = por_ingreso.head(5)
    top5.plot(kind='bar', figsize=(8,5))
    plt.title("Top 5 productos por ingreso")
    plt.xlabel("Producto")
    plt.ylabel("Ingreso total")
    plt.tight_layout()
    plt.savefig(output)
    plt.show()


# Punto de entrada
if __name__ == "__main__":
    df = cargar_y_validar(CSV_PATH)
    # calcular ventas por mes
    ventas_mes = calcular_ventas_mes(df)
    print("\nVentas por mes:\n", ventas_mes)

    # producto mas vendido por cantidad
    top_prod, by_qty = producto_mas_vendido(df)
    print(f"\nProducto más vendido (cantidad): {top_prod}")
    print(by_qty)

    # producto con mayor ingreso
    top_ing, by_ing = producto_mayor_ingreso(df)
    print(f"\nProducto con mayor ingreso: {top_ing}")
    print(by_ing)

    # Graficas
    
    graficar_ventas_mes(ventas_mes)
    graficar_top5_productos_por_ingreso(by_ing)