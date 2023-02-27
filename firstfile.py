import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#url_ = 'https://raw.githubusercontent.com/janumirra/asnmnt_data/main/Bhumio%20Asnmnt.xlsx'
GDP_df = pd.read_excel("Bhumio Asnmnt.xlsx",'GDP') 
CLI_df = pd.read_excel("Bhumio Asnmnt.xlsx",'CLI')
CPI_df = pd.read_excel("Bhumio Asnmnt.xlsx",'CPI of all items')
#print(GDP_df)
#GDP cleaning
GDP_df.rename(columns={'Period': 'Time'}, inplace=True)
GDP_df['India'] = GDP_df['India'].astype(str).str.replace('..', '0')
GDP_df['India']=GDP_df['India'].astype('float64',copy=False)
GDP_df[['Quarter', 'Year']] = GDP_df.Time.str.split("-", expand = True)
#GDP_df.drop(columns=['Quarter'])
conditions = {
    "Q1": '-3-31',
    "Q2": '-6-30',
    "Q3": '-9-30',
    "Q4": '-12-31' 
}
GDP_df['Time']=[GDP_df["Year"][i]+ conditions[j] for i in range(len(GDP_df["Year"])) for j in conditions if GDP_df["Quarter"][i]==j]
GDP_df['Time'] =  pd.to_datetime(GDP_df['Time'])
GDP_df['Year']=GDP_df['Year'].astype('int64',copy=False)

##################################
#CLI Cleaning
CLI_df[['Month', 'Year']] = CLI_df.Time.str.split("-", expand = True)
CLI_df['Year']=CLI_df['Year'].astype('int64',copy=False)
CLI_df['Time'] =  pd.to_datetime(CLI_df['Time'])
###################################
#CPI cleaning

#CPI_df[['Month', 'Year']] = CPI_df['Time'].astype(str).str.split("-", expand = True)
#CPI_df[['Month', 'Year']] = CPI_df.Time.str.split("-", expand = True)
CPI_df['Year'] = CPI_df['Time'].astype(str).str.split('-', expand = True)[1]
CPI_df['Year']=CPI_df['Year'].astype('int64',copy=False)
CPI_df['Time'] =  pd.to_datetime(CPI_df['Time'])

######################################

st.set_page_config(page_title ="Investment helper App",
                page_icon= ":chart_with_upwards_trend:",
                layout= "wide"
                )
              
st.sidebar.header(":chart_with_upwards_trend: Investment Helper Dashboard")
st.sidebar.image("https://wp-asset.groww.in/wp-content/uploads/2018/01/19131009/businessman-gc41b408d6_1280.png")
expander = st.sidebar.expander("What is GDP?")
expander.write("""
    Gross Domestic Product.
     If GDP is rising—meaning the economy is performing well—those same
     companies can also raise additional funds by borrowing from banks 
     or issuing new debt, called bonds. The bonds are purchased by investors,
      and the funds are used for business expansion and growth; also boosting 
      GDP. A growing GDP indicates a strong economy, one where people are
    employed and companies are growing

""")
expander.image("https://media.istockphoto.com/id/1279128755/vector/gross-domestic-product-concept.jpg?s=612x612&w=0&k=20&c=8vYjysgN1f6j2LcxT616sNjDZYoYRh3edwAMGfeJfA8=")
#st.markdown('##')

