# import streamlit as st
# import pandas as pd
# import requests
# import smtplib
# import os
# import PyPDF2
# from io import BytesIO
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Load environment variables
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = "gemma2-9b-it"
# SENDER_EMAIL = os.getenv("EMAIL_USER")
# SENDER_PASSWORD = os.getenv("EMAIL_PASS")

# # Streamlit UI Setup
# st.set_page_config(page_title="AI Customer Support", page_icon="🤖", layout="wide")
# st.title("🤖 AI-Powered Smartphone Customer Support")
# st.markdown("Enhance customer experience with AI-driven responses! 🚀")

# role = st.sidebar.selectbox("Select Role:", ["User", "Admin"], help="Admin can upload data, User can only ask questions.")

# # Function to upload product data (Admin only)
# def upload_product_data():
#     uploaded_file = st.file_uploader("📂 Upload smartphone data (CSV/Excel)", type=["csv", "xlsx"], help="Admin can upload the smartphone product dataset.")
#     if uploaded_file is not None:
#         if uploaded_file.name.endswith('.csv'):
#             product_data = pd.read_csv(uploaded_file)
#         else:
#             product_data = pd.read_excel(uploaded_file)

#         st.session_state['product_data'] = product_data
#         st.success("✅ Product data uploaded successfully!")

# def load_product_data():
#     return st.session_state.get('product_data', None)

# # Function to upload customer queries (Admin only)
# def upload_customer_queries():
#     uploaded_file = st.file_uploader("📂 Upload customer queries (CSV, Excel, PDF)", type=["csv", "xlsx", "pdf"], help="Admin can upload customer queries.")
#     if uploaded_file is not None:
#         if uploaded_file.name.endswith('.csv'):
#             data = pd.read_csv(uploaded_file)
#         elif uploaded_file.name.endswith('.xlsx'):
#             data = pd.read_excel(uploaded_file)
#         elif uploaded_file.name.endswith('.pdf'):
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
#             data = pd.DataFrame({"Query": text.split("\n")})  # Convert PDF text into DataFrame

#         st.session_state['customer_queries'] = data
#         st.success("✅ Customer queries uploaded successfully!")

# def load_customer_queries():
#     return st.session_state.get('customer_queries', None)

# # AI Response Generation
# # def generate_response(query, product_data):
# #     if product_data is None:
# #         return "⚠️ No product data available. Admin needs to upload the dataset."

# #     words = query.lower().split()
# #     quantity = 1
# #     for i, word in enumerate(words):
# #         if word.isdigit():
# #             quantity = int(word)
# #             break

# #     relevant_products = product_data[product_data['model'].str.contains("iphone 11", case=False, na=False)]

# #     if not relevant_products.empty:
# #         row = relevant_products.iloc[0]
# #         price_per_unit = row.get('price', 'N/A')
# #         stock = row.get('stock', 'N/A')
# #         condition = row.get('condition', 'N/A')
# #         total_cost = price_per_unit * quantity if price_per_unit != 'N/A' else 'N/A'

# #         return (
# #             f"📱 iPhone 11 Details:\n"
# #             f"💰 Price per unit: ₹{price_per_unit}\n"
# #             f"🛒 Quotation for {quantity} units: ₹{total_cost}\n"
# #             f"📦 Stock: {stock}\n"
# #             f"✅ Condition: {condition}"
# #         )
# #     else:
# #         return "⚠️ iPhone 11 details are not available in the uploaded dataset."

# def generate_response(query, product_data):
#     if product_data is None:
#         return "⚠️ No product data available. Please upload the dataset."

#     words = query.lower().split()
#     quantity = 1
#     for i, word in enumerate(words):
#         if word.isdigit():
#             quantity = int(word)
#             break

#     relevant_products = product_data[product_data['model'].str.contains("iphone 11", case=False, na=False)]

#     if not relevant_products.empty:
#         row = relevant_products.iloc[0]
#         price_per_unit = row.get('price', 'N/A')
#         stock = row.get('stock', 'N/A')
#         condition = row.get('condition', 'N/A')
#         total_cost = price_per_unit * quantity if price_per_unit != 'N/A' else 'N/A'

