# import modules
import numpy as np
import matplotlib.pyplot as plt
import itertools
from scipy.optimize import curve_fit

# Raw_data class
class Raw_data:
    """Stores raw data taken from the lab measurements."""
    # calibration weights
    weights_g = np.array([
        0, 331.7, 1331.7, 2331.7, 3331.7, 4331.7, 5331.7, 5331.7, 5331.7, 4331.7, 3331.7, 2331.7,
        1331.7, 331.7, 0
    ])

    # motor settings for investigating side force
    motor_settings = np.array([1, 2, 3, 3, 4, 5 , 6, 7])

    # yaw angles for side load investigation
    yaw_angles_3_kg = np.array([5, 10, 15, 2.5, 7.5, 12.5])
    yaw_angles_5_kg = np.array([2.5, 5, 7.5, 10, 12.5, 15])

    # longitudinal creep data
    longitudinal_creep = {
        "delta = 0": {
            "W = 3 kg": {
                "T = 0 kg": {
                    "revolutions": 1.5, "x_1": 4.24, "x_max": 0, "x_2": 4.24
                },
                "T = 1 kg": {
                    "x_1": 3.88, "x_max": 0.43, "x_2": 3.52
                },
                "T = 2 kg": {
                    "x_1": 3.52, "x_max": 0.28, "x_2": 2.93
                },
                "T = 3 kg": {
                    "x_1": 4.48, "x_max": 0, "x_2": 3.78
                }
            },
            "W = 5 kg": {
                "T = 0 kg": {
                    "revolutions": 1.33333, "x_1": 3.99, "x_max": 0, "x_2": 3.95
                },
                "T = 1 kg": {
                    "x_1": 4.77, "x_max": 1.37, "x_2": 4.51
                },
                "T = 2 kg": {
                    "x_1": 4.51, "x_max": 1.2, "x_2": 4.1
                },
                "T = 3 kg": {
                    "x_1": 4.03, "x_max": 0.83, "x_2": 3.48
                }
            }
        },
        "delta = 5": {
            "W = 3 kg": {
                "T = 0 kg": {
                    "revolutions": 1.5, "x_1": 4.48, "x_max": 0.09, "x_2": 4.44
                },
                "T = 1 kg": {
                    "x_1": 4.41, "x_max": 0, "x_2": 3.8
                },
                "T = 2 kg": {
                    "x_1": 3.6, "x_max": 0, "x_2": 2.98
                },
                "T = 3 kg": {
                    "x_1": 3.51, "x_max": 0, "x_2": 2.63
                }
            }

        },
        "delta = 15": {
            "W = 3 kg": {
                "T = 0 kg": {
                    "revolutions": 1.5, "x_1": 4.76, "x_max": 0.13, "x_2": 4.73
                },
                "T = 1 kg": {
                    "x_1": 4.59, "x_max": 0, "x_2": 3.6
                },
                "T = 2 kg": {
                    "x_1": 4.58, "x_max": 0, "x_2": 3.09
                },
                "T = 3 kg": {
                    "x_1": 4.18, "x_max": 0, "x_2": 2.38
                }
            }
        }
    }

# Inputs class
class Inputs:
    """Stores input parameters and default values."""
    # file names dictionary
    file_names = {
        "calibration": "../trad3 and df431/calibration.csv",
        "effect_of_speed": "../trad3 and df431/4.2 Effective speed on side force.csv",
        "effect_of_normal_load_3_kg": "../trad3 and df431/4.3 Effect of normal load on steady state side force.csv",
        "effect_of_normal_load_5_kg": "../trad3 and df431/4.3 Effect of normal load on steady state side force 5kg.csv",
        #"lateral_and_longitudinal_creep_delta_5": "../trad3 and df431/5.3 combined lateral and longitudinal creep - delta 5 re-run.csv",
        "lateral_and_longitudinal_creep_delta_5": "../trad3 and df431/5.3 combined lateral and longitudinal creep - delta 5.csv",
        "lateral_and_longitudinal_creep_delta_15": "../trad3 and df431/5.3 combined lateral and longitudinal creep - delta 15.csv"
    }

    # default length of arrays
    N = 100

    # default plotting parameters
    figsize = (9, 4)
    alpha = 0.4

    # experiment values
    metres_per_volt = 1 / 12            # m / V
    drum_diameter = 74 / 1000           # m
    drum_radius = drum_diameter / 2

    # constants
    g = 9.80665

