const wideScreen = window.matchMedia("(min-width: 600px)");
if (wideScreen.matches) {
  console.log('Running tests for widescreen display');

  QUnit.test("flyout should become visible when navigation tab is hovered over", function (assert) {
    window.jvlog.initialise();
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
    $('.navlink.about').trigger('mouseover');
    assert.true($('.navlink.about').children('.flyout').is(':visible'));
  });

  QUnit.test("only the flyout within the hovered-over tab should become visible on hover", function (assert) {
    window.jvlog.initialise();
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
    assert.false($('.navlink.learn').children('.flyout').is(':visible'));
    $('.navlink.about').trigger('mouseover');
    assert.true($('.navlink.about').children('.flyout').is(':visible'));
    assert.false($('.navlink.learn').children('.flyout').is(':visible'));
  });

  QUnit.test("flyout should be hidden again on mouseout of flyout", function (assert) {
    window.jvlog.initialise();
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
    $('.navlink.about').trigger('mouseover');
    assert.true($('.navlink.about').children('.flyout').is(':visible'));
    $('.navlink.about').children('.flyout').trigger('mouseout');
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
  });

  QUnit.test("flyout should be hidden again on mouseout of nav tab", function (assert) {
    window.jvlog.initialise();
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
    $('.navlink.about').trigger('mouseover');
    assert.true($('.navlink.about').children('.flyout').is(':visible'));
    $('.navlink.about').trigger('mouseout');
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
  });

  QUnit.test("selected nav tab should gain displaying-flyout class on hover", function(assert) {
    window.jvlog.initialise();
    assert.equal($('.selected').children('a').attr('class'), 'green_border');
    $('.selected').trigger('mouseover');
    assert.equal($('.selected').children('a').attr('class'), 'green_border displaying-flyout');
  });

  QUnit.test("normal (not selected) nav tab should not gain displaying-flyout class on hover", function(assert) {
    window.jvlog.initialise();
    assert.equal($('.learn').children('a').attr('class'), 'green_border');
    $('.learn').trigger('mouseover');
    assert.equal($('.learn').children('a').attr('class'), 'green_border');
  });

  QUnit.test("selected nav tab should lose displaying-flyout class on mouseout", function(assert) {
    window.jvlog.initialise();
    assert.equal($('.selected').children('a').attr('class'), 'green_border');
    $('.selected').trigger('mouseover');
    assert.equal($('.selected').children('a').attr('class'), 'green_border displaying-flyout');
    $('.selected').trigger('mouseout');
    assert.equal($('.selected').children('a').attr('class'), 'green_border');
  });

} else {
  console.log('Running test for smallscreen display');

  QUnit.test("flyout should not be shown if the screen width is less than 600px", (assert) => {
    window.jvlog.initialise();
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
    $('.navlink.about').trigger('mouseover');
    assert.false($('.navlink.about').children('.flyout').is(':visible'));
  });

}
