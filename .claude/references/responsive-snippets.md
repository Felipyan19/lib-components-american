# Snippets canónicos — Responsive Email AMEX Argentina

> Fuente única de verdad para patrones responsive. No copiar variantes sueltas.
> Si cambias una regla aquí, refleja el cambio en el skill que la referencia.

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
