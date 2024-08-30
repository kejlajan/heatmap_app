import streamlit as st
import pandas as pd

def load_data(file):
    """Load data from a TSV file."""
    return pd.read_csv(file, sep='\t')

def display_data(df, custom_name):
    """Display the data from a dataframe."""
    st.write(f"### Data for `{custom_name}`")
    st.dataframe(df)

def plot_data(list_of_filenames_and_custom_names:list):
    print("hello")
    

def main():
    st.title("TSV Files Viewer")
    
    # Step 1: File selection
    uploaded_files = st.file_uploader(
        "Choose TSV files", 
        type="tsv", 
        accept_multiple_files=True)

    if uploaded_files:
        # Step 2: Create a list to store file and custom name associations
        files_with_names = []

        # Display a row for each file with an input field for the name
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            # Display input field with default value as the filename
            custom_name = st.text_input(f"Enter a name for the data in `{file_name}`:", value=file_name.split(".")[0], key=file_name)
            # Append the file and its custom name to the list
            files_with_names.append((uploaded_file, custom_name))

        # Step 3: Display the contents of each file as a dataframe with the custom name
        for uploaded_file, custom_name in files_with_names:
            df = load_data(uploaded_file)
            display_data(df, custom_name)

        # step 4: plot the contents of the files:
        if st.button("Plot heatmap"):
            st.write("graphs plotted!")


    else:
        st.write("Please upload one or more .tsv files.")

if __name__ == "__main__":
    main()

