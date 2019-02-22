#look at try/except for error handling and screening for correct inputs
#look at mapping to simplify the iterations

import pandas as pd
import numpy as np 
import xlsxwriter as xls
import datasheetFormat as form

workbook = xls.Workbook('ava_Datasheets.xlsx')
actDescriptors = {'type': ('Basic', 'Smart'), 'size': ('20', '60', '110', '200', '400'), 'operation':('on/off', 'modulating'), 'voltage':('95 - 265 VAC', '24 VAC/DC', '24 VDC', '24 VAC', '12 VDC'), 'signal': ('current', 'voltage', 'variable', 'contacts')} 
characteristics = actDescriptors.keys()
signals = {'signal': ('current', 'voltage', 'variable', 'contacts')}
options = {'fast':'1 Second Cycles', 'fs' : 'Fail Safe', 'alm' : 'Alarm Output', 'na' : 'None}
sizes = {'20': '20', '60': '60', '110': '110', '200': '200', '400': '400' }
ops = {'onf':'on/off', 'mod': 'modulating'}
voltage = {}
gendetails = {'Housing Material' : 'ABS', \
             'Heater' : 'yes', \
             'Wiring Box Inserts' : 'Asahi Spec', \
             'Override Return': 'Shortest Path', \
            'IP Rating' : 'IP67', \
            'Limit Switches' : 'Open/Close', \
            'Flying Leads' : 'Nylon', \
            'Cable Length' : '0.8m', \
            'Indicator' : 'Dome', \
            'Cover Color' : 'Red', 'Base Color' : 'Red', \
            'Conduit Box Screws' : 'Asahi Spec', \
            'Cover Screws' : 'Asahi Spec', \
            'Manual Override' : 'Asahi Spec', \
            'Connecting Cable' : '0.8mm rated at 300V', \
            'Sound Level' : 'max 50dB(A)', \
            'Electrical Safety' : 'Ground protection III safety', \
            'Inflaming Retarding Level' : 'V0 UL94 tested', \
            'Enclosure Rating' : 'IP67', \
            'Insulation Resistance' : '100M / 500VDC', \
            'Withstand Voltage' : '500VAC', \
            'Temperature Rating': '-20c to 60c', \
            'Explosion Proof Rating' : 'None', \
            'Humidity Rating' : '5 - 95% Non-condensing', \
            'Shock Resistance' : '<<300m/s^2', \
            'Vibration Resistance' : '10 - 55 Hz, 1.5mm double amplitude', \
            'Installation Orientation' : 'Any', \
            'Maintenance' : 'None Required', \
            'Certification':'CE', \
            }

gencomments = {'Housing Material' : 'PA 757', \
               'Heater' : 'Internal Space Heater', \
               'Wiring Box Inserts' : 'Electroless Nickel Plated', \
            'Override Return': 'Always returns to home via shortest path on power-up', \
            'IP Rating' : 'Factory tested', \
            'Limit Switches' : 'End of travel limit switches', \
            'Flying Leads' : 'UL Approved, with pin connectors 0.8m long', \
            'Cable Length' : 'Standard length', \
            'Indicator' : 'Yellow = closed, Black = Open', \
            'Conduit Box Screws' : 'Stainless steel, hex head, captivated', \
            'Cover Screws' : 'Stainless steel, standard', \
            'Manual Override' : 'via allen key on base, Electro-less nickel plated allen key', \
            'Cover Color' : 'Pantone 185 C', \
            'Base Color' : 'Pantone xxx',  \
            'Connecting Cable' : '', \
            'Sound Level' : '', \
            'Electrical Safety' : '', \
            'Inflaming Retarding Level' : '', \
            'Enclosure Rating' : 'As per EN60529/GB4208-2008', \
            'Insulation Resistance' : 'Motor Insulation?', \
            'Withstand Voltage' : 'Motor Insulation?', \
            'Temperature Rating': 'ambient', \
            'Explosion Proof Rating' : 'Not for use in hazardous environments', \
            'Humidity Rating' : '', \
            'Shock Resistance' : '', \
            'Vibration Resistance' : '', \
            'Installation Orientation' : '', \
            'Maintenance' : '', \
            'Certification':'' , \
            }

typedetails = {'Smart' : ['Smart', 'Yes', 'v11.0'], \
                'Basic' : ['Basic', 'None', 'N/A']}
typecomments = {'Smart' : ['Asahi branded smart actuator', '1.3" OLED color screen', 'Confirm with factory, Asahi branded firmware'], \
                'Basic' : ['Asahi branded basic actuator', 'N/A', 'N/A']}
typeNumbers = {'Type' : 0, 'OLED Screen' : 1, 'Firmware' : 2}

smartsizedetails = {'Mounting Patterns': ['F03, F04, F05', 'F05, F07', 'F05, F07', 'F07, F10', 'F07, F10'], \
                    'Output drive' : ['14mm', '17mm', '17mm', '22mm', '22mm'], \
                    'Run Time' : ['10 seconds', '10 seconds', '10 seconds', '30 seconds', '30 seconds'], \
                    'Torque Output' : ['20Nm', '60Nm', '110Nm', '200Nm', '400Nm']
                    }
smartsizecomments = {'Mounting Patterns': ['ISO 5211, electro-less nickel plated inserts', 'ISO 5211, electro-less nickel plated inserts' , 'ISO 5211, electro-less nickel plated inserts', 'ISO 5211, electro-less nickel plated inserts', 'ISO 5211, electro-less nickel plated inserts'], \
                    'Output drive' : ['Female octagon, electroless nickel plated', 'Female octagon, electroless nickel plated', 'Female octagon, electroless nickel plated', 'Female octagon, electroless nickel plated', 'Female octagon, electroless nickel plated' ],\
                    'Run Time' : ['0 - 90 degree operation', '0 - 90 degree operation', '0 - 90 degree operation', '0 - 90 degree operation', '0 - 90 degree operation'], \
                    'Torque Output' : ['Rated Torque. maximum torque varies', 'Rated Torque. maximum torque varies', 'Rated Torque. maximum torque varies', 'Rated Torque. maximum torque varies', 'Rated Torque. maximum torque varies']
                    }
smartsizenumbers = {'20' : 0, \
                    '60' : 1, \
                    '110' : 2, \
                    '200' : 3, \
                    '400' : 4
                    }
powerConsumption = { '95 - 265 VAC' : ['9.6W run, 0.12W hold', '30W run, 3.9W hold', '30W run, 3.9W hold', '150W run, 0.7W hold', '150W run, 0.7W hold'], \
                    '24 VAC/DC' : ['9.6W run, 0.12W hold', '30W run, 3.9W hold', '30W run, 3.9W hold', '120W run, 1.5W hold', 'to be confirmed'], \
                    '24 VDC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD'], \
                    '24 VAC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD'], \
                    '12 VDC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD']
                    }
