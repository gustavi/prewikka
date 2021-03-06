String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};


$(document).ready(function(){
  var $cache = null;
  var $cachef = null;

  $.fn.popupUnique = function(animshow, animhide) {
        if ( $cache && this.is(':visible') ) {
                $cachef($cache);
                $cache = null;
        } else {
                animshow(this);
                if ( $cache )
                        $cachef($cache);
                $cachef = animhide;
                $cache = this;
        }

        return false;
  };

  $.fn.check = function(mode){
        return this.each(function() { this.checked = mode; } );
  };

  $(document).on("click", ".popup_menu_toggle", function(){
    $(this).next().popupUnique(function(data){data.show('fast'); data.css('display','block')}, function(data){data.hide('fast')});
  });

  $(document).on("show.bs.popover", '[data-toggle="popover"]', function() {
    $('[data-toggle="popover"]').not(this).popover("hide");
  });

  $(document).on("hidden.bs.popover", '[data-toggle="popover"]', function() {
    // See https://github.com/twbs/bootstrap/issues/16732
    $(this).data("bs.popover").inState.click = false;
  });


  $(document).on("click", "#logout", function() {
    this.href = "logout?redirect=" + encodeURIComponent(location.href);
  });

// Repeatable entries

  $(document).on("click", ".del_entry_row", function() {
      var row = $(this).parents(".repeat-entry");
      if ( row.siblings(".repeat-entry").length > 0 )
          row.remove();
      else
          row.trigger("reset_row");
      return false;
  });

  $(document).on("click", ".add_entry_row", function() {
      var row = $(this).parents(".repeat-entry");
      var newrow = row.clone();
      row.after(newrow);
      newrow.trigger("reset_row");
      return false;
  });

  $(document).on('click', '[data-confirm]', function() {
      var input = $(this);
      var confirm = input.data("confirm");

      function confirm_handler() {
          input.removeData("confirm").removeAttr('data-confirm');

          /*
           * Simulate a click using the DOM's native click() method
           * as jQuery's function does not work properly on "a" tags.
           * See http://stackoverflow.com/a/21762745 for more information.
           */
          input[0].click();
          input.attr("data-confirm", confirm).data("confirm", confirm);
          $('#prewikka-dialog-confirm').modal('hide');
          return false;
      }

      // Remove the handler in case it was already set. And set the correct handler
      $('#prewikka-dialog-confirm-OK').off("click").on("click", confirm_handler);

      prewikka_dialog({message: confirm, type: "confirm"});
      return false;
  });

  $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function() {
      $(this).closest(".dropdown-submenu").toggleClass("open");
      return false;
  });

  $(document).on('click', '.popup_menu_dynamic', function() {
      $(this).removeClass("popup_menu_dynamic");

      if ( ! $(this).data("popup-url") )
          return;

      var popup_menu = $(this).next(".popup_menu");
      popup_menu.append($("<span>", {
        "class": "popup_menu_loading",
        "text": "Loading..."
      }));

      $.ajax({
          type: "GET",
          url: $(this).data("popup-url"),
          success: function(data) {
              popup_menu.find(".popup_menu_loading").remove();
              popup_menu.append(data.join(""));
          }
      });
  });

  $(document).on('click', '#prewikka-notification .close', function() {
    $("#prewikka-notification").hide();
  });

  /*
   * Make sure bootstrap modal appear in the order they are drawn (as opposed to html order).
   */
  $(document).on('show.bs.modal', '.modal', function () {
    var zIndex = 1050 + $('.modal-backdrop:visible').length;
    $(this).css('z-index', zIndex);
  });

  /*
   * Destroy AJAX modal completly when they are removed.
   */
  $(document).on('hidden.bs.modal', '.ajax-modal', function () {
    $(this).data('bs.modal', null);
    $(this).remove();
  });
});

function prewikka_resizeTopMenu() {
    var mainmenu = $('#main_menu_navbar');
    var topmenu = $("#topmenu .topmenu_nav");
    var main = $("#main");
    var window_width = $(window).width();

    mainmenu.removeClass('collapsed'); // set standard view
    main.css("margin-top", "");
    mainmenu.css("margin-top", "");
    topmenu.css("height", "").css("width", "");

    if ( window_width > 768 ) {
        topmenu.css("width", window_width - mainmenu.innerWidth());

        if ( Math.max(mainmenu.innerHeight(), topmenu.innerHeight()) > 60 ) { // check if the topmenu or mainmenu is split across two lines
            mainmenu.addClass('collapsed');

            topmenu.css("width", window_width - mainmenu.innerWidth());

            var height = Math.max(mainmenu.innerHeight(), topmenu.innerHeight());

            if ( height > 60 ) { // check if we've still got 2 lines or more
                main.css("margin-top", height - 40);
                topmenu.css("height", height);
            }
        }
    }
    else {
        mainmenu.css("margin-top", topmenu.innerHeight());
        main.css("margin-top", mainmenu.innerHeight());
    }
}


