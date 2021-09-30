import streamlit as st
import icd10
import sklearn
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta, date
import datetime as dt
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import LabelEncoder
  
st.set_page_config(page_title="NZ Hospital Demand Forecast APP",layout="centered",initial_sidebar_state="expanded")

st.sidebar.header('User Input Parameters')
   
    # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:light green;padding:13px"> 
    <h1 style ="color:orange;text-align:center;">NZ Hospital Demand Forecast APP</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.subheader('by Falalu Sani Barde, Manusree Banerjee, Sarah El Shatby, Toyin Ogunlade ')
      
# following lines create boxes in which user can enter data required to make prediction
page=st.sidebar.slider("Age",1,100)
psex = st.sidebar.radio("Select Gender: ", ('Male', 'Female'))
alpha_index = st.sidebar.selectbox('ICD Alphabetical Index', ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'))
code_num = st.sidebar.slider('ICD Numerical Index',0,99)
dhb = st.sidebar.selectbox("Select District: ", ('Auckland', 'Bay of Plenty', 'Canterbury', 'Capital and Coast', 'Counties Manukau', "Hawke's Bay", 'Hutt Valley', 'Lakes', 'Midcentral', 'Nelson Marlborough', 'Northland', 'South 3', 'South Canterbury', 'Southern', 'Tairawhiti', 'Taranaki', 'Waikato', 'Wairarapa', 'Waitemata', 'West Coast', 'Whanganui', 'Unknown'))
cols1,_ = st.columns((1,4)) # To make it narrower
format = 'MMM DD, YYYY'  # format output
start_date = dt.date(year=2021,month=1,day=1)  #  I need some range in the past
end_date = dt.date(year=2022,month=12,day=31)
max_days = end_date-start_date
date = st.sidebar.slider('Select admission date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
## Sanity check
st.sidebar.table(pd.DataFrame([[start_date, date, end_date]],columns=['start','selected','end'],index=['date']))

if psex=='Female':
  sex=1
else:
  sex=0
if code_num<10:
  icdcode=alpha_index+'0'+str(code_num)
else:
  icdcode=alpha_index+str(code_num)
 
dist_dict = {'Auckland':1, 'Bay of Plenty':2, 'Canterbury':3, 'Capital and Coast':4, 'Counties Manukau':5, "Hawke's Bay":6, 'Hutt Valley':7, 'Lakes':8, 'Midcentral':9, 'Nelson Marlborough':10, 'Northland':11, 'South Canterbury':12, 'Southern':13, 'Tairawhiti':14, 'Taranaki':15, 'Unkown':16, 'Waikato':17, 'Wairarapa':18, 'Waitemata':19, 'West Coast':20, 'Whanganui':21}
# Accessing integer using roman key
district = dist_dict[dhb]

if st.button("PREDICT"):
  if icd10.exists(icdcode):
    st.write("ICD code is", icdcode)
    code = icd10.find(icdcode)
    if icdcode=='A00' or icdcode=='B00':
      chap=1
    elif icdcode=='C00' or icdcode=='D00':
      chap=2
    elif icdcode=='E00':
      chap=4
    elif icdcode=='F00':
      chap=5
    elif icdcode=='G00':
      chap=6
    elif icdcode=='H00':
      chap=7
    elif icdcode=='I00':
      chap=9
    elif icdcode=='J00':
      chap=10
    elif icdcode=='K00':
      chap=11
    elif icdcode=='L00':
      chap=12
    elif icdcode=='M00':
      chap=13
    elif icdcode=='N00':
      chap=14
    elif icdcode=='O00':
      chap=15
    elif icdcode=='P00':
      chap=16
    elif icdcode=='Q00':
      chap=17
    elif icdcode=='R00':
      chap=18
    elif icdcode=='S00' or icdcode=='T00':
      chap=19
    elif icdcode=='U00':
      chap=22
    elif icdcode=='V00' or icdcode=='W00' or icdcode=='X00' or icdcode=='Y00':
      chap=20
    elif icdcode=='Z00':
      chap=21
    else:
      # Creating a Roman to Int Dictionary
      romtoint = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12,'XIII':13,'XIV':14,'XV':15,'XVI':16,'XVII':17,'XVIII':18,'XIX':19,'XX':20,'XXI':21,'XXII':22}
      # Accessing integer using roman key
      icd_chap=code.chapter
      chap=romtoint[icd_chap] 
      st.write("ICD chapter is", chap)
    year=2021
    user_input=[[year,district,sex,page,chap]]
    #load the model from disk
    loaded_model = pickle.load(open('randforestreg.pkl', 'rb'))
    mlos = loaded_model.predict(user_input) 
    st.write("Mean Length of Stay is ",np.round(mlos[0],0))
    dis_date=date+ timedelta(days=mlos[0])
    fdis_date = dis_date.strftime("%b %d, %Y")
    st.write("Predicted Discharge date is ",fdis_date)
  else:
    st.write("Entered ICD Code doesn't exist!!!")
  st.info("Don't forget to rate this app")
  
feedback = st.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)
  
if feedback:
    st.header("Thank you for rating the app!")


st.subheader("About App")

st.info("This web app helps you to find approximate discharge date of a patient.")
st.info("Enter the required fields and click on the 'PREDICT' button to check your probable discharge date.")


st.caption("Caution: This is just a prediction and may not be exact.") 