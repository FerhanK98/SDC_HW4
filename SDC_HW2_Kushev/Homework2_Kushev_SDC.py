import pandas as pd
import streamlit as st
import json
import requests
import altair as alt

st.title('COVID-19 Dashboard') 
st.subheader('(Data is from June 2022 - November 2022)')

def load_data():
    df = pd.read_csv('data.csv') # https://www.ecdc.europa.eu/en/publications-data/data-covid-19-vaccination-eu-eea 
    df = df[(df.TargetGroup != 'Age<18') & 
        (df.TargetGroup != 'AgeUNK') & 
        (df.TargetGroup != 'ALL') & 
        (df.TargetGroup != 'HCW') & 
        (df.TargetGroup != 'LTCF') & 
        (df.TargetGroup != '1_Age60+') & 
        (df.TargetGroup != '1_Age<60') &
        (df.YearWeekISO.str.startswith('2022-W22'))] # from June until Now
    return df

data = load_data()

option = st.selectbox(
    'Choose an option to display the amount of doses by age group:',
    ['First Dose', 'Second Dose', 'Both'])

option1 = st.selectbox(
    'Which country would you like to check out?',
    ['ALL', 'AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK'])

if option1 == 'ALL':
    df2 = data
else:
    df2 = data[data['ReportingCountry']==option1]

if option == 'First Dose':
    option = 'FirstDose'
    df33 = df2.groupby('TargetGroup')[option].sum()
    df333 = pd.DataFrame(df2.groupby('Vaccine')[option].sum()).reset_index()
    xxx = df2['Population'].sum()
    yyy = df2['Population'].unique()[0]
    if option1 == 'ALL':
        st.text('Population (filterable by Country)')
        to_displ = (f"""
        <style>
        p.a {{
            font: bold 55px Courier;
            color: blue;
        }}
        </style>
        <p class="a">{xxx}</p>""")
        st.markdown(to_displ, unsafe_allow_html=True)
    else:
        st.text('Population (filterable by Country)')
        to_displ = (f"""
        <style>
        p.a {{
            font: bold 55px Courier;
            color: blue;
        }}
        </style>
        <p class="a">{yyy}</p>""")
        st.markdown(to_displ, unsafe_allow_html=True)
    st.bar_chart(df33)
    df333['FirstDose%'] = (round(df333['FirstDose']/df333['FirstDose'].sum()*100, 2))
    df333 = df333[df333['FirstDose%'] >= 1]
    df333 = df333.sort_values(by='FirstDose%', ascending=False)
    base = alt.Chart(df333).encode(
    theta=alt.Theta("FirstDose%:Q", stack=True), color=alt.Color("Vaccine:N"))
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=150, size=10).encode(text="Vaccine:N")
    pie + text
    st.table(df333)
    
elif option == 'Second Dose':
    option = 'SecondDose'
    df22 = df2.groupby('TargetGroup')[option].sum()
    df222 = pd.DataFrame(df2.groupby('Vaccine')[option].sum()).reset_index()
    xxx = df2['Population'].sum()
    yyy = df2['Population'].unique()[0]
    if option1 == 'ALL':
        st.text('Population (filterable by Country)')
        to_displ = (f"""
        <style>
        p.a {{
            font: bold 55px Courier;
            color: blue;
        }}
        </style>
        <p class="a">{xxx}</p>""")
        st.markdown(to_displ, unsafe_allow_html=True)
    else:
        st.text('Population (filterable by Country)')
        to_displ = (f"""
        <style>
        p.a {{
            font: bold 55px Courier;
            color: blue;
        }}
        </style>
        <p class="a">{yyy}</p>""")
        st.markdown(to_displ, unsafe_allow_html=True)
    st.bar_chart(df22)
    df222['SecondDose%'] = (round(df222['SecondDose']/df222['SecondDose'].sum()*100, 2))
    df222 = df222[df222['SecondDose%'] >= 1]
    df222 = df222.sort_values(by='SecondDose%', ascending=False)
    base = alt.Chart(df222).encode(
    theta=alt.Theta("SecondDose%:Q", stack=True), color=alt.Color("Vaccine:N"))
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=150, size=10).encode(text="Vaccine:N")
    pie + text
    st.table(df222)
    
else:
    df3 = df2.groupby('TargetGroup')['FirstDose'].sum()
    df4 = df2.groupby('TargetGroup')['SecondDose'].sum()
    list4 = df2.TargetGroup.unique()
    viz = pd.DataFrame(zip(list4, df3, df4, ), columns=['TargetGroups', 'First Dose', 'Second Dose'])
    c = alt.Chart(viz).mark_circle(size=100).encode(
    x='First Dose',
    y='Second Dose',
    color='TargetGroups')
    xxx = df2['Population'].sum()
    yyy = df2['Population'].unique()[0]
    if option1 == 'ALL':
        st.text('Population (filterable by Country)')
        to_displ = (f"""
        <style>
        p.a {{
            font: bold 55px Courier;
            color: blue;
        }}
        </style>
        <p class="a">{xxx}</p>""")
        st.markdown(to_displ, unsafe_allow_html=True)
    else:
        st.text('Population (filterable by Country)')
        to_displ = (f"""
        <style>
        p.a {{
            font: bold 55px Courier;
            color: blue;
        }}
        </style>
        <p class="a">{yyy}</p>""")
        st.markdown(to_displ, unsafe_allow_html=True)        
    st.altair_chart(c, use_container_width=True)
    
    df99 = pd.DataFrame(df2.groupby('Vaccine')['FirstDose'].sum()).reset_index()
    df9 = pd.DataFrame(df2.groupby('Vaccine')['SecondDose'].sum()).reset_index()
    df9['Category'] = 'Second Dose'
    df99['Category'] = 'First Dose'
    viz99 = pd.concat([df99, df9])
    viz99 = viz99.fillna(0)
    viz99['Dose'] = round(viz99['FirstDose']+viz99['SecondDose'])
    viz99 = viz99[(viz99['Dose']>=1) & ((viz99['FirstDose']>=1) | (viz99['SecondDose']>=1))]
    asd = alt.Chart(viz99).mark_bar().encode(
    x='Dose:Q',
    y='Category:N',
    color='Category:N',
    row='Vaccine:N')
    st.altair_chart(asd, use_container_width=True)
    st.table(viz99[['Vaccine', 'Category', 'Dose']])
    
st.header("FastAPI")
st.write("Select two numbers from the sliders below and a percentage will be calculated (First number is for example 40% of the second number)")
one = st.slider('x', 0, 100, 1)
two = st.slider('y', 1, 100, 1)

input_vars = { "x":one, "y":two}

if st.button('Do it'):
    result = requests.post(url = "http://127.0.0.1:8000/do_it", data = json.dumps(input_vars))
    st.subheader(f"Result: {result.text}")




