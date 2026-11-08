// The "Keep in touch" form in the footer: post the address to phail.ai, which keeps the one list of both sites,
// without leaving the page, and say what happened.
(function () {
  var form = document.getElementById("updates-form");
  if (!form) return;

  // The browser checks the address only when this script does not run.
  form.noValidate = true;
  var status = form.querySelector(".updates-status");
  var button = form.querySelector("button[type=submit]");

  function say(text, ok) {
    status.textContent = text;
    status.classList.toggle("is-error", ok === false);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var email = form.elements.email.value.trim();
    if (email.indexOf("@") < 1 || email.indexOf(".") < 0) {
      say("That address does not look right.", false);
      return;
    }
    button.disabled = true;
    say("Sending…");
    fetch(form.action, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ email: email, company: form.elements.company.value }),
    })
      .then(function (response) {
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
