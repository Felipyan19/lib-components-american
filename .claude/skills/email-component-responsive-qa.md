---
description: Valida el responsive de un componente HTML de email después de editar o refactorizar, verificando reglas mínimas de calidad sin renderizar. Usar sobre componentes en libs/components/*/*.html o libs/Click Experts/*/*.html tras aplicar email-component-responsive-refactor, o antes de fusionar un componente al template final. Activa cuando el usuario pide "validar", "verificar QA", "pasar QA", "comprobar" o "está listo para producción" un componente de email.
---

# Skill: email-component-responsive-qa

## Objetivo
Verificación rápida post-refactor. No modifica código. Corre el script de validación automática y reporta el resultado con checklist de aprobación.

## Paso 1 — Detectar familia y correr validación automática

Primero determinar la familia (Clásica o Centurion) según las clases del `<style>`.

Ejecutar el script de validación:
```bash
# Componentes en libs/components/
node scripts/validate-responsive.js libs/components/[familia]/[componente].html

# Templates Centurion/Marigold
node scripts/validate-responsive.js "libs/Click Experts/[template]/[componente].html"

# Directorio completo
node scripts/validate-responsive.js libs/components/
node scripts/validate-responsive.js "libs/Click Experts/"
```

El script verifica automáticamente:
- Meta viewport presente
- `@media only screen and (max-width: 619px)` presente
- Imágenes con `alt` y `height:auto`
- No hay `width` fijo inline en imágenes sin `max-width:100%`

**Nota**: el script no distingue entre familias de clases. Los checks manuales del Paso 2 sí lo hacen.

## Paso 2 — Checklist manual por tipo

### Todos los tipos
- [ ] Archivo abre sin errores (HTML válido)
- [ ] Breakpoint `@media only screen and (max-width: 619px)` en `<style>`
- [ ] Contenido principal a 620px de ancho (como `max-width:620px` o `width="620"`)

### Familia CLÁSICA — componentes de 2 columnas (horizontal-pair, hotel-card, section-*)
- [ ] Ambas columnas son `<th>`, no `<td>`
- [ ] Ambos `<th>` tienen clase `.full-width-block`
- [ ] Si hay `height` fijo en `<th>`, tiene clase `.height-auto`
- [ ] Si hay imagen desktop con size fijo: existe imagen mobile (`.mobile-on`)

### Familia CENTURION — CIM02 Horizontal Pairs
- [ ] Las 4 columnas (`gutter + col-A + col-B + gutter`) usan `<th>`
- [ ] Los dos `<th>` gutter tienen clase `.hideMbl`
- [ ] `col-A` y `col-B` tienen clase `.im-block` (o `.im-block-auto`)
- [ ] Si hay `height` fijo en la columna, tiene clase `.hb-reset` o está controlado por contenido
- [ ] Si hay imagen desktop con URL fija: existe par `hideMbl`/`showMbl` para imagen mobile
- [ ] La columna de contenido tiene `.im-horz-pair-padding` para padding mobile
- [ ] Si hay `border-right` entre columnas: se evalúa si debe colapsar con `.no-border`

### Familia CENTURION — Separadores / Spacers
- [ ] Separadores con `class="hideMbl"` desaparecen en mobile ✅
- [ ] Separadores SIN `hideMbl` que tienen `height` fijo: ⚠️ deberían colapsar o marcarse como riesgo

### Hero con overlay (hero-banner) — familia Clásica
- [ ] Columna spacer tiene `.mobile-off`
- [ ] Columna texto tiene `.full-width-auto` y `.BgBlue`
- [ ] Columna imagen mobile tiene `mso-hide:all` y `.mobile-on`
- [ ] Existe bloque VML `<!--[if gte mso 9]-->` para bg-image

### Footer nav — familia Clásica
- [ ] Cada `<th>` de enlace tiene `.full-width-block`
- [ ] Cada `<th>` (salvo el primero) tiene `.fm-border`
- [ ] `.fm-nav-link` para override de padding en mobile

### Footer nav — familia Centurion (CFM02)
- [ ] Cada `<th>` de enlace tiene `.fm-nav-link` con `display:inline-block` en mobile
- [ ] Cada `<th>` (salvo el primero) tiene `.fm-border`

### Todas las imágenes
- [ ] `alt` presente (puede ser `""` si es decorativa)
- [ ] `style` incluye `height:auto; display:block`
- [ ] `max-width:100%` o imagen mobile alternativa presente

## Paso 3 — Matriz de prueba mínima

Completar antes de marcar como listo:

| Cliente | Resultado esperado | Estado |
|---|---|---|
| iOS Mail (14+) | Stack columnas, imágenes fluidas, padding correcto | ⬜ No probado |
| Gmail app Android | Imágenes fluidas, texto legible sin zoom | ⬜ No probado |
| Outlook desktop 2019/365 | Sin CSS, estructura tabla intacta, VML activo | ⬜ No probado |
| Outlook Web App | Media query activo, layout correcto | ⬜ No probado |

**Si no se puede probar en un cliente, declararlo explícitamente en el reporte.**

## Paso 4 — Reporte de QA

```
## QA Responsive — [nombre-componente.html]
**Tipo:** [tipo]
**Validación automática:** [PASS / FAIL — N errores]

### Errores del script
[lista o "ninguno"]

### Checklist manual
[resultado por tipo]

### Matriz de prueba
[completar según acceso disponible]
[NO PROBADO: lista de clientes no verificados]

### Veredicto
[ ] APROBADO — listo para fusión al template
[ ] APROBADO CON OBSERVACIONES — riesgos conocidos: [describir]
[ ] RECHAZADO — corregir antes de fusionar: [describir]

### Notas para siguiente iteración
[Si algo falló en un cliente real, documentar aquí el patrón/solución
para agregar al skill o a references/]
```

## Regla de iteración
Si el componente falla QA en un cliente real (al probarlo externamente):
1. Documentar el fallo en la sección "Notas"
2. Agregar la regla/patrón al skill de refactor o al archivo de referencias correspondiente
3. No crear variantes sueltas del patrón: actualizar la fuente única de verdad
