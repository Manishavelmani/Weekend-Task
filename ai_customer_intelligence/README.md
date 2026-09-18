# AI Customer Intelligence Platform

## Project Overview

The **AI Customer Intelligence Platform** is an end-to-end customer analytics and AI application.

The project combines:

- Data Analysis
- SQL Analytics
- Machine Learning
- ANN
- SHAP Explainability
- NLP
- Text Embeddings
- FAISS Semantic Search
- Knowledge Base
- RAG
- Local LLM
- AI Customer Assistant
- Flask Web Application

The main purpose of this project is to analyze customer behavior, predict customer churn, explain predictions, search customer-support information, and provide AI-based customer assistance.

---

## Dataset

### Customer Churn Dataset

**Dataset:** IBM Telco Customer Churn Dataset

- Customers: 7,043
- Columns: 21
- Target: `Churn`

The dataset contains information about:

- Customer demographics
- Tenure
- Contract
- Internet service
- Payment method
- Monthly charges
- Total charges
- Customer services
- Churn status

### Customer Support Ticket Dataset

**Dataset:** Customer Support Ticket Dataset

- Tickets: 8,469
- Columns: 17

The dataset contains:

- Ticket subject
- Ticket description
- Ticket type
- Ticket status
- Ticket priority
- Customer information
- Resolution information

This dataset is used for NLP, embeddings, semantic search, and RAG.

---

## Project Workflow

```text
Data Understanding
        ↓
EDA
        ↓
SQL Analysis
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Machine Learning
        ↓
Model Improvement
        ↓
ANN
        ↓
SHAP
        ↓
NLP
        ↓
Text Embeddings
        ↓
FAISS
        ↓
Knowledge Base
        ↓
RAG
        ↓
Local LLM
        ↓
AI Customer Assistant
        ↓
Flask Application
Project Structure
ai_customer_intelligence/
│
├── Datasets/
├── models/
├── notebooks/
├── static/
├── templates/
│
├── app.py
├── assistant_agent.py
├── requirements.txt
├── Pipfile
├── Pipfile.lock
├── README.md
└── AI Customer Intelligence Platform.docx
Main Components
1. Data Analysis

Performed exploratory data analysis to understand:

Customer distribution
Churn distribution
Missing values
Data types
Customer behavior
Service usage
Contract patterns
2. SQL Analysis

SQLite was used for customer analytics such as:

Total customers
Churned customers
Churn rate
Average charges
Contract-based analysis
Payment method analysis
3. Machine Learning

Multiple models were trained for churn prediction:

Logistic Regression
Decision Tree
Random Forest
Gradient Boosting
XGBoost
KNN
4. ANN

A neural network was developed using TensorFlow for customer churn prediction.

5. SHAP

SHAP is used to explain customer churn predictions and identify important features affecting each prediction.

6. NLP

Customer support tickets were processed using:

Text cleaning
Tokenization
Stopword removal
TF-IDF
N-gram analysis
7. Text Embeddings

Sentence Transformers were used to convert customer-support text into numerical vectors.

Model used:

all-MiniLM-L6-v2
8. FAISS

FAISS is used for semantic similarity search over customer-support ticket embeddings.

9. Knowledge Base

A customer-support knowledge base was created containing information about:

FAQs
Billing
Cancellation
Contracts
Services
Support procedures
Business rules
10. RAG

RAG retrieves relevant information from the knowledge base and provides it as context to the local LLM.

11. Local LLM

A lightweight local LLM is used to generate natural-language responses without depending on paid cloud APIs.

12. AI Customer Assistant

The AI assistant combines:

Customer Profile
      +
Churn Prediction
      +
SHAP Explanation
      +
Knowledge Base Search
      +
RAG
      +
Local LLM
13. Flask Application

The complete system is integrated into a Flask web application.

Main pages include:

Home
Dashboard
Customer
Prediction
Explanation
AI Assistant
Technologies Used
Data Analysis
Python
Pandas
NumPy
Matplotlib
Seaborn
Machine Learning
Scikit-learn
XGBoost
Joblib
Explainable AI
SHAP
Deep Learning
TensorFlow
NLP
NLTK
TF-IDF
Embeddings
Sentence Transformers
Vector Search
FAISS
Local LLM
llama.cpp
llama-cpp-python
GGUF
Web Application
Flask
HTML
CSS
Bootstrap
Database
SQLite
Installation

Clone the repository:

git clone <repository-url>
cd Weekend-Task

Create the environment:

pipenv install

Activate the environment:

pipenv shell

Install required packages:

pip install -r requirements.txt
Run the Application

Run the Flask application:

python app.py

Then open the local Flask URL in your browser.

Key Features
Customer churn prediction
Customer risk analysis
SHAP-based prediction explanation
Customer-support text analysis
Semantic search
Knowledge-base search
RAG-based responses
Local LLM integration
AI customer assistant
Flask web interface
CPU-friendly architecture
Future Improvements
Improve churn prediction
Improve NLP classification
Improve RAG retrieval
Add conversation memory
Add more knowledge-base documents
Improve UI
Add batch customer analysis
Add model monitoring
Deploy the application
Conclusion

The AI Customer Intelligence Platform combines data analytics, machine learning, explainable AI, NLP, semantic search, RAG, and local LLM technologies into one application.

The project demonstrates an end-to-end approach for building a practical customer intelligence and AI assistant platform using Python and Flask.