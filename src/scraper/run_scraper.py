import sys

sys.path.append("src/scraper")

from scraper.erowid_scraper import ErowidScraper
import pandas as pd


def main():
    print("🚀 Starting Erowid Trip Report Scraper")
    print("=" * 50)

    # Initialize scraper
    scraper = ErowidScraper()

    # Start with a small test
    print("📝 Testing with 5 reports first...")
    test_reports = scraper.scrape_reports(num_reports=5)

    if test_reports:
        print(f"✅ Test successful! Scraped {len(test_reports)} reports")

        # Show sample data
        sample = test_reports[0]
        print("\n📊 Sample report structure:")
        for key, value in sample.items():
            if key == "experience_text":
                print(f"  {key}: {str(value)[:100]}..." if value else f"  {key}: None")
            else:
                print(f"  {key}: {value}")

        # Save test data
        scraper.save_data("data/scraped/test_reports.json")

        # Ask user if they want to continue with full scraping
        response = input(
            "\n🤔 Test successful! Continue with full scraping (200 reports)? (y/n): "
        )

        if response.lower() == "y":
            print("\n🏃‍♂️ Starting full scraping...")
            all_reports = scraper.scrape_reports(num_reports=200)
            scraper.save_data("data/scraped/all_reports.json")

            # Basic statistics
            df = pd.DataFrame(all_reports)
            print(f"\n📈 Scraping Complete!")
            print(f"Total reports: {len(all_reports)}")
            print(
                f"Average text length: {df['experience_text'].str.len().mean():.0f} characters"
            )
            print(f"Reports with substance info: {df['substance'].notna().sum()}")

    else:
        print("❌ Test failed. Check the scraper configuration and website structure.")
        print("\n🔧 Debugging tips:")
        print("1. Check if Erowid.org is accessible")
        print("2. Inspect the HTML structure of experience pages")
        print("3. Update CSS selectors in erowid_scraper.py")
        print("4. Check robots.txt compliance")


if __name__ == "__main__":
    main()
