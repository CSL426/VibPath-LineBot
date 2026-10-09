"""
Admin configuration and pause management for VibPath LINE Bot.
"""
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo
import re
import os


class AdminConfig:
    """Manages admin users and bot pause state"""

    def __init__(self):
        # Load admin user IDs from environment variable
        # Support multiple separators: : (colon), | (pipe), or , (comma)
        admin_ids_str = os.getenv("ADMIN_USER_IDS", "")
        if ":" in admin_ids_str:
            separator = ":"
        elif "|" in admin_ids_str:
            separator = "|"
        else:
            separator = ","
        self.admin_users = set(
            uid.strip() for uid in admin_ids_str.split(separator) if uid.strip()
        )

        if self.admin_users:
            print(f"Loaded {len(self.admin_users)} admin user(s)")
        else:
            print("Warning: No admin users configured")

        # Timezone configuration
        self.timezone = ZoneInfo(os.getenv("TIMEZONE", "Asia/Taipei"))

        # Pause state
        self.is_paused = False
        self.pause_until: Optional[datetime] = None
        self.paused_by: Optional[str] = None

    def is_admin(self, user_id: str) -> bool:
        """Check if user is admin"""
        return user_id in self.admin_users

    def pause_bot(self, duration_minutes: int = 60, admin_id: str = None):
        """
        Pause bot responses for specified duration.

        Args:
            duration_minutes: Duration in minutes (default 60 = 1 hour)
            admin_id: Admin user ID who initiated pause
        """
        self.is_paused = True
        self.pause_until = datetime.now(self.timezone) + timedelta(minutes=duration_minutes)
        self.paused_by = admin_id
        print(f"Bot paused by {admin_id} until {self.pause_until}")

    def resume_bot(self, admin_id: str = None):
        """Resume bot responses"""
        self.is_paused = False
        self.pause_until = None
        print(f"Bot resumed by {admin_id}")

    def check_pause_status(self) -> bool:
        """
        Check if bot is currently paused.
        Auto-resume if pause duration expired.

        Returns:
            bool: True if paused, False if active
        """
        if not self.is_paused:
            return False

        # Check if pause duration has expired
        if self.pause_until and datetime.now(self.timezone) >= self.pause_until:
            print(f"Pause duration expired, auto-resuming bot")
            self.is_paused = False
            self.pause_until = None
            self.paused_by = None
            return False

        return True

    def get_pause_info(self) -> dict:
        """Get current pause status information"""
        if not self.is_paused:
            return {"paused": False}

        remaining = None
        if self.pause_until:
            remaining_delta = self.pause_until - datetime.now(self.timezone)
            remaining = int(remaining_delta.total_seconds() / 60)

        return {
            "paused": True,
            "pause_until": self.pause_until.strftime("%Y-%m-%d %H:%M:%S") if self.pause_until else None,
            "remaining_minutes": remaining,
            "paused_by": self.paused_by
        }

    # Matches a pause duration such as 30分鐘 / 15m / 2小時 / 2hr
    _DURATION_RE = re.compile(r'(\d+)\s*(分鐘?|mins?|m(?!in)|小時?|hours?|hrs?|h(?!our|r))')
    _PAUSE_RE = re.compile(r'暫停\s*(\d+\s*(分鐘?|mins?|m|小時?|hours?|hrs?|h))?')
    _RESUME_KEYWORDS = {'恢復', '繼續', '啟動', 'resume', 'start'}
    _STATUS_KEYWORDS = {'狀態', 'status'}
    _HELP_KEYWORDS = {'指令', 'commands', 'admin'}

    def match_exact_command(self, text: str) -> Optional[str]:
        """Return command when the whole message is a command keyword."""
        text = text.strip().lower()
        if self._PAUSE_RE.fullmatch(text):
            return "pause"
        if text in self._RESUME_KEYWORDS:
            return "resume"
        if text in self._STATUS_KEYWORDS:
            return "status"
        if text in self._HELP_KEYWORDS:
            return "help"
        return None

    async def classify_command(self, text: str) -> Optional[str]:
        """
        Classify an admin message: exact keyword first, then the decision model.

        Returns:
            'pause' / 'resume' / 'status' / 'help', or None if it is not a command
            (including when the decision API is unavailable or not confident enough)
        """
        exact = self.match_exact_command(text)
        if exact:
            return exact

        # Import here to avoid circular import (decision_service imports env_config)
        from ..services.decision_service import decision_service
        from .env_config import settings

        result = await decision_service.classify_admin_command(text)
        if result is None:
            return None
        command, confidence = result
        if command == "none" or confidence < settings.decision_action_min_confidence:
            return None
        return command

    def parse_pause_duration(self, text: str) -> int:
        """
        Parse pause duration in minutes from command text (default 60).

        Args:
            text: Command text, e.g. 暫停30分鐘 / 先停兩小時 / 暫停2h
        """
        match = self._DURATION_RE.search(text.strip().lower())
        if not match:
            return 60
        duration, unit = int(match.group(1)), match.group(2)
        return duration * 60 if unit.startswith(('小', 'h')) else duration

    def get_admin_help_message(self) -> str:
        """Get admin help message"""
        return """👤 管理員指令說明

⏸️ 暫停 Bot
• 暫停 → 暫停 1 小時
• 暫停15分鐘 / 暫停15m / 暫停15min
• 暫停2小時 / 暫停2h / 暫停2hr

▶️ 恢復運作
• 恢復 / 繼續 / resume

📊 查看狀態
• 狀態 / status

💡 顯示說明
• 指令 / commands / admin"""


# Global admin config instance
admin_config = AdminConfig()
