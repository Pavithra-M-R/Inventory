# Copyright (c) 2025, Pavithra M R and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class InventoryOptimizationRules(Document):
    pass 

@frappe.whitelist()
def calculate_optimal_distribution(docname):
	print("11111111111111")
	doc = frappe.get_doc("Inventory Optimization Rules", docname)
	print("00000",docname)
	items = frappe.get_all("Item", filters={"item_group": doc.item_category}, fields=["name"])
	print("ITEM",items)
	results = []

	for item in items:
		stock_data = frappe.db.sql("""
			SELECT warehouse, actual_qty
			FROM tabBin
			WHERE item_code = %s
		""", (item.name,), as_dict=True)
		print("stock data",stock_data)
		if not stock_data or len(stock_data) < 2:
			continue

		total_stock = sum(row.actual_qty for row in stock_data)
		ideal_qty = total_stock // len(stock_data)  
		excess_list = []
		shortage_list = []

		for s in stock_data:
			if s.actual_qty > ideal_qty:
				excess_list.append({
					"warehouse": s.warehouse,
					"qty": s.actual_qty - ideal_qty,
					"current_qty": s.actual_qty,
					"required_qty": ideal_qty
				})
			elif s.actual_qty < ideal_qty:
				shortage_list.append({
					"warehouse": s.warehouse,
					"qty": ideal_qty - s.actual_qty,
					"current_qty": s.actual_qty,
					"required_qty": ideal_qty
				})

		for excess in excess_list:
			for shortage in shortage_list:
				if excess["qty"] <= 0:
					break
				if shortage["qty"] <= 0:
					continue

				transfer_qty = min(excess["qty"], shortage["qty"])

				results.append({
					"item_code": item.name,
					"from_warehouse": excess["warehouse"],
					"to_warehouse": shortage["warehouse"],
					"qty_to_transfer": transfer_qty,
					"current_qty": excess["current_qty"],
					"required_qty": excess["required_qty"]
				})

				excess["qty"] -= transfer_qty
				shortage["qty"] -= transfer_qty
	print("result",results)
	doc.set("optimal_distribution_result", [])

	for row in results:
		doc.append("optimal_distribution_result", row)

	doc.save()

	frappe.msgprint("Optimal stock distribution calculated and displayed in the table.")