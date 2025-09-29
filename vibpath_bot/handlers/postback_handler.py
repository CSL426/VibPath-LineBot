"""
Postback event handler for LINE Bot.
Handles postback actions from buttons and manages explanation responses.
"""
import logging
from typing import Dict, Any, Optional
from linebot.models import TextSendMessage, FlexSendMessage, QuickReply

logger = logging.getLogger(__name__)


class PostbackHandler:
    """Handles postback events and explanation responses"""

    def __init__(self):
        self.explanations = self._initialize_explanations()

    def _initialize_explanations(self) -> Dict[str, str]:
        """Initialize explanation content (you can modify these later)"""
        return {
            "explain_company": """🏢 VibPath 頻率治療中心

我們是專業的頻率治療設備製造商，專精於極低頻電磁波技術，致力於為客戶提供高品質的頻率治療體驗。

🎯 我們的使命：
透過精準的頻率調節技術，幫助每個人找回內在的和諧與平衡。

🔬 核心技術優勢：
• 波形極低失真度 - 確保治療效果最大化
• 磁場強度充足 - 提供更深層的共振效果
• 波形純淨穩定 - 每一台機器都經過精密調校
• 專業頻率配方 - 基於科學研究和實務經驗

⚡ 產品特色：
• 不只修行人適用，一般人也能輕鬆使用
• 涵蓋助眠、專注、修行等多元需求
• 每款產品都具備卓越的技術規格
• 長期使用安全可靠

✨ 服務理念：
以技術為本，用心製造每一台設備，讓頻率治療真正發揮應有的效果。

📞 歡迎體驗我們的專業產品，感受高品質頻率治療的神奇力量！""",

            "explain_frequency": """🎵 頻率治療原理說明

頻率治療是運用特定的極低頻電磁波來調節身心狀態的自然療法。

🧠 科學基礎：
• 大腦會與外部頻率產生共振現象
• 不同頻率對應不同的腦波狀態
• α波(7.83-8Hz)：大腦靜下來後的狀態，助眠效果
• θ波(4Hz)：醒睡之間的腦波，比α波更積極的助眠作用
• γ波(40Hz)：高度專注時的大腦腦波

⚡ 我們的技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足，能發揮更好效果
• 每一台機器都經過精密調校
• 不只修行人輔助好用，一般人用也都很好

🎯 主要應用：
• 助眠放鬆：舒曼波、α波、θ波
• 提升專注：γ波(40Hz)
• 修行輔助：θ波幫助進入更深的定靜狀態
• 脈輪調理：13頻脈輪波對應瑜珈系統

🌟 使用效果：
• θ波(4Hz)特別適合修行人，幫助修行時更容易進入深層定靜狀態
• 所有產品共同特點：波形純淨、失真度低、磁場強度足""",

            "explain_7_83hz": """🌍 7.83Hz 舒曼共振療法

7.83Hz 是地球的基本振動頻率，被稱為「地球心跳」，是大家一般所知的極低頻電磁波，主要用於助眠。

🔬 科學發現：
• 1952年由物理學家舒曼發現
• 地球電離層的自然共振頻率
• 屬於α波範圍，是大腦靜下來後的腦波狀態
• 與人體生物節律高度吻合

⚡ 我們的技術優勢：
✅ 波形極低失真度 - 確保純淨的頻率輸出
✅ 磁場強度充足 - 能發揮更好的助眠效果
✅ 波形穩定純淨 - 經過精密調校的專業設備
✅ 8Hz優化版本 - 根據經驗，效果比7.83Hz更佳

🌱 主要功效：
• 深度放鬆身心，有效助眠
• 釋放日常累積的壓力
• 平衡情緒波動
• 改善睡眠品質
• 幫助進入深層休息狀態

🧘 適合族群：
• 失眠困擾者
• 工作壓力大的上班族
• 需要深度放鬆的人
• 想改善睡眠品質的人

⏰ 使用建議：
睡前使用30-60分鐘，幫助身心放鬆，自然進入深層睡眠狀態。""",

            "explain_13Freq": """🕉️ 13頻脈輪波療法

13頻脈輪波，如其名「脈輪」，屬於瑜珈系統，對應從海底輪到頂輪的完整能量中心調理。

🔮 脈輪系統說明：
• 共13個頻率對應不同脈輪位置
• 從海底輪到頂輪的完整覆蓋
• 結合古老瑜珈智慧與現代頻率技術
• 每個頻率都經過精密調校

⚡ 技術特色：
✅ 波形極低失真度 - 確保純淨的脈輪共振
✅ 磁場強度充足 - 深層激活能量中心
✅ 13個專業頻率 - 對應完整脈輪系統
✅ 波形穩定純淨 - 每一台都經過精密調校

🎯 主要功效：
• 平衡身體各個能量中心
• 調理相對位置的健康狀況
• 促進能量流動順暢
• 增強身心靈整體和諧
• 輔助冥想修行進入更深層狀態

🧘 適合族群：
• 修行人士 - 絕佳的修行輔助工具
• 瑜珈練習者 - 深化練習效果
• 身心調理需求者 - 平衡能量狀態
• 一般人日常保健 - 維持能量流動

🌟 使用效果：
除了修行人輔助使用外，一般人使用也都很有幫助，能感受到身心能量的平衡與流動。

⏰ 使用建議：
建議在安靜環境中使用，搭配冥想或瑜珈練習，每次30-60分鐘。""",

            "explain_40hz": """⚡ 40Hz γ波頻率療法

40Hz 是人高度專注時大腦的腦波，使用目的是期望誘發大腦的同步性，促使提高專注力。

🔬 科學研究：
• 這是人高度專注時大腦的腦波狀態
• 誘發大腦同步性，提高專注力
• 在醫學上有不少研究支持
• 可以搜尋「MIT 40HZ」了解相關研究

⚡ 技術特色：
✅ 波形極低失真度 - 確保純淨的γ波輸出
✅ 磁場強度充足 - 有效誘發大腦同步
✅ 波形穩定純淨 - 經過精密調校
✅ 專業級頻率 - 符合研究標準的40Hz

🎯 主要功效：
• 提高專注力和注意力
• 促進大腦同步性
• 增強認知功能
• 改善學習效率
• 輔助深度專注狀態

🧘 適合族群：
• 需要高度專注的工作者
• 學習者和研究人員
• 修行人士
• 一般人提升專注力需求

🌟 使用效果：
不只修行人輔助好用，一般人用也都很好，能明顯感受到專注力的提升。

⏰ 使用建議：
需要專注時使用，每次15-45分鐘，可搭配學習或工作使用。""",

            "explain_double_freq": """🔄 雙頻複合治療法

結合多種頻率的複合療法，提供更全面的身心靈療癒體驗。

🎵 複合原理：
• 同時運用多個治療頻率
• 不同頻率相互協調
• 層次性的療癒過程
• 全方位的身心調節

🌊 頻率組合：
1️⃣ 7.83Hz + 10Hz：深度放鬆 + 專注
2️⃣ 13Freq + 40Hz：專注 + 覺知提升
3️⃣ 三頻組合：全面平衡療法
4️⃣ 漸進式頻率：引導式深度療癒

💎 療效特色：
✅ 深層次身心療癒
✅ 多維度能量平衡
✅ 整體性調和效果
✅ 加速療癒進程
✅ 持久穩定的效果

🎯 適合族群：
• 需要深度療癒的人
• 多重身心困擾者
• 追求全面平衡的人
• 希望快速見效的人

⭐ 獨特優勢：
相比單一頻率，複合療法能夠：
• 同時處理多個問題
• 提供更豐富的體驗
• 達到更深層的療效
• 適應個人化需求

⏰ 建議療程：
每次45-90分鐘，每週1-2次，適合作為深度療癒的主要方案。"""
        }

    def handle_postback(self, postback_data: str, user_id: str, with_quick_reply: bool = True) -> TextSendMessage:
        """
        Handle postback event and return appropriate response.

        Args:
            postback_data: Postback data from button
            user_id: LINE user ID
            with_quick_reply: Whether to include quick reply buttons

        Returns:
            TextSendMessage: Response message with optional quick reply
        """
        try:
            logger.info(f"Handling postback: {postback_data} for user: {user_id}")

            explanation = self.explanations.get(postback_data)
            if explanation:
                message = TextSendMessage(text=explanation)
                if with_quick_reply:
                    # Import here to avoid circular import
                    from .message_handler import MessageHandler
                    handler = MessageHandler()
                    message.quick_reply = handler.create_quick_reply_detailed()
                return message
            else:
                return TextSendMessage(text="抱歉，目前沒有相關說明資訊。請聯繫客服獲得更多幫助。")

        except Exception as e:
            logger.error(f"Error handling postback {postback_data}: {e}")
            return TextSendMessage(text="系統處理時發生錯誤，請稍後再試。")

    def add_explanation(self, key: str, content: str):
        """Add or update explanation content"""
        self.explanations[key] = content

    def get_explanation(self, key: str) -> Optional[str]:
        """Get explanation content by key"""
        return self.explanations.get(key)

    def list_available_explanations(self) -> list:
        """List all available explanation keys"""
        return list(self.explanations.keys())


# Default postback handler instance
postback_handler = PostbackHandler()