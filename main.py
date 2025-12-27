import json
import random
import time
from playwright.sync_api import sync_playwright

def run():
    url = "https://www.zara.com/tr/tr/kadin-ceket-l1114.html"
    data = []

    print("🥷 ZARA'ya Ninja Modunda Giriliyor...")
    
    with sync_playwright() as p:
        # 1. KAMUFLAJ: Tarayıcıyı özel argümanlarla başlat
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled', # Otomasyon izini sil
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-position=0,0',
                '--ignore-certifcate-errors',
                '--ignore-certifcate-errors-spki-list',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        )
        
        # 2. KAMUFLAJ: Tarayıcı penceresi (Context) ayarları
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="tr-TR",
            timezone_id="Europe/Istanbul"
        )
        
        # 3. KAMUFLAJ: Robot izlerini JavaScript ile sil
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            # Siteye git
            page.goto(url, timeout=90000, wait_until="domcontentloaded")
            print("Siteye istek atıldı, bekleniyor...")
            
            # Rastgele bekleme (İnsan taklidi)
            time.sleep(random.uniform(5, 8))
            
            # Tekrar Fotoğraf Çek (Bakalım kandırabildik mi?)
            page.screenshot(path="son_durum.png", full_page=True)
            print("📸 Ekran görüntüsü alındı: son_durum.png")

            # Ürünleri bul
            # Zara bazen CSS class'larını değiştirir, en genel yapıyı arayalım
            products = page.locator("li").filter(has=page.locator("a[href*='/tr/tr/']")).all()
            
            print(f"📦 Tahmini {len(products)} adet kutu bulundu.")

            count = 0
            for item in products:
                if count >= 5: break # İlk 5 ürün
                try:
                    # Linki bul
                    link_el = item.locator("a").first
                    link = link_el.get_attribute("href")
                    
                    # Fiyatı bul (Metin olarak ne varsa al)
                    text = item.inner_text()
                    
                    if "TL" in text and link:
                        data.append({
                            "sira": count + 1,
                            "link": link,
                            "ham_veri": text.replace("\n", " ")[:100]
                        })
                        count += 1
                        print(f"   ✅ Ürün bulundu: {link[:30]}...")
                except:
                    continue

        except Exception as e:
            print(f"❌ Hata: {e}")
            page.screenshot(path="hata_resmi.png")
        
        browser.close()

    # Sonucu kaydet
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("🏁 İşlem tamamlandı.")

if __name__ == "__main__":
    run()
