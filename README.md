# serviseleads

Фабрика SEO-лендов для партнёрской программы **Leads Market** (`leads-market.ru`):
один домен, программатик-SEO по схеме `направление × город`, форма → лид в партнёрку
или телефон → колл-центр по нашему ID.

## Стек (планируемый)
Next.js + Strapi CMS + PostgreSQL. Партнёрка — сменный адаптер (`LeadProvider`).

## Документы
- **[docs/PLAN.md](docs/PLAN.md)** — план реализации, архитектура, модель данных, roadmap, риски, открытые вопросы.
- **[docs/analytics/SUMMARY.md](docs/analytics/SUMMARY.md)** — резюме аналитики: гео, направления, объём первой волны, экономика.
- **[docs/analytics/directions-summary.md](docs/analytics/directions-summary.md)** — сводка по 16 направлениям.
- **[docs/analytics/geo-matrix.csv](docs/analytics/geo-matrix.csv)** — матрица `направление × город` (2270 строк).
- **[docs/analytics/directions-summary.json](docs/analytics/directions-summary.json)** — машинно-читаемая сводка + недельные дельты.
- **[docs/research/affiliates.md](docs/research/affiliates.md)** — справочно: сравнение партнёрок, API и риск-профиль (решение: работаем только с Leads Market).
- **[docs/research/alternatives.md](docs/research/alternatives.md)** — альтернативные партнёрки вертикали (Руки из плеч, FirstLead, FIXCPA, ASC-Service и др.), чек-лист проверки.
- **[docs/research/approach-review.md](docs/research/approach-review.md)** — критический разбор подхода, риски и альтернативное видение.
- **[docs/research/channels.md](docs/research/channels.md)** — сравнение каналов: Avito, Яндекс.Услуги, Директ, SEO, экономика и риски.
- **[docs/research/avito-factory.md](docs/research/avito-factory.md)** — рабочая Avito-модель, «бронеаккаунты», масспостинг и тулкит фабрики.
- **[docs/specs/avito-factory.md](docs/specs/avito-factory.md)** — техническая спецификация софта: модули, модель данных, стек, roadmap.
- **[docs/plan/manual-month.md](docs/plan/manual-month.md)** — ручной пилот на 1 месяц: подготовка, план по неделям, гейт на масштабирование.
  - Шаблоны логов: [log-operations.csv](docs/plan/log-operations.csv), [log-ads.csv](docs/plan/log-ads.csv).
- **[docs/research/avito-tools.md](docs/research/avito-tools.md)** — build vs buy: обзор готовых сервисов (Reyting Pro, AviTool, AviForce и др.), что строить самим.

## Аналитика из `pulse.xlsx`
| Метрика | Значение |
|---|---:|
| Направлений | 16 |
| Городов-отделов | 64 |
| Населённых точек (вкл. спутники) | 148 |
| Комбинаций `направление × город` | 2270 |
| `Увеличить` | 375 |
| `без изменений` | 152 |
| `Отключить` | 1743 |

## Пересборка аналитики
```bash
python3 docs/analytics/parse_pulse.py /path/to/pulse.xlsx
```
Скрипт читает XLSX и перезаписывает `geo-matrix.csv`, `directions-summary.{md,json}`.
