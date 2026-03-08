/**
 * Código para n8n: extrae HTML del output del agente y lo devuelve limpio.
 * Maneja: array [{ output: "..." }], markdown con bloques ```html.
 */

const fallback = String($('Code_fusionarHTML1').item.json.html ?? '').trim();

// Obtener raw: soporta array [{ output }] o objeto directo
const getRaw = (data) => {
  if (Array.isArray(data) && data.length > 0) {
    const first = data[0];
    return String(
      first.output ??
      first.html ??
      first.response ??
      first.text ??
      first.result ??
      first.message?.content?.[0]?.text ??
      first.content?.[0]?.text ??
      ''
    ).trim();
  }
  const obj = data && typeof data === 'object' ? data : {};
  return String(
    obj.output ??
    obj.html ??
    obj.response ??
    obj.text ??
    obj.result ??
    obj.message?.content?.[0]?.text ??
    obj.content?.[0]?.text ??
    ''
  ).trim();
};

const raw = getRaw($input?.item?.json ?? $json ?? $input ?? {});

// Extraer solo el bloque ```html ... ```
let html = '';
const htmlBlockMatch = raw.match(/```html\s*([\s\S]*?)```/i);
if (htmlBlockMatch) {
  html = htmlBlockMatch[1].trim();
} else {
  // Fallback: quitar prefijo markdown y sufijo ```
  html = raw
    .replace(/^[\s\S]*?```html\s*/i, '')
    .replace(/\s*```[\s\S]*$/i, '')
    .trim();
}

if (!html) {
  html = fallback;
}

const looksLikeHtml = /<(html|body|table|div|tr|td|img|a|p)\b/i.test(html);
if (!looksLikeHtml) {
  html = fallback;
}

if (!html) {
  throw new Error('AI Agent1 no devolvió HTML utilizable y no hay fallback.');
}

const source = html === fallback ? 'fallback_code_fusionar' : 'agent_output';

// Minificar: quitar saltos de línea y espacios múltiples entre tags
html = html
  .replace(/>\s+</g, '><')
  .replace(/\s+/g, ' ')
  .trim();

return [{
  json: {
    html,
    source,
  },
}];
