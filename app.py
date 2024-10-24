import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

def plot_data(list_of_DFs_and_custom_names):
    """Plot heatmaps for each passed DF."""
    names = [df_and_name[1] for df_and_name in list_of_DFs_and_custom_names]
    first_df, first_name = list_of_DFs_and_custom_names[0]

    first_df_grouped = first_df.groupby(by = "kingdom; phylum; class; order; family; genus; species").sum()

    for index, name_and_DF in enumerate(list_of_DFs_and_custom_names):
        # st.write(index)
        # st.write(name_and_DF)
        df, name = name_and_DF
        if index == 0:
            pass
        else:
            # group:
            df = df.groupby(by = "kingdom; phylum; class; order; family; genus; species").sum()
            
            # left join to the first df:
            first_df_grouped = first_df_grouped.merge(df, on="kingdom; phylum; class; order; family; genus; species", how = 'left')
    #st.write(first_df_grouped[names])
            
    # # FINAL touches:        
    # # ------------------------- #
    merged_df = first_df_grouped
    # sort values by the first sample:
    merged_df.sort_values(by=first_name, ascending = False, inplace=True)

    # show the top 25
    final_df = merged_df[names][:25]
    st.dataframe(final_df)

    plt.figure(figsize=(6,15))
    sns.heatmap(data = final_df, cmap = "coolwarm", annot = True)
    st.pyplot(plt)

def main():

    st.title("TSV Files Viewer")

    # Step 1: File selection
    uploaded_files = st.file_uploader(
        "Choose TSV files", 
        type="tsv", 
        accept_multiple_files=True)
    
    if uploaded_files:
        # Step 2: Create a list to store df and custom name associations
        DFs_with_names = []

        # Display a row for each file with an input field for the name
        st.write("### Choose custom column names:")
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            # Display input field with default value as the filename
            custom_name = st.text_input(f"Enter a name for the data in `{file_name}`:", value=file_name.split(".")[0], key=file_name)
            # Append the file's dataframe and its custom name to the list
            DFs_with_names.append((load_file_into_DF(uploaded_file), custom_name))

        # debug:
        with st.sidebar:
            st.write("## Debug bar:")
            st.write("debugging:")
            st.write(uploaded_files)

        # group by selected level:
        with st.sidebar:
            st.multiselect(label="Level", options=["laska", "smrt", "pravda", "lez"], placeholder="Choose the level of aggregation")

        # Step 3: Display the contents of each file as a dataframe with the custom name
        for df, custom_name in DFs_with_names:
            display_data(df.head(), custom_name)
        
        # change the 'abundance' column into whatever we want this series to be called in the output -- the custom colname
        apply_custom_colnames(DFs_with_names)

        # Step 4: Plot the contents of the files
        if st.button("Plot heatmap"):
            st.write("Graphs plotted!")
            plot_data(DFs_with_names)
            
    else:
        st.write("Please upload one or more .tsv files.")

if __name__ == "__main__":
    main()