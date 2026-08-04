(function(){
  "use strict";
  const form=document.querySelector("[data-s90g-professional-interest-form]");
  if(!form)return;
  const feedback=form.querySelector("[data-s90g-interest-feedback]");
  const submit=form.querySelector("button[type=submit]");
  const active=form.getAttribute("data-active")==="true";
  const endpoint=active?String(form.getAttribute("data-endpoint")||"").trim():"";
  let startedAt=Date.now();
  let attemptKey=null;
  const params=new URLSearchParams(location.search);
  const sourceContent=params.get("source_content")||params.get("utm_content")||"pagina-professionisti";

  function uuid(){
    if(window.crypto&&typeof window.crypto.randomUUID==="function")return window.crypto.randomUUID();
    return "s90g-"+Date.now().toString(36)+"-"+Math.random().toString(36).slice(2)+Math.random().toString(36).slice(2);
  }
  function show(message,kind){
    if(!feedback)return;
    feedback.textContent=message;
    feedback.dataset.visible="true";
    feedback.dataset.kind=kind||"success";
    feedback.focus({preventScroll:true});
  }
  function analyticsAllowed(){
    try{return window.localStorage.getItem("s90g_cookie_consent")==="accepted";}catch{return false;}
  }
  function track(name,extra){
    if(!analyticsAllowed()||typeof window.gtag!=="function")return;
    window.gtag("event",name,Object.assign({event_category:"professional_interest",source_content:sourceContent},extra||{}));
  }
  function clearAttemptKey(){
    if(!submit.disabled)attemptKey=null;
  }
  function applyInactiveState(){
    const robots=document.querySelector('meta[name="robots"]');
    if(robots)robots.setAttribute("content","noindex,nofollow,noarchive");
    form.setAttribute("aria-disabled","true");
    submit.disabled=true;
    submit.textContent="Modulo in preparazione";
    show("Il modulo non è ancora attivo. La pagina resta disponibile soltanto per il collaudo prima della pubblicazione.","info");
  }

  if(!active||!endpoint){
    applyInactiveState();
    return;
  }

  form.addEventListener("input",clearAttemptKey);
  form.addEventListener("change",clearAttemptKey);
  track("professional_interest_form_view");

  form.addEventListener("submit",async function(event){
    event.preventDefault();
    if(!form.checkValidity()){
      form.reportValidity();
      show("Completa i campi obbligatori e verifica i dati inseriti.","error");
      return;
    }

    const data=new FormData(form);
    const email=String(data.get("email")||"").trim();
    const consentReply=data.get("consent_reply")==="on";
    const consentUpdates=data.get("consent_updates")==="on";
    if(email&&!consentReply&&!consentUpdates){show("Se indichi l’email, seleziona almeno una finalità autorizzata.","error");return;}
    if(!email&&consentReply){show("Indica un’email per ricevere la risposta scritta.","error");return;}
    if(!email&&consentUpdates){show("Indica un’email per ricevere eventuali aggiornamenti.","error");return;}

    attemptKey=attemptKey||uuid();
    const payload={
      professional_role:String(data.get("professional_role")||""),
      recognized_situation:String(data.get("recognized_situation")||""),
      desired_action:String(data.get("desired_action")||""),
      message:String(data.get("message")||""),
      contact_name:String(data.get("contact_name")||""),
      organization:String(data.get("organization")||""),
      email,
      consent_reply:consentReply,
      consent_updates:consentUpdates,
      privacy_accepted:data.get("privacy_accepted")==="on",
      website:String(data.get("website")||""),
      form_started_at:startedAt,
      idempotency_key:attemptKey,
      source_page:location.pathname,
      source_content:sourceContent,
      utm_source:params.get("utm_source")||"",
      utm_medium:params.get("utm_medium")||"",
      utm_campaign:params.get("utm_campaign")||"",
      utm_content:params.get("utm_content")||""
    };
    submit.disabled=true;
    submit.textContent="Invio in corso…";
    try{
      const response=await fetch(endpoint,{method:"POST",headers:{"Content-Type":"application/json","Idempotency-Key":attemptKey},body:JSON.stringify(payload),mode:"cors",credentials:"omit"});
      const body=await response.json().catch(function(){return{};});
      if(!response.ok||body.ok!==true)throw new Error("submission_failed");
      show("La manifestazione di interesse è stata registrata.","success");
      track("professional_interest_submitted",{professional_role:payload.professional_role,desired_action:payload.desired_action,reply_expected:Boolean(body.replyExpected)});
      form.reset();
      attemptKey=null;
      startedAt=Date.now();
    }catch{
      show("Invio non riuscito. Riprova più tardi oppure usa i contatti indicati nel sito.","error");
      track("professional_interest_error");
    }finally{
      submit.disabled=false;
      submit.textContent="Invia la manifestazione di interesse";
    }
  });
})();
