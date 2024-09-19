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
            return "None"  # or handle the case when there are no temperatures
        return "{:.2f}".format(media)
    return f"{temperaturas}"

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

# print(dis('2024-07-07'))
