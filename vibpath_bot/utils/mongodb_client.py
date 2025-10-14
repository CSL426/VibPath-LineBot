"""
MongoDB Client for VibPath LINE Bot
Manages user preferences including AI reply toggle
"""
from datetime import datetime, timezone
from typing import Optional
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError
from vibpath_bot.config.env_config import settings
from vibpath_bot.utils.logger import db_logger as logger
from vibpath_bot.utils.exceptions import MongoDBConnectionError, UserPreferenceError


class MongoDBClient:
    """MongoDB client for managing user preferences"""

    def __init__(self):
        """Initialize MongoDB client"""
        self.mongo_uri = settings.get_mongodb_uri()

        if self.mongo_uri:
            logger.info("MongoDB URI configured")
        else:
            logger.warning("MongoDB not configured. AI toggle feature will be disabled.")

        self.client = None
        self.db = None
        self.user_preferences = None

        if self.mongo_uri:
            self._connect()

    def _connect(self):
        """Establish connection to MongoDB with connection pool"""
        try:
            self.client = MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,  # Connection pool size
                minPoolSize=10,
                maxIdleTimeMS=45000,  # 45 seconds idle cleanup
                retryWrites=True,
                retryReads=True
            )
            # Test connection
            self.client.server_info()

            # Get database and collection
            self.db = self.client.get_database(settings.mongodb_database)
            self.user_preferences = self.db.get_collection("user_preferences")

            # Create index on userId for faster queries
            self.user_preferences.create_index([("userId", ASCENDING)], unique=True)

            logger.info("MongoDB connected successfully with connection pool")
        except PyMongoError as e:
            logger.error(f"MongoDB connection failed: {e}", exc_info=True)
            self.client = None
            # Don't raise exception - allow app to start without MongoDB
            logger.warning("Application will continue without MongoDB (AI toggle feature disabled)")

    def is_connected(self) -> bool:
        """Check if MongoDB is connected"""
        return self.client is not None

    def get_ai_reply_status(self, user_id: str) -> bool:
        """
        Get AI reply enabled status for a user

        Args:
            user_id: LINE user ID

        Returns:
            bool: True if AI reply is enabled, False otherwise
            Default: True (AI enabled) if user not found
        """
        if not self.is_connected():
            return True  # Default to enabled if DB not available

        try:
            user_pref = self.user_preferences.find_one({"userId": user_id})

            if user_pref is None:
                # User not found, default to AI enabled
                return True

            return user_pref.get("aiReplyEnabled", True)

        except PyMongoError as e:
            logger.error(f"Error getting AI reply status for {user_id}: {e}", exc_info=True)
            return True  # Default to enabled on error

    def set_ai_reply_status(self, user_id: str, enabled: bool) -> bool:
        """
        Set AI reply enabled status for a user

        Args:
            user_id: LINE user ID
            enabled: True to enable AI reply, False to disable

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            logger.warning("MongoDB not connected. Cannot update AI status.")
            return False

        try:
            now = datetime.now(timezone.utc)

            result = self.user_preferences.update_one(
                {"userId": user_id},
                {
                    "$set": {
                        "aiReplyEnabled": enabled,
                        "lastUpdated": now
                    }
                },
                upsert=True
            )

            status = "enabled" if enabled else "disabled"
            logger.info(f"AI reply {status} for user {user_id}")
            return True

        except PyMongoError as e:
            logger.error(f"Error setting AI reply status for {user_id}: {e}", exc_info=True)
            raise UserPreferenceError(f"Failed to set AI reply status", detail=str(e))

    def toggle_ai_reply(self, user_id: str) -> bool:
        """
        Toggle AI reply status for a user

        Args:
            user_id: LINE user ID

        Returns:
            bool: New AI reply status (True=enabled, False=disabled)
        """
        current_status = self.get_ai_reply_status(user_id)
        new_status = not current_status
        self.set_ai_reply_status(user_id, new_status)
        return new_status

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global MongoDB client instance
mongodb_client = MongoDBClient()
