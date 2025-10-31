#!/bin/bash
# Script para activar el entorno virtual de backtesting

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}  Entorno de Backtesting S&P Options${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activar entorno virtual
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    echo -e "${GREEN}✓ Entorno virtual activado${NC}"
    echo ""
    echo -e "Python version: ${BLUE}$(python --version)${NC}"
    echo ""
    echo -e "${GREEN}Comandos disponibles:${NC}"
    echo "  - jupyter lab          : Iniciar JupyterLab"
    echo "  - jupyter notebook     : Iniciar Jupyter Notebook"
    echo "  - deactivate          : Desactivar entorno"
    echo ""
    echo -e "${GREEN}Notebooks disponibles:${NC}"
    echo "  - notebooks/01_ejemplo_backtesting_opciones_sp500.ipynb"
    echo ""
else
    echo -e "${RED}✗ Error: No se encontró el entorno virtual${NC}"
    echo "Por favor ejecuta: python3 -m venv .venv"
    exit 1
fi

