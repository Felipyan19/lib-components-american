# Referencias Responsive — Horizontal Pair & Hotel Card

Cubre: `horizontal-pair-ltr`, `horizontal-pair-rtl`, `horizontal-pair-ltr-logos`,
`hotel-card-ltr`, `hotel-card-rtl`

Todos son layouts de **2 columnas 50/50** (`<th>` de 310px cada uno) que deben
apilar en mobile (imagen arriba, contenido abajo).

---

## Patrón canónico 2 columnas → stack mobile

```html
<table role="none" cellpadding="0" cellspacing="0" border="0" width="620"
    style="margin:0 auto;width:620px;background:#FFFFFF;" class="container">
  <tr>
    <!-- Columna imagen (LTR: izquierda | RTL: derecha según dir) -->
    <th class="full-width-block" dir="ltr" width="50%" align="center" valign="middle">
      <!-- Par desktop/mobile: ver responsive-snippets.md -->
    </th>

    <!-- Columna contenido -->
    <th class="full-width-block height-auto" width="50%" height="354"
        align="center" valign="middle" bgcolor="#FFFFFF"
        style="background-color:#FFFFFF;">
      <!-- contenido interno -->
    </th>
  </tr>
</table>
```

Media query mínimo:
```css
@media only screen and (max-width: 619px) {
  .container        { padding: 0 !important; width: 100% !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .height-auto      { height: auto !important; }
  .mobile-off, .show-desktop {
    display: none !important; height: 0px !important; width: 0px !important;
  }
  .mobile-on        { display: block !important; }
}
```

---

## Dirección de stack en mobile

- **LTR** (`dir="ltr"`, imagen izquierda desktop): en mobile, imagen va **arriba** (primer `<th>`)
- **RTL** (`dir="rtl"`, imagen derecha desktop): en mobile, imagen va **abajo** (segundo `<th>`)
  → Para que imagen RTL quede arriba en mobile, usar `dir="rtl"` en la tabla raíz o re-ordenar los `<th>` con CSS (no soportado en todos los clientes → preferir aceptar imagen abajo)

---

## Variante con logos de marca (horizontal-pair-ltr-logos)

La columna de contenido incluye una fila adicional con 3 logos inline:

```html
<!-- Fila de logos de marca (Jumbo, Disco, Vea, etc.) -->
<tr>
  <td align="center" style="padding: 10px 0 0;">
    <img src="logo1.png" alt="Marca 1" width="60" height="auto"
         style="border:0; display:inline-block; height:auto; max-width:100%;" />
    <img src="logo2.png" alt="Marca 2" width="60" height="auto"
         style="border:0; display:inline-block; height:auto; max-width:100%; margin-left:10px;" />
    <img src="logo3.png" alt="Marca 3" width="60" height="auto"
         style="border:0; display:inline-block; height:auto; max-width:100%; margin-left:10px;" />
  </td>
</tr>
```

En mobile (columna al 100%), los logos se mantienen inline → no se necesita cambio extra.

---

## Hotel Card (hotel-card-ltr / hotel-card-rtl)

Igual que `horizontal-pair` en estructura. Diferencias:
- Fondo: `#F4F5F6` (gris claro)
- No tiene CTA button
- Columna contenido: solo texto (nombre hotel, descripción, fechas)

```html
<th class="full-width-block" width="50%" bgcolor="#F4F5F6"
    style="background-color:#F4F5F6;" valign="middle">
  <table role="none" ...>
    <tr>
      <td style="padding: 20px; font-family:...; font-size:16px; color:#00175A;">
        <strong>Nombre del Hotel</strong>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 20px 5px; font-size:15px; color:#53565A;">
        Descripción del hotel.
      </td>
    </tr>
    <tr>
      <td style="padding: 0 20px 20px; font-size:10px; color:#53565A; text-transform:uppercase;">
        Validez: DD/MM/AAAA al DD/MM/AAAA
      </td>
    </tr>
  </table>
</th>
```

---

## Riesgos conocidos

| Problema | Causa | Solución |
|---|---|---|
| Columnas no apilan en Outlook | Outlook ignora `display:block` en `<th>` | `<th>` en Outlook sí apila si el contenedor es 100% ancho — verificar que el contenedor no tenga `width:620px` hardcodeado en Outlook con condicional `<!--[if mso]>` |
| Imagen desktop visible en mobile | Falta clase `.mobile-off` o `.show-desktop` | Agregar clase y verificar que la media query la oculte |
| Imagen mobile visible en desktop | Falta `style="display:none; mso-hide:all"` en el `<span>` | Agregar atributo inline |
| Contenido muy pequeño en mobile al 100% | Padding interno insuficiente en mobile | Agregar clase de padding override en el `<td>` de contenido |
