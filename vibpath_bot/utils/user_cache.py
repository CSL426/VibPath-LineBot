"""
User Preferences Cache with TTL (Time To Live)
Reduces MongoDB queries by caching frequently accessed user preferences
"""
import time
from typing import Optional, Dict
from threading import Lock


class UserPreferencesCache:
    """
    In-memory cache for user preferences with TTL support
    Thread-safe implementation
    """

    def __init__(self, ttl_seconds: int = 600):
        """
        Initialize cache

        Args:
            ttl_seconds: Time to live in seconds (default: 600 = 10 minutes)
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, dict] = {}
        self._lock = Lock()

    def get(self, user_id: str) -> Optional[bool]:
        """
        Get cached AI reply status for a user

        Args:
            user_id: LINE user ID

        Returns:
            bool: AI reply status if found and not expired, None otherwise
        """
        with self._lock:
            if user_id not in self._cache:
                return None

            cache_entry = self._cache[user_id]
            current_time = time.time()

            # Check if cache entry has expired
            if current_time - cache_entry["timestamp"] > self.ttl_seconds:
                # Cache expired, remove it
                del self._cache[user_id]
                return None

            return cache_entry["ai_reply_enabled"]

    def set(self, user_id: str, ai_reply_enabled: bool):
        """
        Set cached AI reply status for a user

        Args:
            user_id: LINE user ID
            ai_reply_enabled: AI reply status
        """
        with self._lock:
            self._cache[user_id] = {
                "ai_reply_enabled": ai_reply_enabled,
                "timestamp": time.time()
            }

    def invalidate(self, user_id: str):
        """
        Invalidate (remove) cache entry for a user
        Used when user changes their preference

        Args:
            user_id: LINE user ID
        """
        with self._lock:
            if user_id in self._cache:
                del self._cache[user_id]
                print(f"🗑️  Cache invalidated for user {user_id}")

    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
            print("🗑️  All cache cleared")

    def get_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            dict: Cache statistics including size and oldest entry age
        """
        with self._lock:
            if not self._cache:
                return {
                    "size": 0,
                    "oldest_entry_age_seconds": 0
                }

            current_time = time.time()
            oldest_timestamp = min(entry["timestamp"] for entry in self._cache.values())
            oldest_age = current_time - oldest_timestamp

            return {
                "size": len(self._cache),
                "oldest_entry_age_seconds": int(oldest_age)
            }

    def cleanup_expired(self):
        """
        Manually cleanup expired cache entries
        This is called automatically during get(), but can be called manually for maintenance
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                user_id
                for user_id, entry in self._cache.items()
                if current_time - entry["timestamp"] > self.ttl_seconds
            ]

            for user_id in expired_keys:
                del self._cache[user_id]

            if expired_keys:
                print(f"🗑️  Cleaned up {len(expired_keys)} expired cache entries")


# Global cache instance with 10 minutes TTL
user_preferences_cache = UserPreferencesCache(ttl_seconds=600)
