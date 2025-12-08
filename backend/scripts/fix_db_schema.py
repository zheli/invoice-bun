
import asyncio
import os
from sqlalchemy import text
from app.db import engine

async def fix_schema():
    async with engine.begin() as conn:
        print("Checking for missing columns...")
        
        # Check if 'provider' column exists
        result = await conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'user' AND column_name = 'provider'"
        ))
        if not result.scalar():
            print("Adding 'provider' column...")
            await conn.execute(text('ALTER TABLE "user" ADD COLUMN provider VARCHAR'))
        else:
            print("'provider' column already exists.")

        # Check if 'provider_id' column exists
        result = await conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'user' AND column_name = 'provider_id'"
        ))
        if not result.scalar():
            print("Adding 'provider_id' column...")
            await conn.execute(text('ALTER TABLE "user" ADD COLUMN provider_id VARCHAR'))
        else:
            print("'provider_id' column already exists.")

    print("Schema fix complete.")

if __name__ == "__main__":
    # Ensure we can import app
    import sys
    sys.path.append(os.getcwd())
    
    asyncio.run(fix_schema())
