# Referencias Responsive — Hero Components

Cubre: `hero-banner-overlay-v40`, `hero-banner-overlay-v42`, `hero-full-width-image`, `hero-full-width-text`

---

## hero-banner-overlay (HB03)

### Estructura de 3 columnas en desktop, apilada en mobile

El `<td>` con `background-image` contiene una tabla de 3 columnas `<th>`:

```
[spacer 43px] [texto / overlay] [imagen mobile hidden]
     ↕               ↕                    ↕
  .mobile-off    .full-width-auto       .full-width-auto
                 .BgBlue               mso-hide:all
                 .height-auto          imagen con .mobile-on
```

### Media query completo requerido

```css
@media only screen and (max-width: 619px) {
  .container    { padding: 0 !important; width: 100% !important; }
  .show-desktop { display: none !important; font-size: 0 !important;
                  max-height: 0 !important; line-height: 0 !important; mso-hide: all !important; }
  .mobile-off   { display: none !important; height: 0px !important; width: 0px !important; }
  .mobile-on, .mobile-display-block { display: block !important; }
  .full-width-auto  { width: auto !important; display: block !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .height-auto  { height: auto !important; }
  .center-text  { text-align: center !important; }
  .pd40         { padding: 40px !important; }
  .FSize01      { font-size: 28px !important; line-height: 32px !important; }
  .BgBlue       { background-color: rgba(0,23,90,0.7) !important; }
}
```

### VML requerido para fondo en Outlook

```html
<!--[if gte mso 9]>
<v:image xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false"
    style="border:0;display:inline-block;width:620px;height:320px;"
    src="https://URL-imagen-desktop.jpg" />
<v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false"
    style="border:0;display:inline-block;position:absolute;width:620px;height:320px;">
<v:fill opacity="0%" color="#ffffff" />
<v:textbox inset="0,0,0,0">
<![endif]-->
  <!-- contenido de la tabla de 3 columnas aquí -->
<!--[if gte mso 9]>
</v:textbox>
</v:rect>
<![endif]-->
```

### Riesgos conocidos
- Si se omite `mso-hide:all` en la columna de imagen mobile, Outlook la muestra siempre → doble imagen
- `rgba()` en `.BgBlue` no funciona en Outlook → el overlay no se ve en Outlook (aceptado: la imagen de fondo tampoco se ve en Outlook, usa VML)
- `background-size:contain` no funciona en Outlook → VML usa imagen full-size sin contain

---

## hero-full-width-image (HB15-v4.2)

### Estructura: 3 filas apiladas

```
[fila 1] imagen fotográfica full-width (desktop + mobile alt)
[fila 2] barra color #5d6165 + título blanco
[fila 3] fondo blanco + texto descriptivo
```

### Responsive mínimo requerido

```css
@media only screen and (max-width: 619px) {
  .container    { padding: 0 !important; width: 100% !important; }
  .mobile-off   { display: none !important; height: 0px !important; width: 0px !important; }
  .mobile-on    { display: block !important; }
  .height-auto  { height: auto !important; }
}
```

Imagen desktop + mobile (aplicar patrón de `responsive-snippets.md`).

---

## hero-full-width-text (HB15-v4.0)

### Estructura: columna única con fondo de color

Sin imagen → bajo riesgo. Solo verificar:
- `.container` en raíz
- Texto con `font-size` legible (≥15px)
- No hay padding fijo excesivo que aplaste el texto en mobile
