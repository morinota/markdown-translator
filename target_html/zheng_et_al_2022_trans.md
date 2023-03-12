## 0.1. title 0.1. タイトル

Evaluating urban heat island mitigation strategies for a subtropical city centre (a case study in Osaka, Japan)

## 0.2. abstruct 0.2. abstruct

Urban heat island (UHI) effects were first observed in London in the 19th century.
都市部のヒートアイランド（UHI）効果は、19世紀にロンドンで初めて観測されました。
The urban heat island is identified by developing higher temperatures in urban areas than the surrounding rural areas that directly surround them.
都市部のヒートアイランドは、都市部を直接取り囲む周辺の農村部よりも高い気温を発生させることで確認されています。
However, there are some main mitigation strategies to deal with subtropical UHI, such as increasing the albedo of the urban environment (reflective pavement) and developing the green infrastructure (green roof) in urban areas.
しかし、亜熱帯UHIの緩和策として、都市環境のアルベドを高める（反射性舗装）、都市部のグリーンインフラを整備する（屋上緑化）などが主に挙げられる。
This study would analyse the microclimate in a subtropical city by evaluating meteorological parameters with a three-dimensional model simulation software of computational fluid dynamics (CFD) named ENVI-Met.
本研究では、ENVI-Metという数値流体力学（CFD）の3次元モデルシミュレーションソフトウェアを用いて、気象パラメータを評価することにより、亜熱帯都市の微気候を解析するものである。

To evaluate Urban Heat Island mitigation strategies for a Subtropical City Centre, subtropical city Osaka, Japan, is selected to investigate UHI with modelling.
亜熱帯都市における都市ヒートアイランド軽減策を評価するために、亜熱帯都市大阪を選び、モデリングによるUHIを調査した。
The simulation has been used to applicate the five scenarios (base scenario, cool pavement scenario, cool roof scenario, increasing vegetation coverage scenario, and integrated scenario) with different albedo and vegetation coverage ratios.
シミュレーションでは、アルベドと植生被覆率の異なる5つのシナリオ（基本シナリオ、涼しい舗装シナリオ、涼しい屋根シナリオ、植生被覆率の増加シナリオ、統合シナリオ）を適用している。
In this study, outdoor air temperature, sky view factor, net radiation, mean radiant temperature and thermal radiative power are considered as five criteria for evaluating the efficiency of UHI mitigation strategies.
本研究では、UHI軽減戦略の効率性を評価するための5つの基準として、外気温度、上空視界係数、純放射、平均放射温度、熱放射パワーを考慮した。
The simulation results of the base model (scenario A) with Osaka's current condition are considered the reference value.
大阪の現状を考慮したベースモデル（シナリオA）のシミュレーション結果を基準値とした。
The relative percentage differences between each scenario with a base model are determined.
各シナリオとベースモデルとの相対的な差分を求めた。
The increased albedo of urban fabric material (scenario B Cool pavement model) showed the most efficient to mitigate UHI.
都市ファブリック材のアルベドを増加させること（シナリオ B クール舗装モデル）は、UHI を軽減するために最も効果的であることが示された。
The relative percentage differences of the five criteria in the Cool pavement model are more significant than other models.
Cool pavement モデルにおける 5 つの基準の相対的なパーセンテージの差は、他のモデルよりも有意であった。
Therefore, the results of this study can provide valuable guidance, both for keeping subtropical residents cooler and informing subtropical climate cities that would be sustainable in the future.
したがって、本研究の結果は、亜熱帯の住民を涼しく保つため、また将来的に持続可能な亜熱帯気候の都市に情報を提供するための貴重なガイダンスとなり得る。

# 1. Introduction 1. はじめに

The Urban Heat Island (UHI) occurs when a city metropolitan area experiences higher temperatures than the surrounding rural areas, which directly surrounds them [1].
都市部のヒートアイランド（UHI）は、都市部の大都市圏が、その周囲を直接取り囲む農村部よりも気温が高くなることで発生します[1]。

The 2018 Revision of World Urbanization Prospects [2] noted that the urban population of the world had proliferated from 751 million in 1950 to 4.2 billion in 2018.
2018 Revision of World Urbanization Prospects[2]では、世界の都市人口が1950年の7億5100万人から2018年には42億人に増殖したことが指摘されています。
The increasing urban population contributes to the development of new mega-cities and the existing mega-cities becoming more populated.
都市人口の増加は、新たなメガシティの発展や既存のメガシティの人口増加に寄与しています。
Most of these mega-cities that have the largest population situate in tropical and subtropical areas.
これらのメガシティの多くは、熱帯・亜熱帯地域に位置し、人口が多い。
Therefore, it is essential for investigating the subtropical UHI phenomenon.
そのため、亜熱帯のUHI現象を解明することが重要である。
There are several causes of the UHI effect in subtropical urban areas, including: (i) urbanization and increasing population [3]; (ii) fewer green spaces in the urban area [4]; (iii) low albedo construction materials in the urban area [5].
亜熱帯都市部におけるUHI現象の原因としては，(i) 都市化と人口増加 [3] ，(ii) 都市部における緑地の減少 [4] ，(iii) 都市部における低アルベド建材 [5] などがある．

This research would analyse the microclimate changing and UHI mitigation strategies in a subtropical city centre (Osaka) in Japan.
本研究は、日本の亜熱帯都市（大阪）の微気候の変化とUHI軽減策を分析するものである。
A three-dimensional model simulation software of computational fluid dynamics (CFD) named ENVI-Met (V 5.0.1) is adopted to visualise research results.
研究結果の可視化には、ENVI-Met (V 5.0.1) という数値流体力学 (CFD) の3次元モデルシミュレーションソフトウェアを採用した。
The designed models employed to simulate thermal interactions between the built-up areas – vegetation – atmosphere condition on a micro-scale perspective and outdoor human thermal comfort is explored by ENVI-Met [6].
ENVI-Met [6]は、マイクロスケールでの建築物-植生-大気の熱的相互作用と屋外の人間の熱的快適性をシミュレートするために設計されたモデルを使用しています。

