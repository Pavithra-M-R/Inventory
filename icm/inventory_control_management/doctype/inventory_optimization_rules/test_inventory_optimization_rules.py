# Copyright (c) 2025, Pavithra M R and Contributors
# See license.txt
import frappe
from frappe.tests.utils import FrappeTestCase
from icm.inventory_control_management.doctype.inventory_optimization_rules.inventory_optimization_rules import calculate_optimal_distribution

class TestInventoryOptimizationRules(FrappeTestCase):
    def setUp(self):
        # Create test item group
        if not frappe.db.exists("Item Group", "Testing Group"):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": "Testing Group",
                "is_group": 0
            }).insert(ignore_permissions=True)

        # Create test item
        if not frappe.db.exists("Item", "TEST-ITEM-001"):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": "TEST-ITEM-001",
                "item_name": "Test Item",
                "item_group": "Testing Group",
                "stock_uom": "Nos"
            }).insert(ignore_permissions=True)

        # Create warehouses with explicit 'name' set to match the label
        for wh in ["Test WH-A", "Test WH-B"]:
            if not frappe.db.exists("Warehouse", wh):
                frappe.get_doc({
                    "doctype": "Warehouse",
                    "warehouse_name": wh,
                    "name": wh  # Explicitly set document name to prevent link errors
                }).insert(ignore_permissions=True)

        # Add stock using Stock Entry (Material Receipt)
        self.create_stock("TEST-ITEM-001", "Test WH-A", 100)
        self.create_stock("TEST-ITEM-001", "Test WH-B", 0)

        # Create Inventory Optimization Rule
        self.rule = frappe.get_doc({
            "doctype": "Inventory Optimization Rules",
            "item_category": "Testing Group"
        }).insert(ignore_permissions=True)

    def create_stock(self, item_code, warehouse, qty):
        # Create and submit a Stock Entry for Material Receipt to add stock
        se = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "items": [{
                "item_code": item_code,
                "qty": qty,
                "t_warehouse": warehouse,
                "uom": "Nos",
                "stock_uom": "Nos"
            }]
        })
        se.insert()
        se.submit()

    def test_optimal_distribution_generated(self):
        # Run the core function to calculate optimal distribution
        calculate_optimal_distribution(self.rule.name)

        # Reload the rule doc to get updated child table
        self.rule.reload()

        # Verify the child table has rows
        result = self.rule.optimal_distribution_result
        self.assertGreater(len(result), 0, "Optimal distribution result should not be empty")

        # Check structure of first row
        first = result[0]
        self.assertEqual(first.item_code, "TEST-ITEM-001")
        self.assertEqual(first.from_warehouse, "Test WH-A")
        self.assertEqual(first.to_warehouse, "Test WH-B")
        self.assertGreater(first.qty_to_transfer, 0)

    def tearDown(self):
        # Clean up Inventory Optimization Rule
        frappe.db.delete("Inventory Optimization Rules", {"item_category": "Testing Group"})

        # Cancel and delete Stock Entries created (optional - to clean test data)
        stock_entries = frappe.get_all("Stock Entry", filters={
            "stock_entry_type": "Material Receipt",
            "docstatus": 1
        }, fields=["name"])

        for se in stock_entries:
            try:
                doc = frappe.get_doc("Stock Entry", se.name)
                doc.cancel()
                doc.delete()
            except Exception:
                pass

        # Delete Items and Warehouses
        frappe.db.delete("Item", {"item_code": "TEST-ITEM-001"})
        frappe.db.delete("Warehouse", {"name": ["Test WH-A", "Test WH-B"]})

        # Commit to finalize deletes
        frappe.db.commit()