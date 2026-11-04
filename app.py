import duckdb
import streamlit as st
import ast
from click import option

con = duckdb.connect(database="data/exercises_sql_tables.duckdb",read_only=False)


# ANSWER_STR = """SELECT * FROM beverages     CROSS JOIN food_items"""
#
# solution_df = duckdb.sql(ANSWER_STR).df()

#st.write("SQL test")
with st.sidebar:
    theme = st.selectbox(
        "What do you want to review",
        ("cross_joins", "Group By", "Window func"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected: ", theme)
    exercise = con.execute(f"select * from memory_state where theme = '{theme}'").df()
    st.write(exercise)
st.header("enter your code:")
query = st.text_area(label="votre sql", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)
#
#     if len(result.columns) != len(solution_df.columns):
#         st.write("Some columns are missing")
#
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing")
#
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#             f"result has a {n_lines_difference} lines difference with the solution_df"
#         )
#     # st.dataframe(result.compare(solution_df))
#
tab2, tab3 = st.tabs(["Tables", "Solution"])
#
with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])

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
