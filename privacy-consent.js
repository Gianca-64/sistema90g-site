const GA_ID='G-G5D6FNDR00';
const CONSENT_KEY='s90g_cookie_consent';
const WHATSAPP_CHAT_URL='https://wa.me/393275478485?text=Ciao%2C%20ho%20una%20domanda%20rapida%20su%20Sistema%2090G.';

function loadAuditFix(){
  if(document.querySelector('link[data-s90g-audit-fix]'))return;
  const link=document.createElement('link');
  link.rel='stylesheet';
  link.href='sistema90g-audit-fix-20260707.css?v=20260707e';
  link.dataset.s90gAuditFix='true';
  document.head.appendChild(link);
}
function loadAnalytics(){if(window.s90gAnalyticsLoaded)return;window.s90gAnalyticsLoaded=true;if(typeof window.gtag!=='function')return;window.gtag('consent','update',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});window.gtag('config',GA_ID)}
function denyAnalytics(){if(typeof window.gtag!=='function')return;window.gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'})}
function hideCookieBanner(b){if(b)b.setAttribute('hidden','')}
function showCookieBanner(b){if(b)b.removeAttribute('hidden')}
function saveConsent(c){window.localStorage.setItem(CONSENT_KEY,c)}
function trackLead(name,link){if(window.localStorage.getItem(CONSENT_KEY)!=='accepted'||typeof window.gtag!=='function')return;window.gtag('event',name,{event_category:'lead',link_url:link.href,link_text:link.textContent.trim(),transport_type:'beacon'})}
function addWhatsAppChat(){if(document.querySelector('.whatsapp-chat'))return;const w=document.createElement('div');w.className='whatsapp-chat';w.innerHTML=`<a href="${WHATSAPP_CHAT_URL}" target="_blank" rel="noopener" data-track-whatsapp aria-label="Apri la chat WhatsApp per una domanda rapida"><span class="whatsapp-chat-copy"><span>Domande rapide</span><strong>Chat WhatsApp</strong></span></a>`;document.body.appendChild(w)}

document.addEventListener('DOMContentLoaded',()=>{
  loadAuditFix();
  addWhatsAppChat();
  const b=document.getElementById('cookie-banner'),c=localStorage.getItem(CONSENT_KEY);
  if(c==='accepted'){hideCookieBanner(b);loadAnalytics()}else if(c==='rejected'){hideCookieBanner(b);denyAnalytics()}else showCookieBanner(b);
  document.querySelectorAll('[data-cookie-choice]').forEach(x=>x.addEventListener('click',()=>{const ok=x.dataset.cookieChoice==='accept';saveConsent(ok?'accepted':'rejected');hideCookieBanner(b);ok?loadAnalytics():denyAnalytics()}));
  document.querySelectorAll('[data-cookie-settings]').forEach(x=>x.addEventListener('click',e=>{e.preventDefault();showCookieBanner(b)}));
  document.querySelectorAll('[data-track-whatsapp]').forEach(x=>x.addEventListener('click',()=>trackLead('whatsapp_chat_open',x)));
  document.querySelectorAll('[data-track-portal]').forEach(x=>x.addEventListener('click',()=>trackLead('public_portal_open',x)));
});
