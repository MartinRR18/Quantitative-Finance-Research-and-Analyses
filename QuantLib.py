'''
Autor: A. Martín Ramírez Rabelo
Fecha: 11.06.2024

Descripción:
Programa para analisis de retornos simples y multiescala o de tendencia de datos financieros.
- Funciones de descarga, lectura, escritura, de preprocesamiento de datos.
	-Genera retornos logaritmicos de los datos de precios de cierre.
    -Genera precios a partir de retornos logaritmicos.
	-Genera los trends y sus LogReturns
	-Separación de retornos positivos y negativos para analisis independiente.
- Diferentes funciones para la visualización de datos. 
	- CDF, PDF, Q-Qplots, HitPlots, KDEplots, Boxplots, etc
- Ajuste de datos a distribuciones teoricas por máxima verosimilitud a través de scipy.stats

- Funciones de normalización de datos
    - Normalización Min-Max
    - Normalización Estandar (media=0, std=1)
- Funciones de resampling de datos por días de trading o días calendario
- Funciones para graficar histogramas y duración de tendencias
- Funciones para ajuste de distribuciones a datos y graficar resultados
- Funciones para generación de tendencias y cálculo de duraciones
- Funciones para cálculo de rendimientos logarítmicos y conversión entre precios y retornos logarítmicos
'''
#Importacion de librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf #para descarga de datos
import numpy as np
import seaborn as sns
#import statsmodels.api as sm
from scipy.stats import kurtosis, skew
import scipy.stats as stats

#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#Funciones para descarga/extracción de datos de yf

def get_stock_data(ticker, start_date, end_date):
    '''Descarga de datos diarios de YahooFinance'''
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def get_stock_intday_data(ticker, start_date, end_date, interval):
    '''
    Descarga de datos intradia de YahooFinance.
    Si start_date y end_date son None, se escoge el máximo
    intervalo posible y más reciente para el 'interval' especificado.
    '''
    
    yf_kwargs = {'ticker': ticker, 'interval': interval}
    
    if start_date is None and end_date is None:
        if interval == '1m':
            yf_kwargs['period'] = '7d' # Máximo período para intervalos de 1 minuto (tier gratuito)
        elif interval in ['2m', '5m', '15m', '30m', '60m', '90m', '1h']:
            yf_kwargs['period'] = '2y' # Máximo período para estos intervalos intradía (tier gratuito)
        else: 
            # Para intervalos diarios, semanales, mensuales, o si el intervalo no es reconocido como intradía específico.
            # yfinance.download con period='max' usa un intervalo de '1d' por defecto si no se especifica.
            # Aquí, 'interval' ya está en yf_kwargs, por lo que se usará el 'interval' proporcionado.
            yf_kwargs['period'] = 'max'
        
        # Si se usa 'period', no se pasan 'start' ni 'end'.
        
    else: # Se proporciona start_date o end_date (o ambos)
        if start_date is not None:
            yf_kwargs['start'] = start_date
        if end_date is not None:
            yf_kwargs['end'] = end_date
        
        # 'interval' ya está en yf_kwargs desde la inicialización.

    stock_data = yf.download(**yf_kwargs)
    return stock_data

