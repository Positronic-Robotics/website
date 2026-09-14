// Keep the run video playing: the autoplay attribute alone is not enough.
// A browser may refuse it, and Chrome stops one it judges off screen.
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
