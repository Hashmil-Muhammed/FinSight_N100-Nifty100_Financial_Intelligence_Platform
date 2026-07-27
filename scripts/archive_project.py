import os
import shutil

def create_archive():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "output", "final_deliverables")
    os.makedirs(target_dir, exist_ok=True)

    files_to_copy = [
        "README.md",
        "nifty100.db",
        "pytest_report.html",
        "docs/analyst_guide.pdf",
        "output/perf_notes.md"
    ]

    print("Archiving Deliverables...")
    for file_path in files_to_copy:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            shutil.copy(full_path, target_dir)
            print(f" Copied: {os.path.basename(file_path)}")
        else:
            print(f" Missing: {file_path} (Please generate it first)")

    print(f"\n All deliverables archived successfully to: {target_dir}")

if __name__ == "__main__":
    create_archive()