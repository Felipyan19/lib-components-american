---
description: Mejora responsive de componentes HTML de email de forma aislada por componente (no layout global), manteniendo ancho desktop 620px y compatibilidad Outlook/MSO. Usar al editar o refactorizar componentes en libs/components/*/*.html o libs/Click Experts/*/*.html para stack móvil, visibilidad mobile/desktop, imágenes fluidas y spacing seguro. Activa cuando el usuario pide "hacer responsive", "arreglar mobile", "aplicar responsive", "refactorizar" o "mejorar" un componente de email.
---

# Skill: email-component-responsive-refactor

## Objetivo
Aplicar mejoras responsive a UN componente de forma conservadora, sin cambiar estructura desktop ni romper Outlook. Cada cambio debe ser justificado.

## Paso 1 — Leer y clasificar antes de tocar

Leer el archivo completo. Identificar:
1. **Tipo de componente** (ver tabla en `audit` skill)
2. **Familia de clases**: ¿usa `hideMbl`/`showMbl` (Centurion) o `mobile-off`/`mobile-on` (Clásica)?
3. **Patrón de layout**: columna única / 2 columnas 50/50 / bg-image+overlay / 2 cols con gutters laterales
4. **Estado actual del `<style>`**: ¿existe `@media`? ¿qué clases hay? ¿dos bloques `<style>` separados?
5. **Imágenes**: ¿hay versión mobile? ¿tienen `alt`? ¿están envueltas en `hideMbl`/`showMbl`?

**Si hay dudas sobre el tipo o la familia → preguntar, no asumir.**
**No mezclar clases de familia Clásica con familia Centurion en el mismo archivo.**

## Paso 2 — Aplicar cambios por tipo

### A) Componentes de columna única (intro-text, cta-banner, terms, preheader, section-divider, contact-cta)

Solo verificar y agregar si falta:
```css
@media only screen and (max-width: 619px) {
  .container { padding: 0 !important; width: 100% !important; }
}
```
En el `<table>` raíz: `class="container"` si no lo tiene.

### B) Componentes de 2 columnas 50/50 — familia Clásica (horizontal-pair, hotel-card, section-*)

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

### B2) CIM02 Horizontal Pairs — familia Centurion (D-Image-Modules, templates Click Experts)

El CIM02 tiene **4 columnas** (gutter izq + col-A + col-B + gutter der). Las dos gutters deben ocultarse en mobile:

```html
<!-- Gutter izquierdo -->
<th width="20" class="im-block no-border hideMbl" dir="ltr"
    style="direction: ltr; font-size: 0px; font-weight: normal; padding: 0px; width: 20px; max-width: 20px;" valign="middle">&nbsp;</th>

<!-- Columna A (contenido) -->
<th width="290" class="im-block no-border" dir="ltr"
    style="direction: ltr; font-size: 0px; font-weight: normal; padding: 0px 0px 0px 0px;" align="left" valign="top">
  <!-- contenido -->
</th>

<!-- Columna B (contenido) -->
<th width="270" height="auto" dir="ltr" class="im-block-auto noPadR"
    style="direction: ltr; font-weight: normal; padding: 0px 0px 0px 0px" align="right" valign="top">
  <!-- contenido -->
</th>

<!-- Gutter derecho -->
<th width="40" class="im-block no-border hideMbl" dir="ltr"
    style="direction: ltr; font-size: 0px; font-weight: normal; padding: 0px; width: 40px; max-width: 40px;" valign="middle">&nbsp;</th>
```

Media query requerida (ya presente en D-Image-Modules como bloque 2):
```css
@media only screen and (max-width: 619px) {
  .hideMbl { display: none !important; }
  .showMbl { display: inline-block !important; }
  .ImgWidth, .full-img { width: 100% !important; display: block !important; }
  .noPadR { padding-top: 30px !important; padding-right: 0px !important; padding-left: 0px !important; border-top: 1px solid #000000 !important; }
  .padd-t30 { padding: 30px 0px 0px 0px !important; }
  .padd-b30 { padding: 0px 0px 30px 0px !important; }
  .PaddLR { padding: 0px 20px !important; }
  .border-top { padding: 20px 0px 20px !important; border-top: 1px solid #000000 !important; }
}
```

Para el par de imágenes desktop/mobile en CIM02 Centurion:
```html
<!-- Imagen DESKTOP -->
<span class="hideMbl">
  <img src="imagen-desktop.jpg" alt="descripción" width="[N]"
       style="height:auto; display:block; color:#333333;" class="full-width">
</span>

<!-- Imagen MOBILE -->
<span class="showMbl" style="display: none;">
  <img src="imagen-mobile.jpg" alt="descripción" width="100%"
       style="height:auto; display:block; color:#333333;" class="full-width">
</span>
```

### B3) CIM02 con una sola columna central (Priority Pass, texto ancho)

Cuando el CIM02 tiene solo una columna activa (la segunda está vacía o ausente):
```html
<th width="290" class="im-block no-border" dir="ltr"
    style="direction: ltr; font-size: 0px; font-weight: normal; padding: 0px;"
    align="left" valign="top">
  <!-- todo el contenido aquí -->
</th>
<!-- No hay segunda columna de contenido, solo el gutter derecho -->
<th width="40" class="im-block no-border hideMbl" ...>&nbsp;</th>
```
En mobile, el contenido ocupa 100% automáticamente por `.im-block`.

### B4) CIM02 imagen + panel (horizontal pair con imagen y panel de contenido — Centurion)

Cuando la columna imagen tiene ancho fijo y la columna panel es flex. Requiere `dir="rtl"` para imagen derecha:
```html
<table dir="rtl" role="presentation" ... bgcolor="#000000">
  <tr>
    <!-- Columna imagen -->
    <th class="im-block" width="50%" dir="ltr" style="..." align="center" valign="middle">
      <span class="hideMbl"><img src="desktop.jpg" width="100%" .../></span>
      <span class="showMbl" style="display:none;"><img src="mobile.jpg" width="100%" .../></span>
    </th>
    <!-- Columna panel -->
    <th width="50%" dir="ltr" class="im-block-auto im-horz-pair-padding PaddLR"
        style="direction: ltr; font-weight: normal; padding: 0; background: #000000"
        align="center" valign="middle">
      <!-- contenido -->
    </th>
  </tr>
</table>
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

### E) Imágenes — par desktop/mobile — familia CLÁSICA

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

### E2) Imágenes — par desktop/mobile — familia CENTURION

```html
<!-- Imagen DESKTOP -->
<span class="hideMbl">
  <img src="imagen-desktop.jpg" alt="descripción" width="310"
       style="height:auto; display:block; color:#333333;" />
</span>

<!-- Imagen MOBILE -->
<span class="showMbl" style="display: none;">
  <img src="imagen-mobile.jpg" alt="descripción" width="100%"
       style="height:auto; display:block; color:#333333;" />
</span>
```

### F) Imágenes fluidas (cualquier tipo)

```html
<img src="..." alt="..." width="[valor-fijo]"
     style="border:0; display:block; height:auto; width:[valor-fijo]px; max-width:100%;" />
```

### G) Separadores/Spacers — familia Centurion

Los separadores con `class="hideMbl"` desaparecen en mobile. Los spacers con `height` fijo sin `.hideMbl` rompen el layout. Verificar y agregar clase cuando corresponda:
```html
<!-- Separador que debe desaparecer en mobile -->
<div style="background: #ffffff; margin: 0px auto; max-width: 620px" class="hideMbl">
  <table ...><tr><td height="34" ...>&nbsp;</td></tr></table>
</div>
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
