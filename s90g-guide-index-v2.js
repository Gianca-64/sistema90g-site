(() => {
  "use strict";

  const body = document.body;

  const input = document.querySelector(
    "#s90g-guide-search"
  );

  const status = document.querySelector(
    "#s90g-guide-search-status"
  );

  const groups = Array.from(
    document.querySelectorAll(
      ".s90g-guide-mode-index .s90g-guide-group"
    )
  );

  const links = Array.from(
    document.querySelectorAll(
      ".s90g-guide-mode-index .s90g-guide-links a"
    )
  );

  const chips = Array.from(
    document.querySelectorAll(
      "[data-guide-query]"
    )
  );

  if (
    !input ||
    !status ||
    groups.length !== 4 ||
    links.length !== 44
  ) {
    return;
  }

  const normalize = (value) =>
    value
      .toLocaleLowerCase("it")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .trim();

  groups.forEach((group) => {
    const groupLinks = Array.from(
      group.querySelectorAll(
        ".s90g-guide-links a"
      )
    );

    const visibleLimit = 6;

    if (groupLinks.length <= visibleLimit) {
      return;
    }

    groupLinks
      .slice(visibleLimit)
      .forEach((link) => {
        link.classList.add(
          "s90g-guide-index-collapsed"
        );
      });

    const button = document.createElement("button");

    button.type = "button";
    button.className = "s90g-guide-index-toggle";

    const hiddenCount =
      groupLinks.length - visibleLimit;

    button.textContent =
      `Mostra altre ${hiddenCount} guide ↓`;

    button.dataset.expanded = "false";

    button.addEventListener("click", () => {
      const expanded =
        button.dataset.expanded === "true";

      groupLinks
        .slice(visibleLimit)
        .forEach((link) => {
          link.classList.toggle(
            "s90g-guide-index-collapsed",
            expanded
          );
        });

      button.dataset.expanded =
        expanded ? "false" : "true";

      button.textContent =
        expanded
          ? `Mostra altre ${hiddenCount} guide ↓`
          : "Mostra meno ↑";
    });

    group.appendChild(button);
  });

  const applySearch = (rawValue) => {
    const query = normalize(rawValue);

    const terms = query
      .split(/\s+/)
      .filter(Boolean);

    const searching = terms.length > 0;

    body.classList.toggle(
      "s90g-guide-search-active",
      searching
    );

    let matches = 0;

    links.forEach((link) => {
      const text = normalize(
        link.textContent
      );

      const match =
        !searching ||
        terms.some((term) =>
          text.includes(term)
        );

      link.hidden = !match;

      if (match) {
        matches += 1;
      }
    });

    groups.forEach((group) => {
      const groupLinks = Array.from(
        group.querySelectorAll(
          ".s90g-guide-links a"
        )
      );

      const groupHasMatch =
        groupLinks.some(
          (link) => !link.hidden
        );

      group.hidden =
        searching && !groupHasMatch;
    });

    if (!searching) {
      status.textContent =
        "44 guide disponibili";
    } else if (matches === 1) {
      status.textContent =
        "1 guida trovata";
    } else {
      status.textContent =
        `${matches} guide trovate`;
    }
  };

  input.addEventListener(
    "input",
    () => applySearch(input.value)
  );

  chips.forEach((chip) => {
    chip.addEventListener(
      "click",
      () => {
        const query =
          chip.dataset.guideQuery || "";

        input.value = query;

        applySearch(query);

        input.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });

        window.setTimeout(
          () => {
            input.focus({
              preventScroll: true
            });
          },
          300
        );
      }
    );
  });

  applySearch("");
})();
