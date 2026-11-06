import duckdb
import streamlit as st
import os
import logging
import ast
from click import option
if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
con = duckdb.connect(database="data/exercises_sql_tables.duckdb",read_only=False)


# ANSWER_STR = """SELECT * FROM beverages     CROSS JOIN food_items"""
#

#st.write("SQL test")
with st.sidebar:
    available_themes_df=con.execute("SELECT DISTINCT Theme from memory_state").df()
    #st.dataframe(available_themes_df["theme"].unique())
    # st.write(available_themes)
    theme = st.selectbox(
        "What do you want to review",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme:
        st.write(f"You selected {theme}")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"

    else:
        select_exercise_query=f"SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    #st.write("You selected: ", theme)
    #exercise = con.execute(f"select * from memory_state where theme = '{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)

    exercise_name= exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql","r") as f:
        answer  = f.read()

    solution_df =  con.execute(answer).df()

st.header("enter your code:")
query = st.text_area(label="votre sql", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)
# #
#     if len(result.columns) != len(solution_df.columns):
#         st.write("Some columns are missing")

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )
    # st.dataframe(result.compare(solution_df))
#
tab2, tab3 = st.tabs(["Tables", "Solution"])
#
with tab2:
    exercise_tables = exercise.loc[0, "tables"]

    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table=  con.execute(f"select * from '{table}'").df()
        st.dataframe(df_table)


#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)
#
with tab3:
    exercise_name= exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql","r") as f:
        answer  = f.read()
    st.write(answer)
