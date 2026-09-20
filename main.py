from core.engine import IntegrationEngine
from core.scheduler import CatchUpScheduler
import sys

def main():
    engine = IntegrationEngine()
    
    scheduler = CatchUpScheduler(engine)
    default_test_url = "https://jsonplaceholder.typicode.com/todos/1"
    scheduler.catch_up_and_run(default_test_url)
    scheduler.start_background_loop(default_test_url)

    print("=" * 50)
    print("  CTA ERHAN - INTELLIGENCE TERMINAL v1.1")
    print("=" * 50)

    while True:
        print("\n[1] Canli Kaynaktan Tekil Veri Cek")
        print("[2] Config.json'daki Tum Kaynaklari Toplu Cek (Multi-Source)")
        print("[3] Havuzda Ara ve Filtrele (Search & Filter)")
        print("[4] Analitik Rapor Olustur ve Goster (Report)")
        print("[5] Analitik Raporu Masaustune Kaydet (Export)")
        print("[6] Cikis (Exit)")
        
        choice = input("\nSeciminiz (1-6): ").strip()

        if choice == "1":
            url = input("Veri cekilecek URL adresini girin: ").strip()
            if url:
                print("Veri çekiliyor ve doğrulanıyor...")
                res = engine.engine.ingest_and_process_url(url) if hasattr(engine, 'engine') else engine.ingest_and_process_url(url)
                print("Sonuç:", res)
            else:
                print("Geçersiz URL!")

        elif choice == "2":
            print("\nconfig.json dosyasındaki kaynaklar taranıyor...")
            res = engine.ingest_all_from_config()
            print("Toplu Ingestion Sonucu:", res)

        elif choice == "3":
            print("\n--- HAVUZDA ARAMA VE FİLTRELEME ---")
            keyword = input("Aranacak anahtar kelime: ").strip()
            if keyword:
                results = engine.query_engine.search_by_keyword(keyword)
                print(f"\nBulunan Kayıt Sayısı: {len(results)}")
                for idx, r in enumerate(results, 1):
                    print(f"- [{idx}] Kaynak: {r.provenance} | Zaman: {r.timestamp}")
            else:
                print("Anahtar kelime boş olamaz!")

        elif choice == "4":
            report = engine.generate_report()
            print("\n--- ANALİTİK RAPOR ---")
            for k, v in report.items():
                print(f"{k}: {v}")

        elif choice == "5":
            report = engine.generate_report()
            result_msg = engine.analytics.export_report_to_desktop(report)
            print(f"\n{result_msg}")

        elif choice == "6":
            print("Terminal kapatılıyor. Görüşmek üzere!")
            scheduler.stop()
            sys.exit(0)
        else:
            print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()