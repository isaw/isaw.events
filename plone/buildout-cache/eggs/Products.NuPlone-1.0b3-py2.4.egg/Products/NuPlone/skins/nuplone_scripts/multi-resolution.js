registerPloneFunction(function() {
  var f = function() {
    var frameWidth;
    if (self.innerWidth) {
      frameWidth = self.innerWidth;
    } else if (document.documentElement && document.documentElement.clientWidth) {
      frameWidth = document.documentElement.clientWidth;
    } else if (document.body) {
      frameWidth = document.body.clientWidth;
    } else {
      return;
    }
    if (frameWidth < 1014) {
      addClassName(document.body, 'narrow');
      removeClassName(document.body, 'medium');
      removeClassName(document.body, 'wide');
    } else if (frameWidth > 1260) {
      removeClassName(document.body, 'narrow');
      removeClassName(document.body, 'medium');
      addClassName(document.body, 'wide');
    } else {
      removeClassName(document.body, 'narrow');
      addClassName(document.body, 'medium');
      removeClassName(document.body, 'wide');
    }
  };
  registerEventListener(window, 'resize', f);
  f();
});
