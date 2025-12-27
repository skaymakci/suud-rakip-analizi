import json
from playwright.sync_api import sync_playwright

def run():
    # Zara Ceket Linki
    url = "https://www.zara.com/tr/tr/kadin-ceket-l1114.html"
    data = []

    print("🕵️‍♀️ ZARA'ya giriliyor...")
    
    with sync_playwright() as p:
        # Tarayıcıyı daha "İnsan" gibi başlatıyoruz
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url, timeout=90000) # Süreyi uzattık
            print("Siteye erişildi, bekleniyor...")
            page.wait_for_timeout(10000) # 10 saniye bekle
            
            # NE GÖRÜYORUZ? FOTOĞRAF ÇEK! 📸
            # Bu fotoğraf sayesinde sorunu anlayacağız.
            page.screenshot(path="hata_resmi.png", full_page=True)
            print("📸 Ekran görüntüsü alındı: hata_resmi.png")

            # Farklı yöntemlerle ürün arayalım
            # Yöntem 1: Standart Zara kartları
            products = page.locator(".product-grid-product")
            
            # Yöntem 2: Link içeren herhangi bir liste elemanı
            if products.count() == 0:
                print("⚠️ Standart yöntem çalışmadı, alternatif deneniyor...")
                products = page.locator("li:has(a[href*='/tr/tr/'])")

            count = products.count()
            print(f"📦 {count} ürün bulundu!")

            for i in range(min(5, count)):
                item = products.nth(i)
                try:
                    # Link
                    link = item.locator("a").first.get_attribute("href")
                    # Fiyat (Zara bazen fiyatı gizler, text content ile alalım)
                    text_content = item.inner_text()
                    
                    data.append({
                        "sira": i+1,
                        "link": link,
                        "ham_veri": text_content[:100] # İlk 100 karakteri al
                    })
                except:
                    pass

        except Exception as e:
            print(f"Hata oluştu: {e}")
            # Hata anında da çeksin
            page.screenshot(path="hata_resmi.png")
        
        browser.close()

    # Sonucu kaydet
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ İşlem bitti.")

if __name__ == "__main__":
    run()
