import xml.etree.ElementTree as ET
from xml.dom import minidom

import urllib.request

url_str = 'http://www.aemet.es/xml/municipios/localidad_18087.xml'
dom = minidom.parse(urllib.request.urlopen(url_str))  # parse the data

tree = ET.parse(urllib.request.urlopen(url_str))
root = tree.getroot()

Climate_Details_File_Name = 'Results/Climate_Details_xml.csv'  # where we gonna store the the details related for each day
Climate_Details = open(Climate_Details_File_Name, "a")
ColumnsTitleRow = "Province,Day,Probability of Precipitation Mean,Province Snow Bound Mean,Sky State Mean,Wind Mean,Temperature Mean,Humidity Mean\n"  # The columns titles

# Fields Variables Declaration
Probability_of_Precipitation = ''


def get_CityName():
    """
        get_CityName used to get the name of the province of the document, which we are working with

        :return: root.find('provincia').text is a string, represents the province, which we are working on
    """
    return str(root.find('provincia').text)  # root.find('province') returns the direct child 'province' of root. ...
    # ... An equivalent way to get the same result is ( root[3].text ), where ...
    # ... root[2] represents 'province' tag and it's the 4th direct child of root.


def get_ElaborateDate():
    """
        get_get_ElaborateDate used to get the date of creation of the file on which we are working

        :return:
    """
    return str(root.find('elaborado').text)  # root.find('elaborado') returns the direct child 'elaborado' of root. ...
    # ... An equivalent way to get the same result is ( root[1].text ), where ...
    # ... root[1] represents 'elaborado' tag and it's the 2d direct child of root.


def TestTagValue(Value):  # Test if Value is a valid number
    try:
        int(Value)
        return True

    except ValueError:
        try:
            float(Value)
            return True
        except ValueError:
            return False


def get_Detail_Field_Mean(day, FieldName):
    """
        :param day: a day, represented by the tag dia
    """

    Length = 0  # the number of prob_precipitacion tags for a day
    Detail_Field_Mean = 0
    Value_Exist = False
    Result = 0

    for Field in day.findall(FieldName):  # iterating over the tag, prob_precipitacion
        if (TestTagValue(str(Field.text))):  # if it's a valid number
            Detail_Field_Mean = Detail_Field_Mean + int(str(Field.text))
            Length = Length + 1
            Value_Exist = True

    if (Value_Exist):
        Result = Detail_Field_Mean / Length  # Calculating the mean
    return Result


def get_Day_Fields_Details(TreeRoot):
    Row_To_Insert = get_CityName() + "," + get_ElaborateDate() + ","  # A new raw to be inserted into Climate_Details file

    for Day in TreeRoot.iter('dia'):  # iterating over dia tags
        Row_To_Insert = Row_To_Insert + str(get_Detail_Field_Mean(Day, 'prob_precipitacion')) + "," + \
                        str(get_Detail_Field_Mean(Day, 'cota_nieve_prov')) + ","


