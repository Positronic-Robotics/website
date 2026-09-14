// Keep the run video playing. The autoplay attribute starts it, and a browser is
// free to refuse or to stop it again: Chrome pauses a muted autoplay whose element
// it judges off screen, and a returning tab resumes suspended. Ask again on each of
// those, and swallow the rejection a refusal returns.
(function () {
  var video = document.querySelector(".reel video");
  if (!video) return;

  function play() {
    if (!video.paused) return;
    var started = video.play();
    if (started && started.catch) started.catch(function () {});
  }

  play();
  document.addEventListener("visibilitychange", play);
  window.addEventListener("pageshow", play);
  video.addEventListener("canplay", play);

  if (window.IntersectionObserver) {
    new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) play();
    }, {threshold: 0}).observe(video);
  }
})();
