const GA_ID='G-G5D6FNDR00';
const CONSENT_KEY='s90g_cookie_consent';
const WHATSAPP_CHAT_URL='https://wa.me/393275478485?text=Ciao%2C%20ho%20una%20domanda%20rapida%20su%20Sistema%2090G.';

window.dataLayer=window.dataLayer||[];
window.gtag=window.gtag||function(){window.dataLayer.push(arguments)};
window.gtag('consent','default',{
  analytics_storage:'denied',
  ad_storage:'denied',
  ad_user_data:'denied',
  ad_personalization:'denied'
});

function loadNavigationConversion(){
  if(document.querySelector('script[data-s90g-navigation-conversion]'))return;
  const script=document.createElement('script');
  script.src='/navigation-conversion.js?v=20260815a';
  script.defer=true;
  script.dataset.s90gNavigationConversion='true';
  document.head.appendChild(script);
}
function loadAuditFix(){
  if(document.querySelector('link[data-s90g-audit-fix]'))return;
  const link=document.createElement('link');
  link.rel='stylesheet';
  link.href='sistema90g-audit-fix-20260707.css?v=20260708am';
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
  if(document.querySelector('script[type="application/ld+json"]'))return;
  const canonical=document.querySelector('link[rel="canonical"]')?.href||location.href;
  const title=document.querySelector('h1')?.textContent.trim()||document.title;
  const description=document.querySelector('meta[name="description"]')?.content||'';
  const image=document.querySelector('main img')?.src||'https://sistema90g.it/images/01_HOME_HERO.jpg';
  const graph=[
    {'@type':'Organization','@id':'https://sistema90g.it/#organization','name':'Sistema 90G','url':'https://sistema90g.it/','logo':{'@type':'ImageObject','url':'https://sistema90g.it/images/favicon-512.png'},'founder':{'@id':'https://sistema90g.it/chi-e-sistema90g.html#person'},'description':'Servizio indipendente dedicato all’analisi preventiva, alla verifica e allo sviluppo di progetti cucina.'},
    {'@type':'Person','@id':'https://sistema90g.it/chi-e-sistema90g.html#person','name':'Gian Carlo Primo','url':'https://sistema90g.it/chi-e-sistema90g.html','jobTitle':'Tecnico indipendente per analisi e progettazione cucina','worksFor':{'@id':'https://sistema90g.it/#organization'}},
    {'@type':'WebSite','@id':'https://sistema90g.it/#website','url':'https://sistema90g.it/','name':'Sistema 90G','publisher':{'@id':'https://sistema90g.it/#organization'},'inLanguage':'it-IT'},
    {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'isPartOf':{'@id':'https://sistema90g.it/#website'},'about':{'@id':'https://sistema90g.it/#organization'},'primaryImageOfPage':{'@type':'ImageObject','url':image},'inLanguage':'it-IT'}
  ];
  if((location.pathname.includes('caso-')||location.pathname.includes('/approfondimenti/'))&&!hasStaticArticleSchema()){
    graph.push({'@type':'Article','headline':title,'description':description,'image':[image],'mainEntityOfPage':canonical,'author':{'@id':'https://sistema90g.it/chi-e-sistema90g.html#person'},'publisher':{'@id':'https://sistema90g.it/#organization'},'inLanguage':'it-IT'});
  }
  const script=document.createElement('script');
  script.type='application/ld+json';
  script.dataset.s90gStructuredData='true';
  script.textContent=JSON.stringify({'@context':'https://schema.org','@graph':graph});
  document.head.appendChild(script);
}
function archiveFallback(img){
  const card=img.closest('.s90g-archive-card');
  const label=card?.querySelector('.s90g-archive-copy span')?.textContent.toLowerCase()||'';
  if(label.includes('cucina')||label.includes('preventivo'))return 'images/19_CASI_CUCINA.jpg?v=20260715a';
  return 'images/19_CASI_CUCINA.jpg?v=20260715a';
}
function optimizeImages(){
  const images=[...document.querySelectorAll('img')];
  images.forEach((img,index)=>{
    img.decoding='async';
    const isArchive=Boolean(img.closest('.s90g-archive-card'));
    const applyFallback=()=>{
      if(img.dataset.s90gFallbackApplied)return;
      img.dataset.s90gFallbackApplied='true';
      img.src=isArchive?archiveFallback(img):'images/19_CASI_CUCINA.jpg?v=20260715a';
    };
    img.addEventListener('error',applyFallback,{once:true});
    if(isArchive){
      img.loading='lazy';
      img.fetchPriority='low';
      requestAnimationFrame(()=>{
        if(img.complete&&img.naturalWidth===0)applyFallback();
      });
    }else if(index===0||img.closest('.s90g-hero-media,.s90g-inner-media,.premium-hero')){
      img.loading='eager';
      img.fetchPriority='high';
    }else{
      img.loading='lazy';
    }
  });
}
function loadAnalytics(){
  window.gtag('consent','update',{
    analytics_storage:'granted',
    ad_storage:'denied',
    ad_user_data:'denied',
    ad_personalization:'denied'
  });
  if(window.s90gAnalyticsLoaded)return;
  window.s90gAnalyticsLoaded=true;
  const script=document.createElement('script');
  script.async=true;
  script.src=`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_ID)}`;
  script.dataset.s90gAnalytics='true';
  document.head.appendChild(script);
  window.gtag('js',new Date());
  window.gtag('config',GA_ID,{send_page_view:true});
}
function denyAnalytics(){
  window.gtag('consent','update',{
    analytics_storage:'denied',
    ad_storage:'denied',
    ad_user_data:'denied',
    ad_personalization:'denied'
  });
}
function hideCookieBanner(b){if(b)b.setAttribute('hidden','')}
function showCookieBanner(b){if(b)b.removeAttribute('hidden')}
function saveConsent(c){window.localStorage.setItem(CONSENT_KEY,c)}
function s90gPageSlug(){
  const name=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'');
  return name==='index'?'home':name;
}
function s90gInferContentType(){
  const slug=s90gPageSlug();
  if(slug.startsWith('caso-'))return 'case';
  if(slug.startsWith('casi-'))return 'case-category';
  if(location.pathname.includes('/approfondimenti/')||slug==='innovazioni')return 'article';
  if(['professionisti','professionisti-progetto-cucina','agenzie-immobiliari-cucina','rivenditori-cucine'].includes(slug))return 'professional';
  if(['progetto-cucina-sistema90g','seconda-opinione-cucina','scelta-finiture-cucina','restyling-cucina-esistente','acquisto-assistito-cucina','servizi','controllo-progetto-cucina'].includes(slug))return 'service';
  if(slug==='esempio-progetto-cucina-90g'||slug==='esempio-fascicolo-cucina')return 'proof';
  return 'page';
}

