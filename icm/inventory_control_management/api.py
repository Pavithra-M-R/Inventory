import frappe
from datetime import datetime
from frappe import _
from frappe.utils import now_datetime
from frappe.utils import nowdate, add_days
from collections import defaultdict
from icm.inventory_control_management.doctype.inventory_optimization_rules.inventory_optimization_rules import calculate_optimal_distribution
#NEW CODE Generate transfer orders when imbalances are detected
#@frappe.whitelist()
def generate_transfer_orders_from_rules():
    rules = frappe.get_all("Inventory Optimization Rules", fields=["name"])
    total_transfers_created = 0

    for rule in rules:
        calculate_optimal_distribution(rule.name)

        doc = frappe.get_doc("Inventory Optimization Rules", rule.name)

        for row in doc.optimal_distribution_result:
            if not row.transfer_created and row.qty_to_transfer > 0:
                created = create_stock_transfer_entry(row)
                if created:
                    row.transfer_created = 1
                    total_transfers_created += 1

        doc.save()

    if total_transfers_created == 0:
        frappe.msgprint(" No new stock transfers were needed.")
    else:
        frappe.msgprint(f" {total_transfers_created} stock transfers were created successfully.")

def create_stock_transfer_entry(row):
    try:
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.purpose = "Material Transfer"
        stock_entry.stock_entry_type = "Material Transfer"
        stock_entry.from_warehouse = row.from_warehouse
        stock_entry.to_warehouse = row.to_warehouse

        stock_entry.append("items", {
            "item_code": row.item_code,
            "qty": row.qty_to_transfer,
            "uom": frappe.db.get_value("Item", row.item_code, "stock_uom"),
            "stock_uom": frappe.db.get_value("Item", row.item_code, "stock_uom"),
            "s_warehouse": row.from_warehouse,
            "t_warehouse": row.to_warehouse
        })

        stock_entry.save()
        stock_entry.submit()
        frappe.logger().info(f"Stock Entry created for {row.item_code} from {row.from_warehouse} to {row.to_warehouse}")
        return True

    except Exception as e:
        frappe.log_error(f"Failed to create Stock Entry: {str(e)}")
        return False
    
#Implement a forecastng algorithm that adjusts reorder points seasonally
@frappe.whitelist()
def calculate_seasonal_forecast(docname):
    doc = frappe.get_doc("Inventory Optimization Rules", docname)

    item_group = doc.item_category
    lead_time_days = doc.lead_time_days or 0
    reorder_days = doc.reorder_point_days or 30

    items = frappe.get_all("Item", filters={"item_group": item_group}, fields=["name"])

    doc.set("forecast_result", [])

    for item in items:
        item_code = item.name

        past_date = add_days(nowdate(), -reorder_days)
        stock_out = frappe.db.sql("""
            SELECT SUM(actual_qty)
            FROM `tabStock Ledger Entry`
            WHERE item_code = %s
              AND posting_date >= %s
              AND actual_qty < 0
        """, (item_code, past_date))[0][0] or 0

        daily_usage = abs(stock_out) / reorder_days if reorder_days else 0
        projected_demand = daily_usage * lead_time_days

        doc.append("forecast_result", {
            "item_code": item_code,
            "avg_daily_usage": daily_usage,
            "projected_demand": projected_demand,
            "lead_time_days": lead_time_days
        })

    doc.save()
    frappe.msgprint(" Forecast result has been calculated and updated in the table.")

def run_forecast_for_all_rules():
    rules = frappe.get_all("Inventory Optimization Rules", fields=["name"])
    for rule in rules:
        calculate_seasonal_forecast(rule.name)

#Create a REST API endpoint that external systems can query for real-time inventory status
@frappe.whitelist(allow_guest=True)
def get_inventory_status(item_code=None, warehouse=None):
    filters = {}
    if item_code:
        filters["item_code"] = item_code
    if warehouse:
        filters["warehouse"] = warehouse

    data = frappe.db.get_all(
        "Bin",
        filters=filters,
        fields=["item_code", "warehouse", "actual_qty"]
    )

    results = []
    for row in data:
        uom = frappe.db.get_value("Item", row.item_code, "stock_uom")
        stock_status = "Healthy"
        if row.actual_qty <= 0:
            stock_status = "Out of Stock"
        elif row.actual_qty < 5:
            stock_status = "Low Stock"

        results.append({
            "item_code": row.item_code,
            "warehouse": row.warehouse,
            "actual_qty": row.actual_qty,
            "stock_uom": uom,
            "stock_status": stock_status
        })

    return results
#Inventory health visualiza<on
@frappe.whitelist()
def get_inventory_health_data():
    counts = {
        "Healthy": 0,
        "Low Stock": 0,
        "Overstocked": 0
    }

    rules = frappe.get_all("Inventory Optimization Rules", fields=["item_category", "min_stock", "max_stock"])
    item_groups = [r.item_category for r in rules]

    items = frappe.get_all("Item", filters={"item_group": ["in", item_groups]}, fields=["name", "item_group"])

    for item in items:
        total_qty = frappe.db.sql("""
            SELECT SUM(actual_qty) AS total
            FROM tabBin
            WHERE item_code = %s
        """, (item.name,), as_dict=True)[0].total or 0

        rule = next((r for r in rules if r.item_category == item.item_group), None)
        if not rule:
            continue

        if total_qty < rule.min_stock:
            counts["Low Stock"] += 1
        elif total_qty > rule.max_stock:
            counts["Overstocked"] += 1
        else:
            counts["Healthy"] += 1

    return {
        "labels": list(counts.keys()),
        "datasets": [
            {"values": list(counts.values())}
        ]
    }

#Alerts for pending stockouts
@frappe.whitelist()
def send_low_stock_alerts():
    low_stock_items = frappe.db.sql("""
        SELECT
            i.name AS item_code,
            b.warehouse,
            b.actual_qty,
            i.min_stock_threshold
        FROM `tabBin` b
        JOIN `tabItem` i ON b.item_code = i.name
        WHERE
            i.min_stock_threshold IS NOT NULL
            AND b.actual_qty < i.min_stock_threshold
    """, as_dict=True)

    if low_stock_items:
        msg = " Pending Stockouts Detected:\n"
        for row in low_stock_items:
            msg += f"\n• Item: {row.item_code} in {row.warehouse} (Qty: {row.actual_qty}, Threshold: {row.min_stock_threshold})"

        frappe.sendmail(
            recipients=["pavithramr88@gmail.com"],
            subject="Low Stock Alert",
            message=msg
        )
        frappe.msgprint("Low stock alerts sent.")
    else:
        frappe.msgprint(" No stockouts detected today.")
