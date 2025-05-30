# scraper_vm.py (Ejecutar en la Máquina Virtual)
import requests
import pandas as pd
import json # Necesario para enviar el payload al proxy
import os
import time # Para añadir un pequeño retraso
import datetime


def llamada_proxy(
        target_url_base = "https://homicidios.spd.gov.cl/homicidios/estadisticasMinisterio-ajax.php",
        original_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
            # 'Content-Type' es importante y se pasa al proxy, que lo usará.
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0", # Este header podría no ser estándar o necesario
            "Referer": "https://homicidios.spd.gov.cl/homicidios/estadisticasMinisterio.php"
        },
        base_payload_data = {
            "token": "61689f586d3ed3c5acbd1a30c964236e",
            "numPagina": "1",
            "regPagina": "1000", # Intentar obtener todos los registros de una vez
            "atr01": "2025", # Año (se actualizará en el bucle)
            "atr02": "Marzo", # Mes (se actualizará en el bucle)
            "atr03": ""      # Parámetro desconocido, se mantiene vacío
        },
        output_directory = "fiscalia3",

    ):
    # --- CONFIGURACIÓN DEL PROXY ---
    # ¡¡¡IMPORTANTE!!!
    # Reemplaza '<IP_DEL_PC_LOCAL>' con la dirección IP real de tu PC 
    # donde se está ejecutando el script 'proxy_server.py'.
    # Ejemplo: PROXY_URL = "http://192.168.1.105:5000/proxy"
    PROXY_URL = "http://186.67.61.252:5000/proxy" 
    # Si cambiaste el puerto en proxy_server.py, actualízalo aquí también.

    # URL de destino original y encabezados
    
    

    # Datos base para el payload del formulario
    # El token "61689f586d3ed3c5acbd1a30c964236e" podría expirar o cambiar. 
    # Si el script deja de funcionar, verifica este token.
    

    # Directorio para guardar los archivos CSV
    
    #os.makedirs(output_directory, exist_ok=True)
    os.makedirs("descarga", exist_ok=True)

    all_dataframes = [] # Lista para almacenar todos los DataFrames y luego concatenarlos


    # Bucle para años y meses
    # Ajusta el rango de años según necesites. Actualmente hasta 2024 (2025 es exclusivo).
    # El año 2025 podría no tener datos todavía.
    max_year = datetime.datetime.now().year + 1
    for anyo in range(2018, max_year): 
        for mes in ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]:
            
            current_payload_data = base_payload_data.copy()
            current_payload_data["atr01"] = str(anyo) # Asegurar que el año sea string
            current_payload_data["atr02"] = mes

            print(f"Procesando: {mes} {anyo}...")

            # Construir el payload que se enviará al servidor proxy
            payload_for_proxy = {
                "url": target_url_base,
                "headers": original_headers,
                "data": current_payload_data # Estos son los datos del formulario
            }

            try:
                # Realizar la solicitud POST al servidor proxy, enviando el payload_for_proxy como JSON.
                # El proxy se encargará de hacer la solicitud POST real con 'data' como form-urlencoded.
                response_from_proxy = requests.post(PROXY_URL, json=payload_for_proxy, timeout=30) # Timeout de 30s
                
                # Verificar si la solicitud al proxy fue exitosa
                response_from_proxy.raise_for_status() 

                # El proxy devuelve una respuesta JSON que contiene 'text', 'status_code' de la respuesta del sitio de destino
                proxy_response_content = response_from_proxy.json()
                
                target_site_status_code = proxy_response_content.get('status_code')
                target_site_html_text = proxy_response_content.get('text')

                if target_site_status_code != 200:
                    print(f"  Error del sitio de destino para {mes} {anyo}: Código {target_site_status_code}")
                    # print(f"  Respuesta del sitio (primeros 300 chars): {target_site_html_text[:300]}")
                    continue

                if not target_site_html_text or "No se encontraron resultados" in target_site_html_text: # Ajustar si el mensaje es otro
                    print(f"  No se encontraron resultados para {mes} {anyo}.")
                    continue
                
                # Intentar leer las tablas HTML de la respuesta
                try:
                    list_of_dataframes = pd.read_html(target_site_html_text)
                    
                    if not list_of_dataframes:
                        print(f"  pd.read_html no encontró tablas para {mes} {anyo}.")
                        continue

                    # El script original usaba df[1]. Hay que ser cauteloso.
                    # Es mejor verificar si la tabla existe.
                    if len(list_of_dataframes) > 1:
                        df = list_of_dataframes[1] 
                    elif len(list_of_dataframes) == 1:
                        print(f"  Advertencia: Solo se encontró 1 tabla para {mes} {anyo}. Usando esa tabla.")
                        df = list_of_dataframes[0]
                    else: # Ya cubierto por 'if not list_of_dataframes', pero por si acaso.
                        print(f"  No se pudo extraer la tabla esperada para {mes} {anyo}.")
                        continue
                    
                    # Añadir columnas adicionales
                    df["fuente"] = "Ministerio Público, los cuales se extraen desde el sistema informático de apoyo a los Fiscales (SAF)"
                    df["AñoConsulta"] = anyo
                    df["MesConsulta"] = mes
                    
                    # Guardar en archivo CSV individual (opcional, si lo prefieres)
                    # filename = os.path.join(output_directory, f"Fiscalia_{anyo}_{mes}.csv")
                    # df.to_csv(filename, index=False)
                    # print(f"  Datos guardados en: {filename}")

                    all_dataframes.append(df)
                    print(f"  Datos de {mes} {anyo} recolectados exitosamente.")

                except ValueError as ve: # Ocurre si read_html no encuentra tablas
                    print(f"  Error al procesar HTML (pd.read_html) para {mes} {anyo}: {ve}")
                    # print(f"  Contenido HTML (primeros 300 chars): {target_site_html_text[:300]}")
                except IndexError as ie:
                    print(f"  Error de índice al acceder a la tabla para {mes} {anyo} (ej. df[1] no existe): {ie}")
                    print(f"  Tablas encontradas: {len(list_of_dataframes) if 'list_of_dataframes' in locals() else 'N/A'}")


            except requests.exceptions.HTTPError as http_err:
                print(f"  Error HTTP al contactar el PROXY para {mes} {anyo}: {http_err}")
                print(f"  Respuesta del proxy (si existe): {response_from_proxy.text[:300] if response_from_proxy else 'N/A'}")
            except requests.exceptions.ConnectionError as conn_err:
                print(f"  Error de Conexión al PROXY ({PROXY_URL}) para {mes} {anyo}: {conn_err}")
                print("    Verifica que el servidor proxy esté corriendo en tu PC local y que la IP sea correcta y accesible.")
                # Podrías querer detener el script aquí si el proxy no es accesible
                # break # Rompe el bucle de meses
            except requests.exceptions.Timeout:
                print(f"  Timeout al contactar el PROXY para {mes} {anyo}.")
            except json.JSONDecodeError as json_err:
                # Esto sucedería si el proxy devuelve algo que no es JSON válido
                print(f"  Error al decodificar JSON de la respuesta del PROXY para {mes} {anyo}: {json_err}")
                print(f"  Respuesta del proxy: {response_from_proxy.text[:300] if 'response_from_proxy' in locals() else 'N/A'}")
            except Exception as e:
                print(f"  Ocurrió un error inesperado procesando {mes} {anyo}: {e}")

        # if 'conn_err' in locals() and conn_err: # Si hubo error de conexión, salir del bucle de años
        #     break

    # Concatenar todos los DataFrames en uno solo al final
    if all_dataframes:
        print("\nConcatenando todos los datos recolectados...")
        try:
            final_df = pd.concat(all_dataframes, ignore_index=True)
            #final_filename = os.path.join(output_directory, f"{output_directory}_Compilado_Total.csv")
            #final_filename = os.path.join("descarga", f"{output_directory}_Compilado_Total.csv")
            final_filename = os.path.join("descarga", f"{output_directory}_Compilado_Total.xlsx")
            #final_df.to_csv(final_filename, index=False)
            final_df.to_xlsx(final_filename, index=False)
            print(f"Todos los datos han sido compilados y guardados en: {final_filename}")
        except Exception as e:
            print(f"Error al concatenar o guardar el DataFrame final: {e}")
    else:
        print("\nNo se recolectaron datos para generar un archivo compilado.")

    print("\nProceso de scraping finalizado.")