function s90gPrepareGuidedPathLinks(){
  const campaignKeys=['utm_source','utm_medium','utm_campaign','utm_content','utm_term'];
  const current=new URL(location.href);
  document.querySelectorAll('a[data-start-path]').forEach((link,index)=>{
    const target=new URL(link.getAttribute('href')||'analisi-preventiva.html#richiedi',location.href);
    target.searchParams.set('source_page',link.dataset.sourcePage||s90gPageSlug());
    target.searchParams.set('content_type',link.dataset.contentType||s90gInferContentType());
    target.searchParams.set('cta_position',link.dataset.ctaPosition||((link.closest('header'))?'header':(link.closest('footer')?'footer':`inline-${index+1}`)));
    if(link.dataset.service)target.searchParams.set('service_hint',link.dataset.service);
    if(link.dataset.roleHint)target.searchParams.set('role_hint',link.dataset.roleHint);
    if(link.dataset.caseId)target.searchParams.set('case_id',link.dataset.caseId);
    campaignKeys.forEach(key=>{if(current.searchParams.get(key))target.searchParams.set(key,current.searchParams.get(key));});
    link.href=target.toString();
  });
}
function s90gPreparePortalLinks(){
  document.querySelectorAll('a[data-final-portal],a[href^="https://portale.sistema90g.it/"]').forEach(link=>{
    link.dataset.trackPortal='true';
    link.dataset.portalEnabled='true';
  });
}
function trackLead(name,link){
  if(window.localStorage.getItem(CONSENT_KEY)!=='accepted'||typeof window.gtag!=='function')return;
  const url=new URL(link.href);
  window.gtag('event',name,{event_category:'lead',link_url:link.href,link_text:link.textContent.trim(),source_page:url.searchParams.get('source_page')||s90gPageSlug(),content_type:url.searchParams.get('content_type')||s90gInferContentType(),service:url.searchParams.get('service')||'',cta_position:url.searchParams.get('cta_position')||'',case_id:url.searchParams.get('case_id')||'',transport_type:'beacon'});
}
function addWhatsAppChat(){
  if(document.querySelector('.s90g-chat-launcher'))return;
  const wrapper=document.createElement('div');
  wrapper.className='s90g-chat-widget';
  wrapper.innerHTML=`<button class="s90g-chat-launcher" type="button" aria-expanded="false" aria-controls="s90g-chat-popup"><span aria-hidden="true">💬</span><span>Chat</span></button><section class="s90g-chat-popup" id="s90g-chat-popup" hidden aria-label="Chat Sistema 90G"><button class="s90g-chat-close" type="button" aria-label="Chiudi la chat">×</button><p class="s90g-chat-kicker">Domande rapide</p><h2>Come posso aiutarti?</h2><p>Per una domanda veloce puoi aprire WhatsApp. Se vuoi sottoporre foto, planimetrie o preventivi, invia gratuitamente il caso: solo se serve un lavoro professionale ti verranno indicati contenuti e prezzo prima di procedere.</p><div class="s90g-chat-actions"><a class="s90g-chat-primary" href="${WHATSAPP_CHAT_URL}" target="_blank" rel="noopener" data-track-whatsapp>Apri WhatsApp</a><a class="s90g-chat-secondary" href="analisi-preventiva.html#richiedi" data-start-path data-content-type="chat" data-cta-position="chat" data-service="">Sottoponi il caso</a></div></section>`;
  document.body.appendChild(wrapper);
  const cookieBanner=document.getElementById('cookie-banner');
  const syncChatVisibility=()=>{const bannerIsVisible=cookieBanner&&!cookieBanner.hidden;wrapper.style.display=bannerIsVisible?'none':'';};
  if(cookieBanner)new MutationObserver(syncChatVisibility).observe(cookieBanner,{attributes:true,attributeFilter:['hidden']});
  syncChatVisibility();
  const launcher=wrapper.querySelector('.s90g-chat-launcher');
  const popup=wrapper.querySelector('.s90g-chat-popup');
  const close=wrapper.querySelector('.s90g-chat-close');
  const setOpen=open=>{popup.hidden=!open;launcher.setAttribute('aria-expanded',String(open));wrapper.classList.toggle('is-open',open)};
  launcher.addEventListener('click',()=>setOpen(popup.hidden));
  close.addEventListener('click',()=>setOpen(false));
  document.addEventListener('keydown',event=>{if(event.key==='Escape')setOpen(false)});
}
function s90gIntegrateAiTransparencyPage(){
  const href='/metodo-sistema90g.html';
  const isPage=location.pathname.endsWith(href);
  const nav=document.querySelector('.s90g-nav');
  if(nav){
    let link=nav.querySelector('a[data-nav-key="method"],a[href$="/metodo-sistema90g.html"],a[href$="metodo-sistema90g.html"]');
    if(!link){link=document.createElement('a');link.href=href;link.dataset.navKey='method';nav.appendChild(link);}
    link.textContent='Metodo e AI';
    if(isPage){nav.querySelectorAll('a[aria-current="page"]').forEach(item=>item.removeAttribute('aria-current'));link.setAttribute('aria-current','page');}
  }
  document.querySelectorAll('.s90g-footer-links').forEach(footerLinks=>{
    let link=footerLinks.querySelector('a[href$="/metodo-sistema90g.html"],a[href$="metodo-sistema90g.html"]');
    if(!link){link=document.createElement('a');link.href=href;const ip=footerLinks.querySelector('a[href$="/proprieta-intellettuale.html"],a[href$="proprieta-intellettuale.html"]');if(ip)ip.before(link);else footerLinks.appendChild(link);}
    link.textContent='Metodo e AI';
  });
}
document.addEventListener('s90g:navigation-ready',s90gIntegrateAiTransparencyPage);

