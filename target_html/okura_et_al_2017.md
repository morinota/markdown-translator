### 0.1. link リンク

- [元論文]https://dl.acm.org/doi/abs/10.1145/3097983.3098108?casa_token=E2V72vGAK60AAAAA:b1coQnhN8zeSe6KNZrv_2T3HC5NfMI5LtYH7Mrj9ckNTblQQuiP9FEvoPtpGYnIN5hbNA7zEwefO6qvo
- [githubのリポジトリ](https://github.com/louislung/DAE_RNN_News_Recommendation)
- [the article embeddings trainingに関するブログ記事](https://medium.com/deep-learning-hk/compute-document-similarity-using-autoencoder-with-triplet-loss-eb7eb132eb38)

### 0.2. title タイトル

Embedding-based News Recommendation for Millions of Users
数百万人のユーザーを対象にした埋め込み型ニュース推薦システム

### 0.3. ABSTRACT ABSTRACT

これはニュースの埋め込みベクトル([the article embeddings trainingに関するブログ記事](https://medium.com/deep-learning-hk/compute-document-similarity-using-autoencoder-with-triplet-loss-eb7eb132eb38))を元にした、コンテンツベースの手法

It is necessary to understand the content of articles and user preferences to make effective news recommendations. While ID-based methods, such as collaborative filtering and low-rank factorization, are well known for making recommendations, they are not suitable for news recommendations because candidate articles expire quickly and are replaced with new ones within short spans of time. Word-based methods, which are often used in information retrieval settings, are good candidates in terms of system performance but have issues such as their ability to cope with synonyms and orthographical variants and define "queries" from users' historical activities. This paper proposes an embedding-based method to use distributed representations in a three step end-to-end manner: (i) start with distributed representations of articles based on a variant of a denoising autoencoder, (ii) generate user representations by using a recurrent neural network (RNN) with browsing histories as input sequences, and (iii) match and list articles for users based on inner-product operations by taking system performance into consideration. The proposed method performed well in an experimental offline evaluation using past access data on Yahoo! JAPAN's homepage. We implemented it on our actual news distribution system based on these experimental results and compared its online performance with a method that was conventionally incorporated into the system. As a result, the click-through rate (CTR) improved by 23% and the total duration improved by 10%, compared with the conventionally incorporated method. Services that incorporated the method we propose are already open to all users and provide recommendations to over ten million individual users per day who make billions of accesses per month.

効果的なニュース推薦を行うためには、記事の内容やユーザの嗜好を理解する必要がある。 推薦を行う手法としては、協調フィルタリングや低ランク因子分解などのIDベースの手法がよく知られているが、**候補となる記事はすぐに期限切れとなり、短いスパンで新しい記事に入れ替わる**ため、ニュース推薦には適さない。 また、情報検索の分野でよく用いられる単語ベースの手法は、システム性能の点では良い候補であるが、同義語や表記ゆれへの対応や、ユーザの過去の行動から「クエリ」を定義するなどの問題がある。

本論文では、

- (i)ノイズ除去オートエンコーダの変形に基づく記事の分散表現から始め、
- (ii)閲覧履歴を入力列とするリカレントニューラルネットワーク（RNN）を用いてユーザ表現を生成し、
- (iii)システム性能を考慮した内積演算に基づいてユーザの記事を照合・リスト化する

という**3段階でエンドツーエンドで利用する埋め込み型方式**を提案する。 提案手法は、Yahoo! JAPANのホームページの過去のアクセスデータを用いたオフラインでの実験評価において、良好な結果を得ました。 この実験結果をもとに実際のニュース配信システムに実装し、従来からシステムに組み込まれている手法とオンライン性能を比較しました。 その結果、従来手法と比較して、クリックスルー率（CTR）が23％、総時間が10％改善されました。 私たちが提案する手法を取り入れたサービスは、すでにすべてのユーザーに公開されており、1日1000万人以上、月に数十億回のアクセスをする個人ユーザーにおすすめ情報を提供しています。

## 1. INTRODUCTION

It is impossible for users of news distributions to read all available articles due to limited amounts of time. Thus, users prefer news services that can selectively provide articles. Such selection is typically done manually by editors and a common set of selected stories are provided to all users in outmoded media such as television news programs and newspapers. However, we can identify users before they select articles that will be provided to them on the Internet by using information, such as that in user ID cookies, and personalize the articles for individual users [3, 22].
ニュース配信の利用者は、**限られた時間の中で、配信されているすべての記事を読むことは不可能**である。 そのため，ユーザは記事を選択的に提供できるニュースサービスを好む。 テレビのニュース番組や新聞のような時代遅れのメディアでは、このような選択は通常編集者の手作業で行われ、選択された記事の共通のセットが全ユーザに提供される。 しかし，インターネット上では，ユーザIDクッキーなどの情報を利用して，提供される記事を選択する前にユーザを特定し，個々のユーザに対して記事をパーソナライズすることができる[3, 22]。

ID-based methods, such as collaborative filtering and low-rank factorization, are well known in making recommendations. However, Zhong et al. [22] suggested that such methods were not suitable for news recommendations because candidate articles expired too quickly and were replaced with new ones within short time spans. Thus, the three keys in news recommendations are: Understanding the content of articles, • Understanding user preferences, and • Listing selected articles for individual users based on content and preferences.
ID ベースの推薦方法としては，協調フィルタリングや低ランク因子法などがよく知られている． しかし，Zhong ら[22]は，**候補となる記事の期限が切れるのが早く，短時間で新しい記事に置き換わるため，このような方法はニュース推薦には適さない**としている．
ニュース推薦における鍵は以下の3つである。

- 記事の内容を理解すること，
- ユーザーの嗜好を理解すること，
- 内容と嗜好に基づいて個々のユーザーに対して選択された記事をリストアップすること

In addition, it is important to make recommendations in the real world [14] that respond to scalability and noise in learning data [14]. Applications also need to return responses within hundreds of milliseconds with every user access.
さらに、学習データのスケーラビリティやノイズに対応した実世界でのレコメンデーション[14]が重要である。 また、アプリケーションは、**ユーザーのアクセスごとに数百ミリ秒以内にレスポンスを返す必要**がある。

A baseline implementation to cover the three keys would be as follows. An **article** is regarded as a collection of words included in its text. A **user** is regarded as a collection of words included in articles he/she has browsed. The implementation learns click probability using co-occurrence of words between candidates of articles and browsing histories as features.
3つの鍵をカバーする基本的な実装は以下の通りである。 **articleは、そのテキストに含まれる単語の集まり**とみなされる。 **ユーザは、自分が読んだ記事に含まれる単語の集まり**とみなす。

This method has some practical advantages. It can immediately reflect the latest trends because the model is very simple so that the model can be taught to learn and update in short periods of time. The estimation of priority can be quickly calculated using existing search engines with inverted indices on words.
この方法には、実用的な利点がある。 **モデルが非常に単純であるため、短期間で学習・更新が可能であるため、最新のトレンドを即座に反映**できる。 優先度の推定は、単語の転置インデックスを持つ既存の検索エンジンを用いて迅速に計算することができる。

The previous version of our implementation was based on this method for these reasons. However, it had some issues that may have had a negative impact on the quality of recommendations. The first regarded the representation of words. When a word was used as a feature, two words that had the same meaning were treated as completely different features if the notations were different. This problem tended to emerge in news articles when multiple providers separately submitted articles on the same event. The second regarded the handling of browsing histories. Browsing histories were handled as a set in this approach. However, they were actually a sequence, and the order of browsing should have represented the transition of user interests. We also had to note large variances in history lengths by users that ranged from private browsing to those who visited sites multiple times per hour. Deep-learning-based approaches have recently been reported to be effective in various domains. Distributed representations of words thoroughly capture semantic information [11, 16]. Recurrent neural networks (RNNs) have provided effective results as a method of handling input sequences of variable length [9, 15, 17].
前バージョンの実装は、これらの理由からこの方法に基づいていました。 しかし、レコメンデーションの品質に悪影響を及ぼす可能性のある問題がいくつかあった。

- ひとつは、単語の表現方法である。
  - 単語を特徴量とした場合、同じ意味の単語でも表記が違えば全く別の特徴量として扱われてしまう。
  - この問題は、同じ出来事について複数のプロバイダが別々に記事を投稿したニュース記事で発生しがちであった。
- 二つ目は、閲覧履歴の扱いである。
  - 本手法では、閲覧履歴を集合として扱っている。
  - しかし、履歴は連続したものであり、本来であれば**閲覧の順番がユーザの興味の変遷を表すもの**である。
  - また、私的な閲覧から1時間に何度もサイトを訪れるユーザーまで、**履歴の長さに大きなばらつきがある**ことに注意する必要がありました。

近年、様々な領域でディープラーニングを用いたアプローチが有効であることが報告されています。
単語の分散表現により、意味情報を徹底的に捉える[11, 16]。 リカレントニューラルネットワーク（RNN）は、可変長の入力列を扱う手法として有効な結果を出している[9, 15, 17]。

If we build a model with a deep network using an RNN to estimate the degree of interest between users and articles, on the other hand, **it is difficult to satisfy the response time constraints on accesses in real systems**. This paper proposes an embedding-based method of using distributed representations in a three step endto-end manner from representing each article to listing articles for each user based on relevance and duplication: Start with distributed representations of articles based on a variant of the denoising autoencoder (which addresses the first issue in Section 3). • Generate user representations by using an RNN with browsing histories as input sequences (which addresses the second issue in Section 4). • Match and list articles for each user based on the inner product of article-user for relevance and article-article for de-duplication (outlined in Section 2).
一方、RNNを用いたディープネットワークでモデルを構築し、ユーザと記事の間の関心度を推定すると、**実システムにおけるアクセスの応答時間制約を満たすことが困難**となる。
本論文では、各記事の表現から、関連性と重複に基づく各ユーザーの記事のリストアップまで、3段階のエンドツーエンドで分散表現を利用する埋め込みベースの手法を提案する。

- ノイズ除去オートエンコーダの変形に基づく**記事の分散表現**から始める（これはセクション3で最初の問題に対処する）。(i.e. **アイテムベクトルの生成**)
- **閲覧履歴を入力列とするRNNを用いてユーザ表現を生成**する（セクション4の第二の課題に対応）。(i.e. **ユーザベクトルの生成**)
- 記事-ユーザ間の関連性と記事-記事の重複排除の内積に基づいて、各ユーザの記事をマッチングしリスト化する（セクション2で概説）。(i.e.**アイテム-ユーザ対の類似度計算**)

The key to our method is using a simple inner product to estimate article-user relevance. We can calculate article representations and user representations before user visits in sufficient amounts of time. When a user accesses our service, we only select his/her representations and calculate the inner product of candidate articles and the representations. Our method therefore both expresses complex relations that are included in the user’s browsing history and satisfies the response time constraints of the real system.
我々の手法の鍵は、**記事とユーザーの関連性を推定するために単純な内積を使うこと**である。
我々は、**ユーザーがアクセスする前に**、十分な量の記事表現とユーザー表現を計算することができる。
ユーザが本サービスにアクセスする際、我々はユーザの表現を選択し、**候補記事と表現の内積を計算するだけ**である。そのため、本手法は**ユーザの閲覧履歴に含まれる複雑な関係を表現**し、かつ**実システムの応答時間の制約を満足する**ことができる。

The proposed method was applied to our news distribution service for smartphones, which is described in the next section. We compared our method to a conventional approach, and the results (see Section 6) revealed that the proposed method outperformed the conventional approach with a real service as well as with static experimental data, even if disadvantages, such as increased learning time and large latency in model updates, are taken into consideration.
提案手法を次節で述べるスマートフォン向けニュース配信サービスに適用しました。 提案手法を従来手法と比較した結果（6章参照），学習時間の増加やモデル更新の遅延が大きいなどのデメリットを考慮しても，実サービスや静的実験データにおいて提案手法が従来手法を上回る性能を持つことが明らかとなった．

## 2. OUR SERVICE AND PROCESS FLOW our service and process flow

The methods discussed in this paper were designed to be applied to the news distribution service on the homepage of Yahoo! JAPAN on smartphones. The online experiments described in Section 6 were also conducted on this page. This section introduces our service and process flow.
本稿で取り上げた手法は，スマートフォンにおけるYahoo! JAPANのトップページでのニュース配信サービスに適用することを想定している． また，6 章で述べたオンライン実験もこのページで行った． 本節では，サービスおよび処理の流れについて紹介する．

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/2-Figure1-1.png">

Figure 1: Example of Yahoo! JAPAN’s homepage on smartphones. This paper discusses methods of providing articles in Personalized module.
図1：スマートフォンにおけるYahoo! JAPANのトップページの例。 本稿では、Personalizedモジュールでの記事提供方法について述べる。

Figure 1 has a mockup of our service that was renewed in May 2015. There is a search window and links to other services at the top as a header. The middle part, called the Topics module, provides six articles on major news selected by human professionals for a general readership. The bottom part, called the Personalized module, provides many articles and advertising that has been personalized for individual users. Users in the Personalized module can see as many articles as they want if they scroll down to the bottom. Typical users scroll down to browse the approximately top 20 articles. This paper describes optimization to provide articles in the Personalized module
図1には、2015年5月にリニューアルした当社サービスのモックアップがあります。 ヘッダーとして上部に検索窓と他サービスへのリンクがあります。 中段はTopicsモジュールと呼ばれ、人間の専門家が選んだ主要なニュースを一般読者向けに6記事提供しています。 下はPersonalizedモジュールと呼ばれ、個々のユーザー向けにパーソナライズされた多くの記事や広告が提供されます。 パーソナライズドモジュールのユーザーは、一番下までスクロールすれば、好きなだけ記事を見ることができます。 一般的なユーザーは、スクロールダウンして上位20記事程度を閲覧する。 本稿では、Personalizedモジュールで記事を提供するための最適化について説明する。

Five processes are executed to select articles for millions of users for each user access. ユーザーアクセスごとに数百万人分の記事を選択するため、**5つのプロセスを実行**する.

- Identify: Obtain user features calculated from user history in advance. ユーザー履歴から算出したユーザーの特徴を事前に取得する。
- Matching: Extract articles from all those available using user features.利用可能なすべての記事から、ユーザーの特徴を用いて記事を抽出する。
- Ranking: Rearrange list of articles on certain priorities. ある優先順位で記事のリストを並べ替える。
- De-duplication: Remove articles that contain the same information as others. 重複排除 他の記事と同じ情報を含む記事を削除する。
- Advertising: Insert ads if necessary. 必要であれば、広告を挿入します。

These processes have to be done within hundreds of milliseconds between user requests and when they are displayed because available articles are constantly changing. In fact, as all articles in our service expire within 24 hours from the viewpoint of information freshness, tens of thousands of new articles are posted every day, and the same number of old articles are removed due to expiration. Thus, each process adopts computationally light methods that leverage pre-computed distributed article representations (described in Section 3) and user representations (described in Section 4).
これらの処理は、利用可能な記事が常に変化しているため、ユーザーがリクエストしてから表示されるまでの数百ミリ秒の間に行わなければならない。 実際、本サービスでは**情報の鮮度の観点から全ての記事が24時間以内に失効**するため、毎日数万件の新しい記事が投稿され、同数の古い記事が失効により削除されている。
そこで、各プロセスでは、**あらかじめ計算された分散記事表現（第3章で説明）とユーザ表現（第4章で説明）を活用した計算量の少ない方法を採用**している。

We use the inner product of distributed representations of a user and candidate articles in matching to quantify relevance and select promising candidates. We determine the order of priorities in ranking by considering additional factors, such as the expected number of page views and freshness of each article, in addition to the relevance used for matching. We skip similar articles in a greedy manner in de-duplication based on the cosine similarity of distributed representations. An article is skipped when the maximum value of its cosine similarity with articles with higher priorities is above a threshold. This is an important process in real news distribution services because similar articles tend to have similar scores in ranking. If similar articles are displayed close to one another, a real concern is that user satisfaction will decrease due to reduced diversity on the display. Details on comparison experiments in this process have been discussed in a report on our previous study [12]. Advertising is also important, but several studies [2, 10] have already reported on the relationship between advertising and user satisfaction, so such discussion has been omitted here.
マッチングに用いる**ユーザと候補記事の分散表現の内積を用いて、関連性を定量化**し、有望な候補を選択する。 マッチングに用いる関連性に加えて、各記事の**予想ページビュー数や鮮度などの要素を加味して、ランキングの優先順位を決定**する。 **重複排除では、分散表現のコサイン類似度に基づいて、類似記事を貪欲にスキップ**する。 
**より優先度の高い記事とのコサイン類似度の最大値が閾値を超えると、その記事はスキップ**される。 これは実際のニュース配信サービスにおいて重要な処理である。なぜなら、類似した記事はランキングにおいて類似したスコアを持つ傾向があるからである。 **類似記事同士が近くに表示されると、表示の多様性が損なわれ**、ユーザーの満足度が低下することが懸念される。 この過程での比較実験の詳細については、我々の先行研究報告[12]で述べている。 広告も重要であるが、広告とユーザ満足度の関係については、すでにいくつかの研究[2, 10]で報告されているので、ここではその議論は省略した。

## 3. ARTICLE REPRESENTATIONS 記事表現

Section 1 discussed a method of using words as features for an article that did not work well in certain cases of extracting and de-duplicating. This section describes **a method of dealing with articles as a distributed representation**. We proposed a method in our previous study [12], from which part of this section has been excerpted.
セクション1では、記事の特徴として単語を用いる方法について述べたが、これは抽出や重複除去の際にうまく機能しない場合があった。 本節では、**記事を分散表現として扱う方法**について述べる。 我々は以前の研究[12]でこの方法を提案したが、本節はその一部を抜粋したものである。

### 3.1. Generating Method 生成方法

Our method generates distributed representation vectors on the basis of a denoising autoencoder [19] with weak supervision. The conventional denoising autoencoder is formulated as:
本手法は，弱い監視を伴うノイズ除去オートエンコーダ[19]に基づいて，分散表現ベクトルを生成する． 従来のノイズ除去オートエンコーダは以下のように定式化される。

$$
\tilde{x} \sim q(\tilde{x}|x) \\
h = f(W\tilde{x} + b) \\
y =f(W'h + b') \\
\theta = \argmin_{W, W', b, b'} \sum_{x \in X} L_R(y, x)
$$

where $x \in X$ is the original input vector and $q(·|·)$ is the corrupting distribution. 
ここで、$x \in X$は元の入力ベクトルであり、$q(-|-)$は破損分布である。
The stochastically corrupted vector, $\tilde{x}$, is obtained from $q(·|x)$.
確率的破壊ベクトル$tilde{x}$は、$q(-|x)$から得られる。
The hidden representation, h, is mapped from $\tilde{x}$ through the network, which consists of an activation function, $f(·)$, parameter matrix W , and parameter vector b.
隠れ表現hは、活性化関数$f(-)$、パラメータ行列W、パラメータベクトルbからなるネットワークを通して$tilde{x}$から写像される。
In the same way, the reconstructed vector, y, is also mapped from h with parameters $W'$ and $b'$ . 
同様に、再構成ベクトルyもhからパラメータ$W'$と$b'$を用いて写像される。
Using a loss function, $L_{R}(·, ·)$, we learn these parameters to minimize the reconstruction errors of y and x. 
損失関数$L_{R}(-, -)$を用いて、これらのパラメータを学習し、yとxの再構成誤差を最小にする。

The h is usually used as a representation vector that corresponds to x. 
However, h only holds the information of x. 
**hは通常xに対応する表現ベクトルとして用いられる**が、hはxの情報しか持たない。
We want to interpret that the inner product of two representation vectors $h_0^T h_1$ is larger if $x_0$ is more similar to $x_1$. 
**2つの表現ベクトルの内積$h_0^T h_1$は、$x_0$が$x_1$とより似ていればより大きくなる**と解釈されたい。 
To achieve that end, we use a triplet, $(x_0, x_1, x_2) \in X^3$ , as input for training and modify the objective function to preserve their categorical similarity as:
そのために、三重項、$(x_0, x_1, x_2) \in X^3$ (つまり、３つの記事！図2を参照！)を学習の入力とし、それらのカテゴリ的類似性を保持するように**目的関数を以下のように修正**する。

$$
\tilde{x}_n \sim q(\tilde{x}_n|x_n) \\
h_n = f(W\tilde{x}_n + b) - f(b) \\
y_n = f(W'h_n + b')
L_T(h_0, h_1, h_2) = \log (1+ \exp(h_0^T h_2 - h_0^T h_1)) \\
\theta = \argmin_{W,W',b, b'} \sum_{x_0,x_1,x_2 \in T}
\sum_{n=0}^2 L_R(y_n,x_n) + \alpha L_T(h_0, h_1, h_2) \\
\tag{1}
$$

where $T \subset X^3$ , such that $x_0$ and $x_1$ are in the same category/similar categories and $x_0$ and $x_2$ are in different categories. The h in Eq.1 satisfies the property, $x = 0 ⇒ h = 0$. This means that an article that has no available information is not similar to any other article. The notation, $L_T (·, ·, ·)$ is a penalty function for article similarity to correspond to categorical similarity, and α is a hyperparameter for balancing. Figure 2 provides an overview of this method.
ここで、$T \subset X^3$ 、$x_0$と$x_1$が**同一カテゴリ/類似カテゴリ**、$x_0$と$x_2$が**異なるカテゴリ**に属するようなものである。
式1中のhは、$x = 0 ⇒ h = 0$という性質を満たす。
これは、利用可能な情報がない記事は、他の記事と類似していないことを意味する。
また、$L_T (-, -, -)$ という表記は、カテゴリの類似度に対応する記事の類似度のペナルティ関数であり、αはバランス調整のためのハイパーパラメータである。図 2 に本手法の概要を示す。

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/3-Figure2-1.png">

We use the elementwise sigmoid function, $\sigma(x)_i = 1/(1+exp(-x_i))$, as $f(·)$, elementwise cross entropy as $L_R(·, ·)$, and masking noise as $q(·|·)$. We train the model, $\theta = {W ,W′, b, b′}$, by using mini-batch stochastic gradient descent (SGD).
f(-)$として要素別シグモイド関数$sigma(x)_i = 1/(1+exp(-x_i))$, $L_R(-, -)$ として要素別クロスエントロピー, $q(-|-)$ としてマスキングノイズを使用する. ミニバッチ確率的勾配降下法(SGD)を用いて、モデル$thetta = {W ,W′, b, b′}$を学習させる。

We construct x˜ in the application phase by using constant decay, instead of stochastic corruption in the training phase, as:
応用段階では、学習段階での確率的な破損の代わりに、一定の減衰を用いて、x〜を次のように構成する。

$$
\tilde{x} = (1-p)x \\
h = f(W\tilde{x} + b) - f(b)
$$

where $p$ is the corruption rate in the training phase. Thus, $h$ is uniquely determined at the time of application. Multiplying $1 − p$ has the effect of equalizing the input distribution to each neuron in the middle layer between learning with masking noise and that without the application of this noise.
ここで、$p$は学習段階での破損率である。 したがって、$h$は適用時に一意に決定される。 $1 - p$を掛けると、マスキングノイズを適用した学習と適用しない学習とで、中間層の各ニューロンへの入力分布が等しくなる効果がある。

We use the $h$ generated above in three applications as the representation of the article: (i) to input the user-state function described in Section 4, (ii) to measure the relevance of the user and the article in matching, and (iii) to measure the similarity between articles in de-duplication.
上記で生成された$h$を記事の表現として3つの用途で用いる。 (i) セクション4で述べるユーザ状態関数の入力、(ii) マッチングにおけるユーザと記事の関連性測定、(iii) 重複排除における記事間の類似度測定である。

## 4. USER REPRESENTATIONS ユーザ表現

This section describes several variations of the method to calculate user preferences from the browsing history of the user. First, we formulate our problem and a simple word-based baseline method and discuss the issues that they have. We then describe some methods of using distributed representations of articles, as was explained in the previous section.
ここでは、ユーザの閲覧履歴からユーザの嗜好を算出する方法について、いくつかのバリエーションを説明する。 まず、我々の問題と単純な単語ベースのベースライン法を定式化し、それらが持つ問題点を議論する。 次に、前節で説明したように、記事の分散表現を利用するいくつかの方法について説明する。

### 4.1. Notation 数式の表記方法

Let $A$ be the entire set of articles. Representation of element $a \in A$ depends on the method. The $a$ is a sparse vector in the word-based method described in Section 4.2, and each element of a vector corresponds to each word in the vocabulary (i.e., $x$ in Section 3). However, $a$ is a distributed representation vector of the article (i.e., $h$ in Section 3) in the method using distributed representations described in Sections 4.3 and 4.4.
記事の全集合を$A$とする。 
$a \in A$の表現は手法に依存する。 
$a$ は4.2節で述べた単語ベースの手法ではスパースベクトルであり、ベクトルの各要素は語彙の各単語に対応する（すなわち、3節でいう$x$）。
しかし、セクション4.3および4.4で述べた分散表現を用いる方法では、$a$は記事の分散表現ベクトル（すなわち、セクション3における$h$）である。

Browse means that the user visits the uniform resource locator (URL) of the page of an article. Let ${a_t^u \in A}_{t=1,\cdots,T_u}$ be the browsing history of user $u \in U$.
**Browse(閲覧)とは、ユーザが記事のページのURL(Uniform Resource Locator)を訪問すること**である。 ここで、${a_t^u \in A}_{t=1,\cdots,T_u}$ を**ユーザ $u \in U$ の閲覧履歴**とする。

Session means that the user visits our recommendation service and clicks one of the articles in the recommended list.
Sessionとは、ユーザーが当社のレコメンデーションサービスにアクセスし、おすすめリストの記事をクリックすることを指します。

When $u$ clicks an article in our recommendation service (a session occurs), he/she will immediately visit the URL of the clicked article (a browse occurs). Thus, there is never more than one session between browses $a_t^u$ and $a^u_{t+1}$ ; therefore, this session is referred to as $s_t^u$ . However, $u$ can visit the URL of an article without our service, e.g., by using a Web search. Therefore, $s_t^u$ does not always exist.
u$は推薦サービスにおいて記事をクリックすると（セッションが発生）、すぐにクリックした記事のURLにアクセスする（ブラウズが発生）。したがって、$a_t^u$と$a^u_{t+1}$の間に複数のセッションが存在することはない；したがって、このセッションを$s_t^u$と呼ぶ。 しかし、$u$は我々のサービスを使わずに、例えばウェブ検索を使って記事のURLを訪れることができる。したがって、$s_t^u$は常に存在するとは限らない。

Since a session corresponds to the list presented to $u$, we express a session, $s^u_t$, by a list of articles $s^u_{t,p} \in A_{p \in P}$. The notation, $P \subseteq N$, is the set of positions of the recommended list that is actually displayed on the screen in this session. Let $P_{+} \subseteq P$ be the clicked positions and $P_{-} = P \ P_{+}$ be non-clicked positions. Although $P$, $P_{+}$, and $P_{-}$ depend on $u$ and $t$, we omit these subscripts to simplify the notation. Figure 3 outlines the relationships between these notations.
セッションは$u$に提示されたリストに対応するので、セッション$s^u_t$を記事のリスト $s^u_{t,p}$ で表現する。 \のリストで表現する。 このとき、$P \subseteq N$という表記は、このセッションで実際に画面に表示される推奨リストの位置の集合である。 P_{+} \subseteq P$をクリックされた位置、$P_{-} = P \ P_{+}$を非クリックの位置とする。 P$、$P*{+}$、$P*{-}$は$u$、$t$に依存するが、表記を簡略化するためにこれらの添え字を省略する。 図3にこれらの表記の関係の概略を示す。

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/4-Figure3-1.png">

Figure 3: Browsing history and session
図3：閲覧履歴とセッション

Let $u_t$ be the user state depending on $a_1^u , \cdots, a_t^u$, i.e., $u_t$ represents the preference of $u$ immediately after browsing $a_t^u$. Let $R(u_t, a)$ be the relevance between the user state, $u_t$, and the article, $a$, which represents the strength of $u$’s interest in a in time t. Our main objective is to constitute user-state function $F(·, . . . , ·)$ and relevance function $R(·, ·)$ that satisfy the property:
u_t$を$a_1^u , \cdots, a_t^u$に依存するユーザ状態、すなわち$u_t$は$a_t^u$を閲覧した直後の$u$の嗜好を表すとする。 また、ユーザ状態$u_t$と記事$a$の関連性を$R(u_t, a)$とすると、時間tにおける$u$のaへの興味の強さを表す。この性質を満たすユーザ状態関数$F(-, ... , -)$と関連性関数$R(-, -)$を構成することが主目的である。

$$
u_t = F(a_1^u, \cdots, a_t^u) \\
\forall{s_t^u} \forall{p_{+}} \in P_{+} \forall{p_{-}}
\in P_{-} R(u_t, s_{t,p_{+}}^u) > R(u_t, s_{t, p_{-}}^u). \\
\tag{2}
$$

($\forall$は"任意の、全称記号"を表す論理記号。全称量化子とも呼ばれる。)
($\forall$ is a logic symbol for "any, all symbol". Also called the full-symmetry quantifier)

When considering the constrained response time of a real news distribution system with large traffic volumes, $R(·, ·)$ must be a simple function that can be quickly calculated. Because candidate articles are frequently replaced, it is impossible to pre-calculate the relevance score, $R(u_t, a)$, for all users ${u_t |u \in U }$ and all articles ${a \in A}$. Thus, it is necessary to calculate this in a very short time until the recommended list from visiting our service page is displayed. However, we have sufficient time to calculate the user state function, $F (·, \cdots, ·)$, until the next session occurs from browsing some article pages.
u \in U }$ and all articles ${a \in A}$. Thus, it is necessary to calculate this in a very short time until the recommended list from visiting our service page is displayed. However, we have sufficient time to calculate the user state function, $F (·, \cdots, ·)$, until the next session occurs from browsing some article pages.

$$
\sum_{s_t^u} \sum_{p_{+} \in P_{+}, p_{-} \in P_{-}} 
- \frac{
    \log (\sigma(R(u_t, s_{t, p_{+}}^u) - R(u_t, s_{t,p_{-}}^u)))
}{
    |P_{+}||P_{-}|
}
$$