#         return f"iPhone 11: ₹{price_per_unit} each. {quantity} units cost ₹{total_cost}. Stock: {stock}. Condition: {condition}."
#     else:
#         return "iPhone 11 details are unavailable."


# # Email sending function
# def send_email(to_email, subject, body):
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = to_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

# # Admin: Upload Data
# if role == "Admin":
#     st.sidebar.subheader("📂 Admin Panel")
#     upload_product_data()
#     upload_customer_queries()

# # User & Admin: Q&A Section
# st.header("💬 Chatbot Q&A")
# user_query = st.text_input("🔍 Ask a question about smartphones:", help="Type your smartphone-related question here.")
# product_data = load_product_data()

# if user_query:
#     chatbot_response = generate_response(user_query, product_data)
#     st.success(f"**AI Response:** {chatbot_response}")

# # Admin: Process Customer Queries and Send Emails
# data = load_customer_queries()
# if role == "Admin" and data is not None and not data.empty:
#     st.header("📧 Email Automation")
#     email_options = st.radio("Select Email Mode:", ("📂 Manual Review", "⚡ Automatic Send"))

#     if email_options == "📂 Manual Review":
#         for index, row in data.iterrows():
#             email = row.get('Customer Email', '')
#             query = row.get('Query', '')

#             if email and query:
#                 ai_response = generate_response(query, product_data)
#                 st.subheader(f"📩 Email to: {email}")
#                 st.text_area(f"✉️ Generated Response for {email}", ai_response, height=150, key=f"response_{index}")
#                 if st.button(f"📤 Send Email to {email}"):
#                     send_email(email, "Smartphone Support Response", ai_response)
#                     st.success(f"✅ Email sent to {email}")
#             else:
#                 st.warning("⚠️ Missing email or query in the dataset.")

#     elif email_options == "⚡ Automatic Send":
#         if st.button("🚀 Send All Emails Automatically"):
#             for index, row in data.iterrows():
#                 email = row.get('Customer Email', '')
#                 query = row.get('Query', '')

#                 if email and query:
#                     ai_response = generate_response(query, product_data)
#                     send_email(email, "Smartphone Support Response", ai_response)
#                 else:
#                     st.warning(f"⚠️ Skipping row {index} due to missing email or query.")
#             st.success("✅ All emails sent successfully!")

# 2nd
# import streamlit as st
# import pandas as pd
# import requests
# import smtplib
# import os
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Load environment variables
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = "gemma2-9b-it"
# SENDER_EMAIL = os.getenv("EMAIL_USER")
# SENDER_PASSWORD = os.getenv("EMAIL_PASS")

# st.set_page_config(page_title="AI Customer Support", page_icon="🤖", layout="wide")
# st.title("🤖 AI-Powered Smartphone Customer Support")
# st.markdown("Enhance customer experience with AI-driven responses! 🚀")
# role = st.sidebar.selectbox("Select Role:", ["User", "Admin"], help="Admin can upload data, User can only ask questions.")

# def upload_product_data():
#     uploaded_file = st.file_uploader("📂 Upload smartphone data CSV (Admin only)", type=["csv"])
#     if uploaded_file is not None:
#         st.session_state['product_data'] = pd.read_csv(uploaded_file)
#         st.success("✅ Product data uploaded successfully!")

# def upload_customer_queries():
#     uploaded_file = st.file_uploader("📂 Upload customer queries (CSV, Excel, PDF)", type=["csv", "xlsx", "xls", "pdf"])
#     if uploaded_file is not None:
#         ext = uploaded_file.name.split('.')[-1]
#         if ext in ['csv']:
#             st.session_state['customer_queries'] = pd.read_csv(uploaded_file)
#         elif ext in ['xlsx', 'xls']:
#             st.session_state['customer_queries'] = pd.read_excel(uploaded_file)
#         st.success("✅ Customer queries uploaded successfully!")

# def load_product_data():
#     return st.session_state.get('product_data', None)

# def load_customer_queries():
#     return st.session_state.get('customer_queries', None)

