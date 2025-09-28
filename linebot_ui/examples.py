"""
Flex Message examples and showcase for LINE Bot development.
This file contains example templates and usage demonstrations.
"""
from .flex_templates import FlexMessageTemplates
from .message_handler import MessageHandler


def example_weather_data():
    """Example weather data for testing Flex Messages"""
    return {
        "status": "success",
        "data": {
            "city": "台北",
            "country": "Taiwan",
            "temperature": "25°C",
            "temperature_f": "77°F",
            "feels_like": "27°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind_speed": "8 km/h",
            "wind_direction": "NE"
        }
    }


def showcase_flex_messages():
    """
    Showcase different types of Flex Messages.
    This function demonstrates how to create various message types.
    """
    templates = FlexMessageTemplates()
    handler = MessageHandler()

    print("🎨 Flex Message Showcase")
    print("=" * 50)

    # 1. Weather Card
    print("\n1. 天氣卡片 (Weather Card)")
    weather_data = example_weather_data()
    weather_flex = templates.weather_card(weather_data)
    print(f"   Alt Text: {weather_flex.alt_text}")
    print(f"   Type: FlexSendMessage")

    # 2. Service Menu
    print("\n2. 服務選單 (Service Menu)")
    menu_flex = templates.service_menu()
    print(f"   Alt Text: {menu_flex.alt_text}")
    print(f"   Type: FlexSendMessage")

    # 3. Error Message
    print("\n3. 錯誤訊息 (Error Message)")
    error_flex = templates.error_message("無法連接到天氣服務")
    print(f"   Alt Text: {error_flex.alt_text}")
    print(f"   Type: FlexSendMessage")

    # 4. Welcome Messages
    print("\n4. 歡迎訊息 (Welcome Messages)")
    welcome_messages = handler.create_welcome_message()
    print(f"   Messages Count: {len(welcome_messages)}")
    for i, msg in enumerate(welcome_messages):
        print(f"   Message {i+1}: {type(msg).__name__}")

    # 5. Help Message
    print("\n5. 說明訊息 (Help Message)")
    help_msg = handler.create_help_message()
    print(f"   Type: {type(help_msg).__name__}")
    print(f"   Preview: {help_msg.text[:50]}...")

    print("\n✅ Showcase completed!")


def test_message_detection():
    """Test message type detection"""
    handler = MessageHandler()

    test_cases = [
        ("台北天氣", "weather"),
        ("今天會下雨嗎", "weather"),
        ("選單", "menu"),
        ("服務", "menu"),
        ("幫助", "help"),
        ("說明", "help"),
        ("你好", "general"),
        ("Hello weather in Tokyo", "weather"),
    ]

    print("\n🔍 訊息類型偵測測試")
    print("=" * 50)

    for text, expected in test_cases:
        detected = handler.detect_message_type(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text}' → {detected} (expected: {expected})")


if __name__ == "__main__":
    # Run showcase when file is executed directly
    showcase_flex_messages()
    test_message_detection()