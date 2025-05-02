import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# Function to generate player report PDF
def generate_player_report(player_data, radar_chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Ark Sports Management - Player Report: {player_data['Name']}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Basic Information", ln=True)
    pdf.set_font("Arial", '', 12)
    basic_info = [
        ["Age", str(player_data['Age'])],
        ["Height", f"{player_data['Height']} cm"],
        ["Weight", f"{player_data['Weight']} kg"],
        ["Position", player_data['Position']]
    ]
    for row in basic_info:
        pdf.cell(100, 10, row[0], border=1)
        pdf.cell(100, 10, row[1], border=1)
        pdf.ln()
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Field Performance", ln=True)
    pdf.set_font("Arial", '', 12)
    field_performance = [
        ["Goals", str(player_data['Goals'])],
        ["Assists", str(player_data['Assists'])],
        ["Passes", str(player_data['Passes'])],
        ["Shots", str(player_data['Shots'])]
    ]
    for row in field_performance:
        pdf.cell(100, 10, row[0], border=1)
        pdf.cell(100, 10, row[1], border=1)
        pdf.ln()
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Training Scores", ln=True)
    pdf.set_font("Arial", '', 12)
    training_scores = [
        ["Speed", str(player_data['Speed'])],
        ["Endurance", str(player_data['Endurance'])],
        ["Power", str(player_data['Power'])]
    ]
    for row in training_scores:
        pdf.cell(100, 10, row[0], border=1)
        pdf.cell(100, 10, row[1], border=1)
        pdf.ln()
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Overall Rating: {round(player_data['Player_Rating'], 2)}", ln=True)
    pdf.ln(10)
    
    pdf.image(radar_chart_path, x=50, y=pdf.get_y(), w=100)
    
    pdf_output = f"{player_data['Name']}_report.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Function to generate comparison report PDF
def generate_comparison_report(selected_players, comparison_df, radar_chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Ark Sports Management - Player Comparison Report", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Selected Players:", ln=True)
    pdf.set_font("Arial", '', 12)
    for player in selected_players:
        pdf.cell(0, 10, player, ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Comparison Table", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, "Attribute", border=1)
    for player in selected_players:
        pdf.cell(40, 10, player, border=1)
    pdf.ln()
    attributes = ['Age', 'Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power', 'Player_Rating']
    for attr in attributes:
        pdf.cell(50, 10, attr, border=1)
        for player in selected_players:
            value = comparison_df.loc[comparison_df['Name'] == player, attr].values[0]
            pdf.cell(40, 10, str(value), border=1)
        pdf.ln()
    pdf.ln(10)
    
    pdf.image(radar_chart_path, x=50, y=pdf.get_y(), w=100)
    
    pdf_output = "comparison_report.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Player data
players_info = [
    {'Name': 'Lionel Messi', 'Age': 34, 'Height': 170, 'Weight': 72, 'Position': 'Forward', 'Goals': 30, 'Assists': 15, 'Passes': 26, 'Shots': 55, 'Speed': 85, 'Endurance': 80, 'Power': 75},
    {'Name': 'Cristiano Ronaldo', 'Age': 36, 'Height': 187, 'Weight': 83, 'Position': 'Forward', 'Goals': 35, 'Assists': 10, 'Passes': 29, 'Shots': 57, 'Speed': 90, 'Endurance': 85, 'Power': 88},
    {'Name': 'Neymar Jr', 'Age': 29, 'Height': 175, 'Weight': 68, 'Position': 'Forward', 'Goals': 20, 'Assists': 18, 'Passes': 22, 'Shots': 52, 'Speed': 88, 'Endurance': 82, 'Power': 70},
    {'Name': 'Kylian Mbappe', 'Age': 22, 'Height': 178, 'Weight': 73, 'Position': 'Forward', 'Goals': 28, 'Assists': 12, 'Passes': 24, 'Shots': 60, 'Speed': 95, 'Endurance': 78, 'Power': 80},
    {'Name': 'Mohamed Salah', 'Age': 29, 'Height': 175, 'Weight': 71, 'Position': 'Forward', 'Goals': 25, 'Assists': 14, 'Passes': 25, 'Shots': 50, 'Speed': 92, 'Endurance': 84, 'Power': 76},
    {'Name': 'Robert Lewandowski', 'Age': 33, 'Height': 185, 'Weight': 81, 'Position': 'Forward', 'Goals': 40, 'Assists': 8, 'Passes': 28, 'Shots': 65, 'Speed': 82, 'Endurance': 88, 'Power': 85},
    {'Name': 'Harry Kane', 'Age': 28, 'Height': 188, 'Weight': 86, 'Position': 'Forward', 'Goals': 27, 'Assists': 16, 'Passes': 30, 'Shots': 54, 'Speed': 78, 'Endurance': 86, 'Power': 83},
    {'Name': 'Erling Haaland', 'Age': 21, 'Height': 194, 'Weight': 88, 'Position': 'Forward', 'Goals': 32, 'Assists': 6, 'Passes': 20, 'Shots': 58, 'Speed': 89, 'Endurance': 75, 'Power': 90},
    {'Name': 'Kevin De Bruyne', 'Age': 30, 'Height': 181, 'Weight': 70, 'Position': 'Midfielder', 'Goals': 10, 'Assists': 20, 'Passes': 40, 'Shots': 40, 'Speed': 80, 'Endurance': 85, 'Power': 78},
    {'Name': 'Luka Modric', 'Age': 36, 'Height': 172, 'Weight': 66, 'Position': 'Midfielder', 'Goals': 5, 'Assists': 12, 'Passes': 35, 'Shots': 30, 'Speed': 75, 'Endurance': 82, 'Power': 70},
    {'Name': 'Bruno Fernandes', 'Age': 27, 'Height': 179, 'Weight': 69, 'Position': 'Midfielder', 'Goals': 15, 'Assists': 18, 'Passes': 38, 'Shots': 45, 'Speed': 78, 'Endurance': 84, 'Power': 75},
    {'Name': 'Joshua Kimmich', 'Age': 26, 'Height': 177, 'Weight': 73, 'Position': 'Midfielder', 'Goals': 3, 'Assists': 10, 'Passes': 42, 'Shots': 25, 'Speed': 76, 'Endurance': 88, 'Power': 72},
    {'Name': 'Phil Foden', 'Age': 21, 'Height': 171, 'Weight': 69, 'Position': 'Midfielder', 'Goals': 8, 'Assists': 14, 'Passes': 32, 'Shots': 35, 'Speed': 84, 'Endurance': 80, 'Power': 68},
    {'Name': 'Virgil van Dijk', 'Age': 30, 'Height': 193, 'Weight': 92, 'Position': 'Defender', 'Goals': 2, 'Assists': 3, 'Passes': 28, 'Shots': 15, 'Speed': 78, 'Endurance': 90, 'Power': 85},
    {'Name': 'Sergio Ramos', 'Age': 35, 'Height': 184, 'Weight': 82, 'Position': 'Defender', 'Goals': 4, 'Assists': 2, 'Passes': 25, 'Shots': 20, 'Speed': 75, 'Endurance': 85, 'Power': 80},
    {'Name': 'Trent Alexander-Arnold', 'Age': 23, 'Height': 175, 'Weight': 69, 'Position': 'Defender', 'Goals': 1, 'Assists': 12, 'Passes': 38, 'Shots': 18, 'Speed': 82, 'Endurance': 83, 'Power': 74},
    {'Name': 'Ruben Dias', 'Age': 24, 'Height': 187, 'Weight': 83, 'Position': 'Defender', 'Goals': 2, 'Assists': 1, 'Passes': 30, 'Shots': 10, 'Speed': 76, 'Endurance': 88, 'Power': 82},
    {'Name': 'Marquinhos', 'Age': 27, 'Height': 183, 'Weight': 75, 'Position': 'Defender', 'Goals': 3, 'Assists': 2, 'Passes': 32, 'Shots': 12, 'Speed': 79, 'Endurance': 86, 'Power': 78},
    {'Name': 'Alisson Becker', 'Age': 29, 'Height': 191, 'Weight': 91, 'Position': 'Goalkeeper', 'Goals': 0, 'Assists': 1, 'Passes': 18, 'Shots': 0, 'Speed': 70, 'Endurance': 75, 'Power': 80},
    {'Name': 'Gianluigi Donnarumma', 'Age': 22, 'Height': 196, 'Weight': 90, 'Position': 'Goalkeeper', 'Goals': 0, 'Assists': 0, 'Passes': 15, 'Shots': 0, 'Speed': 68, 'Endurance': 72, 'Power': 82}
]

# Create DataFrame
df = pd.DataFrame(players_info)

# Calculate Player Rating
def calculate_rating(row):
    return (
        0.25 * row['Goals'] +
        0.20 * row['Assists'] +
        0.15 * row['Passes'] / 100 +
        0.15 * row['Shots'] / 10 +
        0.10 * row['Speed'] +
        0.10 * row['Endurance'] +
        0.05 * row['Power']
    )

df['Player_Rating'] = df.apply(calculate_rating, axis=1)

# Streamlit app configuration
st.set_page_config(page_title="Ark Sports Management - Player Assessment", layout="wide")
st.title("Ark Sports Management - Player Assessment Demo")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a section:", ["Players", "Player Comparison"])

# Initialize session state for view mode
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "list"
if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None

# Players Tab
if app_mode == "Players":
    if st.session_state.view_mode == "list":
        st.header("Players")
        
        # Search bar and position filter
        search_query = st.text_input("Search players:", "")
        positions = df['Position'].unique()
        selected_positions = st.multiselect("Filter by position:", positions, default=positions)
        
        # Filter DataFrame based on search query and selected positions
        df_filtered = df[
            (df['Name'].str.contains(search_query, case=False, na=False)) &
            (df['Position'].isin(selected_positions))
        ].sort_values('Player_Rating', ascending=False)
        
        st.write("### Players List")
        if not df_filtered.empty:
            col_names = ['Name', 'Age', 'Position', 'Player Rating', 'View Profile']
            cols = st.columns([3, 1, 2, 2, 2])
            for i, col_name in enumerate(col_names):
                with cols[i]:
                    st.write(f"**{col_name}**")
            
            for index, row in df_filtered.iterrows():
                cols = st.columns([3, 1, 2, 2, 2])
                with cols[0]:
                    st.write(row['Name'])
                with cols[1]:
                    st.write(row['Age'])
                with cols[2]:
                    st.write(row['Position'])
                with cols[3]:
                    st.write(round(row['Player_Rating'], 2))
                with cols[4]:
                    if st.button("View", key=f"view_{row['Name']}"):
                        st.session_state.view_mode = "profile"
                        st.session_state.selected_player = row['Name']
                        st.rerun()
        else:
            st.write("No players found.")
    
    elif st.session_state.view_mode == "profile":
        player_name = st.session_state.selected_player
        player_data = df[df['Name'] == player_name].iloc[0]
        st.write(f"## Player Profile: {player_name}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Basic Information**")
            basic_cols = st.columns(4)
            basic_cols[0].write(f"Age: {player_data['Age']}")
            basic_cols[1].write(f"Height: {player_data['Height']} cm")
            basic_cols[2].write(f"Weight: {player_data['Weight']} kg")
            basic_cols[3].write(f"Position: {player_data['Position']}")
            
            st.write("**Field Performance**")
            field_cols = st.columns(4)
            field_cols[0].write(f"Goals: {player_data['Goals']}")
            field_cols[1].write(f"Assists: {player_data['Assists']}")
            field_cols[2].write(f"Passes: {player_data['Passes']}")
            field_cols[3].write(f"Shots: {player_data['Shots']}")
            
            st.write("**Training Scores**")
            training_cols = st.columns(3)
            training_cols[0].write(f"Speed: {player_data['Speed']}")
            training_cols[1].write(f"Endurance: {player_data['Endurance']}")
            training_cols[2].write(f"Power: {player_data['Power']}")
            
            st.write("**Overall Rating**")
            st.metric(label="Player Rating", value=round(player_data['Player_Rating'], 2))
        
        with col2:
            attributes = ['Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power']
            values = [player_data[attr] for attr in attributes]
            fig = px.line_polar(r=values, theta=attributes, line_close=True, title=f"Attribute Profile for {player_name}")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig, use_container_width=True)
        
        # Download button for player report
        if st.button("Download Player Report"):
            radar_chart_path = "radar_chart.png"
            fig.write_image(radar_chart_path)
            pdf_output = generate_player_report(player_data, radar_chart_path)
            with open(pdf_output, "rb") as file:
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=pdf_output,
                    mime="application/pdf"
                )
            os.remove(radar_chart_path)
            os.remove(pdf_output)
        
        # Back button to return to list
        if st.button("Back to List"):
            st.session_state.view_mode = "list"
            st.session_state.selected_player = None
            st.rerun()

# Player Comparison Tab
elif app_mode == "Player Comparison":
    st.header("Player Comparison")
    selected_players = st.multiselect("Select up to 3 players:", df['Name'].unique(), max_selections=3)
    
    if selected_players:
        comparison_df = df[df['Name'].isin(selected_players)]
        
        st.write("**Comparison Table**")
        st.dataframe(comparison_df.set_index('Name')[['Age', 'Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power', 'Player_Rating']].T)
        
        st.write("**Radar Chart Comparison**")
        attributes = ['Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power']
        melted_df = comparison_df.melt(id_vars='Name', value_vars=attributes, var_name='Attribute', value_name='Value')
        fig = px.line_polar(
            melted_df,
            r='Value',
            theta='Attribute',
            color='Name',
            line_close=True,
            title="Player Attributes Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Download Comparison Report"):
            radar_chart_path = "comparison_radar_chart.png"
            fig.write_image(radar_chart_path)
            pdf_output = generate_comparison_report(selected_players, comparison_df, radar_chart_path)
            with open(pdf_output, "rb") as file:
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=pdf_output,
                    mime="application/pdf"
                )
            os.remove(radar_chart_path)
            os.remove(pdf_output)