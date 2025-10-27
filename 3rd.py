import streamlit as st
import random

# --- Simulation Function ---
def simulate_virus(num_systems, infection_chance, defense_strength, num_files, initial_state):
    systems = [initial_state] + ["Healthy"] * (num_systems - 1)
    infection_history = []

    for i in range(num_files):
        if systems[i % num_systems] == "Infected":
            for j in range(num_systems):
                if systems[j] == "Healthy":
                    if random.random() < infection_chance / 100:
                        systems[j] = "Infected"
        elif systems[i % num_systems] == "Healthy":
            if random.random() < defense_strength / 100:
                systems[i % num_systems] = "Defended"

        infection_history.append((i + 1, systems.copy()))

    return systems, infection_history


# --- Streamlit UI ---
st.title("🛡️ Simple Virus Simulation Tool")

# Sidebar for configuration
st.sidebar.header("⚙️ Simulation Settings")
num_systems = st.sidebar.number_input("Total Systems in Network:", 2, 50, 10)
infection_chance = st.sidebar.slider("Infection Chance (%)", 0, 100, 40)
defense_strength = st.sidebar.slider("Defense Strength (%)", 0, 100, 30)
num_files = st.sidebar.number_input("Number of Files in System:", 1, 100, 20)
initial_state = st.sidebar.selectbox("Initial System State:", ["Healthy", "Infected", "Defended"])

# Buttons for control
st.subheader("▶️ Run Simulation")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    run_button = st.button("Run Simulation")

with col2:
    defender_button = st.button("Activate Defender")

with col3:
    reset_button = st.button("Reset Simulation")


# Run Simulation
if run_button:
    systems, history = simulate_virus(num_systems, infection_chance, defense_strength, num_files, initial_state)

    st.subheader("📊 Final Simulation Results")
    result_table = {"System": list(range(1, num_systems + 1)), "State": systems}
    st.table(result_table)

    st.subheader("📝 Infection Timeline")
    for step, state in history:
        st.text(f"Step {step}: {state}")


# Defender Simulation
if defender_button:
    systems, history = simulate_virus(num_systems, infection_chance // 2, defense_strength + 20, num_files, initial_state)

    st.subheader("🛡️ Defender Results")
    result_table = {"System": list(range(1, num_systems + 1)), "State": systems}
    st.table(result_table)


# Reset
if reset_button:
    st.rerun()
