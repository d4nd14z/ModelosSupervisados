import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio

class Graficos():

    def __init__(self, df: pd.DataFrame):
        pio.renderers.default = "png"
        self.df = df

    def heatMapValoresNulos(self):
        """
        Gráfica de valores nulos del DataFrame completo 
        """
        plt.figure(figsize=(10,6))
        sns.heatmap(self.df.isnull(), yticklabels=False, cbar=False, cmap="Blues")
        plt.title("Mapa de Valores Nulos")
        plt.show()

    def graficarValoresColumna(self, columna:str):
        """
        Gráfica de Histograma y Boxplot sobre una única línea (1 fila y dos columnas)
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        # Histograma con KDE
        sns.histplot(self.df[columna], kde=True, ax=axes[0])
        axes[0].set_title(f"Histograma {columna}")
        # Boxplot
        sns.boxplot(x=self.df[columna], ax=axes[1])
        axes[1].set_title(f"Boxplot {columna}")
        plt.tight_layout()
        plt.show()

    def graficarColumnasPlotly(self, columna: str):    
        df = self.df

        # -----------------------------
        # 1. VARIABLE NUMÉRICA
        # -----------------------------
        if df[columna].dtype in ["int64", "float64"]:

            # Histograma
            fig_hist = px.histogram(df, x=columna)

            fig_hist.update_traces(
                marker=dict(color="rgba(0, 0, 255, 0.4)")
            )

            # Boxplot horizontal
            df_temp = df.copy()
            df_temp["_dummy"] = " "
            fig_box = px.box(df_temp, x=columna, y="_dummy")

            fig = fig_hist

            # agregar boxplot
            for trace in fig_box.data:
                fig.add_trace(trace)

            fig.data[1].update(
                fillcolor="rgba(0, 0, 255, 0.15)"
            )

            # layout tipo 2 columnas simuladas
            fig.update_layout(
                xaxis=dict(domain=[0.0, 0.48]),
                xaxis2=dict(domain=[0.52, 1.0]),
                yaxis=dict(domain=[0.0, 1.0]),
                yaxis2=dict(domain=[0.0, 1.0]),
                title=f"Histograma y Boxplot de {columna}",
                showlegend=False
            )

            # asignar ejes
            fig.data[0].xaxis = "x"
            fig.data[0].yaxis = "y"

            fig.data[1].xaxis = "x2"
            fig.data[1].yaxis = "y2"

            # Calcular outliers con IQR
            q1 = df[columna].quantile(0.25)
            q3 = df[columna].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = df[(df[columna] < lower) | (df[columna] > upper)]

            # Agregar SOLO outliers como scatter rojo
            fig.add_scatter(            
                x=outliers[columna],
                y=[" "] * len(outliers),
                mode="markers",
                marker=dict(color="red", size=6),
                showlegend=False
            )

            fig.data[2].xaxis = "x2"
            fig.data[2].yaxis = "y2"

            fig.update_yaxes(showticklabels=False)

        # -----------------------------
        # 2. VARIABLE CATEGÓRICA
        # -----------------------------
        else:

            conteos = df[columna].value_counts().reset_index()
            conteos.columns = [columna, "conteo"]

            fig = px.bar(
                conteos,
                x=columna,
                y="conteo",
                color=columna,
                color_discrete_sequence = px.colors.qualitative.Pastel,
                title=f"Frecuencia de {columna}"
            )

            fig.update_traces(opacity=0.7)

        fig.show()
        return fig
        
    
    def graficarHeatMapMatrizCorrelaciones(self):
        correlation_matrix = self.df.corr(numeric_only=True)
        fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, width=800, height=800, title="HeatMap de Correlaciones")
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))        
        return fig


