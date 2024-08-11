import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go

from config import GO_BASE_LAYOUT

app = st.navigation({
    "": [st.Page("views/Home.py", title="Home", icon=":material/home:")],
    "Tasks": [
        st.Page("views/Task_1.py", title="1 - Projectile Motion"),
        st.Page("views/Task_2.py", title="2 - Analytical Model"),
        st.Page("views/Task_3.py", title="3 - Hitting a Target"),
        st.Page("views/Task_4.py", title="4 - Maximize Projectile Range"),
        st.Page("views/Task_5.py", title="5 - Bounding Parabola"),
        st.Page("views/Task_6.py", title="6 - Arc Length of Projectile Motion"),
        st.Page("views/Task_7.py", title="7 - Range of Projectile vs. Time"),
        st.Page("views/Task_8.py", title="8 - Bouncing Projectile"),
        st.Page("views/Task_9.py", title="9 - Air Resistance"),
    ]
})

if __name__ == "__main__":
    app.run()
