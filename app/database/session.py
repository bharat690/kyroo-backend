# app/database/session.py
# This file is no longer used - we use Supabase now
# Kept for backwards compatibility but does nothing

from app.database.supabase_client import get_supabase

# Alias for any code that might still reference this
SessionLocal = None
engine = None