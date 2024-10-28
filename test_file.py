import pandas as pd

#test_file.py


def split_hierarchy_column(DF, colname_with_hierarchy):
    """Eats a DF with the name of the column that contains the info about hierarchy.
    Spits out the DF with the hierarchy column split into several other columns"""
    
    DF[colname_with_hierarchy.split(';')] = DF[colname_with_hierarchy].str.split(';', expand = True)

    return colname_with_hierarchy.split(';'), DF

df = {
        "ahoj"  :   [1,2,3,7,6,5],
        "omacka;brambory;cesnecka" :   ["ahoj;rad;te", "rad;te;vidim","te;vidim;jak", "vidim;jak;je", "jak;je;vole", "je;mi;hezky"]
      }

df = pd.DataFrame(df)


print(split_hierarchy_column(df, "omacka;brambory;cesnecka"))


# df["omacka;brambory;cesnecka".split(';')] = df["omacka;brambory;cesnecka"].str.split(';', expand=True)
# print(df)