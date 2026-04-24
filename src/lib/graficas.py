import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

class Graficos():

    def __init__(self, df: pd.DataFrame):
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

    def graficarHistogramaPlotly(self, columna:str, nbins=30):
        """
        Gráfica de Histograma utilizando plotly.express
        """
        fig = px.histogram(self.df, x=columna, nbins=nbins, histnorm="density", opacity=0.75, title=f"Histograma {columna}")
        return fig
    
    def graficarHeatMapMatrizCorrelaciones(self):
        correlation_matrix = self.df.corr(numeric_only=True)
        fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, width=800, height=800, title="HeatMap de Correlaciones")
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))        
        return fig