In this research, five scenarios (Base scenario, Cool pavement scenario, Cool roof scenario, increasing vegetation coverage scenario, and integrated scenario) with different albedo and vegetation coverage ratios have been designed to investigate the local climate changing under the UHI phenomenon in Osaka city centre.
本研究では、大阪都心部におけるUHI現象による地域気候の変化を調べるために、アルベドと植生被覆率の異なる5つのシナリオ（基本シナリオ、クールペイブメントシナリオ、クールルーフシナリオ、植生被覆率増加シナリオ、統合シナリオ）を作成した。
The five scenarios have been simulated by ENVI-Met.
5つのシナリオは、ENVI-Metによってシミュレーションされた。
The simulation results of Scenario A (Base model) are considered the reference value.
シナリオA（ベースモデル）のシミュレーション結果を参照値とした。
The five criteria (outdoor air temperature, sky view factor, net radiation, mean radiant temperature and thermal radiative power) are considered standard for evaluating the efficiency of UHI mitigation strategies.
5つの基準（外気温度、スカイビューファクター、純放射量、平均放射温度、熱放射パワー）は、UHI軽減戦略の効率性を評価するための標準とみなされる。
According to the simulation results and discussion, Scenario B has the ability to approximate decrease the outdoor air temperature (10% in summer, 20% in winter); net radiation (40% in summer, 20% in winter; Thermal radiative power (50%in summer, 40% in winter) and thermal radiant temperature (10% in summer, 80% in winter).
シミュレーション結果と考察によると、シナリオBは、外気温度（夏10%、冬20%）、正味放射量（夏40%、冬20%）、熱放射電力（夏50%、冬40%）、熱放射温度（夏10%、冬80%）をおおよそ減少させる能力があることがわかった。
Therefore, an increasing albedo of urban pavement is the most efficient mitigation strategy to manage UHI in a subtropical city.
したがって、都市舗装のアルベドを増加させることは、亜熱帯都市におけるUHIを管理するための最も効率的な緩和策である。

# 2. Literature review 2. 文献調査

## 2.1. The main mitigation strategies of subtropical UHI 2.1. 亜熱帯UHIの主な軽減策

Mitigation techniques of subtropical UHI aim to balance the thermal budget of urban areas by increasing thermal losses and decreasing the corresponding gains [7].
亜熱帯UHIの緩和技術は、熱損失を増加させ、対応する利 益を減少させることによって、都市部の熱収支のバランスをとるこ とを目的としている[7]。
For dissipating the excess heat, the mitigation strategies of UHI are usually divided into two categories: increasing urban albedo and increasing evapotranspiration.
過剰な熱を放散するために、UHIの緩和戦略は通常、都市のアルベドを増やすことと蒸発散を増やすことの2つのカテゴリーに分けられる。
Increasing albedo is generally accomplished by increasing the albedo of the roof and pavement.
アルベドを増加させることは，一般に屋根や舗道のアルベドを増加させることによって達成される．
An increase in evapotranspiration is performed by a combination of decreasing the distribution of impervious surfaces and expanding the space of vegetation in urban areas (shade trees, vegetated walls, and rooftop gardens [8].
蒸発散量の増加は、不浸透面の分布を減少させることと、都市部における植生の空間（日陰樹、植生壁、屋上庭園）を拡大することの組み合わせによって行われる[8]。
All mitigation strategies constitute common relationships between energy and water cycles, environmental and socioeconomic measures, human activities and natural systems.
すべての緩和戦略は、エネルギーと水の循環、環境と社会経済的措置、人間活動と自然システムとの間の共通の関係を構成している。

## 2.2. Green infrastructure 2.2. グリーンインフラ

With subtropical climate conditions, the green roof can effectively mitigate UHI in Xiamen, China [9].
亜熱帯気候の条件下では，中国の厦門でグリーンルーフが効果的にUHIを軽減することができます[9]．
This research adopted high-resolution remote sensing images to collect the data for land use and land surface temperatures (LST) in Xiamen from 2014 to 2017.
本研究では，高解像度リモートセンシング画像を採用し，2014年から2017年までの厦門の土地利用および地表温度（LST）のデータを収集した。
Besides, Landsat 8 remote sensing data (column number: 119,043) were selected to invert the LST.
その上、LSTを反転させるためにLandsat 8リモートセンシングデータ（列番号：119,043）が選択された。
This research showed that the average LST difference between green roofs and Xiamen Island decreased by 0.91 °C.
この研究により、グリーンルーフと厦門島のLSTの差は平均0.91℃減少したことが分かった。
Besides, regression analysis revealed that for every 1000 m^2 increase in the green roof area, the average LST of the roof decreased by 0.4 °C.
その上、回帰分析の結果、屋上緑化の面積が1000m^2増加するごとに、屋上の平均LSTは0.4℃減少することが明らかになった。

The cool roofs and urban forestry also can mitigate UHI in Phoenix, USA [10].
米国フェニックスでは，涼しい屋根と都市林業もUHIを軽減することができる[10]．
Under current climate conditions, this study assessed the UHI mitigation strategies on daytime microclimate for a pre-monsoon summer day.
本研究では，現在の気候条件の下で，モンスーン前の夏の日中の微気候に対するUHI緩和策を評価した．
They designed two climate scenarios by using the microclimate model ENVI-met.
彼らは、微気象モデルENVI-metを使用して、2つの気候シナリオを設計した。
The results showed that the relationship between per cent canopy cover and air temperature is linear, with a 0.14 °C cooling per cent increase in tree cover for the urban.
その結果、樹冠被覆率パーセントと気温の関係は線形であり、都市部では樹冠被覆率パーセントの増加で0.14℃の冷却が可能であることがわかった。
An increase in tree canopy cover from the current 10%–25% resulted in an average daytime cooling benefit of up to 2.0 °C at a local scale.
樹冠被覆率を現在の10%～25%から増加させると、局所的なスケールで日中の平均冷却効果が最大2.0 °Cとなった。
Meanwhile, cool roofs reduced air temperature by 0.3 °C.
一方、涼しい屋根は気温を0.3 °C下げることができた。

Besides, the differences in air temperature in Hong Kong have been simulated between extensive green roofs (EGR) and intensive green roofs (IGR) [11].
また，香港では，広範緑化屋根（EGR）と集約緑化屋根（IGR）の間の気温の違いもシミュレーションされている[11]．
This research showed that EGR decreased air temperature by 0.4–0.7 °C, and IGR decreased by 0.5–1.7 °C.
この研究では、EGRは0.4-0.7℃、IGRは0.5-1.7℃気温を低下させることが示された。
However, this research also presented that the cooling effect merely distributes in high-density buildings.
しかし、この研究は、高密度の建物では冷却効果が単に分散しているだけであることも示している。
Although of limited value, the GR still can mitigate UHI in subtropics, and the cooling effect of EGR is more visible in open-set low rise buildings.
GRは亜熱帯のUHIを軽減することができ、EGRの冷却効果は開放型低層建物でより顕著である。

## 2.3. Cool pavements with advanced higher albedo materials 2.3. 先進の高アルベド素材によるクール舗装

The effect of pavements has been quantified on the urban thermal environment in Phoenix, the USA, at multiple scales [12].
米国フェニックスでは，舗装が都市の熱環境に与える影 響を複数のスケールで定量化している[12]．
A developed urban canopy model (UCM) was implemented into the WRF model (version 3.4.1).
開発された都市キャノピーモデル（UCM）は，WRF モデル（バージョン 3.4.1）に実装された．
They evaluated the effect of pavements on the road and wall surface temperatures in Phoenix was investigated to identify the importance of thermal interactions between building–environment thermal interactions.
彼らは，建物-環境間の熱的相互作用の重要性を明らかにするために，フェニックスにおける道路と壁の表面温度に対する舗装の影響を評価した．
The initial meteorological data for the simulation were collected from the National Centres for Environmental Predication Final Operational Global Analysis data.
シミュレーションのための初期気象データは、National Centres for Environmental Predication Final Operational Global Analysisのデータから収集した。
The sunny pre-monsoon period (12–17 June 2012) was used.
晴天のプレモンスーン期間（2012 年 6 月 12 日～17 日）を使用した．
To assess the performance of pavements, the researchers assumed that the road surface was 100% pavement with no trees or vegetation.
舗装の性能を評価するため、研究者は、路面が100%舗装で、樹木や植生がないものと仮定しました。
The results showed that an increased albedo (0.6) of the pavement led to a pavement surface temperature reduction of up to 20 °C in the daytime.
その結果、舗装のアルベド（0.6）が増加すると、日中の舗装表面温度が最大で20℃低下することが分かりました。
In most of the diurnal cycle, the reflective pavement led to the cooling of wall surface temperatures.
日周期の大部分において、反射性舗装は壁面温度の冷却につながった。
The maximum cooling effect of about 1.9 °C occurred at 21:00 local time.
最大で約1.9 °Cの冷却効果が現地時間21時に発生しました。
This study revealed the importance of building-environment thermal interactions in determining thermal conditions inside the urban canopy.
この研究により、都市キャノピー内の温熱環境を決定する上で、建物と環境の熱的相互作用が重要であることが明らかになりました。

Furthermore, a new permeable pavement structure called evaporation-enhancing permeable pavement has been assessed for UHI mitigation [13].
さらに，蒸発促進透水性舗装と呼ばれる新しい透水性舗装の構造が，UHI軽減のために評価されている[13]．
The new pavement has capillary columns in aggregate and a liner at the bottom of the pavement.
この新しい舗装は、骨材に毛細管カラムがあり、舗装の底にライナーがあります。
Results showed that the capillary column was crucial in increasing evaporation by lifting water from the bottom to the surface, and the evaporation-enhancing permeable pavement was cooler than a conventional permeable pavement by 9.4 °C.
その結果，毛細管カラムが底面から表面へ水を持ち上げることによって蒸発量を増加させるのに重要であり，蒸発量を増加させた透水性舗装は従来の透水性舗装よりも 9.4 ℃涼しくなったことがわかった．
Statistical analysis result reveals that evaporation-enhancing permeable pavement can mitigate the UHI effect significantly more than conventional permeable pavement.
統計解析の結果、蒸発促進透水性舗装は従来の透水性舗装よりも有意にUHIの影響を緩和できることが明らかになった。

## 2.4. Integrated strategy 2.4. 統合戦略

The integrated urban planning and design strategies have been investigated to mitigate UHI using multi-sourced open satellite data [14].
UHIを軽減するための統合的な都市計画・設計戦略が、マルチソーシングのオープン衛星データを用いて研究されている[14]。
The researchers adopted the local climate zone scheme to classify the two urban cities (Guangzhou, Hong Kong, China) based on the urban features such as building morphology and land cover.
研究者は、建物の形態や土地被覆などの都市の特徴に基 づいて、2つの都市（広州、香港、中国）を分類するために、局所 気候帯スキームを採用した。
The results of the experiment indicated significant LST differences between pairs of local climate zones (LCZs).
実験の結果，局所気候帯（LCZ）の組の間でLSTに有意な差があることが示された．
Compared with other LCZs, high density urban LCZs tended to have higher surface temperatures, while natural LCZs with a large percentage of vegetation have lower LSTs.
他のLCZと比較して、高密度都市LCZは地表温度が高くなる傾向があり、植生の割合が多い自然LCZはLSTが低くなることがわかった。
The study provided that urban design is a fast and efficient way to mitigate UHI in a subtropical city.
本研究は、亜熱帯都市におけるUHIを緩和するために、都市設計が迅速かつ効率的な方法であることを提供した。

Moreover, the urban configuration has been indicated that could influence the local thermal environment and mitigate UHI [15].
さらに，都市の形態が地域の熱環境に影響を与え，UHIを軽減する可能性があることが指摘されている[15]．
This research quantified the UHII in subtropical cities in China from Landsat 8 by using Moderate Resolution Imaging Spectroradiometer (MODIS) LST.
本研究では，中分解能撮像分光放射計（MODIS）LSTを用いて，Landsat 8から中国の亜熱帯都市におけるUHIIを定量的に評価した．
The results showed that a lower UHI occurred in the smaller built-up area with dispersed distribution when compared to the larger built-up areas.
その結果，分散して分布する小規模な既成市街地では，大規模な既成市街地と比較してUHIが低いことが示された．
Besides, the urban configuration can influence UHI by 41% on a summer day and 51% on a summer night.
また、都市形態はUHIに夏の日中に41%、夏の夜間に51%の影響を与えることがわかった。
Therefore, the design of urban configuration is an effective strategy to mitigate UHI.
したがって、都市配置の設計はUHIを軽減するための効果的な戦略である。

## 2.5. Summary of the leading mitigation strategies in subtropical cities 2.5. 亜熱帯都市における主要な緩和策の概要

Existing studies have concluded that many variables can affect the performance of mitigation strategies in subtropical UHI, such as the height and species of vegetation, leaf canopy cover of vegetation, the green coverage ratio of vegetation; the colour and density of surface; and the albedo value of building materials.
既存の研究では、植生の高さや種類、葉の被覆率、植生の緑被率、地表の色や密度、建築材料のアルベド値など、多くの変数が亜熱帯UHIの緩和戦略の性能に影響を与えることが結論付けられている。
Regarding the performance of mitigation strategies in subtropical UHI, the efficient mitigation strategies have been understood the key issues, such as air temperature reduction, land surface temperature reduction; energy saving; and thermal comfort improvement.
亜熱帯UHIの緩和策の性能については、大気温度低下、地表面温度低下、省エネルギー、熱的快適性の向上など、効率的な緩和策が重要な課題として理解されてきた。

# 3. Background of the research area (osaka, Japan) 3. 調査地域の背景（大阪府大阪市）

## 3.1. Study area 3.1. 研究領域

The study area is selected in Osaka, Japan, located in the subtropical area at latitude 34.6937° N and longitude 135.5023°E.
調査地域は、北緯34.6937°、東経135.5023°の亜熱帯地域に位置する日本の大阪府を選んだ。
In Osaka, the annual mean maximum air temperature is 20.08 °C, the mean annual air temperature is 15.9 °C, and the mean annual minimum is 11.75 °C.
大阪の年平均最高気温は 20.08 ℃、年平均気温は 15.9 ℃、年平均最低気温は 11.75 ℃である。
The annual relative humidity of Osaka is 65.3%.
大阪の年間相対湿度は65.3%である。
The annual average wind speed in Osaka is 4.5 m
大阪の年間平均風速は4.5mです。

The research domain for the urban microclimate modelling covers an area of 2.5 km^2, which comprised the Chuo Ward and the surrounding area.
都市微気候のモデリングを行う研究領域は、中央区とその周辺地域からなる2.5 km^2の範囲です。
This domain consists of typical urban land-use types: residential area, commercial area, industrial areas, roads, parks and open spaces.
この領域は、住宅地、商業地、工業地、道路、公園、空き地など、典型的な都市の土地利用タイプで構成されています。

## 3.2. Urban ground surface 3.2. 都市部の地表

The fraction of urban green coverage (UGC) in Osaka is under 9%, about 2% in the city centre.
大阪の都市緑地面積（UGC）は9％未満で、市街地では約2％である。
Increasing vegetation contributes to mitigating the UHI in several ways, such as intercepting solar energy and reducing the temperature of surfaces below while increasing the latent heat exchange for the evapotranspiration process [17].
植生を増やすことは、太陽エネルギーを遮断し、蒸発散プロセスのための潜熱交換を増加させながら、下の表面の温度を下げるなど、いくつかの方法でUHIを軽減することに貢献する[17]。
Besides, asphalt and concrete constitute most of Osaka urban surface area.
さらに，大阪の都市部の表面積の大部分は，アスファルトとコンクリートで占められている．
Asphalt and concrete have a low albedo, with values as low as 0.1 on average for asphalt and 0.3 for concrete.
アスファルトとコンクリートはアルベドが低く，アスファルトの平均値は 0.1， コンクリートの平均値は 0.3 である．
As a UHI mitigation strategy, surface materials with high albedo and emissivity have been proposed worldwide since they remain cooler when exposed to solar energy [7].
UHIの緩和策として、アルベドや放射率の高い表面材は、太陽エネルギーを受けても涼しいため、世界的に提案されている[7]。

# 4. Method 4. 方法

## 4.1. Software and 3D model 4.1. ソフトウェアと 3D モデル

This research uses the simulation approach to analyse the UHI mitigation strategies in subtropical climate zones.
本研究では、シミュレーションの手法を用いて、亜熱帯気候帯における UHI の緩和策を分析する。
ENVI-met (version5.0.1) is a 3D software designed to explore microclimates by the fundamental standards of fluids and thermodynamics.
ENVI-met (version 5.0.1) は，流体と熱力学の基本的な基準によって微気候を探索するために設計された 3D ソフトウェアである．
It can simulate thermal interactions between building areas, soil, vegetation and atmosphere condition [18,19].
このソフトは，建築物，土壌，植生，大気条件間の熱的相互作用をシミュレートすることができる[18,19]．
In numerical methods, ENVI-met uses an orthogonal Arakawa C-grid to represent its environment, and it adopts the finite difference method to solve a lot of partial differential equations (PED) and other aspects in the model.
ENVI-met は，数値計算方法として，直交する荒川C格子を用いて環境を表現し，モデル内の多くの偏微分方程式（PED）などを解くために有限差分法を採用している．
Therefore, ENVI-met only permits linear and rectangular structures (ENVI-met.info.com), and all the building structures are simplified to straight and rectangular in this study for easy simulation.
そのため，ENVI-met は直線的で長方形の構造物しか許可しておらず（ENVI-met.info.com），本研究ではシミュレーションを容易にするために，すべての建築構造を直線と長方形に簡略化しています．

In particular, ENVI-met simulation is suitable for the subtropical city centres.
特に、ENVI-metシミュレーションは、亜熱帯の都市中心部に適している。
A study is conducted in Hong Kong China [20] that demonstrated the proper tree planning is able to mitigate UHI effectively during daytime by using ENVI-met simulation.
中国の香港で行われた研究[20]では、ENVI-metシミュレーションを使用して、適切な樹木計画が日中のUHIを効果的に軽減できることが実証されている。
Besides, ENVI-met can calibrate the subtropical city São Paulo, Brazil [6] by combining land use data and field campaigns, microclimate measurements.
さらに、ENVI-met は、土地利用データとフィールドキャンペーン、微気候測定値を組み合わせることで、ブラジルの亜熱帯都市サンパウロのキャリブレーションを行うことができる[6]。
Moreover, Shanghai China as a case study is validated ENVI- met software is still a helpful tool for modelling microclimate in the subtropical city centre [21].
さらに、中国上海の事例では、ENVI-metが亜熱帯都市中心部の微気候のモデリングに有用なツールであることが検証されています[21]。
Fig. 1 shows the research location (Chuo Ward) in Osaka, Japan.
図1は、日本の大阪市中央区にある研究場所です。
The 3D model represents the base situation of the research area in ENVI-met.
3Dモデルは、ENVI-metにおける調査地の基本状況を表しています。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr1.jpg)

Fig. 1.
図1.
The research area (Chuo Ward) in Osaka, Japan and its 3D model in ENVI-met.
大阪の研究エリア（中央区）とENVI-metによる3Dモデル。

## 4.2. Parameters set in the ENVI-met simulation 4.2. ENVI-metシミュレーションで設定されたパラメータ

The meteorological parameters are collected from Japan Meteorological Agency (JMA).
気象パラメータは気象庁から収集したものである。
A typical hottest summer day (05
典型的な夏の猛暑日(05

Table 1.
表1.
The initialisation detailed input parameters for Osaka, adopted by the Japan Meteorological Agency.
気象庁が採用した大阪の初期化詳細入力パラメータ。

## 4.3. Simulation model design in Osaka 4.3. 大阪でのシミュレーションモデル設計

To compare the efficiency of different UHI mitigation strategies in Osaka.
大阪における様々なUHI軽減戦略の効率性を比較すること。
Five scenarios (A-E) have been considered (see Table 2):
5 つのシナリオ（A-E）が検討された（表 2 参照）。

Table 2.
表 2.
Details of the input set in the simulation models for different scenarios.
異なるシナリオのシミュレーションモデルで設定された入力の詳細。

Scenarios A: Base model:
シナリオA：ベースモデル。
The current condition with the albedo of asphalt roads and concrete roof are 0.1 and 0.2, respectively.
ベースモデル：アスファルト道路とコンクリート屋根のアルベドがそれぞれ0.1、0.2である現状を想定している。
Besides, the green coverage ratio is 2%.
また、緑被率は2％である。

Scenarios B: Cool pavement model: dark asphalt roads (albedo = 0.1) are replaced by concrete pavement (light white cement concrete) with higher surface albedo (0.8) and lower heat capacity (the emissivity is 0.9).
シナリオB：クールペイブメントモデル：暗いアスファルト道路（アルベド＝0.1）を、表面アルベド（0.8）が高く、熱容量（放射率）が小さいコンクリート舗装（明るい白色セメントコンクリート）に置き換えたモデル。

Scenarios C: Cool roof model: dark concrete roof (albedo = 0.2) are changed to high reflective roof (albedo = 0.8, emissivity = 0.9).
シナリオC：クールルーフモデル：暗いコンクリート屋根（アルベド＝0.2）を高反射率屋根（アルベド＝0.8、放射率＝0.9）に変更したもの。

Scenarios D:
シナリオ D:
Greenspace model: increasing a vegetation coverage ratio to 20%.
緑地モデル：植生被覆率を 20%にする。
The parameters of trees are reported in Table 3.
樹木のパラメータは表 3 に報告されている。

Table 3.
表3.
Parameters of trees in each scenario.
各シナリオにおける樹木のパラメータ。

Scenarios E: Integrated model: a combination of the three previous UHI mitigation strategies (Scenarios B, C and D).
シナリオE：統合モデル：これまでの3つのUHI緩和策（シナリオB、C、D）を組み合わせたもの。

# 5. Simulation results and discussion 5. シミュレーション結果と考察

In this study, outdoor air temperature ($T_a$), Sky view factor (SVF), Net radiation ($R_{n}$), thermal radiative power (TRP) and Mean radiant temperature ($T_{mrt}$) are standards for evaluating the efficiency of urban heat island mitigation strategies in the subtropical city centre.
本研究では、亜熱帯都市中心部のヒートアイランド緩和戦略の効率性を評価するために、外気温度（$T_a$）、スカイビューファクター（SVF）、ネット放射（$R_{n}$）、熱放射パワー（TRP）、平均放射温度（$T_{mrt}$）を基準値とする。
The simulation results of Scenario A (base model) is considered as the reference value.
シナリオA（ベースモデル）のシミュレーション結果を基準値とした。
Scenario B (Cool pavement model), C (Cool roof model), D (Greenspace model) and E (Integrated model) have been compared with Scenario A to determine the relative percentage difference.
シナリオB（涼しい舗装モデル）、C（涼しい屋根モデル）、D（緑地モデル）、E（統合モデル）は、シナリオAと比較され、相対的なパーセント差が決定された。
The positive percentage difference represents which scenario has the positive ability to mitigate subtropical UHI.
この差は、どのシナリオが亜熱帯UHIを軽減する能力が高いかを示している。

## 5.1. Outdoor air temperature ($T_a$) and distributions 5.1. 外気温度 ($T_a$) とその分布

Fig. 2 shows the change in outdoor air temperature ($T_a$) during the research period for each scenario.
図2は、各シナリオの調査期間中の外気温度の変化（$T_a$）を示したものである。
The maximum, average, and minimum outdoor air temperature are $T_{a-max}, T_{a-avg}$, and $T_{a-min}$ for the five scenarios, respectively.
最高外気温度、平均外気温度、最低外気温度は、それぞれ5つのシナリオの$T_{a-max}、T_{a-avg}$、$T_{a-min}$である。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr2.jpg)

Fig. 2.
図2.
The change of $T_{a-max}$, $T_{a-avg}$, and $T_{a-min}$ during the research period for each simulated scenario.
各シミュレーションシナリオの研究期間中の$T_{a-max}$, $T_{a-avg}$, $T_{a-min}$の変化を示す。

In the summertime, the maximum $T_{a-max}$ of Scenario A is 35.46 °C, which is close to the record temperature from the meteorological station.
夏期において、シナリオ A の最大 $T_{a-max}$ は 35.46 ℃であり、気象台の記録温度に近い。
The maximum $T_{a-max}$ (45.64 °C) from all scenarios is observed at 12:00 in Scenario E during the research period.
研究期間中、シナリオ E では 12 時に全シナリオの中で最大の $T_{a-max}$ (45.64 ℃) が観測されている。
Scenario B has the lowest $T_{a-max}$ (33.24 °C), which is the most decreased model.
シナリオ B では、$T_{a-max}$ が最も小さく (33.24 ℃) 、最も減少したモデルであることがわかる。
In the wintertime, the maximum Ta is found in Scenario A at 14:00, and the value is 15.21 °C.
冬期には、シナリオ A で 14:00 に最大 Ta が得られ、その値は 15.21 ℃である。
The minimum $T_{a-max}$ (13.09 °C) have been found in Scenario B at 18:00.
また、シナリオ B では 18 時に $T_{a-max}$ の最小値 (13.09 ℃) が得られている。
Besides, the distribution of $T_a$ are analysed in this research.
さらに、本研究では、$T_a$の分布も分析した。
Fig. 3 and Fig. 4 show the distribution of $T_{a-max}$, for each scenario in summertime and wintertime.
図3および図4は、夏期および冬期の各シナリオにおける $T_{a-max}$ の分布を示している。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr3.jpg)

Fig. 3.
図3.
The distribution of $T_{a-max}$ for each scenario in the summertime.
夏期における各シナリオの $T_{a-max}$ の分布.

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr4.jpg)

