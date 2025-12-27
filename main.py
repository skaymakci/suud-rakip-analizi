import json
import time
from playwright.sync_api import sync_playwright

def run():
    # Zara Ceket Linki
    url = "https://www.zara.com/tr/tr/kadin-ceket-l1114.html"
    data = []

    print("🕵️‍♀️ ZARA'ya Gizli Ajan Gönderiliyor...")
    
    with sync_playwright() as p:
        # MASKE TAKMA (User-Agent)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url, timeout=60000)
            print("Siteye girildi, bekleniyor...")
            page.wait_for_timeout(5000) # 5 saniye bekle
            
            # Ürünleri bul
            products = page.locator(".product-grid-product")
            if products.count() == 0:
                products = page.locator("li[data-productid]")
            
            count = products.count()
            print(f"📦 {count} ürün bulundu!")

            for i in range(min(5, count)):
                item = products.nth(i)
                try:
                    # Linki al
                    link = item.locator("a.product-link").get_attribute("href")
                    # Fiyatı al (Farklı etiketler deniyoruz)
                    price = item.locator(".price-current__amount, .money-amount__main").first.inner_text()
                    
                    data.append({"urun": link, "fiyat": price})
                except:
                    pass

        except Exception as e:
            print(f"Hata: {e}")
        
        browser.close()

    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ Bitti.")

if __name__ == "__main__":
    run()