peakCurrent = { '95 - 265 VAC' : ['35mA (230V)', '0.26A (230V)', '0.26A (230V)', '0.7A(230V)', '1.8A (230V)'], \
                    '24 VAC/DC' : ['350mA (24V)', '2.5A (24V)', '2.5A (24V)', '6A (24V)', 'to be confirmed'], \
                    '24 VDC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD'], \
                    '24 VAC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD'], \
                    '12 VDC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD']
                    }
fuses = { '95 - 265 VAC' : ['1A', '2A', '2A', '5A', '10A'], \
                    '24 VAC/DC' : ['2A', '5A', '5A', '10A', 'to be confirmed'], \
                    '24 VDC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD'], \
                    '24 VAC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD'], \
                    '12 VDC' : ['TBD', 'TBD', 'TBD', 'TBD', 'TBD']
                    }

finalChars = { 'wiring diagram': '***', \
                'label number' : '***', \
                'Function' : '***', \
                'Signal' : '***', \
                'Failsafe' : '***', \
                'Alarm' : '***'
                }

generalKeys = gendetails.keys()
typeKeys = typeNumbers.keys()
smartsizeKeys = smartsizedetails.keys()
finalcharKeys = finalChars.keys()

#Define some functions for building information about each actuator
def genextractor(characteristics, details, comments):
    temp = []
    tempKeys = pd.DataFrame()
    tempKeys['Characteristics'] =  characteristics
    keys = pd.DataFrame()
    keys['keys'] = characteristics
    row = len(characteristics)
    for i in range(row):
        keyIndex = keys['keys'][i]
        tempKeys.loc[[i], 'Details'] = details[keyIndex]
        tempKeys.loc[[i], 'Comments'] = comments[keyIndex]
    for row in tempKeys.itertuples(False):
        temp.append(row)
    return(temp)  

def seriesextractor(style, characteristics, details, comments):
    temp = []
    tempKeys = pd.DataFrame()
    tempKeys['Characteristics'] = characteristics
    row = len(characteristics)
    for i in range(row):
        tempKeys.loc[[i], 'Details'] = details[style][i]
        tempKeys.loc[[i], 'Comments'] = comments[style][i]
    for row in tempKeys.itertuples(False):
        temp.append(row)
    return(temp)
        