Fig. 4.
図 4.
The distribution of $T_{a-max}$ for each scenario in the wintertime.
冬期における各シナリオの $T_{a-max}$ の分布.

Scenario B has the higher temperature distribution inside the buildings and the lower temperature outside and around the street.
シナリオ B は、建物内の温度分布が高く、屋外や道路周辺の温度が低くなっている。
However, scenario E has the highest temperature distribution inside the buildings but higher temperatures around the road and outside the buildings.
しかし、シナリオ E は、建物内の温度分布が最も高く、道路周辺と建物外の温度が高くなる。

Fig. 5 shows the relative percentage difference of outdoor air temperature compared with Scenario A (base model).
図5は、シナリオA（ベースモデル）と比較した外気温度の相対的な差のパーセンテージを示したものである。
In the summertime, the percentages of $T_{a-max}$ significantly increased in Scenario B during the daytime, and it slightly increased during nighttime.
夏期において、$T_{a-max}$の割合は、昼間はシナリオBで著しく増加し、夜間はわずかに増加した。
Furthermore, the percentages of $T_{a-avg}$ and $T_{a-min}$ have been identified as the highest trend In Scenario C. This implies that Scenario B and Scenario C both are the great efficient model to decrease $T_{a}$ in the summertime.
さらに、$T_{a-avg}$と$T_{a-min}$の割合は、シナリオCで最も高い傾向が確認された。これは、シナリオBとシナリオCが、夏場の$T_{a}$の減少に非常に有効なモデルであることを示唆している。
However, in the wintertime, the most remarkable percentages tendency of the $T_{a-max}$, $T_{a-avg}$, $T_{a-min}$ have been found in Scenario B. It indicates that Scenario B has the more efficient ability to decrease $T_a$ in the wintertime.
しかし、冬期においては、$T_{a-max}$, $T_{a-avg}$, $T_{a-min}$の比率は、シナリオBで最も顕著な傾向が見られた。これは、シナリオBが冬期における$T_a$の減少に対してより有効な能力を持っていることを意味している。
Therefore, Scenario B can be considered as the most efficient model to reduce $T_a$ in summer and wintertime.
したがって、シナリオBは、夏期と冬期の$T_a$を減少させるのに最も効率の良いモデルであると考えることができる。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr5.jpg)

