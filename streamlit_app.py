import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection("snowflake")   # requires [connections.snowflake] in secrets
session = cnx.session()

# Load options
rows = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"))
           .collect()
)
fruit_options = [r["FRUIT_NAME"] for r in rows]

name_on_order = st.text_input("Name on Smoothie:")
ingredients_list = st.multiselect(
    "Select your favorite fruits (up to 5):",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredient_list = " ".join(ingredients_list)
    st.write(f"Fruit list is {ingredient_list}")

    if st.button("Place Order"):
        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER) "
            f"VALUES ('{ingredient_list}', '{name_on_order}')"
        ).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True )
