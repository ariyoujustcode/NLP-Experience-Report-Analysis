import pandas as pd
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict


class AlternativeDataCollector:
    """Collect trip report data from alternative sources"""

    def __init__(self):
        self.substances = [
            "LSD",
            "Psilocybin",
            "MDMA",
            "DMT",
            "Mescaline",
            "Cannabis",
            "Ketamine",
            "2C-B",
            "Ayahuasca",
        ]

        self.experience_types = [
            "positive",
            "mixed",
            "difficult",
            "neutral",
            "transformative",
        ]

        self.intensities = ["mild", "moderate", "strong", "overwhelming"]

    def generate_synthetic_reports(self, num_reports: int = 200) -> List[Dict]:
        """Generate synthetic trip reports for model development"""

        print(f"Generating {num_reports} synthetic trip reports...")

        reports = []
        for i in range(num_reports):
            report = self._generate_single_report(i)
            reports.append(report)

        return reports

    def _generate_single_report(self, report_id: int) -> Dict:
        """Generate a single synthetic report"""

        substance = random.choice(self.substances)
        experience_type = random.choice(self.experience_types)
        intensity = random.choice(self.intensities)

        # Generate realistic-looking synthetic text
        experience_templates = {
            "positive": [
                f"My experience with {substance} was incredible. The visuals were beautiful and I felt a deep connection to nature. The come-up took about 45 minutes and lasted for 6 hours. I experienced enhanced creativity and emotional openness.",
                f"This {substance} trip was life-changing. I had profound insights about my relationships and felt overwhelming love and compassion. The peak lasted about 2 hours with gentle aftereffects.",
            ],
            "difficult": [
                f"My {substance} experience was challenging. I felt anxious during the come-up and had some difficult thoughts. However, I learned a lot about myself and felt better after integration.",
                f"This {substance} trip was intense and overwhelming at times. I experienced some fear and confusion but had support from friends. The experience taught me about facing difficult emotions.",
            ],
            "mixed": [
                f"My {substance} experience had both positive and challenging aspects. Beautiful visuals mixed with some anxiety. Overall transformative but required careful integration.",
                f"This {substance} trip was a roller coaster. Moments of pure bliss alternated with periods of introspection and mild discomfort. Glad I had a safe setting.",
            ],
        }

        base_text = random.choice(
            experience_templates.get(experience_type, experience_templates["positive"])
        )

        # Add substance-specific details
        if substance == "LSD":
            base_text += " The geometric patterns were intricate and the time dilation was significant."
        elif substance == "Psilocybin":
            base_text += " The natural setting enhanced the mushroom experience with earthy visuals."
        elif substance == "MDMA":
            base_text += (
                " The empathogenic effects were strong with enhanced social connection."
            )

        report = {
            "report_id": f"synthetic_{report_id:04d}",
            "substance": substance,
            "experience_type": experience_type,
            "intensity": intensity,
            "experience_text": base_text,
            "age": random.randint(18, 65),
            "weight": f"{random.randint(120, 220)} lbs",
            "dosage": self._generate_dosage(substance),
            "duration": f"{random.randint(4, 12)} hours",
            "setting": random.choice(["home", "nature", "festival", "therapeutic"]),
            "generated_at": datetime.now().isoformat(),
            "data_source": "synthetic",
        }

        return report

    def _generate_dosage(self, substance: str) -> str:
        """Generate realistic dosage information"""
        dosages = {
            "LSD": [f"{random.randint(50, 300)} μg"],
            "Psilocybin": [f"{random.randint(1, 5)} g dried"],
            "MDMA": [f"{random.randint(80, 150)} mg"],
            "Cannabis": [f"{random.randint(1, 5)} joints"],
            "DMT": [f"{random.randint(20, 50)} mg vaporized"],
        }
        return random.choice(dosages.get(substance, ["Unknown dosage"]))

    def collect_reddit_data(self):
        """Placeholder for Reddit API collection"""
        print("Reddit data collection would require:")
        print("1. Reddit API credentials")
        print("2. PRAW library installation")
        print("3. Compliance with Reddit API terms")
        print("4. Subreddit: r/Psychonaut, r/Drugs, r/TripReports")

        # Implementation would go here with proper API usage
        pass

    def save_data(self, reports: List[Dict], filepath: str):
        """Save collected data"""
        # Save as JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2, ensure_ascii=False)

        # Save as CSV
        csv_filepath = filepath.replace(".json", ".csv")
        df = pd.DataFrame(reports)
        df.to_csv(csv_filepath, index=False)

        print(f"Data saved to {filepath} and {csv_filepath}")


# Academic/Research data source suggestions
class ResearchDataSources:
    """Information about legitimate research data sources"""

    @staticmethod
    def print_sources():
        sources = {
            "MAPS": {
                "description": "Multidisciplinary Association for Psychedelic Studies",
                "url": "https://maps.org/research-archive",
                "data_type": "Clinical trial data, research papers",
            },
            "PsychonautWiki": {
                "description": "Harm reduction database with API",
                "url": "https://psychonautwiki.org/",
                "data_type": "Substance information, experience reports",
            },
            "Heffter Research Institute": {
                "description": "Psilocybin research data",
                "url": "https://heffter.org/",
                "data_type": "Clinical research findings",
            },
            "Usona Institute": {
                "description": "Psilocybin therapy research",
                "url": "https://www.usonainstitute.org/",
                "data_type": "Clinical trial data",
            },
        }

        print("Legitimate Research Data Sources:")
        print("=" * 50)
        for name, info in sources.items():
            print(f"\n{name}:")
            print(f"  Description: {info['description']}")
            print(f"  URL: {info['url']}")
            print(f"  Data Type: {info['data_type']}")


# Example usage
if __name__ == "__main__":
    # Generate synthetic data for development
    collector = AlternativeDataCollector()

    # Create synthetic dataset
    synthetic_reports = collector.generate_synthetic_reports(200)
    collector.save_data(synthetic_reports, "data/scraped/synthetic_reports.json")

    # Show research sources
    ResearchDataSources.print_sources()

    print("\nNext steps:")
    print("1. Use synthetic data to develop your NLP pipeline")
    print("2. Contact research institutions for real data access")
    print("3. Apply for IRB approval if conducting research")
    print("4. Consider partnering with existing research groups")
