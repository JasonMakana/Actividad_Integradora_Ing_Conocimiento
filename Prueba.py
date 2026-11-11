import rdflib

# 1. Cargar el grafo en memoria
g = rdflib.Graph()
print("Cargando ontología y datos...")
g.parse("ontologia_v1.ttl", format="turtle")
g.parse("datos_ejemplo.ttl", format="turtle")
print(f"-> Base de conocimiento cargada con {len(g)} tripletas.\n")

prefijos = """
PREFIX :     <http://example.org/cumbres/catalogo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# =============================================================================
# CQ1: Reportes que dependen de activos o columnas confidenciales
# =============================================================================
q_cq1 = prefijos + """
SELECT DISTINCT ?reporte ?nombreReporte ?activoConfidencial
WHERE {
  ?reporte a :Reporte ;
           rdfs:label ?nombreReporte ;
           :dependeDe+ ?activo .
  ?activo :tieneNivel :Nivel_Confidencial ;
          rdfs:label ?activoConfidencial .
}
"""
print("=" * 60)
print("CQ1: Reportes que dependen de datos confidenciales")
print("=" * 60)
for fila in g.query(q_cq1):
    print(f"Reporte: {fila.nombreReporte}")
    print(f"ID Reporte: {fila.reporte.split('#')[-1]}")
    print(f"Activo confidencial detectado: {fila.activoConfidencial}\n")

# =============================================================================
# CQ2: Responsable (custodio) de la tabla de alumnos
# =============================================================================
q_cq2 = prefijos + """
SELECT ?tabla ?nombreCustodio ?correo
WHERE {
  :tbl_Alumnos :tieneCustodio ?custodio .
  ?custodio rdfs:label ?nombreCustodio ;
            :correoInstitucional ?correo .
  BIND(:tbl_Alumnos AS ?tabla)
}
"""
print("=" * 60)
print("CQ2: Custodio de la tabla de alumnos")
print("=" * 60)
for fila in g.query(q_cq2):
    print(f"Tabla: {fila.tabla.split('#')[-1]}")
    print(f"Custodio responsable: {fila.nombreCustodio}")
    print(f"Correo de contacto: {fila.correo}\n")

# =============================================================================
# CQ3: Procesos ETL que alimentan el tablero de deserción
# =============================================================================
q_cq3 = prefijos + """
SELECT ?reporte ?nombreETL ?tablaDestino
WHERE {
  :Dashboard_Desercion :consultaA ?datasetDestino .
  ?procesoETL a :ProcesoETL ;
              rdfs:label ?nombreETL ;
              :escribeEn ?datasetDestino .
  ?datasetDestino rdfs:label ?tablaDestino .
  BIND(:Dashboard_Desercion AS ?reporte)
}
"""
print("=" * 60)
print("CQ3: Procesos ETL que alimentan el tablero de deserción")
print("=" * 60)
for fila in g.query(q_cq3):
    print(f"Tablero analítico: {fila.reporte.split('#')[-1]}")
    print(f"Pipeline ETL: {fila.nombreETL}")
    print(f"Escribe en (destino intermedio): {fila.tablaDestino}\n")

# =============================================================================
# CQ4: Columnas que contienen datos personales o sensibles
# =============================================================================
q_cq4 = prefijos + """
SELECT ?tabla ?columna ?tipoDato ?esSensible
WHERE {
  ?tabla :tieneColumna ?columna .
  ?columna :tieneClasificacion ?clasif .
  ?clasif rdfs:label ?tipoDato ;
          :esDatoSensible ?esSensible .
}
"""
print("=" * 60)
print("CQ4: Columnas con datos personales o sensibles")
print("=" * 60)
for fila in g.query(q_cq4):
    print(f"Tabla: {fila.tabla.split('#')[-1]}")
    print(f"Columna: {fila.columna.split('#')[-1]}")
    print(f"Tipo legal: {fila.tipoDato}")
    print(f"¿Es dato sensible?: {fila.esSensible}\n")

# =============================================================================
# CQ5: Fuentes o tablas sin custodio asignado
# =============================================================================
q_cq5 = prefijos + """
SELECT ?tabla ?nombreTabla
WHERE {
  ?tabla a :Tabla ;
         rdfs:label ?nombreTabla .
  FILTER NOT EXISTS {
    ?tabla :tieneCustodio ?custodio .
  }
}
"""
print("=" * 60)
print("CQ5: Tablas sin responsable/custodio asignado")
print("=" * 60)
for fila in g.query(q_cq5):
    print(f"Tabla huérfana detectada: {fila.nombreTabla} ({fila.tabla.split('#')[-1]})\n")

# =============================================================================
# CQ6: Conjuntos de datos que superaron su periodo de conservación
# =============================================================================
q_cq6 = prefijos + """
SELECT ?dataset ?nombreDataset ?fechaCreacion ?mesesRetencion
WHERE {
  ?dataset a ?tipo ;
           rdfs:label ?nombreDataset ;
           :fechaCreacion ?fechaCreacion ;
           :mesesRetencion ?mesesRetencion .
  FILTER(?tipo IN (:Tabla, :ConjuntoDeDatos, :VistaAnalitica))
  FILTER(?fechaCreacion < "2024-11-10T00:00:00"^^xsd:dateTime && ?mesesRetencion <= 24)
}
"""
print("=" * 60)
print("CQ6: Conjuntos de datos que superaron su periodo de conservación")
print("=" * 60)
for fila in g.query(q_cq6):
    print(f"Dataset caduco: {fila.nombreDataset}")
    print(f"Fecha de creación: {fila.fechaCreacion}")
    print(f"Retención máxima autorizada: {fila.mesesRetencion} meses\n")