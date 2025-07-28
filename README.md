# Org ID to Name CSV Converter

A professional Streamlit-based web application to convert exported Mixpanel scan reports by mapping organization IDs (`org_id`) to friendly organization names using a separate mapping file.

## 🚀 Features

- Upload your Org Mapping CSV (`$distinct_id`, `$name`)
- Automatically detect the latest Mixpanel scan report in your Downloads folder
- OR upload the scan report manually
- Adds an `OrgName` column beside `org_id` with mapped names
- Stylish dark theme with smooth animations
- Instant CSV download of the result

## 🖼️ Optional

You can upload a custom header image (`.png`, `.jpg`, `.webp`) to display your logo at the top.

## 📦 Requirements

- Python 3.8+
- `streamlit`
- `pandas`
- `Pillow`

Install with:

```bash
pip install -r requirements.txt
