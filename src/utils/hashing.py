"""
Utility functions for hashing and anonymisation.
"""
import hashlib

def hash_user_id(uid: str) -> str:
    """Return a SHA-256 hash of the user ID as a hex string."""
    return hashlib.sha256(uid.encode("utf-8")).hexdigest()
