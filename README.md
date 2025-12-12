# Challenge-Tecnico-Tradespark

## Algoritmic Trading Backtester — SMA & Golden Cross Strategies

Algortmico que permite ejecutar estrategias basadas en medias móviles simples utilizando Backtrader, con administración separada de capital por estrategia.

### Descripcion
Este proyecto es un entorno modular de backtesting para estrategias de trading algorítmico escrito en Python.
Esta diseñado para probar estrategias tecnicas (como Cruce Dorado y Medias Móviles) sobre datos historicos de acciones tecnologicas (AAPL, GOOGL, MSFT, TSLA) en 2021, pero pueden ser modificables en archivo de configuracion.

### Caracteristicas

Características
* Arquitectura Modular: Separación clara entre datos, estrategias, gestión de tamaño de posición (sizers) y ejecución.

* Estrategias Implementadas:

    * SMAStrategy: Estrategia basada en Medias Móviles Simples.

    * GoldenCrossStrategy: Estrategia de cruce de medias (Cruce Dorado).

* Gestión de Capital: Módulo de sizers personalizado para gestionar el tamaño de la posición por operación.

* Reportes: Generación automática de reportes de transacciones y evolución del valor del portafolio en la carpeta outputs.


### Estructura del Proyecto
```text 
.
├── data/  
│   └── stocks/          # Datos históricos en formato CSV
├── outputs/             # Resultados de la ejecución
│   ├── analysis/        # Gráficos y análisis de resultados
│   └── reports/         # Reportes de transacciones y valor de portafolio
├── src/
│   ├── sizers/          # Lógica para el tamaño de la posición
│   ├── strategies/      # Clases con la lógica de compra/venta
│   ├── utils/           # Cargadores de datos y herramientas de reporte
│   └── config.py        # Configuraciones globales (paths, parámetros)
├── main.py              # Punto de entrada principal del script
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación
```

### Instalacion y Configuracion
1. #### Clonar el Repositorio:
```bash
    git clone <tu-repositorio-url>
    cd <nombre-carpeta>
```

2. #### Configurar entorno virtual
```bash
    python -m venv .venv
    # En Windows:
    .venv\Scripts\activate
    # En Mac/Linux:
    source .venv/bin/activate
```

3. #### Instalar dependencias
```bash
    pip install -r requirements.txt
```

### Uso
Para ejecutar la simulacion de trading para datos historicos y periodo definido en el archivo `utils/config.py`:
``` bash
    python main.py
```

#### Configuracion de datos
    En el archivo `utils/config.py` se pueden configurar las siguientes opciones:
    1. STRATEGY_TICKERS que define en una lista los tickets de los instrumentos a utilizar
    2. INIT_DATE inicio de periodo en formato 'yyyy-mm-dd'
    3. END_DATE fin de periodo en formato 'yyyy-mm-dd'

#### Añadir nueva estrategia
1. Crea un nuevo archivo en `src/strategies/`
2. Hereda de BaseStrategy
3. Implementa la logica en el metodo next()
4. Importa y añade la estrategia en main.py


### Resultados
Despues de cada ejecucion, verifica la carpeta `outputs/`
* `analysis/figures`: Graficos generados por script `src\utils\strategies_transaction_resume.py` que realiza en procesamiento de los reportes generados para mostrar graficos derivados de los mismos, sobre el rendimiento de las estrategias.
* `reports/transaction_report`: Log detallado de cada operacion compra/venta
* `reports/value_report`: Evolucion del dinero y valor de portafolio por cada cierre. 