Fig. 5.
図5.
The percentages of outdoor air temperature in summer and wintertime.
夏期と冬期の外気温度の割合。

## Sky view factor 空の見え方係数

The Sky View Factor (SVF) is the fraction at a point in space between the visible sky and a hemisphere centred over the research location.
スカイビューファクター（SVF）とは，調査地点を中心とした半球と可視空との間の空間上の割合のことである．
The SVF serves as an index of urban morphology widely used for comparing thermal conditions in different building environments [22].
SVFは、都市形態の指標として、異なる建築環境における温熱条件の比較に広く用いられている[22]。
This study has set four locations to assess the SVF in simulation (Fig. 6).
本研究では、4つの場所を設定し、シミュレーションによるSVFの評価を行いました（図6）。
The average SVF for each simulated scenario is also shown in Fig. 6.
また、各シミュレーションシナリオの平均SVFも図6に示しています。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr6.jpg)

Fig. 6.
図6.
Four selected points to assess the SVF and the value of SVF in each scenario.
SVFを評価するために選択された4つのポイントと、各シナリオにおけるSVFの値。

The comparison of the SVF of each scenario showed that the highest average SVF had been found in Scenario B; the value is 0.31.
各シナリオの SVF を比較すると、シナリオ B の SVF が最も高く、0.31 という値であった。
The lowest SVF value is 0.15 in scenario E. According to Fig. 5, Scenario B has the highest SVF, decreasing net heat storage inside buildings and UHI.
図 5 によれば、シナリオ B が最も SVF が高く、建物内の正味の熱蓄積と UHI を減少させている。
Besides, adding urban shading provided by extra vegetation makes the lower SVF in scenarios D and E.
また、植栽による都市部の遮光を追加すると、シナリオDとEでSVFが低くなる。

