import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import csv
import numpy as np
import plotly.express as px

# Load models at app initialization
models = {
    'defenders': joblib.load('models/defenders_model.pkl'),
    'midfielders': joblib.load('models/midfielders_model.pkl'),
    'forwards': joblib.load('models/forwards_model.pkl'),
    'goalkeepers': joblib.load('models/goalkeepers_model.pkl'),
}

# Mapping of positions to model keys
position_to_model_key = {
    'DF': 'defenders',
    'DFM': 'defenders',
    'CDM': 'midfielders',
    'MF': 'midfielders',
    'AM': 'midfielders',
    'FW': 'forwards',
    'GK': 'goalkeepers',
}

# Define features specific to each model
features_per_model = {
    'defenders': ['TklWon', 'Int', 'AerWon', 'BlkSh'],
    'midfielders': ['PasProg', 'Assists', 'ToSuc', 'Tkl'],
    'forwards': ['Goals', 'SoT', 'Assists', 'ToSuc'],
    'goalkeepers': ['SoT', 'PasTotCmp', 'PasShoAtt', 'Touches', 'AerWon', 'Clr', 'Err']
}

# Precomputed min and max predictions for each model (should be computed from training data)
min_max_predictions = {
    'defenders': {'min': 0.0, 'max': 10.0},
    'midfielders': {'min': 0.0, 'max': 10.0},
    'forwards': {'min': 0.0, 'max': 10.653},
    'goalkeepers': {'min': 0.0, 'max': 14.79},
}

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Football Analytics & Performance Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to detect delimiter
def detect_delimiter(file):
    """Detect the delimiter used in the CSV file by analyzing a sample of its content."""
    sample = file.read(1024).decode()
    file.seek(0)
    sniffer = csv.Sniffer()
    try:
        delimiter = sniffer.sniff(sample).delimiter
    except csv.Error:
        delimiter = ','
    return delimiter

# Function to load data
def load_data(uploaded_file):
    """Load the uploaded CSV file into a pandas DataFrame, handling parsing errors gracefully."""
    delimiter = detect_delimiter(uploaded_file)
    try:
        df = pd.read_csv(uploaded_file, delimiter=delimiter, on_bad_lines='skip')
        if df.empty:
            st.error("The uploaded file is empty or all lines were skipped due to formatting issues.")
            return None
        st.warning("Some lines were skipped due to formatting issues, but the remaining data was loaded successfully.")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Function to preprocess data
def preprocess_data(df):
    """Filter DataFrame based on selected player positions."""
    positions = st.sidebar.multiselect(
        "Select Player Position", 
        df["Position_Cleaned"].unique(), 
        default=df["Position_Cleaned"].unique()
    )
    return df[df["Position_Cleaned"].isin(positions)]

# Function to manually test the model
def manual_model_testing():
    """Allow users to test the model with custom inputs based on player position."""
    st.header("Test the Model with Custom Inputs")
    position = st.selectbox("Select Player Position:", list(position_to_model_key.keys()))
    model_key = position_to_model_key[position]
    model = models[model_key]
    
    input_values = {}
    for feature in features_per_model[model_key]:
        input_values[feature] = st.number_input(f"{feature}", value=0, step=1, format="%d")
    
    if st.button("Predict Performance"):
        input_df = pd.DataFrame([input_values])
        prediction = model.predict(input_df)[0]
        
        # Get precomputed min and max for the selected model
        min_pred = min_max_predictions[model_key]['min']
        max_pred = min_max_predictions[model_key]['max']
        
        # Compute scaled percentage
        if max_pred > min_pred:
            scaled_prediction = ((prediction - min_pred) / (max_pred - min_pred)) * 100
        else:
            scaled_prediction = 50.0
        
        # Display both raw and scaled predictions
        st.success(f"Predicted Performance Score: {prediction:.2f}")
        st.success(f"Scaled Performance Percentage: {scaled_prediction:.2f}%")

