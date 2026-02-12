"""aiosqlite connection management."""

import aiosqlite
from ..config import settings

_db: aiosqlite.Connection | None = None


async def get_db() -> aiosqlite.Connection:
    """Get the database connection, creating it if needed."""
    global _db
    if _db is None:
        _db = await aiosqlite.connect(settings.database_path)
        _db.row_factory = aiosqlite.Row
        await _db.execute("PRAGMA journal_mode=WAL")
        await _db.execute("PRAGMA foreign_keys=ON")
    return _db


async def close_db() -> None:
    """Close the database connection."""
    global _db
    if _db is not None:
        await _db.close()
        _db = None


async def init_db() -> None:
    """Initialize database: create tables if they don't exist."""
    from .tables import CREATE_TABLES
    db = await get_db()
    for sql in CREATE_TABLES:
        await db.execute(sql)
    await db.commit()
