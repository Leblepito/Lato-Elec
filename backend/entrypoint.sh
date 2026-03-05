#!/bin/sh
echo "ElectroPMS Backend starting on port ${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
