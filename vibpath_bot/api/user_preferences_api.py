"""
RESTful API Router for User Preferences Management
Handles CRUD operations for user preferences
"""
from fastapi import Request, HTTPException, APIRouter
from vibpath_bot.services.user_preference_service import user_preference_service
from vibpath_bot.utils.mongodb_client import mongodb_client
from vibpath_bot.utils.user_cache import user_preferences_cache

# Create router
router = APIRouter(prefix="/api/users", tags=["user-preferences"])


@router.get("/{user_id}/preferences")
async def get_user_preferences(user_id: str):
    """
    Get user preferences (AI reply status)

    GET /api/users/{user_id}/preferences
    """
    try:
        ai_reply_enabled = user_preference_service.is_ai_reply_enabled(user_id)

        return {
            "status": "success",
            "data": {
                "userId": user_id,
                "aiReplyEnabled": ai_reply_enabled
            }
        }
    except Exception as e:
        print(f"Error getting user preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get user preferences: {str(e)}")


@router.put("/{user_id}/preferences")
async def update_user_preferences(user_id: str, request: Request):
    """
    Update user preferences (AI reply status)

    PUT /api/users/{user_id}/preferences
    Body: {"aiReplyEnabled": true/false}
    """
    try:
        body = await request.json()
        ai_reply_enabled = body.get("aiReplyEnabled")

        if ai_reply_enabled is None:
            raise HTTPException(status_code=400, detail="aiReplyEnabled field is required")

        if not isinstance(ai_reply_enabled, bool):
            raise HTTPException(status_code=400, detail="aiReplyEnabled must be a boolean")

        success = user_preference_service.set_ai_reply_status(user_id, ai_reply_enabled)

        if success:
            return {
                "status": "success",
                "message": "User preferences updated successfully",
                "data": {
                    "userId": user_id,
                    "aiReplyEnabled": ai_reply_enabled
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update user preferences")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating user preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update user preferences: {str(e)}")


@router.delete("/{user_id}/preferences")
async def delete_user_preferences(user_id: str):
    """
    Delete user preferences (reset to default)

    DELETE /api/users/{user_id}/preferences
    """
    try:
        if mongodb_client.client:
            result = mongodb_client.user_preferences.delete_one({"userId": user_id})
            # Also clear from cache
            user_preferences_cache._cache.pop(user_id, None)

            return {
                "status": "success",
                "message": f"User preferences deleted (deleted {result.deleted_count} document)",
                "data": {
                    "userId": user_id,
                    "deletedCount": result.deleted_count
                }
            }
        else:
            raise HTTPException(status_code=503, detail="MongoDB not connected")

    except Exception as e:
        print(f"Error deleting user preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete user preferences: {str(e)}")


@router.get("")
async def list_all_users():
    """
    List all users with their preferences

    GET /api/users
    """
    try:
        if mongodb_client.client:
            users = list(mongodb_client.user_preferences.find({}, {"_id": 0}))

            return {
                "status": "success",
                "count": len(users),
                "data": users
            }
        else:
            raise HTTPException(status_code=503, detail="MongoDB not connected")

    except Exception as e:
        print(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list users: {str(e)}")
