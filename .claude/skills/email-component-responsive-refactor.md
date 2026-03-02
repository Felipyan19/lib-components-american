---
description: Mejora responsive de componentes HTML de email de forma aislada por componente (no layout global), manteniendo ancho desktop 620px y compatibilidad Outlook/MSO. Usar al editar o refactorizar componentes en libs/components/*/*.html para stack móvil, visibilidad mobile/desktop, imágenes fluidas y spacing seguro. Activa cuando el usuario pide "hacer responsive", "arreglar mobile", "aplicar responsive", "refactorizar" o "mejorar" un componente de email.
---

# Skill: email-component-responsive-refactor

## Objetivo
Aplicar mejoras responsive a UN componente de forma conservadora, sin cambiar estructura desktop ni romper Outlook. Cada cambio debe ser justificado.

## Paso 1 — Leer y clasificar antes de tocar

Leer el archivo completo. Identificar:
1. **Tipo de componente** (ver tabla en `audit` skill)
2. **Patrón de layout**: columna única / 2 columnas 50/50 / bg-image+overlay
3. **Estado actual del `<style>`**: ¿existe `@media`? ¿qué clases hay?
4. **Imágenes**: ¿hay versión mobile? ¿tienen `alt`?

**Si hay dudas sobre el tipo → preguntar, no asumir.**

## Paso 2 — Aplicar cambios por tipo

### A) Componentes de columna única (intro-text, cta-banner, terms, preheader, section-divider, contact-cta)

Solo verificar y agregar si falta:
```css
@media only screen and (max-width: 619px) {
  .container { padding: 0 !important; width: 100% !important; }
}
```
En el `<table>` raíz: `class="container"` si no lo tiene.

### B) Componentes de 2 columnas 50/50 (horizontal-pair, hotel-card, section-* body)

Las dos columnas deben ser `<th>` (no `<td>`). Agregar clase `.full-width-block` a cada `<th>`:

```html
<!-- Desktop: lado a lado | Mobile: apiladas -->
<th class="full-width-block" width="50%" ...>
  <!-- columna imagen -->
</th>
<th class="full-width-block" width="50%" ...>
  <!-- columna contenido -->
</th>
```

Media query requerida:
```css
@media only screen and (max-width: 619px) {
  .container { padding: 0 !important; width: 100% !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .height-auto { height: auto !important; }
  .mobile-off { display: none !important; height: 0px !important; width: 0px !important; }
  .mobile-on { display: block !important; }
}
```

### C) Hero con imagen de fondo + VML (hero-banner overlay)

El overlay requiere 3 columnas dentro del `<td>` background:
- Spacer izquierdo: clase `.mobile-off`
- Columna texto: clase `.full-width-auto` + `.BgBlue` (para overlay semitransparente en mobile)
- Columna imagen mobile: clase `.full-width-auto` + `style="mso-hide:all"` + imagen interna con clase `.mobile-on`

```css
@media only screen and (max-width: 619px) {
  .container { padding: 0 !important; width: 100% !important; }
  .show-desktop { display: none !important; font-size: 0 !important; max-height: 0 !important; line-height: 0 !important; mso-hide: all !important; }
  .mobile-off { display: none !important; height: 0px !important; width: 0px !important; }
  .mobile-on, .mobile-display-block { display: block !important; }
  .full-width-auto { width: auto !important; display: block !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .height-auto { height: auto !important; }
  .center-text { text-align: center !important; }
  .pd40 { padding: 40px !important; }
  .FSize01 { font-size: 28px !important; line-height: 32px !important; }
  .BgBlue { background-color: rgba(0,23,90,0.7) !important; }
}
```

### D) Footer nav (single-row con `<th>` por link)

Cada `<th>` de link debe tener `.full-width-block` + `.fm-border` para simular separadores:
```css
@media only screen and (max-width: 619px) {
  .container { padding: 0 !important; width: 100% !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .fm-nav-link { padding: 15px 0 !important; }
  .fm-border { border-top: 1px solid #EFEFEF !important; }
}
```

### E) Imágenes — patrón de visibilidad desktop/mobile

Si el componente tiene imagen desktop y necesita imagen mobile alternativa:

```html
<!-- Imagen DESKTOP (se oculta en mobile) -->
<span class="mobile-off show-desktop">
  <img src="imagen-desktop.jpg" alt="descripción" width="310"
       style="border:0; display:block; height:auto; width:310px; max-width:100%;" />
</span>

<!-- Imagen MOBILE (se muestra en mobile, oculta en desktop y Outlook) -->
<span class="mobile-on" style="display:none; mso-hide:all;">
  <img src="imagen-mobile.jpg" alt="descripción" width="100%"
       style="border:0; display:block; height:auto; width:100%; max-width:100%;" />
</span>
```

### F) Imágenes fluidas (cualquier tipo)

```html
<img src="..." alt="..." width="[valor-fijo]"
     style="border:0; display:block; height:auto; width:[valor-fijo]px; max-width:100%;" />
```

## Paso 3 — Restricciones de baja libertad

- **NO** cambiar colores, tipografías, textos ni URLs
- **NO** reestructurar filas/columnas desktop que ya funcionan
- **NO** eliminar bloques VML de Outlook
- **NO** agregar propiedades CSS no soportadas por email clients sin fallback
- **NO** cambiar `width="620"` ni `style="width:620px"` del contenedor raíz
- Agregar solo las clases que faltan, sin reescribir el HTML completo

## Paso 4 — Entregar contrato de salida

Siempre terminar con este resumen:

```
## Cambios aplicados — [nombre-componente.html]

### Qué cambió
- [clase X agregada en elemento Y] → [razón]
- [media query Z actualizada] → [razón]
- [imagen mobile añadida/corregida] → [razón]

### Por qué
[justificación breve de cada cambio]

### Impacto mobile
[cómo se ve ahora en mobile vs antes]

### Impacto desktop / Outlook
[confirmación de que nada cambió en desktop 620px]

### Checklist QA
- [ ] iOS Mail — stack correcto
- [ ] Gmail app Android — imágenes fluidas
- [ ] Outlook desktop — estructura intacta, sin CSS
- [ ] Outlook web — comportamiento esperado
- [ ] NO PROBADO: [listar clientes no verificados explícitamente]
```
