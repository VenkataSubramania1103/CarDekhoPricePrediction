import streamlit as st
import pandas as pd
import pickle

# Title of the application
st.title("Car dekho Price predition")

data_frame=pd.read_csv('cols_cars_details.csv')
oem_list=data_frame['oem'].unique()


# Input fields for user data
engine_displacement = st.number_input('Engine Displacement (cc):', min_value=0)
Torque = st.number_input('Torque (Nm):', min_value=0)
wheel_size = st.number_input('Wheel Size (inches):', min_value=0.0)
cylinder = st.number_input('Number of Cylinders:', min_value=1, step=1)
cruise = st.number_input('Cruise Control (1 for Yes, 0 for No):', min_value=0, max_value=1)
ignitor = st.number_input('Start-Stop Button (1 for Yes, 0 for No):', min_value=0, max_value=1)
steer = st.number_input('Steering Wheel Gearshift Paddles (1 for Yes, 0 for No):', min_value=0, max_value=1)
transmission = st.selectbox('Transmission Type:', ['Manual', 'Automatic'])
oem = st.selectbox('Choose a car brand:', oem_list)
model_list=list(data_frame['model'].unique())
models=[model for model in model_list if model.startswith(oem)]
model = st.selectbox('Choose a car model:', models)
kilometer = st.number_input('Kilometers Driven:', min_value=0.0)

# Button to submit the data
if st.button('Submit'):
    # Define the columns
    cols = ['Engine Displacement', 'Torque', 'Wheel Size', 'No of Cylinder',
            'Cruise Control.1', 'Engine Start Stop Button',
            'Steering Wheel Gearshift Paddles', 'transmission_Manual',
            'oem_Mercedes-Benz', 'model_Mercedes-Benz AMG G 63',
            'model_Toyota Land Cruiser 300', 'km']

    # Create a DataFrame with one row
    X = pd.DataFrame([[engine_displacement, Torque, wheel_size, cylinder,
                       cruise, ignitor, steer, 
                       1 if transmission == 'Manual' else 0,
                       1 if oem == 'Mercedes-Benz' else 0,
                       1 if model == 'Mercedes-Benz AMG G 63' else 0,
                       1 if model == 'Toyota Land Cruiser 300' else 0,
                       kilometer]], columns=cols)

    # Display the DataFrame
    #st.subheader("Input Data")
    #st.dataframe(X)

    df=pd.read_csv('StandardScalerMapping.csv')
    for i in df.columns[1:]:
        a=df[i]
        X[i]=(X[i]-a[0])/a[1]

    with open('best_prediction_model.pkl', 'rb') as file:
        model = pickle.load(file)
    st.header("Predicted Price:(Rs)")
    st.markdown(float(abs(model.predict(X)/70)))
    
