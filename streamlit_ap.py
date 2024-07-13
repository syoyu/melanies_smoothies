# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be', name_on_order)

#フルーツテーブルを表示
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True) --描画の指示


#複数選択ボックス
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5 #選択数の上限を設定
)

#選択された項目をリスト化（何も選ばれていないときは表示しない）
if ingredients_list: #実質is not nullという判定を含む
    ingredients_string = '' #空の文字列で変数を定義

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '#選択されたフルーツを文字列リストに追加する

    #st.write(ingredients_string)

    #テーブルへのインサートSQL文を作成
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()

    #注文確定ボタンを作成
    time_to_insert = st.button('Submit Order')

    #注文確定ボタンが押されたら、インサートSQL文を実行し、完了メッセージを出す
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

