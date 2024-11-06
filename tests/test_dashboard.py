# Create the dashboard test file
with open('/content/drive/MyDrive/tello-simulation/tests/test_dashboard.py', 'w') as f:
    f.write('''
import streamlit as st
import plotly.graph_objects as go
from mock_data.states import TelloState
import time

def main():
    st.set_page_config(layout="wide")
    st.title("Tello Digital Twin Dashboard")

    # Initialize drone
    tello = TelloState()

    # Create columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Control Panel")
        
        # Basic commands
        st.write("Basic Commands")
        cmd_cols = st.columns(4)
        
        if cmd_cols[0].button("Takeoff"):
            tello.take_off()
            
        if cmd_cols[1].button("Land"):
            tello.land()
            
        if cmd_cols[2].button("Emergency Stop"):
            tello.land()
            
        # Height control
        st.write("Height Control")
        target_height = st.slider("Target Height (m)", 0.3, 10.0, 1.0, 0.1)
        if st.button("Set Height"):
            tello.set_height(target_height)

        # Movement control
        st.write("Movement Control")
        move_cols = st.columns(2)
        
        direction = move_cols[0].selectbox(
            "Direction",
            ["forward", "back", "left", "right"]
        )
        
        distance = move_cols[1].number_input(
            "Distance (cm)",
            min_value=20,
            max_value=500,
            value=100
        )
        
        if st.button("Move"):
            tello.move(direction, distance)

    with col2:
        st.subheader("Drone State")
        
        # Create state display
        state = tello.get_state_dict()
        
        # Create metrics
        metrics_cols = st.columns(3)
        metrics_cols[0].metric("Height (m)", f"{state['height']:.2f}")
        metrics_cols[1].metric("Battery %", state['battery'])
        metrics_cols[2].metric("Speed (km/h)", f"{state['speed']:.1f}")
        
        # Create 3D visualization
        fig = go.Figure(data=[
            go.Scatter3d(
                x=[state['x_pos']],
                y=[state['y_pos']],
                z=[state['height']],
                mode='markers+text',
                marker=dict(size=10, color='red'),
                text=['Drone'],
                name='Current Position'
            )
        ])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='X Position (m)',
                yaxis_title='Y Position (m)',
                zaxis_title='Height (m)',
                aspectmode='cube'
            ),
            title='Drone Position',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
''')

# Now let's run it with ngrok to make it accessible
!pip install pyngrok
from pyngrok import ngrok

# Start Streamlit
!streamlit run /content/drive/MyDrive/tello-simulation/tests/test_dashboard.py &

# Create tunnel
public_url = ngrok.connect(port='8501')
print(f"Dashboard is available at: {public_url}")