import sys
# print("Output from Python")
# print("Amount: " + sys.argv[1],end=",")
# print("Time: " + sys.argv[2],end=",")
# print("Safety: " + sys.argv[3],end=",")
import numpy as np
import re
import pandas as pd
import os

if os.path.exists("table.html"):
    os.remove("table.html")
# Define the dataset
data = {
    "Type of Investment": ["Post Office FD", "Post Office FD", "Post Office FD", "Post Office FD", "Bank FD", "Bank FD", "Bank FD", "SIP", "Mutual Fund", "Gold Bar Investment", "Gold Jewellery", "Stocks"],
    "Return Rate": [6.9, 7, 7, 7.5, 6.8, 6.5, 6.5, 14, 10, 13, 13, 21.5],
    "Risk Level": [0, 0, 0, 0, 1, 1, 1, 2, 3, 1, 1, 4],
    "Term-Bond": [1, 2, 3, 5, 1, 3, 5, 0, 0, 0, 0, 0],
    "Tax Imposed": [0, 0, 0, 0, 0.1, 0.1, 0.1, 0.13, 0.15, 0.03, 0.11, 0.15],
    "Minimum Investment": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 500, 1000, 6000, 6000, 25],
    "Ease of Management": [4, 4, 4, 4, 3, 3, 3, 2, 2, 5, 5, 1]
}

# Create a DataFrame
data = pd.DataFrame(data)

# Get user input for the amount
user_amount  = int(sys.argv[2])
#Filter the DataFrame to include investments with initial investments less than the user input amount
filtered_df = data[data["Minimum Investment"] < user_amount]
# print(filtered_df)
# Calculate the differences between the user input amount and initial investments
filtered_df["Difference"] = abs(filtered_df["Minimum Investment"] - user_amount)

# Sort the filtered DataFrame by investment type and then by the differences
sorted_df = filtered_df.sort_values(["Type of Investment", "Difference"])

# Drop duplicates and keep the first occurrence of each investment type
final_df = sorted_df.drop_duplicates("Type of Investment")

# Drop the "Difference" column
data = final_df.drop(columns=["Difference"])



# data.dict_reader()
# Processing the data
collect_numbers = lambda x: [int(i) for i in re.split("[^0-9]", x) if i != ""]
# temp = "5"
# numbers = "1,1,${temp},1,1,1"  # Provide your weights as a string, e.g., "1, 2, 3"
# print(numbers)
weight_input_1 = 10
weight_input_2 = int(sys.argv[4])
weight_input_3 = int(sys.argv[3])
weight_input_4 = 1
weight_input_5 = 10
weight_input_6 = int(sys.argv[5])
weights = [weight_input_1, weight_input_2, weight_input_3, weight_input_4, weight_input_5, weight_input_6]

string = "+,-,-,-,-,+"  # Provide your impact values as a string, e.g., "+,-"
impact = string.split(",")
#weights = collect_numbers(numbers)

df = data.drop(data.columns[[0]], axis=1)

sos = []
for i in range(df.shape[1]):
    sum = 0
    for j in range(df.shape[0]):
        sum = sum + df.iloc[j, i] ** 2
    sos.append(sum)

rosos = np.sqrt(sos)

for i in range(df.shape[1]):
    for j in range(df.shape[0]):
        df.iloc[j, i] = df.iloc[j, i] / rosos[i]

for i in range(df.shape[1]):
    for j in range(df.shape[0]):
        df.iloc[j, i] = df.iloc[j, i] * weights[i]

idbest = []
idworst = []

for i in range(df.shape[1]):
    if impact[i] == "+":
        idbest.append(df.iloc[:, 1].max(axis=0))
        idworst.append(df.iloc[:, 1].min(axis=0))
    elif impact[i] == "-":
        idbest.append(df.iloc[:, 1].min(axis=0))
        idworst.append(df.iloc[:, 1].max(axis=0))

sp = []
sn = []
for i in range(df.shape[0]):
    sump = 0
    sumn = 0
    for j in range(df.shape[1]):
        sump = sump + (df.iloc[i, j] - idbest[j]) ** 2
        sumn = sumn + (df.iloc[i, j] - idworst[j]) ** 2
    sp.append(sump)
    sn.append(sumn)

sp = np.sqrt(sp)
sn = np.sqrt(sn)
time_period=2
p = []
tim = []
for i in range(df.shape[0]):
    p.append(sn[i] / (sp[i] + sn[i]))
    ci=user_amount *(1 +(df.iloc[i]["Return Rate"])/100) ** time_period
    ta=ci-((df.iloc[i]["Tax Imposed"])*ci)
    tim.append(ta)

data["P"] = p
data["Rank"] = data["P"].rank()
data["Investment Value after the time"] = tim
sorted_data = data.sort_values(by='Rank')[['Type of Investment','Risk Level', 'Return Rate', 'Investment Value after the time', 'Rank']]
sorted_data=sorted_data.head(3)
# print(sorted_data)
table = "<table>"
table += "<tr><th>Type of Investment</th><th>Risk Level</th><th>Return Rate</th><th>Investment Value after the time</th><th>Rank</th></tr>"
for i in range(len(sorted_data)):
    table += "<tr>"
    table += "<td>" + sorted_data["Type of Investment"].iloc[i] + "</td>"
    table += "<td>" + str(sorted_data["Risk Level"].iloc[i]) + "</td>"
    table += "<td>" + str(sorted_data["Return Rate"].iloc[i]) + "</td>"
    table += "<td>" + str(sorted_data["Investment Value after the time"].iloc[i]) + "</td>"
    table += "<td>" + str(sorted_data["Rank"].iloc[i]) + "</td>"
    table += "</tr>"
table += "</table>"

print(table)

with open("table.html", "w") as file:
    file.write(table)
