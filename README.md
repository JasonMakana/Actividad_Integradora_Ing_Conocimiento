# Catálogo de Datos y Gobernanza Institucional (Ontología OWL 2 DL)

Ontología formal desarrollada bajo la metodología **METHONTOLOGY** orientada a la gobernanza de activos de información, auditoría de linaje ETL, clasificación de datos personales (LGPDPPSO) y control de vigencia documental institucional.

---

## 1. Estructura del Repositorio
* `ontologia_v1.ttl`: Definición formal del esquema (TBox: 14 clases, 9 propiedades de objeto, 4 propiedades de datos).
* `datos_ejemplo.ttl`: Conjunto de datos de prueba con 25 individuos representativos (ABox).
* `consultas.rq`: Archivo estándar que contiene las 6 consultas SPARQL correspondientes a las Preguntas de Competencia (CQ1–CQ6).
* `probar_todo.py`: Script automatizado en Python para cargar el grafo y ejecutar las 6 consultas SPARQL mostrando resultados tabulados en consola.
* `docs/`: Documentación técnica formal (`especificacion.pdf`, `conceptualizacion.pdf`, `evaluacion.pdf`).

---

## 2. Ejecución Rápida y Pruebas Automatizadas (Vía Python)

Para reproducir y verificar las 6 Preguntas de Competencia de forma inmediata sin necesidad de software gráfico:

### Requisitos previos
Tener instalado Python 3.8+ y la biblioteca `rdflib`:
```bash
pip install rdflib