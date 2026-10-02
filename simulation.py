import pandas as pd


def run_simulation(
    starting_inventory,
    daily_demand,
    supplier_lead_time,
    selling_price,
    cost_per_unit,
    days=30,
):
    inventory = starting_inventory
    total_sold = 0
    total_lost_sales = 0
    total_revenue = 0
    total_cost = 0

    inventory_history = []

    # Reorder when inventory reaches this level
    reorder_point = daily_demand * supplier_lead_time

    # Order enough stock to cover lead time + 7 days
    target_inventory = daily_demand * (
        supplier_lead_time + 7
    )

    pending_orders = []

    for day in range(1, days + 1):

        # Receive orders whose delivery date has arrived
        arriving_orders = [
            order for order in pending_orders
            if order["arrival_day"] == day
        ]

        for order in arriving_orders:
            inventory += order["quantity"]

        pending_orders = [
            order for order in pending_orders
            if order["arrival_day"] != day
        ]

        # Meet customer demand using available inventory
        units_sold = min(inventory, daily_demand)
        lost_sales = daily_demand - units_sold

        inventory -= units_sold

        # Calculate daily business results
        revenue = units_sold * selling_price
        cost = units_sold * cost_per_unit

        total_sold += units_sold
        total_lost_sales += lost_sales
        total_revenue += revenue
        total_cost += cost

        # Reorder if stock reaches the reorder point
        if (
            inventory <= reorder_point
            and not pending_orders
        ):
            order_quantity = max(
                0, int(target_inventory - inventory)
            )

            if order_quantity > 0:
                pending_orders.append({
                    "quantity": order_quantity,
                    "arrival_day": day + supplier_lead_time,
                })

        inventory_history.append({
            "Day": day,
            "Inventory": inventory,
            "Units Sold": units_sold,
            "Lost Sales": lost_sales,
            "Revenue": revenue,
            "Cost": cost,
            "Profit": revenue - cost,
        })

    results = pd.DataFrame(inventory_history)

    summary = {
        "units_sold": total_sold,
        "lost_sales": total_lost_sales,
        "revenue": total_revenue,
        "cost": total_cost,
        "gross_profit": total_revenue - total_cost,
        "ending_inventory": inventory,
    }

    return results, summary

