import mysql.connector

def obtener_temperaturas(fecha, avg: bool = True):
    conn = mysql.connector.connect(
        host='localhost',
        port=33,
        user='root',
        password='',
        database='iot'
    )
    cursor = conn.cursor()
    query = "SELECT temperature FROM information WHERE date = %s"
    cursor.execute(query, (fecha,))
    temperaturas = [fila[0] for fila in cursor.fetchall()]
    conn.close()

    if avg:
        if temperaturas:
            media = sum(temperaturas) / len(temperaturas)
        else:
            return None  # or handle the case when there are no temperatures
        return "{:.2f}".format(media)
    return temperaturas

# print(obtener_temperaturas('2023-12-01', avg=True))

def distribucion_temperaturas(fecha):
    conn = mysql.connector.connect(
        host='localhost',
        port=33,
        user='root',
        password='',
        database='iot'
    )
    cursor = conn.cursor()
    query = "SELECT temperature, datahour FROM information WHERE date = %s"
    cursor.execute(query, (fecha,))
    resultados = cursor.fetchall()
    conn.close()

    return resultados

def dis(dia):
    import matplotlib.pyplot as plt
    resultados = distribucion_temperaturas(dia)

    # Extract temperatures and hours
    temperaturas = [registro[0] for registro in resultados]
    horas = [registro[1] for registro in resultados]

    if len(temperaturas) == 0:
        return "No hay datos para mostrar"

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(horas, temperaturas, marker='o')
    plt.title(f'Distribución de Temperaturas para {dia}')
    plt.xlabel('Hora')
    plt.ylabel('Temperatura')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(f'distribucion_temperaturas_{dia}.png')
    plt.show()

    return "Imagen creada con la distribución de las temperaturas"

# print(dis('2024-07-07'))
