import numpy as np
import matplotlib.pyplot as plt

#Chart of the last non-crisis year based on the ratio of indicator= '# housing crisis debate files' / '# all debate files'

with open(r'C:\TT\NCI2024\2026Jan_ReSit\Phase01\Result_API_XML_NumResults_d1v2.txt', "r") as f01:#Result_Relevance_nb_years_d1v2.txt
    data = []
    next(f01)  # header
    j=0
    for line in f01:#data rows
        element = line.strip().split(",")#break up lines
        data.append(element)
        j+=1
yearData=[]
debateData=[]
for i in range(0,j):
    yearData.append(int(data[i][0]))# data type conversion, year data
    debateData.append(100*(int(data[i][2])/int(data[i][1])))# data type conversion, percentage of ' nb housing crisis' files/ 'nb all files' 

if False:# test
    print(yearData)
    print(yearData[:23])
    for i, value in enumerate(debateData):
        print(f" i, {value:.1f}")
    print(debateData[:23])


# 1st phase: data and plot without trend
if False:# data test
    print("List:", yearData)
    print("List:", debateData)

# Plot 
plt.plot(yearData, debateData, marker="o") 
plt.xlabel("Year")
plt.xticks(yearData[::5]) 
plt.ylabel("Percentage") 
plt.title("Percentage of \n'Number of debate files mentioning housing crisis' /\n ' Number of all debate files'") 
plt.grid(True)
plt.show()

# 2nd phase: split time range into two in numpy at 2012
yearNp00=np.array(yearData)
debateNp00=np.array(debateData)

yearNp01=np.array(yearData[:23])
yearNp02=np.array(yearData[23:])

debateNp01=np.array(debateData[:23])
debateNp02=np.array(debateData[23:])

if False:# data test
    print("Year ranges:", yearNp01, '\n', yearNp02)
    print("Nr debates ranges:",debateNp01, '\n', debateNp02)

# Fit trendlines (linear, quadratic, cubic regression, depending on the settings below)
split01 = np.polyfit(yearNp01, debateNp01, 3)  # b0, b1, b2, ... coefficients
trend01 = np.poly1d(split01)

split02 = np.polyfit(yearNp02, debateNp02, 3)  # # b0, b1, b2, ... coefficients
trend02 = np.poly1d(split02)

if False:# test
    print("phase01: b0, b1=", round(split01[1],1), round(split01[0],1) )
    print("Phase02: b0, b1=", round(split02[1],1), round(split02[0],1) )

# Plot the original + trendlines
#plt.scatter(yearNp00, debateNp00, label="Data", color="black")
plt.plot(yearData, debateData, marker="o", linewidth=1) 
plt.plot(yearNp01, trend01(yearNp01), color="red",  linewidth=3, label="Trend line in [1990;2012]",linestyle="--")
plt.plot(yearNp02, trend02(yearNp02), color="green", linewidth=3, label="Trend line in [2013;2025]")
plt.xlabel("Year")
plt.ylabel("Percentage") 
plt.title("Trend lines \n in [1990;2012] and [2013;2025] \n (nb: 2020: COVID year)")
plt.legend()
plt.grid(True)
plt.show()

