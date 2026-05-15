import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

st.set_page_config(page_title="Olist Churn Dashboard", layout="wide")
st.title("📊 Анализ оттока клиентов Olist")
st.markdown("Когортный анализ, RFM-сегментация, предсказание оттока")

# ----------------------------------------------------------------------
# 1. Загрузка данных (реальные из папки data/ или демо)
# ----------------------------------------------------------------------
DATA_DIR = "data"

@st.cache_data
def load_real_data():
    """Загружает данные из CSV-файлов, если они есть в папке data/"""
    try:
        retention = pd.read_csv(os.path.join(DATA_DIR, "retention_matrix.csv"))
        rfm = pd.read_csv(os.path.join(DATA_DIR, "rfm_segments.csv"))
        features = pd.read_csv(os.path.join(DATA_DIR, "feature_importance.csv"))
        # ROC-AUC можно хранить в отдельном файле или в features метаинфо
        roc_auc = 0.82
        return retention, rfm, features, roc_auc, True
    except Exception as e:
        st.info(f"Не удалось загрузить реальные данные: {e}. Используются демо-данные.")
        return None, None, None, None, False

retention, rfm, features, roc_auc, has_real = load_real_data()

if not has_real:
    # Демо-данные (для презентации)
    retention = pd.DataFrame({
        'cohort_month': ['2025-01', '2025-02', '2025-03'],
        'month_0': [100, 100, 100],
        'month_1': [65, 60, 55],
        'month_2': [45, 42, 38],
        'month_3': [35, 30, 25]
    })
    rfm = pd.DataFrame({
        'segment': ['Champions', 'Loyal', 'Potential', 'At Risk', 'Lost'],
        'count': [120, 300, 450, 200, 430]
    })
    features = pd.DataFrame({
        'feature': ['recency', 'frequency', 'monetary', 'avg_review_score'],
        'importance': [0.45, 0.25, 0.20, 0.10]
    })
    roc_auc = 0.82

# ----------------------------------------------------------------------
# 2. Боковая панель с фильтрами (можно расширить)
# ----------------------------------------------------------------------
st.sidebar.header("Фильтры")
if has_real:
    st.sidebar.success("✅ Данные загружены из папки data/")
else:
    st.sidebar.info("ℹ️ Демо-данные. Чтобы загрузить реальные, положите CSV в папку data/")

# ----------------------------------------------------------------------
# 3. Визуализация
# ----------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("ROC-AUC модели", f"{roc_auc:.2f}")
col2.metric("Всего сегментов", len(rfm))
col3.metric("Клиентов (демо)", sum(rfm['count']) if not has_real else "—")
col4.metric("Отток (3 мес)", "~35%")

tab1, tab2, tab3 = st.tabs(["📈 Когортный анализ", "🎯 RFM-сегменты", "🤖 ML модель"])

with tab1:
    st.subheader("Retention rate по когортам")
    retention_melted = retention.melt(id_vars=['cohort_month'], var_name='month', value_name='retention')
    fig1 = px.bar(retention_melted, x='month', y='retention', color='cohort_month',
                  barmode='group', title="Удержание клиентов по месяцам",
                  labels={'retention': 'Retention (%)', 'month': 'Номер месяца'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # тепловая карта
    retention_pivot = retention.set_index('cohort_month')
    fig2 = px.imshow(retention_pivot, text_auto=True, aspect="auto",
                     labels=dict(x="Номер месяца", y="Когорта", color="Retention %"),
                     title="Матрица удержания")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Распределение клиентов по RFM-сегментам")
    fig3 = px.pie(rfm, values='count', names='segment', title="Доля сегментов")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    **Что означают сегменты:**
    - **Champions** – лучшие клиенты (высокий чек, часто)
    - **Loyal** – лояльные, стабильные
    - **Potential** – перспективные, можно повысить
    - **At Risk** – риск оттока, нужны акции
    - **Lost** – потерянные
    """)

with tab3:
    st.subheader("Важность признаков для предсказания оттока")
    fig4 = px.bar(features, x='importance', y='feature', orientation='h',
                  title="Feature Importance (Random Forest)",
                  labels={'importance': 'Влияние', 'feature': 'Признак'})
    st.plotly_chart(fig4, use_container_width=True)
    st.metric("ROC-AUC", f"{roc_auc:.3f}")
    st.progress(roc_auc)
    st.write("Модель обучена на признаках: recency, frequency, monetary, avg_review_score.")

# ----------------------------------------------------------------------
# 4. Дополнительные инструкции
# ----------------------------------------------------------------------
with st.expander("📘 Как подготовить реальные данные"):
    st.markdown("""
    1. В Colab после выполнения кода сохраните:
       ```python
       retention_matrix.to_csv('retention_matrix.csv')
       rfm[['segment','count']].to_csv('rfm_segments.csv')
       feature_importance_df.to_csv('feature_importance.csv')
