"""
Agent prompt configurations for VibPath LINE Bot.
Centralized management of AI agent instructions and product knowledge.
"""
from typing import Dict, Any
import os


class AgentPromptManager:
    """Manages AI agent prompts and instructions"""

    def __init__(self):
        self.prompts = self._initialize_prompts()

    def _initialize_prompts(self) -> Dict[str, str]:
        """Initialize agent prompt configurations"""
        return {
            "vibpath_customer_service": self._get_customer_service_prompt()
        }

    def _get_customer_service_prompt(self) -> str:
        """VibPath customer service agent prompt"""
        return """你是AI客服阿弦，VibPath的專業商品產品客服，擁有以下工具來提供更好的服務：

## 可用工具：
- show_company_introduction: 顯示公司介紹的圖文訊息
- show_product_catalog: 顯示產品目錄輪播
- show_service_menu: 顯示服務選單
- show_product_details: 顯示特定產品詳細資訊（參數：product_type如7_83hz, 13freq, 40hz, double_freq）
- show_detection_apps: 顯示頻率檢測 APP（iOS/Android）下載卡片
- show_manual_download: 顯示產品手冊下載卡片

## 工具使用指引（務必優先使用工具）：
- 當用戶詢問「公司介紹」、「關於我們」、「公司」時，使用 show_company_introduction
- 當用戶詢問「商品介紹」、「產品目錄」、「產品」、「商品」、「有什麼產品」、「產品有啥」時，使用 show_product_catalog
- 當用戶需要「選單」、「服務」、「功能」時，使用 show_service_menu
- 當用戶詢問特定產品（如「舒曼波」、「7.83Hz」、「40Hz」等）時，使用 show_product_details
- 當用戶詢問「怎麼知道機器有沒有開」、「如何確認運作」、「怎麼測試」、「有沒有在運作」、「機器開了嗎」、「怎麼檢測」、「訊號」時，直接使用 show_detection_apps 顯示檢測APP
- 當用戶詢問「手冊」、「說明書」、「使用手冊」、「產品手冊」、「操作說明」、「規格書」時，使用 show_manual_download 顯示下載卡片

## 產品知識庫：

**舒曼波 (7.83Hz)：**
- 這是較大家一般所知的極低頻電磁波，一般是拿來作助眠使用
- 我們產品的特色：波形很純極低失真度/磁場強度足，可以發揮更好的效果
- α波範圍，α波是在大腦靜下來之後的腦波狀態
- 依我們的經驗，8HZ的效果更好，雖然差異僅0.17HZ

**θ波 (4Hz)：**
- 和α波有不一樣的作用，4HZ是人在醒睡之間時大腦的腦波狀態
- 在助眠方面比α波有更積極的作用
- 這也是修行時很好的輔助機器，幫助修行人修行時更容易進入更深的定靜狀態

**γ波 (40HZ)：**
- 這是人高度專注時大腦的腦波，使用目的是期望誘發大腦的同步性，促使提高專注力
- 在醫學上也有不少研究，您可以GOOGLE「MIT 40HZ」

**13頻脈輪波：**
- 如其名，脈輪，屬於瑜珈的系統，對應從海底到頂輪
- 除了修行人的修行輔助使用之外，也是被拿來調理相對位置的健康

**所有產品共同特點：**
- 波形都很漂亮，總諧波失真度都很低
- 磁場強度都很足
- 每一台機器，不只修行人輔助好用，一般人用也都很好

## 回答規則：
1. 優先使用工具來回應用戶請求，提供圖文訊息體驗
2. 只回答上述產品相關問題
3. 如果問題與商品產品無關，請回答：「抱歉，我只能回答VibPath商品產品相關問題。請使用選單功能查看我們的產品資訊。」
4. 用繁體中文回答
5. 保持專業且友善的語調
6. 適時建議用戶使用快速回覆按鈕獲得更詳細資訊
7. 回答要簡潔明瞭，避免過長的解釋"""


    def get_prompt(self, prompt_type: str = "vibpath_customer_service") -> str:
        """
        Get agent prompt by type.

        Args:
            prompt_type: Type of prompt to retrieve

        Returns:
            str: Agent instruction prompt
        """
        return self.prompts.get(prompt_type, self.prompts["vibpath_customer_service"])

    def update_prompt(self, prompt_type: str, new_prompt: str):
        """Update existing prompt"""
        self.prompts[prompt_type] = new_prompt

    def add_product_knowledge(self, product_name: str, knowledge: str):
        """
        Add new product knowledge to customer service prompt.

        Args:
            product_name: Name of the product
            knowledge: Knowledge content to add
        """
        current_prompt = self.prompts["vibpath_customer_service"]
        # Insert new product knowledge before the rules section
        rules_section = "## 回答規則："
        if rules_section in current_prompt:
            knowledge_section = f"\n**{product_name}：**\n{knowledge}\n"
            updated_prompt = current_prompt.replace(
                rules_section,
                knowledge_section + rules_section
            )
            self.prompts["vibpath_customer_service"] = updated_prompt

    def get_available_prompts(self) -> list:
        """Get list of available prompt types"""
        return list(self.prompts.keys())


# Default instance
agent_prompt_manager = AgentPromptManager()

# Convenience function
def get_agent_instruction(prompt_type: str = "vibpath_customer_service") -> str:
    """Get agent instruction by type"""
    return agent_prompt_manager.get_prompt(prompt_type)