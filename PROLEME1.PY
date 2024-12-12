import tkinter as tk
from tkinter import messagebox
from gurobipy import Model, GRB

# Function to solve the optimization problem
def solve_optimization():
    try:
        # Get user inputs
        budget = float(entry_budget.get())
        min_female_exposure = float(entry_min_female_exposure.get())

        # Retrieve coefficients
        exposure_coeffs = [
            float(entry_exposure_local.get()),
            float(entry_exposure_satellite.get()),
            float(entry_exposure_radio.get()),
            float(entry_exposure_newspaper.get())
        ]

        cost_coeffs = [
            float(entry_cost_local.get()),
            float(entry_cost_satellite.get()),
            float(entry_cost_radio.get()),
            float(entry_cost_newspaper.get())
        ]

        female_exposure_coeffs = [
            float(entry_female_local.get()),
            float(entry_female_satellite.get()),
            float(entry_female_radio.get()),
            float(entry_female_newspaper.get())
        ]

        # Create the model
        model = Model("MediaBudget")

        # Decision variables
        x1 = model.addVar(vtype=GRB.INTEGER, name="x1")  # Television local
        x2 = model.addVar(vtype=GRB.INTEGER, name="x2")  # Television satellite
        x3 = model.addVar(vtype=GRB.INTEGER, name="x3")  # Radio
        x4 = model.addVar(vtype=GRB.INTEGER, name="x4")  # Newspapers

        # Objective: Maximize total exposure
        model.setObjective(
            exposure_coeffs[0] * x1 + exposure_coeffs[1] * x2 + exposure_coeffs[2] * x3 + exposure_coeffs[3] * x4, GRB.MAXIMIZE
        )

        # Constraints
        model.addConstr(
            cost_coeffs[0] * x1 + cost_coeffs[1] * x2 + cost_coeffs[2] * x3 + cost_coeffs[3] * x4 <= budget, "Budget"
        )
        model.addConstr(
            female_exposure_coeffs[0] * x1 + female_exposure_coeffs[1] * x2 + female_exposure_coeffs[2] * x3 + female_exposure_coeffs[3] * x4 >= min_female_exposure, "FemaleExposure"
        )
        model.addConstr(x1 >= 3, "MinLocalTV")
        model.addConstr(x2 >= 2, "MinSatelliteTV")
        model.addConstr(x3 >= 5, "MinRadio")
        model.addConstr(x3 <= 10, "MaxRadio")
        model.addConstr(x4 >= 5, "MinNewspaper")
        model.addConstr(x4 <= 10, "MaxNewspaper")

        # Optimize
        model.optimize()

        # Display the results
        if model.status == GRB.OPTIMAL:
            result = (
                f"Optimal Solution:\n"
                f"Local TV Spots (x1): {x1.x}\n"
                f"Satellite TV Spots (x2): {x2.x}\n"
                f"Radio Spots (x3): {x3.x}\n"
                f"Newspaper Ads (x4): {x4.x}\n"
                f"Total Cost: {cost_coeffs[0] * x1.x + cost_coeffs[1] * x2.x + cost_coeffs[2] * x3.x + cost_coeffs[3] * x4.x} DT\n"
                f"Total Exposure: {exposure_coeffs[0] * x1.x + exposure_coeffs[1] * x2.x + exposure_coeffs[2] * x3.x + exposure_coeffs[3] * x4.x} clients\n"
            )
            result_label.config(text=result, fg="green")
        else:
            result_label.config(text="No optimal solution found.", fg="red")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the GUI
