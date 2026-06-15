(function () {
  'use strict';

  function insertAtCursor(input, text) {
    var start = input.selectionStart;
    var end = input.selectionEnd;
    if (typeof start === 'number') {
      input.value = input.value.slice(0, start) + text + input.value.slice(end);
      var pos = start + text.length;
      input.setSelectionRange(pos, pos);
    } else {
      input.value += text;
    }
    input.focus();
  }

  function attach(input) {
    if (input.dataset.emojiReady) return;
    input.dataset.emojiReady = '1';

    // Wrap the input, keeping its .invalid-feedback sibling alongside so
    // Bootstrap's error styling keeps working.
    var wrap = document.createElement('div');
    wrap.className = 'emoji-field';
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);
    var next = wrap.nextSibling;
    if (next && next.nodeType === 1 && next.classList.contains('invalid-feedback')) {
      wrap.appendChild(next);
    }

    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'emoji-toggle';
    toggle.setAttribute('aria-label', 'Choose an emoji');
    toggle.title = 'Choose an emoji';
    toggle.innerHTML = '<span class="emoji-toggle__face">😊</span>' +
      '<span class="emoji-toggle__caret" aria-hidden="true">▾</span>';

    // <emoji-picker> is the custom element provided by emoji-picker-element.
    var popover = document.createElement('div');
    popover.className = 'emoji-popover';
    var picker = document.createElement('emoji-picker');
    picker.classList.add('dark');
    popover.appendChild(picker);

    wrap.appendChild(toggle);
    wrap.appendChild(popover);

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      popover.classList.toggle('is-open');
    });
    picker.addEventListener('emoji-click', function (e) {
      insertAtCursor(input, e.detail.unicode);
    });
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) popover.classList.remove('is-open');
    });
  }

  function init(root) {
    (root || document).querySelectorAll('.js-emoji-input').forEach(attach);
  }

  // Exposed so re-rendered modal forms (after an AJAX validation error) re-init.
  window.initEmojiPickers = init;
  document.addEventListener('DOMContentLoaded', function () { init(); });
})();
