import pandas as pd
import csv


def save_results(results):
    with open('likelion_9th_Reruiting.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for result in results:
            writer.writerow(result)
