import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Create Snowflake connection and get Snowpark session
cnx = st.connection("snowflake")        # requires secrets.toml (see below)
session = cnx.session()                 # <-- get a Snowpark Session
# If you only need SQL and not Snowpark, you could also use: cnx.query("SELECT ...")

# Pull fruit options and turn into a simple Python list
fruit_rows = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"))
           .collect()
)
fruit_options = [row["FRUIT_NAME"] for row in fruit_rows]

name_on_order = st.text_input("Name on Smoothie:")
ingredients_list = st.multiselect(
    "Select your favorite fruits (up to 5):",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredient_list = " ".join(ingredients_list)
    st.write(f"Fruit list is {ingredient_list}")

    # Parameterized SQL is safer, but keeping it simple:
    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
        VALUES (%s, %s)
    """
    time_to_place_order = st.button("Place Order")
    if time_to_place_order:
        # Use Snowpark to run the insert
        session.sql(
            f"INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER) "
            f"VALUES ('{ingredient_list}', '{name_on_order}')"
        ).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
