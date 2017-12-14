import urllib.request
import ssl
import json

Climate_Details_File_Name = '../Results/Climate_Details_api.csv'  # where we gonna store the the details related for each day
Climate_Details = open(Climate_Details_File_Name, "a")
ColumnsNamesRow = "Province;Date;TemperatureMax;TemperatureMin;TemperatureMean"
#Climate_Details.write(ColumnsNamesRow)

context = ssl._create_unverified_context() # we disable the ssl certificate verification, however it's not recommended but it's not our goal in this project
door_page_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2017-12-04T10:00:00UTC/fechafin/2017-12-11T10:00:00UTC/estacion/5530E/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyYXNoems5NUBnbWFpbC5jb20iLCJqdGkiOiJiYWIzZDBlYi05YzgyLTRlZWItYmVkMS1kZmNmYjhmNzdmYTIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTUxMjI1NDA5NSwidXNlcklkIjoiYmFiM2QwZWItOWM4Mi00ZWViLWJlZDEtZGZjZmI4Zjc3ZmEyIiwicm9sZSI6IiJ9.eHzVHMeH3TWOhD_oAaaI82Q-oThYEK-gXo_qbhdHkSU'
#door_page_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2017-12-04T10:00:00UTC/fechafin/2017-12-11T10:00:00UTC/todasestaciones/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyYXNoems5NUBnbWFpbC5jb20iLCJqdGkiOiJiYWIzZDBlYi05YzgyLTRlZWItYmVkMS1kZmNmYjhmNzdmYTIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTUxMjI1NDA5NSwidXNlcklkIjoiYmFiM2QwZWItOWM4Mi00ZWViLWJlZDEtZGZjZmI4Zjc3ZmEyIiwicm9sZSI6IiJ9.eHzVHMeH3TWOhD_oAaaI82Q-oThYEK-gXo_qbhdHkSU'

with urllib.request.urlopen(door_page_url,context=context) as url:
    Door_Page=json.loads(url.read().decode()) # Door_Page represents the main page which contains the data url, metadata url, state and description


main_data_url = Door_Page['datos'] #datos represents the data url. for example -> 'datos': 'https://opendata.aemet.es/opendata/sh/a3763958'
with urllib.request.urlopen(main_data_url,context=context) as main_page_url:
    main_page=json.loads(main_page_url.read().decode('latin-1'))

def write_ClimateVariablesValues(data,file):
    for index in range(0,(len(data)-1) ):
        Row_To_Insert=data[index]['provincia']+";"+data[index]['fecha']+";"+data[index]['tmax']+";"+data[index]['tmin']+";"+data[index]['tmed']+"\n"
        file.write(Row_To_Insert)


