from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from uuid import UUID
import ollama
import json
import re

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from services.postgres_service import (
    company_service, ledger_service, transaction_service, product_service,
    tax_service, financial_year_service, user_company_service
)

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
    endpoint_called: str
    data: Any
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
async def smart_search(request: SmartSearchRequest, session: AsyncSession = Depends(get_async_session)):
    """
    Analyze natural language query using Ollama and route to appropriate API endpoint.
    
    Examples:
    - "Show me all companies" → calls /api/companies
    - "Get ledger with id abc-123" → calls /api/ledgers/{ledger_id}
    - "List all products for company xyz" → calls /api/companies/{company_id}/products
    """
    try:
        # Send query to Ollama for analysis
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
            raise HTTPException(status_code=400, detail="Could not parse AI response")
        
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
            raise HTTPException(
                status_code=400, 
                detail=f"Could not determine appropriate endpoint for query: '{request.query}'. Please try rephrasing."
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
            endpoint_called=endpoint_called,
            data=data,
            explanation=explanation
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