expander = st.sidebar.expander("What is CLI?")
expander.write("""
    The composite leading indicator (CLI) (business confidence indicator-BCI + consumer confidence indicator-CCI)
    is designed to provide early signals of turning points in business cycles showing fluctuation of the economic 
    activity around its long term potential level.

BCI provides information on future developments, based upon opinion surveys on developments in production,
 orders and stocks of finished goods in the industry sector. Numbers above 100 suggest an
   increased confidence in near future business performance, and numbers below 100 indicate pessimism towards
    future performance.

CCI provides an indication of future developments of households’ consumption and saving, based upon answers 
regarding their expected financial situation, their sentiment about the general economic situation, unemployment 
and capability of savings. An indicator above 100 signals a boost in the consumers’ confidence towards the future economic situation, as a consequence of which they are less prone to 
save, and more inclined to spend money on major purchases in the next 12 months. Values below 100 indicate a 
  pessimistic attitude towards future developments in the economy, possibly resulting in a tendency to save more 
  and consume less. 
""")
expander.image("https://media.istockphoto.com/id/1144244585/vector/businessman-hanging-on-needle-speed-gauge-low-risk-management-concept.jpg?s=612x612&w=0&k=20&c=9PkKoYygbMh9MZkTv4vgtLfjmpTwOjTQvuj47UJ8p2A=")
#st.markdown('##')
expander = st.sidebar.expander("What is CPI?")
expander.write("""
    A consumer price index is estimated as a series of summary measures of the period-to-period proportional 
    change in the prices of a fixed set of consumer goods and services of constant quantity and characteristics,
     acquired, used or paid for by the reference population. 
     CPI is the measure of inflation. As inflation occurs, purchasing power decreases, meaning that it 
     costs more to buy the same good or service, or that the same amount of money buys fewer goods and services.
    For investors, it is important that the returns on their investments are at least the same rate as inflation;
     if they are less, then their investments are losing money even if it shows gains. Similarly, 
     individuals should ensure that their salaries increase every year at least as much as the rate of inflation,
      otherwise, they are technically making less money.For consumers, inflation means higher prices on goods and services, and a loss of purchasing power if their income fails to keep up. For investors, it means moving some of their money to assets that benefit from inflation or at least keep up with its pace.

""")
expander.image("https://media.istockphoto.com/id/1271390356/photo/shopping-basket-with-indian-rupees-money-around-food-products-vegetables-and-fruits-the.jpg?s=612x612&w=0&k=20&c=wwg9vQ1xV8uErTzrF6RJnOkf--LMgei6XVz179OFyJc=")
#st.markdown('##')
#top slider and dropdown
left_column, right_column=st.columns(2)
with left_column:
    graph_drop = st.selectbox(
    'Which Graph_detail would you like to view?',
    ('GDP', 'CPI', 'CLI'))
    st.write('You selected:', graph_drop)

with right_column:
    Year_chosen = st.slider(
    'Slide to select Year-range',
    2020, 2023, (2021, 2023))
    st.write('Years:', Year_chosen)
st.markdown("---")


 # grapgh and card
if graph_drop=='GDP':
    gdp_df=GDP_df.copy()
    dff=gdp_df[(gdp_df["Year"]>=Year_chosen[0])&(gdp_df["Year"]<Year_chosen[1])]
    df = dff.drop(columns=['Time','Quarter','Year']) 
     
    fig = px.line(dff, x="Time", y=df.columns,
              hover_data={"Time": "|%B , %Y"},# only month and year
              title='Which country has a rising economy?')
    fig.update_xaxes(
      dtick="M1",
      tickformat="%b\n%Y",
      ticklabelmode="period")
    fig.update_layout(
      yaxis_title="GDP",
      )
    #fig.show()
elif graph_drop=="CLI":
    cli_df=CLI_df.copy()
    dff=cli_df[(cli_df["Year"]>=Year_chosen[0])&(cli_df["Year"]<Year_chosen[1])]
    df = dff.drop(columns=['Time','Month','Year'])
    fig = px.line(dff, x="Time", y=df.columns,
              hover_data={"Time": "|%B , %Y"},# only month and year
              title='Which country has an increased confidence in near-future business performance?')
    fig.update_xaxes(
      dtick="M1",
      tickformat="%b\n%Y",
      ticklabelmode="period")
    fig.update_layout(
      xaxis_title='Period',
      yaxis_title="CLI",
        )
    #fig.show()
elif graph_drop=="CPI":
    cpi_df=CPI_df.copy()
    dff=cpi_df[(cpi_df["Year"]>=Year_chosen[0])&(cpi_df["Year"]<Year_chosen[1])]
    df = dff.drop(columns=['Time','Year'])
    
    fig = px.line(dff, x="Time", y=df.columns,
              hover_data={"Time": "|%B , %Y"},# only month and year
              title='Which country has an increasing inflation rate?')
    fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y",
            ticklabelmode="period")
    fig.update_layout(
        xaxis_title='Period',
        yaxis_title="CPI of all items(inflation rate)",
        )
    #fig.show()

st.plotly_chart(fig)
