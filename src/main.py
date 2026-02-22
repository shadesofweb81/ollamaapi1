from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from uuid import UUID
import ollama
import json
import re
import jwt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from services.postgres_service import (
    company_service, ledger_service, transaction_service, product_service,
    tax_service, financial_year_service, user_company_service
)
from routes_config import ROUTE_MAPPINGS

# JWT helper - extracts jti (user ID) from Bearer token
def extract_jti_from_token(authorization: str) -> str:
    """
    Extract the 'jti' claim from a Bearer JWT token.
    jti is used as the UserId stored in the UserCompanies table.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header. Expected: Bearer <token>"
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        logger.info(f"JWT payload claims: {list(payload.keys())}")

        jti = payload.get("jti")
        if not jti:
            raise HTTPException(
                status_code=401,
                detail=f"Token does not contain a 'jti' claim. Available claims: {list(payload.keys())}"
            )

        logger.info(f"Extracted jti (user_id): {jti}")
        return str(jti)
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token - cannot be decoded")

# Configure Ollama client
ollama_client = ollama.Client(host='http://localhost:11434')

app = FastAPI(
    title="FastAPI Ollama API",
    description="API for interacting with Ollama and PostgreSQL Database",
    version="1.0.0"
)

# Pydantic models for Ollama
class QueryRequest(BaseModel):
    query: str
    model: str = "gemma3:1b"

class QueryResponse(BaseModel):
    response: str
    model: str

# Smart Search Request/Response models
class SmartSearchRequest(BaseModel):
    query: str
    company_id: Optional[UUID] = None
    model: str = "gemma3:1b"

class SmartSearchResponse(BaseModel):
    query: str
    search_type: str  # "navigation", "data", or "unknown"
    endpoint_called: Optional[str] = None
    data: Optional[Any] = None
    route_path: Optional[str] = None
    route_name: Optional[str] = None
    description: Optional[str] = None
    confidence: Optional[str] = None
    explanation: str

# Route Navigation models
class RouteNavigationRequest(BaseModel):
    query: str
    model: str = "gemma3:1b"

class RouteNavigationResponse(BaseModel):
    query: str
    route_name: str
    route_path: str
    description: str
    confidence: str
    explanation: str

# System prompt for Ollama to analyze queries
ENDPOINT_ANALYSIS_PROMPT = """You are an API routing assistant. Analyze the user's natural language query and determine which API endpoint to call.

Available endpoints:
1. GET /api/companies - List all companies
2. GET /api/companies/{company_id} - Get a specific company by ID
3. GET /api/companies/{company_id}/ledgers - Get all ledgers for a company
4. GET /api/ledgers/{ledger_id} - Get a specific ledger by ID
5. GET /api/companies/{company_id}/products - Get all products for a company
6. GET /api/products/{product_id} - Get a specific product by ID
7. GET /api/companies/{company_id}/transactions - Get all transactions for a company
8. GET /api/transactions/{transaction_id} - Get a specific transaction by ID

Respond ONLY with a JSON object in this exact format (no other text):
{
    "endpoint": "endpoint_name",
    "params": {"param_name": "value"},
    "explanation": "brief explanation of why this endpoint was chosen"
}