#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#Funciones de visualización de datos
def histograms4(ticker,df_PosRets,df_NegRets,df_PosTRets,df_NegTRets):
    # Crear una figura y dos subgráficas en una fila
    fig, axs = plt.subplots(2, 2, figsize=(12, 5))  # 2 fila, 2 columnas
    # Descomponer el arreglo de ejes en variables individuales
    ax1, ax2, ax3, ax4 = axs.flatten()  # Aplana el arreglo de ejes

    # Graficar en la primera subgráfica
    #ax1.plot(x1, y1, color='blue', label='LogRet_{ticker}')
    ax1.hist(df_PosRets, bins=100, alpha=0.7, color='blue', label=f'+LogSRet_{ticker}')
    ax1.set_title(f'{ticker} LogRets  Positivos')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Ocurrencias')
    ax1.legend()
    ax1.grid(True)
    # Graficar en la segunda subgráfica
    #ax2.plot(x2, y2, color='red', label='Log-TReturns') 
    ax2.hist(abs(df_NegRets), bins=100, alpha=0.7, color='green', label=f'-LogSRet_{ticker}')
    ax2.set_title(f'{ticker} LogRets Negativos')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Ocurrencias')
    ax2.legend()
    ax2.grid(True)
    # Graficar en la primera subgráfica
    #ax1.plot(x1, y1, color='blue', label='LogRet_{ticker}')
    ax3.hist(df_PosTRets, bins=100, alpha=0.7, color='black', label=f'+LogTRet_{ticker}')
    ax3.set_title(f'{ticker} Log-TRets Positivos')
    ax3.set_xlabel('Index')
    ax3.set_ylabel('Ocurrencias')
    ax3.legend()
    ax3.grid(True)
    # Graficar en la segunda subgráfica
    #ax2.plot(x2, y2, color='red', label='Log-TReturns') 
    ax4.hist(abs(df_NegTRets), bins=100, alpha=0.7, color='brown', label=f'-LogTRet_{ticker}')
    ax4.set_title(f'{ticker} Log-TRets Negativos')
    ax4.set_xlabel('Index')
    ax4.set_ylabel('Ocurrenciass')
    ax4.legend()
    ax4.grid(True)

    # Ajustar el layout
    plt.tight_layout()
    # Mostrar la figura
    plt.show()



def grafica2_cdf(ticker, df1, df2, name='string'):
    # Calcular la CDF
    sorted_data100 = np.sort(abs(df1))
    sorted_data1 = sorted_data100#[sorted_data100>.085]
    cdf1 = np.arange(1, len(sorted_data1) + 1) / len(sorted_data1)
    #if df2 != None: 
    sorted_data200 = np.sort(abs(df2))
    sorted_data2 = sorted_data200#[sorted_data100>.085]
    cdf2 = np.arange(1, len(sorted_data2) + 1) / len(sorted_data2)

    # Graficar la CDF
    plt.plot(sorted_data1, 1-cdf1, marker='.', linestyle='none',  label='1-CDF PosTRets')
    plt.plot(sorted_data2, 1-cdf2, marker='.', linestyle='none',  label='1-CDF NegTRets')
    plt.title(f'1-CDF _ {ticker}, {name}')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad Acumulada')
    plt.yscale('log')  # Cambiar a escala logarítmica
    #plt.xscale('log')
    plt.legend()
    plt.grid()
    plt.show()
    return sorted_data1, sorted_data2
#----------------------------------------------------------------------------------#

def grafica_cdf(ticker, df, name='string'):
    # Calcular la CDF
    sorted_data100 = np.sort(abs(df))
    sorted_data = sorted_data100#[sorted_data100>.085]
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

    # Graficar la CDF
    plt.plot(sorted_data, 1-cdf, marker='.', linestyle='none',  label='CDF Empirica')
    plt.title(f'1-CDF _ {ticker}, {name}')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad Acumulada')
    plt.yscale('log')  # Cambiar a escala logarítmica
    #plt.xscale('log')
    plt.legend()
    plt.grid()
    plt.show()
    return sorted_data

