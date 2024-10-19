import Generator_DFN_2D
import numpy as np
"""
Data z SKB report:
Intenzita: p_32 celková: 0.60 až 2.60 
Exponent škálování velikosti puklin k_r: 2.55 až 2.79 
Nejmenší velikost pukliny (tj. poloměr vrtu): r_min: 0.038 
Nejvetší velikost pukliny: r_max = 169
"""
r_min = 0.038
r_max = 0.5
file_path = "C:/Plocha/vysledky_dfn.txt"
p_32_values = np.linspace(0.60, 2.60, 10)  # 10 hodnot od 0.60 do 2.60
k_r_values = np.linspace(2.55, 2.79, 10)  # 10 hodnot od 2.55 do 2.79

with open(file_path, "w") as file:
    for i in range(10):
        p_32 = p_32_values[i]
        k_r = k_r_values[i]
        file.write("--------------------------------------------------------\n")
        file.write(f"Test Case {i + 1}: p_32 = {p_32:.2f}, k_r = {k_r:.2f}\n")
        mean_size, amount_of_fractures = Generator_DFN_2D.plot_dfn(k_r, p_32, r_min, r_max)
        file.write(f"Mean size of fractures: {mean_size:.4f}\n")
        file.write(f"Number of fractures: {amount_of_fractures}\n")

print("Test cases have been written to the file.")
