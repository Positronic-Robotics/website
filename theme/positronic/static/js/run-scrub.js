// One real run, scrubbed by scroll. Each text step names a run second (data-t); the
// reader's position between two steps sets the run clock, the video frame and the labels.
// The video file is the run at 1/speed: run seconds = video seconds x data-video-speed.
(function () {
  var run = document.querySelector(".ev-run");
  if (!run) return;
  var video = run.querySelector("video");
  var steps = Array.prototype.slice.call(run.querySelectorAll(".ev-step"));
  var total = parseFloat(run.dataset.runSeconds);
  var speed = parseFloat(run.dataset.videoSpeed);
  var items = parseInt(run.dataset.items, 10);
  var placements = run.dataset.placements.split(",").map(parseFloat);
  var clock = run.querySelector(".ev-run-clock b");
  var nowText = run.querySelector(".ev-now-text");
  var list = run.querySelector(".ev-run-items");
  var focusable = Array.prototype.slice.call(run.querySelectorAll(".ev-run-stage [data-focus]"));
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var cells = [];
  for (var i = 0; i < items; i++) {
    var li = document.createElement("li");
    li.innerHTML = "<span>Item " + (i + 1) + "</span><b>–</b>";
    list.appendChild(li);
    cells.push(li);
  }

  function mmss(s) {
    s = Math.max(0, Math.floor(s));
    return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
  }

  function itemSeconds(k) { return placements[k] - (k ? placements[k - 1] : 0); }

  function render(t, focus) {
    clock.textContent = mmss(t);
    var placed = 0;
    while (placed < placements.length && placements[placed] <= t) placed++;
    cells.forEach(function (li, k) {
      var done = k < placed, missed = !done && t >= total;
      li.className = done ? "is-placed" : missed ? "is-missed" : k === placed ? "is-now" : "";
      li.lastChild.textContent = done ? itemSeconds(k).toFixed(1) + " s" : missed ? "not placed" : "–";
    });
    var since = t - (placed ? placements[placed - 1] : 0);
    nowText.textContent = t >= total ? "Time limit reached"
      : placed >= items ? "All items placed"
      : "Item " + (placed + 1) + " · " + since.toFixed(1) + " s";
    run.classList.toggle("is-over", t >= total);
    focusable.forEach(function (el) { el.classList.toggle("is-focus", el.dataset.focus === focus); });
  }

  if (still) {
    video.src = video.dataset.src;
    video.controls = true;
    render(total, "result");
    return;
  }

  var loaded = false;
  function load() {
    if (loaded) return;
    loaded = true;
    video.preload = "auto";
    video.src = video.dataset.src;
    video.load();
    // iOS paints a seeked frame only after the element has played once.
    var p = video.play();
    if (p && p.then) p.then(function () { video.pause(); }).catch(function () {});
  }
  new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) load();
  }, {rootMargin: "800px"}).observe(run);

  var queued = false;
  function update() {
    queued = false;
    var anchor = window.innerHeight * 0.5;
    var t = 0, active = -1;
    for (var i = 0; i < steps.length; i++) {
      var r = steps[i].getBoundingClientRect();
      if (r.top > anchor) break;
      active = i;
      var t0 = parseFloat(steps[i].dataset.t);
      var t1 = i + 1 < steps.length ? parseFloat(steps[i + 1].dataset.t) : t0;
      t = t0 + Math.min(1, (anchor - r.top) / Math.max(1, r.height)) * (t1 - t0);
    }
    t = Math.min(total, t);
    steps.forEach(function (s, k) { s.classList.toggle("is-on", k === active); });
    render(t, active >= 0 ? steps[active].dataset.focus : "task");
    if (loaded && video.readyState >= 1) {
      var target = Math.min(video.duration - 0.05, t / speed);
      if (Math.abs(video.currentTime - target) > 0.03) video.currentTime = target;
    }
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(update); } }
  window.addEventListener("scroll", queue, {passive: true});
  window.addEventListener("resize", queue);
  video.addEventListener("loadedmetadata", queue);
  update();
})();