# def generate_response(query, product_data):
#     refund_keywords = ["refund", "return", "damaged", "broken"]
#     if any(word in query.lower() for word in refund_keywords):
#         return "Your order is eligible for a return. Please contact support."
    
#     if product_data is None:
#         return "⚠️ No product data available. Admin needs to upload the dataset."
    
#     relevant_products = product_data[product_data['model'].str.contains(query, case=False, na=False)]
#     if not relevant_products.empty:
#         row = relevant_products.iloc[0]
#         return f"{row['model']}: ₹{row['price']}. Stock: {row.get('stock', 'N/A')}. Condition: {row.get('condition', 'N/A')}."
    
#     return "Product details not available. Please check with the store."

# def send_email(to_email, subject, body):
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = to_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

# if role == "Admin":
#     st.sidebar.subheader("📂 Admin Panel")
#     upload_product_data()
#     upload_customer_queries()

# st.header("💬 Chatbot Q&A")
# user_query = st.text_input("🔍 Ask a question about smartphones:")
# product_data = load_product_data()
# if user_query:
#     chatbot_response = generate_response(user_query, product_data)
#     st.success(f"**AI Response:** {chatbot_response}")

# data = load_customer_queries()
# if role == "Admin" and data is not None and not data.empty:
#     st.header("📧 Email Automation")
#     email_options = st.radio("Select Email Mode:", ("📂 Manual Review", "⚡ Automatic Send"))
#     if email_options == "📂 Manual Review":
#         for index, row in data.iterrows():
#             email = row.get('Customer Email', '')
#             query = row.get('Query', '')
#             if email and query:
#                 ai_response = generate_response(query, product_data)
#                 st.subheader(f"📩 Email to: {email}")
#                 st.text_area("✉️ Generated Response", ai_response, height=100, key=f"email_{index}")
#                 if st.button(f"📤 Send Email to {email}", key=f"send_{index}"):
#                     send_email(email, "Smartphone Support Response", ai_response)
#                     st.success(f"✅ Email sent to {email}")
#     elif email_options == "⚡ Automatic Send":
#         if st.button("🚀 Send All Emails Automatically"):
#             for index, row in data.iterrows():
#                 email = row.get('Customer Email', '')
#                 query = row.get('Query', '')
#                 if email and query:
#                     ai_response = generate_response(query, product_data)
#                     send_email(email, "Smartphone Support Response", ai_response)
#             st.success("✅ All emails sent successfully!")


# 3rd
# import streamlit as st
# import pandas as pd
# import smtplib
# import os
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Load environment variables
# load_dotenv()
# SENDER_EMAIL = os.getenv("EMAIL_USER")
# SENDER_PASSWORD = os.getenv("EMAIL_PASS")

# # Load or create product dataset
# PRODUCT_DATA_FILE = "product_data.csv"
# if os.path.exists(PRODUCT_DATA_FILE):
#     product_data = pd.read_csv(PRODUCT_DATA_FILE)
# else:
#     product_data = pd.DataFrame(columns=["model", "price", "stock", "condition"])
#     product_data.to_csv(PRODUCT_DATA_FILE, index=False)

# st.set_page_config(page_title="AI Customer Support", page_icon="🤖", layout="wide")
# st.title("🤖 AI-Powered Smartphone Customer Support")
# st.markdown("Enhance customer experience with AI-driven responses! 🚀")
# role = st.sidebar.selectbox("Select Role:", ["User", "Admin"], help="Admin can upload data, User can only ask questions.")

# def upload_product_data():
#     uploaded_file = st.file_uploader("📂 Upload smartphone data CSV (Admin only)", type=["csv"])
#     if uploaded_file is not None:
#         global product_data
#         product_data = pd.read_csv(uploaded_file)
#         product_data.to_csv(PRODUCT_DATA_FILE, index=False)
#         st.success("✅ Product data uploaded and saved!")

# def generate_response(query):
#     refund_keywords = ["refund", "return", "damaged", "broken"]
#     if any(word in query.lower() for word in refund_keywords):
#         return "Your order is eligible for a return. Please contact support."
    
