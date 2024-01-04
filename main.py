from fastapi import FastAPI, HTTPException
import mysql.connector
import httpx

app = FastAPI()

# Configura la conexión a la base de datos MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "admin123",
    "database": "empleadosGeoreferencia",
}

# Conecta a la base de datos
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor(dictionary=True)

# URL de la API de geocode.xyz
geocode_api_url = "https://geocode.xyz/{}?auth=110638016191619233760x31268"

@app.get("/obtener_ciudad/{nombre}")
async def obtener_ciudad(nombre: str):
    # Consulta para obtener la ciudad basada en el nombre
    query = "SELECT ciudad FROM base_usuarios WHERE nombre = %s"
    cursor.execute(query, (nombre,))
    result = cursor.fetchone()

     # Verifica si se encontró el nombre en la base de datos
     # Verifica si se encontró el nombre en la base de datos
    if result:
        ciudad = result["ciudad"]
        return {"nombre": nombre, "ciudad": ciudad}
    else:
        raise HTTPException(status_code=404, detail="Nombre no encontrado")

# Endpoint para obtener información de geolocalización basada en la ciudad
@app.get("/obtener_info_geolocalizacion/{ciudad}")
async def obtener_info_geolocalizacion(ciudad: str):
    # Consulta el servicio de geolocalización (usando Geocode.xyz como ejemplo)
    api_url = f"https://geocode.xyz/{ciudad}?json=1"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)

    if response.status_code == 200:
        data = response.json()

        # Inserta la respuesta en la tabla ciudades
        insert_query = "INSERT INTO ciudades (nombre_ciudad, georeferenciacion) VALUES (%s, %s) ON DUPLICATE KEY UPDATE georeferenciacion = %s"
        cursor.execute(insert_query, (ciudad, response.text, response.text))
        connection.commit()

        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener información de geolocalización")

# Cierra la conexión después de cada solicitud
@app.on_event("shutdown")
def shutdown_event():
    cursor.close()
    connection.close()
