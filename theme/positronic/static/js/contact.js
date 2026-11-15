// Homepage contact form: post it without leaving the page, and say what happened.
(function () {
  // phail.ai stores the lead; the visitor's browser posts there, so its hourly limit counts the visitor.
  var LEADS_URL = "https://phail.ai/api/interest";
  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = form.querySelector(".contact-status");
  var button = form.querySelector("button[type=submit]");
  var heardSelect = form.elements.heard_from;
  var heardDetail = form.elements.heard_from_detail;

  heardSelect.addEventListener("change", function () {
    heardDetail.hidden = heardSelect.value !== "other";
  });

  function say(text, ok) {
    status.textContent = text;
    status.classList.toggle("is-error", ok === false);
  }

  // base.html loads attribution.js ahead of every page script.
  var arrival = window.positronicArrival;

  // Both trackers autocapture the submit EVENT, which counts an attempt that the
  // API can still refuse. Name the ones that reached us.
  function lead(method, heard) {
    var props = arrival.sources();
    props.method = method;
    if (heard && heard.length) props.heard_from = heard.join(",");
    if (window.plausible) window.plausible("Lead", { props: props });
    if (window.gtag) window.gtag("event", "generate_lead", props);
  }

  var booking = document.querySelector(".contact-alt a[href*='calendar.notion.so']");
  if (booking) {
    booking.addEventListener("click", function () {
      lead("book_a_call");
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var email = form.elements.email.value.trim();
    if (email.indexOf("@") < 0 || email.indexOf(".") < 0) {
      say("That address does not look right.", false);
      return;
    }
    if (!heardSelect.value) {
      say("Pick where you heard about us.", false);
      heardSelect.focus();
      return;
    }
    // phail.ai takes a list of channels.
    var heard = [heardSelect.value];
    var detail = heardSelect.value === "other" ? heardDetail.value.trim() : "";
    button.disabled = true;
    say("Sending…");

    var body = arrival.fields();
    body.email = email;
    body.note = form.elements.note.value.trim();
    body.company = form.elements.company.value;
    body.heard_from = heard;
    body.heard_from_detail = detail;
    body.source = "positronic-home";
    body.page = window.location.pathname;
    fetch(LEADS_URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    })
      .then(function (response) {
        if (!response.ok) throw new Error(response.status);
        form.reset();
        heardDetail.hidden = true;
        say("Got it. We answer within a day.");
        lead("contact_form", heard);
      })
      .catch(function () {
        say("That did not go through. Write to hi@positronic.ro.", false);
      })
      .finally(function () {
        button.disabled = false;
      });
  });
})();
