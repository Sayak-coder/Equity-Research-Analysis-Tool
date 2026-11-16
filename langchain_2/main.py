import streamlit as st 
import langchain_helper 

st.title("Know Your President")
st.write("This will help you to know about your president and his or her age")

country_name = st.text_input("Enter your country name: ").strip()

if country_name:
    response = langchain_helper.get_president_info(country_name)
    st.header(response["president_name"])
    st.write(response["age"])