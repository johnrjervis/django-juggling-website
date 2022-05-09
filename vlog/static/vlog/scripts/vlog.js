window.jvlog = {};

window.jvlog.initialise = () => {
  $('#id_author').on('keypress', () => {
    $('.comment.error').hide();
  });

  $('#id_text').on('keypress', () => {
    $('.comment.error').hide();
  });

  $('.btn_close').click(function() {
    $(this).parent().hide();
  });

  $('.navlink').mouseover(function() {
    if (window.matchMedia("(min-width: 600px)").matches) {
      $(this).children('.flyout').show();
    }
  });

  $('.navlink.selected').mouseover(function() {
    if ($(this).children('.flyout').length) {
      $(this).children('a').addClass('displaying-flyout');
    }
  });

  $('.flyout').mouseout(function() {
    $(this).hide();
    $(this).parent('.selected').children('a').removeClass('displaying-flyout');
  });

  $('.navlink').mouseout(function() {
    $(this).children('.flyout').hide();
    $(this).children('a').removeClass('displaying-flyout');
  });

};
