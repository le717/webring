/*! webring v{{ config.API_VERSION }} - https://github.com/le717/webring */
(async function() {
  "use strict";

  const qWebringEmbedArea = document.querySelector("#webring-embed-area");
  const markup = ["<dl>"];
  const webring = {{ all_links }};

  // If there's no embed area or no weblinks, we can't do anything
  if (qWebringEmbedArea === null || webring.length === 0) {
    return;
  }

  // Generate the markup for each item in the webring
  webring.forEach((item) => {
    markup.push(
      `<dt>
        <a id="webring-${item.id}" href="${item.url}">${item.title}</a>
      </dt>
      <dd>${item.description}</dd>`
    );
  });
  markup.push("</dl>");

  // Add the completed markup into the page
  qWebringEmbedArea.insertAdjacentHTML("beforeend", markup.join(""));
}());
