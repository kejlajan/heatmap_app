import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


cmap_keywords = [
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "coolwarm",
    "jet",
    "gray",
    "spring",
    "summer",
    "autumn",
    "winter",
    "bone",
    "copper",
    "hsv",
    "twilight",
    "twilight_shifted",
    "Set1",
    "Set2",
    "Set3",
    "Dark2",
    "Paired",
]

def load_file_into_DF(file):
    """Load data from a TSV file (uploaded through Streamlit)."""
    return pd.read_csv(file, sep='\t')

def display_data(df, custom_name):
    """Display the data from a dataframe."""
    st.write(f"### Top five rows from: `{custom_name}`")
    st.dataframe(df)

def apply_custom_colnames(list_of_DFs_and_custom_names):
    """Changes the abundance column name to the custom colname for each DF in place."""
    for df, colname in list_of_DFs_and_custom_names:
        df.rename(columns={"abundance":colname}, inplace=True)
    
def get_hierarchy_colname(DF) -> str:
    """Returns the colname of the column that contains hierarchy levels"""    
    for colname in DF.columns:
        for level in colname.split(";"):
            for keyword in ["kingdom", "phylum", "class", "family", "genus", "species"]:
                if keyword.lower() in level.lower():
                    return colname
    return None

def split_hierarchy_column(DF, colname_with_hierarchy):
    """Eats a DF with the name of the column that contains the info about hierarchy.
    Spits out the DF with the hierarchy column split into several other columns"""
    
    # add new columns -- that are from the split -- did not wanna use a for loop for performance issues
    DF[colname_with_hierarchy.split(';')] = DF[colname_with_hierarchy].str.split(';', expand = True)
    
    # return both -- the split colname as a list and the DF with added columns
    return colname_with_hierarchy.split(';'), DF


def plot_data(list_of_DFs_and_custom_names, hierarchy_selection, number_of_records, cmap_color):
    """Plot heatmaps for each passed DF."""
    names = [df_and_name[1] for df_and_name in list_of_DFs_and_custom_names]
    first_df, first_name = list_of_DFs_and_custom_names[0]

    first_df_grouped = split_hierarchy_column(first_df, get_hierarchy_colname(first_df))[1].groupby(by = hierarchy_selection).sum()

    first_df_sorted = first_df_grouped.sort_values(by=first_name, ascending = False)[:number_of_records]

    for index, name_and_DF in enumerate(list_of_DFs_and_custom_names):
        df, name = name_and_DF
        if index == 0:
            pass # ignore the first one
        else:
            # group by hierarchy:
            df = split_hierarchy_column(df, get_hierarchy_colname(df))[1].groupby(by = hierarchy_selection).sum()
            
            # sort by abundance:
            df.sort_values(by=name, ascending = False, inplace = True)

            # cut:
            df = df[:number_of_records]

            # full join to the first df:
            first_df_sorted = first_df_sorted.merge(df, on = hierarchy_selection, how = 'outer')
            
    # get only the colnames that matter
    final_df = first_df_sorted.sort_values(by = first_name, ascending = False)[names]

    col1, col2 = st.columns(2)

    with col1:
        plt.figure(figsize=(6,15))
        sns.heatmap(data = final_df, cmap = cmap_color, annot = True)
        st.pyplot(plt)

    with col2:
        st.dataframe(final_df)

def main():
    st.set_page_config(layout="wide", page_title="tsv2png")
    st.title("TSV Files Viewer")

    # Step 1: File selection
    col_file_select, col_filenames = st.columns(2)
    
    with col_file_select:
        uploaded_files = st.file_uploader(
            "Choose TSV files", 
            type="tsv", 
            accept_multiple_files=True)
    
    if uploaded_files:
        with col_filenames:
            # Step 2: Create a list to store df and custom name associations
            DFs_with_names = []

            # Display a row for each file with an input field for the name
            st.write("### Choose custom column names:")
            for uploaded_file in uploaded_files[::-1]:
                file_name = uploaded_file.name
                # Display input field with default value as the filename
                custom_name = st.text_input(f"Enter a name for the data in `{file_name}`:", value=file_name.split(".")[0], key=file_name)
                # Append the file's dataframe and its custom name to the list
                DFs_with_names.append((load_file_into_DF(uploaded_file), custom_name))

        st.write("---")

        # select a hierarchy level:
        with st.sidebar:
           hierarchy_selection = st.multiselect("Level", get_hierarchy_colname(DFs_with_names[0][0]).split(';'), " species", placeholder="Choose the level of aggregation")
           number_of_records = st.slider("How many top records from each file", 1, 100, 25)
           selected_cmap = st.selectbox("Color scheme", cmap_keywords)

        # Step 3: Display the contents of each file as a dataframe with the custom name
        for df, custom_name in DFs_with_names:
            display_data(df.head(), custom_name)
        
        # change the 'abundance' column into whatever we want this series to be called in the output -- the custom colname
        apply_custom_colnames(DFs_with_names)

        st.write("---")

        # Step 4: Plot the contents of the files
        with st.sidebar:
            plot_heatmap = st.button("Plot heatmap")
                
        if plot_heatmap:        
            st.write("Heatmap plotted!")
            plot_data(DFs_with_names, hierarchy_selection, number_of_records, selected_cmap)
            
    else:
        st.write("Please upload one or more .tsv files.")

if __name__ == "__main__":
    main()