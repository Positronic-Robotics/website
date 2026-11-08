// The "Keep in touch" form in the footer: post the address to phail.ai, which keeps the list, and say what happened.
// The browser's own email check runs before the submit event; phail.ai's stricter one answers 400.
(function () {
  var form = document.getElementById("updates-form");
  if (!form) return;

  var status = form.querySelector(".updates-status");
  var button = form.querySelector("button[type=submit]");

  function say(text, ok) {
    status.textContent = text;
    status.classList.toggle("is-error", ok === false);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    button.disabled = true;
    say("Sending…");
    fetch(form.action, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ email: form.elements.email.value.trim(), company: form.elements.company.value }),
    })
      .then(function (response) {
        if (response.status === 400) {
          say("That address does not look right.", false);
          return;
        }
        if (!response.ok) throw new Error(response.status);
        form.reset();
        say("Thanks, you are on the list.");
      })
      .catch(function () {
        say("That did not go through. Write to hi@positronic.ro.", false);
      })
      .finally(function () {
        button.disabled = false;
      });
  });
})();
