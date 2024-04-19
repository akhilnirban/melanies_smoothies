import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# st.title('My Parents New Healthy Diner')

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("""Choose the fruit you want in your smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be: ', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options")
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_dy=my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
    ingredients_string=''
    for fruit in ingredients_list:
        ingredients_string+= fruit + ' '
        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""
    # st.write(my_insert_stmt)
    # st.stop()
    
    # st.write(my_insert_stmt)
    if ingredients_string:

        time_to_insert= st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")


