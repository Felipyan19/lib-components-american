---
description: Audita el responsive de un componente HTML de email de forma aislada (no layout global), verificando compatibilidad Outlook/MSO y ancho desktop 620px. Usar al revisar o diagnosticar componentes en libs/components/*/*.html para detectar problemas de stack móvil, visibilidad mobile/desktop, imágenes no fluidas y spacing inseguro. Activa cuando el usuario pide "auditar", "revisar responsive", "diagnosticar" o "qué le falta" a un componente de email.
---

# Skill: email-component-responsive-audit

## Objetivo
Diagnosticar el estado responsive de UN componente sin modificarlo. Entregar un informe con hallazgos y riesgos clasificados por severidad.

## Paso 1 — Identificar tipo de componente

Leer el archivo y clasificarlo según su estructura:

| Tipo | Layout | Riesgo principal |
|---|---|---|
| `hero-banner` (overlay) | bg-image + VML + texto | VML Outlook, imagen mobile oculta |
| `hero-full-width` | stacked image+bars | imagen mobile alt |
| `horizontal-pair` / `hotel-card` | 2 columnas 50/50 `<th>` | stack mobile de `<th>` a bloque |
| `section-*` (compras/gastro/hoteles) | header + 2 columnas | clases faltantes en celda de contenido |
| `cross-sell-icons` | fila de íconos | wrap vs stack en mobile |
| `footer-nav` / `footer-tagline` | fila única / imagen | padding mobile, imagen fluida |
| `brand-panel` | 2 filas complejas | ocultar tagline en mobile |
| `preheader` / `intro-text` / `cta-banner` / `terms` | columna única | mínimo riesgo, verificar padding |

## Paso 2 — Checklist de auditoría

Verificar cada punto y marcar: ✅ OK | ⚠️ Advertencia | ❌ Falla

### Estructura base
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">` presente
- [ ] Contenedor raíz: `width="620"` + `style="width:620px"` + clase `.container`
- [ ] `@media only screen and (max-width: 619px)` como breakpoint

### Clases responsive usadas correctamente
- [ ] `.container` → `width:100% !important; padding:0 !important`
- [ ] `.full-width-block` → en columnas `<th>` de 2 columnas (stack a 100%)
- [ ] `.full-width-auto` → en elementos que deben ser `display:block; width:auto`
- [ ] `.mobile-off` / `.show-desktop` → para ocultar en mobile (ambos: `display:none !important; height:0; width:0`)
- [ ] `.mobile-on` / `.mobile-display-block` → para mostrar en mobile con `display:block !important`
- [ ] `.height-auto` → en celdas con `height` fijo que debe colapsar en mobile

### Imágenes
- [ ] Imágenes en columnas de 2-col tienen `width="100%"` o versión mobile alternativa
- [ ] Imágenes fluidas: `style="height:auto; display:block; max-width:100%"`
- [ ] Imágenes decorativas: `alt=""` presente
- [ ] Imágenes con contenido: `alt` descriptivo presente
- [ ] Imagen mobile tiene `style="display:none"` + clase `.mobile-on` (para mostrar vía media query)

### Compatibilidad Outlook/MSO
- [ ] Columnas 2-col usan `<th>` (no `<td>`) para stack en Outlook
- [ ] Si hay background-image en `<td>`: existe bloque VML `<!--[if gte mso 9]>...<![endif]-->`
- [ ] Botones CTA: existe bloque `<!--[if mso]><v:roundrect>...<![endif]-->` O se acepta el riesgo
- [ ] No hay propiedades CSS no soportadas por Outlook sin fallback inline

### Spacing mobile
- [ ] Celdas con `padding` fijo en desktop tienen clase para override en mobile (`.pd40` u otro)
- [ ] No hay `width` fijo en px en elementos inline que rompan en mobile

## Paso 3 — Entregar informe

Formato de salida obligatorio:

```
## Auditoría Responsive — [nombre-componente.html]
**Tipo detectado:** [tipo según tabla]
**Ancho desktop:** [620px ✅ / otro ❌]
**Breakpoint:** [619px ✅ / otro/ausente ❌]

### Hallazgos
| Severidad | Elemento | Problema | Impacto |
|---|---|---|---|
| ❌ CRÍTICO | ... | ... | Desktop o mobile roto |
| ⚠️ MEDIO | ... | ... | Visual degradado |
| ℹ️ INFO | ... | ... | Mejora opcional |

### Clases responsive presentes
[lista de clases encontradas]

### Clases responsive faltantes (recomendadas)
[lista con justificación]

### Compatibilidad Outlook
[OK / Riesgo: descripción]

### Acción recomendada
[ ] Aplicar email-component-responsive-refactor
[ ] Solo ajustes menores (describir)
[ ] No requiere cambios
```

## Restricciones
- NO modificar el archivo durante la auditoría
- Si el componente tiene VML, reportar su estado pero no evaluar su corrección interna
- Si no se puede determinar el tipo, preguntar antes de asumir