def graficos_sub4(ticker,
                  sorted_data_pos,cdf_empirical_pos,
                  cdf_fitted_pos,ye_pos,
                  sorted_data_neg,cdf_empirical_neg,
                  cdf_fitted_neg,ye_neg):
    plt.figure(figsize=(10, 7))  # Crea Figura y ajusta su tamaño 
    plt.subplot(2,2,1)
    # Graficar la CDF empírica
    plt.plot(sorted_data_pos,1-cdf_empirical_pos, marker='.', linestyle='none', label='CDF Empírica')
    # Graficar la CDF ajustada
    plt.plot(sorted_data_pos,1-cdf_fitted_pos, marker='.',linestyle='none', label='CDF Ajustada')
    # Configurar el gráfico
    plt.title(f'1-CDF ({ticker} TReturns)')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad Acumulada')
    plt.yscale('log')  # Cambiar a escala logarítmica
    #plt.xscale('log')
    plt.grid()
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(sorted_data_pos[:-1],ye_pos,linestyle='none',marker='.')
    #plt.yscale('log')
    plt.title(' log[(1-cdf_Empirica)/(1-cdf_Fit)]')
    plt.xlabel('Datos ordenados')
    plt.ylabel('Diferencia EmpíricosVsTeóricos')
    # Fijar los límites de los ejes
    #plt.xlim(0, 10)  # Límite del eje x
    plt.ylim(-5, 5)  # Límite del eje y
    plt.grid()
    plt.tight_layout()

    plt.subplot(2,2,3)
    # Graficar la CDF empírica
    plt.plot(sorted_data_neg,1-cdf_empirical_neg, marker='.', linestyle='none', label='CDF Empírica')
    # Graficar la CDF ajustada
    plt.plot(sorted_data_neg,1-cdf_fitted_neg, marker='.',linestyle='none', label='CDF Ajustada ')
    # Configurar el gráfico
    plt.title(f'1-CDF ({ticker} TReturns)')
    plt.xlabel('Valor')
    plt.ylabel('Probabilidad Acumulada')
    plt.yscale('log')  # Cambiar a escala logarítmica
    #plt.xscale('log')
    plt.grid()
    plt.legend()

    plt.subplot(2,2,4)
    plt.plot(sorted_data_neg[:-1],ye_neg,linestyle='none',marker='.')
    #plt.yscale('log')
    plt.title(' log[(1-cdf_Empirica)/(1-cdf_Fit)]')
    plt.xlabel('Datos ordenados')
    plt.ylabel('Diferencia EmpíricosVsTeóricos')
    # Fijar los límites de los ejes
    #plt.xlim(0, 10)  # Límite del eje x
    plt.ylim(-5, 5)  # Límite del eje y
    plt.grid()
    plt.tight_layout()
    plt.show()



#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
# Función para calcular rendimientos logarítmicos
def calculate_log_returns(prices):
    return np.log(prices / prices.shift(1))#.dropna()


# Función para convertir precios a retornos logarítmicos
def log_returns_to_prices(initial_price, log_returns):
    """
    Convierte retornos logarítmicos a precios.
    :param initial_price: Precio inicial (float)
    :param log_returns: Lista de retornos logarítmicos (list o numpy array)
    :return: Lista de precios (numpy array)
    """
    # Convertir la lista de retornos logarítmicos a un array de numpy
    log_returns = np.array(log_returns)
    # Calcular los precios a partir de los retornos logarítmicos
    prices = initial_price * np.exp(np.cumsum(log_returns))
    return prices


#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#--------------------####..............####---------------------#


#Funcion para generar Tendencias
def generate_trends(prices):
    '''
    Regresa una lista de tuplas [(0, prices.iloc[0], tendencia_actual)]
    que indican los puntos de cambio de tendencia en los precios.
    - Input: pd.Series de precios.
    - Output: lista de tuplas (idx, price, trend) donde trend es 'alcista' o 'bajista'.
    '''
    trends = [] #[(0, prices.iloc[0], tendencia_actual)]
    ctrend = None
    for i in range(1, len(prices)):
        # Tendencia alcista
        if prices.iloc[i] > prices.iloc[i - 1] and ctrend != 'alcista':  
            trends.append((i-1, prices.iloc[i-1], 'alcista'))
            ctrend = 'alcista'
        # Tendencia bajista
        elif prices.iloc[i] < prices.iloc[i - 1] and ctrend != 'bajista':  
            trends.append((i-1, prices.iloc[i-1], 'bajista'))
            ctrend = 'bajista' 
    # Agregar el último precio de stock_data
    if ctrend is not None:
        trends.append((len(prices)-1, prices.iloc[-1], ctrend))
    return trends


