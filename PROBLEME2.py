import tkinter as tk
from tkinter import messagebox
from gurobipy import Model, GRB

# Function to calculate and display the optimal energy distribution
def optimize_energy():
    try:
        # Retrieve user inputs
        demand = float(entry_demand.get())
        solar_cost = float(entry_solar_cost.get())
        wind_cost = float(entry_wind_cost.get())
        grid_cost = float(entry_grid_cost.get())

        # Create the optimization model
        model = Model("EnergyOptimization")

        # Decision variables: amount of energy from each source
        solar = model.addVar(vtype=GRB.CONTINUOUS, name="Solar", lb=0, ub=100)
        wind = model.addVar(vtype=GRB.CONTINUOUS, name="Wind", lb=0, ub=80)
        grid = model.addVar(vtype=GRB.CONTINUOUS, name="Grid", lb=0)

        # Objective: Minimize the total energy cost
        model.setObjective(solar_cost * solar + wind_cost * wind + grid_cost * grid, GRB.MINIMIZE)

        # Constraints
        model.addConstr(solar + wind + grid >= demand, "Demand")  # Energy demand must be met

        # Optimize the model
        model.optimize()

        # Check if an optimal solution was found
        if model.status == GRB.OPTIMAL:
            result_text = "Solution optimale trouvée :\n"
            result_text += f"\u2022 Energie solaire : {solar.x:.2f} kWh\n"
            result_text += f"\u2022 Energie éolienne : {wind.x:.2f} kWh\n"
            result_text += f"\u2022 Energie du réseau : {grid.x:.2f} kWh\n"
            result_text += f"\u2022 Coût total : {model.objVal:.2f} DT"
            result_label.config(text=result_text, fg="green")
        else:
            result_label.config(text="Aucune solution optimale trouvée.", fg="red")

    except ValueError:
        messagebox.showerror("Erreur de saisie", "Veuillez entrer des valeurs numériques valides.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

# Create the UI
def create_ui():
    window = tk.Tk()
    window.title("Optimisation de l'Énergie")

    # Style
    window.configure(bg="#f0f0f0")

    # Input frame
    input_frame = tk.LabelFrame(window, text="Entrée des paramètres", padx=10, pady=10, font=("Arial", 12))
    input_frame.pack(padx=10, pady=10)

    # Labels and entry fields
    tk.Label(input_frame, text="Demande d'énergie (kWh) :", font=("Arial", 10)).grid(row=0, column=0, sticky='e')
    global entry_demand
    entry_demand = tk.Entry(input_frame, font=("Arial", 10), width=15)
    entry_demand.grid(row=0, column=1)

    tk.Label(input_frame, text="Coût par kWh (Solaire) :", font=("Arial", 10)).grid(row=1, column=0, sticky='e')
    global entry_solar_cost
    entry_solar_cost = tk.Entry(input_frame, font=("Arial", 10), width=15)
    entry_solar_cost.grid(row=1, column=1)

    tk.Label(input_frame, text="Coût par kWh (Éolien) :", font=("Arial", 10)).grid(row=2, column=0, sticky='e')
    global entry_wind_cost
    entry_wind_cost = tk.Entry(input_frame, font=("Arial", 10), width=15)
    entry_wind_cost.grid(row=2, column=1)

    tk.Label(input_frame, text="Coût par kWh (Réseau) :", font=("Arial", 10)).grid(row=3, column=0, sticky='e')
    global entry_grid_cost
    entry_grid_cost = tk.Entry(input_frame, font=("Arial", 10), width=15)
    entry_grid_cost.grid(row=3, column=1)

     # Cadre pour afficher les contraintes
    frame_constraints = tk.LabelFrame(window, text="Contraintes du problème", padx=10, pady=10, font=("Arial", 12))
    frame_constraints.pack(padx=10, pady=10)

    # Affichage des contraintes
    constraints_text = """
    1. La demande d'énergie doit être satisfaite :  Solar + Wind + Grid >= demand kWh
    2. L'énergie solaire doit être comprise entre 0 et 100 kWh.
    3. L'énergie éolienne doit être comprise entre 0 et 80 kWh.
    4. L'énergie du réseau doit être >= 0 kWh.
    """
    constraints_label = tk.Label(frame_constraints, text=constraints_text, justify="left", font=("Arial", 10))
    constraints_label.pack()

    # Solve button
    solve_button = tk.Button(window, text="Optimiser", command=optimize_energy, font=("Arial", 10), bg="#77DD77", fg="white")
    solve_button.pack(pady=10)

    # Result label
    global result_label
    result_label = tk.Label(window, text="", justify="left", font=("Arial", 12), pady=10)
    result_label.pack(padx=10, pady=10)

    # Run the UI loop
    window.mainloop()

# Run the program
create_ui()
