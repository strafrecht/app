function createPollChooser(id, modelString) {
	var customAdmin = "cms" || false
    var chooserElement = $('#' + id + '-chooser');
    var docTitle = chooserElement.find('.title');
    var input = $('#' + id);
    var editLink = chooserElement.find('.edit-link');

    $('.action-choose', chooserElement).on('click', function() {
        ModalWorkflow({
            //url: window.chooserUrls.pollsChooser + modelString + '/',
			url: `/${customAdmin}/polls/choose/`,
            onload: SNIPPET_CHOOSER_MODAL_ONLOAD_HANDLERS,
            responses: {
                snippetChosen: function(snippetData) {
                    input.val(snippetData.id);
                    docTitle.text(snippetData.string);
                    chooserElement.removeClass('blank');
                    editLink.attr('href', snippetData.edit_link);
                }
            }
        });
    });

    $('.action-clear', chooserElement).on('click', function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}

/*
function createPollChooser(id) {
	var customAdmin = "cms" || false
	console.log('got here');
	var chooserElement = $('#' + id + '-chooser');
	var docTitle = chooserElement.find('.title');
	var input = $('#' + id);
	var editLink = chooserElement.find('.edit-link');
	var pollChooser = `/${customAdmin}/polls/choose/`;

	$('.action-choose', chooserElement).click(function(e) {
		e.preventDefault();
		console.log("HERE")

		ModalWorkflow({
			url: pollChooser,
			responses: {
				pollChosen: function(pollData) {
					console.log(pollData)
					input.val(pollData.id);
					docTitle.text(pollData.string);
					chooserElement.removeClass('blank');
					editLink.attr('href', pollData.edit_link);
				}
			}
		});
	});

	$('.action-clear', chooserElement).click(function() {
		input.val('');
		chooserElement.addClass('blank');
	});
}
*/
