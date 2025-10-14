"""
User Preference Service
Integrates MongoDB and in-memory cache for user preferences
"""
from vibpath_bot.utils.mongodb_client import mongodb_client
from vibpath_bot.utils.user_cache import user_preferences_cache


class UserPreferenceService:
    """Service for managing user preferences with caching"""

    @staticmethod
    def is_ai_reply_enabled(user_id: str) -> bool:
        """
        Check if AI reply is enabled for a user
        Uses database-first pattern: check MongoDB first, fallback to cache if DB unavailable

        Args:
            user_id: LINE user ID

        Returns:
            bool: True if AI reply enabled, False otherwise
            Default: True (enabled) if not found
        """
        # Check if MongoDB is connected
        if mongodb_client.is_connected():
            # Try MongoDB first
            print(f"🔌 MongoDB connected, querying for user {user_id}...")
            db_status = mongodb_client.get_ai_reply_status(user_id)

            # Update cache with fresh data from DB
            user_preferences_cache.set(user_id, db_status)
            print(f"✅ Got status from MongoDB for user {user_id}: AI={db_status}")

            return db_status
        else:
            # MongoDB not available, fallback to cache
            print(f"⚠️ MongoDB not connected, using cache for user {user_id}...")
            cached_status = user_preferences_cache.get(user_id)

            if cached_status is not None:
                print(f"🎯 Cache FALLBACK for user {user_id}: AI={cached_status}")
                return cached_status
            else:
                # No cache available either, return default
                print(f"⚠️ No cache available for user {user_id}, using default: AI=True")
                return True

    @staticmethod
    def set_ai_reply_status(user_id: str, enabled: bool) -> bool:
        """
        Set AI reply status for a user
        Updates both DB and cache

        Args:
            user_id: LINE user ID
            enabled: True to enable, False to disable

        Returns:
            bool: True if successful, False if failed
        """
        # Try to update MongoDB
        db_success = mongodb_client.set_ai_reply_status(user_id, enabled)

        if db_success:
            # Only update cache if DB write succeeded
            user_preferences_cache.set(user_id, enabled)
            print(f"✅ Updated both DB and cache for user {user_id}: AI={enabled}")
            return True
        else:
            # DB write failed - invalidate cache to force re-fetch from DB next time
            user_preferences_cache.invalidate(user_id)
            print(f"❌ MongoDB write failed for user {user_id} - cache invalidated")
            return False

    @staticmethod
    def toggle_ai_reply(user_id: str) -> bool:
        """
        Toggle AI reply status for a user

        Args:
            user_id: LINE user ID

        Returns:
            bool: New AI reply status (True=enabled, False=disabled)
        """
        # Get current status (will use cache if available)
        current_status = UserPreferenceService.is_ai_reply_enabled(user_id)

        # Toggle to opposite
        new_status = not current_status

        # Update both DB and cache
        UserPreferenceService.set_ai_reply_status(user_id, new_status)

        return new_status

    @staticmethod
    def get_cache_stats() -> dict:
        """
        Get cache statistics

        Returns:
            dict: Cache statistics
        """
        return user_preferences_cache.get_stats()

    @staticmethod
    def clear_cache():
        """Clear all cache entries"""
        user_preferences_cache.clear()


# Create service instance
user_preference_service = UserPreferenceService()
