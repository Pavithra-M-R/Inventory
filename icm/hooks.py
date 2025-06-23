app_name = "icm"
app_title = "Inventory Control Management"
app_publisher = "Pavithra M R"
app_description = "Inventory Control Management"
app_email = "pavithramr88@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/icm/css/icm.css"
# app_include_js = "/assets/icm/js/icm.js"

# include js, css files in header of web template
# web_include_css = "/assets/icm/css/icm.css"
# web_include_js = "/assets/icm/js/icm.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "icm/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "icm/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "icm.utils.jinja_methods",
# 	"filters": "icm.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "icm.install.before_install"
# after_install = "icm.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "icm.uninstall.before_uninstall"
# after_uninstall = "icm.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "icm.utils.before_app_install"
# after_app_install = "icm.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "icm.utils.before_app_uninstall"
# after_app_uninstall = "icm.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "icm.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"icm.tasks.all"
# 	],
# 	"daily": [
# 		"icm.tasks.daily"
# 	],
# 	"hourly": [
# 		"icm.tasks.hourly"
# 	],
# 	"weekly": [
# 		"icm.tasks.weekly"
# 	],
# 	"monthly": [
# 		"icm.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "icm.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "icm.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "icm.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["icm.utils.before_request"]
# after_request = ["icm.utils.after_request"]

# Job Events
# ----------
# before_job = ["icm.utils.before_job"]
# after_job = ["icm.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"icm.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

scheduler_events = {
    "hourly": [
        "icm.inventory_control_management.api.generate_transfer_orders_from_rules"
    ]
}

scheduler_events = {
    "weekly": [
        "icm.inventory_control_management.api.run_forecast_for_all_rules"
    ]
}

override_whitelisted_methods = {
    "icm.inventory_control_management.api.get_inventory_status": "icm.inventory_control_management.api.get_inventory_status"
}

scheduler_events = {
    "daily": [
        "icm.inventory_control_management.api.send_low_stock_alerts"
    ]
}

fixtures = [
    {
        "dt": "Report",
        "filters": [
            ["name", "in", [
                "Inventory Health Report_2",
                "Stock Movement Analytics_2",
                "ROI Metrics_2"
            ]]
        ]
    },
    {
        "dt": "Dashboard Chart",
        "filters": [
            ["name", "in", [
                "Inventory Health Report_2",
                "Stock Movement Analytics_2",
                "ROI Metrics_2"
            ]]
        ]
    },
    {
        "dt": "Dashboard",
        "filters": [
            ["name", "in", [
                "Inventory Health Report_2",
                "Stock Movement Analytics_2",
                "ROI Metrics_2"
            ]]
        ]
    },
    {
        "dt": "Workspace",
        "filters": [
            ["name", "=", "Inventory Management"]
        ]
    }
]
