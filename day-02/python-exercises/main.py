import csv
from collections import defaultdict
from typing import Any


class StudentDataAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.headers: list[str] = []
        self.records: list[dict[str, str]] = []
        self._load_data()

    def _load_data(self) -> None:
        """Reads the CSV file and stores raw rows."""
        with open(self.filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.headers = [h.strip() for h in (reader.fieldnames or [])]
            for row in reader:
                # Strip keys and values to normalize whitespace
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                self.records.append(cleaned_row)

    def total_records(self) -> int:
        return len(self.records)

    def missing_values_report(self) -> dict[str, int]:
        """Counts empty or whitespace-only values per column."""
        missing = {header: 0 for header in self.headers}
        for row in self.records:
            for header in self.headers:
                val = row.get(header, "")
                if val is None or val == "":
                    missing[header] += 1
        return missing

    def duplicate_count(self, primary_key: str | None = None) -> int:
        """
        Counts duplicates. If primary_key is supplied, checks for duplicated IDs.
        Otherwise, checks for completely identical rows.
        """
        seen = set()
        duplicates = 0

        for row in self.records:
            if primary_key:
                identifier = row.get(primary_key, "")
            else:
                identifier = tuple(sorted(row.items()))

            if identifier in seen:
                duplicates += 1
            else:
                seen.add(identifier)

        return duplicates

    def numeric_stats(self, column: str) -> dict[str, float | None]:
        """Calculates min, max, and average for a numeric column."""
        values: list[float] = []
        for row in self.records:
            val_str = row.get(column, "")
            try:
                values.append(float(val_str))
            except ValueError:
                continue

        if not values:
            return {"count": 0, "min": None, "max": None, "average": None}

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "average": round(sum(values) / len(values), 2)
        }

    def category_stats(self, category_col: str, metric_col: str) -> dict[str, dict[str, Any]]:
        """Computes count, min, max, and average of a metric grouped by category."""
        grouped: dict[str, list[float]] = defaultdict(list)

        for row in self.records:
            category = row.get(category_col, "Unknown") or "Unknown"
            metric_str = row.get(metric_col, "")
            try:
                grouped[category].append(float(metric_str))
            except ValueError:
                continue

        stats = {}
        for cat, values in grouped.items():
            if values:
                stats[cat] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "average": round(sum(values) / len(values), 2)
                }
        return stats

    def generate_report(self, id_col: str, score_col: str, group_col: str) -> None:
        """Prints a comprehensive diagnostic summary."""
        print("=" * 45)
        print(" STUDENT CSV ANALYSIS REPORT ")
        print("=" * 45)
        print(f"Total Rows Processed: {self.total_records()}")
        print(f"Duplicate Rows (Exact): {self.duplicate_count()}")
        print(f"Duplicate IDs ({id_col}): {self.duplicate_count(primary_key=id_col)}")

        print("\n--- Missing Values by Column ---")
        for col, count in self.missing_values_report().items():
            print(f"  {col}: {count}")

        print(f"\n--- Overall Numeric Stats ({score_col}) ---")
        stats = self.numeric_stats(score_col)
        print(f"  Valid entries: {stats['count']}")
        print(f"  Minimum: {stats['min']}")
        print(f"  Maximum: {stats['max']}")
        print(f"  Average: {stats['average']}")

        print(f"\n--- Grouped Stats ({score_col} by {group_col}) ---")
        cat_stats = self.category_stats(category_col=group_col, metric_col=score_col)
        for cat, data in cat_stats.items():
            print(f"  [{cat}] -> Count: {data['count']} | Min: {data['min']} | Max: {data['max']} | Avg: {data['average']}")
        print("=" * 45)


# --- Example Usage ---
if __name__ == "__main__":
    # Create sample CSV
    sample_csv = "students.csv"
    with open(sample_csv, "w", newline="", encoding="utf-8") as f:
        f.write(
            "student_id,name,grade_level,score\n"
            "101,Alice,10,88.5\n"
            "102,Bob,10,92.0\n"
            "103,Charlie,11,\n"       # Missing score
            "104,,11,75.0\n"          # Missing name
            "101,Alice,10,88.5\n"     # Duplicate record
            "105,David,12,64.0\n"
            "106,Eva,12,98.5\n"
        )

    # Initialize and run report
    analyzer = StudentDataAnalyzer(sample_csv)
    analyzer.generate_report(id_col="student_id", score_col="score", group_col="grade_level")
