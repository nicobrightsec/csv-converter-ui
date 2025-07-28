import streamlit as st
import pandas as pd
import io
from PIL import Image
import base64
import os
import glob


def main():
    st.set_page_config(page_title="Org ID to Name CSV Converter", page_icon="📄", layout="centered")

    # Theme colors fixed to dark mode
    bg_color = "#1e1e2f"
    font_color = "#ffffff"
    footer_color = "#aaaaaa"

    # Inject CSS animation and styles
    st.markdown(f"""
        <style>
            html, body, [class*="css"]  {{
                background-color: {bg_color};
                color: {font_color};
                font-family: 'Segoe UI', sans-serif;
            }}
            h2, p {{
                animation: fadeInDown 1s ease-in-out;
            }}
            .stButton button {{
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                animation: pulse 1.5s infinite;
            }}
            @keyframes fadeInDown {{
                0% {{opacity: 0; transform: translateY(-20px);}}
                100% {{opacity: 1; transform: translateY(0);}}
            }}
            @keyframes pulse {{
                0% {{box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);}}
                70% {{box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);}}
                100% {{box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);}}
            }}
        </style>
    """, unsafe_allow_html=True)

    def display_banner():
        uploaded_image = st.file_uploader("Optional: Upload Header Image", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_image:
            encoded = base64.b64encode(uploaded_image.read()).decode()
            banner_html = f"""
                <div style='width:100%; padding:10px 0; background-color:{bg_color}; text-align:left;'>
                    <img src='data:image/webp;base64,{encoded}' style='height:35px; margin-left:15px;'>
                </div>
            """
            st.markdown(banner_html, unsafe_allow_html=True)

    display_banner()

    st.markdown(f"<h2 style='color:{font_color}; font-weight:600;'>Org ID to Name CSV Converter</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{font_color};'>Upload the Org Mapping file and either use the latest downloaded Scan Report or upload one manually.</p>", unsafe_allow_html=True)

    org_map_file = st.file_uploader("Upload Org Mapping CSV (with $distinct_id and $name)", type="csv")
    use_latest_file = st.checkbox("Use latest downloaded Scan Report")
    scan_data_file = None

    if use_latest_file:
        download_dir = st.text_input("Path to your Downloads folder", value="/app/downloads")
        pattern = os.path.join(download_dir, "Scan-2621196-*.csv")
        matching_files = sorted(glob.glob(pattern), reverse=True)
        if matching_files:
            scan_data_file = matching_files[0]
        else:
            st.warning("No matching Scan Report file found in the specified Downloads folder.")
    else:
        uploaded_file = st.file_uploader("Upload Scan Report CSV (with org_id)", type="csv")
        if uploaded_file is not None:
            scan_data_file = uploaded_file

    output_filename = st.text_input("Enter output file name (without extension)", value="LongScansReport")

    if st.button("Convert"):
        if not org_map_file or not scan_data_file:
            st.error("Please upload both the Org Mapping and Scan Report CSV files.")
            return

        try:
            df_orgs = pd.read_csv(org_map_file)
            df_scan = pd.read_csv(scan_data_file)

            if "$distinct_id" not in df_orgs.columns or "$name" not in df_orgs.columns or "org_id" not in df_scan.columns:
                st.error("Files must contain correct columns: '$distinct_id', '$name' in orgs, 'org_id' in scan report.")
                return

            org_map = {
                str(row["$distinct_id"]).strip(): str(row["$name"]).strip()
                for _, row in df_orgs.iterrows()
                if pd.notna(row["$distinct_id"]) and pd.notna(row["$name"])
            }

            df_scan.insert(1, "OrgName", df_scan["org_id"].astype(str).str.strip().map(org_map).fillna("Unknown"))

            csv_buffer = io.StringIO()
            df_scan.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode("utf-8")

            file_display = os.path.basename(scan_data_file.name) if hasattr(scan_data_file, 'name') else os.path.basename(scan_data_file)
            st.success(f"CSV conversion successful using: {file_display}")
            st.download_button(
                label="Download Converted CSV",
                data=csv_bytes,
                file_name=f"{output_filename.strip() or 'converted_output'}.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"An error occurred while converting: {e}")

    st.markdown(f"""
        <hr style='margin-top:3rem; border-top: 1px solid #666;'>
        <div style='text-align:center; font-size:13px; color:{footer_color}; margin-top:1rem;'>
            <strong>Coded by: Nicolas Alejandro Bello</strong><br>
            <span style='font-size:12px;'>All rights to BrightSec</span>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
