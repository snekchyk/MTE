import ctypes
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(current_dir, '..', 'simulation', 'simulation.dll')
lib = ctypes.CDLL(dll_path)

ptr_double = ctypes.POINTER(ctypes.c_double)

lib.run_simulation.argtypes = [
    ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int,

    ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double), ctypes.POINTER(ptr_double)
]
lib.run_simulation.restype = ctypes.c_int


t_ptr = ptr_double()
x_ptr = ptr_double()
y_ptr = ptr_double()
vx_ptr = ptr_double()
vy_ptr = ptr_double()
ax_ptr = ptr_double()
ay_ptr = ptr_double()
Ep_ptr = ptr_double()
Ek_ptr = ptr_double()
m_ptr = ptr_double()
fuel_ptr = ptr_double()

d = []

for i in range(0, 90):
    ptrs = lib.run_simulation(
        0, 0, i, 250, 20000, 50, 500, 2, 

        ctypes.byref(t_ptr), ctypes.byref(x_ptr), ctypes.byref(y_ptr),
        ctypes.byref(vx_ptr), ctypes.byref(vy_ptr), ctypes.byref(ax_ptr),
        ctypes.byref(ay_ptr), ctypes.byref(Ep_ptr), ctypes.byref(Ek_ptr),
        ctypes.byref(m_ptr), ctypes.byref(fuel_ptr)
    )
    if ptrs > 0 and x_ptr:
        dist = float(x_ptr[ptrs - 1])
    else: 
        dist = 0.0
    
    
    d.append(dist)

best_distance = 0
best_angle = 0
for i in range(90):
    if d[i] > best_distance:
        best_distance = d[i]
        best_angle = i

print(best_distance)
print(best_angle)

print(f"Optimal angle: {best_angle}, distance: {best_distance}")

with open("distances.txt", "w", encoding="utf-8") as f:
    for angle, dist in enumerate(d):
        f.write(f"{angle} – {dist}\n")

