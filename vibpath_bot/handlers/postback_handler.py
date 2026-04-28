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
            "explain_company": """🏢 VibPath 商品中心

我們是專業的商品設備製造商，專精於極低頻電磁波技術，致力於為客戶提供高品質的商品體驗。

🎯 我們的使命：
透過精準的商品技術，幫助每個人找回內在的和諧與平衡。

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
以技術為本，用心製造每一台設備，讓商品真正發揮應有的效果。

📞 歡迎體驗我們的專業產品，感受高品質商品的神奇力量！""",

            "explain_frequency": """🎵 商品原理說明

商品產品是運用特定的極低頻電磁波來調節身心狀態的自然方法。

🧠 科學基礎：
• 大腦會與外部頻率產生共振現象
• 不同頻率對應不同的腦波狀態
• α波(7.83-8Hz)：大腦靜下來後的狀態，幫助身心平衡、放鬆，助眠效果
• θ波(4Hz)：醒睡之間的腦波，比α波更積極的助眠作用
• γ波(40Hz)：提升記憶力與專注力，適合高效學習與思考時使用

⚡ 我們的技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足，能發揮更好效果，同時皆符合國家(極)低頻電磁波暴露規範
• 每一台機器都經過精密調校
• 不只修行人輔助好用，一般人用也都很好

🎯 主要應用：
• 助眠放鬆：舒曼波、α波、θ波，放鬆、助眠
• 提升專注：γ波(40Hz)，提升記憶力與專注力
• 修行輔助：α波、θ波、γ波，幫助修行時更容易進入深層定靜狀態
• 脈輪調理：13頻脈輪波對應瑜珈系統修行，多頻率選擇，支援Theta、Alpha、Gamma波，幫助冥想、放鬆與情緒穩定

🌟 產品共同特點：波形純淨、失真度低、磁場強度足""",

            "explain_7_83hz": """🎵 舒曼波 (7.83Hz)

這是較大家一般所知的極低頻電磁波，一般是拿來作助眠使用。

🧠 原理：
• α波(7.83-8Hz)：大腦靜下來後的狀態，幫助身心平衡、放鬆，助眠效果
• 相對於7.83Hz，依我們的經驗，8Hz的效果更好，雖然差異僅0.17Hz

⚡ 技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足，能發揮更好效果，同時皆符合國家(極)低頻電磁波暴露規範
• 每一台機器都經過精密調校

🎯 適用：放鬆、助眠""",

            "explain_13Freq": """🕉️ 13頻脈輪波

如其名，脈輪，屬於瑜珈的系統，對應從海底到頂輪。

🎯 主要用途：
• 對應瑜珈系統修行
• 多頻率選擇，支援Theta、Alpha、Gamma波
• 幫助冥想、放鬆與情緒穩定
• 調理相對位置的健康

⚡ 技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足
• 不只修行人輔助好用，一般人用也都很好""",

            "explain_40hz": """⚡ γ波(GAMMA) 40Hz

這是人高度專注時大腦的腦波。

🧠 效果：
• 提升記憶力與專注力
• 適合高效學習與思考時使用
• 期望誘發大腦的同步性

⚡ 技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足，能發揮更好效果，同時皆符合國家(極)低頻電磁波暴露規範
• 不只修行人輔助好用，一般人用也都很好

💡 在醫學上也有不少研究，您可以GOOGLE「MIT 40Hz」。""",

            "explain_double_freq": """🔄 α/θ波

🧠 雙頻說明：

1、α波(7.83-8Hz)：
• 大腦靜下來後的狀態，幫助身心平衡、放鬆，助眠效果
• 相對於7.83Hz，依我們的經驗，8Hz的效果更好，雖然差異僅0.17Hz

2、θ波(4Hz)：
• 醒睡之間的腦波，比α波更積極的助眠作用
• 修行時很好的輔助機器，幫助修行人修行時更容易進入更深的定靜狀態

⚡ 技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足，能發揮更好效果，同時皆符合國家(極)低頻電磁波暴露規範
• 不只修行人輔助好用，一般人用也都很好""",

            "explain_pulse_gen": """🔧 客製頻率 脈衝產生器

程式修改客製頻率，目前已完成共11頻率可選：
(選一個頻率進行燒寫，一台機器固定一個頻率，不能切換頻率)

📋 可選頻率：
• 0.1Hz：Sub-Delta Wave
• 0.5Hz：Delta Wave
• 4.0Hz：Theta Wave（可選α/θ波雙頻版）
• 8.0Hz：Alpha Wave（可選α/θ波雙頻版）
• 10.0Hz：Middle Alpha Wave
• 12.0Hz：Low Beta Wave
• 25.0Hz：Beta Wave
• 40.0Hz：Gamma Wave（可選γ波獨立版）
• 111Hz：Angel Frequency
• 128Hz：Grounding Frequency (Otto 128)
• 136.1Hz：OM Frequency
（亦可依需求重新設計新頻率）

⚡ 機器特色：
• 出貨前重新燒錄新頻率程式，可微調至誤差0.5%以內
• 波形維持超低總失真度(THD)
• 磁場強度維持銅線加強版
• 使用有效距離約5公尺以內，3公尺以內效果佳

⚠️ 與人體安全距離：
• 0.1 / 0.5 / 4.0 Hz：0公分，可貼身使用
• 8.0Hz：4公分
• 12.0Hz：5公分
• 25.0 / 40.0 / 111 / 128 / 136.1 Hz：7公分

機器皆以舒曼波機重新編寫、燒錄新程式碼達成。""",

            "explain_composite_freq": """🎛️ 複合式頻率產生器 (0.5Hz + 8.0Hz)

同一台機器同時產出 0.5Hz 與 8.0Hz 兩組極低頻電磁波，複合式共振體驗。

🧠 頻率原理：
• 0.5Hz (Delta Wave)：深層睡眠腦波，幫助深度放鬆、修復
• 8.0Hz (Alpha Wave)：大腦靜下來後的狀態，放鬆、助眠、身心平衡
• 兩頻同時作用，兼顧深層修復與身心平衡

⚡ 技術特色：
• 波形都很漂亮，總諧波失真度都很低
• 磁場強度都很足，能發揮更好效果，同時皆符合國家(極)低頻電磁波暴露規範
• 銅線加強版，磁場穩定
• 每一台機器都經過精密調校

🎯 適用：深層助眠、放鬆、修復共振
""",

            "explain_ten_freq": """🎚️ 十頻儀 (0.1Hz~136.1Hz)

PEMF 脈衝電磁場產生器強化版，一台機器整合 10 種頻率，側按切換鍵即時切換，OLED 螢幕顯示當前頻率資訊。

📋 內建 10 頻率：
• 0.1Hz：Sub-Delta Wave
• 0.5Hz：Deep Delta Wave
• 4.0Hz：Theta Wave
• 8.0Hz：Low Alpha Wave
• 10.0Hz：Middle Alpha Wave
• 12.0Hz：Low Beta Wave
• 40.0Hz：Gamma Wave
• 111Hz：Angel Frequency
• 128Hz：Grounding Frequency (Otto 128)
• 136.1Hz：OM Frequency

⚡ 機器特色：
• 側按頻率切換鍵，免重新燒錄即可切換頻率
• OLED 螢幕即時顯示當前頻率與波型資訊
• 3A 大電晶體驅動，磁場強度充足
• LED 呼吸燈，運作狀態一目了然
• Type-C (USB-C) 供電，接線方便
• 銅線加強版線圈，波形純淨、總諧波失真度低
• 每一台皆單獨確認頻率精度，微調至誤差 0.3% 以內
• 100% 台灣設計製造，符合國家(極)低頻電磁波暴露規範

📏 使用距離：
• 有效距離約 5 公尺以內，3 公尺以內效果佳

⚠️ 與人體安全距離：
• 0.1 / 0.5 / 4.0 Hz：0 公分，可貼身使用
• 8.0Hz：4 公分
• 12.0Hz：5 公分
• 40.0 / 111 / 128 / 136.1 Hz：7 公分

🎯 適用：助眠、放鬆、專注提升、修行輔助、健康調理
"""
        }

    def handle_postback(self, postback_data: str, user_id: str, request_host: str = None, with_quick_reply: bool = True):
        """
        Handle postback event and return appropriate response.

        Args:
            postback_data: Postback data from button
            user_id: LINE user ID
            request_host: Request host for dynamic URL generation
            with_quick_reply: Whether to include quick reply buttons

        Returns:
            TextSendMessage or FlexSendMessage: Response message with optional quick reply
        """
        try:
            logger.info(f"Handling postback: {postback_data} for user: {user_id}")

            # Special handlers for different UI actions
            if postback_data == "toggle_ai_reply":
                # Handle AI reply toggle from Rich Menu
                from .ai_toggle_handler import ai_toggle_handler
                return ai_toggle_handler.handle_toggle(user_id)

            elif postback_data == "check_ai_status":
                # Check AI reply status
                from .ai_toggle_handler import ai_toggle_handler
                return ai_toggle_handler.get_status(user_id)

            elif postback_data == "show_product_details":
                # Show product details menu with product quick reply
                from .message_handler import MessageHandler
                handler = MessageHandler()
                return TextSendMessage(
                    text="📖 產品詳細說明\n\n請選擇您想了解的產品：",
                    quick_reply=handler.create_quick_reply_products()
                )

            elif postback_data == "show_basic_menu":
                # Return to basic menu
                from .message_handler import MessageHandler
                handler = MessageHandler()
                return TextSendMessage(
                    text="◀️ 返回基本選單",
                    quick_reply=handler.create_quick_reply_basic()
                )

            elif postback_data == "show_frequency_products":
                # Import here to avoid circular import
                from ..templates.custom_templates import BusinessTemplates
                from .message_handler import MessageHandler

                flex_msg = BusinessTemplates.frequency_services_carousel(request_host)
                # Add quick reply to flex message
                handler = MessageHandler()
                flex_msg.quick_reply = handler.create_quick_reply_products()
                return flex_msg

            elif postback_data == "show_company_intro":
                # Import here to avoid circular import
                from ..templates.custom_templates import BusinessTemplates
                from .message_handler import MessageHandler

                flex_msg = BusinessTemplates.company_introduction_with_homepage(request_host)
                # Add quick reply to flex message
                handler = MessageHandler()
                flex_msg.quick_reply = handler.create_quick_reply_basic()
                return flex_msg

            elif postback_data == "show_manual_download":
                from .message_handler import MessageHandler
                handler = MessageHandler()
                flex_msg = handler.create_manual_download_card(request_host)
                flex_msg.quick_reply = handler.create_quick_reply_basic()
                return flex_msg

            elif postback_data == "show_service_menu":
                # Import here to avoid circular import
                from ..templates.flex_templates import FlexMessageTemplates
                from .message_handler import MessageHandler

                flex_msg = FlexMessageTemplates.service_menu()
                # Add quick reply to flex message
                handler = MessageHandler()
                flex_msg.quick_reply = handler.create_quick_reply_basic()
                return flex_msg

            explanation = self.explanations.get(postback_data)
            if explanation:
                if with_quick_reply:
                    # Import here to avoid circular import
                    from .message_handler import MessageHandler
                    handler = MessageHandler()

                    # Use product quick reply for product explanations
                    product_postbacks = ["explain_7_83hz", "explain_13Freq", "explain_40hz", "explain_double_freq", "explain_pulse_gen", "explain_composite_freq", "explain_ten_freq", "explain_frequency"]
                    if postback_data in product_postbacks:
                        quick_reply = handler.create_quick_reply_products()
                    else:
                        quick_reply = handler.create_quick_reply_basic()

                    message = TextSendMessage(text=explanation, quick_reply=quick_reply)
                else:
                    message = TextSendMessage(text=explanation)
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