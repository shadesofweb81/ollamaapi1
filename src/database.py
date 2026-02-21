from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL, DATABASE_URL_SYNC

# Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync engine (for scripts or sync operations)
sync_engine = create_engine(DATABASE_URL_SYNC, echo=True)
SyncSessionLocal = sessionmaker(bind=sync_engine)

async def get_async_session() -> AsyncSession:
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_session() -> Session:
    """Get sync database session"""
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()