function setup_position(obj)
{
    $(obj).css({top:0, left:0}).position({
        my: "center top",
        at: "center top",
        of: $(window),
        collision: "none"
    });
}


function prewikka_notification(data)
{
    var notification = $("#prewikka-notification");

    setup_position(notification);

    $(notification).find(".title").text(data.name || "");
    $(notification).find(".content").text(data.message);

    if ( typeof(data.classname) === 'undefined' )
        data.classname = "success";

    $(notification).find(".alert").removeClass().addClass("alert alert-" + data.classname);
    $(notification).find(".fa").removeClass().addClass("fa fa-" + data.icon);
    $(notification).stop().fadeIn(0).show().delay(data.duration || 2000).fadeOut(1000);
}


function _dialog_common(dialog)
{
    $(dialog).modal();
    setup_position(dialog);

    if ( $(dialog).attr("data-draggable") )
        $(dialog).draggable({ handle: ".modal-header" });

    _initialize_components(dialog);
}


function prewikka_json_dialog(data)
{
    var dialog;

    $("#prewikka-dialog-container").append(data.content);
    dialog = $("#prewikka-dialog-container > :last-child");

    $(dialog).addClass("modal ajax-modal fade");
    _dialog_common(dialog);
}


function prewikka_dialog(data)
{
    if ( typeof(data.type) == 'undefined' )
        data.type = "standard";

    var dialog = $("#prewikka-dialog-" + data.type);
    var header = $(dialog).find(".modal-header");

    $(header).removeClass().addClass("modal-header");
    if ( data.classname )
            $(header).addClass("alert-" + data.classname);

    $(dialog).find(".content").text(data.message);
    _dialog_common(dialog);
}


function prewikka_dialog_getMaxHeight() {
    return $(window).height() - $("#topmenu").height() - 100;
}


function prewikka_getRenderSize(container, options)
{
        var parent;
        var size = [0, 0];
        var overflow_backup = document.body.style.overflow;

        /*
         * take into account potential scrollbar size.
         */
        document.body.style.overflow = "scroll";

        /*
         * Get the first parent block level element, so that we gather
         * the full usable width.
         */
        parent = $(container).parents().filter(function() {
            return $(this).css("display") == "block";
        }).first();

        size[0] = options.width;
        if ( ! size[0] )
            size[0] = $(parent).width();

        if ( typeof(options.width) == "string" && options.width.indexOf("%") != -1 ) {
            if ( ! options.spacing )
                options.spacing = 0;

            size[0] = ($(parent).width() - options.spacing) / 100 * parseInt(options.width) - options.spacing;
        }

        if ( typeof(options.height) == "string" && options.height.indexOf("%") != -1 )
            size[1] = ($(parent).width() - options.spacing) / 100 * parseInt(options.height) - options.spacing;
        else {
            size[1] = options.height;
            if ( ! size[1] )
                size[1] = $("#_main_viewport").height();
        }

        document.body.style.overflow = overflow_backup;

        return size;
}


function prewikka_grid(table, settings) {
    var conf = _mergedict({
        datatype: "local",
        cmTemplate: {title: false},
        autoencode: true,
        autowidth: true,
        forceFit: true,
        shrinkToFit: true,
        guiStyle: "bootstrap",
        iconSet: "fontAwesome",
        prmNames: {sort: "sort_index", order: "sort_order", search: null, nd: null}
    }, settings);

    return $(table).jqGrid(conf);
}


function prewikka_autocomplete(field, url, submit) {
    field.autocomplete({
        minLength: 0,
        autoFocus: true,
        source: function(request, response) {
            $.ajax({
                url: url,
                data: {query: request.term},
                dataType: "json",
                global: false, // No prewikka dialog in case of error
                success: function(data) {
                    var rows = $.map(data.rows, function(row) {
                        return row.cell.name;
                    });
                    response(rows);
                    field.parent("div").toggleClass("has-error", !rows.length);
                    field.next().toggleClass("fa-close", !rows.length);
                    if ( submit ) submit.prop("disabled", $(".has-error").length);
                },
                error: function(xhr, status, error) {
                    field.parent("div").addClass("has-error");
                    field.next().addClass("fa-close");
                    if ( submit ) submit.prop("disabled", true);
                    var message = xhr.responseText ? $.parseJSON(xhr.responseText).details : error || "Connection error";
                    field.prop("title", message);
                    response([]);
                }
            });
        },
        select: function() {
            if ( submit ) submit.prop("disabled", $(".has-error").length);
        }
    })
    .focus(function() {
        $(this).autocomplete("search");
    });
}
