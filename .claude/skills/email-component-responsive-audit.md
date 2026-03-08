---
description: Audita el responsive de un componente HTML de email de forma aislada (no layout global), verificando compatibilidad Outlook/MSO y ancho desktop 620px. Usar al revisar o diagnosticar componentes en libs/components/*/*.html o libs/Click Experts/*/*.html para detectar problemas de stack móvil, visibilidad mobile/desktop, imágenes no fluidas y spacing inseguro. Activa cuando el usuario pide "auditar", "revisar responsive", "diagnosticar" o "qué le falta" a un componente de email.
---

# Skill: email-component-responsive-audit

## Objetivo
Diagnosticar el estado responsive de UN componente sin modificarlo. Entregar un informe con hallazgos y riesgos clasificados por severidad.

## Paso 1 — Identificar tipo de componente y familia de clases

Leer el archivo y clasificarlo según su estructura:

| Tipo | Layout | Riesgo principal |
|---|---|---|
| `hero-banner` (overlay) | bg-image + VML + texto | VML Outlook, imagen mobile oculta |
| `hero-full-width` | stacked image+bars | imagen mobile alt |
| `horizontal-pair` / `hotel-card` | 2 columnas 50/50 `<th>` | stack mobile de `<th>` a bloque |
| `section-*` (compras/gastro/hoteles) | header + 2 columnas | clases faltantes en celda de contenido |
| `cross-sell-icons` / `CFM01` | fila de íconos | wrap vs stack en mobile |
| `footer-nav` / `footer-tagline` / `CFM02` | fila única / imagen | padding mobile, imagen fluida |
| `brand-panel` / `BP01` | 2 filas complejas | ocultar tagline en mobile |
| `preheader` / `intro-text` / `cta-banner` / `terms` | columna única | mínimo riesgo, verificar padding |
| **CIM02 Horizontal Pairs (Centurion)** | 2 columnas con gutter `<th>` laterales | columnas gutters sin `hideMbl`, imagen sin par mobile |
| **CIM05 Vertical Pairs (Centurion)** | fila con 2 tarjetas verticales y separadores | separadores fijos sin colapso mobile |
| **CTM03 Full Width Text (Centurion)** | tabla al 100% con texto centrado | ancho máximo fijo sin `max-width:100%` |
| **CIM03 Horizontal Pair + Logo (Centurion)** | imagen + panel de contenido con subcolumnas | padding lateral fijo en panel |

### Detectar familia de clases del template

Hay dos familias de nomenclatura. Identificar cuál usa el archivo:

| Familia | Clases características | Templates |
|---|---|---|
| **Clásica** (libs/components) | `mobile-off`, `mobile-on`, `show-desktop`, `full-width-block` | social-icons, hero-banner, footer-nav, section-* |
| **Centurion** (libs/Click Experts) | `hideMbl`, `showMbl`, `im-block`, `im-block-auto`, `im-horz-pair-padding` | D-Image-Modules, templates Centurion/Marigold |

**Si el template usa clases Centurion, verificar contra esa familia (no confundir ausencia de `mobile-off` como error).**

## Paso 2 — Checklist de auditoría

Verificar cada punto y marcar: ✅ OK | ⚠️ Advertencia | ❌ Falla

### Estructura base
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">` presente
- [ ] `@media only screen and (max-width: 619px)` como breakpoint canónico
- [ ] Contenedor de contenido a 620px (como `max-width:620px` o `width="620"`)
- [ ] Wrapper externo (800px) usa clase `.wrapper` con override `width:100% !important` en media query

### Clases responsive — familia CLÁSICA (`libs/components`)
- [ ] `.container` → `width:100% !important; padding:0 !important`
- [ ] `.full-width-block` → en columnas `<th>` de 2 columnas (stack a 100%)
- [ ] `.full-width-auto` → en elementos que deben ser `display:block; width:auto`
- [ ] `.mobile-off` / `.show-desktop` → para ocultar en mobile
- [ ] `.mobile-on` / `.mobile-display-block` → para mostrar en mobile con `display:block !important`
- [ ] `.height-auto` → en celdas con `height` fijo que debe colapsar en mobile