def create_gui():
    window = tk.Tk()
    window.title("Media Budget Allocation")
    window.geometry("800x600")
    window.configure(bg="#f9f9f9")

    # Title Label
    tk.Label(window, text="Media Budget Allocation Problem", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

    # Input Frame
    input_frame = tk.Frame(window, bg="#f9f9f9")
    input_frame.pack(pady=10)


    
    # Budget Input
    tk.Label(input_frame, text="Total Budget (DT):", font=("Arial", 12), bg="#f9f9f9").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    global entry_budget
    entry_budget = tk.Entry(input_frame, font=("Arial", 12), width=20)
    entry_budget.grid(row=0, column=1, padx=5, pady=5)

    # Minimum Female Exposure Input
    tk.Label(input_frame, text="Minimum Female Exposure:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    global entry_min_female_exposure
    entry_min_female_exposure = tk.Entry(input_frame, font=("Arial", 12), width=20)
    entry_min_female_exposure.grid(row=1, column=1, padx=5, pady=5)

    # Coefficients Input Frame
    coeff_frame = tk.Frame(window, bg="#f9f9f9")
    coeff_frame.pack(pady=20)

    # Exposure Coefficients
    tk.Label(coeff_frame, text="Exposure Coefficients", font=("Arial", 12, "bold"), bg="#f9f9f9").grid(row=0, column=1, padx=10)
    tk.Label(coeff_frame, text="Local TV:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    global entry_exposure_local
    entry_exposure_local = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_exposure_local.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(coeff_frame, text="Satellite TV:", font=("Arial", 12), bg="#f9f9f9").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    global entry_exposure_satellite
    entry_exposure_satellite = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_exposure_satellite.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(coeff_frame, text="Radio:", font=("Arial", 12), bg="#f9f9f9").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    global entry_exposure_radio
    entry_exposure_radio = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_exposure_radio.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(coeff_frame, text="Newspaper:", font=("Arial", 12), bg="#f9f9f9").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    global entry_exposure_newspaper
    entry_exposure_newspaper = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_exposure_newspaper.grid(row=4, column=1, padx=5, pady=5)

    # Cost Coefficients
    tk.Label(coeff_frame, text="Cost Coefficients", font=("Arial", 12, "bold"), bg="#f9f9f9").grid(row=0, column=3, padx=10)
    tk.Label(coeff_frame, text="Local TV:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    global entry_cost_local
    entry_cost_local = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_cost_local.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(coeff_frame, text="Satellite TV:", font=("Arial", 12), bg="#f9f9f9").grid(row=2, column=2, sticky="e", padx=5, pady=5)
    global entry_cost_satellite
    entry_cost_satellite = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_cost_satellite.grid(row=2, column=3, padx=5, pady=5)

    tk.Label(coeff_frame, text="Radio:", font=("Arial", 12), bg="#f9f9f9").grid(row=3, column=2, sticky="e", padx=5, pady=5)
    global entry_cost_radio
    entry_cost_radio = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_cost_radio.grid(row=3, column=3, padx=5, pady=5)

    tk.Label(coeff_frame, text="Newspaper:", font=("Arial", 12), bg="#f9f9f9").grid(row=4, column=2, sticky="e", padx=5, pady=5)
    global entry_cost_newspaper
    entry_cost_newspaper = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_cost_newspaper.grid(row=4, column=3, padx=5, pady=5)

    # Female Exposure Coefficients
    tk.Label(coeff_frame, text="Female Exposure Coefficients", font=("Arial", 12, "bold"), bg="#f9f9f9").grid(row=0, column=5, padx=10)
    tk.Label(coeff_frame, text="Local TV:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=4, sticky="e", padx=5, pady=5)
    global entry_female_local
    entry_female_local = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_female_local.grid(row=1, column=5, padx=5, pady=5)

    tk.Label(coeff_frame, text="Satellite TV:", font=("Arial", 12), bg="#f9f9f9").grid(row=2, column=4, sticky="e", padx=5, pady=5)
    global entry_female_satellite
    entry_female_satellite = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_female_satellite.grid(row=2, column=5, padx=5, pady=5)

    tk.Label(coeff_frame, text="Radio:", font=("Arial", 12), bg="#f9f9f9").grid(row=3, column=4, sticky="e", padx=5, pady=5)
    global entry_female_radio
    entry_female_radio = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_female_radio.grid(row=3, column=5, padx=5, pady=5)

    tk.Label(coeff_frame, text="Newspaper:", font=("Arial", 12), bg="#f9f9f9").grid(row=4, column=4, sticky="e", padx=5, pady=5)
    global entry_female_newspaper
    entry_female_newspaper = tk.Entry(coeff_frame, font=("Arial", 12), width=10)
    entry_female_newspaper.grid(row=4, column=5, padx=5, pady=5)



      # Cadre pour afficher les contraintes
    frame_constraints = tk.LabelFrame(window, text="Contraintes du problème", padx=10, pady=10, font=("Arial", 12))
    frame_constraints.pack(padx=10, pady=10)

    # Affichage des contraintes
    constraints_text ="""
    1. Coût total :{entry_cost_local} x1 + {entry_cost_satellite}x2 +{entry_cost_radio} x3 + {entry_cost_newspaper}x4 <= 800
    2. Nombre minimum de femmes : {entry_female_local}x1 +{entry_female_satellite} x2 + {entry_female_radio}x3 + {entry_female_newspaper}x4 >= 2000
    3. Coût de la télévision locale : {entry_cost_local}x1 <= 500
    4. Spots télévision locale : x1 >= 3
    5. Spots télévision par satellite : x2 >= 2
    6. Spots radio : 5 <= x3 <= 10
    7. Spots journaux : 5 <= x4 <= 10
    """
    constraints_label = tk.Label(frame_constraints, text=constraints_text, justify="left", font=("Arial", 10))
    constraints_label.pack()


    # Solve Button
    solve_button = tk.Button(window, text="Solve", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=solve_optimization)
    solve_button.pack(pady=20)

    # Result Label
    global result_label
    result_label = tk.Label(window, text="", font=("Arial", 12), bg="#f9f9f9", justify="left")
    result_label.pack(pady=10, padx=20)

    # Run the GUI loop
    window.mainloop()

# Run the GUI
create_gui()
