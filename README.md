# sphinxcontrib-diff2html

## 概要

[diff2html](https://diff2html.rtfpessoa.xyz/)をSphinx、reSTの中から使うための拡張です。

literalincludeのdiffオプションではなく、github風に見せたいという方向けです。

## 機能

- diff2htmlに準じます。

## 使い方

### conf.pyでの設定

拡張を有効にします。

```py
extensions = [
  'sphinxcontrib.diff2html'
]
```

内部でハイライトを行う際に、highlightJsを使用しています。

ここで、特定のjsやcssを読ませたい場合は、以下のように記述します。

未指定の場合は、拡張側で指定するjsとcssが適用されます。

```py
#jsの指定
diff2html_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/highlight.min.js',
                     'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/languages/scala.min.js']

#cssスタイルの指定
diff2html_style = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/styles/androidstudio.min.css'
```

### reSTでの使用

```rst
.. diff2html ::
      
    <git diffで出力される形式の文字列>

```

## demo