Where endpoint_name is one of:
- "list_companies"
- "get_company" (requires company_id)
- "list_ledgers" (requires company_id)
- "get_ledger" (requires ledger_id)
- "list_products" (requires company_id)
- "get_product" (requires product_id)
- "list_transactions" (requires company_id)
- "get_transaction" (requires transaction_id)
- "unknown" (if query doesn't match any endpoint)

Extract any IDs mentioned in the query. If a company_id is needed but not provided in the query, use "NEEDS_COMPANY_ID" as placeholder.

User query: """

# Intent Classification prompt - decides if user wants navigation or data search
INTENT_CLASSIFICATION_PROMPT = """You are an intent classifier for an accounting/ERP application. Analyze the user's query and determine if they want to:
1. Navigate to a page/form (to add, create, view, or access a specific page)
2. Search for data (to retrieve, find, or query database records)

Respond ONLY with a JSON object in this exact format (no other text):
{
    "intent": "navigation|data_search",
    "reasoning": "brief explanation of why you chose this intent"
}

Guidelines:
- "navigation" intent: User wants to go to a page, form, or report
  Examples: "add ledger", "new sale invoice", "open company page", "daybook report", "create product"
  
- "data_search" intent: User wants to retrieve or find database records
  Examples: "find companies", "search items", "get all ledgers", "show products", "list transactions"

Key differences:
- Navigation uses action words like: add, new, create, open, go to, show form, + page names/reports
- Data search uses query words like: find, search, get, show records, list data, fetch

User query: """

# Route Navigation prompt for frontend routing
ROUTE_NAVIGATION_PROMPT = """You are a navigation assistant for an accounting/ERP application. Analyze the user's command and determine which page they want to navigate to.

The user can perform actions like:
- Adding/Creating new records (e.g., "add ledger", "new sale invoice", "create company")
- Viewing/Listing records (e.g., "view ledgers", "show sales invoices", "list companies")
- Editing records (requires ID, e.g., "edit ledger", "update company")
- Viewing reports (e.g., "daybook report", "gstr1", "sales register")
- Managing system features (e.g., "import data", "export data", "select company")

Respond ONLY with a JSON object in this exact format (no other text):
{
    "route_key": "route_identifier",
    "confidence": "high|medium|low",
    "explanation": "brief explanation of the match"
}

Available route identifiers and their purposes:
- home: Dashboard/home page
- search: Search functionality
- company_list: List all companies
- company_add: Add new company
- financial_year_list: List financial years
- financial_year_add: Add financial year
- ledger_list: List all ledgers/accounts
- ledger_add: Add new ledger/account
- item_list: List all items/products
- item_add: Add new item/product
- tax_list: List all taxes
- tax_add: Add new tax
- sales_invoice_list: List sales invoices
- new_sale_invoice: Create new sales invoice
- new_sale_order: Create new sales order
- new_sale_quotation: Create new sales quotation
- new_sale_return: Create new sales return
- purchase_invoice_list: List purchase invoices
- new_purchase_bill: Create new purchase bill
- new_purchase_order: Create new purchase order
- new_purchase_quotation: Create new purchase quotation
- new_purchase_return: Create new purchase return
- new_cash_payment: Create cash payment
- new_bank_payment: Create bank payment
- new_cash_receipt: Create cash receipt
- new_bank_receipt: Create bank receipt
- new_journal_entry: Create journal entry
- ledger_report: Ledger report
- stock_ledger_report: Stock/inventory report
- daybook_report: Daybook report
- sales_register: Sales register report
- purchase_register: Purchase register report
- gstr1_report: GSTR1 GST report
- gstr2_report: GSTR2 GST report
- gstr3b_report: GSTR3B GST report
- stock_reconciliation_list: Stock reconciliation list
- stock_reconciliation_new: Add new stock reconciliation
- import_data: Import data
- export_data: Export data
- select_company: Select/switch company

Analyze the user's intent:
- Action words like "add", "new", "create" → navigation to add/create forms
- Action words like "view", "show", "list", "display" → navigation to list pages
- Report names like "daybook", "gstr1", "sales register" → navigation to report pages

If the query doesn't match any route, use "home" as fallback with "low" confidence.

User query: """

# Pydantic models for database responses
class CompanyResponse(BaseModel):
    id: UUID
    name: str
    email: str
    city: Optional[str] = None
    state: str
    country: str
    currency: str
    
    class Config:
        from_attributes = True

class LedgerResponse(BaseModel):
    id: UUID
    name: str
    type: Optional[str] = None
    code: Optional[str] = None
    is_group: bool
    
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: UUID
    name: str
    product_code: str
    purchase_price: float
    selling_price: float
    stock_quantity: int
    is_active: bool
    
    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: UUID
    transaction_number: str
    invoice_number: Optional[str] = None
    total: float
    is_paid: bool
    
    class Config:
        from_attributes = True

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI Ollama API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/debug/token")
async def debug_token(http_request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Debug endpoint: decodes the JWT and shows the extracted user_id and
    which companies that user has in the UserCompanies table.
    Remove or protect this endpoint before going to production.
    """
    authorization = http_request.headers.get("Authorization") or http_request.headers.get("authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return {"error": "No Bearer token provided"}

    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except jwt.DecodeError:
        return {"error": "Cannot decode token"}

    jti = payload.get("jti")

    # Fetch all UserCompany rows for this jti
    from sqlalchemy import select as sa_select
    from models.user_company import UserCompany
    rows = []
    if jti:
        result = await session.execute(
            sa_select(UserCompany).where(UserCompany.user_id == str(jti))
        )
        uc_list = result.scalars().all()
        rows = [{"user_id_in_db": uc.user_id, "company_id": str(uc.company_id), "role": uc.role} for uc in uc_list]

    return {
        "jti": jti,
        "user_companies_in_db": rows,
        "all_jwt_claims": {k: v for k, v in payload.items()},
        "tip": "'jti' from the token is matched against UserId in UserCompanies table"
    }

@app.post("/generate", response_model=QueryResponse)
async def generate_response(request: QueryRequest):
    """Generate response from Ollama model"""
    try:
        response = ollama_client.generate(
            model=request.model,
            prompt=request.query
        )
        return QueryResponse(
            response=response['response'],
            model=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

# Database Endpoints - Companies
@app.get("/api/companies", response_model=List[CompanyResponse])
async def get_companies(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    """Get all companies"""
    companies = await company_service.get_all(session, skip=skip, limit=limit)
    return companies

@app.get("/api/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Get a company by ID"""
    company = await company_service.get_by_id(session, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# Database Endpoints - Ledgers
@app.get("/api/companies/{company_id}/ledgers", response_model=List[LedgerResponse])
async def get_ledgers(company_id: UUID, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    """Get all ledgers for a company"""
    ledgers = await ledger_service.get_by_company_id(session, company_id, skip=skip, limit=limit)
    return ledgers

@app.get("/api/ledgers/{ledger_id}", response_model=LedgerResponse)
async def get_ledger(ledger_id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Get a ledger by ID"""
    ledger = await ledger_service.get_by_id(session, ledger_id)
    if not ledger:
        raise HTTPException(status_code=404, detail="Ledger not found")
    return ledger

# Database Endpoints - Products
@app.get("/api/companies/{company_id}/products", response_model=List[ProductResponse])
async def get_products(company_id: UUID, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    """Get all products for a company"""
    products = await product_service.get_by_company_id(session, company_id, skip=skip, limit=limit)
    return products

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Get a product by ID"""
    product = await product_service.get_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Database Endpoints - Transactions
@app.get("/api/companies/{company_id}/transactions", response_model=List[TransactionResponse])
async def get_transactions(company_id: UUID, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    """Get all transactions for a company"""
    transactions = await transaction_service.get_by_company_id(session, company_id, skip=skip, limit=limit)
    return transactions

@app.get("/api/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: UUID, session: AsyncSession = Depends(get_async_session)):
    """Get a transaction by ID"""
    transaction = await transaction_service.get_by_id(session, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Smart Search Endpoint - Natural Language Query Routing
@app.post("/api/search", response_model=SmartSearchResponse)
async def smart_search(request: SmartSearchRequest, http_request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Unified smart search endpoint where AI decides the intent:
    1. Navigation intent - returns route URLs for pages/forms
    2. Data search intent - returns database records
    
    The AI (gemma3:1b) analyzes the query and determines which endpoint logic to use.
    
    Examples:
    Navigation Intent:
    - "add ledger" → returns route path /ledgers/add
    - "new sale invoice" → returns route path /transactions/new/sale-invoice
    - "daybook report" → returns route path /reports/daybook
    
    Data Search Intent:
    - "find all companies" → returns company records from database
    - "search items" → returns product records
    - "show ledgers" → returns ledger records
    """
    try:
        # Step 0: Extract jti from JWT and verify user has access to the requested company
        # --- JWT VALIDATION TEMPORARILY COMMENTED OUT FOR TESTING ---
        # authorization = http_request.headers.get("Authorization") or http_request.headers.get("authorization")
        # jti = extract_jti_from_token(authorization)

        # if not request.company_id:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="company_id is required in the request body"
        #     )

        # # Query UserCompanies WHERE UserId = jti AND CompanyId = company_id
        # logger.info(f"Checking access: jti='{jti}' company_id='{request.company_id}'")
        # user_company = await user_company_service.get_by_user_and_company(
        #     session, jti, request.company_id
        # )
        # if not user_company:
        #     logger.warning(f"Access denied: jti='{jti}' not found for company_id='{request.company_id}'")
        #     raise HTTPException(
        #         status_code=403,
        #         detail=f"Access denied: user '{jti}' does not have access to company '{request.company_id}'."
        #     )
        logger.info(f"/api/search endpoint hit - JWT validation skipped for testing. query='{request.query}'")

        # Step 1: Ask AI to classify the intent
        intent_prompt = INTENT_CLASSIFICATION_PROMPT + request.query
        
        intent_response = ollama_client.generate(
            model=request.model,
            prompt=intent_prompt
        )
        
        intent_text = intent_response['response'].strip()
        
        # Parse AI intent classification
        intent_json_match = re.search(r'\{[\s\S]*\}', intent_text)
        
        if intent_json_match:
            try:
                intent_data = json.loads(intent_json_match.group())
                classified_intent = intent_data.get("intent", "data_search")
                reasoning = intent_data.get("reasoning", "")
            except json.JSONDecodeError:
                # Default to data search if can't parse
                classified_intent = "data_search"
                reasoning = "Defaulted to data search - could not parse AI response"
        else:
            # Default to data search if no JSON found
            classified_intent = "data_search"
            reasoning = "Defaulted to data search - no JSON response from AI"
        
        # Step 2: Route based on AI's intent classification
        
        if classified_intent == "navigation":
            # AI determined this is a navigation request
            # Try AI-powered route matching
            try:
                prompt = ROUTE_NAVIGATION_PROMPT + request.query
                response = ollama_client.generate(
                    model=request.model,
                    prompt=prompt
                )
                
                response_text = response['response'].strip()
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                
                if json_match:
                    parsed_response = json.loads(json_match.group())
                    route_key = parsed_response.get("route_key", "home")
                    confidence = parsed_response.get("confidence", "medium")
                    ai_explanation = parsed_response.get("explanation", "")
                    
                    if route_key in ROUTE_MAPPINGS:
                        route_data = ROUTE_MAPPINGS[route_key]
                        return SmartSearchResponse(
                            query=request.query,
                            search_type="navigation",
                            route_path=route_data["path"],
                            route_name=route_data["name"],
                            description=route_data["description"],
                            confidence=confidence,
                            explanation=f"AI Intent: {reasoning}. {ai_explanation}"
                        )
            except:
                pass  # Fall through to keyword matching
            
            # Fallback to keyword-based route matching
            route_match = _fallback_route_matching(request.query)
            return SmartSearchResponse(
                query=request.query,
                search_type="navigation",
                route_path=route_match.route_path,
                route_name=route_match.route_name,
                description=route_match.description,
                confidence=route_match.confidence,
                explanation=f"AI Intent: {reasoning}. {route_match.explanation}"
            )
        
        else:
            # AI determined this is a data search request
            # Send query to Ollama for endpoint analysis
            prompt = ENDPOINT_ANALYSIS_PROMPT + request.query
            
            response = ollama_client.generate(
                model=request.model,
                prompt=prompt
            )
            
            # Parse the Ollama response
            response_text = response['response'].strip()
            
            # Extract JSON from response (handle potential extra text)
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if not json_match:
                return SmartSearchResponse(
                    query=request.query,
                    search_type="unknown",
                    explanation=(
                        f"Sorry, I couldn't understand '{request.query}'. "
                        "Try something like 'add ledger', 'new sale invoice', 'show products', or 'daybook report'."
                    )
                )
            
            parsed_response = json.loads(json_match.group())
            endpoint = parsed_response.get("endpoint", "unknown")
            params = parsed_response.get("params", {})
            explanation = parsed_response.get("explanation", "")
            
            # Use company_id from request if provided and needed
            if request.company_id and params.get("company_id") == "NEEDS_COMPANY_ID":
                params["company_id"] = str(request.company_id)
            
            # Route to appropriate endpoint based on analysis
            data = None
            endpoint_called = ""
            
            if endpoint == "list_companies":
                data = await company_service.get_all(session, skip=0, limit=100)
                endpoint_called = "/api/companies"
                
            elif endpoint == "get_company":
                company_id = params.get("company_id")
                if not company_id or company_id == "NEEDS_COMPANY_ID":
                    raise HTTPException(status_code=400, detail="Company ID is required for this query")
                data = await company_service.get_by_id(session, UUID(company_id))
                endpoint_called = f"/api/companies/{company_id}"
                if not data:
                    raise HTTPException(status_code=404, detail="Company not found")
                    
            elif endpoint == "list_ledgers":
                company_id = params.get("company_id")
                if not company_id or company_id == "NEEDS_COMPANY_ID":
                    raise HTTPException(status_code=400, detail="Company ID is required for this query. Please provide company_id in the request.")
                data = await ledger_service.get_by_company_id(session, UUID(company_id), skip=0, limit=100)
                endpoint_called = f"/api/companies/{company_id}/ledgers"
                
            elif endpoint == "get_ledger":
                ledger_id = params.get("ledger_id")
                if not ledger_id:
                    raise HTTPException(status_code=400, detail="Ledger ID is required for this query")
                data = await ledger_service.get_by_id(session, UUID(ledger_id))
                endpoint_called = f"/api/ledgers/{ledger_id}"
                if not data:
                    raise HTTPException(status_code=404, detail="Ledger not found")
                    
            elif endpoint == "list_products":
                company_id = params.get("company_id")
                if not company_id or company_id == "NEEDS_COMPANY_ID":
                    raise HTTPException(status_code=400, detail="Company ID is required for this query. Please provide company_id in the request.")
                data = await product_service.get_by_company_id(session, UUID(company_id), skip=0, limit=100)
                endpoint_called = f"/api/companies/{company_id}/products"
                
            elif endpoint == "get_product":
                product_id = params.get("product_id")
                if not product_id:
                    raise HTTPException(status_code=400, detail="Product ID is required for this query")
                data = await product_service.get_by_id(session, UUID(product_id))
                endpoint_called = f"/api/products/{product_id}"
                if not data:
                    raise HTTPException(status_code=404, detail="Product not found")
                    
            elif endpoint == "list_transactions":
                company_id = params.get("company_id")
                if not company_id or company_id == "NEEDS_COMPANY_ID":
                    raise HTTPException(status_code=400, detail="Company ID is required for this query. Please provide company_id in the request.")
                data = await transaction_service.get_by_company_id(session, UUID(company_id), skip=0, limit=100)
                endpoint_called = f"/api/companies/{company_id}/transactions"
                
            elif endpoint == "get_transaction":
                transaction_id = params.get("transaction_id")
                if not transaction_id:
                    raise HTTPException(status_code=400, detail="Transaction ID is required for this query")
                data = await transaction_service.get_by_id(session, UUID(transaction_id))
                endpoint_called = f"/api/transactions/{transaction_id}"
                if not data:
                    raise HTTPException(status_code=404, detail="Transaction not found")
                    
            else:
                # Unknown / gibberish query - return friendly response instead of error
                return SmartSearchResponse(
                    query=request.query,
                    search_type="unknown",
                    explanation=(
                        f"Sorry, I couldn't understand '{request.query}'. "
                        "Try something like 'add ledger', 'new sale invoice', 'show products', or 'daybook report'."
                    )
                )
            
            # Convert SQLAlchemy models to dict for JSON response
            if isinstance(data, list):
                data = [item.__dict__ if hasattr(item, '__dict__') else item for item in data]
                # Remove SQLAlchemy internal state
                for item in data:
                    if isinstance(item, dict):
                        item.pop('_sa_instance_state', None)
            elif hasattr(data, '__dict__'):
                data = {k: v for k, v in data.__dict__.items() if k != '_sa_instance_state'}
            
            return SmartSearchResponse(
                query=request.query,
                search_type="data",
                endpoint_called=endpoint_called,
                data=data,
                explanation=f"AI Intent: {reasoning}. {explanation}"
            )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Route Navigation Endpoint - Natural Language to Frontend Route
@app.post("/api/navigate", response_model=RouteNavigationResponse)
async def navigate_by_command(request: RouteNavigationRequest):
    """
    Analyze natural language command using Ollama and return the appropriate frontend route.
    
    Examples:
    - "add ledger" → returns /ledgers/add
    - "new sale invoice" → returns /transactions/new/sale-invoice
    - "view companies" → returns /companies
    - "daybook report" → returns /reports/daybook
    - "create journal entry" → returns /transactions/journal-entry/new
    """
    try:
        # Prepare route context for better matching
        route_context = "\n".join([
            f"- {key}: {data['description']} (keywords: {', '.join(data['keywords'])})"
            for key, data in ROUTE_MAPPINGS.items()
        ])
        
        # Send query to Ollama for analysis
        prompt = ROUTE_NAVIGATION_PROMPT + request.query
        
        response = ollama_client.generate(
            model=request.model,
            prompt=prompt
        )
        
        # Parse the Ollama response
        response_text = response['response'].strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if not json_match:
            # Fallback to simple keyword matching
            return _fallback_route_matching(request.query)
        
        parsed_response = json.loads(json_match.group())
        route_key = parsed_response.get("route_key", "home")
        confidence = parsed_response.get("confidence", "low")
        explanation = parsed_response.get("explanation", "")
        
        # Get route details from mappings
        if route_key in ROUTE_MAPPINGS:
            route_data = ROUTE_MAPPINGS[route_key]
            return RouteNavigationResponse(
                query=request.query,
                route_name=route_data["name"],
                route_path=route_data["path"],
                description=route_data["description"],
                confidence=confidence,
                explanation=explanation
            )
        else:
            # Fallback to keyword matching
            return _fallback_route_matching(request.query)
            
    except json.JSONDecodeError:
        # Fallback to simple keyword matching if JSON parsing fails
        return _fallback_route_matching(request.query)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing navigation command: {str(e)}")

def _fallback_route_matching(query: str) -> RouteNavigationResponse:
    """
    Fallback route matching using simple keyword search when AI parsing fails.
    """
    query_lower = query.lower().strip()
    
    # Score each route based on keyword matching
    best_match = None
    best_score = 0
    
    for route_key, route_data in ROUTE_MAPPINGS.items():
        score = 0
        
        # Check if any keyword matches
        for keyword in route_data["keywords"]:
            if keyword.lower() in query_lower:
                score += len(keyword.split())  # Multi-word keywords get higher score
        
        # Boost score if query contains action words matching the route type
        if any(word in query_lower for word in ["add", "new", "create"]) and "add" in route_key.lower():
            score += 2
        if any(word in query_lower for word in ["list", "view", "show"]) and "list" in route_key.lower():
            score += 2
        if "report" in query_lower and "report" in route_key.lower():
            score += 2
            
        if score > best_score:
            best_score = score
            best_match = (route_key, route_data)
    
    # If no match found or very low score, return home
    if not best_match or best_score == 0:
        home_data = ROUTE_MAPPINGS["home"]
        return RouteNavigationResponse(
            query=query,
            route_name=home_data["name"],
            route_path=home_data["path"],
            description=home_data["description"],
            confidence="low",
            explanation="No specific match found, returning home page"
        )
    
    route_key, route_data = best_match
    confidence = "high" if best_score >= 3 else "medium" if best_score >= 2 else "low"
    
    return RouteNavigationResponse(
        query=query,
        route_name=route_data["name"],
        route_path=route_data["path"],
        description=route_data["description"],
        confidence=confidence,
        explanation=f"Matched based on keywords: {', '.join(route_data['keywords'][:3])}"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
