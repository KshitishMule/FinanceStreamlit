# CSV full form: Comma Separated Values
import streamlit as st               # Streamlit for UI
import pandas as pd                 # Pandas for CSV and data handling
import plotly.express as px         # Plotly for visualizing data (charts)
import json                         # For saving/loading categories to/from a file
import os                           # To check file existence

# Streamlit app page configuration
st.set_page_config(page_title="Simple App", page_icon="💰", layout="wide")

category_file = "categories.json"  # File to save/load categorized keywords

# Initialize categories in session state
if "categories" not in st.session_state:
    if os.path.exists(category_file):
        # Load from file if it exists
        with open(category_file, "r") as f:
            st.session_state.categories = json.load(f)
    else:
        # Default category if no file exists
        st.session_state.categories = {
            "Uncategorized": [],
        }

# Function to save categories to JSON
def save_categories():
    with open("categories.json", "w") as f:
        json.dump(st.session_state.categories, f)

# Function to categorize transactions based on keywords
def categorize_tranctions(df):
    df["Category"] = "Uncategorized"  # Set default category

    # Loop over each defined category
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue  # Skip default or empty categories

        for idx, row in df.iterrows():
            lowered_keywords = [keyword.lower() for keyword in keywords]  # Normalize for comparison
            details = row["Details"].lower().strip()
            if details in lowered_keywords:
                df.at[idx, "Category"] = category  # Assign category if matched

    return df

# Function to load and clean uploaded transactions file
def load_transactions(file):
    try:
        df = pd.read_csv(file)  # Read CSV file into DataFrame
        df.columns = [col.strip() for col in df.columns]  # Remove any spaces in column names
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)  # Clean and convert Amount column
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")  # Convert date format
        if "Category" not in df.columns:
            df["Category"] = "Uncategorized"  # Add if not present
        return categorize_tranctions(df)  # Categorize based on keywords
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# Function to add a keyword to an existing category
def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)  # Add keyword to category
        save_categories()  # Save updates
        return True
    return False

# Main app logic
def main():
    st.title("Simple Dashboard")  # App title

    # File upload widget
    uploaded_file = st.file_uploader("Upload the File In CSV", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)  # Process uploaded file

        if df is not None:
            # Split the DataFrame into debits and credits
            debits_df = df[df["Debit/Credit"] == "Debit"]
            credits_df = df[df["Debit/Credit"] == "Credit"]

            # Save debits in session state to allow editing
            st.session_state.debits_df = debits_df.copy()

            # Create two tabs: Expenses and Payments
            tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])

            with tab1:
                st.subheader("Categorize Your Expenses")

                # Input for adding a new category
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                # Add new category to session state if it doesn't already exist
                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.rerun()  # Refresh UI to show updates

                # Show editable table of expenses (debits only)
                st.subheader("Your Expences")
                edited_df = st.data_editor(
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category", options=list(st.session_state.categories.keys())
                        ),
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )

                # Button to save changes made by user
                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    for idx, row in edited_df.iterrows():
                        new_category = row["Category"]

                        # Skip if no change in category
                        if row["Category"] == st.session_state.debits_df.at[idx, "Category"]:
                            continue

                        # Update session data and add new keyword for future auto-tagging
                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_category
                        add_keyword_to_category(new_category, details)

                    st.session_state.debits_df.update(edited_df)  # Apply all edits
                    st.success("Changes Applied!")  # Show success message

            # Show category-wise expense summary
            st.subheader("Expence Summary")
            category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
            category_totals = category_totals.sort_values("Amount", ascending=False)

            # Show totals as a table
            st.dataframe(
                category_totals,
                column_config={"Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")},
                use_container_width=True,
                hide_index=True
            )

            # Show a pie chart of expenses by category
            fig = px.pie(
                category_totals,
                values="Amount",
                names="Category",
                title="Expenses by Category"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Payments (credits) section
            with tab2:
                st.subheader("Payments (Credits)")
                total_payments = credits_df["Amount"].sum()
                st.metric("Total Payments", f"{total_payments :.2f} AED")  # Show total credits
                st.dataframe(credits_df, use_container_width=True)  # Show all credit entries

# Run the Streamlit app
main()