def trend_durations(trends, index=None, inclusive=False):
    """
    Calcula duraciones (en número de muestras) de cada tendencia
    trends: lista de tuplas (idx, price, trend) devuelta por generate_trends.
    index: opcional, pd.Index (fechas) para mapear índices a fechas.
    inclusive: si True, cuenta la duración incluyendo ambos extremos (+1).
    Devuelve un pd.DataFrame con columnas:
      start_idx, start_date (opcional), start_price,
      end_idx, end_date (opcional), end_price,
      trend, duration
    """
    import pandas as pd

    if not trends or len(trends) < 2:
        return pd.DataFrame(columns=['start_idx','start_date','start_price','end_idx','end_date','end_price','trend','duration'])

    rows = []
    for i in range(len(trends) - 1):
        s_idx, s_price, tr = trends[i]
        e_idx, e_price, _ = trends[i + 1]
        dur = e_idx - s_idx
        if inclusive:
            dur += 1
        row = {
            'start_idx': int(s_idx),
            'start_price': float(s_price),
            'end_idx': int(e_idx),
            'end_price': float(e_price),
            'trend': tr,
            'duration': int(dur)
        }
        if index is not None:
            try:
                row['start_date'] = index[s_idx]
                row['end_date'] = index[e_idx]
            except Exception:
                row['start_date'] = None
                row['end_date'] = None
        else:
            row['start_date'] = None
            row['end_date'] = None
        rows.append(row)

    return pd.DataFrame(rows)

#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
# Funciones de normalización de datos
def standar_norm(data):
    '''Normaliza los datos a una distribución normal estándar (media=0, desviación estándar=1)'''
    # Calcular la media y la desviación estándar de cada columna
    media = np.mean(data)
    stdev = np.std(data)
    data_norm = (data-media)/stdev
    return data_norm

def min_max_norm(data):
       '''Normaliza entre 0 y 1'''
       return (data - data.min()) / (data.max() - data.min())


#--------------------####..............####---------------------#
#--------------------####..............####---------------------#
#--------------------####..............####---------------------#

#Lectura de datos y creacion de DFs -> CPrice,Rets y TCPrice,TRets 
def rdata_genRets_TRets(Sdata):
    '''Lectura de datos y creacion de DFs -> CPrice_Rets y TCPrice,TRets'''
    #ticker = Sdata[:20] #Intradia
    ticker = Sdata[6:] #diarios
    StockData = pd.read_csv(Sdata)
    StockData.set_index('Date', inplace=True) #Poner la fecha como el indice del dataframe; datetime para intradia

    #--------------------------------------------------------------------------------------------#
    CPrices_Rets_df = StockData[['Adj Close']].copy() #Hacemos una copia de la columna Close de DowData
    CPrices_Rets_df['LogRet_CPrice'] = calculate_log_returns(CPrices_Rets_df) #Agregamos columna de LogReturns
    CPrices_Rets_df = CPrices_Rets_df.dropna() # Eliminamos elementos NaN
    
    #--------------------------------------------------------------------------------------------#
    # Generamos trends y dataframe con los LogReturns Correspondientes.
    trends_Tupla = generate_trends(CPrices_Rets_df['Adj Close']) 
    idx,cprice,label = zip(*trends_Tupla) # zip descompone la lista de tuplas en 3 tuplas x, y, z.
    TDates = [CPrices_Rets_df.index[i] for i in idx] #Extraemos las fechas con método index de pd
    CTPrices_TRets_df = pd.DataFrame({'TrendDates': TDates, 'TrendPrices': cprice})
    CTPrices_TRets_df['Log-TReturns'] = calculate_log_returns(CTPrices_TRets_df['TrendPrices'])
    CTPrices_TRets_df = CTPrices_TRets_df.dropna()
    #CTrends_df.set_index('TrendDates', inplace=True)
    CTPrices_TRets_df
    return CPrices_Rets_df, CTPrices_TRets_df



