import requests
import json
import os

# Cấu hình
API_URL = "https://hieuha.net/wp-json/aff-upog/v1/feed"
API_KEY = os.environ.get("WP_API_KEY") # Lấy Key từ Secret
OUTPUT_FILE = "ads.json"

def sync_data():
    try:
        # 1. Gọi API về Website (Giả lập Header)
        headers = {
            "X-App-Key": API_KEY,
            "User-Agent": "GitHub-Action-Sync-Bot"
        }
        print(f"📡 Đang gọi API: {API_URL}...")
        response = requests.get(API_URL, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"Lỗi API: {response.status_code} - {response.text}")

        wp_data = response.json()
        
        # 2. CHUYỂN ĐỔI DỮ LIỆU (Mapping)
        # Web trả về A, nhưng App cần B. Ta phải convert.
        
        # Giả sử cấu trúc WP trả về list sản phẩm, ta lấy cái đầu làm Banner, còn lại làm Sidebar
        # Bạn cần in cái wp_data ra xem cấu trúc thật để map cho đúng nhé.
        
        items = wp_data if isinstance(wp_data, list) else wp_data.get("items", [])
        
        new_ads_structure = {
            "banner": {
                "show": False,
                "text": "",
                "url": "",
                "bg_color": "#333",
                "text_color": "#fff"
            },
            "sidebar": []
        }

        if len(items) > 0:
            # Lấy item đầu tiên làm Banner (Ví dụ)
            first = items[0]
            new_ads_structure["banner"] = {
                "show": True,
                "text": f"[HOT] {first.get('title', 'Khuyến mãi')}", # Sửa key theo JSON thật
                "url": first.get('aff_link', ''),                    # Sửa key theo JSON thật
                "bg_color": "#d32f2f",
                "text_color": "#ffffff"
            }

            # Các item còn lại đưa vào Sidebar
            for item in items[1:]:
                ad_item = {
                    "title": item.get('title', 'No Title'),
                    "desc": item.get('description', 'Click để xem chi tiết'),
                    "url": item.get('aff_link', ''),
                    "color": "#1565c0" # Hoặc random màu
                }
                new_ads_structure["sidebar"].append(ad_item)

        # 3. Ghi đè vào file ads.json trên GitHub
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(new_ads_structure, f, indent=2, ensure_ascii=False)
            
        print("✅ Đã cập nhật ads.json thành công!")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        exit(1) # Báo lỗi để GitHub Action biết

if __name__ == "__main__":
    sync_data()
