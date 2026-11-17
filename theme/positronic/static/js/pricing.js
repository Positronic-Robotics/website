// The Pricing page slider: per episode + per minute × length = the cost of one episode, for each environment.
(function () {
  var slider = document.getElementById("pf-length");
  if (!slider) return;

  // Minutes with one decimal, so every length has the same shape: 0.5 min, 2.0 min, 10.0 min.
  function length(seconds) {
    return (seconds / 60).toFixed(1) + " min";
  }

  function money(dollars) {
    return "$" + (dollars >= 1 ? dollars.toFixed(2).replace(/\.00$/, "") : Number(dollars.toPrecision(2)));
  }

  function update() {
    var seconds = Number(slider.value);
    document.querySelectorAll(".pf-length-value").forEach(function (el) { el.textContent = length(seconds); });
    document.querySelectorAll(".pf-rates tr[data-episode]").forEach(function (row) {
      var cost = Number(row.dataset.episode) + Number(row.dataset.minute) * seconds / 60;
      row.querySelector(".pf-total").textContent = money(cost);
    });
  }

  slider.addEventListener("input", update);
  update();
})();
