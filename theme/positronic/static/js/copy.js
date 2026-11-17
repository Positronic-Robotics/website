// A Copy button puts the text of the element that its data-copy names on the clipboard.
(function () {
  document.querySelectorAll("[data-copy]").forEach(function (button) {
    var source = document.getElementById(button.getAttribute("data-copy"));
    if (!source || !navigator.clipboard) return;
    button.addEventListener("click", function () {
      navigator.clipboard.writeText(source.textContent).then(function () {
        button.textContent = "Copied";
        setTimeout(function () { button.textContent = "Copy"; }, 2000);
      });
    });
  });
})();
