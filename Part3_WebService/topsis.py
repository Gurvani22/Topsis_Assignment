import sys
import pandas as pd
import numpy as np
import os

def topsis(input_file, weights, impacts, output_file):

    if not os.path.exists(input_file):
        print("Error: File not found.")
        return

    if input_file.endswith('.csv'):
        data = pd.read_csv(input_file)
    elif input_file.endswith('.xlsx'):
        data = pd.read_excel(input_file)
    else:
        print("Error: Only .csv or .xlsx files are supported.")
        return

    if data.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns.")
        return

    numeric_data = data.iloc[:, 1:]

    if not all(np.issubdtype(dtype, np.number) for dtype in numeric_data.dtypes):
        print("Error: Columns must contain numeric values only.")
        return

    weights = weights.split(',')
    impacts = impacts.split(',')

    if len(weights) != len(impacts):
        print("Error: Number of weights and impacts must be same.")
        return

    if len(weights) != numeric_data.shape[1]:
        print("Error: Number of weights must equal number of numeric columns.")
        return

    weights = np.array(weights, dtype=float)

    for impact in impacts:
        if impact not in ['+', '-']:
            print("Error: Impacts must be '+' or '-'.")
            return

    normalized = numeric_data / np.sqrt((numeric_data**2).sum())
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    s_plus = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
    s_minus = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))

    score = s_minus / (s_plus + s_minus)

    data['Topsis Score'] = score
    data['Rank'] = score.rank(ascending=False)

    data.to_csv(output_file, index=False)

    print("Success! Result saved to", output_file)


def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <InputFile> <Weights> <Impacts> <OutputFile>")
        return
    topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
