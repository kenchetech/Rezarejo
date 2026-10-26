from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import endpoints, mpesa_routes, compliance_and_fleet

app = FastAPI(
    title="Rezarejo Circular Economy & Traceability ERP",
    description="Powered by Pamarsons Technology (rezarejo.pamarsonstech.co.ke)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rezarejo.pamarsonstech.co.ke", "https://pamarsonstech.co.ke"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)
app.include_router(mpesa_routes.router)
app.include_router(compliance_and_fleet.router)

@app.get('/health', tags=['System Health'])
async def health_check():
    return {'status': 'ONLINE', 'platform': 'Rezarejo ERP', 'domain': 'rezarejo.pamarsonstech.co.ke'}