#     relevant_products = product_data[product_data['model'].str.contains(query, case=False, na=False)]
#     if not relevant_products.empty:
#         row = relevant_products.iloc[0]
#         return f"{row['model']}: ₹{row['price']}. Stock: {row.get('stock', 'N/A')}. Condition: {row.get('condition', 'N/A')}."
    
#     return "Product details not available. Please check with the store."

# def send_email(to_email, subject, body):
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = to_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

# if role == "Admin":
#     st.sidebar.subheader("📂 Admin Panel")
#     upload_product_data()

# st.header("💬 Chatbot Q&A")
# user_query = st.text_input("🔍 Ask a question about smartphones:")
# if user_query:
#     chatbot_response = generate_response(user_query)
#     st.success(f"**AI Response:** {chatbot_response}")

# st.header("📧 Email Automation")
# email_data_file = st.file_uploader("📂 Upload customer queries (CSV)", type=["csv"])
# if email_data_file is not None:
#     email_data = pd.read_csv(email_data_file)
#     if st.button("🚀 Send All Emails Automatically"):
#         for _, row in email_data.iterrows():
#             email = row.get('Customer Email', '')
#             query = row.get('Query', '')
#             if email and query:
#                 ai_response = generate_response(query)
#                 send_email(email, "Smartphone Support Response", ai_response)
#         st.success("✅ All emails sent successfully!")

# 4th
# import os
# import streamlit as st
# import pandas as pd
# import chromadb
# import fitz  # PyMuPDF for PDF processing
# from openai import OpenAI
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Load environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = "gemma2-9b-it"
# SENDER_EMAIL = os.getenv("EMAIL_USER")
# SENDER_PASSWORD = os.getenv("EMAIL_PASS")
# ADMIN_PASSWORD = "admin123"  # Change this to a secure password

# # Initialize ChromaDB client
# chroma_client = chromadb.PersistentClient(path="./chroma_db")
# customer_collection = chroma_client.get_or_create_collection(name="customer_queries")
# product_collection = chroma_client.get_or_create_collection(name="product_data")

# # Function to send email
# # Function to send email
# def send_email(to_email, subject, message):
#     try:
#         if isinstance(message, list):
#             message = "\n".join(message)  # Convert list to string
        
#         msg = MIMEMultipart()
#         msg["From"] = SENDER_EMAIL
#         msg["To"] = to_email
#         msg["Subject"] = subject
#         msg.attach(MIMEText(message, "plain"))
        
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
#         server.quit()
#     except Exception as e:
#         st.error(f"Failed to send email: {str(e)}")


# # Function to handle AI-generated responses
# def get_response(query, collection):
#     results = collection.query(query_texts=[query], n_results=1)
#     if results and results["documents"]:
#         return results["documents"][0] if isinstance(results["documents"][0], str) else str(results["documents"][0])
#     else:
#         return "No relevant information found. Please refine your query."


# # Function to process uploaded files
# def process_uploaded_file(uploaded_file):
#     if uploaded_file.name.endswith(".csv"):
#         return pd.read_csv(uploaded_file)
#     elif uploaded_file.name.endswith(".xlsx"):
#         return pd.read_excel(uploaded_file)
#     elif uploaded_file.name.endswith(".pdf"):
#         doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#         text = "\n".join([page.get_text("text") for page in doc])
#         return pd.DataFrame({"product_info": [text], "product_id": ["pdf_upload"]})
#     else:
#         st.error("Unsupported file format. Please upload CSV, XLSX, or PDF.")
#         return None

# # Function to send automatic responses from uploaded customer queries
# def process_customer_queries(df):
#     if "Customer Email" in df.columns and "Query" in df.columns:
#         for _, row in df.iterrows():
#             response = get_response(row["Query"], product_collection)
#             send_email(row["Customer Email"], "Query Response", response)
#     else:
#         st.error("Dataset missing required columns: 'Customer Email' and 'Query'")

# # Streamlit UI
# st.set_page_config(page_title="AI Query System", layout="wide")
# st.title("📩 AI-Powered Customer Support")

# # Sidebar navigation
# section = st.sidebar.radio("Select Section", ["User", "Admin"])

