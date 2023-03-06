# Importing required Libraries
import streamlit as st
import pandas as pd
import numpy as np
import os, pickle

# Setting up page configuration and directory path
st.set_page_config(page_title= "Customer Churn Prediction", page_icon="🛳️", layout="centered")
DIRPATH = os.path.dirname(os.path.realpath(__file__))

# Setting background image
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('images/background.jpg')

# Setting up logo
left, mid, mid1, right = st.columns(4)
with mid:
    st.image("images/logo.jpeg", use_column_width=True)

# Setting up Sidebar
social_acc = ['Data Field Description', 'EDA', 'About App']
social_acc_nav = st.sidebar.radio('**INFORMATION SECTION**', social_acc)

if social_acc_nav == 'Data Field Description':
    st.sidebar.markdown("<h2 style=[],'text-align: center;'> Data Field Description </h2> ", unsafe_allow_html=True)
    st.sidebar.markdown("""
    The table below gives a description on the variables required to make predictions.
    | Variable      | Definition:       |
    | :------------ |:--------------- |
    | FREQUENCE     | number of times the client has made an income |
    | TENURE        | duration in the network |
    | FREQUENCE_RECH| number of times the customer refilled |
    | MONTANT       | top-up amount   |
    | DATA_VOLUME   | number of connections|
    | ORANGE        | call to orange |
    | ARPU_SEGMENT  | income over 90 days / 3 |
    | ON_NET        | inter expresso call |
    | REGULARITY    | number of times the client is active for 90 days   |
    | FREQ_TOP_PACK | number of times client has activated the top pack packages|
    | REVENUE       | monthly income of each client   |
    """)
  
elif social_acc_nav == 'EDA':
    st.sidebar.markdown("<h2 style=[],'text-align: center;'> Exploratory Data Analysis </h2> ", unsafe_allow_html=True)
    st.sidebar.markdown('''---''')
    st.sidebar.markdown("""
                        | About EDA|
                        | :------------ |
                        The exploratory data analysis of this project can be find in a Jupyter notebook from the link below""" )
    st.sidebar.markdown("[Open Notebook](https://github.com/Kyei-frank/Titanic-Project---Machine-Learning-from-Disaster/blob/main/workflow.ipynb)")

elif social_acc_nav == 'About App':
    st.sidebar.markdown("<h2 style=[],'text-align: center;'> Titanic Survival Prediction App </h2> ", unsafe_allow_html=True)
    st.sidebar.markdown('''---''')
    st.sidebar.markdown("""
                        | Brief Introduction|
                        | :------------ |
                        This projet is based on a Zindi challenge for an African telecommunications company (Expresso)
                        that provides customers with airtime and mobile data bundles. The objective of this challenge
                        is to develop a machine learning model to predict the likelihood of each customer “churning,”
                        i.e. becoming inactive and not making any transactions for 90 days. This solution will help
                        this telecom company to better serve their customers by understanding which customers are at risk of leaving""")
    st.sidebar.markdown("")
    st.sidebar.markdown("[ Visit Github Repository for more information](https://github.com/Kyei-frank/Titanic-Project---Machine-Learning-from-Disaster)")

# Loading Machine Learning Objects
@st.cache_data
def load_saved_objects(file_path = 'ML_items'):
    # Function to load saved objects
    with open('ML_items', 'rb') as file:
        loaded_object = pickle.load(file)
        
    return loaded_object

# Instantiating ML_items
Loaded_object = load_saved_objects(file_path = 'ML_items')
pipeline_of_my_app = Loaded_object["pipeline"]


# Setting up variables for input data
@st.cache_data
def setup(tmp_df_file):
    "Setup the required elements like files, models, global variables, etc"
    pd.DataFrame(
        dict(
            FREQUENCE= [],
            TENURE= [],
            FREQUENCE_RECH= [],
            MONTANT= [],
            DATA_VOLUME= [],
            ORANGE= [], 
            ARPU_SEGMENT= [],
            ON_NET= [],
            REGULARITY= [],
            FREQ_TOP_PACK= [],
            REVENUE= [],
        )
    ).to_csv(tmp_df_file, index=False)

