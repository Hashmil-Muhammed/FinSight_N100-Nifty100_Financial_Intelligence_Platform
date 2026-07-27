import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os


def generate_radar_charts(db_path="nifty100.db", output_dir="reports/radar_charts"):
    print("\n Generating Plotly radar charts...")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Read the latest year data from peer_percentiles
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(
            """
                         SELECT * FROM peer_percentiles
                         WHERE year = (SELECT MAX(year) FROM peer_percentiles)
                         """,
            conn,
        )
    metrics_to_plot = [
        "ROE_Rank",
        "ROCE_Rank",
        "Net_Profit_Margin_Rank",
        "PAT_CAGR_5Y_Rank",
        "Debt_to_Equity_Rank",
    ]
    labels = ["ROE", "ROCE", "Net Profit Margin", "PAT CAGR (5Y)", "Debt safety"]

    # Dynamically find the actual peer group column name
    peer_group_col = [
        col
        for col in df.columns
        if col.lower() not in ["company_id", "year"] and not col.endswith("_Rank")
    ][0]

    count = 0
    for _, row in df.iterrows():
        company = row["company_id"]
        peer_group = row[peer_group_col]

        # Extract values and close the polygon (append first value at the end)
        values = [row.get(m, 0) for m in metrics_to_plot]
        values.append(values[0])
        theta = labels + [labels[0]]

        fig = go.Figure()

        # Add Peer Group Median (50th Percentile benchmark)
        fig.add_trace(
            go.Scatterpolar(
                r=[50, 50, 50, 50, 50, 50],
                theta=theta,
                fill="toself",
                name=f"{peer_group} Median",
                line_color="grey",
                opacity=0.4,
            )
        )

        # Add Company Performance
        fig.add_trace(
            go.Scatterpolar(
                r=values, theta=theta, fill="toself", name=company, line_color="#0A9EDC"
            )
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title=f"Peer Comparison: {company} vs {peer_group}",
        )

        # Save as PNG
        file_path = os.path.join(output_dir, f"{company}_radar.png")
        fig.write_image(file_path, width=800, height=600)
        count += 1

    print(f"Successfully generated {count} Radar Chart PNGs in '{output_dir}'")


if __name__ == "__main__":
    generate_radar_charts()
