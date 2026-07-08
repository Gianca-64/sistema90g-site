const GA_ID='G-G5D6FNDR00';
const CONSENT_KEY='s90g_cookie_consent';
const WHATSAPP_CHAT_URL='https://wa.me/393275478485?text=Ciao%2C%20ho%20una%20domanda%20rapida%20su%20Sistema%2090G.';

function loadAuditFix(){
  if(document.querySelector('link[data-s90g-audit-fix]'))return;
  const link=document.createElement('link');
  link.rel='stylesheet';
  link.href='sistema90g-audit-fix-20260707.css?v=20260708al';
  link.dataset.s90gAuditFix='true';
  document.head.appendChild(link);
}
function hasArticleType(item){
  if(!item)return false;
  const type=item['@type'];
  return type==='Article'||(Array.isArray(type)&&type.includes('Article'));
}
function hasStaticArticleSchema(){
  return [...document.querySelectorAll('script[type="application/ld+json"]')].some(script=>{
    try{
      const data=JSON.parse(script.textContent||'{}');
      const items=Array.isArray(data)?data:(Array.isArray(data['@graph'])?data['@graph']:[data]);
      return items.some(hasArticleType);
    }catch{return false;}
  });
}
function addStructuredData(){
  if(document.querySelector('script[data-s90g-structured-data]'))return;
  const canonical=document.querySelector('link[rel="canonical"]')?.href||location.href;
  const title=document.querySelector('h1')?.textContent.trim()||document.title;
  const description=document.querySelector('meta[name="description"]')?.content||'';
  const image=document.querySelector('main img')?.src||'https://sistema90g.it/images/01_HOME_HERO.png';
  const graph=[
    {'@type':'Organization','@id':'https://sistema90g.it/#organization','name':'Sistema 90G','url':'https://sistema90g.it/','logo':{'@type':'ImageObject','url':'https://sistema90g.it/images/favicon-512.png'},'founder':{'@id':'https://sistema90g.it/chi-e-sistema90g.html#person'},'description':'Servizio indipendente di analisi preventiva per progetti casa, cucine, distribuzione interna e preventivi.'},
    {'@type':'Person','@id':'https://sistema90g.it/chi-e-sistema90g.html#person','name':'Gian Carlo Primo','url':'https://sistema90g.it/chi-e-sistema90g.html','jobTitle':'Tecnico indipendente per analisi preventiva di progetti casa e cucina','worksFor':{'@id':'https://sistema90g.it/#organization'}},
    {'@type':'WebSite','@id':'https://sistema90g.it/#website','url':'https://sistema90g.it/','name':'Sistema 90G','publisher':{'@id':'https://sistema90g.it/#organization'},'inLanguage':'it-IT'},
    {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'isPartOf':{'@id':'https://sistema90g.it/#website'},'about':{'@id':'https://sistema90g.it/#organization'},'primaryImageOfPage':{'@type':'ImageObject','url':image},'inLanguage':'it-IT'}
  ];
  if(location.pathname.includes('caso-')&&!hasStaticArticleSchema()){
    graph.push({'@type':'Article','headline':title,'description':description,'image':[image],'mainEntityOfPage':canonical,'author':{'@id':'https://sistema90g.it/chi-e-sistema90g.html#person'},'publisher':{'@id':'https://sistema90g.it/#organization'},'inLanguage':'it-IT'});
  }
  const script=document.createElement('script');
  script.type='application/ld+json';
  script.dataset.s90gStructuredData='true';
  script.textContent=JSON.stringify({'@context':'https://schema.org','@graph':graph});
  document.head.appendChild(script);
}
function optimizeImages(){
  const images=[...document.querySelectorAll('img')];
  images.forEach((img,index)=>{
    img.decoding='async';
    if(img.getAttribute('src')?.includes('case-19-tiranti-cavi-ispezionabilita.svg')){
      img.src='images/20_CASI_DISTRIBUZIONE.png?v=20260708al';
    }
    img.addEventListener('error',()=>{
      if(img.dataset.s90gFallbackApplied)return;
      img.dataset.s90gFallbackApplied='true';
      img.src='images/20_CASI_DISTRIBUZIONE.png?v=20260708al';
    });
    if(index===0||img.closest('.s90g-hero-media,.s90g-inner-media,.premium-hero')){
      img.loading='eager';
      img.fetchPriority='high';
    }else{
      img.loading='lazy';
    }
  });
}
function loadAnalytics(){if(window.s90gAnalyticsLoaded)return;window.s90gAnalyticsLoaded=true;if(typeof window.gtag!=='function')return;window.gtag('consent','update',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});window.gtag('config',GA_ID)}
function denyAnalytics(){if(typeof window.gtag!=='function')return;window.gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'})}
function hideCookieBanner(b){if(b)b.setAttribute('hidden','')}
function showCookieBanner(b){if(b)b.removeAttribute('hidden')}
function saveConsent(c){window.localStorage.setItem(CONSENT_KEY,c)}
function trackLead(name,link){if(window.localStorage.getItem(CONSENT_KEY)!=='accepted'||typeof window.gtag!=='function')return;window.gtag('event',name,{event_category:'lead',link_url:link.href,link_text:link.textContent.trim(),transport_type:'beacon'})}
function addWhatsAppChat(){
  if(document.querySelector('.s90g-chat-launcher'))return;
  const wrapper=document.createElement('div');
  wrapper.className='s90g-chat-widget';
  wrapper.innerHTML=`<button class="s90g-chat-launcher" type="button" aria-expanded="false" aria-controls="s90g-chat-popup"><span aria-hidden="true">💬</span><span>Chat</span></button><section class="s90g-chat-popup" id="s90g-chat-popup" hidden aria-label="Chat Sistema 90G"><button class="s90g-chat-close" type="button" aria-label="Chiudi la chat">×</button><p class="s90g-chat-kicker">Domande rapide</p><h2>Come posso aiutarti?</h2><p>Per una domanda veloce puoi aprire WhatsApp. Per inviare foto, planimetrie o preventivi usa invece il portale pubblico.</p><div class="s90g-chat-actions"><a class="s90g-chat-primary" href="${WHATSAPP_CHAT_URL}" target="_blank" rel="noopener" data-track-whatsapp>Apri WhatsApp</a><a class="s90g-chat-secondary" href="https://sistema90g-console.sistema90g.workers.dev/richiesta" target="_blank" rel="noopener" data-track-portal>Invia un caso</a></div></section>`;
  document.body.appendChild(wrapper);
  const launcher=wrapper.querySelector('.s90g-chat-launcher');
  const popup=wrapper.querySelector('.s90g-chat-popup');
  const close=wrapper.querySelector('.s90g-chat-close');
  const setOpen=open=>{popup.hidden=!open;launcher.setAttribute('aria-expanded',String(open));wrapper.classList.toggle('is-open',open)};
  launcher.addEventListener('click',()=>setOpen(popup.hidden));
  close.addEventListener('click',()=>setOpen(false));
  document.addEventListener('keydown',event=>{if(event.key==='Escape')setOpen(false)});
}

document.addEventListener('DOMContentLoaded',()=>{
  loadAuditFix();
  addStructuredData();
  optimizeImages();
  addWhatsAppChat();
  const b=document.getElementById('cookie-banner'),c=localStorage.getItem(CONSENT_KEY);
  if(c==='accepted'){hideCookieBanner(b);loadAnalytics()}else if(c==='rejected'){hideCookieBanner(b);denyAnalytics()}else showCookieBanner(b);
  document.querySelectorAll('[data-cookie-choice]').forEach(x=>x.addEventListener('click',()=>{const ok=x.dataset.cookieChoice==='accept';saveConsent(ok?'accepted':'rejected');hideCookieBanner(b);ok?loadAnalytics():denyAnalytics()}));
  document.querySelectorAll('[data-cookie-settings]').forEach(x=>x.addEventListener('click',e=>{e.preventDefault();showCookieBanner(b)}));
  document.querySelectorAll('[data-track-whatsapp]').forEach(x=>x.addEventListener('click',()=>trackLead('whatsapp_chat_open',x)));
  document.querySelectorAll('[data-track-portal]').forEach(x=>x.addEventListener('click',()=>trackLead('public_portal_open',x)));
});