"""
Image management utilities for LINE Bot.
Handles image upload, storage, and URL generation for Flex Messages.
"""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ImageManager:
    """Manages image storage and URL generation for LINE Bot"""

    def __init__(self, base_upload_dir: str = "static/uploads"):
        """
        Initialize image manager.

        Args:
            base_upload_dir: Base directory for uploaded images
        """
        self.base_upload_dir = base_upload_dir
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure upload directories exist"""
        directories = [
            f"{self.base_upload_dir}/packages",
            f"{self.base_upload_dir}/business",
            f"{self.base_upload_dir}/temp"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def save_uploaded_image(self, image_data: bytes, filename: str, category: str = "temp") -> Optional[str]:
        """
        Save uploaded image to local storage.

        Args:
            image_data: Image binary data
            filename: Original filename
            category: Image category (packages, business, temp)

        Returns:
            str: Saved file path or None if failed
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            unique_filename = f"{timestamp}_{name}{ext}"

            # Ensure valid category
            if category not in ["packages", "business", "temp"]:
                category = "temp"

            file_path = f"{self.base_upload_dir}/{category}/{unique_filename}"

            # Save image
            with open(file_path, 'wb') as f:
                f.write(image_data)

            logger.info(f"Image saved: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return None

    def get_image_url(self, file_path: str, base_url: Optional[str] = None) -> str:
        """
        Get public URL for saved image.

        Args:
            file_path: Local file path
            base_url: Base URL for the application

        Returns:
            str: Public image URL
        """
        if base_url:
            # Convert local path to web path
            web_path = file_path.replace("static/", "")
            return f"{base_url.rstrip('/')}/{web_path}"
        else:
            # Return placeholder for development
            filename = os.path.basename(file_path)
            return f"https://via.placeholder.com/1024x640/E0E0E0/666666?text={filename}"

    def create_package_data_template(self, images: Dict[str, str]) -> Dict[str, Any]:
        """
        Create package data template with user images.

        Args:
            images: Dictionary of image URLs

        Returns:
            Dict: Package data template
        """
        return {
            "title": "四天三夜精選行程",
            "subtitle": "探索美麗風景，享受難忘旅程",
            "price": "NT$ 12,800",
            "original_price": "NT$ 15,000",
            "image_url": images.get("main", "https://via.placeholder.com/1024x640/4CAF50/FFFFFF?text=Main+Image"),
            "highlights": [
                "專業導遊帶領",
                "精選景點遊覽",
                "在地美食體驗",
                "舒適住宿安排"
            ],
            "included": [
                "住宿三晚",
                "每日早餐",
                "專業導遊",
                "交通接送",
                "旅遊保險"
            ],
            "duration": "4天3夜",
            "departure": "2024年4月1日起",
            "contact_action": "📞 立即諮詢",
            "detail_url": "https://example.com/package-details"
        }

    def create_business_data_template(self, images: Dict[str, str]) -> Dict[str, Any]:
        """
        Create business data template with user images.

        Args:
            images: Dictionary of image URLs

        Returns:
            Dict: Business data template
        """
        return {
            "company_name": "VibPath 旅遊顧問",
            "tagline": "專業旅遊規劃 · 貼心服務體驗",
            "description": "我們擁有20年的旅遊規劃經驗，致力於為每位客戶量身打造最適合的旅行體驗。從行程規劃到住宿安排，我們提供一站式的專業服務。",
            "logo_url": images.get("logo", "https://via.placeholder.com/1024x640/2196F3/FFFFFF?text=Company+Logo"),
            "services": [
                "客製化旅遊規劃",
                "住宿訂房服務",
                "交通接送安排",
                "在地導覽服務",
                "團體旅遊企劃"
            ],
            "features": [
                "20年專業經驗",
                "24小時客服支援",
                "客製化服務",
                "優質合作夥伴",
                "滿意度保證"
            ],
            "contact_phone": "0800-123-456",
            "website": "https://vibpath.com",
            "line_id": "@vibpath"
        }

    def get_sample_package_images(self) -> Dict[str, str]:
        """
        Get sample package image URLs.

        Returns:
            Dict: Sample image URLs
        """
        return {
            "main": "https://via.placeholder.com/1024x640/4CAF50/FFFFFF?text=Beautiful+Destination",
            "day1": "https://via.placeholder.com/800x600/FF9800/FFFFFF?text=Day+1",
            "day2": "https://via.placeholder.com/800x600/2196F3/FFFFFF?text=Day+2",
            "day3": "https://via.placeholder.com/800x600/9C27B0/FFFFFF?text=Day+3",
            "day4": "https://via.placeholder.com/800x600/E91E63/FFFFFF?text=Day+4"
        }

    def get_sample_business_images(self) -> Dict[str, str]:
        """
        Get sample business image URLs.

        Returns:
            Dict: Sample image URLs
        """
        return {
            "logo": "https://via.placeholder.com/1024x640/2196F3/FFFFFF?text=VibPath+Logo",
            "office": "https://via.placeholder.com/800x600/607D8B/FFFFFF?text=Our+Office",
            "team": "https://via.placeholder.com/800x600/795548/FFFFFF?text=Our+Team"
        }


class FlexMessageBuilder:
    """Helper class to build Flex Messages with user content"""

    def __init__(self, image_manager: ImageManager):
        """
        Initialize Flex Message builder.

        Args:
            image_manager: ImageManager instance
        """
        self.image_manager = image_manager

    def build_four_night_package(self, custom_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build four-night package with user data.

        Args:
            custom_data: Custom package data to override defaults

        Returns:
            Dict: Complete package data
        """
        # Start with template
        sample_images = self.image_manager.get_sample_package_images()
        package_data = self.image_manager.create_package_data_template(sample_images)

        # Override with custom data if provided
        if custom_data:
            package_data.update(custom_data)

        return package_data

    def build_business_introduction(self, custom_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build business introduction with user data.

        Args:
            custom_data: Custom business data to override defaults

        Returns:
            Dict: Complete business data
        """
        # Start with template
        sample_images = self.image_manager.get_sample_business_images()
        business_data = self.image_manager.create_business_data_template(sample_images)

        # Override with custom data if provided
        if custom_data:
            business_data.update(custom_data)

        return business_data


# Default instances
default_image_manager = ImageManager()
default_flex_builder = FlexMessageBuilder(default_image_manager)