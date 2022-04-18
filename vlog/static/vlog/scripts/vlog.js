window.jvlog = {};

window.jvlog.initialise = () => {
  $('#id_author').on('keypress', () => {
    $('.comment.error').hide();
  });

  $('#id_text').on('keypress', () => {
    $('.comment.error').hide();
  });
};
