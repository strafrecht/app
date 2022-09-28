//require('codemirror/lib/codemirror.css');
//require('tui-editor/dist/tui-editor.css');
//require('tui-editor/dist/tui-editor-contents.css');
//require('highlight.js/styles/github.css');

//import { Editor } from 'tui-editor'

//var Editor = require('tui-editor');
//var Viewer = require('tui-editor/dist/tui-editor-Viewer');

if (document.querySelector('.modern')) {
	var text = document.querySelector('.modern')
	var content = text.textContent.trimLeft()

	var editor = new tui.Editor({
		el: document.querySelector('.editor'),
		initialEditType: 'wysiwyg',
		previewStyle: 'vertical',
		height: '600px',
		initialValue: content,
		usageStatistics: false,
	})

	editor.on('change', function() {
		text.innerHTML = editor.getValue().replace(/\\/g, '')
	})

	/*
	var viewer = new tui.Viewer({
		el: document.querySelector('.viewer'),
		height: '500px',
		initialValue: 'test'
	})
	*/
}