# Results class
class Results:
    """Stores results and reusable analysis features."""
    def __init__(self, m_1, c_1, m_2, c_2):
        """Creates an instance of the Results class."""
        # store input_variables
        self.m_1 = m_1
        self.c_1 = c_1
        self.m_2 = m_2
        self.c_2 = c_2
    
    def forwards_calibrate(self, x):
        """Returns the forwards-calibrated force reading for a given transducer reading."""
        # invert linear regression
        return (x - self.c_1) / self.m_1
    
    def backwards_calibrate(self, x):
        """Returns the backwards-calibrated force reading for a given transducer reading."""
        # invert linear regression
        return (x - self.c_2) / self.m_2

    # effect_of_speed function
    def effect_of_speed(self):

        # read data
        data = np.genfromtxt(Inputs.file_names["effect_of_speed"], delimiter = ",")
        data = data.transpose()

        # create plot
        fig, ax = plt.subplots(figsize = Inputs.figsize)

        # get colours iterater
        colours = itertools.cycle(plt.cm.tab10.colors)

        # create empty list of mean values
        mean_values = []

        # loop for each motor setting
        for index, setting in enumerate(Raw_data.motor_settings):

            # for duplicate entry with motor setting 3
            if index == 2:

                # do not plot
                continue

            # get colour
            colour = next(colours)

            # mask zeros padded at end of data after recording had ended
            mask = (data[2 * index + 1] != 0)
            x_masked = data[2 * index][mask]
            x_masked -= x_masked[0]
            y_masked = data[2 * index + 1][mask]

            # get a second mask clipping the 10th percentile x-values off from either end
            percentile = 0.1
            x_min = np.min(x_masked)
            x_max = np.max(x_masked)
            mask = (
                (x_masked > x_min + percentile * (x_max - x_min))
                & (x_masked < x_max - 3 * percentile * (x_max - x_min))
            )

            # calculate mean value
            mean_value = np.mean(y_masked[mask])
            mean_values.append(mean_value)

            # plot data
            ax.plot(
                x_masked, y_masked, color = colour,
                label = f"Motor setting {setting}: mean = {mean_value:.3g}"
            )

        # configure plot
        ax.grid()
        ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        ax.set_xlabel("Displacement Transducer Reading (V)")
        ax.set_ylabel('Side Force Transducer Reading (V)')
        ax.set_title("Effect of Speed on Side Force")
        plt.tight_layout()

        # create bar chart
        fig, ax = plt.subplots(figsize = Inputs.figsize)

        # populate bar chart
        mean_values_N = self.forwards_calibrate(mean_values)
        colours = plt.rcParams['axes.prop_cycle'].by_key()['color'][:len(mean_values)]
        ax.bar(np.arange(len(mean_values)) + 1, mean_values_N, color = colours)

        # configure plot
        ax.grid(alpha = Inputs.alpha)
        ax.set_xlabel("Motor Setting")
        ax.set_ylabel('Mean Side Force (N)')
        ax.set_title("Effect of Speed on Side Force")
        plt.tight_layout()

    # effect_of_normal_load function
    def effect_of_normal_load(self, weight):

        # read data
        data = np.genfromtxt(Inputs.file_names[f"effect_of_normal_load_{weight}"], delimiter = ",")
        data = data.transpose()

        # create plot
        fig, ax = plt.subplots(figsize = Inputs.figsize)

        # sort yaw angles in ascending order
        yaw_angles = getattr(Raw_data, f"yaw_angles_{weight}")
        sorted_indices = np.argsort(yaw_angles)
        sorted_yaw_angles = yaw_angles[sorted_indices]

        # create empty list of mean values to populate
        mean_values = np.zeros(len(yaw_angles))

        # loop for each yaw angle
        for sorted_index, yaw_angle in enumerate(sorted_yaw_angles):

            # get range of values
            index = sorted_indices[sorted_index]
            #mean_values[sorted_index] = 0.5 * (np.max(data[2 * index + 1]) - np.min(data[2 * index + 1]))
            mean_values[sorted_index] = np.max(data[2 * index + 1])

            # plot data
            ax.plot(
                data[2 * index], data[2 * index + 1],
                label = f"Yaw angle = {yaw_angle}°, Mean value = {mean_values[sorted_index]:.3g} V"
            )

        # configure plot
        ax.grid()
        ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        ax.set_xlabel("Displacement Transducer Reading (V)")
        ax.set_ylabel('Side Force Transducer Reading (V)')
        ax.set_title(f"Effect of Normal Load on Steady State Side Force {weight.replace('_', ' ')}")
        plt.tight_layout()

        # yaw angle-side force plot does not yet exist
        if not hasattr(self, "fig"):

            # create plot
            self.fig, self.ax = plt.subplots(figsize = Inputs.figsize)

        # calibrate transducer readings as forwards value
        mean_values_N = self.forwards_calibrate(mean_values)

        # find lateral creep values
        lateral_creeps = np.tan(deg_to_rad(sorted_yaw_angles))

        # plot mean side force against lateral creep
        self.ax.plot(
            lateral_creeps, mean_values_N, label = f"Normal load = {weight.replace('_', ' ')}"
        )

        # linear regression
        m, c = np.polyfit(np.insert(lateral_creeps, 0, 0), np.insert(mean_values_N, 0, 0), 1)
        xx = np.linspace(np.min(lateral_creeps), np.max(lateral_creeps), Inputs.N)

        # plot line of best fit
        self.ax.plot(
            xx, m * xx + c, label = f"Line of best fit {weight}"
        )

        # configure plot
        self.ax.grid(True)
        self.ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        self.ax.set_xlabel("Lateral Creep")
        self.ax.set_ylabel("Mean Side Force (N)")
        self.ax.set_title("Effect of Normal Load on Side Force")
        plt.tight_layout()

    # no_load_creep function
    def no_load_creep(self):

        # read data
        data = Raw_data.longitudinal_creep["delta = 0"]["W = 3 kg"]["T = 0 kg"]

        # calculate rolling radius
        self.rolling_radius = (
            Inputs.metres_per_volt * (data["x_1"] - data["x_max"] + data["x_2"])
            / (data["revolutions"] * 2 * np.pi)
        )
        print(f"self.rolling_radius: {self.rolling_radius}")

    # applied_torque_creep function
    def applied_torque_creep(self, weight):

        # read data
        data = Raw_data.longitudinal_creep["delta = 0"][f"W = {weight.replace('_', ' ')}"]

        # create empty lists of data
        self.weights = []
        creep_coefficients = []

        # loop for each applied torque value
        for key, value in data.items():

            # store extracted torque value
            self.weights.append(
                int(key.replace("T = ", "").replace(" kg", ""))
            )

            # store displacement variables separately for convenience
            x_1 = data[key]["x_1"]
            x_max = data[key]["x_max"]
            x_2 = data[key]["x_2"]

            # calculate and store creep coefficient
            creep_coefficients.append(
                (x_2 - x_1) / (x_max - x_1 + x_max - x_2)
            )

        # convert weights to tyre longitudinal forces
        self.longitudinal_loads = np.array(self.weights) * Inputs.g * Inputs.drum_radius / self.rolling_radius

        # plot does not yet exist
        if not hasattr(self, "fig"):

            # create plot
            self.fig, self.ax = plt.subplots(figsize = Inputs.figsize)
        
        # plot data
        self.ax.plot(self.longitudinal_loads, creep_coefficients, label = rf"W = {weight.replace('_', ' ')}, $\delta$ = 0")
        
        # configure plot
        self.ax.grid(True)
        self.ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        self.ax.set_xlabel("Longitudinal Force (N)")
        self.ax.set_ylabel("Longitudinal Creep")
        self.ax.set_title("Creep with an Applied Torque")
        plt.tight_layout()

    # lateral_and_longitudinal_creep function
    def lateral_and_longitudinal_creep(self, yaw_angle):

        # read data from spreadsheet
        data = Raw_data.longitudinal_creep[f"delta = {yaw_angle}"][f"W = 3 kg"]

        # create empty list for creep coefficients
        creep_coefficients = []

        # loop for each applied torque value
        for key, value in data.items():

            # store displacement variables separately for convenience
            x_1 = data[key]["x_1"]
            x_max = data[key]["x_max"]
            x_2 = data[key]["x_2"]

            # calculate and store creep coefficient
            creep_coefficients.append(
                (x_2 - x_1) / (x_max - x_1 + x_max - x_2)
            )
            data[key]["longitudinal_creep"] = (x_2 - x_1) / (x_max - x_1 + x_max - x_2)

        # plot does not yet exist
        if not hasattr(self, "fig"):

            # create plot
            self.fig, self.ax = plt.subplots(figsize = Inputs.figsize)

        # plot data
        self.ax.plot(self.longitudinal_loads, creep_coefficients, label = rf"W = 3 kg, $\delta$ = {yaw_angle}°")

        # configure plot
        self.ax.grid(True)
        self.ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        self.ax.set_xlabel('Force Applied (N)')
        self.ax.set_ylabel('Longitudinal Creep')
        self.ax.set_title("Combined Lateral and Longitudinal Creep")
        plt.tight_layout()

        # read data from transducers
        data = np.genfromtxt(Inputs.file_names[f"lateral_and_longitudinal_creep_delta_{yaw_angle}"], delimiter = ",")
        data = data.transpose()

        print(f"data: {data}")

        # create new plot
        fig, ax = plt.subplots(figsize = Inputs.figsize)

        mean_values = np.zeros(len(self.longitudinal_loads))

        # loop for each applied longitudinal load value
        for index, weight in enumerate(self.weights):
        
            # mask zeros padded at end of data after recording had ended
            mask = (data[2 * index + 1] != 0)
            x_masked = data[2 * index][mask]
            y_masked = data[2 * index + 1][mask]

            # plot masked data
            ax.plot(x_masked, y_masked, label = rf"W = {weight} kg, $\delta$ = {yaw_angle}°")

            # get mean values of lateral transducer readings based on percentile data
            #percentile = 0.05
            mean_values[index] = np.max(data[2 * index + 1])

        ax.grid(True)
        ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        ax.set_xlabel('Longitudinal Transducer Reading (V)')
        ax.set_ylabel('Side Force Transducer Reading (V)')
        ax.set_title("Combined Lateral and Longitudinal Creep")
        plt.tight_layout()

        # get forwards-calibrated lateral force values
        mean_values_N = self.forwards_calibrate(mean_values)

        # plot does not yet exist
        if not hasattr(self, "fig2"):

            # create plot

            self.fig2, self.ax2 = plt.subplots(figsize = Inputs.figsize)

        self.ax2.plot(self.longitudinal_loads, mean_values_N, label = rf"$\delta$ = {yaw_angle}")

        # configure plot
        self.ax2.grid(True)
        self.ax2.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
        self.ax2.set_xlabel('Longitudinal Force (N)')
        self.ax2.set_ylabel('Lateral Force (N)')
        self.ax2.set_title("Combined Lateral and Longitudinal Creep")
        plt.tight_layout()


