(function () {
  'use strict';

  // Open a modal from a button inside another modal, closing the first cleanly
  // (Bootstrap 4 does not handle stacked modals well on its own).
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-modal-switch]');
    if (!trigger || !window.jQuery) return;
    e.preventDefault();
    var target = trigger.getAttribute('data-modal-switch');
    var current = trigger.closest('.modal');
    if (current) {
      $(current).one('hidden.bs.modal', function () { $(target).modal('show'); });
      $(current).modal('hide');
    } else {
      $(target).modal('show');
    }
  });

  // Submit modal forms over fetch so the user never leaves the page.
  document.addEventListener('submit', function (e) {
    var form = e.target.closest('.js-modal-form');
    if (!form) return;
    e.preventDefault();

    var submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    fetch(form.action, {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      body: new FormData(form),
    })
      .then(function (resp) { return resp.json(); })
      .then(function (payload) {
        if (payload.success) {
          window.location.href = payload.redirect;
          return;
        }
        // Re-render the form (with validation errors) inside the modal.
        var wrap = form.closest('.js-modal-form-wrap');
        if (wrap) {
          wrap.outerHTML = payload.html;
          if (window.initEmojiPickers) window.initEmojiPickers();
        }
        if (submitBtn) submitBtn.disabled = false;
      })
      .catch(function () {
        // Network/JS failure: fall back to a normal full-page submit.
        if (submitBtn) submitBtn.disabled = false;
        form.submit();
      });
  });
})();