### Clases responsive — familia CENTURION (`libs/Click Experts`)
- [ ] `.hideMbl` → en columnas gutters laterales (`width=20`, `width=40`) y elementos desktop-only
- [ ] `.showMbl` → en elementos mobile-only (requiere `style="display:none;"` inline en desktop)
- [ ] `.im-block` → en `<th>` de 2 columnas (equivalente a `full-width-block`)
- [ ] `.im-block-auto` → en columna de contenido que puede ser auto-width
- [ ] `.im-horz-pair-padding` → padding override para columna de contenido en mobile
- [ ] `.full-width` / `.full-img` → en imágenes que deben ser 100% en mobile
- [ ] `.hb-reset` → en `<td>` con `height` fijo (colapsa en mobile)
- [ ] `.noPadR`, `.padd-t30`, `.padd-b30`, `.PaddLR` → utilitarios de padding mobile

### Patrones Centurion — CIM02 Horizontal Pairs
- [ ] Columnas gutter laterales (`width=20` / `width=40`) tienen clase `.hideMbl`
- [ ] Columnas principales tienen clase `.im-block` (no `.im-block-auto`)
- [ ] La columna de contenido tiene clase `.im-block-auto` Y `.im-horz-pair-padding`
- [ ] Si hay imágenes desktop fijas: existe par `hideMbl`/`showMbl` para imagen mobile
- [ ] `border-right` entre columnas: se revisa si debe colapsar en mobile (`.no-border`)

### Imágenes
- [ ] Imágenes en columnas de 2-col tienen `width="100%"` o versión mobile alternativa
- [ ] Imágenes fluidas: `style="height:auto; display:block; max-width:100%"`
- [ ] Imágenes decorativas: `alt=""` presente
- [ ] Imágenes con contenido: `alt` descriptivo presente
- [ ] Imagen mobile tiene `style="display:none"` + clase `.showMbl` o `.mobile-on`

### Compatibilidad Outlook/MSO
- [ ] Columnas 2-col usan `<th>` (no `<td>`) para stack en Outlook
- [ ] Si hay background-image en `<td>`: existe bloque VML `<!--[if gte mso 9]>...<![endif]-->`
- [ ] Botones CTA: existe bloque `<!--[if mso]><v:roundrect>...<![endif]-->` O se acepta el riesgo
- [ ] Elementos mobile-only tienen `mso-hide:all` o `style="display:none; mso-hide:all;"`
- [ ] No hay propiedades CSS no soportadas por Outlook sin fallback inline

### Spacing mobile
- [ ] Celdas con `padding` fijo en desktop tienen clase para override en mobile
- [ ] No hay `width` fijo en px en elementos inline que rompan en mobile
- [ ] Separadores/spacers con `height` fijo tienen clase `.hideMbl` o colapso via media query

## Paso 3 — Entregar informe

Formato de salida obligatorio:

```
## Auditoría Responsive — [nombre-componente.html]
**Tipo detectado:** [tipo según tabla]
**Familia de clases:** [Clásica / Centurion]
**Ancho desktop:** [620px ✅ / otro — describir]
**Breakpoint:** [619px ✅ / otro/ausente ❌]

### Hallazgos
| Severidad | Elemento | Problema | Impacto |
|---|---|---|---|
| ❌ CRÍTICO | ... | ... | Desktop o mobile roto |
| ⚠️ MEDIO | ... | ... | Visual degradado |
| ℹ️ INFO | ... | ... | Mejora opcional |

### Clases responsive presentes
[lista de clases encontradas — indicar si son familia Clásica o Centurion]

### Clases responsive faltantes (recomendadas)
[lista con justificación — usar nomenclatura de la familia detectada]

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
- Si no se puede determinar el tipo o la familia de clases, preguntar antes de asumir
- No mezclar clases de familia Clásica y Centurion en las recomendaciones
