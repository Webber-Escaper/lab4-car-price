# Данные

Исходный датасет — Car Price Prediction — Used Cars.
[Страница источника](https://www.kaggle.com/datasets/vijayaadithyanvg/car-price-predictionused-cars/data)

Сохраните загруженный CSV в каталоге `data/` под именем `car_data.csv`.
После выполнения анализа ЛР1 очищенные данные сохраняются в `clean_data.pkl`.
Файлы CSV и очищенные pickle-файлы исключены из Git, как в репозитории ЛР3.

Для работы prediction API готовая модель уже включена в
`services/models/model.pkl`. В `services/models/reference_data.json`
сохранены средняя `Present_Price` по 286 очищенным строкам и SHA-256
очищенного файла, использованного для расчета этого ориентира.
