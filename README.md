# Backtesting S&P Options

Proyecto de backtesting para opciones del S&P 500.

## Configuración del Entorno

### 1. Crear entorno virtual

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En macOS/Linux:
source .venv/bin/activate
# En Windows:
# .venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus propias configuraciones
```

### 4. Iniciar Jupyter Notebook

```bash
jupyter notebook
# o para JupyterLab:
jupyter lab
```

## Librerías Incluidas (Versiones Actualizadas 2025)

### Análisis de Datos
- **pandas** (>=2.2.3): Manipulación y análisis de datos
- **numpy** (>=1.26.4): Computación numérica
- **scipy** (>=1.14.1): Algoritmos científicos

### Visualización
- **matplotlib** (>=3.9.2): Gráficos estáticos
- **seaborn** (>=0.13.2): Visualizaciones estadísticas
- **plotly** (>=5.24.1): Gráficos interactivos

### Datos Financieros
- **yfinance** (>=0.2.48): Descarga de datos de Yahoo Finance
- **pandas-datareader** (>=0.10.0): Múltiples fuentes de datos financieros

### Backtesting
- **backtrader** (>=1.9.78.123): Framework completo de backtesting
- **backtesting** (>=0.3.3): Framework ligero y moderno

### Análisis Técnico
- **ta** (>=0.11.0): Indicadores técnicos
- **pandas-ta** (>=0.3.14b): Análisis técnico con pandas
- **statsmodels** (>=0.14.4): Modelos estadísticos
- **scikit-learn** (>=1.5.2): Machine learning

### Opciones y Métricas
- **py_vollib** (>=1.0.1): Volatilidad implícita y greeks de opciones
- **mibian** (>=0.1.3): Cálculo de precios de opciones (Black-Scholes, etc.)
- **pyfolio-reloaded** (>=0.9.5): Análisis de rendimiento de portafolio
- **quantstats** (>=0.0.62): Métricas cuantitativas

## Estructura de Proyecto Sugerida

```
backtesting_SP_options/
├── data/              # Datos descargados
├── notebooks/         # Jupyter notebooks
├── src/              # Código fuente
│   ├── strategies/   # Estrategias de trading
│   ├── indicators/   # Indicadores personalizados
│   └── utils/        # Utilidades
├── results/          # Resultados de backtests
├── .env             # Variables de entorno (no subir a git)
├── .env.example     # Plantilla de variables de entorno
├── requirements.txt  # Dependencias
└── README.md        # Este archivo
```

## Notebooks Disponibles

1. **01_ejemplo_backtesting_opciones_sp500.ipynb**
   - Estrategia de Put Credit Spread
   - Ejemplo básico de backtesting con opciones

2. **02_estrategia_cobertura_put_spy.ipynb**
   - Estrategia de cobertura con PUT 10% OTM
   - Comparación con Buy & Hold
   - Análisis conservador con costes reales

## Uso Básico

```python
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Descargar datos
ticker = yf.Ticker("SPY")
data = ticker.history(period="1y")

# Tu código de backtesting aquí
```

## Notas

- Asegúrate de tener Python 3.10 o superior instalado (recomendado Python 3.11+)
- Para usar algunas APIs necesitarás registrarte y obtener claves API gratuitas
- El archivo `.env` debe estar en `.gitignore` para no exponer tus API keys
- El `requirements.txt` usa operadores `>=` para instalar las últimas versiones compatibles

### Verificar Versiones Instaladas

```bash
# Ver versiones instaladas
pip list | grep -E "pandas|numpy|matplotlib|yfinance|jupyter"

# Actualizar todas las librerías a sus últimas versiones
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

## Recursos

- [Documentación de Backtrader](https://www.backtrader.com/docu/)
- [Documentación de Backtesting.py](https://kernc.github.io/backtesting.py/)
- [yfinance en PyPI](https://pypi.org/project/yfinance/)

