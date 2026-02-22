"""
Vue Router configuration mapping for natural language navigation.
This file contains all frontend routes with metadata for intelligent routing.
"""

ROUTE_MAPPINGS = {
    # Home & Search
    "home": {
        "path": "/",
        "name": "Home",
        "keywords": ["home", "dashboard", "main", "start"],
        "description": "Home page / Dashboard"
    },
    "search": {
        "path": "/search",
        "name": "Search",
        "keywords": ["search", "find", "lookup"],
        "description": "Search functionality"
    },
    
    # Authentication
    "login": {
        "path": "/login",
        "name": "Login",
        "keywords": ["login", "signin", "sign in", "authenticate"],
        "description": "Login page"
    },
    "register": {
        "path": "/register",
        "name": "Register",
        "keywords": ["register", "signup", "sign up", "create account"],
        "description": "Registration page"
    },
    "logout": {
        "path": "/logout",
        "name": "Logout",
        "keywords": ["logout", "signout", "sign out"],
        "description": "Logout"
    },
    "profile": {
        "path": "/profile",
        "name": "UserProfile",
        "keywords": ["profile", "user profile", "my profile", "account"],
        "description": "User profile page"
    },
    
    # File Management
    "upload": {
        "path": "/upload",
        "name": "Upload",
        "keywords": ["upload", "upload file"],
        "description": "Upload files"
    },
    "download": {
        "path": "/download",
        "name": "Download",
        "keywords": ["download", "download file"],
        "description": "Download files"
    },
    
    # Company Management
    "select_company": {
        "path": "/select-company",
        "name": "SelectCompany",
        "keywords": ["select company", "choose company", "switch company"],
        "description": "Select/Switch company"
    },
    "company_list": {
        "path": "/companies",
        "name": "CompanyList",
        "keywords": ["companies", "company list", "list companies", "view companies", "show companies"],
        "description": "List all companies"
    },
    "company_add": {
        "path": "/companies/add",
        "name": "CompanyAdd",
        "keywords": ["add company", "new company", "create company"],
        "description": "Add new company"
    },
    "export_data": {
        "path": "/export-data",
        "name": "ExportData",
        "keywords": ["export", "export data", "download data"],
        "description": "Export data"
    },
    "import_data": {
        "path": "/import-data",
        "name": "ImportData",
        "keywords": ["import", "import data", "upload data"],
        "description": "Import data"
    },
    
    # Financial Year
    "financial_year_list": {
        "path": "/financial-years",
        "name": "FinancialYearList",
        "keywords": ["financial years", "financial year list", "list financial years", "view financial years"],
        "description": "List financial years"
    },
    "financial_year_add": {
        "path": "/financial-years/add",
        "name": "FinancialYearAdd",
        "keywords": ["add financial year", "new financial year", "create financial year"],
        "description": "Add financial year"
    },
    
    # Items/Products
    "item_list": {
        "path": "/items",
        "name": "ItemList",
        "keywords": ["items", "products", "item list", "product list", "list items", "view items", "show items"],
        "description": "List all items/products"
    },
    "item_add": {
        "path": "/items/add",
        "name": "ItemAdd",
        "keywords": ["add item", "add product", "new item", "new product", "create item", "create product"],
        "description": "Add new item/product"
    },
    
    # Ledgers
    "ledger_list": {
        "path": "/ledgers",
        "name": "LedgerList",
        "keywords": ["ledgers", "ledger list", "list ledgers", "view ledgers", "show ledgers", "accounts"],
        "description": "List all ledgers"
    },
    "ledger_add": {
        "path": "/ledgers/add",
        "name": "LedgerAdd",
        "keywords": ["add ledger", "new ledger", "create ledger", "add account", "new account"],
        "description": "Add new ledger"
    },
    
    # Taxes
    "tax_list": {
        "path": "/taxes",
        "name": "TaxList",
        "keywords": ["taxes", "tax list", "list taxes", "view taxes", "show taxes"],
        "description": "List all taxes"
    },
    "tax_add": {
        "path": "/taxes/add",
        "name": "TaxAdd",
        "keywords": ["add tax", "new tax", "create tax"],
        "description": "Add new tax"
    },
    
    # Transactions - General
    "transaction_list": {
        "path": "/transactions",
        "name": "TransactionList",
        "keywords": ["transactions", "transaction list", "list transactions", "view transactions", "show transactions"],
        "description": "List all transactions"
    },
    
    # Sale Transactions
    "sales_invoice_list": {
        "path": "/transactions/sales-invoice",
        "name": "SalesInvoiceList",
        "keywords": ["sales invoices", "sale invoice list", "view sales invoices"],
        "description": "List sales invoices"
    },
    "new_sale_invoice": {
        "path": "/transactions/new/sale-invoice",
        "name": "NewSaleInvoice",
        "keywords": ["add sales invoice", "new sales invoice", "create sales invoice", "new sale", "add sale"],
        "description": "Create new sales invoice"
    },
    "sales_order_list": {
        "path": "/transactions/sales-order",
        "name": "SalesOrderList",
        "keywords": ["sales orders", "sale order list", "view sales orders"],
        "description": "List sales orders"
    },
    "new_sale_order": {
        "path": "/transactions/new/sale-order",
        "name": "NewSaleOrder",
        "keywords": ["add sales order", "new sales order", "create sales order"],
        "description": "Create new sales order"
    },
    "new_sale_quotation": {
        "path": "/transactions/new/sale-quotation",
        "name": "NewSaleQuotation",
        "keywords": ["add sales quotation", "new sales quotation", "create sales quotation", "new quote", "add quote"],
        "description": "Create new sales quotation"
    },
    "sales_return_list": {
        "path": "/transactions/sales-return",
        "name": "SalesReturnList",
        "keywords": ["sales returns", "sale return list", "view sales returns"],
        "description": "List sales returns"
    },
    "new_sale_return": {
        "path": "/transactions/new/sale-return",
        "name": "NewSaleReturn",
        "keywords": ["add sales return", "new sales return", "create sales return"],
        "description": "Create new sales return"
    },
    
    # Purchase Transactions
    "purchase_invoice_list": {
        "path": "/transactions/purchase-invoice",
        "name": "PurchaseInvoiceList",
        "keywords": ["purchase invoices", "purchase bill", "purchase invoice list", "view purchase invoices"],
        "description": "List purchase invoices"
    },
    "new_purchase_bill": {
        "path": "/transactions/new/purchase-bill",
        "name": "NewPurchaseBill",
        "keywords": ["add purchase invoice", "new purchase invoice", "create purchase invoice", "new purchase", "add purchase"],
        "description": "Create new purchase bill"
    },
    "purchase_order_list": {
        "path": "/transactions/purchase-order",
        "name": "PurchaseOrderList",
        "keywords": ["purchase orders", "purchase order list", "view purchase orders"],
        "description": "List purchase orders"
    },
    "new_purchase_order": {
        "path": "/transactions/new/purchase-order",
        "name": "NewPurchaseOrder",
        "keywords": ["add purchase order", "new purchase order", "create purchase order"],
        "description": "Create new purchase order"
    },
    "new_purchase_quotation": {
        "path": "/transactions/new/purchase-quotation",
        "name": "NewPurchaseQuotation",
        "keywords": ["add purchase quotation", "new purchase quotation", "create purchase quotation"],
        "description": "Create new purchase quotation"
    },
    "purchase_return_list": {
        "path": "/transactions/purchase-return",
        "name": "PurchaseReturnList",
        "keywords": ["purchase returns", "purchase return list", "view purchase returns"],
        "description": "List purchase returns"
    },
    "new_purchase_return": {
        "path": "/transactions/new/purchase-return",
        "name": "NewPurchaseReturn",
        "keywords": ["add purchase return", "new purchase return", "create purchase return"],
        "description": "Create new purchase return"
    },
    
    # Payment & Receipt Transactions
    "cash_payment_list": {
        "path": "/transactions/cash-paid",
        "name": "CashPaymentList",
        "keywords": ["cash payments", "cash paid", "view cash payments"],
        "description": "List cash payments"
    },
    "new_cash_payment": {
        "path": "/transactions/new/cash-payment",
        "name": "NewCashPayment",
        "keywords": ["add cash payment", "new cash payment", "create cash payment", "pay cash"],
        "description": "Create new cash payment"
    },
    "bank_payment_list": {
        "path": "/transactions/bank-payment",
        "name": "BankPaymentList",
        "keywords": ["bank payments", "view bank payments"],
        "description": "List bank payments"
    },
    "new_bank_payment": {
        "path": "/transactions/new/bank-payment",
        "name": "NewBankPayment",
        "keywords": ["add bank payment", "new bank payment", "create bank payment", "pay by bank"],
        "description": "Create new bank payment"
    },
    "cash_receipt_list": {
        "path": "/transactions/cash-received",
        "name": "CashReceiptList",
        "keywords": ["cash receipts", "cash received", "view cash receipts"],
        "description": "List cash receipts"
    },
    "new_cash_receipt": {
        "path": "/transactions/new/cash-receipt",
        "name": "NewCashReceipt",
        "keywords": ["add cash receipt", "new cash receipt", "create cash receipt", "receive cash"],
        "description": "Create new cash receipt"
    },
    "bank_receipt_list": {
        "path": "/transactions/bank-payment-received",
        "name": "BankReceiptList",
        "keywords": ["bank receipts", "view bank receipts"],
        "description": "List bank receipts"
    },
    "new_bank_receipt": {
        "path": "/transactions/new/bank-receipt",
        "name": "NewBankReceipt",
        "keywords": ["add bank receipt", "new bank receipt", "create bank receipt", "receive by bank"],
        "description": "Create new bank receipt"
    },
    
    # Journal Entries
    "journal_entries_list": {
        "path": "/transactions/journal-entries",
        "name": "JournalEntriesList",
        "keywords": ["journal entries", "journal entry list", "view journal entries"],
        "description": "List journal entries"
    },
    "new_journal_entry": {
        "path": "/transactions/journal-entry/new",
        "name": "NewJournalEntryForm",
        "keywords": ["add journal entry", "new journal entry", "create journal entry"],
        "description": "Create new journal entry"
    },
    
    # Reports - Ledger
    "ledger_report": {
        "path": "/reports/ledger",
        "name": "LedgerReport",
        "keywords": ["ledger report", "view ledger report", "show ledger report"],
        "description": "Ledger report"
    },
    "ledger_report_by_type": {
        "path": "/reports/ledger-by-type",
        "name": "LedgerReportByType",
        "keywords": ["ledger report by type", "view ledger by type"],
        "description": "Ledger report by type"
    },
    
    # Reports - Stock
    "stock_ledger_report": {
        "path": "/reports/stock-ledger",
        "name": "StockLedgerReport",
        "keywords": ["stock ledger report", "stock report", "inventory report"],
        "description": "Stock ledger report"
    },
    "item_monthly_chart": {
        "path": "/reports/item-monthly-chart",
        "name": "ItemMonthlyChart",
        "keywords": ["item monthly chart", "monthly item report", "item chart"],
        "description": "Item monthly chart"
    },
    
    # Reports - Daybook
    "daybook_report": {
        "path": "/reports/daybook",
        "name": "DaybookReport",
        "keywords": ["daybook", "daybook report", "daily report", "view daybook"],
        "description": "Daybook report"
    },
    
    # Reports - Trial Balance
    "current_asset_report": {
        "path": "/reports/current-stock",
        "name": "CurrentAssetReport",
        "keywords": ["current assets", "current stock", "asset report"],
        "description": "Current asset report"
    },
    "current_liabilities_report": {
        "path": "/reports/current-liabilities",
        "name": "CurrentLiabilitiesReport",
        "keywords": ["current liabilities", "liability report"],
        "description": "Current liabilities report"
    },
    
    # Reports - Registers
    "sales_register": {
        "path": "/reports/sales-register",
        "name": "SalesRegister",
        "keywords": ["sales register", "view sales register"],
        "description": "Sales register report"
    },
    "purchase_register": {
        "path": "/reports/purchase-register",
        "name": "PurchaseRegister",
        "keywords": ["purchase register", "view purchase register"],
        "description": "Purchase register report"
    },
    
    # Reports - GST
    "gstr1_report": {
        "path": "/reports/gst/gstr1",
        "name": "Gstr1Report",
        "keywords": ["gstr1", "gstr-1", "gst r1", "gstr1 report"],
        "description": "GSTR1 report"
    },
    "gstr2_report": {
        "path": "/reports/gst/gstr2r",
        "name": "Gstr2Report",
        "keywords": ["gstr2", "gstr-2", "gst r2", "gstr2 report"],
        "description": "GSTR2 report"
    },
    "gstr3b_report": {
        "path": "/reports/gst/gstr3b",
        "name": "Gstr3bReport",
        "keywords": ["gstr3b", "gstr-3b", "gst r3b", "gstr3b report"],
        "description": "GSTR3B report"
    },
    
    # Stock Management
    "physical_stock_form": {
        "path": "/stock/physical-stock",
        "name": "PhysicalStockForm",
        "keywords": ["physical stock", "add physical stock", "stock entry"],
        "description": "Physical stock form"
    },
    "stock_reconciliation_list": {
        "path": "/stock-reconciliation",
        "name": "StockReconciliationList",
        "keywords": ["stock reconciliation", "reconciliation list", "view reconciliation"],
        "description": "Stock reconciliation list"
    },
    "stock_reconciliation_new": {
        "path": "/stock-reconciliation/new",
        "name": "StockReconciliationForm",
        "keywords": ["add stock reconciliation", "new stock reconciliation", "create reconciliation"],
        "description": "Create new stock reconciliation"
    }
}

# Category mappings for better context understanding
CATEGORIES = {
    "company": ["company", "companies", "organization"],
    "ledger": ["ledger", "account", "accounts"],
    "item": ["item", "product", "stock", "inventory"],
    "tax": ["tax", "taxes", "gst", "vat"],
    "transaction": ["transaction", "voucher", "entry"],
    "sale": ["sale", "sales", "selling"],
    "purchase": ["purchase", "buying"],
    "payment": ["payment", "pay", "paid"],
    "receipt": ["receipt", "receive", "received"],
    "report": ["report", "view", "show", "display"],
    "journal": ["journal", "journal entry"],
}
