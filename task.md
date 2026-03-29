# Tareas de Revisión Humana — Aula del Futuro

Cosas que el equipo debe revisar y que no se pueden automatizar.

---

## Entrevistas (pendientes)

- [ ] **Aplicar las entrevistas** a estudiantes de ambos niveles (primaria-secundaria y preparatoria-universidad)
- [ ] **Completar las secciones de "Voces de los Estudiantes"** en ambos documentos HTML — actualmente tienen texto placeholder:
  - `documento/primaria-secundaria.html` (líneas ~318-341): 2 bloques con `[Nombre, grado]` y `[Insertar transcripción]`
  - `documento/preparatoria-universidad.html` (líneas ~318-341): 2 bloques con `[Nombre, carrera, semestre]`
- [ ] **Completar Anexo B** en ambos documentos (líneas ~467-471): mismos placeholders de evidencia
- [ ] Después de insertar datos reales, eliminar los bloques de `<div class="entrevista-aviso">` con las instrucciones

---

## Contenido académico

- [ ] **Verificar citas UNESCO 2015a/b** — Se corrigió la asignación para cumplir con APA 7 (orden alfabético por título):
  - **2015a** = "Educación 2030: Declaración de Incheon y Marco de Acción" (ODS 4, educación equitativa)
  - **2015b** = "Replantear la educación: ¿Hacia un bien común mundial?" (diversidad cultural, diálogo)
  - Revisar que cada cita en el texto refiera a la obra correcta. Ver `documento/verificacion-citas.html` como guía.
- [ ] **Verificar que las 25 referencias** en `references.json` tengan datos completos y correctos (autores, año, título, DOI/URL)
- [ ] **Revisar las nuevas referencias Pozo (1990) y Pozo y Postigo (1994)** — solo aparecen en las slides, no en los documentos HTML. Si se citan en los documentos, agregar los IDs al mapeo en `scripts/render-refs.js`
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

## Antes de entregar

- [ ] **Ejecutar `npm run build:refs`** si se modifica `references.json` — esto actualiza las referencias en los 3 archivos automáticamente
- [ ] **Verificar el sitio desplegado** en GitHub Pages después de cada push a main
- [ ] **Crear grupo Zotero** (opcional) para gestión colaborativa de referencias — ver plan en `.claude/plans/shimmying-dazzling-pillow.md`
