#!/usr/bin/env python3
"""
Script para corregir el cálculo de drawdown usando retornos acumulados mensuales
"""
import json

with open('notebooks/02_estrategia_cobertura_put_spy.ipynb', 'r') as f:
    nb = json.load(f)

print("="*80)
print("CORRIGIENDO CÁLCULO DE DRAWDOWN MENSUAL")
print("="*80 + "\n")

# Buscar la celda de calculate_metrics
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        if 'def calculate_metrics(returns, portfolio_values' in source:
            print(f"✓ Celda {i}: Actualizando calculate_metrics")
            
            # Nueva función que calcula drawdown correctamente desde retornos acumulados
            new_function = '''def calculate_metrics(returns, portfolio_values, initial_capital, strategy_name, risk_free_rate_avg):
    """
    Calcula métricas de rendimiento para una estrategia.
    IMPORTANTE: Esta función espera RETORNOS MENSUALES.
    """
    final_value = portfolio_values.iloc[-1]
    total_return = (final_value / initial_capital - 1) * 100
    
    # Retorno anualizado
    months = len(returns)
    years = months / 12
    annualized_return = ((final_value / initial_capital) ** (1 / years) - 1) * 100
    
    # Volatilidad anualizada (retornos mensuales → anuales)
    volatility = returns.std() * np.sqrt(12) * 100
    
    # Sharpe Ratio (con retornos mensuales)
    risk_free_monthly = (risk_free_rate_avg / 12)
    excess_returns = returns - risk_free_monthly
    sharpe = np.sqrt(12) * excess_returns.mean() / returns.std() if returns.std() > 0 else np.nan
    
    # Sortino Ratio (solo considera volatilidad negativa)
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std() * np.sqrt(12)
    sortino = (annualized_return / 100 - risk_free_rate_avg) / downside_std if downside_std > 0 else np.nan
    
    # Máximo Drawdown - CALCULADO DESDE RETORNOS ACUMULADOS MENSUALES
    # Esto evita el problema de tomar valores al final del mes después de pagar primas
    cumulative_returns = (1 + returns).cumprod()
    cumulative_values = initial_capital * cumulative_returns
    cummax = cumulative_values.cummax()
    drawdown = (cumulative_values - cummax) / cummax * 100
    max_drawdown = drawdown.min()
    
    # Ratio Calmar
    calmar = annualized_return / abs(max_drawdown) if max_drawdown != 0 else np.nan
    
    metrics = {
        'Estrategia': strategy_name,
        'Retorno Total (%)': total_return,
        'Retorno Anualizado (%)': annualized_return,
        'Volatilidad Anual (%)': volatility,
        'Sharpe Ratio': sharpe,
        'Sortino Ratio': sortino,
        'Max Drawdown (%)': max_drawdown,
        'Ratio Calmar': calmar,
        'Valor Final ($)': final_value
    }
    
    return metrics, drawdown'''
            
            cell['source'] = new_function.split('\n')
            if not cell['source'][-1]:
                pass
            else:
                cell['source'].append('')
            
            print("  → Drawdown ahora se calcula desde RETORNOS ACUMULADOS MENSUALES")
            print("  → Esto evita el sesgo de tomar valores justo después de pagar primas")
            break

# Guardar
with open('notebooks/02_estrategia_cobertura_put_spy.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("\n✅ Corrección aplicada")
print("="*80)

