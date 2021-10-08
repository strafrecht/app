import Editor from '@toast-ui/editor'

const initEditor = () => {
    if (document.querySelector('.modern')) {
        var text = document.querySelector('.modern')
        var content = text.textContent.trimLeft()

        const editor = new Editor({
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
    }
}

export { initEditor }