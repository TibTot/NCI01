import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import pandas as pd
import numpy as np
import tabulate

##      Read cso.ie cencus 2011, 2016, 2022 data after: a) initial data processing, b) CSV to PostgeSQL, c) PostgeSQL to csv phase.
##      Re-coding was necessary for efficient data processing.
##      Restructuring of the Electoral Division (ED) in the 2022 census caused losing some data. It does not impact signifiantly the study results.
##      Data are limited to the need of this phase of the planned study.


dataneed11 = pd.read_csv(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\SQL_queries\ED2011_Result01_d1v3.csv')
dataneed16 = pd.read_csv(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\SQL_queries\ED2016_Result01_d1v3.csv')
dataneed22 = pd.read_csv(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\SQL_queries\ED2022_Result01_d1v3.csv')

# Electoral Division number
dEDCode11=dataneed11.iloc[:,0:1].values
dEDCode16=dataneed16.iloc[:,0:1].values
dEDCode22=dataneed22.iloc[:,0:1].values

# Needed data on ED level 
dataneed11=dataneed11.iloc[:,3:].values#
dataneed16=dataneed16.iloc[:,3:].values#
dataneed22=dataneed22.iloc[:,3:].values#

## State level sum of needed data
dset11=dataneed11.sum(axis=0)
dset16=dataneed16.sum(axis=0)
dset22=dataneed22.sum(axis=0)

## 2011: Split the Theme 2 of census into 3 parts: count Irish born, EU born (incl. UK) and Rest of the World population
EUBorn11=dset11[4]-(dset11[1]+dset11[2]+dset11[3])+dset11[3]*((dset11[4]-(dset11[1]+dset11[2]+dset11[3]))/(dset11[4]-dset11[3]))#old: dset11[4]-(dset11[1]+dset11[2]+dset11[3]*(dset11[1]+dset11[2])/dset11[4])
RoWBorn11=dset11[4]-dset11[1]-EUBorn11#dset11[4]-(dset11[1]+EUBorn11)
IrishBorn11= dset11[1]

#2016:
EUBorn16=dset16[3]-(dset16[1]+dset16[2])
RoWBorn16=dset16[2]
IrishBorn16= dset16[1]

#2022: data: population by location of birth
EUBorn22=dset22[3]-(dset22[1]+dset22[2]+dset22[4])
RoWBorn22=dset22[2]+dset22[4]#dset22[3]-(dset22[1]+EUBorn22)
IrishBorn22= dset22[1]#dset22[12]=EUBorn22# faulty overwrite

# Create 2012 dataset: as the last non-"housing crisis" year: ASSUMPTION: linear change between 2011 and 2016
dset12=[0]*16

## 2012:   Calculation based on 2011 and 2016 data: assumption: linear change
for i in range(0,2):
    dset12[i]=dset11[i]+(dset16[i]-dset11[i])/(2016-2011)# [0]=total; [1]=IEBorn

dset12[3]=dset11[4]+(dset16[3]-dset11[4])/(2016-2011)#[3]=total birthplace. [2] and [4] are not contain values.

for i in range(5,13):
     dset12[i]=dset11[i]+(dset16[i-1]-dset11[i])/(2016-2011)     

EUBorn12=EUBorn11+(EUBorn16-EUBorn11)/(2016-2011)
RoWBorn12=RoWBorn11+(RoWBorn16-RoWBorn11)/(2016-2011)
IrishBorn12= dset12[1]

# for plot01
years = [2011, 2012, 2016, 2022]
IrishBorn = [dset11[1], dset12[1], dset16[1], dset22[1]]
EUBorn = [EUBorn11, EUBorn12, EUBorn16, EUBorn22]
RestofWorldBorn = [RoWBorn11, RoWBorn12, RoWBorn16, RoWBorn22]

# Plot lines
plt.figure(figsize=(7,4))#(figsize=(8,5))
# setting facecolor and background with fig ax
plt.plot(years, IrishBorn, marker='o', label='Irish Born')
plt.plot(years, EUBorn, marker='x', label='EU Born')
plt.plot(years, RestofWorldBorn, marker='*', label='Rest of World Born')
for x, y in zip(years, IrishBorn):
    plt.text(x, y, f"{y:,.0f}", ha='center', va='bottom', fontsize=6)
for x, y in zip(years, EUBorn):
    plt.text(x, y, f"{y:,.0f}", ha='center', va='bottom', fontsize=6)
for x, y in zip(years, RestofWorldBorn):
    plt.text(x, y, f"{y:,.0f}", ha='center', va='bottom', fontsize=6)
# Labels and title
plt.xlabel("Year")
plt.ylabel("Number of Births")
plt.yticks(range(0, 5000000, 500000), fontsize=8)# 500,000 births step
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.gca().yaxis.set_minor_locator(MultipleLocator(500000))
plt.gca().yaxis.set_major_locator(MultipleLocator(1000000))
plt.grid(which='major', color='gray', linestyle='-', linewidth=0.8)
plt.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)
plt.title("Population by origin (2011, 2012 (est.), 2016, 2022)")
plt.legend()
plt.grid(True)
plt.xticks(range(2011, 2023, 1))# 1 year step
# Save and show chart
plt.savefig(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\FinalChart01_d1v1.png')
plt.show()

## Create homogenous indexes for a new 2016: a dset16a (with 2012 indexes = 2022 indexes)
dset16a=np.array([0]*14)

for i in range (0,2):
    dset16a[i]=dset16[i]
    # There is not a [2] and [4] in this coding.
dset16a[3]=dset16[3]  

for i in range (5,13):
    dset16a[i]=dset16[i-1]

## Create  1st level indicator table
Indicator01=np.array([[0.00]*8]*17)# 20 indicators

Opin01=np.array([[None]*12]*40)# Max. 12 parts of the opinion, max 40 opinions.

# code 0/7: nr total population / nr households
Indicator01[0][1]=dset12[0]/dset12[7]
Indicator01[0][2]=dset16a[0]/dset16a[7]
Indicator01[0][3]=dset22[0]/dset22[7]

#Delta%: 2016/2012; 2022/2016; 2022/2012
Indicator01[0][5]=100*(Indicator01[0][2]/Indicator01[0][1]-1)
Indicator01[0][6]=100*(Indicator01[0][3]/Indicator01[0][2]-1)
Indicator01[0][7]=100*(Indicator01[0][3]/Indicator01[0][1]-1)


Opin01[0][0]=" The (Population / Total number of households) in 2012, 2016, 2022:" + format(round(Indicator01[0][1],2))+", " +format(round(Indicator01[0][2],2))+", "+format(round(Indicator01[0][3],2))+". It has not changed significantly between 2022 and 2012. Moreover, in 2022 it is slightly lower than its 2016 value. The average size of households is stable in time."
print ('\n',Opin01[0][0],'\n')

years01 = [2012, 2016, 2022]
Population_per_Households = [Indicator01[0][1], Indicator01[0][2], Indicator01[0][3]]

# Plot lines
plt.figure(figsize=(8,5))
plt.plot(years01, Population_per_Households, marker='o', label='Irish Born')
plt.xlabel("Year")
plt.ylabel("Population_per_Households")
for x, y in zip(years01, Population_per_Households):
    plt.text(x, y, f"{y:,.2f}", ha='center', va='bottom', fontsize=8)
plt.yticks(range(0, 5, 1))# 1 step
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.2f}"))
plt.gca().yaxis.set_minor_locator(MultipleLocator(0.5))
plt.gca().yaxis.set_major_locator(MultipleLocator(1))
plt.grid(which='major', color='gray', linestyle='-', linewidth=0.8)
plt.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)
plt.title("Population_per_Households (2012–2022)")
#plt.legend("Pop/Hholds")
plt.grid(True)
plt.xticks(range(2011, 2023, 1))# 1 year step
# Save and show chart
plt.savefig(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\FinalChart02_d1v1.png')
plt.show()

#code 10/12: total person in dwellings / total dwelling
Indicator01[1][1]=dset12[10]/dset12[12]
Indicator01[1][2]=dset16a[10]/dset16a[12]
Indicator01[1][3]=dset22[10]/dset22[12]
print('\n',"total nr person in dwellings / total nr dwelling")

#Delta%
Indicator01[1][5]=100*(Indicator01[1][2]/Indicator01[1][1]-1)# 2016 / 2012 -1
Indicator01[1][6]=100*(Indicator01[1][3]/Indicator01[1][2]-1)# 2022 / 2016 -1
Indicator01[1][7]=100*(Indicator01[1][3]/Indicator01[1][1]-1)# 2022 / 2012 -1

Opin01[1][0]="There is a significant increase in the indicator of Total number of persons / Total number of dwellings between 2012 and 2022. In 2012, 2016, 2022 it was "  + format(round(Indicator01[1][1],2))+", " +format(round(Indicator01[1][2],2))+", "+format(round(Indicator01[1][3],2))+", which means that 100 dwellings served 5 more people in 2016 compared to 2012 and another 5 more in 2022. In percentages: The majority of growth is between [2012; 2016] in 4 years: "+ format(round(Indicator01[1][5],1))+"%. Over the next 6 years, growth was :"+ format(round(Indicator01[1][6],1))+"%, as a multiplicator over the previous 4 years, resulting "+ format(round(Indicator01[1][7],1))+"%, between 2022 and 2012 in total."
print (Opin01[1][0],'\n')
Opin01[2][0]="The Delta percentage (i.e. second-level) indicators detail the dynamics of change."
print (Opin01[2][0],'\n')
print('\n',"Total nr persons in dwellings / Total nr dwellings: 2012, 2016, 2022.")
for i in range(1,4):print("Indicator01[1][",i,"]",f"{Indicator01[1][i]:.2f}")

print('\n',"Delta%: 2016 vs 2012, 2022 vs 2016, 2022 vs 2012")
for i in range(5,8):print("Indicator01[1][",i,"]",f"{Indicator01[1][i]:.2f}")

years01 = [2012, 2016, 2022]
PeopleDwellings_per_Dwellings = [Indicator01[1][1], Indicator01[1][2], Indicator01[1][3]]

# Plot lines
plt.figure(figsize=(8,5))
plt.plot(years01, PeopleDwellings_per_Dwellings, marker='o', label='Irish Born')
plt.xlabel("Year")
plt.ylabel("People_per_Dwellings")
for x, y in zip(years01, PeopleDwellings_per_Dwellings):
    plt.text(x, y, f"{y:,.2f}", ha='center', va='bottom', fontsize=12)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.2f}"))
plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
plt.gca().yaxis.set_major_locator(MultipleLocator(1))
plt.ylim(2, 3)
plt.grid(which='major', color='gray', linestyle='-', linewidth=0.8)
plt.grid(which='minor', color='lightgray', linestyle='--', linewidth=0.5)
plt.title("People_per_Dwellings (2012–2022)")
plt.grid(True)
plt.xticks(range(2011, 2023, 1))# 1 year step
# Save and show chart
plt.savefig(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\FinalChart03_d1v1.png')
plt.show()




# code 0/11 #Tot population / # Occupied dwellings
Indicator01[2][1]=dset12[0]/dset12[11]
Indicator01[2][2]=dset16a[0]/dset16a[11]
Indicator01[2][3]=dset22[0]/dset22[11]

#Delta%
Indicator01[2][5]=100*(Indicator01[2][2]/Indicator01[2][1]-1)
Indicator01[2][6]=100*(Indicator01[2][3]/Indicator01[2][2]-1)
Indicator01[2][7]=100*(Indicator01[2][3]/Indicator01[2][1]-1)
#print('\n',"nr of popupation / # Occupied dwellings:2012, 2016, 2022. Delta%: 2016 vs 2012, 2022 vs 2016, 2022 vs 2012")
#for i in range(1,8):print("Indicator01[2][",i,"]:",f"{Indicator01[2][i]:.2f}")# for test

# code 8/5: nr HouseBungalowPerson / nr HouseBungalow
Indicator01[3][1]=dset12[8]/dset12[5]
Indicator01[3][2]=dset16a[8]/dset16a[5]
Indicator01[3][3]=dset22[8]/dset22[5]

#Delta%
Indicator01[3][5]=100*(Indicator01[3][2]/Indicator01[3][1]-1)
Indicator01[3][6]=100*(Indicator01[3][3]/Indicator01[3][2]-1)
Indicator01[3][7]=100*(Indicator01[3][3]/Indicator01[3][1]-1)
#print('\n',"nr HouseBungalowPerson / nr HouseBungalow:2012, 2016, 2022. Delta%: 2016 vs 2012, 2022 vs 2016, 2022 vs 2012")
#for i in range(1,8):print("Indicator01[3][",i,"]:",f"{Indicator01[3][i]:.2f}")# for test



# code 9/6: "nr FlatApartPerson / nr FlatApart"
Indicator01[4][1]=dset12[9]/dset12[6]
Indicator01[4][2]=dset16a[9]/dset16a[6]
Indicator01[4][3]=dset22[9]/dset22[6]

#Delta%
Indicator01[4][5]=100*(Indicator01[4][2]/Indicator01[4][1]-1)
Indicator01[4][6]=100*(Indicator01[4][3]/Indicator01[4][2]-1)
Indicator01[4][7]=100*(Indicator01[4][3]/Indicator01[4][1]-1)
#print('\n',"nr FlatApartPerson / nr FlatApart:2012, 2016, 2022. Delta%: 2016 vs 2012, 2022 vs 2016, 2022 vs 2012")
#for i in range(1,8):print("Indicator01[4][",i,"]:",f"{Indicator01[4][i]:.2f}")# for test
Opin01[3][0]="The number of people living in Flat and apartments has increased substantially in 2012, 2016, 2022:" + format(round(Indicator01[4][1],2))+", " +format(round(Indicator01[4][2],2))+", "+format(round(Indicator01[4][3],2))+"."
Opin01[4][0]=" Also in the [2012; 2016] was the period for most of the growth, which means that 100 flats/apartments served 11 more people in 2016 compared to 2012 and another 6 more in 2022, so it is flatter  in [2016; 2022]."
print('\n', Opin01[3][0], '\n',Opin01[4][0])

## Indicators , level 2: explain the level 1 numbers and further research

# Dwelling shortage @2022:
Indicator01[6][1]=dset22[0]/Indicator01[1][1]-dset22[12]#  population 2022 / (average people/dwelling2012)- number of dwellings 2022

# New dwelling request 2022-2030:
Indicator01[6][2]=((dset22[0]-dset16a[0])/(2022-2016))*(2030-2022)# expected population increasing [2022-2030]
Indicator01[6][3]=Indicator01[6][2]/Indicator01[1][1]# 

# Total need for dwellings  in 2022-2030:
Indicator01[6][4]=Indicator01[6][1]+Indicator01[6][3]
Opin01[5][0]="1) The Shortage (2012 - 2022) (K dwellings): "+ format(round(Indicator01[6][1]/1000,0))
Opin01[6][0]="2) The New needs (2022 -2030) (K dwellings): "+ format(round(Indicator01[6][3]/1000,0))
Opin01[7][0]="3) The Total shortage (2022-2030)(sum of two results above) (K dwellings): "+ format(round(Indicator01[6][4]/1000,0))
Opin01[8][0]="4) This 'Total shortage' result should be compared to the 300K in Government' communication of early 2025."


print('\n', f"Final results (K dwellings): \n1) Shortage (2012 - 2022): {Indicator01[6][1]/1000:,.0f}")
print(f"2) New needs (2022 -2030) {Indicator01[6][3]/1000:,.0f}")
print(f"3) Total shortage (2022-2030)(sum of two results above): {Indicator01[6][4]/1000:,.0f} ")
print(f"4) This 'Total shortage' result should be compared to the 300 in Government communication of early 2025.")

#for i in range(5,9):print('\n',Opin01[i][0])#"Indicator01[1][",i,"]",f"{Indicator01[1][i]:.2f}")

with open(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\ReportResult01_d1v1.txt', "w") as f: 
    for i in range (0,9):
        f.write('\n')
        f.write(Opin01[i][0])
        f.write('\n')