# Plan Final — Aula del Futuro (Primaria y Secundaria)

## Context

La Mtra. Socorro Guevara (Coco) entregó dos archivos PDF con la consigna y la rúbrica del Proyecto Final del curso "Estrategias para la Comprensión" (UPAEP, Maestría en Pedagogía). El equipo entregó una versión en DOCX (`Copia de primaria-secundaria.docx`) que tiene gaps importantes:

- **Secciones vacías**: Arquitectura, Conclusión, Anexos (encabezado en TOC sin contenido).
- **Tablas de entrevista vacías** (instrumento diseñado, sin datos).
- **Placeholder literal** `(cita?)` en Contexto Educativo.
- **Falta el documento completo de Características del Aula**: solo incluye Enseñanza–Aprendizaje–Evaluación parcial, sin las 3 estrategias innovadoras ni las entrevistas procesadas.
- **Referencias**: híbrido APA+URL, ~13 fuentes.

En paralelo, Hesus y Claude construyeron tres variantes HTML con el marco de Coco aplicado (`primaria-secundaria-final.html`, `-conservador.html`, `-radical.html`). El objetivo ahora es:

1. **Fase 1 — Baseline**: dejar documentada la entrega del equipo (DOCX) como punto de partida.
2. **Fase 2 — Díaz Barriga / Coco**: usar `primaria-secundaria-final.html` como base pedagógica (backward design, 6 facetas, rúbrica 5×4, enseñanza situada, Nuevo Traje del Profesor).
3. **Fase 3 — Rúbrica-tuned**: re-incorporar las secciones obligatorias de la rúbrica oficial que la Fase 2 sacrificó (Contexto, Necesidades, Resultados Esperados, Conclusión, Anexos) sin perder la estructura pedagógica.
4. **Fase 4 — Publicación**: una página de handoff en GitHub Pages que muestre a los compañeros del equipo qué cambió, por qué, y qué pueden hacer ellos (entrevistas reales, fotos, pilotaje).

GitHub Pages ya está configurado y publicando automáticamente desde `main` vía `.github/workflows/deploy.yml`. El plan se ejecutará en otra máquina; este documento queda comiteado como `PLAN_FINAL.md` en la raíz del repo.

---

## Decisiones tomadas

| Decisión | Elección |
|---|---|
| Base para Fase 2 | `documento/primaria-secundaria-final.html` |
| Framing del changelog | 3 fases (DOCX → Fase 2 Coco → Fase 3 Rúbrica) + TODO list para el equipo |
| Gaps del DOCX | Llamar out explícitamente, tono neutral (no blame) |

---

## Rúbrica oficial vs. `final.html` actual (mapa de gaps)

| Sección rúbrica | Puntos | ¿Está en `final.html`? | Acción Fase 3 |
|---|---:|---|---|
| Portada | 1 | Sí | Revisar que incluya título + 4 integrantes + asignatura + UPAEP + fecha |
| Nivel Educativo | 2.5 | No (subsumido en "¿Por Qué?") | Agregar sección dedicada al inicio |
| Contexto (Social/Eco/Edu) | 4 | No | Portar desde DOCX + versión original `primaria-secundaria.html` (sin `(cita?)`) |
| Necesidades | 4 | No | Portar las 6 necesidades del DOCX |
| Resultados Esperados | 4 | No | Portar los 6 resultados del DOCX (ya mapeados a 6 facetas) |
| Perfil Docente | 5 | Sí (4 competencias Nuevo Traje) | Añadir desglose explícito: Conocimientos / Habilidades / Destrezas / Actitudes / Hábitos / Valores |
| Características del Aula | 5 | Parcial | Añadir sub-sección con **3 Estrategias Innovadoras** etiquetadas (tomar del original) + proceso E–A–E |
| Arquitectura | 5 | Sí (6 zonas + espacio) | Mantener |
| Conclusión | 3 | No | Añadir cierre reflexivo |
| Anexos | — | No | Añadir (links a 3D demo, slides, instrumento, entrevistas cuando existan) |
| Referencias APA 7 | 1.5 | Sí (~16) | Revisar formato APA 7 completo via `references.json` + `build:refs` |
| **Total** | **35** | | |

---

## Fases de ejecución

### Fase 0 — Preparación (máquina de ejecución)

1. `git pull origin main`
2. `npm ci` (instala Slidev y dependencias JS)
3. `pip3 install -r requirements.txt` (instala `python-docx` para el exporter)
4. Verificar que `npm run build:refs` corre sin error.

### Fase 1 — Snapshot DOCX como baseline (read-only, ya hecho)