# Setting up a file to save our input data
tmp_df_file = os.path.join(DIRPATH, "tmp", "data.csv")
setup(tmp_df_file)

# setting Title for forms
st.markdown("<h2 style=[],'text-align: right;'>....... Customer Churn Prediction ...... </h2> ", unsafe_allow_html=True)
st.markdown("<h6 style=[],'text-align: center;'> Fill in the details below and click on SUBMIT button to make a prediction for a Client. </h6> ", unsafe_allow_html=True)

# Creating columns for input data(forms)
left_col, middle_col, right_col = st.columns(3)

# Developing forms to collect input data
with st.form(key="information", clear_on_submit=True):
    
    # Setting up input data for 1st column
    left_col.markdown(":blue[**CALLS & ACTIVITY DETAILS**]")
    ORANGE = left_col.number_input("Insert Number of calls to ORANGE")
    ON_NET = left_col.number_input("Insert Number of inter expresso calls")
    DATA_VOLUME = left_col.number_input("Insert Number of connections")
    REGULARITY = left_col.number_input("Insert number of times the client is active for 90 days")
    FREQ_TOP_PACK = left_col.number_input("Insert number of times client has activated the top pack packages")
    
    # Setting up input data for 2nd column
    middle_col.markdown(":blue[**TOP-UP & INCOME DETAILS**]")
    MONTANT = middle_col.number_input("Insert top-up amount")
    FREQUENCE_RECH = middle_col.number_input("Insert Number of times the customer refilled")
    REVENUE = middle_col.number_input("Insert monthly income of client")
    ARPU_SEGMENT = middle_col.number_input("Insert income over 90 days / 3")
    FREQUENCE = middle_col.number_input("Insert number of times client has made an income")
    
    # Setting up input data for 2nd column
    right_col.markdown(":blue[**TENURE DETAILS**]")
    TENURE = right_col.radio("What is Client's duration in the network?", ('D 3-6 month',
                            'E 6-9 month', 'F 9-12 month', 'G 12-15 month', 'H 15-18 month',
                            'I 18-21 month', 'J 21-24 month', 'K > 24 month',))
    
    submitted = st.form_submit_button(label="Submit")
    
# Setting up background operations after submitting forms
if submitted:
    # Saving input data as csv after submission
    pd.read_csv(tmp_df_file).append(
        dict(
            FREQUENCE= FREQUENCE,
            TENURE= TENURE,
            FREQUENCE_RECH= FREQUENCE_RECH,
            MONTANT= MONTANT,
            DATA_VOLUME= DATA_VOLUME,
            ORANGE= ORANGE, 
            ARPU_SEGMENT= ARPU_SEGMENT,
            ON_NET= ON_NET,
            REGULARITY= REGULARITY,
            FREQ_TOP_PACK= FREQ_TOP_PACK,
            REVENUE= REVENUE,
            ),
            ignore_index=True,
    ).to_csv(tmp_df_file, index=False)
    st.balloons()

    # Converting input data to a dataframe for prediction
    df = pd.read_csv(tmp_df_file)
    df= df.copy()
    
    # Making Predictions
    # Passing data to pipeline to make prediction
    pred_output = pipeline_of_my_app.predict(df)
    prob_output = np.max(pipeline_of_my_app.predict_proba(df))
    
    # Interpleting prediction output for display
    X= pred_output[-1]
    if X == 1:
        explanation = 'Client will CHURN'
    else: 
        explanation = 'Client will NOT CHURN'
    output = explanation
    
    # Displaying prediction results
    st.markdown('''---''')
    st.markdown("<h4 style=[],'text-align: center;'> Prediction Results </h4> ", unsafe_allow_html=True)
    st.success(f"Prediction:  {output}")
    st.success(f"Confidence Probability:  {prob_output}")
    st.markdown('''---''')    

    # Making expander to view all records
    expander = st.expander("See all records")
    with expander:
        df = pd.read_csv(tmp_df_file)
        df['Survival']= pred_output
        st.dataframe(df)

    
    