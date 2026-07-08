(function () {
  const endpoint = "https://sistema90g-public-requests.sistema90g.workers.dev/api/public-requests";
  const form = document.getElementById("public-request-form");
  const status = document.getElementById("public-request-status");
  const fileInput = document.getElementById("request-files");
  const fileSummary = document.getElementById("request-files-summary");

  if (!form || !status) return;

  if (fileInput && fileSummary) {
    fileInput.addEventListener("change", function () {
      const files = Array.from(fileInput.files || []);
      if (!files.length) {
        fileSummary.textContent = "Nessun file selezionato";
        return;
      }

      fileSummary.textContent = files.length === 1
        ? files[0].name
        : files.length + " file selezionati";
    });
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const submitButton = form.querySelector("button[type='submit']");
    const formData = new FormData(form);

    status.textContent = "Invio richiesta in corso...";
    status.className = "s90g-form-status";
    if (submitButton) submitButton.disabled = true;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData
      });

      const result = await response.json().catch(function () {
        return {};
      });

      if (!response.ok || !result.ok) {
        throw new Error(result.error || "request_failed");
      }

      form.reset();
      if (fileSummary) fileSummary.textContent = "Nessun file selezionato";
      status.textContent = "Richiesta ricevuta. Ti risponderemo dopo una prima verifica del materiale.";
      status.className = "s90g-form-status success";
    } catch (error) {
      status.textContent = "Non siamo riusciti a inviare la richiesta. Puoi scrivere a sistema90g@icloud.com e riprovare piu tardi.";
      status.className = "s90g-form-status error";
    } finally {
      if (submitButton) submitButton.disabled = false;
    }
  });
})();
