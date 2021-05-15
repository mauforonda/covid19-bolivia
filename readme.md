## ⚠ Archivado ⚠

Si buscas datos oficiales y actualizados de casos de covid-19 en Bolivia utiliza [mauforonda/covid19-bolivia-udape](mauforonda/covid19-bolivia-udape). 

---

> Series de tiempo de casos de covid-19 en Bolivia en base a datos oficiales

- [El branch `master`](https://github.com/mauforonda/covid19-bolivia/tree/master/)contiene datos de [boliviasegura](https://www.boliviasegura.gob.bo/), el sitio oficial del gobierno nacional, irregulares desde Octubre de 2020.
- [El branch `opsoms`](https://github.com/mauforonda/covid19-bolivia/tree/opsoms) contiene datos de la [Organizacion Panamericana de la Salud](https://paho-covid19-response-who.hub.arcgis.com/datasets/uvw-daily-reports-amro-adm1-output-latest-rate-new-view), útiles mientras el sitio oficial no actualice datos.

---

## Sobre los datos oficiales en `opsoms`

Los documentos `confirmados.csv` y `decesos.csv` se reportan en tiempo local (`GMT-4`).

Algunos días la fuente no reporta datos correctamente. El directorio `patches` incluye los parches que se aplican a los datos de estos días. Puedes sugerir nuevos parches creando un issue o pull request.
