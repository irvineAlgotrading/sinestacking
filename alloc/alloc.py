#alloc.py
import numpy as np

# Define parameters

number_of_machines = 10

price_per_service = 2000
services_per_machine_per_month = 5

operational_cost_per_month_per_service_machine = 2000 # materials/power/labor
maintenance_cost_per_month_per_service_machine = 1000 # spares/repairs/labor

machine_sale_price = 60000 # new
cost_to_produce_machine = 20000 # production cost of full system
spare_parts_sales_per_month = 2000 # machine owners by spares/repairs
cost_to_support_machine_sold = 1000 # support engineering/interaction
cost_to_acquire_sale = 2000

resell_price = 10000 #resell value of machine after 36 months

depreciation_period_months = 36
months_in_year = 12

# Calculate profit from services sold
def calculate_profit(num_machines, service_price, machine_cost, machine_sale_price):
    # Calculate profits from services
    total_services_per_month = services_per_machine_per_month * num_machines
    monthly_service_revenue = service_price * total_services_per_month
    annual_service_revenue = monthly_service_revenue * months_in_year

    monthly_operational_cost = operational_cost_per_month_per_service_machine * num_machines
    monthly_maintenance_cost = maintenance_cost_per_month_per_service_machine * num_machines
    annual_operational_and_maintenance_cost = (monthly_operational_cost + monthly_maintenance_cost) * months_in_year
    annual_depreciation = ((machine_sale_price - resell_price) * num_machines) / depreciation_period_months * months_in_year
    profit_services = annual_service_revenue - annual_operational_and_maintenance_cost - annual_depreciation

    # Calculate profits from machines sold
    annual_machine_production_cost = machine_cost * num_machines
    annual_spare_parts_sales_revenue = spare_parts_sales_per_month * months_in_year * num_machines
    annual_machine_sale_revenue = machine_sale_price * num_machines + annual_spare_parts_sales_revenue
    profit_machines = annual_machine_sale_revenue - annual_machine_production_cost
    total_additional_costs_for_machine_sales = (cost_to_support_machine_sold + cost_to_acquire_sale) * num_machines
    profit_machines_with_additional_costs = profit_machines - total_additional_costs_for_machine_sales

    return profit_services, profit_machines_with_additional_costs

# Sensitivity Analysis
print("Sensitivity Analysis:")
for num_machines in range(5, 100):  # Varying the number of machines
    for service_price in range(1500, 2500, 3500):  # Varying the service price
        profit_services, profit_machines = calculate_profit(num_machines, service_price, cost_to_produce_machine, machine_sale_price)
        print(f"Number of Machines: {num_machines}, Service Price: ${service_price}")
        print(f"Profit from Services: ${profit_services:,.2f}, Profit from Machines: ${profit_machines:,.2f}\n")

# Original comparison
profit_from_services, profit_from_machines_sold_with_additional_costs = calculate_profit(number_of_machines, price_per_service, cost_to_produce_machine, machine_sale_price)
print("Original Comparison:")
print(f"Annual Service Profit: ${profit_from_services:,.2f}")
print(f"Annual Machine Sales Profit: ${profit_from_machines_sold_with_additional_costs:,.2f}")

if profit_from_services > profit_from_machines_sold_with_additional_costs:
    print("Services Sold is more profitable.")
elif profit_from_machines_sold_with_additional_costs > profit_from_services:
    print("Machines Sold is more profitable.")
else:
    print("Both avenues are equally profitable.")