# if section == "User":
#     st.sidebar.subheader("User Menu")
#     menu = st.sidebar.radio("Navigation", ["FAQs & Products", "Ask Q&A", "Submit Query"])
    
#     if menu == "FAQs & Products":
#         st.subheader("Frequently Asked Questions")
#         st.write("1. How to request a refund?\nRefunds are processed within 5-7 business days after approval.")
#         st.write("2. How to return a product?\nReturns are accepted within 14 days of delivery.")
        
#         st.subheader("Available Products")
#         products = product_collection.get()

#         if products and "documents" in products and products["documents"]:
#             for idx, product in enumerate(products["documents"]):
#                 product_details = product.split(" - ₹")  # Extract name and price
#                 product_name = product_details[0]
#                 product_price = f"₹{product_details[1].split(',')[0]}" if len(product_details) > 1 else "Price Not Available"
                
#                 with st.container():
#                     st.write(f"### 🛒 Product: {product_name}")
#                     st.write(f"📌 Price: {product_price}")
#                     st.button("View Details", key=f"view_details_{idx}")  # Unique key added
#         else:
#             st.warning("No products available!")

#     elif menu == "Ask Q&A":
#         st.subheader("Ask a Question")
#         user_query = st.text_input("Enter your query")
        
#         if st.button("Get Answer"):
#             product_response = get_response(user_query, product_collection)
#             st.write("### AI Response: ", product_response)

    
#     elif menu == "Submit Query":
#         st.subheader("Submit Your Query")
#         user_email = st.text_input("Enter your email")
#         user_message = st.text_area("Enter your query message")
#         if st.button("Submit"):
#             send_email(SENDER_EMAIL, "User Query", f"From: {user_email}\nMessage: {user_message}")
#             st.success("Your query has been submitted successfully!")

# elif section == "Admin":
#     st.sidebar.subheader("Admin Login")
#     admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
#     if admin_password == ADMIN_PASSWORD:
#         menu = st.sidebar.radio("Admin Menu", ["Upload Dataset", "Upload Product Data", "Query Logs"])
        
#         if menu == "Upload Dataset":
#             st.subheader("Upload Customer Query Dataset")
#             uploaded_file = st.file_uploader("Upload customer query dataset (CSV/XLSX)", type=["csv", "xlsx"])
#             if uploaded_file:
#                 df = process_uploaded_file(uploaded_file)
#                 if df is not None:
#                     process_customer_queries(df)
#                     st.success("Customer queries processed and emails sent successfully!")
        
#         elif menu == "Upload Product Data":
#             st.subheader("Upload Product Dataset")
#             uploaded_product_file = st.file_uploader("Upload product dataset (CSV/XLSX/PDF)", type=["csv", "xlsx", "pdf"])
#             if uploaded_product_file:
#                 product_df = process_uploaded_file(uploaded_product_file)
#                 if product_df is not None:
#                     for _, row in product_df.iterrows():
#                         product_collection.add(documents=[row["model"] + " - ₹" + str(row["price"]) + ", " + row["processor_brand"] + " " + str(row["num_cores"]) + " cores, " + str(row["ram_capacity"]) + "GB RAM, " + str(row["internal_memory"]) + "GB Storage"], ids=[str(row["brand_name"])] if "model" in product_df.columns and "price" in product_df.columns else [])
#                     st.success("Product dataset uploaded successfully!")
        
#         elif menu == "Query Logs":
#             st.subheader("Query History")
#             st.write("(Coming soon!)")
#     else:
#         st.warning("Incorrect password! Access denied.")

