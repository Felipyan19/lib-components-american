# Snippets canónicos — Responsive Email AMEX Argentina

> Fuente única de verdad para patrones responsive. No copiar variantes sueltas.
> Si cambias una regla aquí, refleja el cambio en el skill que la referencia.
>
> **Dos familias de clases coexisten en este repositorio:**
> - **Clásica**: `libs/components/*/` → usa `mobile-off`, `mobile-on`, `full-width-block`, `container`
> - **Centurion**: `libs/Click Experts/*/` → usa `hideMbl`, `showMbl`, `im-block`, `im-block-auto`, `im-horz-pair-padding`
>
> **No mezclar clases de ambas familias en el mismo archivo.**

---

## Media query base (breakpoint canónico)

```css
@media only screen and (max-width: 619px) {
  /* solo agregar lo que el componente necesita */
}
```

Breakpoint: **619px** (desktop = 620px, mobile = ≤ 619px).

---

## Clases responsive canónicas

### Contenedor raíz
```css
.container { padding: 0 !important; width: 100% !important; }
```
HTML: `<table width="620" style="width:620px; margin:0 auto;" class="container">`

### Stack de columnas (2-col 50/50)
```css
.full-width-block { width: 100% !important; display: block !important; }
```
HTML: `<th class="full-width-block" width="50%" ...>`

### Elemento auto-width en mobile
```css
.full-width-auto { width: auto !important; display: block !important; }
```

### Altura que colapsa en mobile
```css
.height-auto { height: auto !important; }
```
HTML: `<th height="354" class="full-width-block height-auto" ...>`

### Ocultar en mobile (desktop-only)
```css
.mobile-off { display: none !important; height: 0px !important; width: 0px !important; }
.show-desktop { display: none !important; font-size: 0 !important; max-height: 0 !important; line-height: 0 !important; mso-hide: all !important; }
```
- `.mobile-off` → para columnas/celdas completas
- `.show-desktop` → para elementos inline o `<span>` que deben desaparecer en mobile

### Mostrar en mobile (mobile-only)
```css
.mobile-on { display: block !important; }
.mobile-display-block { display: block !important; }
```
HTML: `<span class="mobile-on" style="display:none; mso-hide:all;">`

### Texto centrado en mobile
```css
.center-text { text-align: center !important; }
```

### Padding mobile en hero
```css
.pd40 { padding: 40px !important; }
```

### Font size mobile para headlines
```css
.FSize01 { font-size: 28px !important; line-height: 32px !important; }
```

### Overlay semitransparente en hero overlay mobile
```css
.BgBlue { background-color: rgba(0,23,90,0.7) !important; }
```

---

## Imagen fluida (canon)

```html
<img src="..." alt="descripción" width="310"
     style="border:0; display:block; height:auto; width:310px; max-width:100%;" />
```

- `width` attr = valor numérico (sin px) para Outlook
- `style` incluye `max-width:100%` para mobile
- `height:auto` siempre

## Par desktop/mobile de imágenes

```html
<!-- Desktop: visible en desktop, oculta en mobile -->
<span class="mobile-off show-desktop">
  <img src="img-desktop.jpg" alt="..." width="310"
       style="border:0; display:block; height:auto; width:310px; max-width:100%;" />
</span>

<!-- Mobile: oculta en desktop y Outlook, visible en mobile -->
<span class="mobile-on" style="display:none; mso-hide:all;">
  <img src="img-mobile.jpg" alt="..." width="100%"
       style="border:0; display:block; height:auto; width:100%; max-width:100%;" />
</span>
```

---

## Botón CTA (con fallback VML para Outlook)

```html
<div align="center">
  <!--[if mso]>
  <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      href="https://URL"
      style="v-text-anchor:middle;width:230px;height:40px;
             font-family:HelveticaNeue,Helvetica Neue Regular,Helvetica,Arial,sans-serif;
             font-size:15px;font-weight:normal;color:#FFFFFF;"
      arcsize="3%" strokecolor="#006fcf" fillcolor="#006fcf" strokeweight="1pt">
    <w:anchorlock/><center>
  <![endif]-->
  <a href="https://URL" target="_blank"
     style="width:230px;height:40px;display:inline-block;
            background-color:#006fcf;border-radius:3px;color:#FFFFFF;
            font-family:HelveticaNeue,Helvetica Neue Regular,Helvetica,Arial,sans-serif;
            font-size:15px;font-weight:normal;line-height:40px;
            text-align:center;text-decoration:none;border:1px solid #006fcf;">
    <strong style="color:#FFFFFF;text-decoration:none;border:none;outline:0;font-weight:normal;">
      Texto del botón
    </strong>
  </a>
  <!--[if mso]></center></v:roundrect><![endif]-->
</div>
```