# Function for exploratory analysis
def exploratory_analysis(df):
    """Perform exploratory data analysis with visualizations."""
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches Played", df["MP"].sum() if "MP" in df.columns else "N/A")
    col2.metric("Total Goals Scored", df["Goals"].sum() if "Goals" in df.columns else "N/A")
    col3.metric("Total Assists", df["Assists"].sum() if "Assists" in df.columns else "N/A")
    col4.metric("Goals per Shot", round(df["G/Sh"].mean(), 2) if "G/Sh" in df.columns else "N/A")

    st.subheader("Goals Distribution")
    if "Goals" in df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df["Goals"], kde=True, ax=ax)
        ax.set_title("Distribution of Goals")
        ax.set_xlabel("Goals")
        ax.set_ylabel("Number of Players")
        st.pyplot(fig)
    else:
        st.write("Goals data is missing.")

    st.subheader("Top Goal Scorers")
    if "Goals" in df.columns and "Player" in df.columns:
        top_scorers = df.nlargest(10, "Goals")[["Player", "Goals"]]
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x="Goals", y="Player", data=top_scorers, ax=ax, palette="Blues_d")
        ax.set_title("Top 10 Goal Scorers")
        ax.set_xlabel("Goals")
        ax.set_ylabel("Player")
        st.pyplot(fig)
    else:
        st.write("Data for goals or player names is missing.")

    st.subheader("Top Assisters")
    if "Assists" in df.columns and "Player" in df.columns:
        top_assisters = df.nlargest(10, "Assists")[["Player", "Assists"]]
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x="Assists", y="Player", data=top_assisters, ax=ax, palette="Greens_d")
        ax.set_title("Top 10 Assisters")
        ax.set_xlabel("Assists")
        ax.set_ylabel("Player")
        st.pyplot(fig)
    else:
        st.write("Data for assists or player names is missing.")

    st.subheader("Players by Nation")
    if "Nation" in df.columns:
        nation_counts = df["Nation"].value_counts().nlargest(10)
        fig, ax = plt.subplots(figsize=(8, 6))
        nation_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Top 10 Nations by Number of Players")
        ax.set_xlabel("Nation")
        ax.set_ylabel("Number of Players")
        st.pyplot(fig)
    else:
        st.write("Nation data is missing.")

    st.subheader("Age Distribution")
    if "Age" in df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df["Age"], bins=20, kde=True, ax=ax, color="purple")
        ax.set_title("Age Distribution of Players")
        ax.set_xlabel("Age")
        ax.set_ylabel("Number of Players")
        st.pyplot(fig)
    else:
        st.write("Age data is missing.")

    st.subheader("Position Distribution")
    if "Position_Cleaned" in df.columns:
        position_counts = df["Position_Cleaned"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        position_counts.plot(kind="pie", ax=ax, autopct='%1.1f%%', startangle=90)
        ax.set_title("Distribution of Player Positions")
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.write("Position data is missing.")

# Function to predict performance on uploaded dataset
def batch_prediction(df):
    """Predict performance for all players in the uploaded dataset."""
    st.header("Predict Performance for Uploaded Dataset")
    
    # Initialize session state for predictions and sorting
    if 'predictions_df' not in st.session_state:
        st.session_state.predictions_df = None
    if 'sort_order' not in st.session_state:
        st.session_state.sort_order = "Descending"

    if st.button("Run Predictions"):
        # Ensure 'Position_Cleaned' exists
        if 'Position_Cleaned' not in df.columns:
            st.error("Error: 'Position_Cleaned' column is missing.")
            return
        
        # Map positions to model keys
        df['model_key'] = df['Position_Cleaned'].map(position_to_model_key)
        
        # Check for unmapped positions
        unmapped = df[df['model_key'].isna()]
        if not unmapped.empty:
            st.warning("Warning: Some positions are not mapped to any model.")
            st.write(unmapped['Position_Cleaned'].unique())
            df = df.dropna(subset=['model_key'])  # Drop unmapped rows
        
        # Prepare feature dataframe with all possible features
        all_features = list(set().union(*features_per_model.values()))
        prediction_df = pd.DataFrame(0, index=df.index, columns=all_features)
        for col in all_features:
            if col in df.columns:
                prediction_df[col] = df[col].fillna(0)
        
        # Make predictions using only relevant features per model
        df['Predicted_Performance'] = np.nan
        for key, model in models.items():
            mask = df['model_key'] == key
            if mask.any():
                model_features = features_per_model[key]
                pred_df = prediction_df.loc[mask, model_features]
                preds = model.predict(pred_df)
                df.loc[mask, 'Predicted_Performance'] = preds
        
        # Scale predictions to percentages within each model group
        def min_max_scale(series):
            min_pred = series.min()
            max_pred = series.max()
            if max_pred > min_pred:
                return ((series - min_pred) / (max_pred - min_pred)) * 100
            else:
                return pd.Series([50] * len(series), index=series.index)
                
        df['Predicted_Performance_Percent'] = df.groupby('model_key')['Predicted_Performance'].transform(min_max_scale)
        
        # Drop temporary column
        df = df.drop('model_key', axis=1)
        
        # Store predictions in session state
        st.session_state.predictions_df = df[['Player', 'Position_Cleaned', 'Predicted_Performance', 'Predicted_Performance_Percent']]

    # Display sorting options and results if predictions are available
    if st.session_state.predictions_df is not None:
        sort_order = st.radio("Sort Predictions By:", ["Ascending", "Descending"], horizontal=True)
        st.session_state.sort_order = sort_order
        
        # Apply sorting
        ascending = st.session_state.sort_order == "Ascending"
        df_sorted = st.session_state.predictions_df.sort_values(by="Predicted_Performance", ascending=ascending)
        
        # Display sorted results
        st.write(df_sorted)
        
        # Download sorted results
        csv = df_sorted.to_csv(index=False)
        st.download_button(
            label="Download Predictions",
            data=csv,
            file_name="predictions_sorted.csv",
            mime="text/csv"
        )

# **New Function for Player Assessment**
def player_assessment():
    """Calculate and visualize detailed player ratings, strengths, and weaknesses in a dashboard-like format."""
    st.header("Player Assessment")
    uploaded_file = st.file_uploader("Upload CSV File for Player Assessment:", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            # Define required columns for the rating calculation
            required_columns = ['Touch', 'Drive', 'Pass', 'Shot', 'Header', 'Sprint', 'Power', 'Endurance', 'TT', 'Height']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing columns: {', '.join(missing_columns)}")
            elif 'Name' not in df.columns:
                st.error("The dataset must include a 'Name' column.")
            else:
                # Calculate player ratings using the provided formula
                df['Player_Rating'] = (
                    0.15 * df['Touch'] +
                    0.12 * df['Drive'] +
                    0.13 * df['Pass'] +
                    0.15 * df['Shot'] +
                    0.10 * df['Header'] +
                    0.10 * df['Sprint'] +
                    0.08 * df['Power'] +
                    0.07 * df['Endurance'] +
                    0.05 * df['TT'] +
                    0.05 * df['Height']
                )

                # Player selection dropdown
                player_name = st.selectbox("Select Player:", df['Name'].unique())
                player_data = df[df['Name'] == player_name]

                if not player_data.empty:
                    # Extract player attributes
                    attributes = player_data[required_columns].iloc[0]

                    # Calculate strengths and weaknesses
                    strengths = attributes.nlargest(3).index.tolist()
                    weaknesses = attributes.nsmallest(3).index.tolist()

                    # Dashboard layout using columns
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        # Display overall rating
                        st.subheader(f"Overall Rating")
                        st.metric(label="Player Rating", value=round(player_data['Player_Rating'].values[0], 2))

                        # Display strengths
                        st.subheader("Strengths")
                        for strength in strengths:
                            st.write(f"- {strength} ({attributes[strength]:.2f})")

                        # Display weaknesses
                        st.subheader("Weaknesses")
                        for weakness in weaknesses:
                            st.write(f"- {weakness} ({attributes[weakness]:.2f})")

                    with col2:
                        # Radar chart for attributes
                        fig = px.line_polar(
                            r=attributes.values,
                            theta=attributes.index,
                            line_close=True,
                            title=f"Attribute Profile for {player_name}"
                        )
                        fig.update_traces(fill='toself')
                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True)),
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)

                else:
                    st.error("Player not found.")
                
                # Optional: Display top 10 players bar chart (retained from original)
                st.subheader("Top 10 Player Ratings")
                df_sorted = df.sort_values(by='Player_Rating', ascending=False)
                top_players = df_sorted.head(10)
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(x='Player_Rating', y='Name', data=top_players, ax=ax, palette='viridis')
                ax.set_title('Top 10 Player Ratings')
                ax.set_xlabel('Player Rating')
                ax.set_ylabel('Player')
                st.pyplot(fig)

# ... (Rest of your script remains unchanged, just ensure the new import and function are included)

# Main Streamlit App Logic
st.title("Football Analytics & Performance Prediction")
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a section:", ["About", "Test Model", "Upload & Analyze Data", "Predict Performance", "Player Assessment"])

if app_mode == "About":
    st.header("About This App")
    st.write("Analyze football player stats and predict their performance using machine learning.")

elif app_mode == "Test Model":
    manual_model_testing()

elif app_mode == "Upload & Analyze Data":
    st.header("Upload & Analyze Your Data")
    uploaded_file = st.file_uploader("Upload CSV File:", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            df = preprocess_data(df)
            st.write("Preview of your data:")
            st.dataframe(df.head())
            exploratory_analysis(df)
    else:
        st.info("Please upload a CSV file to proceed.")

elif app_mode == "Predict Performance":
    st.header("Predict Player Performance from Your Data")
    uploaded_file = st.file_uploader("Upload CSV File for Prediction:", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            df = preprocess_data(df)
            batch_prediction(df)
    else:
        st.info("Please upload a CSV file to proceed.")

elif app_mode == "Player Assessment":
    player_assessment()