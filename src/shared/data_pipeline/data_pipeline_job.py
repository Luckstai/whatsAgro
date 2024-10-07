import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import xarray as xr
import boto3
from io import StringIO
from botocore.exceptions import NoCredentialsError

from src.config import settings

TOKEN_EARTHDATA = settings.TOKEN_EARTHDATA
AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET_NAME = settings.S3_BUCKET_NAME

if not os.path.isdir("Dados"):
  os.mkdir("Dados")
if not os.path.isdir("Dados/raw"):
  os.mkdir("Dados/raw")
if not os.path.isdir("Dados/trusted"):
  os.mkdir("Dados/trusted")

# Criando um cliente S3
s3 = boto3.client(
's3',
aws_access_key_id=AWS_ACCESS_KEY,
aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def save_nc_to_s3_public(local_file, bucket_name, s3_file):
    """Uploads a file to an S3 bucket

    :param local_file: File to upload
    :param bucket_name: Bucket to upload to
    :param s3_file: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """


    try:
        s3.upload_file(local_file, bucket_name, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    

def get_last_data(directory_url, file_ext):
  filenames = [1]
  while filenames:
    response = requests.get(directory_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        files = soup.find_all('a')
        filenames = [file.get('href') for file in files if (file.get('href').endswith('/') or file.get('href').endswith(file_ext)) and not file.get('href').endswith('doc/')]
        last_value = [f for f in filenames][-1]
        directory_url+=last_value
        if last_value.endswith(file_ext):
          return directory_url
    else:
      print(f"Erro na requisição. Código de status: {response.status_code}")
  return directory_url

def get_filenames(directory_url, file_ext):
  response = requests.get(directory_url)
  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      files = soup.find_all('a')
      file_names = [file.get('href') for file in files if not file.get('href').endswith('/')]

      # Imprimir os nomes dos arquivos
      # for file_name in file_names:
      #     print(file_name)
      return [f for f in file_names if  f.endswith(file_ext)]
  else:
      print(f"Erro na requisição. Código de status: {response.status_code}")

def get_datas_raw(directory_url, filenames, bucket_name=S3_BUCKET_NAME):
  for fn in filenames:
    f = fn.split("/")[-1]
    base_url = f"{directory_url}/{f}"
    print(base_url)

    headers = {
        "Authorization": f"Bearer {TOKEN_EARTHDATA}"
    }

    # Fazer o request com o Bearer Token no cabeçalho
    response = requests.get(base_url, headers=headers)

    # Verificar se o request foi bem-sucedido
    if response.status_code == 200:
        print("Request bem-sucedido!")
        # print(response.text)  # Exibir os dados retornados
    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")

    if not os.path.isdir(f"Dados/raw/{f.split('_', 1)[0]}"):
      os.mkdir(f"Dados/raw/{f.split('_', 1)[0]}")
    # Abrir um arquivo para escrever o conteúdo da resposta
    with open(f"./Dados/raw/{f.split('_', 1)[0]}/{f}", 'wb') as fl:
        # Escrever o conteúdo em partes (streaming)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                fl.write(chunk)

    save_nc_to_s3_public(f"./Dados/raw/{f.split('_', 1)[0]}/{f}", bucket_name, f"raw/{f.split('_', 1)[0]}/{f}")
  return

def trusted_LPRM(filenames, bucket_name=S3_BUCKET_NAME):
  for fn in filenames:
    f = fn.split("/")[-1]

    if not os.path.isdir(f"Dados/trusted/{f.split('_', 1)[0]}"):
      os.mkdir(f"Dados/trusted/{f.split('_', 1)[0]}")

    dataset = xr.open_dataset(f"./Dados/raw/{f.split('_', 1)[0]}/{f}")

    coords = [c for c in dataset.coords]
    results = pd.DataFrame(columns=coords)
    for var_name in dataset.data_vars:
      if var_name != 'mask':
        try:
          tmp = dataset[var_name]
          df = pd.DataFrame(tmp.values, columns=tmp[coords[0]], index=tmp[coords[1]])
          df = df.stack().reset_index()
          df.columns = [coords[0], coords[1], var_name]
          results = pd.merge(results, df, on=coords, how='outer')
          if var_name == 'scantime':
            results = results.dropna(subset = results.drop([coords[0], coords[1], 'scantime'], axis=1).columns, how='all')
          results = results.dropna(subset = results.drop([coords[0], coords[1]], axis=1).columns, how='all')
        except:
          print("except")
    file_name = f"trusted/{f.split('_', 1)[0]}/{f.split('.', 1)[0]}.csv"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=results.to_csv(index=False))
  return


def trusted_NLDAS(filenames, bucket_name=S3_BUCKET_NAME):
  for fn in filenames:
    f = fn.split("/")[-1]

    if not os.path.isdir(f"Dados/trusted/{f.split('_', 1)[0]}"):
      os.mkdir(f"Dados/trusted/{f.split('_', 1)[0]}")

    dataset = xr.open_dataset(f"./Dados/raw/{f.split('_', 1)[0]}/{f}")

    coords = ['lon', 'lat']
    coords_pad = ['Longitude', 'Latitude']
    results = pd.DataFrame(columns=coords)
    for var_name in dataset.data_vars:
      if var_name != 'time_bnds':
        try:
          tmp = dataset[var_name]
          df = pd.DataFrame(tmp.values[0], columns=tmp[coords[0]], index=tmp[coords[1]])
          df = df.stack().reset_index()
          df.columns = [coords[0], coords[1], var_name]
          results = pd.merge(results, df, on=coords, how='outer')
          if var_name == 'scantime':
            results = results.dropna(subset = results.drop([coords[0], coords[1], 'scantime'], axis=1).columns, how='all')
          results = results.dropna(subset = results.drop([coords[0], coords[1]], axis=1).columns, how='all')
        except:
          print(var_name, "except")
    file_name = f"trusted/{f.split('_', 1)[0]}/{f.rsplit('.', 1)[0]}.csv"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=results.to_csv(index=False))
  return

def data_pipeline_job_run():
  print('INICIANDO DATA PIPELINE')
  directory_url_LPRM = "https://hydro1.gesdisc.eosdis.nasa.gov/data/WAOB/LPRM_AMSR2_DS_A_SOILM3.001/"
  file_ext_LPRM = ".nc4"
  directory_url_NLDAS = "https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_NOAH0125_H.2.0/"
  file_ext_NLDAS = ".nc"
  
  filename = get_last_data(directory_url_LPRM, file_ext_LPRM)
  directory_url_LPRM, filename = filename.rsplit("/", 1)
  filenames = [filename]
  get_datas_raw(directory_url_LPRM, filenames)
  trusted_LPRM(filenames)

  filename = get_last_data(directory_url_NLDAS, file_ext_NLDAS)
  directory_url_NLDAS, filename = filename.rsplit("/", 1)
  filenames = [filename]
  get_datas_raw(directory_url_NLDAS, filenames)
  trusted_NLDAS(filenames)