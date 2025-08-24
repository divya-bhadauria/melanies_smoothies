# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie: ")

ingredients_list = st.multiselect(
    "Select your favorite fruits (upto 5):",
    my_dataframe,
    max_selections= 5
)

if ingredients_list:
    ingredient_list = ''
    #st.write("You selected:")
    for fruit_choosen in ingredients_list:
        #st.write(fruit_choosen)
        ingredient_list += fruit_choosen + " "

    st.write(f"Fruit list is {ingredient_list}")

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_list + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_place_order = st.button('Place Order')
    if time_to_place_order:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")




