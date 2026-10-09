"""
Decision model client for intent routing.
Calls a typed decision API and returns choice probabilities (no text generation).
"""
from typing import Optional, Tuple
import aiohttp
from ..config.env_config import settings
from ..utils.logger import webhook_logger as logger

# Option IDs match MessageHandler.detect_message_type return values
INTENT_CRITERIA = {
    "manual": "想要產品手冊、說明書、規格文件或操作手冊（下載文件）",
    "frequency": "想看有哪些產品、產品目錄、價格或怎麼購買",
    "business": "想了解 VibPath 這間公司、品牌、關於我們",
    "menu": "想叫出功能選單／服務選單",
    "help": "問這個聊天機器人怎麼使用、有哪些指令",
    "ai_on": "明確要求開啟「AI 自動回覆」這個功能",
    "ai_off": "明確要求關閉「AI 自動回覆」這個功能",
    "ai_status": "詢問「AI 自動回覆」功能目前開著還是關著",
    "general": "其他：具體的產品使用問題、閒聊、打招呼、問你是誰、要找真人客服、售後、客訴等，需要客服逐句回答",
}

ADMIN_CRITERIA = {
    "pause": "要求機器人暫停自動回覆（可能帶時間，如暫停30分鐘）",
    "resume": "要求機器人恢復／重新開始自動回覆",
    "status": "詢問機器人目前是否暫停中、運作狀態",
    "help": "詢問管理員有哪些指令可用",
    "none": "不是對機器人下指令：一般對話、轉述客人的話、問產品或機器的事",
}


class DecisionService:
    """Async client for the decision API"""

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def enabled(self) -> bool:
        return bool(settings.decision_api_url)

    def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=settings.decision_timeout_seconds)
            )
        return self._session

    async def classify_intent(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Classify user message intent.

        Returns:
            (intent, confidence), or None if the decision API is disabled or the call failed
        """
        return await self._choose(
            f"VibPath（極低頻電磁波／頻率產品）LINE 官方帳號客服。使用者傳來訊息：「{text}」",
            "這位使用者這則訊息，客服機器人應該走哪個分流？",
            INTENT_CRITERIA,
        )

    async def classify_admin_command(self, text: str) -> Optional[Tuple[str, float]]:
        """Classify an admin message as pause/resume/status/help/none."""
        return await self._choose(
            f"LINE bot 管理員傳來訊息：「{text}」",
            "這則訊息是不是對機器人下的管理指令？是哪一種？",
            ADMIN_CRITERIA,
        )

    async def _choose(self, state: str, instructions: str, criteria: dict) -> Optional[Tuple[str, float]]:
        """Ask one choice question; returns (choice, confidence) or None on failure."""
        if not self.enabled:
            return None

        payload = {
            "state": state,
            "questions": {
                "intent": {"type": "choice", "instructions": instructions, "criteria": criteria}
            },
        }
        if settings.decision_model:
            payload["model"] = settings.decision_model
        try:
            async with self._get_session().post(settings.decision_api_url, json=payload) as resp:
                resp.raise_for_status()
                body = await resp.json()
            answer = body["answers"]["intent"]
            return answer["choice"], float(answer["confidence"])
        except Exception as e:
            logger.warning(f"Decision API call failed: {e}")
            return None

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()


decision_service = DecisionService()
