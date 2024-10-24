import pandas as pd

#test_file.py



def get_hierarchy_colname(DF) -> str:
    """Returns the colname of the column that contains hierarchy levels"""    
    for colname in DF.columns:
        for level in colname.split(";"):
            for keyword in ["kingdom", "phylum", "class", "family", "genus", "species"]:
                if keyword.lower() in level.lower():
                    return colname
    return None
    

df = {
        "ahoj"  :   [1,2,3,7,6,5],
        "omacka" :   ["ahoj", "rad","te", "vidim", "jak", "je"]
      }

df = pd.DataFrame(df)


print(get_hierarchy_colname(df))
