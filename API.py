import aiohttp
import asyncio

async def consumir_api():
    # URL de la API que deseas consumir
    url = "https://openexchangerates.org/api/latest.json?app_id=bcc9fcbfee734ad1bf8a54c06a22ac71"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Verificar el estado de la respuesta
                if response.status == 200:
                    # La solicitud fue exitosa
                    datos = await response.json()
                    print(datos['rates']["COP"])
                    print('entro en if')
                    pesos= datos['rates']["COP"]
                    bs = datos['rates']["VES"]
                else:
                    # La solicitud no fue exitosa
                    print("Error en la solicitud. Código de estado:", response.status)
                    print('entro en else')

    except aiohttp.ClientError as e:
        # Ocurrió un error en la conexión
        print("Error de conexión:", str(e))
    suma1= round(5 * pesos,2)
    print(suma1)
    suma1= round(5 * bs,2)
    print(suma1)
async def main():
    await consumir_api()

#Ejecutar el bucle de eventos para ejecutar funciones asíncronas
loop = asyncio.get_event_loop()
loop.run_until_complete(main())