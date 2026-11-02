// Two real runs side by side. Both videos play the run at data-video-speed; the first one
// sets the clock, the second follows it. Each card counts its placements from data-placements
// (run seconds) and shows its lost items and result when its run ends (data-end).
(function () {
  var duel = document.querySelector(".ev-duel");
  if (!duel) return;
  var speed = parseFloat(duel.dataset.videoSpeed);
  var cards = Array.prototype.slice.call(duel.querySelectorAll(".ev-duel-card")).map(function (el) {
    return {
      el: el,
      video: el.querySelector("video"),
      placements: el.dataset.placements.split(",").map(parseFloat),
      end: parseFloat(el.dataset.end),
      lost: el.dataset.lost,
      placed: el.querySelector(".ev-duel-placed"),
      lostOut: el.querySelector(".ev-duel-lost"),
      clock: el.querySelector(".ev-duel-clock"),
      bar: Array.prototype.slice.call(el.querySelectorAll(".ev-duel-bar li")),
      result: el.querySelector(".ev-duel-result"),
      final: el.querySelector(".ev-duel-result").innerHTML
    };
  });
  var lead = cards[0].video;
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function mmss(s) {
    s = Math.max(0, Math.floor(s));
    return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
  }

  function render(t) {
    cards.forEach(function (c) {
      var runT = Math.min(t, c.end), n = 0;
      while (n < c.placements.length && c.placements[n] <= runT) n++;
      c.placed.textContent = n;
      c.bar.forEach(function (li, k) { li.className = k < n ? "is-placed" : ""; });
      c.clock.textContent = mmss(runT);
      var over = t >= c.end;
      c.lostOut.textContent = over ? c.lost : "–";
      if (over !== c.over) {
        c.over = over;
        c.result.innerHTML = over ? c.final : "Running…";
        c.el.classList.toggle("is-running", !over);
      }
    });
  }

  function load() {
    cards.forEach(function (c) {
      if (!c.video.src) { c.video.src = c.video.dataset.src; c.video.load(); }
    });
  }

  if (still) {
    load();
    cards.forEach(function (c) { c.video.controls = true; });
    render(Infinity);
    return;
  }

  var visible = false;
  function playAll() {
    if (!visible || document.hidden) return;
    load();
    cards.forEach(function (c) {
      var p = c.video.play();
      if (p && p.catch) p.catch(function () {});
    });
  }
  function pauseAll() { cards.forEach(function (c) { c.video.pause(); }); }

  new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) load();
  }, {rootMargin: "600px"}).observe(duel);
  new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting;
    if (visible) playAll(); else pauseAll();
  }, {threshold: 0.3}).observe(duel.querySelector(".ev-duel-row"));
  document.addEventListener("visibilitychange", function () { if (document.hidden) pauseAll(); else playAll(); });

  // Both files have the same length, so one restart keeps them in step. The final state
  // stays on screen for a few seconds first.
  lead.addEventListener("ended", function () {
    setTimeout(function () {
      cards.forEach(function (c) { c.video.currentTime = 0; });
      playAll();
    }, 3000);
  });

  function tick() {
    var t = lead.currentTime;
    for (var i = 1; i < cards.length; i++) {
      var v = cards[i].video;
      if (v.readyState >= 2 && Math.abs(v.currentTime - t) > 0.25) v.currentTime = t;
    }
    render(t * speed);
    requestAnimationFrame(tick);
  }
  render(0);
  requestAnimationFrame(tick);
})();
