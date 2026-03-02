# Referencias Responsive — Footer Components

Cubre: `footer-tagline`, `social-icons`, `footer-nav-v40`, `footer-nav-v42`,
`terms-v40`, `terms-v42`, `footer-combined`

---

## footer-tagline (FM05)

Imagen centrada de slogan. Bajo riesgo. Patrón:

```html
<span class="mobile-off">
  <img src="tagline-desktop.jpg" alt="No vivas la vida sin ella" width="100%"
       style="vertical-align:top; height:auto; color:#333333;" />
</span>
<span class="mobile-on" style="display:none;">
  <img src="tagline-mobile.jpg" alt="No vivas la vida sin ella" width="100%"
       style="display:block; vertical-align:top; height:auto; color:#333333;" />
</span>
```

Si solo hay una imagen (sin versión mobile), asegurarse de que sea `width="100%"` y `height:auto`.

---

## social-icons (FM02)

Fila de 3 íconos 28px con 30px de separación. No requiere stack en mobile.
Verificar únicamente:
- `width="28"` + `height="28"` en cada `<img>`
- `style="display:block; height:28px; width:28px;"` — **NO** `height:auto` (íconos cuadrados fijos)
- `alt` descriptivo en cada ícono

---

## footer-nav-v40 (FM03-v4.0)

Links en `<th>` con `padding: 0 30px`. En mobile: stack vertical con separadores.

```css
@media only screen and (max-width: 619px) {
  .container        { padding: 0 !important; width: 100% !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .fm-nav-link      { padding: 15px 0 !important; }
  .fm-border        { border-top: 1px solid #EFEFEF !important; }
}
```

HTML de cada link (salvo el primero que no lleva `.fm-border`):
```html
<th class="fm-nav-link full-width-block fm-border"
    style="padding: 0 30px; font-family:...">
  <a href="..." target="_blank" class="link"
     style="color:#006fcf; font-size:15px; line-height:22px;
            text-decoration:none; padding:12px 0; font-family:...">
    Privacidad
  </a>
</th>
```

---

## footer-nav-v42 (FM03-v4.2)

Igual estructura que v4.0 pero:
- Color de links: `#000000` (no `#006fcf`)
- Padding interno: `0 10px` (no `0 30px`)
- Cada link tiene `display:block` en el `<a>` (no solo en el `<th>`)
- Roles ARIA: `role="list"` en `<tr>`, `role="listitem"` en cada `<th>`

```html
<table role="none" ...>
  <tr role="list">
    <th role="listitem" class="fm-nav-link full-width-block"
        style="padding: 0 10px; font-family:...">
      <a href="..." class="link"
         style="color:#000000; display:block; padding:12px 0; ...">
        Privacidad
      </a>
    </th>
    <th role="listitem" class="fm-nav-link full-width-block fm-border"
        style="padding: 0 10px; font-family:...">
      ...
    </th>
  </tr>
</table>
```

---

## terms-v40 (FM04-v4.0)

- Fondo: `#D9D9D6`
- Incluye imagen CFT (`368×65px`) con clase `.Cft`
- Texto legal justificado, uppercase, 13px

```css
@media only screen and (max-width: 619px) {
  .container { padding: 0 !important; width: 100% !important; }
  .Cft { width: 96% !important; max-width: 96% !important; height: auto !important; }
}
```

---

## terms-v42 (FM04-v4.2)

- Fondo: `#E0E0E0`
- Sin imagen CFT, solo texto legal
- Media query: solo `.container`

---

## footer-combined

Contiene los 4 sub-componentes en secuencia. Aplicar reglas de cada sección.
Media query combinado (unión de todas las reglas necesarias):

```css
@media only screen and (max-width: 619px) {
  .container        { padding: 0 !important; width: 100% !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .mobile-off       { display: none !important; height: 0px !important; width: 0px !important; }
  .mobile-on        { display: block !important; }
  .fm-nav-link      { padding: 15px 0 !important; }
  .fm-border        { border-top: 1px solid #EFEFEF !important; }
  .Cft              { width: 96% !important; max-width: 96% !important; height: auto !important; }
}
```

---

## Riesgos conocidos

| Problema | Causa | Solución |
|---|---|---|
| Links del footer-nav no apilan en mobile | Falta `.full-width-block` en `<th>` | Agregar clase |
| Separadores no aparecen entre links en mobile | Falta `.fm-border` en los `<th>` | Agregar clase (excepto primer link) |
| Imagen CFT desborda en mobile | Falta `.Cft` o media query | Agregar clase y regla CSS |
| Imagen tagline no cambia en mobile | Falta versión mobile o clase `.mobile-on` | Agregar par desktop/mobile |
