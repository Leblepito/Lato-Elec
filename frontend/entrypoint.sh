#!/bin/sh
echo "ElectroPMS Frontend starting on port ${PORT:-3000}"
exec npx serve -s dist -l ${PORT:-3000}
