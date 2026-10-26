# PayFlow Control Plane

## Run checks

- Python 3.11+
- Node.js 22+

```powershell
python -m pip install -e ".[dev]"
pytest -q
ruff check .
cd dashboard
npm install
npm run build
```

The API starts with `uvicorn payflow.api:app --reload` from the repository root. The dashboard starts with `npm run dev` from `dashboard/`.
