

# 💰 FinanceStreamlit

A simple yet powerful Streamlit web application to **analyze and categorize personal finance transactions** from CSV files. Users can upload bank/exported statements, assign categories, visualize spending, and track payments with ease.

---

## 🚀 Features

- 📂 **Upload CSV Files**: Accepts transaction files in CSV format.
- 🧠 **Auto Categorization**: Matches transaction descriptions to saved keywords for fast classification.
- ✍️ **Manual Categorization**: Edit categories directly via an interactive table.
- 🏷️ **Smart Learning**: Adds transaction descriptions as keywords to improve future auto-tagging.
- 📊 **Expense Visualization**:
  - Pie chart by category
  - Table summary of total spending
- 💸 **Credit Tracking**: View total credit (payments) with a breakdown.
- 💾 **Persistent Category Storage**: Saves user-defined categories in `categories.json`.


## 🛠️ Installation

**Clone the repository**
   git clone https://github.com/KshitishMule/FinanceStreamlit.git
   cd FinanceStreamlit
pip install -r requirements.txt
streamlit run finance.py
FinanceStreamlit/
│
├── finance.py       

       # Main Streamlit app
├── categories.json    

     # Saved categories and keywords (auto-created)
├── requirements.txt  

      # Python dependencies
└── README.md               # You're here!
# ✅ TODO / Improvements
 Add filters by month/date range

 Export categorized data as CSV

 Dark mode or theming

 User authentication for multi-user use

📚 Dependencies
Streamlit

Pandas

Plotly

[JSON, OS] (standard Python libraries)

