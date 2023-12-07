import base64
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pipe = pickle.load(open('pipe.pkl', 'rb'))

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

color_theme = """
<style>

    @font-face {
        font-family: 'Graphik';
        src: url('./Graphik-BlackItalic-Trial.otf');
    }
    
    body {
        font-family: 'Graphik', sans-serif;
        background-color: #4B0082; 
        color: #FFFFFF;  
        margin: 20px;  
    }

    .stTextInput {
        background-color: #800080;  
        color: #FFFFFF;  
        border-radius: 12px;  
        text-align: center;  
        margin-bottom: 20px;  
        font-family: 'Graphik', sans-serif;
    }

    .stMarkdown {
        background-color: #0496FF;  
        color: #FFFFFF;  
        border-radius: 12px;  
        text-align: center;  
        margin-bottom: 20px;  
        font-family: 'Graphik', sans-serif;
    }

    .css-19ih76x {
        background-color: #26F7FD !important;
        color: #FFFFFF;  
        border-radius: 12px;  
        margin-bottom: 20px;  
        font-family: 'Graphik', sans-serif;
    }

    .stButton {
        color: #FFFFFF;  
        border-radius: 12px;  
        margin-bottom: 20px;  
        font-family: 'Graphik', sans-serif;
    }

    .stSelectbox {
        background-color: #42A5F5; 
        color: #FFFFFF;
        border-radius: 12px;  
        margin-bottom: 20px;  
        text-align: center;
        font-family: 'Graphik', sans-serif;
    }

    .stNumberInput {
        background-color: #42A5F5;  
        color: #FFFFFF;  
        border-radius: 12px;  
        text-align: center;  
        margin-bottom: 20px;  
        font-family: 'Graphik', sans-serif;
    }

    .stDataFrame {
        background-color: #6A5ACD;  
        color: #FFFFFF;  
        border-radius: 12px;  
        text-align: center;  
        margin-bottom: 20px;  
        font-family: 'Graphik', sans-serif;
    }

    .stSelectbox label {
        text-align: center !important;  
    }
    
</style>
"""

st.markdown(color_theme, unsafe_allow_html=True)

st.image('bgbg2.png', width=120, caption='')

st.title('IPL Win Predictor')
st.sidebar.header('Set Match Conditions')

with st.sidebar:
    batting_team = st.selectbox(' 🏏 Select the batting team', sorted(teams))
    bowling_team = st.selectbox(' 🔴 Select the bowling team', sorted(teams))
    selected_city = st.selectbox(' 🏟️ Select host city', sorted(cities))
    target = st.slider(' 🏏🔢 Select Target Score', min_value=50, max_value=300, value=150, step=1)

col1, col2 = st.columns(2)

with col1:
    score = st.number_input(' 🔢 Score', help="Enter the current score")
with col2:
    overs = st.number_input(' 🕒 Overs completed', help="Enter the number of overs completed")

col3, col4, col5 = st.columns(3)

with col3:
    wickets = st.number_input(' 🏏🚶 Wickets out', help="Enter the number of wickets fallen")
with col4:
    st.text("")
with col5:
    st.text("")

if st.button('Get Win Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets],
                             'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    win_probability = round(result[0][1] * 100)
    loss_probability = round(result[0][0] * 100)

    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#1E1E1E", "grid.color": "#3E3E3E", "text.color": "white"})

    st.success(f"{batting_team} Win Probability: {win_probability}%")
    st.error(f"{bowling_team} Win Probability: {loss_probability}%")

    chart_data = pd.DataFrame(
        {'Team': [batting_team, bowling_team], 'Probability': [win_probability, loss_probability]})
    st.write("### Win Probability Chart")
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#1E1E1E')
    sns.barplot(x='Team', y='Probability', data=chart_data, ax=ax, palette=['green', 'red'])
    ax.set_ylabel('Win Probability (%)', color='white')
    ax.set_xlabel('Team', color='white')
    ax.tick_params(axis='both', colors='white')
    ax.set_title('Win Probability Chart', color='white')
    st.pyplot(fig)

    st.info(
        f"With {balls_left} balls left and {wickets} wickets in hand, the required run rate (RRR) is {round(rrr, 2)}.")

    if runs_left <= 0:
        st.success("The target has been achieved!")
    elif runs_left <= 10:
        st.warning("It's a close match! The target is within reach.")
    elif rrr > crr:
        st.warning("The required run rate is higher than the current run rate. The team needs to accelerate.")
    else:
        st.success("The team is in a good position to win!")


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('blu.jpg')
