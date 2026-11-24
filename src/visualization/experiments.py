import ctypes
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

BASE_PARAMS = {
    "x0": 0.0,
    "y0": 0.0,
    "angle": 45.0,
    "dry_mass": 500.0,
    "thrust": 20000.0,
    "burn_rate": 50.0,
    "fuel": 500.0,
    "atmosphere_mode": 2,
}

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get dll file path
dll_path = os.path.join(current_dir, '..', 'simulation', 'simulation.dll')
# Load compiled C library into Python's memory. To be able to ue that.
lib = ctypes.CDLL(dll_path)

# Create a shorthand for a C-style pointer to a double
ptr_double = ctypes.POINTER(ctypes.c_double)
# Specify input types (7 doubles) and output types (11 double pointers) for the C function
lib.run_simulation.argtypes = [
    ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int,

    ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double)
]

# Specify the function's return type as a C integer
lib.run_simulation.restype = ctypes.c_int

print(" --- Missile Trajectory Engine --- ")

# Promt the user to input simulation parametres and parse them as float
try:
    x_inp = float(input("Enter initial x coordinate (m): "))
    y_inp = float(input("Enter initial y coordinate (m): "))
    angle_inp = float(input("Enter angle (degree): "))
    dry_m_inp = float(input("Enter dry mass (kg): "))
    thrust_inp = float(input("Enter thrust (N): "))
    burn_rate_inp = float(input("Enter burn rate (kg/s): "))
    fuel_inp = float(input("Enter fuel (kg): "))
    mode_inp = int(input("Enter atmosphere mode (0 - no drag, 1 - const density, 2 - variable density): "))
except:
    print("Error. Please enter valid values.")
    sys.exit(1)

t_ptr1 = ptr_double()
x_ptr1 = ptr_double()
y_ptr1 = ptr_double()
vx_ptr1 = ptr_double()
vy_ptr1 = ptr_double()
ax_ptr1 = ptr_double()
ay_ptr1 = ptr_double()
Ep_ptr1 = ptr_double()
Ek_ptr1 = ptr_double()
m_ptr1 = ptr_double()
fuel_ptr1 = ptr_double()

experiment1 = lib.run_simulation(
    x_inp, y_inp, angle_inp, dry_m_inp, thrust_inp, burn_rate_inp, fuel_inp, mode_inp, 

    ctypes.byref(t_ptr1), ctypes.byref(x_ptr1), ctypes.byref(y_ptr1),
    ctypes.byref(vx_ptr1), ctypes.byref(vy_ptr1), ctypes.byref(ax_ptr1),
    ctypes.byref(ay_ptr1), ctypes.byref(Ep_ptr1), ctypes.byref(Ek_ptr1),
    ctypes.byref(m_ptr1), ctypes.byref(fuel_ptr1)
)

t_ptr2 = ptr_double()
x_ptr2 = ptr_double()
y_ptr2 = ptr_double()
vx_ptr2 = ptr_double()
vy_ptr2 = ptr_double()
ax_ptr2 = ptr_double()
ay_ptr2 = ptr_double()
Ep_ptr2 = ptr_double()
Ek_ptr2 = ptr_double()
m_ptr2 = ptr_double()
fuel_ptr2 = ptr_double()

basic = lib.run_simulation(
    BASE_PARAMS["x0"], BASE_PARAMS["y0"], BASE_PARAMS["angle"], BASE_PARAMS["dry_mass"], BASE_PARAMS["thrust"], BASE_PARAMS["burn_rate"], BASE_PARAMS["fuel"], BASE_PARAMS["atmosphere_mode"],
    ctypes.byref(t_ptr2), ctypes.byref(x_ptr2), ctypes.byref(y_ptr2),
    ctypes.byref(vx_ptr2), ctypes.byref(vy_ptr2), ctypes.byref(ax_ptr2),
    ctypes.byref(ay_ptr2), ctypes.byref(Ep_ptr2), ctypes.byref(Ek_ptr2),
    ctypes.byref(m_ptr2), ctypes.byref(fuel_ptr2)
)

if experiment1 <= 0:
    print("Error")