import os
import streamlit as st
import pandas as pd
import chromadb
import fitz  # PyMuPDF for PDF processing
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "gemma2-9b-it"
# SENDER_EMAIL = os.getenv("EMAIL_USER")
# SENDER_PASSWORD = os.getenv("EMAIL_PASS")
ADMIN_PASSWORD = "admin123"  # Change this to a secure password

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
EMAIL_USER = st.secrets["EMAIL_USER"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
customer_collection = chroma_client.get_or_create_collection(name="customer_queries")
product_collection = chroma_client.get_or_create_collection(name="product_data")

# Function to send email
def send_email(to_email, subject, message):
    """
    Sends an email to the given recipient with the subject and message.
    """
    try:
        if isinstance(message, list):
            message = "\n".join(message)  # Convert list to string
        
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")


# Function to handle AI-generated responses
def get_response(query, collection):
    """
    Fetches a relevant response based on the customer query from the product collection.
    """
    results = collection.query(query_texts=[query], n_results=1)
    if results and results["documents"]:
        return results["documents"][0] if isinstance(results["documents"][0], str) else str(results["documents"][0])
    else:
        return "No relevant information found. Please refine your query."


# Function to process uploaded files
def process_uploaded_file(uploaded_file):
    """
    Processes the uploaded file based on its type (CSV, XLSX, PDF).
    """
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text("text") for page in doc])
        return pd.DataFrame({"product_info": [text], "product_id": ["pdf_upload"]})
    else:
        st.error("Unsupported file format. Please upload CSV, XLSX, or PDF.")
        return None

# Function to send automatic responses from uploaded customer queries
def process_customer_queries(df):
    """
    Processes the customer queries and sends the relevant email responses based on the content of each query.
    """
    if "Customer Email" in df.columns and "Query" in df.columns:
        for _, row in df.iterrows():
            response = get_response(row["Query"], product_collection)

            # Improved response handling based on specific customer queries (refund, quotation, etc.)
            if "damaged" in row["Query"].lower() or "refund" in row["Query"].lower():
                response = f"""
                Subject: Query Response - product Refund Request

                Dear Customer,

                Thank you for reaching out to us regarding your recent order.

                We sincerely apologize for the inconvenience caused by receiving a damaged product. We understand your concern and would like to assist you with the refund process.

                To initiate the refund, please contact our customer support team at [support@yourcompany.com] or call us at [1-800-123-4567], and we will provide further instructions on how to return the item and process your refund.

                If you have any further questions or require assistance, please don’t hesitate to reach out. We are here to help!

                Thank you for your understanding, and we look forward to resolving this matter for you.

                Best regards,
                Customer Support Team
                """
            elif "quotation" in row["Query"].lower() or "price" in row["Query"].lower():
                response = f"""
                Subject: Product Quotation

                Dear Customer,

                Thank you for reaching out to us. Below is the quotation for the product you requested:
            

                We are also offering a **10% discount** on your next purchase. Simply use the code **DISCOUNT10** at checkout.

                Additionally, we have a wide variety of products in our catalog:

                - **Apple iPhone 12** - ₹59,999
                - **Samsung Galaxy S21** - ₹49,999
                - **OnePlus 9 Pro** - ₹64,999

                You can view all our latest products [here](https://www.yourcompany.com/products).

                If you have any more questions or need further details, feel free to ask!

                Best regards,
                Customer Support Team
                """
            elif "latest" in row["Query"].lower():
                response = f"""
                Subject: Latest Product Information

                Dear Customer,

                Thank you for your interest in our latest products. Here are some of our newest arrivals:

                - **Apple iPhone 13 Pro** - ₹1,19,999
                - **Samsung Galaxy Z Fold 3** - ₹1,49,999
                - **OnePlus 10 Pro** - ₹74,999

                You can explore more about these products [here](https://www.yourcompany.com/new-arrivals).

                If you would like more details or have any other questions, please feel free to contact us.

                Best regards,
                Customer Support Team
                """
            elif "live agent" in row["Query"].lower() or "talk to someone" in row["Query"].lower():
                response = f"""
                Subject: Contacting a Live Agent

                Dear Customer,

                Thank you for reaching out to us. We understand that you may have specific questions or need assistance. You can easily get in touch with our live agent for immediate help.

                Please reach us via the following channels:
                - **Live Chat**: Visit our [website](https://www.yourcompany.com/chat) and click on the live chat option.
                - **Phone Support**: Call us at **1-800-123-4567** for real-time assistance.

                We are here to help you with all your inquiries.

                Best regards,
                Customer Support Team
                """
            else:
                # Default response for product-related queries
                response = f"""
                Subject: Query Response

                Dear Customer,

                Thank you for contacting us regarding your query.

                We found the following product information based on your query:

                **Product: Apple iPhone 11**  
                - Bionic 6.0 cores, 4GB RAM, 64GB Storage

                If you have any more questions or need additional information, feel free to ask.

                Thank you for reaching out to us. If you need further assistance, please let us know.

                Best regards,
                Customer Support Team
                """
            
            send_email(row["Customer Email"], "Query Response", response)
    else:
        st.error("Dataset missing required columns: 'Customer Email' and 'Query'")

