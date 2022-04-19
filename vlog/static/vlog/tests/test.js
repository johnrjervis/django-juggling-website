QUnit.test("errors should be hidden on keypress in comment author input", (assert) => {
  window.jvlog.initialise();
  $('#id_author').trigger('keypress');
  assert.equal($('.comment.error').is(':visible'), false);
});

QUnit.test("errors should be hidden on keypress in comment textfield", (assert) => {
  window.jvlog.initialise();
  $('#id_text').trigger('keypress');
  assert.equal($('.comment.error').is(':visible'), false);
});

QUnit.test("errors should be hidden when close button is clicked", (assert) => {
  window.jvlog.initialise();
  $('.btn_close').trigger('click');
  assert.equal($('.comment.error').is(':visible'), false);
});

QUnit.test("errors aren't hidden if there is no keypress", (assert) => {
  window.jvlog.initialise();
  assert.equal($('.comment.error').is(':visible'), true);
});