## Net radiation ($R_n$) 純放射能 ($R_n$)

The value of net radiation ($R_n$) is the difference between incoming and outgoing radiation of both short and long wavelengths.
正味放射量（$R_n$）の値は、短波長および長波長の放射の入射と出射の差である。
It depends on the temperature and reflectivity of the ground surface exposed to radiative exchange [23]Error!
放射交換にさらされる地表の温度と反射率に依存する[23]Error!
Reference source not found.
Reference source not found.
.
.
Fig. 7 shows the change of net radiation ($R_n$) during the research period.
図 7 は、調査期間中の純放射量 ($R_n$) の変化を示したものである。
The maximum $R_n$ in summer time was found in Scenario A at 11:00, the value is 1936.01 W
夏時間における最大の$R_n$は、シナリオAの11:00に見られ、その値は1936.01Wであった。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr7.jpg)

Fig. 7.
図7.
The value of $R_n$ for each scenario in summer and wintertime.
夏期と冬期の各シナリオにおける$R_n$の値。

Fig. 8 shows the relative percentage difference of $R_n$, which compared with Scenario A. In the summer daytime, Scenario E is the most efficient model to decline $R_{n-max}$, Scenario B is the most powerful model to reduce $R_{n-min}$.
図8は、シナリオAと比較した$R_n$の相対差分です。夏の昼間は、シナリオEが最も効率的に$R_{n-max}$を減少させ、シナリオBが最も強力に$R_{n-min}$を減少させるモデルであることを示しています。
Furthermore, in the wintertime, Scenario B generally has the most significant trend to decrease the $R_{n-max}$ and $R_{n-min}$ during the research period.
さらに、冬期には、研究期間中に$R_{n-max}$と$R_{n-min}$を減少させるために、シナリオBが概して最も大きな傾向を示している。
To sum up, Scenario B is considered the most powerful model to reduce net radiation both in summer and wintertime.
以上のことから、シナリオBは、夏期、冬期ともに純放射量を減少させる最も強力なモデルであると考えられる。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr8.jpg)

