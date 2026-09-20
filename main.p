elif choice == "3":
            report = engine.generate_report()
            print("\n--- ANALİTİK RAPOR ---")
            for k, v in report.items():
                print(f"{k}: {v}")

        elif choice == "4":
            report = engine.generate_report()
            result_msg = engine.analytics.export_report_to_desktop(report)
            print(f"\n{result_msg}")