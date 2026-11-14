// The contact form posts without leaving the page and says what happened; a booking link counts as a lead.
(function () {
  // phail.ai stores the lead; the visitor's browser posts there, so its hourly limit counts the visitor.
  var LEADS_URL = "https://phail.ai/api/interest";
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

  document.querySelectorAll("a[href*='calendar.notion.so']").forEach(function (booking) {
    booking.addEventListener("click", function () {
      lead("book_a_call");
    });
  });

  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = form.querySelector(".contact-status");
  var button = form.querySelector("button[type=submit]");
  var heardBoxes = form.querySelectorAll("input[name=heard_from]");
  var heardOther = form.querySelector("input[name=heard_from][value=other]");
  var heardDetail = form.elements.heard_from_detail;

  heardOther.addEventListener("change", function () {
    heardDetail.hidden = !heardOther.checked;
  });

  // The ticked answers, in the order the form lists them.
  function heardFrom() {
    return Array.prototype.filter
      .call(heardBoxes, function (box) {
        return box.checked;
      })
      .map(function (box) {
        return box.value;
      });
  }

  function say(text, ok) {
    status.textContent = text;
    status.classList.toggle("is-error", ok === false);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var email = form.elements.email.value.trim();
    if (email.indexOf("@") < 0 || email.indexOf(".") < 0) {
      say("That address does not look right.", false);
      return;
    }
    var heard = heardFrom();
    var detail = heardOther.checked ? heardDetail.value.trim() : "";
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
