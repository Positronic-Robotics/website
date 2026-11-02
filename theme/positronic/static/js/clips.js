// Lab clips: each loads when it nears the screen, plays while on screen and pauses
// off it. A reader who asks for reduced motion gets the poster and the controls.
(function () {
  var clips = document.querySelectorAll(".ev-clip video");
  if (!clips.length) return;
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function load(video) {
    if (video.dataset.src && !video.src) {
      video.src = video.dataset.src;
      video.load();
    }
  }

  function play(video) {
    if (still || !video.paused) return;
    load(video);
    var started = video.play();
    if (started && started.catch) started.catch(function () {});
  }

  if (still) {
    clips.forEach(function (video) { video.controls = true; video.removeAttribute("autoplay"); load(video); });
    return;
  }

  if (!window.IntersectionObserver) {
    clips.forEach(play);
    return;
  }

  var near = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) load(e.target); });
  }, {rootMargin: "600px"});

  var onScreen = [];
  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var i = onScreen.indexOf(e.target);
      if (e.isIntersecting) { if (i < 0) onScreen.push(e.target); play(e.target); }
      else { if (i >= 0) onScreen.splice(i, 1); e.target.pause(); }
    });
  }, {threshold: 0.15});

  clips.forEach(function (video) { near.observe(video); seen.observe(video); });
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) clips.forEach(function (v) { v.pause(); });
    else onScreen.forEach(play);
  });
})();
