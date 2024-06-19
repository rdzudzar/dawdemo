import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta


data = {
    'Numerical': [1,5,3,8,0,2,3,0,4,5, 1,5,3,8,0,2,3,0,4,5],
    'Numerical 2': [23, 35, 46, 75, 79, 45, 23, 12, 5, 5, 1,5,3,8,0,2,3,0,4,5],
    'Categorical': ['Cat A', 'Cat A', 'Cat C', 'Cat B', 'Cat A','Cat A', 'Cat A', 'Cat C', 'Cat B', 'Cat A',
                    'Cat A', 'Cat B', 'Cat B', 'Cat A', 'Cat A','Cat A', 'Cat A', 'Cat A', 'Cat A', 'Cat A'],
    'Text': ['Text 1', 'Text 1', 'Text 1', 'Text 2', 'Text 2', 'Text 1', 'Text 1', 'Text 2', 'Text 2', 'Text 2',
             'Text 2', 'Text 1', 'Text 2', 'Text 2', 'Text 2', 'Text 2', 'Text 1', 'Text 1', 'Text 1', 'Text 2'],
    'Datetime': [datetime.now() - timedelta(days=i) for i in range(20)],
}

df = pd.DataFrame(data)


# TITLE
#----------------------------
st.title("DAW DEMO")

slider_num = st.slider("Numerical value", 0, 10)
number = st.number_input("Pick a number", 100, 200)
selectbox = st.selectbox("Pick from list", ["A", "B", "C", "D"])
checkbox = st.checkbox("Select this")

if checkbox:
    st.write(f"YOUR LETTER IS {selectbox}")


#----------------------------
# Sidebar 
st.sidebar.title("Filter Data")
selected_text = st.sidebar.multiselect("Select Text", df['Text'].unique())
start_date = st.sidebar.date_input("Start Date", df['Datetime'].min().date())
end_date = st.sidebar.date_input("End Date", df['Datetime'].max().date())




# Filter table
filtered_df = df[(df['Text'].isin(selected_text)) & (df['Datetime'].dt.date >= start_date) & (df['Datetime'].dt.date <= end_date)]
# Display the filtered DataFrame
#----------------------------
st.write("Filtered DataFrame:")
st.dataframe(filtered_df)




fig = px.line(filtered_df, x='Datetime', y='Numerical', title='Time Series Plot')
#----------------------------
st.plotly_chart(fig)




#----------------------------
# Just adding stuff to Expander
with st.expander("Expand"):
    #----------------------------
    aggregation_level = st.radio("Select the aggregation level:", ('Daily', 'Weekly'))

    # Just a python code
    if aggregation_level == 'Daily':
        aggregated_df = df.resample('D', on='Datetime').sum().reset_index()
        aggregated_df['Date'] = aggregated_df['Datetime'].dt.strftime('%Y-%m-%d')

    elif aggregation_level == 'Weekly':
        aggregated_df = df.resample('W-Mon', on='Datetime').sum().reset_index()

        df['Week Start'] = df['Datetime'] - df['Datetime'].dt.weekday * pd.Timedelta(days=1)
        df['Week End'] = df['Week Start'] + pd.Timedelta(days=6)
        aggregated_df['Week Start'] = aggregated_df['Datetime'] - pd.Timedelta(days=6)
        aggregated_df['Week End'] = aggregated_df['Datetime']
        aggregated_df['Date'] = aggregated_df['Week Start'].dt.strftime('%Y-%m-%d') + ' to ' + aggregated_df['Week End'].dt.strftime('%Y-%m-%d')


    fig = px.bar(aggregated_df, x='Datetime', y='Numerical', 
                title=f'Time Series Plot - {aggregation_level} Aggregation',
                hover_data={'Date': True, 'Numerical': True})
    #----------------------------
    st.plotly_chart(fig)




#----------------------------
with st.sidebar:
    check = st.checkbox("Written Summary")
    if check:
        st.write(f"Selectected {selected_text} within \
            {start_date} and {end_date}. \
            Average of the Numerical data was {np.mean(filtered_df['Numerical'])}")
        check2 = st.checkbox("Even more details?")
        if check2:
            avg_numerical_per_category = df.groupby('Categorical')['Numerical'].mean().reset_index()
            avg_numerical_per_category.columns = ['Categorical', 'Average Numerical']

            st.write("Average Numerical per Category:")
            st.dataframe(avg_numerical_per_category)