# main function
def main():

    # run functions corresponding to each report section
    results = calibration()
    results.effect_of_speed()
    results.effect_of_normal_load("3_kg")
    results.effect_of_normal_load("5_kg")
    delattr(results, "fig")
    results.no_load_creep()
    results.applied_torque_creep("3_kg")
    results.applied_torque_creep("5_kg")
    delattr(results, "fig")
    results.lateral_and_longitudinal_creep(5)
    results.lateral_and_longitudinal_creep(15)

# calibration function
def calibration():

    # read data
    data = np.genfromtxt("../trad3 and df431/calibration.csv", delimiter = ",")
    data = data.reshape(-1, 2).transpose()

    # convert weights to N
    weights_N = Raw_data.weights_g * Inputs.g / 1000

    # get indices of maximum weight value
    ascent_index = np.argmax(weights_N)
    descent_index = np.argmax(weights_N[::-1])

    # get line of best fit for monotonically increasing and decreasing weight values
    m_1, c_1 = np.polyfit(weights_N[:ascent_index + 1], data[1][:ascent_index + 1], 1)
    m_2, c_2 = np.polyfit(weights_N[-1 - descent_index:], data[1][-1 - descent_index:], 1)

    # store best fits as separate arrays
    xx = np.linspace(np.min(weights_N), np.max(weights_N), Inputs.N)
    yy_1 = m_1 * xx + c_1
    yy_2 = m_2 * xx + c_2

    # quantify hysteresis
    mean_hysteresis = np.mean(np.abs(yy_1 - yy_2))
    mean_hysteresis_percent = 100 * mean_hysteresis / (np.max(data[1]) - np.min(data[1]))

    # create plot
    fig, ax = plt.subplots(figsize = Inputs.figsize)

    # plot raw data and lines of best fit
    ax.plot(
        weights_N, data[1], marker = '.', markersize = 6, color = 'C0',
        label = "Measurements"
    )
    ax.plot(
        xx, yy_1, color = 'C1', label = f"Line of best fit: m = {m_1:.3g}, c = {c_1:.3g}"
    )
    ax.plot(
        xx, yy_2, color = 'C2', label = f"Line of best fit: m = {m_2:.3g}, c = {c_2:.3g}"
    )

    # display mean hysteresis separation on legend
    ax.plot([], [], linestyle = '', label = f"Hysteresis = {mean_hysteresis:.3g} V")
    ax.plot([], [], linestyle = '', label = f"Hysteresis (%) = {mean_hysteresis_percent:.3g} %")

    # configure plot
    ax.grid()
    ax.legend(loc = 'center left', bbox_to_anchor = (1, 0.5))
    ax.set_xlabel('Force Applied (N)')
    ax.set_ylabel('Side Force Transducer Reading (V)')
    ax.set_title("Load Cell Calibration Results")
    plt.tight_layout()

    # store calibration coefficients
    return Results(m_1, c_1, m_2, c_2)

# deg_to_rad function
def deg_to_rad(x):

    # convert from degrees to radians and return
    return x * np.pi / 180

# on script execution
if __name__ == "__main__":

    # run main
    main()

    # show all plots
    plt.show()
