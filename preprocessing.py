import pandas as pd


def cleaning_set(dataframe):
    dataframe = dataframe.drop(["None_Experiencing", "Age_0-9", "Age_10-19", "Age_20-24", "Age_25-59",
                                "Age_60+", "Gender_Female", "Gender_Male", "Gender_Transgender", "Severity_Mild",
                                "Severity_Moderate", "Severity_None", "Severity_Severe", "Contact_Dont-Know",
                                "Contact_No", "Contact_Yes", "Country"], axis=1)

    return dataframe


def main():
    try:
        dataframe = pd.read_csv("Cleaned-Data.csv")
        dataframe = cleaning_set(dataframe)
        dataframe.to_csv('Cleaned-Data2.csv', index=False)
        print(dataframe)
    except FileNotFoundError as e:
        print(e)
        print("file not found")


main()
