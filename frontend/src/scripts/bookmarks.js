const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

const initBookmarks = () => {
  $(".js-bookmarks a.bookmark-create").click(function(x) {
    axios
      .post(this.href, {}, axios_config)
      .then(response => {
        $(this).parent().removeClass("bookmark-absent");
        $(this).parent().addClass("bookmark-present");
      })
      .catch(error => console.log(error));
    return false;
  });

  $(".js-bookmarks a.bookmark-delete").click(function(x) {
    axios
      .delete(this.href, axios_config)
      .then(response => {
        $(this).parent().addClass("bookmark-absent");
        $(this).parent().removeClass("bookmark-present");
      })
      .catch(error => console.log(error));
    return false;
  });

}

export { initBookmarks }
