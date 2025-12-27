import json
from playwright.sync_api import sync_playwright

def run():
    # Zara ceket kategorisi
    url = "https://www.zara.com/tr/tr/kadin-ceket-l1114.html"
    data = []

    print("ZARA'ya gidiliyor...")
    
    with sync_playwright() as p:
        # headless=True: tarayıcıyı gizli açar
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Sayfaya git (60 saniye bekleme süresi)
        page.goto(url, timeout=60000)
        
        # Yüklenmesini bekle
        page.wait_for_load_state("networkidle")
        
        # Ürünleri bul
        products = page.locator("ul.product-grid__product-list > li")
        count = products.count()
        print(f"Toplam {count} ürün bulundu.")

        # İlk 5 ürünü çek
        for i in range(min(5, count)):
            item = products.nth(i)
            try:
                name = item.locator(".product-grid-product-info__name").inner_text()
                price = item.locator(".price-current__amount").inner_text()
                
                data.append({"urun": name, "fiyat": price})
                print(f"Çekildi: {name}")
            except:
                pass
        
        browser.close()

    # Sonucu kaydet
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Bitti! sonuc.json dosyası oluştu.")

if __name__ == "__main__":
    run()