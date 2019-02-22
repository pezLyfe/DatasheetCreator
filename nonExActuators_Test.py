#look at try/except for error handling and screening for correct inputs
#look at mapping to simplify the iterations

import pandas as pd
import numpy as np 
import xlsxwriter as xls
import datasheetFormat as form
import nonExActuatorInformation as nonInfo

workbook = xls.Workbook('ava_Datasheets.xlsx')

styles = nonInfo.actDescriptors['type']
sizes = nonInfo.actDescriptors['size']
operations = nonInfo.actDescriptors['operation']
voltages = nonInfo.actDescriptors['voltage']
signals = nonInfo.actDescriptors['signal']

combos = [[style, size, operation, voltage, signal] for style in styles for size in sizes for operation in operations for voltage in voltages for signal in signals ]

actuatorMaster = pd.DataFrame()
for i in range(len(combos)):
    tempStyle = combos[i][0]
    tempSize = combos[i][1]
    tempVoltage = combos[i][2]
    tempFunction = combos[i][3]
    tempSignal = combos[i][4]
    actuatorMaster = actuatorMaster.append({'Style' : tempStyle,
                           'Size' : tempSize,
                           'Voltage' : tempVoltage,
                           'Function' : tempFunction,
                           'Signal' : tempSignal}, ignore_index = True)
    

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

