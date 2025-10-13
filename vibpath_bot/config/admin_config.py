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

    def parse_pause_command(self, text: str) -> Optional[int]:
        """
        Parse pause duration from command text.

        Args:
            text: Command text

        Returns:
            int: Duration in minutes, or None if not a pause command
        """
        text = text.strip().lower()

        # Check if it's a pause command
        if not text.startswith('暫停'):
            return None

        # Default pause duration (1 hour)
        if text == '暫停':
            return 60

        # Parse duration with regex - support various formats
        patterns = [
            (r'暫停\s*(\d+)\s*分鐘?', 1),           # 分鐘/分
            (r'暫停\s*(\d+)\s*mins?', 1),           # min/mins
            (r'暫停\s*(\d+)\s*m(?!in)', 1),         # m (but not min)
            (r'暫停\s*(\d+)\s*小時?', 60),          # 小時/小
            (r'暫停\s*(\d+)\s*hours?', 60),         # hour/hours
            (r'暫停\s*(\d+)\s*hrs?', 60),           # hr/hrs
            (r'暫停\s*(\d+)\s*h(?!our|r)', 60),     # h (but not hour/hr)
        ]

        for pattern, multiplier in patterns:
            match = re.match(pattern, text)
            if match:
                duration = int(match.group(1))
                return duration * multiplier

        # If no pattern matches, return default
        return 60

    def parse_resume_command(self, text: str) -> bool:
        """
        Check if text is a resume command.

        Args:
            text: Command text

        Returns:
            bool: True if it's a resume command
        """
        text = text.strip().lower()
        resume_keywords = ['恢復', '繼續', '啟動', 'resume', 'start']
        return any(keyword in text for keyword in resume_keywords)

    def parse_help_command(self, text: str) -> bool:
        """
        Check if text is an admin help command.

        Args:
            text: Command text

        Returns:
            bool: True if it's a help command
        """
        text = text.strip().lower()
        help_keywords = ['指令', 'commands', 'admin']
        return any(keyword == text for keyword in help_keywords)

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
