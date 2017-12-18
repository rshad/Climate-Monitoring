import urllib.request
import ssl
import json
import pandas as pd

Climate_Details_File_Name = '../Results/Files/Climate_Details_api.csv'  # where we gonna store the the details related for each day
Climate_Details = open(Climate_Details_File_Name, "a")
ColumnsNamesRow = "Province;Name;ID;Date;TemperatureMax;TemperatureMin;TemperatureMean;Direction;Racha;Sun;PresMaxima;PresMínima\n"
#Climate_Details.write(ColumnsNamesRow)

context = ssl._create_unverified_context() # we disable the ssl certificate verification, however it's not recommended but it's not our goal in this project
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

def GetData(month,id):
    """

    :param month: the specified month for which we want to get the data
    :param id: the province id
    :return main_page: represents the json file content
    """

    door_page_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2017-'+month+'-01T10:00:00UTC/fechafin/2017-'+month+'-30T10:00:00UTC/estacion/'+id+'/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyYXNoems5NUBnbWFpbC5jb20iLCJqdGkiOiJiYWIzZDBlYi05YzgyLTRlZWItYmVkMS1kZmNmYjhmNzdmYTIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTUxMjI1NDA5NSwidXNlcklkIjoiYmFiM2QwZWItOWM4Mi00ZWViLWJlZDEtZGZjZmI4Zjc3ZmEyIiwicm9sZSI6IiJ9.eHzVHMeH3TWOhD_oAaaI82Q-oThYEK-gXo_qbhdHkSU'

    with urllib.request.urlopen(door_page_url, context=context) as url:
        Door_Page = json.loads(
            url.read().decode())  # Door_Page represents the main page which contains the data url, metadata url, state and description

    main_data_url = Door_Page[
        'datos']  # datos represents the data url. for example -> 'datos': 'https://opendata.aemet.es/opendata/sh/a3763958'
    with urllib.request.urlopen(main_data_url, context=context) as main_page_url:
        main_page = json.loads(main_page_url.read().decode('latin-1'))

    return main_page

def write_ClimateVariablesValues(data,file):
    for index in range(0,(len(data)-1) ):
        Row_To_Insert=data[index]['provincia']+";"+data[index]['nombre']+";"+data[index]['indicativo']+";"+data[index]['fecha']+";"+data[index]['tmax']+";"+data[index]['tmin']+";"+data[index]['tmed']+";" \
                      +data[index]['dir']+";"+data[index]['racha']+";"+data[index]['sol']+";"+data[index]['presMax']+";"+data[index]['presMin']+"\n"
        file.write(Row_To_Insert)


def plot_(file,feature):
    """
    plot_ plot the data of file specified for the feature 'feature' with determined type of graph, we specify inside

    :param file: represents the file which contains the data to be plotted
    :param feature: the feature of the graph

    """

    import plotly.plotly as py
    import plotly.graph_objs as go
    import plotly

    plotly.tools.set_credentials_file(username='RashPlotly', api_key='mShgbTicudYnkcAZA3eH')

    df = pd.read_csv(file,delimiter=";") # reading the file
    subset = df
    subset = subset[subset['Province'].str.contains("GRANADA")]

    used=['Date','PresMaxima','PresMinima'] # determine the used columns or features
    X = subset[used]
    data = [go.Heatmap(x=X['Date'], y=X['PresMinima'],z=X['PresMaxima'])] # define the graph
    py.plot(data) # plotting

if __name__ == "__main__" :
    """
    for month in months: # Reading data for the province with idem= ... , in months
        print(month)
        main_page_data = GetData(month,'1082')
        write_ClimateVariablesValues(main_page_data,Climate_Details)
    """
    plot_("../Results/Files/Climate_Details_api.csv",'') # ploting


