import matplotlib.pyplot as plt
from database_connection import DatabaseConnection

def get_temperatures(fecha, avg=True):
    db = DatabaseConnection()
    query = "SELECT temperature FROM information WHERE date = %s"
    temperaturas = [fila[0] for fila in db.execute_query(query, (fecha,))]
    db.close()

    if avg:
        if temperaturas:
            media = sum(temperaturas) / len(temperaturas)
        else:
            return "None"
        return "{:.2f}".format(media)
    return f"{temperaturas}"

def temperature_distribution(fecha):
    db = DatabaseConnection()
    query = "SELECT temperature, datahour FROM information WHERE date = %s"
    resultados = db.execute_query(query, (fecha,))
    db.close()

    temperaturas = [registro[0] for registro in resultados]
    horas = [registro[1] for registro in resultados]

    if len(temperaturas) == 0:
        return "No hay datos para mostrar"

    plt.figure(figsize=(10, 5))
    plt.plot(horas, temperaturas, marker='o')
    plt.title(f'Distribución de Temperaturas para {fecha}')
    plt.xlabel('Hora')
    plt.ylabel('Temperatura')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(f'images/distribucion_temperaturas_{fecha}.png')
    plt.show()

    return "Imagen creada con la distribución de las temperaturas"