def sizeextractor(size, characteristics, details, comments):
    temp = []
    tempKeys = pd.DataFrame()
    tempKeys['Characteristics'] = characteristics
    selector = smartsizenumbers[size]
    keys = pd.DataFrame()
    keys['keys'] = characteristics
    row = len(characteristics)
    for i in range(row):
        keyIndex = keys['keys'][i]
        tempKeys.loc[[i], 'Details'] = details[keyIndex][selector]
        tempKeys.loc[[i], 'Comments'] = comments[keyIndex][selector]
    for row in tempKeys.itertuples(False):
        temp.append(row)
    return(temp)

def powerextractor(size, voltage):
    temp = []
    tempKeys = pd.DataFrame()
    tempKeys['Characteristics'] = ['Power Consumption', 'Peak Current', 'Fuses']
    selector = smartsizenumbers[size]
    tempKeys.loc[[0], 'Details'] = powerConsumption[voltage][selector]
    tempKeys.loc[[1], 'Details'] = peakCurrent[voltage][selector]
    tempKeys.loc[[2], 'Details'] = fuses[voltage][selector]
    for row in tempKeys.itertuples(False):
        temp.append(row)
    return(temp)

voltCounts = len(actDescriptors['voltage']) #Count the number of descriptors in voltage since it's the largest
smart = pd.DataFrame() #Set a dataframe for smart actuators
basic = pd.DataFrame() #Set a dataframe for basic actuators
indices = [] #An empty list for index numbers

for i in range(0, voltCounts ** 2): #Fill the indices list with the maximum number of combinations available
    indices.append(i)
    