- DOCX del equipo ya analizado. Inventario completo documentado en la sección "DOCX inventory" más abajo.
- **No modificar `primaria-secundaria.html`** (se conserva como referencia histórica pre-Coco).
- **Eliminar `primaria-secundaria-conservador.html` y `primaria-secundaria-radical.html`** al final de Fase 3 para limpiar el repo.

### Fase 2 — Base pedagógica con `final.html`

**Archivo objetivo**: renombrar `documento/primaria-secundaria-final.html` → `documento/primaria-secundaria-v2-diazbarriga.html` (snapshot de Fase 2, conservado para el changelog).

```bash
cp documento/primaria-secundaria-final.html documento/primaria-secundaria-v2-diazbarriga.html
```

No editar este archivo después del copy — es el "antes" de Fase 3.

### Fase 3 — Rúbrica-tuned: `primaria-secundaria.html` nuevo

**Archivo objetivo**: reemplazar `documento/primaria-secundaria.html` con la versión final tuneada a rúbrica.

Orden canónico del documento nuevo (alineado a rúbrica, conservando marcos de Coco):

1. **Portada** — título, 4 integrantes, asignatura, UPAEP, fecha, docente Socorro Guevara
2. **Nivel Educativo** — primaria + secundaria (6–15 años), con justificación UNESCO del DOCX
3. **Contexto** — Social / Económico / Educativo (del DOCX, reemplazando `(cita?)` por cita real o eliminando la oración)
4. **Necesidades** — 6 necesidades del DOCX (motivación intrínseca, aprendizaje lúdico, socioemocional, UDL, escuela-vida, espacios reconfigurables)
5. **Resultados Esperados** — 6 resultados mapeados a 6 facetas (ya está en `final.html`, reorganizar en sección propia)
6. **¿Por Qué este diseño?** — Grandes Ideas + preguntas esenciales (de `final.html`)
7. **Perfil del Docente del Aula del Futuro** — Nuevo Traje (4 competencias) + desglose explícito Conocimientos/Habilidades/Destrezas/Actitudes/Hábitos/Valores (reconstruir del DOCX original)
8. **Características del Aula del Futuro**
   - 8.1 Proceso E–A–E (de `final.html` + `primaria-secundaria.html`)
   - 8.2 **3 Estrategias Innovadoras** (etiquetadas): (a) Unidades Temáticas Integradas sobre Problemas Reales, (b) Centros de Aprendizaje Lúdico con Exploración Guiada, (c) Desarrollo Metacognitivo mediante Diarios de Aprendizaje — todas con fundamentación Díaz Barriga/Pimienta (del `primaria-secundaria.html` original)
   - 8.3 Entrevistas a 2 estudiantes (Sofía + Diego, versiones contextualizadas de `final.html` — reemplazar con reales cuando el equipo las levante)
9. **Arquitectura para el Aprendizaje** — 6 zonas + ambiente emocional + mapeo a 6 facetas (de `final.html`)
10. **Cómo Evaluamos — Rúbrica 5×4** (de `final.html`: 5 criterios × 4 niveles Ingenua/Principiante/Aprendiz/Maestría)
11. **Proyecto Ejemplo: El Agua de mi Colonia** — 5 fases (de `final.html`)
12. **Protocolo de Metacognición** (de `final.html`)
13. **Instrumento de Recopilación** — 4 bloques con indicadores (del DOCX, ya diseñado)
14. **Reflexión del Equipo** (de `final.html`)
15. **Conclusión** — nueva, cierre reflexivo integrando los marcos (Coco espera las 3 preguntas: ¿Por qué importa? ¿Cómo se usa? ¿Cómo lo expreso?)
16. **Anexos** — links a recorrido 3D, slides, verificación de citas
17. **Referencias APA 7** — vía `references.json` + `npm run build:refs`

**Proceso de construcción de `primaria-secundaria.html` (Fase 3)**:

1. Usar `documento/primaria-secundaria-v2-diazbarriga.html` (copia de Fase 2) como esqueleto HTML.
2. Insertar las secciones 2, 3, 4, 5, 7 (desglose), 8.2 (estrategias etiquetadas), 15, 16 — tomando el contenido del DOCX y del `primaria-secundaria.html` original (pre-Coco) que ya está en el repo.
3. Mantener estilo via `assets/css/documento.css` (sin cambios de CSS).
4. Verificar que toda cita tenga entrada en `references.json`; si falta alguna (p. ej. la que reemplace `(cita?)`), añadirla y correr `npm run build:refs`.
5. Eliminar cualquier cita de Fullan o Fraser 1982 que quede (ya hubo un commit que las reemplazó — verificar).