else:
    print("Success")

    t1 = np.ctypeslib.as_array(t_ptr1, shape=(experiment1,))
    x1 = np.ctypeslib.as_array(x_ptr1, shape=(experiment1,))
    y1 = np.ctypeslib.as_array(y_ptr1, shape=(experiment1,))
    vx1 = np.ctypeslib.as_array(vx_ptr1, shape=(experiment1,))
    vy1 = np.ctypeslib.as_array(vy_ptr1, shape=(experiment1,))
    ax1 = np.ctypeslib.as_array(ax_ptr1, shape=(experiment1,))
    ay1 = np.ctypeslib.as_array(ay_ptr1, shape=(experiment1,))
    Ep1 = np.ctypeslib.as_array(Ep_ptr1, shape=(experiment1,))
    Ek1 = np.ctypeslib.as_array(Ek_ptr1, shape=(experiment1,))
    m1 = np.ctypeslib.as_array(m_ptr1, shape=(experiment1,))
    fuel1 = np.ctypeslib.as_array(fuel_ptr1, shape=(experiment1,))

    t2 = np.ctypeslib.as_array(t_ptr2, shape=(basic,))
    x2 = np.ctypeslib.as_array(x_ptr2, shape=(basic,))
    y2 = np.ctypeslib.as_array(y_ptr2, shape=(basic,))
    vx2 = np.ctypeslib.as_array(vx_ptr2, shape=(basic,))
    vy2 = np.ctypeslib.as_array(vy_ptr2, shape=(basic,))
    ax2 = np.ctypeslib.as_array(ax_ptr2, shape=(basic,))
    ay2 = np.ctypeslib.as_array(ay_ptr2, shape=(basic,))
    Ep2 = np.ctypeslib.as_array(Ep_ptr2, shape=(basic,))
    Ek2 = np.ctypeslib.as_array(Ek_ptr2, shape=(basic,))
    m2= np.ctypeslib.as_array(m_ptr2, shape=(basic,))
    fuel2 = np.ctypeslib.as_array(fuel_ptr2, shape=(basic,))

    target_points = 300
    k1 = max(1, len(x1) // target_points)
    k2 = max(1, len(x2) // target_points)

    # Stylization and creating first window
    plt.style.use("dark_background")
    fig, axis = plt.subplots(facecolor="black")
    axis.set_xlim([min(min(x1), min(x2)), max(max(x1), max(x2))])
    axis.set_ylim([min(min(y1), min(y2)), max(max(y1), max(y2))])
    axis.plot(x2[::k2], y2[::k2], color="#b8ceda", linewidth=2, label="Basic Trajectory", zorder=1)
    axis.plot(x1[::k1], y1[::k1], color='#3e83ab', linewidth=2, label='Experiment trajetory', zorder=2)
    axis.grid(linestyle='dashed', color='#64748b')
    axis.set_facecolor("#0B132B")
    axis.set_title("Ballistic Missile Trajectory", fontsize=16, color='#3e83ab')
    axis.set_xlabel("X Distance (m)", fontsize=12, color="gray")
    axis.set_ylabel("Y Altitude (m)", fontsize=12, color="gray")
    axis.spines['bottom'].set_color('#1e293b')
    axis.spines['bottom'].set_linewidth(1.5)
    axis.spines['top'].set_color('#1e293b')
    axis.spines['top'].set_linewidth(1.5)
    axis.spines['left'].set_color('#1e293b')
    axis.spines['left'].set_linewidth(1.5)
    axis.spines['right'].set_color('#1e293b')
    axis.spines['right'].set_linewidth(1.5)
    speed_arr1 = np.sqrt(vx1 * vx1 + vy1 * vy1)
    speed_arr2 = np.sqrt(vx2 * vx2 + vy2 * vy2)
    curr_speed1 = speed_arr1[-1]
    curr_speed2 = speed_arr2[-1]

    telemetry_box = axis.text(
        0.01, 0.98,
        f"PARAM   | EXP         | BASIC\n"
        f"TIME    | {t1[-1]:8.2f} s  | {t2[-1]:8.2f} s\n"
        f"X       | {x1[-1]:8.2f} m  | {x2[-1]:8.2f} m\n"
        f"Y       | {y1[-1]:8.2f} m  | {y2[-1]:8.2f} m\n"
        f"V       | {curr_speed1:7.2f} m/s | {curr_speed2:7.2f} m/s\n"
        f"VX      | {vx1[-1]:7.2f} m/s | {vx2[-1]:7.2f} m/s\n"
        f"VY      | {vy1[-1]:7.2f} m/s | {vy2[-1]:7.2f} m/s\n"
        f"AX      | {ax1[-1]:6.2f} m/s² | {ax2[-1]:6.2f} m/s²\n"
        f"AY      | {ay1[-1]:6.2f} m/s² | {ay2[-1]:6.2f} m/s²\n"
        f"Ek      | {Ek1[-1]:10.0f} J| {Ek2[-1]:10.0f} J\n"
        f"M       | {m1[-1]:8.2f} kg | {m2[-1]:8.2f} kg\n"
        f"FUEL    | {fuel1[-1]:8.2f} kg | {fuel2[-1]:8.2f} kg",
        transform=axis.transAxes, fontsize=9,
        family='monospace', color='#f8fafc',
        verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#0f172a", edgecolor="#334155", alpha=0.85)
    )

    axis.legend()

    # Stylization and creating second window
    fig2, axs = plt.subplots(2, 2, figsize=(12, 8), facecolor="black")
    fig2.suptitle("Graphics", color='#3e83ab')

    axs[0, 0].plot(t1, speed_arr1, color='cyan', linewidth=2, label="Exp V")
    axs[0, 0].plot(t2, speed_arr2, color='#c8ffff', linewidth=1.8, label="Basic V")
    axs[0, 0].set_title("Velocity over time", color="white")

    axs[0, 1].plot(t1, y1, color='lime', linewidth=2, label="Exp Y")
    axs[0, 1].plot(t2, y2, color='#ccffcc', linewidth=1.8, label="Basic Y")
    axs[0, 1].set_title("Altitude over time", color="white")

    axs[1, 0].plot(t1, ax1, color='orange', label='Exp AX')
    axs[1, 0].plot(t1, ay1, color='red', label='Exp AY')
    axs[1, 0].plot(t2, ax2, color='#ffe4b8', label='Basic AX')
    axs[1, 0].plot(t2, ay2, color='#ffcccc', label='Basic AY')
    axs[1, 0].set_title("Acceleration over time", color="white")

    total_E1 = Ek1 + Ep1
    total_E2 = Ek2 + Ep2
    axs[1, 1].plot(t1, Ek1, color="magenta", linewidth=2, label="Exp Ek")
    axs[1, 1].plot(t1, Ep1, color="blue", linewidth=2, label="Exp Ep")
    axs[1, 1].plot(t1, total_E1, color="yellow", linewidth=2, label="Exp E")
    axs[1, 1].plot(t2, Ek2, color="#ffccff", linewidth=1.5, label="Basic Ek")
    axs[1, 1].plot(t2, Ep2, color="#c2d6ff", linewidth=1.5, label="Basic Ep")
    axs[1, 1].plot(t2, total_E2, color="#ffffcc", linewidth=1.5, label="Basic E")
    axs[1, 1].set_title("Energy over time", color="white")

    for a in axs.flat:
        a.set_facecolor("#0B132B")
        a.grid(color='gray')
        a.tick_params(colors='white')
        for spine in a.spines.values():
            spine.set_color("#1e293b")
            spine.set_linewidth(1.5)
        a.set_xlabel("Time (s)", color='gray')
        a.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='white', fontsize=8)

    axs[1, 0].legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='white')
    axs[1, 1].legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='white')

    plt.show()

# Cleaning memory
print("Cleaning up memory...")
lib.free_memory(t_ptr1)
lib.free_memory(x_ptr1)
lib.free_memory(y_ptr1)
lib.free_memory(vx_ptr1)
lib.free_memory(vy_ptr1)
lib.free_memory(ax_ptr1)
lib.free_memory(ay_ptr1)
lib.free_memory(Ep_ptr1)
lib.free_memory(Ek_ptr1)
lib.free_memory(m_ptr1)
lib.free_memory(fuel_ptr1)
lib.free_memory(t_ptr2)
lib.free_memory(x_ptr2)
lib.free_memory(y_ptr2)
lib.free_memory(vx_ptr2)
lib.free_memory(vy_ptr2)
lib.free_memory(ax_ptr2)
lib.free_memory(ay_ptr2)
lib.free_memory(Ep_ptr2)
lib.free_memory(Ek_ptr2)
lib.free_memory(m_ptr2)
lib.free_memory(fuel_ptr2)
print("Memory cleaned. Done!")
