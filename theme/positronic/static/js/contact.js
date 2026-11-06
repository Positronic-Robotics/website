// Homepage contact form: post it without leaving the page, and say what happened.
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = form.querySelector(".contact-status");
  var button = form.querySelector("button[type=submit]");
  var heardFrom = form.elements.heard_from;
  var heardDetail = form.elements.heard_from_detail;

  heardFrom.addEventListener("change", function () {
    heardDetail.hidden = heardFrom.value !== "other";
  });

  function say(text, ok) {
    status.textContent = text;
    status.classList.toggle("is-error", ok === false);
  }

  // Both trackers autocapture the submit EVENT, which counts an attempt that the
  // API can still refuse. Name the ones that reached us.
  function lead(method, heard) {
    var props = { method: method };
    if (heard) props.heard_from = heard;
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
    var heard = heardFrom.value;
    var detail = heard === "other" ? heardDetail.value.trim() : "";
    button.disabled = true;
    say("Sending…");

    // Only the browser knows the page before this one.
    fetch("/api/contact", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        email: email,
        note: form.elements.note.value.trim(),
        company: form.elements.company.value,
        heard_from: heard,
        heard_from_detail: detail,
        referrer: document.referrer,
      }),
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
