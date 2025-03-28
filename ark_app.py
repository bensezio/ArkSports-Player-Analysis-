import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64
import os

# Fixed player data with categorized attributes
players_data = {
    # Basic Information
    'Name': ['Lionel Messi', 'Cristiano Ronaldo', 'Neymar Jr'],
    'Age': [34, 36, 29],
    'Height': [170, 187, 175],  # cm
    'Weight': [72, 83, 68],     # kg
    'Position': ['Forward', 'Forward', 'Forward'],
    
    # Field Performance Attributes
    'Goals': [30, 35, 20],
    'Assists': [15, 10, 18],
    'Passes': [26, 29, 22],
    'Shots': [55, 57, 52],
    
    # Training Scores (out of 100)
    'Speed': [85, 90, 88],
    'Endurance': [80, 85, 82],
    'Power': [75, 88, 70]
}

# Create DataFrame
df = pd.DataFrame(players_data)

# Function to calculate an overall player rating based on relevant attributes
def calculate_rating(row):
    return (
        0.25 * row['Goals'] +           # Field performance weighted higher
        0.20 * row['Assists'] +
        0.15 * row['Passes'] / 100 +    # Scaled for balance
        0.15 * row['Shots'] / 10 +      # Scaled for balance
        0.10 * row['Speed'] +           # Training scores contribute less
        0.10 * row['Endurance'] +
        0.05 * row['Power']
    )

# Add Player Rating to DataFrame
df['Player_Rating'] = df.apply(calculate_rating, axis=1)

# Streamlit app configuration
st.set_page_config(page_title="Ark Sports Management - Player Assessment", layout="wide")
st.title("Ark Sports Management - Player Assessment Demo")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a section:", ["Player Profiles", "Player Comparison", "Custom Reports"])

# Section 1: Player Profiles (Unchanged)
if app_mode == "Player Profiles":
    st.header("Player Profiles")
    player_name = st.selectbox("Select Player:", df['Name'].unique())
    player_data = df[df['Name'] == player_name].iloc[0]

    st.subheader(f"Profile for {player_name}")
    col1, col2 = st.columns([1, 2])

    with col1:
        # Basic Information
        st.write("**Basic Information**")
        basic_cols = st.columns(4)
        basic_cols[0].write(f"Age: {player_data['Age']}")
        basic_cols[1].write(f"Height: {player_data['Height']} cm")
        basic_cols[2].write(f"Weight: {player_data['Weight']} kg")
        basic_cols[3].write(f"Position: {player_data['Position']}")

        # Field Performance Attributes
        st.write("**Field Performance**")
        field_cols = st.columns(4)
        field_cols[0].write(f"Goals: {player_data['Goals']}")
        field_cols[1].write(f"Assists: {player_data['Assists']}")
        field_cols[2].write(f"Passes: {player_data['Passes']}")
        field_cols[3].write(f"Shots: {player_data['Shots']}")

        # Training Scores
        st.write("**Training Scores**")
        training_cols = st.columns(3)
        training_cols[0].write(f"Speed: {player_data['Speed']}")
        training_cols[1].write(f"Endurance: {player_data['Endurance']}")
        training_cols[2].write(f"Power: {player_data['Power']}")

        # Overall Rating
        st.write("**Overall Rating**")
        st.metric(label="Player Rating", value=round(player_data['Player_Rating'], 2))

    with col2:
        # Radar chart for visualization
        attributes = ['Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power']
        values = [player_data[attr] for attr in attributes]
        fig = px.line_polar(
            r=values,
            theta=attributes,
            line_close=True,
            title=f"Attribute Profile for {player_name}"
        )
        fig.update_traces(fill='toself')
        st.plotly_chart(fig, use_container_width=True)

# Section 2: Player Comparison (Unchanged)
elif app_mode == "Player Comparison":
    st.header("Player Comparison")
    selected_players = st.multiselect("Select up to 3 players:", df['Name'].unique(), max_selections=3)
    
    if selected_players:
        comparison_df = df[df['Name'].isin(selected_players)]
        
        # Comparison Table
        st.write("**Comparison Table**")
        st.dataframe(comparison_df.set_index('Name')[['Age', 'Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power', 'Player_Rating']].T)

        # Radar Chart for Attributes Comparison
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

# Section 3: Custom Reports (Updated with PDF Visualization)
elif app_mode == "Custom Reports":
    st.header("Custom Reports")
    player_name = st.selectbox("Select Player for Report:", df['Name'].unique())
    
    if st.button("Generate Report"):
        player_data = df[df['Name'] == player_name].iloc[0]
        
        # Generate Radar Chart and save as image
        attributes = ['Goals', 'Assists', 'Passes', 'Shots', 'Speed', 'Endurance', 'Power']
        values = [player_data[attr] for attr in attributes]
        fig = px.line_polar(r=values, theta=attributes, line_close=True, title=f"Attribute Profile for {player_name}")
        fig.update_traces(fill='toself')
        fig.write_image("radar_chart.png")
        
        # Preview the report (unchanged)
        st.subheader("Report Preview")
        st.write(f"**Ark Sports Management - Player Report: {player_name}**")
        
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
        
        st.write(f"**Overall Rating: {round(player_data['Player_Rating'], 2)}**")
        st.image("radar_chart.png", caption="Attribute Profile", use_column_width=True)
        
        # Generate PDF with visualization
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title
        pdf.cell(200, 10, txt=f"Ark Sports Management - Player Report: {player_name}", ln=True, align="C")
        pdf.ln(10)
        
        # Basic Information Table
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
        
        # Field Performance Table
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
        
        # Training Scores Table
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
        
        # Overall Rating
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Overall Rating: {round(player_data['Player_Rating'], 2)}", ln=True)
        pdf.ln(10)
        
        # Add Radar Chart Image to PDF
        pdf.image("radar_chart.png", x=50, y=pdf.get_y(), w=100)
        
        # Save and provide download
        pdf_output = f"{player_name}_report.pdf"
        pdf.output(pdf_output)
        
        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name=pdf_output,
                mime="application/pdf"
            )
        
        # Clean up the temporary image file
        os.remove("radar_chart.png")
