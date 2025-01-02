"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import zipfile
import pandas as pd
import glob

def zip_to_df(zip, csv_name):
    with zipfile.ZipFile(zip, 'r') as archivo_zip:
        with archivo_zip.open(csv_name) as archivo_csv:
            df = pd.read_csv(archivo_csv)
    return df

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day:tecrear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months

    

    """ 
    files = glob.glob("files/input/*.zip")
    dataframes = []

    for file in files: 
        with zipfile.ZipFile(file, 'r') as archivo_zip:
            archivo_csv = archivo_zip.namelist()[0] 
            with archivo_zip.open(archivo_csv) as archivo:
                df = pd.read_csv(archivo)
                dataframes.append(df)


    df_combinado = pd.concat(dataframes, ignore_index=False)
    df_combinado['month'] = pd.to_datetime(df_combinado['month'], format='%b').dt.month

    # client    
    client = df_combinado[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    client['job'] = client['job'].str.replace('.', '').str.replace('-', '_')
    client['education'] = client['education'].str.replace('.', '_').replace('unknown', pd.NA)
    client['credit_default'] = client['credit_default'].map({'yes': 1}).fillna(0)
    client['mortgage'] = client['mortgage'].map({'yes': 1}).fillna(0)
    client.to_csv('files/output/client.csv', index=False)

    # campaign
    campaign = df_combinado[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome']].copy()  
    campaign['previous_outcome']= campaign['previous_outcome'].map({'success': 1}).fillna(0)
    campaign['campaign_outcome']= campaign['campaign_outcome'].map({'yes': 1}).fillna(0)
    campaign['last_contact_date']= pd.to_datetime('2022-' + df_combinado['month'].astype(str) + '-' + df_combinado['day'].astype(str) , format='%Y-%m-%d')
    # campaign['last_contact_date']= '2022-' + df_combinado['day'].astype(str) + '-' + df_combinado['month'].astype(str)
    campaign.to_csv('files/output/campaign.csv', index=False)

    # print(campaign['last_contact_date'].value_counts())

    # economics
    economics = df_combinado[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()    
    economics.to_csv('files/output/economics.csv', index=False)
    
    return


if __name__ == "__main__":
    clean_campaign_data()