#Separaramos retornos positivos de negativos en series de pandas
def split_PosNegData4(CPrices_Rets_df, CTPrices_TRets_df):
    '''Separa retornos positivos de negativos en series de pandas; regresa 4 pdseries'''
    df_PosRets = CPrices_Rets_df['LogRet_CPrice'][CPrices_Rets_df['LogRet_CPrice']>0]
    df_NegRets = CPrices_Rets_df['LogRet_CPrice'][CPrices_Rets_df['LogRet_CPrice']<=0]
    df_PosTRets = CTPrices_TRets_df['Log-TReturns'][CTPrices_TRets_df['Log-TReturns']>0]
    df_NegTRets = CTPrices_TRets_df['Log-TReturns'][CTPrices_TRets_df['Log-TReturns']<=0]
    #PdSeries_4list = [df_PosRets, -df_NegRets, df_PosTRets, -df_NegTRets]
    return df_PosRets, df_NegRets, df_PosTRets, df_NegTRets

#Separa retornos positivos de negativos en dataFrames de pandas
def split_PosNegData4DFs(CPrices_Rets_df, CTPrices_TRets_df):
    #Forma alternativa de separar los retornos positivos de negativo manteniendo un DataFrame
    df_PosRets = CPrices_Rets_df[CPrices_Rets_df['LogRet_CPrice']>0]
    df_NegRets = CPrices_Rets_df[CPrices_Rets_df['LogRet_CPrice']<=0]
    df_PosTRets = CTPrices_TRets_df[CTPrices_TRets_df['Log-TReturns']>0]
    df_NegTRets = CTPrices_TRets_df[CTPrices_TRets_df['Log-TReturns']<=0]
    #PdDFs_4list = [df_PosRets, -df_NegRets, df_PosTRets, -df_NegTRets]
    return df_PosRets, df_NegRets, df_PosTRets, df_NegTRets 

def resample_by_trading_minutes(df, n_minutes=5, on=None, agg=None, label='end'):
    """
    Agrupa el dataframe por ventanas de n_minutes muestras (minutos de trading).
    Asume que cada fila del DataFrame de entrada representa un minuto.
    - df: pd.DataFrame con índice datetime o con columna de fecha (pasar `on='Datetime'`).
    - n_minutes: tamaño de la ventana en número de filas (e.g., 5 para 5 minutos).
    - on: nombre de la columna de fecha/hora si no está en el índice.
    - agg: diccionario de agregación o None para usar OHLC+Volume.
    - label: 'end' -> fecha de índice será la última fecha del bloque;
                'start' -> será la primera fecha del bloque.
    Retorna: DataFrame agregado con índice datetime.
    """

    if on is not None:
        if on not in df.columns:
            raise ValueError(f"Columna {on} no encontrada en df")
        d = df.copy()
        d.index = pd.to_datetime(d[on])
    else:
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("El DataFrame debe tener DatetimeIndex o pasar on='fecha_col'.")
        d = df.copy()

    if agg is None:
        # agregaciones típicas para precios OHLCV
        def _has(col): return col in d.columns
        agg = {}
        if _has('Open'): agg['Open'] = 'first'
        if _has('High'): agg['High'] = 'max'
        if _has('Low'):  agg['Low']  = 'min'
        if _has('Close'):agg['Close']= 'last'
        if _has('Adj Close'): agg['Adj Close'] = 'last'
        if _has('Volume'): agg['Volume'] = 'sum'
        # si no hay columnas estándar, agrupa por primer/last para todas
        if not agg:
            agg = {c: 'last' for c in d.columns}

    groups = np.arange(len(d)) // int(n_minutes)
    grouped = d.groupby(groups).agg(agg)

    # construir índice de fechas (start o end de cada bloque)
    if label == 'end':
        idx = d.index.to_series().groupby(groups).last().values
    else:
        idx = d.index.to_series().groupby(groups).first().values

    grouped.index = pd.to_datetime(idx)
    # opcional: eliminar filas con NaN completos (ej. ventana incompleta)
    grouped = grouped.dropna(how='all')

    return grouped