document.addEventListener('DOMContentLoaded',()=>{
  loadNavigationConversion();
  s90gIntegrateAiTransparencyPage();
  loadAuditFix();
  addStructuredData();
  optimizeImages();
  addWhatsAppChat();
  s90gPrepareGuidedPathLinks();
  s90gPreparePortalLinks();
  const b=document.getElementById('cookie-banner'),c=localStorage.getItem(CONSENT_KEY);
  if(c==='accepted'){hideCookieBanner(b);loadAnalytics()}else if(c==='rejected'){hideCookieBanner(b);denyAnalytics()}else showCookieBanner(b);
  document.querySelectorAll('[data-cookie-choice]').forEach(x=>x.addEventListener('click',()=>{const ok=x.dataset.cookieChoice==='accept';saveConsent(ok?'accepted':'rejected');hideCookieBanner(b);ok?loadAnalytics():denyAnalytics()}));
  document.querySelectorAll('[data-cookie-settings]').forEach(x=>x.addEventListener('click',e=>{e.preventDefault();showCookieBanner(b)}));
  document.querySelectorAll('[data-track-whatsapp]').forEach(x=>x.addEventListener('click',()=>trackLead('whatsapp_chat_open',x)));
  document.querySelectorAll('[data-start-path]').forEach(x=>x.addEventListener('click',()=>trackLead('guided_path_open',x)));
  document.querySelectorAll('[data-track-portal]').forEach(x=>x.addEventListener('click',()=>{if(x.dataset.portalEnabled==='true')trackLead('public_portal_open',x)}));
  document.addEventListener('s90g:path-result',event=>{if(localStorage.getItem(CONSENT_KEY)==='accepted'&&typeof window.gtag==='function')window.gtag('event','guided_path_result',{event_category:'lead',requester_role:event.detail?.role||'',service:event.detail?.service||'',units:event.detail?.units||'',transport_type:'beacon'});});
});
