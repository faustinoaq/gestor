# Coffescript code for default theme
$ ->

    # Toggle class show in nav on click in menu
    $(".menu").click (event) =>
        $(".nav").toggleClass 'show'
        false

    # Hide nav on click in content
    $("section").click =>
        if $(".nav").hasClass "show"
            $(".nav").removeClass "show"
        return

    # Hide parent element
    $(".close").click (event) =>
        $(event.currentTarget).parent().hide()
        return

    # Avoid multiple send in forms
    $("form").submit (event) =>
        $(event.currentTarget).submit =>
            false
        true

    # Delete comments with Ajax
    $('.comment-delete').click (event) =>
        if confirm "If you delete this comment you can't recover\nDo you want to delete it anyway?"
            link = $(event.currentTarget).data('path')
            $.ajax link,
                type: 'DELETE'
                error: ->
                    alert('Delete Error')
                    return
                success: (data) ->
                    $(event.currentTarget).parent().hide()
                    return
        false

    # Confirm when deleting an item
    $('.delete').click (event) =>
        if confirm "If you delete this post you can't recover\nDo you want to delete it anyway?"
            true
        else
            false

    # Cancel back
    $('.cancel').click (event) =>
        window.history.back()
        false

    return
