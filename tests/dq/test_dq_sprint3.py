import sqlite3
import pandas as pd
import os


def run_sprint3_dq_tests(db_path="nifty100.db"):
    print("\n Starting Sprint 3 Data Quality(DQ) tests...")

    if not os.path.exists(db_path):
        print(f"Fail: Database file '{db_path}' not found!")
        return False

    try:
        conn = sqlite3.connect(db_path)

        # Test 1: Check if peer_percentiles table exists and has data
        df_peer = pd.read_sql("SELECT * FROM peer_percentiles", conn)
        if df_peer.empty:
            print("FAIL: peer_percentiles table is empty!")
            return False
        print("PASS: 'peer_percentiles' table exists and contains data")

        # Test 2: Check if Ranks are valid (between 0 and 100)
        rank_cols = [col for col in df_peer.columns if "Rank" in col]
        invalid_ranks_found = False
        for col in rank_cols:
            invalid = df_peer[(df_peer[col] < 0) | (df_peer[col] > 100)]
            if not invalid.empty:
                invalid_ranks_found = True
        if invalid_ranks_found:
            print("FAIL: Found invalid ranks (outside 0-100 bounds)")
            return False
        print("PASS: All calculated ranks are within valid bounds (0-100)")

        # Test 3: Check for blank Peer Groups
        null_groups = df_peer[df_peer["peer_group_name"].isnull()]
        if not null_groups.empty:
            print("FAIL: Found companies with no peer_group_name")
            return False
        print("PASS : All companies are assigned to a valid peer group")

        print("\n All Tests Green! Sprint 3 DQ Passed Successfully.")
        return True

    except Exception as e:
        print(f"Error During testing: {str(e)}")
        return False
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    run_sprint3_dq_tests()