def resample_by_trading_days(df, n_days=2, on=None, agg=None, label='end'):
    """
    Agrupa el dataframe por ventanas de n_days muestras (días de trading).
    - df: pd.DataFrame con índice datetime o con columna de fecha (pasar `on='Date'`).
    - n_days: tamaño de la ventana en número de filas (2,3,...).
    - on: nombre de la columna de fecha si no está en el índice.
    - agg: diccionario de agregación o None para usar OHLC+Volume.
    - label: 'end' -> fecha de índice será la última fecha del bloque;
             'start' -> será la primera fecha del bloque.
    Retorna: DataFrame agregado con índice datetime.
    """
    import numpy as np
    import pandas as pd

    if on is not None:
        if on not in df.columns:
            raise ValueError(f"Columna {on} no encontrada en df")
        d = df.copy()
        d.index = pd.to_datetime(d[on])
    else:
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("El DataFrame debe tener DatetimeIndex o pasar on='fecha_col'.")
        d = df.copy()

    if agg is None:
        # agregaciones típicas para precios OHLCV
        def _has(col): return col in d.columns
        agg = {}
        if _has('Open'): agg['Open'] = 'first'
        if _has('High'): agg['High'] = 'max'
        if _has('Low'):  agg['Low']  = 'min'
        if _has('Close'):agg['Close']= 'last'
        if _has('Adj Close'): agg['Adj Close'] = 'last'
        if _has('Volume'): agg['Volume'] = 'sum'
        # si no hay columnas estándar, agrupa por primer/last para todas
        if not agg:
            agg = {c: 'last' for c in d.columns}

    groups = np.arange(len(d)) // int(n_days)
    grouped = d.groupby(groups).agg(agg)

    # construir índice de fechas (start o end de cada bloque)
    if label == 'end':
        idx = d.index.to_series().groupby(groups).last().values
    else:
        idx = d.index.to_series().groupby(groups).first().values

    grouped.index = pd.to_datetime(idx)
    # opcional: eliminar filas con NaN completos (ej. ventana incompleta)
    grouped = grouped.dropna(how='all')

    return grouped

def resample_by_calendar_days(df, n_days=2, on=None, agg=None, closed='right', label='right'):
    """
    Resample por calendario: ventanas de n_days calendario (2D,3D,...).
    - df: pd.DataFrame con DatetimeIndex o columna fecha (usar on=...).
    - n_days: int número de días calendario.
    - closed/label: parámetros para pandas.Grouper/resample.
    Retorna: DataFrame agregado.
    """
    import pandas as pd

    if on is not None:
        if on not in df.columns:
            raise ValueError(f"Columna {on} no encontrada en df")
        d = df.copy()
        d.index = pd.to_datetime(d[on])
    else:
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("El DataFrame debe tener DatetimeIndex o pasar on='fecha_col'.")
        d = df.copy()

    if agg is None:
        agg = {}
        if 'Open' in d.columns: agg['Open'] = 'first'
        if 'High' in d.columns: agg['High'] = 'max'
        if 'Low' in d.columns: agg['Low'] = 'min'
        if 'Close' in d.columns: agg['Close'] = 'last'
        if 'Adj Close' in d.columns: agg['Adj Close'] = 'last'
        if 'Volume' in d.columns: agg['Volume'] = 'sum'
        if not agg:
            agg = {c: 'last' for c in d.columns}

    rule = f'{int(n_days)}D'
    res = d.resample(rule, closed=closed, label=label).agg(agg)
    res = res.dropna(how='all')
    return res

