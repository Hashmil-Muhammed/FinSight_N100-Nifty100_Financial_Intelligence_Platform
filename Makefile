load:
	python src/etl/loader.py

ratios:
	python src/analytics/ratios.py

test:
	python -m pytest tests/ --html=reports/pytest_report.html

report:
	python src/reports/portfolio_report.py

dashboard:
	streamlit run src/dashboard/app.py

api:
	uvicorn src.api.main:app --port 8000 --reload