Fig. 8.
図8.
The percentages tendency of net radiation.
純放射の割合の傾向。

## Thermal radiative power (TRP) 熱放射パワー (TRP)

The thermal radiative power (TRP) is used to assess the impact of the solar reflectance of a surface on the UHI effect [24].
熱放射パワー(TRP)は、表面の日射反射率がUHI効果に与える影響を評価するために用いられる[24]。
According to Stefan-Boltzmann law, the average TRP per $m^2$ of each element of urban surfaces in each scenario was calculated and shown in Fig. 9.
ステファン-ボルツマンの法則に従って、各シナリオにおける都市表面の各要素の$m^2$あたりの平均TRPを計算し、図9に示した。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr9.jpg)

Fig. 9.
図9.
The calculated average TRP per m^2 of each element of urban surfaces in each scenario.
各シナリオにおける都市表面の各要素の1m^2あたりの平均TRPの計算値。

In the summertime, the values of TRP in Scenario A and C were close during the research period.
夏期において、シナリオ A とシナリオ C の TRP は、調査期間中、近い値であった。
In Scenario D and E increased rapidly from 07:00 to 14:00, then decreased until 20:00.
シナリオ D と E では、07:00 から 14:00 まで急激に増加し、20:00 まで減少している。
The values of TRP in all scenarios are stable during the nighttime.
夜間は、全てのシナリオで TRP の値は安定している。
In the wintertime, Scenario B showed the lowest trend of the TRP values.
冬期は、シナリオ B が最も低い TRP 値の傾向を示している。
The values of TRP in Scenario C, D and E were close during the research period.
シナリオ C、D、E の TRP は、調査期間中、近い値を示している。

