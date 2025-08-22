import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import urllib3
import re
import os
from datetime import datetime
from typing import List, Dict, Optional
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import logging


class ErowidScraper:
    def __init__(
        self, base_url: str = "https://erowid.org", delay_range: tuple = (1, 3)
    ):
        self.base_url = base_url
        self.delay_range = delay_range
        self.session = requests.Session()
        self.ua = UserAgent()
        self.scraped_reports = []

        # Setup logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Headers to appear more human-like
        self.session.headers.update(
            {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }
        )

        # Disable SSL verification to handle certificate issues
        self.session.verify = False
        # Suppress SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_experience_urls(self, substance: str = None, limit: int = 200) -> List[str]:
        """Get URLs of individual experience reports"""
        # Erowid experience browse URL
        browse_url = f"{self.base_url}/experiences/exp_list.shtml"

        try:
            response = self.session.get(browse_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Find experience links (adjust selector based on actual HTML structure)
            experience_links = []

            # Look for experience links - these typically have pattern like exp.cgi?ID=12345
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "exp.php?ID=" in href or "/exp/" in href:
                    full_url = urljoin(self.base_url, href)
                    experience_links.append(full_url)

            self.logger.info(f"Found {len(experience_links)} experience URLs")
            return experience_links[:limit] if limit else experience_links

        except Exception as e:
            self.logger.error(f"Error getting experience URLs: {e}")
            return []

    def scrape_single_report(self, url: str) -> Optional[Dict]:
        """Scrape a single trip report"""
        try:
            # Random delay to be respectful
            time.sleep(random.uniform(*self.delay_range))

            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            report_data = {
                "url": url,
                "scraped_at": datetime.now().isoformat(),
            }

            # Extract report ID from URL
            if "ID=" in url:
                report_data["report_id"] = url.split("ID=")[1].split("&")[0]

            # Extract main content - adjust selectors based on actual HTML structure
            # These are common patterns, but you'll need to inspect the actual pages

            # Title
            title_elem = soup.find("div", class_="title")
            if title_elem:
                report_data["title"] = title_elem.get_text().strip()

            # Substance information
            substance_elem = soup.find("td", class_="dosechart-substance")
            if substance_elem:
                # Navigate to get the actual substance value
                parent = substance_elem.parent
                if parent and parent.find_next_sibling():
                    report_data["substance"] = (
                        parent.find_next_sibling().get_text().strip()
                    )

            # Dosage
            dosage_elem = soup.find("td", class_="dosechart-amount")
            if dosage_elem:
                parent = dosage_elem.parent
                if parent and parent.find_next_sibling():
                    report_data["dosage"] = (
                        parent.find_next_sibling().get_text().strip()
                    )

            # Form of substance
            form_elem = soup.find("td", class_="dosechart-form")
            if form_elem:
                parent = form_elem.parent
                if parent and parent.find_next_sibling():
                    report_data["form"] = parent.find_next_sibling().get_text().strip()

            # Experience text - this is the main content we want
            # Look for the main experience text block
            experience_text = ""

            html_content = str(soup)

            # Find content between <!--startbody--> and <!--endbody--> (or similar ending comment)
            start_marker = "<!--Start Body-->"
            end_markers = ["<!--End Body-->", "<!--end report-text-surround-->"]

            start_index = html_content.find(start_marker)
            if start_index != -1:
                # Move past the start marker
                start_index += len(start_marker)

                # Find the end marker
                end_index = -1
                for end_marker in end_markers:
                    end_index = html_content.find(end_marker, start_index)
                    if end_index != -1:
                        break

                if end_index == -1:
                    # If no end marker found, take a reasonable chunk (e.g., next 10000 chars)
                    end_index = start_index + 10000

                # Extract the HTML between markers
                body_html = html_content[start_index:end_index]

                # Parse this chunk and extract clean text
                body_soup = BeautifulSoup(body_html, "html.parser")
                experience_text = body_soup.get_text().strip()

                # Clean up extra whitespace
                experience_text = re.sub(r"\s+", " ", experience_text)
                experience_text = re.sub(r"\n\s*\n", "\n\n", experience_text)

            report_data["experience_text"] = experience_text

            # Body weight
            weight_elem = soup.find("td", text="bodyweight-amount") or soup.find(
                text="Body Weight"
            )
            if weight_elem:
                parent = weight_elem.parent
                if parent and parent.find_next_sibling():
                    report_data["weight"] = (
                        parent.find_next_sibling().get_text().strip()
                    )

            # Only return if we got substantial content
            if len(report_data.get("experience_text", "")) > 100:
                self.logger.info(
                    f"Successfully scraped report: {report_data.get('report_id', 'unknown')}"
                )
                return report_data
            else:
                self.logger.warning(f"Insufficient content for report: {url}")
                return None

        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None

    def scrape_reports(
        self, num_reports: int = 200, substance: str = None
    ) -> List[Dict]:
        """Scrape multiple reports"""
        self.logger.info(f"Starting to scrape {num_reports} reports")

        # Get experience URLs
        experience_urls = self.get_experience_urls(
            substance=substance, limit=num_reports * 2
        )  # Get more URLs as backup

        if not experience_urls:
            self.logger.error("No experience URLs found")
            return []

        scraped_count = 0
        for url in experience_urls:
            if scraped_count >= num_reports:
                break

            report_data = self.scrape_single_report(url)
            if report_data:
                self.scraped_reports.append(report_data)
                scraped_count += 1

                # Save progress periodically
                if scraped_count % 10 == 0:
                    self.save_data(f"data/scraped/interim_reports_{scraped_count}.json")
                    self.logger.info(
                        f"Progress: {scraped_count}/{num_reports} reports scraped"
                    )

        self.logger.info(
            f"Scraping completed. Total reports: {len(self.scraped_reports)}"
        )
        return self.scraped_reports

    def save_data(self, filepath: str):
        """Save scraped data to JSON and CSV"""
        if not self.scraped_reports:
            self.logger.warning("No data to save")
            return

        # Save as JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.scraped_reports, f, indent=2, ensure_ascii=False)

        # Save as CSV
        csv_filepath = filepath.replace(".json", ".csv")
        df = pd.DataFrame(self.scraped_reports)
        df.to_csv(csv_filepath, index=False)

        self.logger.info(f"Data saved to {filepath} and {csv_filepath}")


# Example usage and testing
if __name__ == "__main__":
    # Test the scraper with a small number first
    scraper = ErowidScraper()

    # For testing, let's try to scrape just 5 reports first
    reports = scraper.scrape_reports(num_reports=5)

    if reports:
        scraper.save_data("data/scraped/test_reports.json")
        print(f"Successfully scraped {len(reports)} reports")
        print("Sample report keys:", list(reports[0].keys()) if reports else "None")
    else:
        print("No reports were scraped. Check the selectors and website structure.")
