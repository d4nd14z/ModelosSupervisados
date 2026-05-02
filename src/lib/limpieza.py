import hashlib
import pandas as pd

class LimpiezaDatos():

    def __init__(self, df: pd.DataFrame):
        """ Constructor de la clase """
        self.df = df
        self.eliminarEncabezado()
        self.ajustarNombresColumnas()        
        self.crearColumnaPeriodo()
        self.anonimizarDatos(["nombre_trabajador", "cedula_trabajador"])   
        self.eliminarRegistrosNulos()
        self.cambiarTipoDatoMes()
        self.limpiezaCargos()                               # Se eliminan espacios al inicio y al final de la variable (SE DEBEN UNIFICAR CATEGORIAS !!!)
        self.limpiezaCodigosCIE10()                         # Se validan codigos, se corrigen valores "X" y con multiple codigo. 
        self.limpiezaProrroga()                             # Se modifican todos los valores para que solo sean 1) SI y 0) NO
        self.eliminarColumnas("lugar_atencion")             # Tiene demasiados nulos. No se puede imputar.
        self.eliminarColumnas("nombre_trabajador")          # Datos Identificadores que no aportan al estudio
        self.eliminarColumnas("cedula_trabajador")          # Datos Identificadores que no aportan al estudio
        self.eliminarColumnas("descripcion_diagnostico")    # Es un texto descriptivo que no aporta al estudio
        self.eliminarColumnas("dias_cargados")              # Todas las variables tienen el mismo valor (0). No aporta al estudio.
        self.eliminarColumnas("inicio_incapacidad")         # No aporta al estudio. Ya se tiene el mes de la incapacidad y la duracion de la incapacidad
        self.eliminarColumnas("fin_incapacidad")            # No aporta al estudio. Ya se tiene el mes de la incapacidad y la duracion de la incapacidad
        
        

    def ajustarNombresColumnas(self):
        self.df.columns = [
            "mes_evento",
            "nombre_trabajador",
            "cedula_trabajador",
            "cargo",
            "dependencia",
            "tipo_evento",
            "inicio_incapacidad",
            "fin_incapacidad",
            "dias_incapacidad",
            "lugar_atencion",
            "prorroga",
            "codigo_cie10",
            "dias_cargados",
            "descripcion_diagnostico",
            "salario_base",
            "valor_salario",
            "valor_incapacidad"
        ]

    def anonimizarDatos(self, columnas: list[str]):
        for col in columnas:
            self.df[col] = self.df[col].apply(lambda val: hashlib.sha256(str(val).encode()).hexdigest()) 

    def eliminarEncabezado(self):
        self.df = self.df.drop(index=[0,1]).reset_index(drop=True)        

    def crearColumnaPeriodo(self):
        self.df["inicio_incapacidad"] = pd.to_datetime(self.df["inicio_incapacidad"], errors="coerce", format="%Y-%m-%d")
        self.df["fin_incapacidad"] = pd.to_datetime(self.df["fin_incapacidad"])
        self.df["periodo"] = self.df["inicio_incapacidad"].dt.year
        self.df = self.df[["periodo"] + [col for col in self.df.columns if col != "periodo"]]
        self.df["periodo"] = self.df["periodo"].astype("Int64")
        self.df["dias_incapacidad"] = self.df["dias_incapacidad"].astype("Int64")
        self.df["dias_cargados"] = self.df["dias_cargados"].astype("Int64")
        self.df["salario_base"] = pd.to_numeric(self.df["salario_base"], errors="coerce").round(2)
        self.df["valor_salario"] = pd.to_numeric(self.df["valor_salario"], errors="coerce").round(2)
        self.df["valor_incapacidad"] = pd.to_numeric(self.df["valor_incapacidad"], errors="coerce").round(2)

    def cambiarTipoDatoMes(self):
        self.df["mes_evento"] = self.df["mes_evento"].astype(str).str.strip().str.upper()
        mes_map = {
            "ENERO": 1,
            "FEBRERO": 2,
            "MARZO": 3, 
            "ABRIL": 4,
            "MAYO": 5,
            "JUNIO": 6,
            "JULIO": 7,
            "AGOSTO": 8,
            "SEPTIEMBRE": 9,
            "OCTUBRE": 10, 
            "NOVIEMBRE": 11, 
            "DICIEMBRE": 12
        }
        self.df["mes_evento"] = self.df["mes_evento"].map(mes_map)

    def limpiezaCargos(self):
        self.df["cargo"] = self.df["cargo"].str.strip()

    def limpiezaCodigosCIE10(self):
        self.df["codigo_cie10"] = self.df["codigo_cie10"].str.replace("X", "0", regex=False)
        self.df["codigo_cie10"] = self.df["codigo_cie10"].str.strip()
        self.df.loc[161, "codigo_cie10"] = "F41"  # Reemplazar el cie_10 a F41 en el Indice 161
        self.df.loc[312, "codigo_cie10"] = "Z750" # Reemplazar el cie_10 a Z750 en el indice 312
        self.df = self.df.reset_index(drop=True)

    def limpiezaProrroga(self):
        self.df["prorroga"] = self.df["prorroga"].astype(str).str.strip().str.upper()
        bool_map = {
            "SI": 1,
            "NO": 0
        }
        self.df["prorroga"] = self.df["prorroga"].map(bool_map)

    def eliminarRegistrosNulos(self):
        self.df = self.df.drop(self.df[self.df["periodo"].isnull() & self.df["codigo_cie10"].isnull()].index)
        self.df = self.df.drop(index=611)
        self.df = self.df.reset_index(drop=True)

    def eliminarColumnas(self, col:str):
        self.df = self.df.drop([col], axis=1)
        self.df = self.df.reset_index(drop=True)

    def getDataFrame(self) -> pd.DataFrame:
        return self.df
    