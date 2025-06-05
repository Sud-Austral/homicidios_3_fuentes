import pandas as pd
import requests
import os
import datetime
import proxy

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
        "regPagina": "18",
        "atr01": "2025",
        "atr02": "Marzo",
        "atr03": ""
    }
    proxy.llamada_proxy(target_url_base=url,original_headers=headers,base_payload_data=data,output_directory="fiscalia")
    


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
        "regPagina": "18",
        "atr01": "2025",
        "atr02": "Febrero",
        "atr03": ""
    }
    proxy.llamada_proxy(target_url_base=url,original_headers=headers,base_payload_data=data,output_directory="policia")

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
        "regPagina": "18",
        "atr01": "2024",
        "atr02": "Febrero",
        "atr03": ""
    }
    proxy.llamada_proxy(target_url_base=url,original_headers=headers,base_payload_data=data,output_directory="cead")

def dd_nacional():
    url = "https://homicidios.spd.gov.cl/homicidios/cifrasOficiales-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Referer": "https://homicidios.spd.gov.cl/homicidios/cifrasOficiales.php"
    }

    data = {
        "token": "0925705fa3d17cbda0e68869dc9fa1fa",
        "numPagina": "1",
        "atr01": "2023",
        "atr02": "",
        "atr03": ""
    }
    proxy.llamada_proxy(target_url_base=url,original_headers=headers,base_payload_data=data,output_directory="nacional")
    

def consolidado_policia():
    ruta = r"policia_Compilado_Total.xlsx"
    df = pd.read_excel(f"descarga/{ruta}")
    df = df[['Año', 'Mes', 'Región','fuente','Frecuencia 2025']]
    df.columns = ["Año","Mes","Region","fuente","Frecuencia"]
    #df.to_excel(f"descarga2/{ruta}", index=False)
    return df

def consolidado_fiscalia():
    ruta = r"fiscalia_Compilado_Total.xlsx"
    df = pd.read_excel(f"descarga/{ruta}")
    df = df[['Año', 'Mes', 'Region', 'Frecuencia', 'fuente']]
    #df.columns = ["Año","Mes","Region","fuente","Frecuencia"]
    #df.to_excel(f"descarga2/{ruta}", index=False)
    return df

def consolidado_cead():
    ruta = r"cead_Compilado_Total.xlsx"
    df = pd.read_excel(f"descarga/{ruta}")
    df = df[['Año', 'Mes', 'Region', 'Frecuencia', 'fuente']]
    #df.columns = ["Año","Mes","Region","fuente","Frecuencia"]
    #df.to_excel(f"descarga2/{ruta}", index=False)
    return df

def consolidado_nacional():
    ruta = r"nacional_Compilado_Total.xlsx"
    df = pd.read_excel(f"descarga/{ruta}")
    df = df[['Año', 'Mes', 'Region', 'Frecuencia', 'fuente']]
    #df.columns = ["Año","Mes","Region","fuente","Frecuencia"]
    #df.to_excel(f"descarga2/{ruta}", index=False)
    return df

def consolidado_stop():
    ruta = r"stop.xlsx"
    df = pd.read_excel(f"descarga/{ruta}")
    df = df[['Año', 'Mes', 'Region', 'Frecuencia', 'fuente']]
    #df.columns = ["Año","Mes","Region","fuente","Frecuencia"]
    #df.to_excel(f"descarga2/{ruta}", index=False)
    return df

def funcion_global():
    dd_fiscalia()
    dd_policia()
    dd_cead()
    df_policia = consolidado_policia()
    df_fiscalia = consolidado_fiscalia()
    df_cead = consolidado_cead()
    df_final = pd.concat([df_policia,df_fiscalia,df_cead])
    df_final["actualizacion"] = datetime.datetime.now() 
    df_historico =pd.read_excel(r"homicidios/test.xlsx")
    pd.concat([df_historico,df_final]) .to_excel(r"homicidios/test.xlsx", index=False)

if __name__ == '__main__': 
    dd_fiscalia()
    dd_policia()
    dd_cead()
    dd_nacional()
    df_policia = consolidado_policia()
    df_fiscalia = consolidado_fiscalia()
    df_cead = consolidado_cead()
    df_nacional = consolidado_nacional()
    df_stop = consolidado_stop()
    df_final = pd.concat([df_policia,df_fiscalia,df_cead,df_nacional,df_stop])
    df_final["actualizacion"] = datetime.datetime.now() 
    df_final.to_excel(r"test1.xlsx", index=False)
    historico = pd.read_excel("https://raw.githubusercontent.com/Sud-Austral/homicidios_3_fuentes/refs/heads/main/homicidios/consolidado_homicidios_historico.xlsx")

    pd.concat([historico,df_final]).to_excel(r"test2.xlsx", index=False)
    print("Cerrado y guardado")

    


      


