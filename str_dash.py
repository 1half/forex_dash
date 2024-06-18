import requests, pandas as pd, streamlit as st
from Trader_made import free_api_key
from datetime import date, timedelta

today = date.today()- timedelta(days=1)

endpoints = st.sidebar.selectbox('End_points',options=['timeseries','historical'])
base_url = f"https://marketdata.tradermade.com/api/v1/{endpoints}?api_key={free_api_key}"

#ISO currency
cur_s = pd.read_csv("countryCurrISO.csv")
cur_s=list(cur_s)

#From API :( !!
#cur_list_url = f"https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key={free_api_key}"
#cur_list = requests.get(cur_list_url).json()
#cur_s = list(cur_list.values())[0]

st.title(":blue[Currency Exchange Rates]", anchor=None)
st.write("""   
                ## Historical currency rates
                source: TraderMade
             
             """)

if endpoints== 'timeseries':
    currency = st.sidebar.selectbox('currency',options=cur_s)
    interval = st.sidebar.selectbox('Inteval',options=['daily','hourly'])
    if interval=='daily':
        delta_date = timedelta(days = 365)
    else:
       delta_date = timedelta(days = 30)

    start_date =st.sidebar.date_input("Start date", today - delta_date,
                                   max_value=today,
                                   min_value=date(2010,1,1),
                                    format="YYYY-MM-DD")
    end_date = st.sidebar.date_input("End date",start_date+delta_date,
                                   max_value=start_date+delta_date,
                                   min_value=start_date,
                                    format="YYYY-MM-DD")

    tail_url = f"&currency={currency}&format=records&start_date={start_date}&end_date={end_date}&interval={interval}&period=1"
    url = base_url+tail_url

#get data       
    data = requests.get(url).json()
   #data from csv file, comment the above line and uncoment these to use csv
    #data = {
    #        "base_currency": "USD",
    #        "end_date": "2024-06-18",
    #        "endpoint": "timeseries",
    #        "quote_currency": "INR"}
    #df = pd.read_csv("2024-06-18T08-04_export.csv",index_col=0)
#heading
    st.header(f"""
                :green[Timeseries.]
            """,help="close: closing rate, high: highest rate, low: lowest rate, open: opening rate")
    try:
    #write info 
        st.write(f"""
                    #### Base Currency(ISO): {data["base_currency"]} | Quote_currency(ISO): {data["quote_currency"]}                 
                    start :{start_date} | end :{end_date}\n                  
                    For daily interval : Data available for one year period. | For hour interval: Data for one month period.
                """)
    #get dataframe of quotes
        df = pd.DataFrame(data["quotes"])
    #st.dataframe to display df.  
        st.dataframe(df,use_container_width = True)
        st.header(f"Value of {data["quote_currency"]} against {data["base_currency"]}",
                help="Scroll in the chart to zoom in, click and drag to move with in the chart")
        st.line_chart(data=df, x='date', y='close', color='#ADD8E6', use_container_width=True)
    except:
    #write data from url if the api returns with any erros ar different data.
        st.write(data)
    data = None

else:
#sidebar
    currency = st.sidebar.selectbox('currency',options=cur_s)
    data_date =st.sidebar.date_input("Date", today,
                                   max_value=today,
                                   min_value=date(2016,1,1),
                                    format="YYYY-MM-DD")
#url for data 
    tail_url = f"&currency={currency}&date={data_date}"
    url = base_url+tail_url
#get data
    data = requests.get(url).json()
    #heading
    st.header(f" :green[Historical]",help=" ")

#read and print data  
    try:
        df = pd.DataFrame(data["quotes"])
        st.dataframe(df,use_container_width = True)
    except:
        st.write(data)

    data = None