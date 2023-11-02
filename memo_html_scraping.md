# 2023/11/02 htmlから翻訳結果を抜き出したいメモ:

## 試しにデベロッパーツールからDeepLのブラウザを探ってみた。

- <span _d-id="392" class="--l --r sentence_highlight"># ヘッダー</span>
- <span _d-id="824" class="--l --r sentence_highlight">MLOpsのライフサイクル</span>
- <span _d-id="907" class="--l --r sentence_highlight">レシシスオプス</span>

わかった事:

- `_d-id`属性は 翻訳を走らせる度にバラバラ。
- `class`属性は 翻訳を何度走らせても共通。(でも他の翻訳結果以外の箇所にもある。)
  - デベロッパーツールで調べた感じでは、翻訳前テキストと翻訳後テキストの2箇所っぽい。
  - よってもっと外側の要素で絞り込む必要がありそう。

## より外側のdev要素をみてみた。

- <div contenteditable="true" role="textbox" aria-multiline="true" tabindex="0" aria-disabled="false" data-content="true" data-dl-no-input-translation="true" _d-id="5" aria-placeholder="" disabled="false" data-remove-rtf="true" aria-labelledby="translation-target-heading" lang="ja-JP" class=""><p _d-id="972"><span _d-id="994" class="--l --r sentence_highlight"># ヘッダー</span></p></div>
- <div contenteditable="true" role="textbox" aria-multiline="true" tabindex="0" aria-disabled="false" data-content="true" data-dl-no-input-translation="true" _d-id="5" aria-placeholder="" disabled="false" data-remove-rtf="true" aria-labelledby="translation-target-heading" lang="ja-JP" class=""><p _d-id="1343"><span _d-id="1383" class="--l --r sentence_highlight">MLOpsのライフサイクル</span></p></div>
- <div contenteditable="true" role="textbox" aria-multiline="true" tabindex="0" aria-disabled="false" data-content="true" data-dl-no-input-translation="true" _d-id="5" aria-placeholder="" disabled="false" data-remove-rtf="true" aria-labelledby="translation-target-heading" lang="ja-JP" class=""><p _d-id="889"><span _d-id="931" class="--l --r sentence_highlight">レシシスオプス</span></p></div>

わかったこと:

- span要素の1つ外側のp属性は共通する属性を持っていない。
- 更に1つ外側のdiv要素には色々共通する属性を持っていそう。
  - 特に`aria-labelledby`属性が`"translation-target-heading"`なので翻訳後テキストを表してくれてそう。

## 翻訳前テキストのdev要素はどうなってるか確認する...!

- <div contenteditable="true" role="textbox" aria-multiline="true" tabindex="0" aria-disabled="false" data-content="true" data-dl-no-input-translation="true" _d-id="1" aria-placeholder="翻訳するにはテキストを入力してください。文書ファイルを翻訳するには、PDF、Word（.docx）またはPowerPoint（.pptx）のファイルをドラッグ＆ドロップしてください。" disabled="false" data-remove-rtf="true" aria-labelledby="translation-source-heading" class="" lang="en-EN"><p _d-id="1439"><span _d-id="1496" class="--l --r sentence_highlight"><span _d-id="1498" class=" --l --r">#</span> <span _d-id="1502" class=" --l --r">header</span></span></p></div>
- <div contenteditable="true" role="textbox" aria-multiline="true" tabindex="0" aria-disabled="false" data-content="true" data-dl-no-input-translation="true" _d-id="1" aria-placeholder="翻訳するにはテキストを入力してください。文書ファイルを翻訳するには、PDF、Word（.docx）またはPowerPoint（.pptx）のファイルをドラッグ＆ドロップしてください。" disabled="false" data-remove-rtf="true" aria-labelledby="translation-source-heading" class="" lang="en-EN"><p _d-id="1012"><span _d-id="1425" class="--l --r sentence_highlight">MLOps Lifecycle</span></p></div>

わかったこと:

- `aria-labelledby`属性が`"translation-source-heading"`なので翻訳前テキストを表してくれてそう。
- `aria-labelledby`属性=`"translation-source-heading"`の要素が、三種類ありそう。`section`属性と`d-textarea`属性と`div`属性の3つ。それぞれ前から外側の要素であり、後ろの要素は手前の要素に含まれている。
