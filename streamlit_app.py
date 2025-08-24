import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection("snowflake")   # needs [connections.snowflake] in secrets
session = cnx.session()

snow_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)
pd_df = snow_df.to_pandas()  # pandas.DataFrame with columns: FRUIT_NAME, SEARCH_ON

fruit_options = pd_df["FRUIT_NAME"].tolist()

name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect(
    "Select your favorite fruits (up to 5):",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    # Join selections into a single string for display / insert
    ingredient_list = " ".join(ingredients_list)
    st.write(f"Fruit list is {ingredient_list}")

    for fruit_chosen in ingredients_list:
        # Lookup SEARCH_ON for the chosen fruit
        row = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"]
        search_on = row.iloc[0] if not row.empty else fruit_chosen

        st.subheader(f"{fruit_chosen} Nutrition Information")

        # Call your API (use search_on if that's what the endpoint expects)
        url = f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        resp = requests.get(url)

        if resp.ok:
            # Show JSON nicely; if you prefer a table, use pd.DataFrame([resp.json()])
            st.json(resp.json())
        else:
            st.error(f"API request failed ({resp.status_code}) for {fruit_chosen}")

    # Place Order button
    if st.button("Place Order"):
        # Basic escaping for single quotes so SQL doesn't break on names like O'Reilly
        safe_ingredients = ingredient_list.replace("'", "''")
        safe_name = (name_on_order or "").replace("'", "''")

        session.sql(
            "INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER) "
            f"VALUES ('{safe_ingredients}', '{safe_name}')"
        ).collect()

        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
