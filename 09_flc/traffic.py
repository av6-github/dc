import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# 1. DEFINE INPUT AND OUTPUT VARIABLES

traffic_density = ctrl.Antecedent(
    np.arange(0, 51, 1),
    'traffic_density'
)

waiting_time = ctrl.Antecedent(
    np.arange(0, 121, 1),
    'waiting_time'
)

green_duration = ctrl.Consequent(
    np.arange(10, 91, 1),
    'green_duration'
)


# 2. TRAFFIC DENSITY MEMBERSHIP FUNCTIONS

traffic_density['low'] = fuzz.trapmf(
    traffic_density.universe,
    [0, 0, 8, 15]
)

traffic_density['medium'] = fuzz.trimf(
    traffic_density.universe,
    [10, 20, 30]
)

traffic_density['high'] = fuzz.trapmf(
    traffic_density.universe,
    [25, 35, 50, 50]
)


# 3. WAITING TIME MEMBERSHIP FUNCTIONS

waiting_time['short'] = fuzz.trapmf(
    waiting_time.universe,
    [0, 0, 15, 30]
)

waiting_time['moderate'] = fuzz.trimf(
    waiting_time.universe,
    [20, 50, 80]
)

waiting_time['long'] = fuzz.trapmf(
    waiting_time.universe,
    [70, 90, 120, 120]
)


# 4. GREEN DURATION MEMBERSHIP FUNCTIONS

green_duration['short'] = fuzz.trimf(
    green_duration.universe,
    [10, 10, 30]
)

green_duration['medium'] = fuzz.trimf(
    green_duration.universe,
    [30, 45, 60]
)

green_duration['long'] = fuzz.trimf(
    green_duration.universe,
    [60, 75, 90]
)


# 5. DEFINE FUZZY RULES

rule1 = ctrl.Rule(
    traffic_density['low'] & waiting_time['short'],
    green_duration['short']
)

rule2 = ctrl.Rule(
    traffic_density['low'] & waiting_time['moderate'],
    green_duration['short']
)

rule3 = ctrl.Rule(
    traffic_density['low'] & waiting_time['long'],
    green_duration['medium']
)

rule4 = ctrl.Rule(
    traffic_density['medium'] & waiting_time['short'],
    green_duration['medium']
)

rule5 = ctrl.Rule(
    traffic_density['medium'] & waiting_time['moderate'],
    green_duration['medium']
)

rule6 = ctrl.Rule(
    traffic_density['medium'] & waiting_time['long'],
    green_duration['long']
)

rule7 = ctrl.Rule(
    traffic_density['high'] & waiting_time['short'],
    green_duration['medium']
)

rule8 = ctrl.Rule(
    traffic_density['high'] & waiting_time['moderate'],
    green_duration['long']
)

rule9 = ctrl.Rule(
    traffic_density['high'] & waiting_time['long'],
    green_duration['long']
)


# 6. CREATE FUZZY CONTROL SYSTEM

traffic_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
])


# 7. CREATE SIMULATION

traffic_sim = ctrl.ControlSystemSimulation(traffic_ctrl)


# 8. DEFINE TEST CASES

test_cases = [

    {
        "name": "Low Traffic",
        "density": 5,
        "waiting": 10
    },

    {
        "name": "Moderate Traffic",
        "density": 20,
        "waiting": 50
    },

    {
        "name": "Heavy Traffic",
        "density": 40,
        "waiting": 90
    },

    {
        "name": "High Traffic and Long Wait",
        "density": 45,
        "waiting": 110
    }

]


# 9. PROCESS EACH TEST CASE

for case in test_cases:

    traffic_sim.input['traffic_density'] = case['density']

    traffic_sim.input['waiting_time'] = case['waiting']

    traffic_sim.compute()

    duration = traffic_sim.output['green_duration']

    print("\nScenario:", case['name'])

    print("Traffic Density:", case['density'])

    print("Waiting Time:", case['waiting'])

    print("Recommended Green Duration:",
          round(duration, 2), "seconds")


# 10. CUSTOM INPUT

density_input = 35

waiting_input = 100

traffic_sim.input['traffic_density'] = density_input

traffic_sim.input['waiting_time'] = waiting_input

traffic_sim.compute()

recommended_duration = traffic_sim.output['green_duration']

print("\nCUSTOM TRAFFIC SCENARIO")

print("Traffic Density:", density_input, "vehicles/min")

print("Waiting Time:", waiting_input, "seconds")

print("Recommended Green Duration:",
      round(recommended_duration, 2), "seconds")