### Fase 4 — Changelog / handoff page

**Archivo nuevo**: `documento/cambios-equipo.html`

Estructura (diseño en 3 columnas / 3 fases, consistente con `documento.css`):

- **Header**: "Cambios al Proyecto Final — notas para el equipo". Fecha. Autor: Hesus.
- **Sección 1 — Contexto del rediseño**: 2 párrafos explicando por qué se rehízo (alineación con los 10 criterios de Coco + rúbrica oficial 35 pts).
- **Sección 2 — Las 3 fases del rediseño**: tabla comparativa con filas = áreas del documento, columnas = DOCX equipo / Fase 2 Díaz Barriga / Fase 3 Rúbrica. Cada celda: qué había / qué cambió.
- **Sección 3 — Qué faltaba en la entrega previa (tono neutral)**:
  - Secciones vacías: Arquitectura, Conclusión, Anexos
  - Placeholder `(cita?)` en Contexto Educativo
  - Tablas del instrumento diseñadas pero vacías (entrevistas reales pendientes)
  - Falta de las 3 estrategias innovadoras etiquetadas
  - Referencias en formato híbrido URL+APA
- **Sección 4 — Qué cambió y por qué (detallado)**: lista de cambios con justificación pedagógica (backward design, 6 facetas, enseñanza situada Díaz Barriga 2006, rúbrica interna 5×4, proyecto ejemplo El Agua).
- **Sección 5 — TODO para el equipo (cosas que ustedes pueden hacer)**:
  - Levantar entrevistas reales con 2 estudiantes (Sofía y Diego son placeholders; reemplazar con datos del campo usando el instrumento ya diseñado — 4 bloques)
  - Fotos del espacio físico actual vs. propuesta de arquitectura
  - Pilotaje de una de las 3 estrategias en un grupo real
  - Validar referencias APA 7 (revisar `references.json`)
  - Revisar/expandir Conclusión con voz de equipo
  - Convertir a DOCX final usando `scripts/html_to_docx.py` (ya existe) antes de entregar
- **Sección 6 — Cómo navegar los archivos**:
  - `primaria-secundaria.html` → versión final (Fase 3) — esta es la entregable
  - `primaria-secundaria-v2-diazbarriga.html` → snapshot Fase 2 (Díaz Barriga/Coco puro, sin rúbrica-tune)
  - Links a recorrido 3D, slides, verificación de citas, personas
- **Footer**: nav back al index.

### Fase 5 — Wiring del site

1. **Actualizar `index.html`**: la card "Primaria y Secundaria" ya apunta a `primaria-secundaria.html` — no cambia. Añadir una nueva card "Notas para el equipo" que apunte a `documento/cambios-equipo.html`.
2. **No tocar `.github/workflows/deploy.yml`**: el step `cp -r documento dist/` ya copia toda la carpeta automáticamente.
3. **Borrar archivos obsoletos** (git rm):
   - `documento/primaria-secundaria-conservador.html`
   - `documento/primaria-secundaria-radical.html`
   - `documento/primaria-secundaria-final.html` (ya renombrado a `-v2-diazbarriga.html`)

### Fase 6 — DOCX export para entrega

```bash
python3 scripts/html_to_docx.py documento/primaria-secundaria.html docs/primaria-secundaria-final.docx
```

Este DOCX es el que se entrega a Coco. No se comitea (es artefacto de build); se sube manualmente al sistema de entrega de UPAEP.

---

## Archivos críticos

**Modificar**:
- `documento/primaria-secundaria.html` — reemplazo completo (Fase 3)
- `index.html` — añadir una card

**Crear**:
- `documento/cambios-equipo.html` — handoff page
- `documento/primaria-secundaria-v2-diazbarriga.html` — snapshot de Fase 2 (copia de `final.html`)

**Eliminar**:
- `documento/primaria-secundaria-conservador.html`
- `documento/primaria-secundaria-radical.html`
- `documento/primaria-secundaria-final.html` (tras copiar a `-v2-diazbarriga.html`)

**Leer / referenciar sin modificar**:
- `coco-soul.md` — criterios de evaluación (10 de Coco)
- `references.json` — fuente única de referencias APA 7
- `scripts/render-refs.js` — render de referencias
- `scripts/html_to_docx.py` — exportador a Word
- `assets/css/documento.css` — estilos compartidos de documentos
- `Copia de primaria-secundaria.docx` (Downloads, fuera del repo) — fuente de Contexto/Necesidades/Instrumento

---

## DOCX inventory (referencia)

Lo que el DOCX del equipo contiene:

- ✅ Portada + TOC
- ✅ Nivel Educativo (~200 palabras, cita UNESCO 2021, 2020)
- ✅ Contexto Social (~300), Económico (~280), Educativo (~270) — con placeholder `(cita?)`
- ✅ Necesidades (6, ~400 palabras)
- ✅ Resultados Esperados (6, ~300 palabras, mapeados a facetas)
- ✅ Perfil Docente (6 categorías, ~500 palabras)
- ✅ ¿Para Quién Diseñamos? (2 personas: Valentina, Prof. Miguel)
- ⚠️  Características del Aula — solo E–A–E parcial; **falta 3 estrategias, entrevistas procesadas, detalles de arquitectura**
- ✅ Instrumento de Recopilación (4 bloques con indicadores — tablas vacías, sin datos)
- ❌ Arquitectura — encabezado sin contenido
- ❌ Conclusión — encabezado sin contenido
- ❌ Anexos — encabezado sin contenido
- ⚠️  Referencias (13, híbrido APA+URL, incluye Fraser 1982 y Fullan que fueron removidos en commits previos del repo)

---

## Verificación end-to-end

Al terminar la ejecución en la máquina destino:

1. **Build local**: `npm run build` — debe generar `dist/slides/` sin errores. Debe correr `build:refs` primero.
2. **Abrir localmente** cada página con un servidor estático:
   ```bash
   npx http-server . -p 8080
   ```
   - `http://localhost:8080/` — landing debe mostrar la nueva card "Notas para el equipo"
   - `http://localhost:8080/documento/primaria-secundaria.html` — versión Fase 3, debe tener las 17 secciones listadas
   - `http://localhost:8080/documento/primaria-secundaria-v2-diazbarriga.html` — snapshot Fase 2
   - `http://localhost:8080/documento/cambios-equipo.html` — handoff page legible
3. **Checklist manual contra rúbrica** (35 pts):
   - [ ] Portada con los 5 elementos esenciales
   - [ ] Nivel Educativo claro y coherente
   - [ ] Contexto en 3 dimensiones sin placeholders
   - [ ] 6 Necesidades fundamentadas
   - [ ] 6 Resultados Esperados alineados
   - [ ] Perfil Docente con las 6 categorías (Conocimientos/Habilidades/Destrezas/Actitudes/Hábitos/Valores)
   - [ ] 3 Estrategias Innovadoras etiquetadas, con fundamentación
   - [ ] 2 Entrevistas (ficticias/contextualizadas hasta que equipo levante reales)
   - [ ] Arquitectura descrita completamente
   - [ ] Conclusión presente y reflexiva
   - [ ] Referencias APA 7 completas (revisar via `references.json`)
4. **Grep de placeholders**: `grep -rn "cita?\|TODO\|TBD\|FIXME" documento/` debe salir vacío.
5. **Grep de citas removidas**: `grep -rn "Fraser.*1982\|Fullan" documento/` debe salir vacío (validar).
6. **Deploy automático**: tras `git push origin main`, verificar en Actions que el workflow `Deploy Slidev to GitHub Pages` completa en verde. La URL publicada: `https://HesusG.github.io/aula-del-futuro/`.
7. **Smoke test en Pages**: abrir la URL pública en incógnito, navegar a los 3 documentos + changelog + slides + demo 3D.
8. **DOCX final**: ejecutar `scripts/html_to_docx.py` y abrir el resultado en Word/Pages — verificar encabezados, tablas y citas.

---

## Commits sugeridos (orden)

```
feat: snapshot Phase 2 base (rename final.html → v2-diazbarriga.html)
feat: rebuild primaria-secundaria.html aligned to rubric (Phase 3)
feat: add cambios-equipo.html handoff page
chore: remove obsolete -conservador.html and -radical.html variants
docs: link cambios-equipo from landing page
```

(Puedes agruparlos en menos commits si prefieres — son lógicamente separables.)

---

## Notas finales

- **No modificar estilos CSS globales** — `documento.css` ya sirve bien, mantener consistencia visual.
- **Todas las citas** deben pasar por `references.json`; si agregas una, corre `npm run build:refs`.
- **Entrevistas**: las de Sofía y Diego en `final.html` son contextualizadas (fundamentadas en personas), no ficticias sin base — el equipo puede reemplazarlas con reales usando el instrumento de 4 bloques ya diseñado (ver sección 13 del doc nuevo).
- **`coco-soul.md` es la brújula**: antes de darlo por terminado, leer los 10 criterios y auto-evaluar en Ingenua/Principiante/Aprendiz/Maestría. Apuntar a Maestría en los 10.
