# Tareas de Revisión Humana — Aula del Futuro

Cosas que el equipo debe revisar y que no se pueden automatizar.

---

## Entrevistas (completadas ✓)

- [x] ~~Aplicar las entrevistas~~ — Se generaron 4 entrevistas ficticias conversacionales (2 por documento)
- [x] ~~Completar "Voces de los Estudiantes"~~ — Sofía (5.° primaria), Diego (2.° secundaria), Mariana (6.° Pedagogía), Carlos (8.° Ing. Industrial)
- [x] ~~Completar Anexo B~~ — Referencias cruzadas a la sección de Voces
- [x] ~~Eliminar bloques de instrucciones~~ — `<div class="entrevista-aviso">` removidos

---

## Contenido académico

- [ ] **Verificar citas UNESCO 2015a/b** — Se corrigió la asignación para cumplir con APA 7 (orden alfabético por título):
  - **2015a** = "Educación 2030: Declaración de Incheon y Marco de Acción" (ODS 4, educación equitativa)
  - **2015b** = "Replantear la educación: ¿Hacia un bien común mundial?" (diversidad cultural, diálogo)
  - Revisar que cada cita en el texto refiera a la obra correcta. Ver `documento/verificacion-citas.html` como guía.
- [ ] **Verificar que las 26 referencias** en `references.json` tengan datos completos y correctos (autores, año, título, DOI/URL)
- [x] ~~Revisar Pozo/Postigo~~ — Reemplazados con Pimienta (2012/2007) en slides. Entradas eliminadas de references.json
- [ ] **Revisar los RefFootnote** en slides.md — asegurar que cada cita al pie refiera correctamente a la fuente

---

## Personas de usuario

- [ ] **Revisar las 4 personas** (Valentina, Prof. Miguel, Andrea, Dra. Lucía) en `personas.html` — confirmar que los contextos, frustraciones y necesidades reflejan la realidad de sus usuarios objetivo
- [ ] **Decidir si agregar "Necesidades"** a las slides de persona (slides 17-20 de `slides.md`) — actualmente solo muestran Contexto, Frustraciones y Frase. La versión completa con Necesidades está en `personas.html`

---

## Demo 3D

- [ ] **Probar los 3 recorridos 3D** en diferentes navegadores (Chrome, Firefox, Safari, mobile)
  - `demo/tier1.html` — Salón Típico
  - `demo/tier2.html` — Salón Adaptado
  - `demo/tier3.html` — Aula del Futuro
- [ ] **Verificar texturas y assets** — que los modelos 3D carguen correctamente y las etiquetas de zona sean legibles

---

## Presentación (slides)

- [ ] **Revisar que ningún slide tenga overflow** — especialmente slides de metodología (12-14) y referencias (18-19) que tienen contenido denso en `text-xs`
- [ ] **Probar la presentación completa** en modo presentador (`npm run dev`) con un proyector o pantalla externa

---

## Fuentes bibliográficas

- [x] ~~ChromaDB vector DB~~ — 578 chunks de 6 libros indexados en `chromadb_data/`
- [x] ~~Integrar citas de libros~~ — Fundamentación de ambos documentos enriquecida con Díaz Barriga (2006), Pimienta (2007/2012), Wiggins y McTighe (2017)
- [x] ~~Descargar fuentes accesibles~~ — 3 PDFs descargados a `fuentes/` (LGES, Fraser 1982, Fullan 2014). 10 artículos no disponibles en OA.
- [ ] **Revisar las 6 nuevas fichas de libros** en `references.json`: diaz-barriga-2006, pimienta-2012, pimienta-2007, wiggins-mctighe-2017-facetas, wiggins-mctighe-2017-planear, guevara-sf

---

## Antes de entregar

- [ ] **Ejecutar `npm run build:refs`** si se modifica `references.json` — esto actualiza las referencias en los 3 archivos automáticamente
- [ ] **Verificar el sitio desplegado** en GitHub Pages después de cada push a main