#--------------------####..............####---------------------#
#--------------------####....Plots.....####---------------------#   
#--------------------####..............####---------------------#
def plot_histogram(df, bins='auto', title='Histograma', xlabel='Valor', ylabel='Frecuencia'):
    plt.figure(figsize=(10, 6))
    plt.hist(df, bins=bins, alpha=0.7, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def dot_hist(df,bins='auto'):
    counts, bins = np.histogram(df, bins=bins)
    #print(counts)
    # Filtrar los valores cero
    nonzero_counts = counts[counts > 0]
    nonzero_bins = bins[:-1][counts > 0]
    #print('nonzero counts -> ', nonzero_counts)
    # Calcular la posición de los puntos (centro de cada bin)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    nonzero_bin_centers = bin_centers[counts > 0]   
    return nonzero_counts, nonzero_bin_centers

def plot_duration_bars(durations, title=None, logy=True, sort=True, figsize=(8,4), color='C0'):
    """
    Grafica un bar por cada duración distinta.
    - durations: puede ser
        * pd.DataFrame con columna 'duration' (resultado de trend_durations),
        * lista/array de enteros (duraciones),
        * lista de tuplas devuelta por generate_trends (se calcula internamente).
    - retorna: pd.Series (conteos por duración)
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Obtener array de duraciones
    if isinstance(durations, pd.DataFrame) and 'duration' in durations.columns:
        vals = durations['duration'].astype(int).values
    elif isinstance(durations, (list, tuple)) and len(durations) > 0 and isinstance(durations[0], tuple):
        # lista de tuplas (idx, price, trend) -> calcular duraciones
        dur_df = trend_durations(durations)
        vals = dur_df['duration'].astype(int).values
    else:
        vals = np.asarray(durations, dtype=int)

    if len(vals) == 0:
        print("No hay duraciones para graficar.")
        return pd.Series(dtype=int)

    counts = pd.Series(vals).value_counts()
    if sort:
        counts = counts.sort_index()

    plt.figure(figsize=figsize)
    plt.bar(counts.index.astype(int).astype(str), counts.values, color=color, width=0.5)
    plt.xlabel("Duration (number of trend days)")
    plt.ylabel("Frecuency")
    if title is None:
        title = "Duration Distribution"
    plt.title(title)
    if logy:
        plt.yscale('log')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()

    return counts

#--------------------####..............####---------------------#
#--------------------####.....Fits.....####---------------------#   
#--------------------####..............####---------------------#

#Determinar que tipo de distribucion ajustara datos
def fit_data(sorted_data, distro):
    # Calcular la CDF empírica
    cdf_empirical = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    print('Cantidad de datos ->', len(sorted_data))
    # Ajustar una distribución a los datos(Por Maxima verosimilidtud)
    #parametros = stats.expon.fit(datas)
    parametros = getattr(stats, distro).fit(sorted_data)

    print(f'Ajuste de distribución {distro} a datos.\nPARAMETROS:')
    print('(shape(alpha), loc, scale)')
    print(parametros)
    #print(f'Media -> {mu} \nDesviacion estandar -> {std}')

    # Calcular la CDF de la distribución ajustada
    #cdf_fitted = stats.crystalball.cdf(sorted_data, beta=parametros[0], m=parametros[1], loc=parametros[2], scale=parametros[3])
    #cdf_fitted = stats.expon.cdf(sorted_data,*parametros)
    cdf_fitted = getattr(stats, distro).cdf(sorted_data,*parametros)

    ye=((np.log((1-cdf_empirical[:-1])/(1-cdf_fitted[:-1]))))#*(1-cdf_empirical[:-1])
    #ye=(((1-cdf_empirical[:-1])/(1-cdf_fitted[:-1])))#*(1-cdf_empirical[:-1])
    return cdf_empirical, cdf_fitted, ye, parametros

#--------------#-------#---------#-------#-#-#-#-#----#-------#-------------------#
#--------------#-#---#-#--------#-#----------#--------#-#-----#-------------------#
#--------------#---#---#-------#-#-#---------#--------#---#---#-------------------#
#--------------#-------#------#-----#--------#--------#-----#-#-------------------#
#--------------#-------#-----#-------#---#-#-#-#-#----#-------#-------------------#
if __name__ == "__main__":

    #Sdata = 'SData_^DJI_1992-2024'
    Sdata = input('Por favor introduce el StockData que deseas analizar(.csv):')
    CPrices_Rets_df, CTPrices_TRets_df = rdata_genRets_TRets(Sdata)
    Rets_TRets4 = split_PosNegData4(CPrices_Rets_df, CTPrices_TRets_df)
    opcion = input('Selecciona una opción:\n1.PosRets\n2.NEgRets\n3.PosTRets\n4.NegTRets\n')
    opcion = int(opcion)-1
    print(Rets_TRets4[opcion])
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
