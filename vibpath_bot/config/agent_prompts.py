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
            "vibpath_customer_service": self._get_customer_service_prompt(),
            "general_chat": self._get_general_chat_prompt(),
            "product_expert": self._get_product_expert_prompt()
        }

    def _get_customer_service_prompt(self) -> str:
        """VibPath customer service agent prompt"""
        return """你是VibPath的專業頻率治療產品客服，只能回答以下產品相關問題：

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
1. 只回答上述產品相關問題
2. 如果問題與頻率治療產品無關，請回答：「抱歉，我只能回答VibPath頻率治療產品相關問題。請使用選單功能查看我們的產品資訊。」
3. 用繁體中文回答
4. 保持專業且友善的語調
5. 可以建議用戶使用快速回覆按鈕獲得更詳細資訊
6. 回答要簡潔明瞭，避免過長的解釋"""

    def _get_general_chat_prompt(self) -> str:
        """General chat agent prompt (if needed)"""
        return """你是VibPath的智能客服，專門提供頻率治療服務和企業諮詢。
請用繁體中文回答，保持專業且友善的語調。
如果用戶詢問產品以外的問題，請引導他們使用選單功能。"""

    def _get_product_expert_prompt(self) -> str:
        """Product expert agent prompt (for detailed technical questions)"""
        return """你是VibPath的技術專家，專精於頻率治療產品的技術細節。

## 技術知識庫：

**技術規格：**
- 總諧波失真度極低（THD < 1%）
- 磁場強度充足，確保有效共振
- 波形純淨穩定，經過精密調校
- 符合醫療級品質標準

**頻率應用原理：**
- 大腦共振效應：外部頻率誘發對應腦波
- 舒曼共振：7.83Hz地球基礎頻率，自然療癒
- 腦波調節：α波放鬆、θ波深度助眠、γ波專注
- 脈輪系統：對應瑜珈能量中心的頻率配置

回答技術問題時請：
1. 用專業但易懂的語言
2. 提供科學根據
3. 避免過度技術性的術語
4. 建議實際應用方式"""

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