Fig. 10 shows the relative percentage difference of TRP, which is compared with Scenario A base model.
図 10 は、シナリオ A のベースモデルとの比較で、TRP の相対的なパーセンテージの違いを示している。
The highest percentage trend of TRP is determined in Scenario B in summer and wintertime.
夏期、冬期ともに、シナリオ B で TRP が最も高い割合で推移していることがわかる。
It means that Scenario B is the most efficient model to decrease thermal radiative power during the research period.
これは、シナリオBが研究期間中の熱放射パワーを減少させるのに最も効率的なモデルであることを意味している。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr10.jpg)

Fig. 10.
図10.
The percentages tendency of net radiation.
純放射の割合の傾向。

## Mean radiant temperature ($T_{mrt}$) 平均放射温度 ($T_{mrt}$)

Mean radiant temperature ($T_{mrt}$) can be utilised to assess the human thermal comfort by evaluating the sum of all short wave and longwave radiation fluxes absorbed by the human body [25].
平均放射温度（$T_{mrt}$）は、人体が吸収するすべての短波および長波放射束の合計を評価することによって、人間の熱的快適性を評価するために利用することができます[25]。
In this research, the following physiological data were assumed to calculate PET: male, 170 cm, 35 years old, and 70 kg.
本研究では，PETを計算するために，男性，170cm，35歳，70kgの生理学的データを仮定した。
Besides, the heat transfer resistance of summer clothes to be 0.5clo, and the activity is 80 W, almost 1.3 m. Mean radiant temperature ($T_{mrt}$) can be used to evaluate the human thermal comfort by assessing the sum of all short wave and longwave radiation fluxes absorbed by the human body.
また、夏服の熱伝達抵抗は0.5clo、活動量は80W、ほぼ1.3mとした。平均放射温度（$T_{mrt}$）は、人体が吸収する短波と長波の放射束の和を評価することにより、人間の熱的快適性の評価に用いることができます。
Fig. 11 shows the change of $T_{mrt-max}$, $T_{mrt-min}$ and $T_{mrt-avg}$ for the five scenarios.
図11は5つのシナリオの$T_{mrt-max}$, $T_{mrt-min}$と$T_{mrt-avg}$の変化を示したものである.

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr11.jpg)

Fig. 11.
図11.
The value of $T_{mrt-max}$, $T_{mrt-min}$ and $T_{mrt-avg}$ in the five scenarios.
5つのシナリオにおける$T_{mrt-max}$, $T_{mrt-min}$と$T_{mrt-avg}$の値を示す。

The maximum $T_{mrt-max}$ in the summertime of all scenarios was observed in Scenarios B at 15:00; the value is 69.29 °C.
夏期における $T_{mrt-max}$ の最大値はシナリオ B の 15:00 であり、その値は 69.29 ℃であった。
The minimum value (23.69 °C) of $T_{mrt-max}$ was found at 05:00 in Scenarios E. In the wintertime, the maximum $T_{mrt-max}$ has also been found in Scenarios B, the value is 54.98 °C.
また、シナリオ E では、5 時に $T_{mrt-max}$ の最小値 (23.69 ℃) が観測された。冬期には、シナリオ B で $T_{mrt-max}$ の最大値 (54.98 ℃) が観測されている。

Fig. 12 shows the relative percentage difference of $T_{mrt}$, which is compared with Scenario A (base model).
図12は、シナリオA（ベースモデル）と比較した$T_{mrt}$の相対的な差のパーセンテージを示したものである。
In the summertime, the stable percentages tendency indicated that $T_{mrt}$ has decreased insignificantly in Scenario C. Bedside, Scenario B has reduced percentages of $T_{mrt}$ in summer daytime, however, it has a significate increased $T_{mrt}$ in the summer nighttime.
夏期には、シナリオCの$T_{mrt}$は、安定した割合で減少している。ベッドサイドでは、シナリオBは、夏期の昼間には$T_{mrt}$の割合が減少するが、夏期の夜間には$T_{mrt}$が有意に増加することがわかる。
The results of $T_{mrt}$ reveals that Scenario B has the most efficient ability to decrease $T_{mrt}$ in the summer nighttime, however, it is unsuitable to decline $T_{mrt}$ in summer daytime.
T*{mrt}$の結果から、シナリオBは夏季夜間の$T*{mrt}$を最も効率的に減少させることができるが、夏季昼間の$T*{mrt}$の減少には不向きであることが明らかになった。
In the wintertime, the percentages of $T*{mrt-max}$ altered to peak during the afternoon winter time in each scenario.
冬期は、各シナリオとも$T_{mrt-max}$の割合が冬期午後をピークに変化する。
However, the percentages of $T_{mrt-max}$ are all negative during the morning and night time.
しかし、$T_{mrt-max}$の割合は、朝・夜間はすべて負である。
The results imply that all Scenario B, C, D and E can decrease $T_{mrt}$ in winter morning and night time.
このことから、シナリオB、C、D、Eは、いずれも冬季の朝晩の$T_{mrt}$を減少させることができることが示唆される。

