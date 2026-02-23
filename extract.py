import streamlit as st
import pandas as pd

def process_csv(input_file):
    """
    Processes the uploaded CSV file to extract records.
    Supports both formats:
    - Multi-row: Registration, Driver Email, Mobile appear in different rows/columns
    - Single-row: All key-value pairs in columns 2-7 of one row
    """
    df = pd.read_csv(input_file, header=None)

    extracted_records = []
    current_record = {}

    for index, row in df.iterrows():
        row_values = row.tolist()

        for i in range(len(row_values) - 1):
            key = row_values[i]
            value = row_values[i + 1]

            if pd.isna(key) or pd.isna(value):
                continue

            key = str(key).strip()
            value = str(value).strip() if not pd.isna(value) else ""

            if key == "Registration":
                if current_record and current_record.get("Driver Email"):
                    extracted_records.append({
                        "Registration": current_record.get("Registration"),
                        "Email": current_record.get("Driver Email"),
                        "Mobile": current_record.get("Mobile"),
                    })
                current_record = {"Registration": value, "Driver Email": None, "Mobile": None}

            elif key == "Driver Email" and current_record:
                current_record["Driver Email"] = value

            elif key == "Mobile" and current_record:
                current_record["Mobile"] = value

    if current_record and current_record.get("Driver Email"):
        extracted_records.append({
            "Registration": current_record.get("Registration"),
            "Email": current_record.get("Driver Email"),
            "Mobile": current_record.get("Mobile"),
        })

    output_df = pd.DataFrame(extracted_records)
    if not output_df.empty and "Email" in output_df.columns:
        output_df.dropna(subset=["Email"], inplace=True)
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