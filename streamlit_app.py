import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection("snowflake")   # requires [connections.snowflake] in secrets
session = cnx.session()

# Load options
snow_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)

pd_df = snow_df.to_pandas()
fruit_options = [r["FRUIT_NAME"] for r in snow_df]

name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect(
    "Select your favorite fruits (up to 5):",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredient_string = ' '
    
    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True )
        
    st.write(f"Fruit list is {ingredient_string}")

    if st.button("Place Order"):
        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER) "
            f"VALUES ('{ingredient_list}', '{name_on_order}')"
        ).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
