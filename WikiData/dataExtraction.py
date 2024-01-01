"""
    Data Extraction from WikiData
    https://www.wikidata.org/wiki/Special:EntityData/Q42.json
    Save to ./data folder
"""

import json
import requests
import pandas as pd
import os


def download(num: int):
    """
    Extracts the data from WikiData

    """
    print(f"Extracting data from WikiData Q{num}")
    # Define the URL of the JSON file
    url = f"https://www.wikidata.org/wiki/Special:EntityData/Q{num}.json"

    # Define the folder where you want to save the JSON file
    folder_path = "./data/"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the filename from the URL
    filename = os.path.join(folder_path, f"Q{num}.json")

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the JSON content to the specified file
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"JSON file saved to {filename}")
    else:
        print(f"Failed to download JSON file. Status code: {response.status_code}")


def extractLabels(num: int) -> pd.DataFrame:
    entities = []
    folder_path = "./data/"
    filename = os.path.join(folder_path, f"Q{num}.json")
    print(f"Reading JSON file from {filename}")
    # Read the JSON file
    with open(filename) as file:
        data = json.load(file)
    x = 0
    df = pd.DataFrame(columns=["label", "language", "value"])
    labelsDict = {}
    for k, v in data["entities"][f"Q{num}"].items():
        if k.lower() == "labels":
            for labelKey, labelValue in v.items():
                if "label" in labelsDict:
                    labelsDict["label"].append(labelKey)
                else:
                    labelsDict["label"] = [labelKey]
                if "language" in labelsDict:
                    labelsDict["language"].append(labelValue["language"])
                else:
                    labelsDict["language"] = [labelValue["language"]]
                if "value" in labelsDict:
                    labelsDict["value"].append(labelValue["value"])
                else:
                    labelsDict["value"] = [labelValue["value"]]
    df_labels = pd.DataFrame(labelsDict)
    # print(df_labels)
    return df_labels


def extractClaims(num: int) -> pd.DataFrame:
    entities = []
    folder_path = "./data/"
    filename = os.path.join(folder_path, f"Q{num}.json")
    print(f"Reading JSON file from {filename}")
    # Read the JSON file
    with open(filename) as file:
        data = json.load(file)
    x = 0
    claimsDict = {}
    for k, v in data["entities"][f"Q{num}"].items():
        if k.lower() == "claims":
            for claimKey, claimValue in v.items():
                for v in claimValue:
                    if v.get("mainsnak"):
                        claimsDict.setdefault("ClaimValue", []).append(claimKey)
                        claimsDict.setdefault("Value", []).append(
                            v["mainsnak"]["datavalue"]["value"]
                        )
                        claimsDict.setdefault("ValueType", []).append(
                            v["mainsnak"]["datatype"]
                        )
    pd.set_option("display.max_colwidth", None)
    df_claims = pd.DataFrame(claimsDict)
    df_claims_sorted = df_claims.sort_values(by="ValueType")
    df_claims_sorted = df_claims_sorted.reset_index(drop=True)
    # print(df_claims_sorted.head())
    return df_claims_sorted


def searchClaims(df: pd.DataFrame, query: str) -> str:
    return df[df["Value"].astype(str).str.contains(query)]


def minMaxPropertyValue(df: pd.DataFrame) -> (int, int):
    # Convert values to numeric, coercing errors to NaN
    numeric_values = pd.to_numeric(df["Value"], errors="coerce")

    min_value = "{:.2f}".format(
        numeric_values.min()
    )  # Format min value with 2 decimal places
    max_value = "{:.2f}".format(
        numeric_values.max()
    )  # Format max value with 2 decimal places
    return min_value, max_value


if __name__ == "__main__":
    download(42)
    df_Labels = extractLabels(42)
    print("Labels", df_Labels.head())
    df_Claims = extractClaims(42)
    print("Claims", df_Claims.head())
    # print(searchClaims(df, "Douglas"))
    print(minMaxPropertyValue(df_Claims))
