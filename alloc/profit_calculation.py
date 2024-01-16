#profit_calculation.py
import numpy as np

# Define machine sale and service scenario parameters
prices = {'initial': {'sale': 100000, 'service': 3000}}
costs = {'operational_cost_per_month': 1000}
sales_targets = {'machine': 30, 'service': 600}  # Assuming 600 services in total, not per month
months = 12  # Assuming a year has 12 months
discount_rate = 0.05  # Assuming an unchanged discount rate
number_of_machines = 30  # Assuming this is the total number of machines for the operational cost calculation
number_of_services = 5 #assumes 5 services per month per machine


# Utilize sales_targets and prices to define ranges
machine_sales_range = range(1, sales_targets['machine'] + 1)  # Dynamically based on sales_targets
service_sales_range = range(5, 6, 1)  # Since 5 services per month per machine is fixed

# Define price ranges around the initial price
machine_price_step = 500  # Step for machine price range
machine_price_range = range(prices['initial']['sale'] - 1000, prices['initial']['sale'] + 1000, machine_price_step)

service_price_step = 100  # Step for service price range
service_price_range = range(max(1000, prices['initial']['service'] - 1000), prices['initial']['service'] + 1000, service_price_step)

def calculate_npv(rate, cash_flows):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))

def calculate_result(prices, costs, targets, months, discount_rate, num_machines, num_services_per_machine):
    monthly_costs = costs['operational_cost_per_month'] * num_machines
    results = {}
    for scenario, price_set in prices.items():
        # Calculate monthly and annual revenue from services
        services_per_month = num_services_per_machine * num_machines
        monthly_service_revenue = price_set['service'] * services_per_month
        annual_service_revenue = monthly_service_revenue * 12

        # Calculate monthly and annual profit from services
        monthly_profit = monthly_service_revenue - monthly_costs
        annual_profit = monthly_profit * 12

        # Calculate Net Present Value (NPV) of the annual profits
        cash_flows = [annual_profit] * (months // 12)
        npv = calculate_npv(discount_rate, [0] + cash_flows)

        # Calculate total revenue from selling machines
        total_revenue = price_set['sale'] * num_machines

        # Store detailed results
        results[scenario] = {
            'selling': total_revenue,
            'services_annual_revenue': annual_service_revenue,
            'services_annual_profit': annual_profit,
            'services_npv': npv,
            'services_per_month': services_per_month,
            'max_sale_price': None  # Removed 'updated' scenario due to undefined prices
        }

    # Sales target calculations
    results['target'] = {
        'machine_sales': targets['machine'] * prices['initial']['sale'],
        'service_sales': targets['service'] * prices['initial']['service']
    }
    return results
