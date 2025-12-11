import streamlit as st
import pandas as pd

def process_csv(input_file):
    """
    Processes the uploaded CSV file to extract records.
    """
    # Load the file without a header from the uploaded file object
    df = pd.read_csv(input_file, header=None)

    # Rename the relevant columns for clarity
    df.rename(columns={2: 'Key1', 3: 'Value1', 4: 'Key2', 5: 'Value2', 6: 'Key3', 7: 'Value3'}, inplace=True)

    extracted_records = []
    current_record = {}

    for index, row in df.iterrows():
        # 1. Check for the start of a new record (Row with 'Registration')
        if row.get('Key1') == 'Registration':
            # If we have an existing record with an email, save it
            if current_record:
                extracted_records.append({
                    'Registration': current_record.get('Registration'),
                    'Email': current_record.get('Driver Email'),
                    'Mobile': current_record.get('Mobile')
                })
            # Start a new record dictionary
            current_record = {}

        # 2. Extract Key-Value pairs across the row
        if pd.notna(row.get('Key1')) and row.get('Key1') == 'Registration':
            current_record[row['Key1']] = row['Value1']

        if pd.notna(row.get('Key2')) and row.get('Key2') == 'Driver Email':
            current_record[row['Key2']] = row['Value2']

        if pd.notna(row.get('Key3')) and row.get('Key3') == 'Mobile':
            current_record[row['Key3']] = row['Value3']

    # 3. Add the final record after the loop finishes, if it has an email
    if current_record:
        extracted_records.append({
            'Registration': current_record.get('Registration'),
            'Email': current_record.get('Driver Email'),
            'Mobile': current_record.get('Mobile')
        })
    
    output_df = pd.DataFrame(extracted_records)
    output_df.dropna(subset=['Email'], inplace=True)
    return output_df

# --- Streamlit User Interface ---

st.title('Customer Data Extractor')

st.write("Upload a CSV file to extract registration, email, and mobile phone information.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    st.write("---")
    st.header("Optional Columns")

    # --- Location Column ---
    add_location = st.checkbox("Add 'Location' column to the output", True)
    location_value = ""
    if add_location:
        location_options = ["Bayswater Hastings - BYD", "Custom"]
        selected_location = st.selectbox("Select a Location", options=location_options)
        
        if selected_location == "Custom":
            location_value = st.text_input("Enter location")
        else:
            location_value = selected_location

    # --- Brand Column ---
    add_brand = st.checkbox("Add 'Brand' column to the output", True)
    brand_value = ""
    if add_brand:
        brand_options = ["BYD", "Custom"]
        selected_brand = st.selectbox("Select a Brand", options=brand_options)

        if selected_brand == "Custom":
            brand_value = st.text_input("Enter brand")
        else:
            brand_value = selected_brand

    st.write("---")

    if st.button("Process Data"):
        with st.spinner('Extracting records...'):
            output_df = process_csv(uploaded_file)

            # Add optional columns if the user has checked the boxes and provided values
            if add_location and location_value:
                output_df['Location'] = location_value
            
            if add_brand and brand_value:
                output_df['Brand'] = brand_value

            st.success('Processing Complete!')

            st.write("### Extracted Data Preview")
            st.dataframe(output_df)

            # Prepare data for download
            csv_data = output_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Extracted Data as CSV",
                data=csv_data,
                file_name='extracted_records.csv',
                mime='text/csv',
            )