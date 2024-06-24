import pandas as pd
import numpy as np


def ajustar_promedio(df, promedio_objetivo_min,promedio_objetivo_max,  condicion):
    # Calcular el promedio actual
    promedio_actual = df['value'].mean()
    df['dia'] = pd.to_datetime(df['dia'])
    # Establecer 'dia' como índice
    df.set_index('dia', inplace=True)
    # Comparar el promedio actual con el objetivo
    if promedio_objetivo_min <= promedio_actual <= promedio_objetivo_max:
        print("El promedio actual ya cumple con la condición.")
        return df

    # Determinar si necesitamos aumentar o disminuir el promedio
    necesita_aumentar = condicion == 'mayor'

    # Ordenar los valores a cambiar para minimizar cambios

    df_sorted = df.sort_values(by='value', ascending= necesita_aumentar).reset_index()
    print(df)
    # Modificar los valores respetando las restricciones
    valores_modificados = []
    promedio_objetivo = promedio_objetivo_max
    if promedio_actual< promedio_objetivo_min:
        promedio_objetivo = promedio_objetivo_min 
    diferencia_total = abs(promedio_objetivo - promedio_actual) * len(df) + np.random.randint(1, 4)
    if promedio_objetivo < promedio_actual:
        diferencia_total = 0 - diferencia_total
    difaleatoria = np.random.randint(2, 4)
    diferencia_parcial = diferencia_total
    print(difaleatoria)
    i = 0
    isrepeat= False
    while i < len(df_sorted):
        row = df_sorted.iloc[i]
        dia_original = row['dia']
        value_sorted = row['value']
        value_i = df_sorted.at[i, 'value']

        # Obtener vecinos del DataFrame original usando el índice original
        original_position = df.index.get_loc(dia_original)

        prev_value = df.iloc[original_position - 1]['value'] if original_position > 0 else None
        next_value = df.iloc[original_position + 1]['value'] if original_position < len(
            df) - 1 else None

        if ((prev_value is not None and next_value is not None)
                 and ((abs(value_i + diferencia_total - prev_value) < difaleatoria)
                 and (abs(value_i + diferencia_total - next_value) < difaleatoria))) and isrepeat == False:
            diferencia_parcial = diferencia_total

        elif prev_value is not None and (abs(value_i + diferencia_total - prev_value) > difaleatoria) \
                and isrepeat == False:
            diferencia_parcial = difaleatoria

        elif next_value is not None and (abs(value_i + diferencia_total - next_value) > difaleatoria)\
                and isrepeat == False:
            diferencia_parcial = difaleatoria

        else:
            if isrepeat == False:
                diferencia_parcial = diferencia_total


        if necesita_aumentar:
            incremento = min(diferencia_total, difaleatoria)  # Incremento máximo de 5 para no exceder la diferencia permitida
            df_sorted.at[i, 'value'] += diferencia_parcial
            df.iloc[original_position]['value']+= diferencia_parcial
        else:
            if diferencia_total < 0 and diferencia_parcial >0:
                diferencia_parcial = diferencia_parcial*(-1)
            if df_sorted.at[i, 'value'] + diferencia_parcial <0:
                diferencia_parcial = diferencia_parcial - (df_sorted.at[i, 'value'] + diferencia_parcial)
            if df_sorted.at[i, 'value'] + diferencia_parcial ==0:
                diferencia_parcial += 1
            df_sorted.at[i, 'value'] += diferencia_parcial
            df.iloc[original_position]['value']+= diferencia_parcial

        valores_modificados.append(df_sorted.at[i, 'value'])
        diferencia_total = (diferencia_total - (diferencia_parcial))

        # Verificar si ya alcanzamos el objetivo
        if ((condicion == 'mayor' and df['value'].mean() >= promedio_objetivo) or (
                condicion == 'menor' and df['value'].mean() <= promedio_objetivo)) and diferencia_total == 0:
            break
        # Verificar si podemos incrementar mas el mismo registro antes de iterar
        value_i = int(df.iloc[original_position]['value'])
        pv = int((df.iloc[original_position]['value'] - prev_value)) if prev_value is not None else None
        nv = int((df.iloc[original_position]['value'] - next_value)) if next_value is not None else None

        if ((prev_value is not None and abs(pv) < difaleatoria and value_i>1) or \
                (next_value is not None and abs(nv) < difaleatoria and value_i>1)):
            diferencia_parcial = difaleatoria - pv if pv is not None and \
                                                      abs(pv < difaleatoria) else difaleatoria - nv
            isrepeat = True
        else:
            i+=1
            isrepeat = False
    # Asignar los valores modificados al dataframe original
    #df['value'] = valores_modificados
    df = df.sort_values(by='dia', ascending=True)
    return df


# Ejemplo de uso
data = {
    'dia': ['2023-06-20', '2023-06-21', '2023-06-22', '2023-06-23'],
    'value': [6, 3, 3, 6]
}
df = pd.DataFrame(data)
promedio_objetivo = 5
condicion = 'mayor'

df_ajustado = ajustar_promedio(df, promedio_objetivo, condicion)
print(df_ajustado)
print(df_ajustado['value'].mean())