smart['Index'] = indices #Set a column with the index numbers
basic['Index'] = indices
voltsIndex = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4] #Do this because I'm dumb and can't do it right
for i in range(voltCounts ** 2): #Fill the columns with unique combinations of data from the pre-defined dictionaries
    smart.loc[[i], 'Type'] = actDescriptors['type'][1]
    smart.loc[[i], 'Size'] = actDescriptors['size'][i // voltCounts]
    smart.loc[[i], 'Voltage'] = actDescriptors['voltage'][voltsIndex[i]]
    
for i in range(voltCounts ** 2):
    basic.loc[[i], 'Type'] = actDescriptors['type'][0] #And do it again for the basic actuators
    basic.loc[[i], 'Size'] = actDescriptors['size'][i // voltCounts]
    basic.loc[[i], 'Voltage'] = actDescriptors['voltage'][voltsIndex[i]]

smartCOPY1 = smart.copy() #Create copies of the smart dataframe so we don't fuck it up
smartCOPY2 = smart.copy()

smartONF = smartCOPY1
smartONF['Function'] = actDescriptors['operation'][0] #Split the smart actuators into modulating and on/off functions

smartONF['Signal'] = signals['signal'][3] #Set the signal for the On/Off actuators to switch contacts

smartMOD = smartCOPY2
smartMOD['Function'] = actDescriptors['operation'][1]

smart20 = smartMOD.copy() #Make a second copy of the smartMOD dataframe before we do work on it

for i in range(0,5):
    smartMOD.drop([i], axis = 0, inplace = True)

for i in range (5, len(smart20['Index'])): #Drop the rows unrelated to the S20 actuators
    smart20.drop([i], axis = 0, inplace = True)

smart20Current = smart20.copy() #Make copies of the smart20 dataframes to add stuff into it
smart20Voltage = smart20.copy()

smart20Current['Signal'] = signals['signal'][0] #Add descriptors from the signals dictionary
smart20Voltage['Signal'] = signals['signal'][1]
smartMOD['Signal'] = signals['signal'][2]

smart20 = pd.concat([smart20Current, smart20Voltage]) #Start zipping things back together
smartMOD = pd.concat([smart20, smartMOD], sort = False)
smart = pd.concat([smartONF, smartMOD], sort = False)

resultFilter1 = smart['Voltage'] == actDescriptors['voltage'][0]
resultFilter2 = smart['Voltage'] == actDescriptors['voltage'][1]
resultFilter = resultFilter1 | resultFilter2 
smartFiltered = smart[resultFilter].copy()
filteredLength = len(smartFiltered)

smartFiltered['Index'] = filteredLength

for i in range(5, len(basic['Index'])):
    basic.drop([i], axis = 0, inplace = True)

basic['Signal'] = actDescriptors['signal'][3]
basic['Function'] = actDescriptors['operation'][0]

actuatorDF = pd.concat([smartFiltered, basic], sort = False)
newRows = []
for i in range(len(actuatorDF['Index'])):
    newRows.append(i)
actuatorDF['Index'] = newRows

class nonExActuators:
    genCharacteristics = genextractor(generalKeys, gendetails, gencomments)
    def __init__(self, style, size, voltage):
        self.style = seriesextractor(style, typeKeys, typedetails, typecomments)
        self.size = sizeextractor(size, smartsizeKeys, smartsizedetails, smartsizecomments)
        self.voltage = powerextractor(size, voltage)

actTuple = []
for row in actuatorDF.itertuples(False):
    actTuple.append(row)
    
dfSize = len(actuatorDF)

header_format = workbook.add_format({'bold' : True, \
                                     'font_color' : 'grey', \
                                     'align' : 'center', \
                                     'valign' : 'center', \
                                     'bg_color' : '#ff9c2b'
        })
    
title_format = workbook.add_format({'bold' : True, \
                                    'font_color' : 'blue', \
                                    'font_size' : 14
                                    }) 
    
content_format= workbook.add_format({
        
        
        })    

for i in range(dfSize):
    tempType = actTuple[i][1]
    tempSize = actTuple[i][2]
    tempVoltage = actTuple[i][3]
    worksheetName = str(i)
    worksheet = workbook.add_worksheet(worksheetName)
    worksheet.set_column(0,0, 23)
    worksheet.set_column(1,1, 32)
    worksheet.set_column(2,2, 48)
    temp = nonExActuators(tempType, tempSize, tempVoltage)
    gen = len(temp.genCharacteristics)    
    series = len(temp.style)
    size = len(temp.size)
    power = len(temp.voltage)
    #docs = len()
    row = 0
    col = 0   
    for i in range(gen + 2):
        if i == 0:
            worksheet.write(row, col, 'General Characteristics', title_format)
        elif i == 1:
            worksheet.write(row, col, 'Parameter', header_format)
            worksheet.write(row, col + 1, 'Details', header_format)
            worksheet.write(row, col + 2, 'Comments', header_format)
        else:
            worksheet.write(row, col, temp.genCharacteristics[i - 2][0])
            worksheet.write(row, col + 1, temp.genCharacteristics[i - 2][1])
            worksheet.write(row, col + 2, temp.genCharacteristics[i - 2][2])
        row += 1

    row = gen + 3
    col = 0

    for i in range(series + 2):
        if i == 0:
            worksheet.write(row, col, 'Series Characteristics', title_format)
        elif i == 1:
            worksheet.write(row, col, 'Parameter', header_format)
            worksheet.write(row, col + 1, 'Details', header_format)
            worksheet.write(row, col + 2, 'Comments', header_format)
        else:
            worksheet.write(row, col, temp.style[i - 2][0])
            worksheet.write(row, col + 1, temp.style[i - 2][1])
            worksheet.write(row, col + 2, temp.style[i - 2][2])  

        row += 1

    row = gen + series + 6
    col = 0

    for i in range(size + 2):
        if i == 0:
            worksheet.write(row, col, 'Size Characteristics', title_format)
        elif i == 1:
            worksheet.write(row, col, 'Parameter', header_format)
            worksheet.write(row, col + 1, 'Details', header_format)
            worksheet.write(row, col + 2, 'Comments', header_format)
        else:
            worksheet.write(row, col, temp.size[i - 2][0])
            worksheet.write(row, col + 1, temp.size[i - 2][1])
            worksheet.write(row, col + 2, temp.size[i - 2][2])  
        row += 1

    row = gen + series + size + 9
    col = 0

    for i in range(power + 2):
        if i == 0:
            worksheet.write(row, col, 'Power Characteristics', title_format)
        elif i == 1:
            worksheet.write(row, col, 'Parameter', header_format)
            worksheet.write(row, col + 1, 'Details', header_format)
            worksheet.write(row, col + 2, 'Comments', header_format)
        else:
            worksheet.write(row, col, temp.voltage[i - 2][0])
            worksheet.write(row, col + 1, temp.voltage[i - 2][1])        

        row += 1    
    
    #row = gen + series + size + power + 4
    #col = 0

        #for i in range(docs):
        #    worksheet.write(row, col, docTup[i][0])
        #    worksheet.write(row, col + 1, docTup[i][1])
        #    row += 1   
workbook.close()

#tempType = actuatorDF.loc[[0], 'Type']
#tempSize = actuatorDF.loc[[0], 'Type']
#tempVoltage = actuatorDF.loc[[0],'Voltage']
#test = nonExActuators(tempType, tempSize, tempVoltage)


#partNumbers = ()
#for i in range(dfSize):
#    tempType = actuatorDF.loc[[i], 'Type']
#    tempSize = actuatorDF.loc[[i], 'Type']
#    tempVoltage = actuatorDF.loc[[i],'Voltage']
#    partNumbers[i] = nonExActuators(tempType, tempSize, tempVoltage)
    
#for i in range(dfSize):
    #partNumbers.append(i)


#actuatorDF.to_csv('actuatorSet.csv', sep=',')

