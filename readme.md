# 🏥 Proyecto Ausentismo Laboral — Modelos Supervisados

Proyecto académico de análisis de datos y construcción de modelos supervisados sobre ausentismo laboral, utilizando registros de incapacidades médicas clasificadas según la CIE-10 (Clasificación Internacional de Enfermedades).

---

## 🎯 Objetivo

Analizar el comportamiento del ausentismo laboral a partir de registros de incapacidades médicas, con el fin de:

- Predecir el número de días de incapacidad según el diagnóstico (código CIE-10)
- Predecir el valor económico de la incapacidad
- Identificar patrones y agrupaciones de diagnósticos por costo e impacto

---

## 📁 Estructura del Proyecto

```
.
├── data/
│   ├── BASE DE AUSENTISMO PARA ANALISIS.xlsx       # Dataset principal de incapacidades
│   └── clasificacion-int-enfermedades-OMS-OPS-V19.xlsx  # Tabla oficial CIE-10
├── requirements.txt                                 # Dependencias del proyecto
└── src/
    ├── ausentismo.ipynb                             # Notebook principal de análisis
    └── lib/
        ├── graficas.py                              # Clase para visualizaciones
        ├── limpieza.py                              # Clase para limpieza de datos
        └── __init__.py
```

---

## 🔄 Pipeline del Proyecto

```
1. Inspección Inicial       → Revisión de tipos, nulos y estructura del dataset
2. Limpieza de Datos        → Eliminación de columnas, corrección de tipos y categorías
3. EDA                      → Análisis exploratorio: distribuciones, correlaciones, outliers
4. Manejo de Outliers       → Detección y tratamiento con IQR
5. Encoding                 → Transformación de variables categóricas
6. Escalado                 → Normalización de variables numéricas
7. Modelo Supervisado       → Construcción y evaluación del modelo
```

---

## 📊 Dataset

| Característica | Detalle |
|---|---|
| Registros | 950 |
| Variables | 11 |
| Período | 2022 — 2024 |
| Clasificación diagnóstica | CIE-10 (OMS/OPS V19) |

### Variables del dataset limpio:

| Variable | Tipo | Descripción |
|---|---|---|
| `periodo` | Ordinal | Año del evento |
| `mes_evento` | Ordinal | Mes del evento |
| `cargo` | Categórica | Cargo del trabajador |
| `dependencia` | Categórica | Área o dependencia |
| `tipo_evento` | Categórica | EC (Enfermedad Común) / AT (Accidente de Trabajo) |
| `dias_incapacidad` | Numérica | Días de incapacidad médica |
| `prorroga` | Booleana | Si la incapacidad fue prorrogada (1/0) |
| `codigo_cie10` | Categórica | Código diagnóstico CIE-10 |
| `valor_salario` | Numérica | Valor del salario diario |
| `valor_incapacidad` | Numérica | Valor total de la incapacidad |

---

## 🛠️ Tecnologías

- Python 3.x
- Pandas
- Seaborn
- Plotly Express
- Scikit-learn *(próximamente)*

---

## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/ausentismo-laboral.git
cd ausentismo-laboral

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el notebook
jupyter notebook src/ausentismo.ipynb
```

---

## 📌 Estado del Proyecto

- [x] Inspección inicial
- [x] Limpieza de datos
- [x] EDA (Análisis Exploratorio)
- [ ] Manejo de outliers
- [ ] Encoding
- [ ] Escalado
- [ ] Modelo supervisado

---

## 👨‍💻 Autor

Proyecto académico desarrollado como parte de un proceso de aprendizaje en análisis de datos y machine learning.