---

## Footer nav — links en columna mobile

```html
<!-- Cada <th> de link en footer-nav -->
<th role="listitem" class="fm-nav-link full-width-block fm-border"
    style="padding: 0 10px; font-family:...">
  <a href="..." target="_blank" class="link"
     style="color:#006fcf; font-size:15px; line-height:22px;
            text-decoration:none; display:block; padding:12px 0; font-family:...">
    Link label
  </a>
</th>
```

Media query para footer-nav:
```css
.fm-nav-link { padding: 15px 0 !important; }
.fm-border { border-top: 1px solid #EFEFEF !important; }
```

---

## Imagen fluida en CFT (footer terms)

```css
.Cft { width: 96% !important; max-width: 96% !important; height: auto !important; }
```
HTML: `<img class="Cft" ... width="368" height="65" style="display:inline-block; outline:none; border:0;">`

---

## FAMILIA CENTURION — Clases canónicas

> Usadas en `libs/Click Experts/*/` (Centurion, Marigold). No mezclar con familia Clásica.

### Visibilidad mobile/desktop

```css
/* Ocultar en mobile */
.hideMbl { display: none !important; }

/* Mostrar en mobile (requiere style="display:none" inline en desktop) */
.showMbl { display: inline-block !important; }
```

HTML para columnas gutter (deben desaparecer en mobile):
```html
<th width="20" class="im-block no-border hideMbl" dir="ltr"
    style="direction:ltr; font-size:0px; font-weight:normal; padding:0px; width:20px; max-width:20px;" valign="middle">&nbsp;</th>
```

### Stack de columnas CIM02

```css
/* Columna principal → stack a 100% en mobile */
.im-block { display: block !important; width: 100% !important; }

/* Columna de contenido → auto width en mobile */
.im-block-auto { display: block !important; width: auto !important; height: auto !important; }

/* Padding override para columna de contenido en mobile */
.im-horz-pair-padding { padding: 48px 6% !important; }
```

### Utilitarios de padding mobile (Centurion)

```css
.noPadR       { padding-top: 30px !important; padding-right: 0px !important; padding-left: 0px !important; border-top: 1px solid #000000 !important; }
.padd-t30     { padding: 30px 0px 0px 0px !important; }
.padd-b30     { padding: 0px 0px 30px 0px !important; }
.PaddLR       { padding: 0px 20px !important; }
.border-top   { padding: 20px 0px 20px !important; border-top: 1px solid #000000 !important; }
.padTop20     { padding-top: 20px !important; padding-bottom: 20px !important; }
.padd-t       { padding-top: 20px !important; }
```

### Par de imágenes desktop/mobile — Centurion

```html
<!-- Desktop: visible normalmente, oculta en mobile vía .hideMbl -->
<span class="hideMbl">
  <img src="imagen-desktop.jpg" alt="descripción" width="310"
       style="height:auto; display:block; color:#333333;" />
</span>

<!-- Mobile: oculta en desktop con style inline, mostrada via .showMbl -->
<span class="showMbl" style="display: none;">
  <img src="imagen-mobile.jpg" alt="descripción" width="100%"
       style="height:auto; display:block; color:#333333;" />
</span>
```

### Separadores — Centurion

```html
<!-- Separador que desaparece en mobile → agregar class="hideMbl" -->
<div style="background:#ffffff; margin:0px auto; max-width:620px" class="hideMbl">
  <table role="presentation" ...>
    <tr><td height="34" style="height:34px; line-height:34px;">&nbsp;</td></tr>
  </table>
</div>
```

### Wrapper pattern — Centurion (800px outer + 620px content)

Los templates Centurion usan un wrapper externo de 800px y tablas de contenido a 620px:
```html
<!-- Wrapper externo 800px -->
<div class="wrapper" style="margin:0px auto; width:800px; background-color:#ffffff">
  <!-- Tablas de contenido con max-width:620px -->
  <table role="presentation" ... style="... max-width:620px" align="center">
    ...
  </table>
</div>
```

Media query para el wrapper:
```css
.wrapper { margin: 0 auto; width: 100% !important; max-width: 800px !important; }
```

**El contenido interno se limita a 620px vía `max-width:620px` en cada tabla, no en el wrapper.**
