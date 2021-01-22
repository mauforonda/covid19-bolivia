> Series de tiempo de casos de covid-19 en Bolivia en base a datos oficiales

**Actualización** 

El [sitio oficial del gobierno nacional](https://boliviasegura.gob.bo/) ha sido rediseñado recientemente, esta vez sin un servicio de datos para monitoreo epidemiológico. Por lo tanto desde ahora (2021-01-22), este repositorio sólo actualizará automáticamente [los datos en el branch opsoms](https://github.com/mauforonda/covid19-bolivia/tree/opsoms), producidos por la Organización Panamericana de la Salud.

---

- [El branch `master`](https://github.com/mauforonda/covid19-bolivia/tree/master/) contiene datos de [boliviasegura](https://www.boliviasegura.gob.bo/), el sitio oficial del gobierno nacional, irregulares desde Octubre de 2020. 
- [El branch `opsoms`](https://github.com/mauforonda/covid19-bolivia/tree/opsoms) contiene datos de la [Organizacion Panamericana de la Salud](https://paho-covid19-response-who.hub.arcgis.com/datasets/uvw-daily-reports-amro-adm1-output-latest-rate-new-view), útiles mientras el sitio oficial no actualice datos.

---

Sobre los datos oficiales en `master`:

- Los documentos `confirmados.csv`, `decesos.csv`, `recuperados.csv`, `sospechosos.csv` y `descartados.csv` se reportan en tiempo local (`GMT-4`). De estos sólo `confirmados` y `decesos` han sido actualizados luego de inicios de Mayo de 2020.
- `data.json` es una representación para ser consumida por proyectos como visualizaciones de datos.
- `total.csv` muestra estos valores en el formato del [repositorio de JHU](https://github.com/CSSEGISandData/COVID-19) para ser fácilmente comparado con datos de otros países. Para facilitar la comparación los tiempos se reportan en `UTC`.
- Los datos comenzaron a ser archivados el 21 de Marzo de 2020, tan pronto como fue publicada la fuente de boliviasegura.
- La fuente de datos dejó de actualizarse regularmente desde Octubre de 2020 y paró completamente el 22 de Noviembre ([acá](https://twitter.com/mauforonda/status/1335805902289575937) puedes ver un gráfico mostrando las interrupciones hasta el 7 de diciembre).