# Streamlit UI
st.set_page_config(page_title="AI Query System", layout="wide")
st.title("📩 AI-Powered Customer Support")

# Sidebar navigation
section = st.sidebar.radio("Select Section", ["User", "Admin"])

if section == "User":
    st.sidebar.subheader("User Menu")
    menu = st.sidebar.radio("Navigation", ["FAQs & Products", "Ask Q&A", "Submit Query"])
    
    if menu == "FAQs & Products":
        st.subheader("Frequently Asked Questions")
        st.write("1. How to request a refund?\nRefunds are processed within 5-7 business days after approval.")
        st.write("2. How to return a product?\nReturns are accepted within 14 days of delivery.")
        
        st.subheader("Available Products")
        products = product_collection.get()

        if products and "documents" in products and products["documents"]:
            for idx, product in enumerate(products["documents"]):
                product_details = product.split(" - ₹")  # Extract name and price
                product_name = product_details[0]
                product_price = f"₹{product_details[1].split(',')[0]}" if len(product_details) > 1 else "Price Not Available"
                
                with st.container():
                    st.write(f"### 🛒 Product: {product_name}")
                    st.write(f"📌 Price: {product_price}")
                    st.button("View Details", key=f"view_details_{idx}")  # Unique key added
        else:
            st.warning("No products available!")

    elif menu == "Ask Q&A":
        st.subheader("Ask a Question")
        user_query = st.text_input("Enter your query")
        
        if st.button("Get Answer"):
            product_response = get_response(user_query, product_collection)
            st.write("### AI Response: ", product_response)

    
    elif menu == "Submit Query":
        st.subheader("Submit Your Query")
        user_email = st.text_input("Enter your email")
        user_message = st.text_area("Enter your query message")
        if st.button("Submit"):
            send_email(SENDER_EMAIL, "User Query", f"From: {user_email}\nMessage: {user_message}")
            st.success("Your query has been submitted successfully!")

elif section == "Admin":
    st.sidebar.subheader("Admin Login")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    if admin_password == ADMIN_PASSWORD:
        menu = st.sidebar.radio("Admin Menu", ["Upload Dataset", "Upload Product Data", "Query Logs"])
        
        if menu == "Upload Dataset":
            st.subheader("Upload Customer Query Dataset")
            uploaded_file = st.file_uploader("Upload customer query dataset (CSV/XLSX)", type=["csv", "xlsx"])
            if uploaded_file:
                df = process_uploaded_file(uploaded_file)
                if df is not None:
                    process_customer_queries(df)
                    st.success("Customer queries processed and emails sent successfully!")
        
        elif menu == "Upload Product Data":
            st.subheader("Upload Product Dataset")
            uploaded_product_file = st.file_uploader("Upload product dataset (CSV/XLSX/PDF)", type=["csv", "xlsx", "pdf"])
            if uploaded_product_file:
                product_df = process_uploaded_file(uploaded_product_file)
                if product_df is not None:
                    for _, row in product_df.iterrows():
                        product_collection.add(documents=[row["model"] + " - ₹" + str(row["price"]) + ", " + row["processor_brand"] + " " + str(row["num_cores"]) + " cores, " + str(row["ram_capacity"]) + "GB RAM, " + str(row["internal_memory"]) + "GB Storage"], ids=[str(row["brand_name"])] if "model" in product_df.columns and "price" in product_df.columns else [])
                    st.success("Product dataset uploaded successfully!")
        
        elif menu == "Query Logs":
            st.subheader("Query History")
            st.write("(Coming soon!)")
    else:
        st.warning("Incorrect password! Access denied.")
