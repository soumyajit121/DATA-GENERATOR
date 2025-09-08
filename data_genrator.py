import streamlit as st
import pandas as pd
from faker import Faker
import inspect

f = Faker()

# ✅ Step 1: Safely collect Faker methods
all_methods = []
for m in dir(f):
    if not   m.startswith("_"):  # ignore dunder methods
        try:
            attr = getattr(f, m)
            if callable(attr) and not inspect.isclass(attr):
                all_methods.append(m)
        except Exception:
            continue

# ✅ Step 2: Streamlit UI
st.title("Fake Data Generator")

# Number of rows input
n = st.number_input("Number of rows", min_value=1, max_value=1000000000, value=10)

# Multiselect for Faker providers
selected_fields = st.multiselect("Choose Faker fields", all_methods, default=["name", "email", "phone_number"])

# ✅ Step 3: Generate data if fields selected
if selected_fields:
    data = {}
    for field in selected_fields:
        try:
            method = getattr(f, field)
            data[field] = [method() for _ in range(n)]
        except Exception as e:
            st.warning(f"Skipping {field}: {e}")
    
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "fake_data.csv", "text/csv")
