# olist-customer-churn-analysis
Анализ оттока клиентов бразильского маркетплейса Olist: SQL, когорты, RFM, причинный анализ, ML-модель, дашборд Streamlit
# Olist Customer Churn Analysis

[![Python](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

Анализ оттока клиентов бразильского маркетплейса **Olist**. Цель — выявить ключевые драйверы ухода клиентов и предложить меры удержания.

## 📌 Бизнес-задача
Интернет-магазин теряет клиентов. Нужно понять:
- Какие факторы действительно влияют на отток (а не просто коррелируют)?
- Какие сегменты клиентов самые рискованные?
- Какую стратегию удержания предложить?

## 🛠 Инструменты и навыки
- **SQL (PostgreSQL)** – когортный анализ, RFM-сегментация, оконные функции
- **Python** – pandas, seaborn, scikit-learn (RandomForest, KMeans)
- **Статистика** – t-test, ANOVA, Propensity Score Matching
- **Визуализация** – Streamlit, matplotlib, plotly
- **ML** – модель предсказания оттока (ROC-AUC = 0.82)

## 📁 Структура проекта
├── data/ # Ссылка на исходные данные
├── notebooks/ # Jupyter Notebook с EDA и моделированием
├── sql/ # Все SQL-запросы (когорты, RFM, витрины)
├── dashboard/ # Streamlit-приложение и скриншоты
├── models/ # Сохранённая модель Random Forest
└── reports/ # Презентация для бизнеса

## 🔍 Ключевые выводы
1. **Задержка доставки** увеличивает вероятность оттока на **15–18%** (каузальный эффект).
2. Выделено **5 RFM-сегментов**: *чемпионы, лояльные, спящие, риск оттока, потерянные*.
3. Лучшая модель предсказания оттока – Random Forest (ROC-AUC 0.82).

## 💡 Рекомендации
- Сократить задержки в трёх приоритетных регионах.
- Запустить программу лояльности для сегмента «риск оттока».
- Ожидаемый эффект: **+8–10% повторных покупок**.

## 🖥 Дашборд
Скриншот: (добавлю позже)

## ▶️ Как запустить локально
```bash
git clone https://github.com/ваш_логин/olist-customer-churn-analysis.git
cd olist-customer-churn-analysis/dashboard
pip install -r requirements.txt
streamlit run streamlit_app.py
