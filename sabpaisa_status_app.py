import streamlit as st
import pandas as pd
import io

st.title("SabPaisa Transaction Status Updater")

# Upload all three files
report_file = st.file_uploader("Upload Reports File", type=["xlsx"])
sabpaisa_04_file = st.file_uploader("Upload SabPaisa 04.05.2025 File", type=["xlsx"])
sabpaisa_05_file = st.file_uploader("Upload SabPaisa 05.05.2025 File", type=["xlsx"])

if report_file and sabpaisa_04_file and sabpaisa_05_file:
    reports_df = pd.read_excel(report_file)
    sp04_df = pd.read_excel(sabpaisa_04_file)
    sp05_df = pd.read_excel(sabpaisa_05_file)

    txn_ids_04 = set(sp04_df['TXN ID'].astype(str))
    txn_ids_05 = set(sp05_df['TXN ID'].astype(str))

    def check_status(txn_id):
        if str(txn_id) in txn_ids_04:
            return "Found in 04.05"
        elif str(txn_id) in txn_ids_05:
            return "Found in 05.05"
        else:
            return "Not Found"

    reports_df['Status'] = reports_df['TXN ID'].apply(check_status)

    st.success("Status column updated successfully.")
    st.dataframe(reports_df)

    output = io.BytesIO()
    reports_df.to_excel(output, index=False)
    st.download_button(
        label="Download Updated Report",
        data=output.getvalue(),
        file_name="Updated_Reports.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
