(function (factory) {
  if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory);
  } else {
    factory(window.jQuery);
  }
}(function ($) {

    var tmpl = $.summernote.renderer.getTemplate();

    $.summernote.addPlugin({
        name: 'codeHighlight',
        buttons: {
            "codeHighlight": function (lang, options) {
                var list = '';
                var langs = hljs.listLanguages();
                for (lang in langs) {
                    list += '<li><a data-event="codeHighlight" href="#" data-value="' + langs[lang] + '">' + langs[lang] + '</a></li>';
                }

                var dropdown = '<ul class="dropdown-menu" style="max-height: 200px; overflow: auto"> ' + list + ' </ul>';
                return tmpl.iconButton('fa fa-lightbulb-o', {
                    value: 'codeHighlight',
                    title: 'Code highlight',
                    hide: true,
                    dropdown: dropdown
                });
            }

        },

        events: {
            "codeHighlight": function (event, editor, layoutInfo, value) {
                var $editable = layoutInfo.editable();
                var code = window.getSelection().toString();
                var codeTag = '<pre><code class="' + value + '">' + code + '</code></pre>';
                console.log(codeTag);
                editor.insertNode($editable, $(codeTag)[0]);
                $('pre code').each(function (i, block) {
                    hljs.highlightBlock(block);
                });
            }
        }

    });
}));