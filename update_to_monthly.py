#!/usr/bin/env python3
"""
Script para actualizar el notebook a análisis mensual
"""
import json
import re

# Leer notebook
with open('notebooks/02_estrategia_cobertura_put_spy.ipynb', 'r') as f:
    nb = json.load(f)

print("="*80)
print("ACTUALIZANDO NOTEBOOK A ANÁLISIS MENSUAL")
print("="*80 + "\n")

cambios = 0

# Recorrer todas las celdas
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'source' in cell:
        source_lines = cell['source']
        source_text = ''.join(source_lines)
        modificado = False
        
        # 1. Actualizar función calculate_metrics
        if 'def calculate_metrics(returns, portfolio_values' in source_text:
            print(f"✓ Celda {i}: Actualizando calculate_metrics para MENSUAL")
            
            # Reemplazar days/252 por months/12
            for j, line in enumerate(source_lines):
                if '# Retorno anualizado' in line:
                    # Encontrar las siguientes líneas y reemplazarlas
                    if j+2 < len(source_lines) and 'days = len(returns)' in source_lines[j+1]:
                        source_lines[j+1] = '    months = len(returns)\n'
                        source_lines[j+2] = '    years = months / 12\n'
                        modificado = True
                
                elif '# Volatilidad anualizada' in line:
                    if j+1 < len(source_lines) and 'np.sqrt(252)' in source_lines[j+1]:
                        source_lines[j+1] = '    volatility = returns.std() * np.sqrt(12) * 100\n'
                        modificado = True
                
                elif '# Sharpe Ratio' in line:
                    if j+1 < len(source_lines) and '/ 252' in source_lines[j+1]:
                        source_lines[j+1] = '    risk_free_monthly = (risk_free_rate_avg / 12)\n'
                    if j+2 < len(source_lines) and 'excess_returns = returns -' in source_lines[j+2]:
                        source_lines[j+2] = '    excess_returns = returns - risk_free_monthly\n'
                    if j+3 < len(source_lines) and 'np.sqrt(252)' in source_lines[j+3]:
                        source_lines[j+3] = '    sharpe = np.sqrt(12) * excess_returns.mean() / returns.std()\n'
                        modificado = True
                
                elif 'downside_std = downside_returns.std() * np.sqrt(252)' in line:
                    source_lines[j] = '    downside_std = downside_returns.std() * np.sqrt(12)\n'
                    modificado = True
            
            if modificado:
                cambios += 1
        
        # 2. Actualizar preparación de datos para resamplear a mensual
        elif 'protected_df = pd.DataFrame(protected_strategy.portfolio_values)' in source_text:
            if '# Calcular retornos diarios' in source_text:
                print(f"✓ Celda {i}: Actualizando preparación de datos a MENSUAL")
                
                # Reemplazar todo el bloque
                new_lines = [
                    '# Convertir resultados a DataFrames (DIARIOS)\n',
                    'protected_df = pd.DataFrame(protected_strategy.portfolio_values).set_index(\'date\')\n',
                    'buy_hold_df = pd.DataFrame(buy_hold_strategy.portfolio_values).set_index(\'date\')\n',
                    '\n',
                    'print("\\n📊 RESAMPLEANDO A DATOS MENSUALES (fin de mes)...")\n',
                    '\n',
                    '# Resamplear a MENSUAL (último día de cada mes)\n',
                    'protected_monthly = protected_df.resample(\'M\').last()\n',
                    'buy_hold_monthly = buy_hold_df.resample(\'M\').last()\n',
                    '\n',
                    '# Crear DataFrame comparativo MENSUAL\n',
                    'comparison_df = pd.DataFrame({\n',
                    '    \'protected\': protected_monthly[\'portfolio_value\'],\n',
                    '    \'buy_hold\': buy_hold_monthly[\'portfolio_value\']\n',
                    '})\n',
                    '\n',
                    '# Calcular retornos MENSUALES\n',
                    'comparison_df[\'protected_returns\'] = comparison_df[\'protected\'].pct_change()\n',
                    'comparison_df[\'buy_hold_returns\'] = comparison_df[\'buy_hold\'].pct_change()\n',
                    '\n',
                    'comparison_df = comparison_df.dropna()\n',
                    '\n',
                    'print(f"✓ Datos resampleados: {len(protected_df)} días → {len(comparison_df)} meses")\n',
                    'print(f"✓ Período: {comparison_df.index[0].strftime(\'%Y-%m\')} a {comparison_df.index[-1].strftime(\'%Y-%m\')}")\n',
                    'print("\\n✓ Resultados preparados para análisis comparativo (MENSUAL)")\n',
                    '\n',
                    'comparison_df.head()'
                ]
                
                cell['source'] = new_lines
                modificado = True
                cambios += 1
        
        # 3. Actualizar etiquetas de gráficos
        elif 'Distribución Retornos Diarios' in source_text:
            print(f"✓ Celda {i}: Actualizando etiquetas de gráficos")
            for j, line in enumerate(source_lines):
                if 'Distribución Retornos Diarios' in line:
                    source_lines[j] = line.replace('Diarios', 'Mensuales')
                    modificado = True
                elif 'Retorno Diario (%)' in line:
                    source_lines[j] = line.replace('Diario', 'Mensual')
                    modificado = True
            
            if modificado:
                cambios += 1
        
        # 4. Actualizar ventana de retornos rodantes
        elif 'window = 252' in source_text:
            print(f"✓ Celda {i}: Actualizando ventana de retornos rodantes")
            for j, line in enumerate(source_lines):
                if 'window = 252' in line:
                    source_lines[j] = 'window = 12  # 12 meses = 1 año\n'
                    modificado = True
                elif 'Retornos Rodantes a 1 Año (252 días)' in line:
                    source_lines[j] = line.replace('(252 días)', '(12 meses)')
                    modificado = True
            
            if modificado:
                cambios += 1

# Guardar notebook
with open('notebooks/02_estrategia_cobertura_put_spy.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n{'='*80}")
print(f"✅ COMPLETADO: {cambios} secciones actualizadas")
print(f"{'='*80}")