![](https://ars.els-cdn.com/content/image/1-s2.0-S0360544222006247-gr12.jpg)

Fig. 12.
図12.
The percentage of mean radiant temperature in summer and wintertime.
夏期と冬期の平均放射温度に対する割合。

Scenario B has the highest negative percentages for reducing $T_{mrt}$ in the wintertime.
シナリオBは、冬期における$T_{mrt}$の低減率が最も高く、負の値であることがわかる。
It shows that $T_{mrt}$ is highest and reach the human comfort in Scenario B during the winter time.
このことから、シナリオBでは、冬期において$T_{mrt}$が最も高く、人間の快適性に到達することがわかる。
In summary, Scenario B is the best model to alter $T_{mrt}$ to achieve the higher human comfort during the summer daytime and night time.
以上のことから、シナリオBは、夏季の昼間と夜間に、より高い人間快適性を得るために$T_{mrt}$を変更するのに最適なモデルであると言える。

# Uncertainty of results and sensitive analysis 結果の不確実性と感度の高い分析

Nowadays, numerical modelling is a capable way to help researchers advance UHI mitigation strategies.
今日、数値モデリングは、研究者がUHI軽減戦略を進めるための有力な手段となっています。
ENVI-met has been widely used to support microclimate-sensitive planning.
ENVI-metは微気候に敏感な計画をサポートするために広く使用されています。
Besides, this research should describe the meaningful characteristics of natural objects.
さらに、この研究では、自然物の意味のある特性を記述する必要があります。
In the Osaka city scale, the modelling process aims to simplify representing the city by computational methods.
大阪市のスケールでは、モデリングプロセスは、計算手法によって都市を表現することを簡素化することを目的としています。
To ensure the certainty of simulation results, the simulation results of outdoor temperature ($T_a$) have been chosen to compare with the actual outdoor temperature organised by the local weather station and Japan Meteorological Agency (JMA).
シミュレーション結果の確実性を確保するために、外気温のシミュレーション結果（$T_a$）は、地元の気象台と気象庁によって組織された実際の外気温と比較するために選ばれたものである。
The average $T_a$ of the local weather station is 30.19 °C and the average simulation $T_a$ is 30.91°Cduring the research period.
気象台の平均気温は30.19℃、シミュレーションの平均気温は30.91℃であった。
The percentage difference is 2.35%, which is at a deficient level.
その差は2.35%であり、不足のレベルである。
Therefore, the simulation results can be considered relatively close and comparable to the real values.
したがって、このシミュレーション結果は、実測値に比較的近く、比較可能であると考えることができる。

Besides, according to the tutorials of ENVI-met (ENVI-met.com), the typical spatial resolution range is from 0.5 to 10 m. Sdeghat and Sharif (2022) studied that the modelled area is 280 × 510m, and the resolution is 5 m for simulating the urban heat island in Tehran, Iran [26].
その上、ENVI-metのチュートリアル（ENVI-met.com）によると、典型的な空間分解能の範囲は0.5から10mであり、SdeghatとSharif（2022）は、イランのテヘランにおける都市のヒートアイランドのシミュレーションでは、モデリング領域は280×510m、分解能は5mと研究しました [26]．
However, the research area in this study is 500 × 500, which is bigger and more complex.
しかし，本研究の研究領域は 500 × 500 であり，より大きく，より複雑である．
Therefore, this study has considered saving the computing cost and time and combining the previous studies, limiting the resolution and grid cells to 10 m.
そこで、本研究では、計算コストと時間を節約することを考え、先行研究を組み合わせ、解像度とグリッドセルを10mに限定した。

# Discussion, conclusion and further work 考察、結論、今後の課題

In this study, UHI mitigation strategies were assessed for a subtropical urban area.
本研究では、亜熱帯都市部におけるUHI緩和戦略を評価した。
The results can provide valuable guidance to develop the UHI mitigation strategies for keeping subtropical residents more suitable for citizens and informing subtropical climate cities that would be sustainable in the future.
この結果は、亜熱帯の住民をより市民に適した状態に保ち、将来的に持続可能な亜熱帯気候の都市を知らせるためのUHI緩和戦略を開発するための貴重なガイダンスを提供することができる。
The different mitigation strategies were analysed by a simulation ENVI-met.
異なる緩和戦略は、シミュレーションENVI-metによって分析された。
In this study, outdoor air temperature ($T_a$), sky view factor (SVF), Net Radiation ($R_n$), thermal radiative power (TRP) and mean radiant temperature () as urban heat island mitigation criteria are standards for evaluating the efficiency of UHI mitigation strategies.
本研究では、都市ヒートアイランド緩和基準として、外気温度（$T_a$）、スカイビューファクター（SVF）、ネット放射（$R_n$）、熱放射パワー（TRP）、平均放射温度（）をUHI緩和戦略の効率性を評価するための基準としている。
The simulation results of Scenario A (Base model) are considered as the reference value.
シナリオ A（ベースモデル）のシミュレーション結果を基準値としている。
The relative percentage differences between Scenario B, C, D, and E with Scenario A are determined.
シナリオ B、C、D、E とシナリオ A との差は、相対的な割合で決定される。
According to the simulation results and discussion, Scenario B can approximate decrease the outdoor air temperature (10% in summer, 20% in winter); net radiation (40% in summer, 20% in winter; thermal radiative power (50% in summer, 40% in winter) and thermal radiant temperature (10% in summer, 80% in winter).
シミュレーション結果と考察によると、シナリオ B は、外気温度（夏 10%、冬 20%）、純放射量（夏 40%、冬 20%）、熱放射パワー（夏 50%、冬 40%）、熱放射温度（夏 10%、冬 80%）をおおよそ減少させることができる。
Therefore, Scenario B (the Cool pavement model) is the most excellent ideal model to mitigate subtropical UHI.
したがって、シナリオB（Cool pavementモデル）は、亜熱帯UHIを緩和するための最も優れた理想的なモデルであると言える。

According to the results of this study, an increasing albedo of urban fabric material and an expanding vegetation coverage ratio both are efficient ways to mitigate UHI.
本研究の結果によれば、都市ファブリック材料のアルベドを増加させることと植生被覆率を拡大することは、いずれもUHIを軽減するための効率的な方法であることがわかった。
Besides, a growing albedo of urban fabric material (Scenario B Cool pavement model) is a better efficient mitigation strategy than increasing vegetation coverage ratio (Scenario D green space model) in the urban area.
また、都市布材のアルベドを増加させること（シナリオB Cool pavementモデル）は、植生被覆率を増加させること（シナリオD Green Spaceモデル）よりも効率的な緩和策である。
This is because higher vegetation coverage has negative effects on city ventilation.
これは、植生被覆率が高くなると、都市の換気にマイナスの影響を与えるからである。
Therefore, increasing more vegetation coverage is not a great way to mitigate UHI in the subtropical city centre.
したがって、植生被覆率を高めることは、亜熱帯都市中心部におけるUHIを緩和するための優れた方法ではない。
For further work, more efficient urban fabric materials should be developed and evaluated for the potential of improving urban microclimate.
さらなる研究のために、より効率的な都市ファブリック材料を開発し、都市の微気候を改善する可能性について評価する必要がある。
