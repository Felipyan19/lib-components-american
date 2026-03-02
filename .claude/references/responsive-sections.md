# Referencias Responsive — Section Components

Cubre: `section-compras`, `section-gastronomia`, `section-hoteles`,
`cross-sell-icons-2`, `cross-sell-icons-4`, `offer-code-hotel-benefits`,
`brand-panel` (consumer/gold/platinum), `preheader`, `intro-text`,
`section-divider`, `contact-cta`, `cta-banner`

---

## section-compras / section-gastronomia / section-hoteles

### Estructura: header azul + body 2 columnas

```
[header] bg #006FCF | ícono 51px | título uppercase blanco
[body]   <th 50%>  |  divisor  |  <th 50%>
```

El `<tr>` del body usa el mismo patrón que `horizontal-pair`:
ambas celdas `<th>` deben tener `.full-width-block`.

```css
@media only screen and (max-width: 619px) {
  .container        { padding: 0 !important; width: 100% !important; }
  .full-width-block { width: 100% !important; display: block !important; }
  .height-auto      { height: auto !important; }
  .mobile-off       { display: none !important; height: 0px !important; width: 0px !important; }
  .mobile-on        { display: block !important; }
}
```

El divisor vertical entre columnas (1px solid) es un `<th>` o `<td>` de 1px de ancho.
En mobile se puede ocultar con `.mobile-off` si está en una celda separada.

---

## cross-sell-icons-2 (FM01-v4.0) y cross-sell-icons-4 (FM01-v4.2)

### cross-sell-icons-2 (2 íconos)
Dos `<th>` de 50% cada uno. Aplicar `.full-width-block` en mobile si se quiere stack.
Si se prefieren en fila en mobile (>320px), no es necesario cambio.

### cross-sell-icons-4 (4 íconos)
Cuatro `<th>` en una fila. En mobile (320px) pueden quedar muy apretados.
Opciones:
1. Stack a 2 columnas: complejo con solo media query → evaluar si es necesario
2. Mantener 4 en fila con íconos más pequeños: aceptable si no rompe visualmente
3. Reemplazar por 2+2 con `full-width-block` en pares

**Default conservador:** verificar que los íconos tengan `max-width:100%` y el texto sea legible.

---

## offer-code-hotel-benefits

### Estructura: columna única, grilla 2x2 de beneficios

Cada beneficio: `<td>` con ícono inline + texto. En mobile, el texto debe ser legible.
Sin cambios estructurales necesarios. Solo verificar:
- Imagen separadora al final tiene `width="100%"` + par mobile si existe
- Íconos 39px tienen `height:auto` si son fluidos (o `height="39"` fijo si son cuadrados)

---

## brand-panel (consumer / gold / platinum)

### Estructura: 2 filas
- Fila 1: logo + tagline (mobile-off) + info cuenta + imagen tarjeta
- Fila 2: saludo nombre + botón "Mi cuenta"

**Tagline** (imagen decorativa entre logo y cuenta): debe tener `.mobile-off` o `.show-desktop`.

```css
@media only screen and (max-width: 619px) {
  .container        { padding: 0 !important; width: 100% !important; }
  .show-desktop     { display: none !important; font-size: 0 !important;
                      max-height: 0 !important; line-height: 0 !important;
                      mso-hide: all !important; }
  .mobile-off       { display: none !important; height: 0px !important; width: 0px !important; }
}
```

La imagen de tarjeta (80px) NO se oculta en mobile.
El botón "Mi cuenta" puede requerir `.full-width-auto` si está en `<td>` con ancho fijo.

---

## preheader (PH01-v4.0 / v4.2)

Columna única, fila única. Mínimo riesgo.
Solo verificar `.container` en el `<table>` raíz.

---

## intro-text (TM04)

Columna única, texto centrado. Mínimo riesgo.
Verificar `padding: 40px 20px` → 20px de padding lateral en mobile es suficiente.

---

## section-divider (TM06)

Columna única con HR + texto + HR. Sin imagen. Mínimo riesgo.
Solo `.container` en raíz.

---

## contact-cta (TM17)

Columna única con texto + botón. Verificar:
- Botón tiene fallback VML si corresponde (ver `responsive-snippets.md`)
- Texto descriptivo no tiene `width` fijo

---

## cta-banner-navy / cta-banner-blue (TM04)

Columna única con fondo de color. Mínimo riesgo.
Solo `.container` y verificar que el padding lateral no aplaste el texto en mobile.
Recomendado: `padding: 35px 20px` como mínimo en mobile.

---

## Tabla de riesgo por tipo

| Componente | Riesgo mobile | Prioridad refactor |
|---|---|---|
| hero-banner overlay | ALTO (VML + 3 col) | Alta |
| horizontal-pair | ALTO (2 col 50/50) | Alta |
| hotel-card | ALTO (2 col 50/50) | Alta |
| section-compras/gastro/hoteles | MEDIO-ALTO (2 col body) | Alta |
| brand-panel | MEDIO (tagline oculta) | Media |
| cross-sell-icons-4 | MEDIO (4 en fila) | Media |
| footer-nav | MEDIO (links en fila) | Media |
| hero-full-width-image | MEDIO (img mobile alt) | Media |
| offer-code-hotel-benefits | BAJO-MEDIO | Baja |
| preheader / intro-text / cta-banner / section-divider / terms | BAJO | Baja |
| social-icons / footer-tagline | BAJO | Baja |
