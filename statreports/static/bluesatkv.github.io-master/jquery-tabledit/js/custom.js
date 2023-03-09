(function($) {

  /** @function loadContent
   * @description Load content by href links
   * @requires nothing
   */

  function loadContent(hash) {
    if (hash === '') {
      hash = 'home';
    }

    $('html, body').animate({scrollTop: 0}, '600', 'swing');
    $('section').load('includes/' + hash + '.html');
  }

  $(window).on('hashchange', function () {
    loadContent(location.hash.slice(1),function(){
      $.getScript("js/jquery.tabledit.min.js");
    });
  });

  var url = window.location.href;
  var hash = url.substring(url.indexOf("#") + 1);

  if (hash === url) {
    hash = 'home';
  }

  $('section').load('includes/' + hash + '.html');
  $('header').load('includes/header.html');
  $('footer').load('includes/footer.html');

})(window.jQuery);