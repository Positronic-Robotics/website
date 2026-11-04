// The lab film over the heading. A narrow screen gets the portrait cut. The film plays
// while it is on screen; a reader who asks for reduced motion gets the poster.
(function () {
  var video = document.querySelector(".ev-film-video");
  if (!video) return;
  var narrow = window.matchMedia("(max-width: 700px)").matches;
  if (narrow) video.poster = video.dataset.posterNarrow;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  video.src = narrow ? video.dataset.srcNarrow : video.dataset.src;
  video.preload = "auto";
  function play() {
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
  }
  var onScreen = true;
  new IntersectionObserver(function (entries) {
    onScreen = entries[0].isIntersecting;
    if (onScreen && !document.hidden) play(); else video.pause();
  }).observe(video);
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) video.pause(); else if (onScreen) play();
  });
})();
