const imageAuditStyles = document.createElement('link');
imageAuditStyles.rel = 'stylesheet';
imageAuditStyles.href = 'sistema90g-final-images.css?v=20260705-audit-images3';
document.head.appendChild(imageAuditStyles);

const conversionStyles = document.createElement('link');
conversionStyles.rel = 'stylesheet';
conversionStyles.href = 'home-conversion.css?v=20260705-home1';
document.head.appendChild(conversionStyles);

import('./site-ui-clean.js?v=20260705-audit-images3');
import('./home-conversion.js?v=20260705-home1');
import('./case-16-inject.js?v=20260704-case16');