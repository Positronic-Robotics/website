// The Pricing page slider: the cost of one episode of the chosen length, for each environment.
(function () {
  var slider = document.getElementById("pf-length");
  if (!slider) return;

  function length(seconds) {
    var min = Math.floor(seconds / 60), sec = seconds % 60;
    if (!min) return sec + " s";
    return sec ? min + " min " + sec + " s" : min + " min";
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
