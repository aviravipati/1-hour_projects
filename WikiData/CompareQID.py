from dataExtraction import *


def compareQID(qid1: int, qid2: int):
    print(f"Comparing Q{qid1} and Q{qid2}")
    download(qid1)
    download(qid2)
    dfClaimsQid1 = extractClaims(qid1)
    dfClaimsQid2 = extractClaims(qid2)
    setPValuesQid1 = set(dfClaimsQid1["ClaimValue"].to_list())
    setPValuesQid2 = set(dfClaimsQid2["ClaimValue"].to_list())
    setCommonPValuesQid1Qid2 = setPValuesQid1.intersection(setPValuesQid2)
    setOnlyPValuesQid1 = setPValuesQid1.difference(setPValuesQid2)
    setOnlyPvaluesQid2 = setPValuesQid2.difference(setPValuesQid1)
    print(f"Common P values: {setCommonPValuesQid1Qid2} \n \n")
    print(f"P values only in Qid{qid1}: {setOnlyPValuesQid1}  \n \n")
    print(f"P values only in Qid{qid2}: {setOnlyPvaluesQid2}  \n \n")


def searchAcrossQID(*args: [int], query: str):
    print(args)
    for qid in args:
        print(f"Downloading Q{qid}")
        download(qid)
        dfClaimsQid = extractClaims(qid)
        print(f"Created Claims dataframe for Q{qid}")
        print(f"Search results from Q{id}", searchClaims(dfClaimsQid, query))


if __name__ == "__main__":
    # compareQID(5, 42)
    searchAcrossQID(5, 42, query="Douglas")
