format:
	poetry run ruff check . --fix
	poetry run ruff format .

typecheck:
	poetry run basedpyright

alembic-revision:
	poetry run alembic revision --autogenerate -m "$(message)"

alembic-upgrade:
	poetry run alembic upgrade head

dev:
	poetry run uvicorn app.main:app --reload

seed:
	poetry run python -m sample_data.seed
