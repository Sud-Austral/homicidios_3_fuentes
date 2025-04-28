import pandas as pd
import requests
import os
import datetime

def dd_fiscalia():
    url = "https://homicidios.spd.gov.cl/homicidios/estadisticasMinisterio-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Referer": "https://homicidios.spd.gov.cl/homicidios/estadisticasMinisterio.php"
    }
    data = {
        "token": "61689f586d3ed3c5acbd1a30c964236e",
        "numPagina": "1",
        "regPagina": "16",
        "atr01": "2025",
        "atr02": "Marzo",
        "atr03": ""
    }
    for anyo in range(2025,2026):
        for mes in ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]:
            data2 = data.copy()
            data2["atr02"] = mes
            data2["atr01"] = anyo
            response = requests.post(url, headers=headers, data=data2)
            df = pd.read_html(response.text)
            df = df[1]
            df["fuente"] = "Ministerio Público, los cuales se extraen desde el sistema informático de apoyo a los Fiscales (SAF)"
            df.to_csv(f"fiscalia/Fiscalia_{data2['atr01']}_{data2['atr02']}.csv", index=False)

def dd_policia():
    url = "https://homicidios.spd.gov.cl/homicidios/estadisticasPoliciales-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Referer": "https://homicidios.spd.gov.cl/homicidios/estadisticasPoliciales.php"
    }
    data = {
        "token": "202d8f3ba54058c848b7d7a6dbcf60bf",
        "numPagina": "1",
        "regPagina": "16",
        "atr01": "2025",
        "atr02": "Febrero",
        "atr03": ""
    }
    for i in ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]:
        data2 = data.copy()
        data2["atr02"] = i
        response = requests.post(url, headers=headers, data=data2)
        df = pd.read_html(response.text)
        df = df[1]
        df["fuente"] = "Carabineros de Chile y la Policía de Investigaciones de Chile"
        df.to_csv(f"policia/Policiales_{data2['atr01']}_{i}.csv", index=False)

def dd_cead():
    url = "https://homicidios.spd.gov.cl/homicidios/estadisticasCead-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Referer": "https://homicidios.spd.gov.cl/homicidios/estadisticasCead.php"
    }
    data = {
        "token": "ebfe6454c9acfbe42d3ac6f5c05ad5f4",
        "numPagina": "1",
        "regPagina": "16",
        "atr01": "2024",
        "atr02": "Febrero",
        "atr03": ""
    }

    for anyo in range(2025,2026):
        for mes in ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]:
            data2 = data.copy()
            data2["atr02"] = mes
            data2["atr01"] = anyo
            response = requests.post(url, headers=headers, data=data2)
            df = pd.read_html(response.text)
            df = df[1]
            df["fuente"] = "CEAD"
            df.to_csv(f"cead/cead_{data2['atr01']}_{data2['atr02']}.csv", index=False)

def consolidado_policia():
    ruta_carpeta = "policia"

    # Listar todos los archivos
    archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]

    acumulador = []
    for archivo in archivos:
        df = pd.read_csv(f"policia/{archivo}")
        acumulador.append(df.copy())

    df = pd.concat(acumulador)
    del df["Frecuencia 2024"]
    df_policia = df.rename(columns={"Frecuencia 2025":"Frecuencia","Región":"Region"}).copy()
    return df_policia

def consolidado_fiscalia():
    ruta_carpeta = "fiscalia"

    # Listar todos los archivos
    archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]

    acumulador = []
    for archivo in archivos:
        df = pd.read_csv(f"fiscalia/{archivo}")
        acumulador.append(df.copy())

    df = pd.concat(acumulador)
    df_fiscalia = df.copy()
    return df_fiscalia

def consolidado_cead():
    ruta_carpeta = "cead"
    # Listar todos los archivos
    archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]

    acumulador = []
    for archivo in archivos:
        df = pd.read_csv(f"cead/{archivo}")
        acumulador.append(df.copy())

    df = pd.concat(acumulador)
    df_cead = df.copy()
    return df_cead

def funcion_global():
    dd_fiscalia()
    dd_policia()
    dd_cead()
    df_policia = consolidado_policia()
    df_fiscalia = consolidado_fiscalia()
    df_cead = consolidado_cead()
    df_final = pd.concat([df_policia,df_fiscalia,df_cead])
    df_final["actualizacion"] = datetime.datetime.now() 
    df_historico =pd.read_excel(r"homicidios/consolidado.xlsx")
    pd.concat([df_historico,df_final]) .to_excel(r"homicidios/consolidado.xlsx", index=False)

if __name__ == '__main__': 
    funcion_global()  


