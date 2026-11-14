"""
客人看得到的固定文案不能出現療效或保證安全的說法。

golden 只保證內容沒變，不管內容該不該講，所以另外檢查用詞。AI 提示詞會把這些詞
列為禁語，不在檢查範圍內。
"""
from pathlib import Path

import pytest

GOLDEN = Path(__file__).parent / "golden" / "line_messages.json"
BANNED = [
    "治療", "療效", "治癒", "修復", "調理", "記憶力", "安全可靠", "神奇",
    "科學驗證", "科學基礎", "科學研究", "靈性覺醒", "意識提升", "在醫學上",
]


@pytest.mark.parametrize("word", BANNED)
def test_fixed_copy_avoids_claim(word):
    assert word not in GOLDEN.read_text(encoding="utf-8")
