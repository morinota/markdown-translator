## Two-Stage Neural Contextual Bandits for Personalised News Recommendation

**Mengyan Zhang** _[∗]_
Australian National University
Data61, CSIRO

**Zhenyu He**
University of Electronic Science
and Technology of China

**Xing Xie** **Cheng Soon Ong**
Microsoft Research Asia Data61, CSIRO
Australian National University

### Abstract

**Thanh Nguyen-Tang** **Fangzhao Wu**
Deakin University Microsoft Research Asia

We consider the problem of personalised news recommendation where each user
consumes news in a sequential fashion. Existing personalised news recommendation methods focus on exploiting user interests and ignores exploration in recommendation, which leads to biased feedback loops and hurt recommendation quality
in the long term. We build on contextual bandits recommendation strategies which
naturally address the exploitation-exploration trade-off. The main challenges are
the computational efficiency for exploring the large-scale item space and utilising
the deep representations with uncertainty. We propose a two-stage hierarchical
topic-news deep contextual bandits framework to efficiently learn user preferences
when there are many news items. We use deep learning representations for users
and news, and generalise the neural upper confidence bound (UCB) policies to
generalised additive UCB and bilinear UCB. Empirical results on a large-scale
news recommendation dataset show that our proposed policies are efficient and
outperform the baseline bandit policies.

### 1 Introduction

Online platforms for news rely on effective and efficient personalised news recommendation [25].
The recommender system faces the exploitation-exploration dilemma, where one can exploit by
recommending items that the users like the most so far, or one can also explore by recommending
items that users have not browsed before but may potentially like [16]. Focusing on exploitation tends
to create a pernicious feedback loop, which amplifies biases and raises the so-called filter bubbles or
_echo chamber [15], where the exposure of items is narrowed by such a self-reinforcing pattern._

Contextual bandits are designed to address the exploitation-exploration dilemma and have been
proposed used to mitigate the feedback loop effect [2, 16] by user interest and item popularity exploration. One can formalise the online recommendation problem as a sequential decision-making under
uncertainty, where given some contextual information, an agent (the recommender system) selects
one or more arms (the news items) from all possible choices according to a policy (recommendation
strategy), with the goal of designing a policy which maximises the cumulative rewards (user clicks).

There are two main challenges on applying contextual bandits algorithms in news recommendations.
First, the recommendations need to be scalable for the large news spaces with millions of news items,
which requires the bandit algorithms to learn efficiently when there are many arms (news items).
Second, contextual bandits algorithms need to utilise good representations of both news and users.

_∗Email: mengyan.zhang@anu.edu.au_

Preprint. Under review.

-----

Figure 1: Two-stage neural contextual bandits framework for news recommendation. We address the
large item space using a two-stage hierarchy of topic and news items.

The state-of-the-art news recommender systems utilise deep neural networks (DNN) with two-tower
structures (user and news encoders) [24]. How to combine contextual bandits models with such DNN
models with valid uncertainty estimations remains an open problem. We review related work which
addresses each challenge respectively in Section 3.3.

We propose a two-stage neural contextual bandits framework to address the above challenges, and
illustrate the mapping in Figure 1. We consider a hierarchical topic-news model, where for each
of the recommendations for one user in one iteration, we recommend topics first and then select
an item from the recommended topics. For each stage, we utilise the state-of-the-art two-tower
deep model NRMS [24] to generate topic, news and user representations. We propose shared neural
generalised additive and bilinear upper confidence bound (UCB) policies, and extend existing neural
contextual bandits approaches like Monte-Carlo dropout [5] UCB, neural-linucb [20, 28] to our
framework as baselines. We evaluate our proposed framework empirically on a large-scale news
recommendation dataset MIND [27] and compare our proposed policies with baseline approaches.
To our knowledge, we are the first work to apply two-stage neural contextual bandits framework to
address above challenges.

Our contributions are 1) We propose a hierarchical two-stage neural contextual bandits framework for
user interest exploration in news recommendation, where in the first stage we dynamically construct
topics. 2) We propose shared neural generalised additive and bilinear upper confidence bound policies
to make use of the deep representation of contextual information. 3) We conduct experiments to

-----

simulate the user interest exploration and compare with baseline policies on a large-scale real-world
news recommendation dataset.

### 2 Problem Setting and Challenges

**Personalised News Recommendation** We consider a news recommender system that sequentially
recommends personalised news to users, with the goal of maximising cumulative clicks for all users.
The recommender system learns from the interaction history with the users, and for any given coming
user, the system displays several news selected from the candidate news set. Then the user will react
as either click or non-click and the system uses this as the feedback to learn the preference of users.
This task is challenging since the candidate news set is in the millions and dynamically changes over
time. In addition, there are a large number of cold users (i.e. users that do not have any history)
and the user interest can shift over time [25]. How to design such a recommendation strategy can
be formulated as a sequential decision-making problem, studied in the field of contextual bandits

[16, 22].

**Cumulative Reward** We first introduce the general bandit problem formulation. A news recommender system is regarded as an agent, news items are arms (choices), and the user and/or item
embedding form the context. At each iteration t = 1, . . ., N, given user ut and candidate arm set At,
one can generate the item embedding xi ∈ R[d][1] for all i ∈At, and the user embedding zut ∈ R[d][2]
as context. In the following, we will drop subscript t for ut when there is no ambiguity. The agent
recommends m ≥ 1 news items Srec according to a policy π given the context. Then the agent
receives the feedback {yt,1, . . ., yt,m}, where yt,i ∈{0, 1} indicating whether the user clicks the
item i or not at iteration t. The reward is defined as yt = [�]i[m]=1 [I][{][y][t,i][ = 1][}][. The goal is to design a]
policy to minimise the expected cumulative regret (Definition 1), which is equivalent to maximise
the expected cumulative rewards [16, 22]. Since in recommender systems the optimal rewards are
usually unknown, we focus on maximising the cumulative rewards in this work.

**Definition 1. For a total iteration N** _, the expected cumulative rewards are E_ ��Nt=1 _[y][t]�. Let the_

_optimal reward for user ut as yt[∗][, the expected cumulative regret is defined as][ E]_ ��Nt=1[(][y]t[∗] _[−]_ _[y][t][)]�_ _._

**Contextual Bandits Policies** Upper Confidence Bound (UCB) are one type of classical bandits
policies proposed to address the exploration-exploitation dilemma and proven to have sublinear regret
bound [1]. The idea is the picking the arm with the highest UCB acquisition score, which capture
the upper confidence bound for predictions in high probability. At iteration t, the UCB acquisition
_function for a pair user-item (u, i) follows_

_α[UCB](u, i) := ˆyu,i + βσu,i,_ (1)

where ˆyu,i is the click prediction, σu,i is the uncertainty of predictions, and β is a hyperparameter
balancing the exploitation and exploration. Li et al. [16] popularised the LinUCB contextual bandits
approach on news recommendation tasks, where the expected reward of item i and user u is assumed
to be linear in terms of the contextual feature cu,i ∈ R[d]. Xu et al. [28], Riquelme et al. [20]
studied neural linear models, where the representation of contextual information is learnt by neural
networks, which further improves the performance. Filippi et al. [4] extended the LinUCB policy
to the Generalised Linear Model s.t. E[yu,i|cu,i] = ρ(c[T]u,i[θ]u[∗][)][, where][ ρ][ :][ R][ →] [R][ is the inverse]
link function, θu[∗] _[∈]_ [R][d][ is the unknown coefficient. When][ ρ][(][x][) =][ x][, the problem is reduced to]
linear bandits. Define the design matrix Du ∈ R[n][u][×][d] at iteration t, where each row contains sample
interacted with user u. With Mu = Du[T] _[D][u]_ [+][ I][d] [and estimated coefficient][ ˆ][θ][u][, the GLM-UCB]
acquisition function follows

_α[GLM]_ _[−][UCB](u, i) := ρ(c[T]u,i[θ][ˆ][u][) +][ β][∥][c][u,i][∥]Mu[−][1]_ _[.]_ (2)

In this paper, we consider GLM-UCB policy as a base policy. Since user feedback is binary, we use
the sigmoid function, i.e. we set ρ(x) = exp(x)/(1 + exp(x)), which is the inverse link function of
a Bernoulli distribution [18].

**Two-tower User and Item Representation Learning** We consider the state-of-the-art news recommendation model NRMS [24] as our base model for predictor, which is a two-tower neural network

-----

**Algorithm 1 Two-stage Exploration Framework**
**Input: number of items to be recommended m, number of simulation N**, number of topics q, N
users {u1, . . ., uN _}, set of topics V = {v1, . . ., vj, . . ., vq}, each topic is associated with a set of_
news Svj, topic acquisition function α1, news acquisition function α2.

1: for t = 1 to N do
2: **Stage One: Topic recommendation**

3: Score each topic α1(ut, vj) for all vj ∈V

4: Sort topic v(1), . . ., v(q) according to topic acquisition scores in non-increasing order s.t.
_α1(ut, v(1)) ≥· · · ≥_ _α1(ut, v(q))_

5: Pick sets of topics as S [1] = {v(1)}, . . ., S _[m]_ = {v(m)}

6: Dynamic topic set reconstruction: expand _, . . .,_ with high-score topics.
_S_ [1] _S_ _[m]_

7: **Stage Two: News recommendation**

8: **for j = 1 to m do**

9: Scoring each item α2(ut, i) for all i ∈Sv, for all v ∈S _[j]._

10: Add the item i[∗] with the highest score α2(ut, i[∗]) to recommendation set Srec.

11: **end for**

12: Show Srec to user u and get feedback [yu,a]a∈Srec = oracle(u, Srec)

13: Update topic and item models with rewards [yu,a]a∈Srec .

14: end for

model with multi-head self-attention. At each stage and time step t, we maintain two modules: 1)
The item encoder ft[n][, which takes item information in (e.g. for topic recommendation: topic id,]
topic name; for news recommendation: news id, title, abstract, etc;) and outputs a news embedding
**_x ∈_** R[d][1], and 2) the user encoder ft[u][, which takes the browsed news embedding of user][ i][ in and]
outputs a user embedding z ∈ R[d][2]. The user and news embedding are treated as context, and the
arms (choices) are the candidate news available to be recommended to the coming user.

**2.1** **Challenges**

**Computational Efficiency: Large Item Space: Large scale commercial recommender system has**
millions of dynamically generated items. Calculating the acquisition scores for all candidate news
can be computationally expensive. We address this by proposing a two-stage framework by selecting
topics first in Section 3. In terms of uncertainty inference, while Bayesian models provide distribution
predictions and have shown good performance in bandits tasks, it is computationally expensive to
maintain Bayesian neural models and updates for large scale systems. Two-tower recommendation
model is popular in practical usage due to its efficient inference. We consider the upper confidence
bound (UCB) based policies and combine it with the two-tower deep learning framework with the
additional generalised linear model to inference uncertainties.

**Exploration-Exploitation: Uncertainty with Deep Representation:** Greedily recommending
news to users according to predictors learnt by user clicks may lead to feedback loop bias and
suboptimal recommendations. Thus, an appropriate level of online explorations can guide the system
to dynamically track user interests and contributes to optimal recommendations. State-of-the-art
news recommender systems make use of deep neural networks to learn news and user representations.
How to make use of the power of deep representation and calculating uncertainties (i.e. confidence
interval for predictions) is the key point of efficient exploration. We propose two exploration policies
to address this in 3.2. We further propose to dynamically form the topic set according to the bandits
acquisition score, which avoids biased exploration due to unbalanced topics.

### 3 Two-Stage Deep Recommendation Framework

Recall our goal is to sequentially recommend m 1 news items to users in a large scale recommender
_≥_
system. To reduce the computational complexity of whole-space news exploration, we consider
a two-stage exploration framework in Algorithm 1. We call each of the m recommendation as
_recommendation slot. In stage one (line 3-6), we recommend a set of topics for each recommendation_
slot. Each topic is treated as an arm, and we decide which topics can be recommended by the topic
acquisition function α1. For example, one can use the UCB acquisition function defined in E.q. (1)

-----

Table 1: Summary of UCB policies. Recall xi, zu are the item and user representation, **_θ[ˆ]u,_** **_θ[ˆ]x,_** **_θ[ˆ]z,_** **_θ[ˆ]_**
are coefficients in generalised linear models, with respect to each user, all items, all users, and all
user-item pairs respectively.function. Yu,i[n] [is a list of predictions via Monte-Carlo dropout,] ft[u]−1[, f]t[ n]−1 [are user, item encoders up to iteration][ ˜][γ][ = 1][ −] _[γ][ ∈][ t][(0][ −][,][ 1)][1][.][ ρ][.][ Note we allow][ is the sigmoid]_
biases inside the parameters, i.e. xi is argumented as (xi,1, . . ., xi,d, 1).

Policy Coefficients Predicted Predicted
Context
Name Parameters Rewards Uncertainty

GLM **_xi_** **_θˆu_** _ρ(x[T]i_ **_[θ][ˆ][u][)]_** _∥xi∥Mu−1_
N-DropoutN-GLM **_xix, zi_** _u_ _fθtˆ[u]−u1, f[, f]t[n]−[ n]t−11_ mean(ρ(x[T]i _Y[θ][ˆ]u,i[u][n][)][)]_ _∥std(xi∥YMu,i[n]u−[)]1_
S-N-GALM **_xi, zu_** _ft[u]−1[, f][ n]t−1[,][ ˆ][θ]x[,][ ˆ][θ]z_ _ρ(γx[T]i_ **_[θ][ˆ][x]_** [+ ˜][γ][ ˆ][θ]z[T] **_[z]u[)]_** _γ∥xi∥A−i_ 1 + ˜γ∥zu∥A−u 1
S-N-GBLM **_xi, zu_** _ft[u]−1[, f][ n]t−1[,][ ˆ][θ]_ _ρ(x[T]i_ **_[θz][ˆ]_** _[u][)]_ _∥vec(xizu[T]_ [)][∥]Wt[−][1]

or (2) as α1. For each recommendation slot, we initialise the set of recommended topics with the top
_m acquisition scores respectively. Then in line 6, we dynamically expand each of the topic set with_
the remaining high-score topics. In stage two (line 8-11), we select the most promising news item
(according to the bandit acquisition function α2) for each of the expanded set of topics chosen in
stage one. The acquisition functions in Algorithm 1 used to recommend topics and news can follow
any contextual bandits policies. We introduce the baselines and proposed policies we used in this
work in Section 3.1 and 3.2, which are summarised in Table 1.

**Dynamic Topic Set Reconstruction** It is common that the sizes of the first stage arms are imbalanced. For example, if one clusters items based on similarity, it is highly likely the clusters will end
up to be imbalanced. In our application, news topics are highly imbalanced, ranging from size of
1 up to 15,000 (number of news per topics). We propose to address the imbalanced topics issue by
dynamically reconstructing the set of topics corresponding to each arm according to topic acquisition
scores in each iteration. After the dynamic topic set reconstruction, each topic set has at least p
candidate news items. The main idea of forming topic sets is to include the topics with high bandits
acquisition scores, which means these topics are either potential good exploitation or exploration for
user interest. Furthermore, we also want to allocate topics with high acquisition scores into different
topic sets, so that topics with high scores will have more chance to be selected. We initialise each
topic set with the top m scoring topics _, . . .,_ . Then until all topic sets have at least p news
_{S_ [1] _S_ _[m]}_
items, we add the topic with the highest topic acquisition score in the remaining topics to each of the
_m topic set in sequential order. We illustrate the detailed description in Algorithm 2 in the Appendix._

Once the agent collects m recommended items (one news item per each of m recommended topics),
those m items will be shown to the user and the agent will get user feedback, which is m binary
scores indicating click or non-click for each recommended item. The topic and news neural models
are updated according to the feedback every lt and ln (pre-defined hyperparameters) iterations
respectively. The coefficients of generalised linear models are updated every iteration if applicable.

**3.1** **Baseline Neural Contextual Bandits Policies: Exploration**

Recent work have studied neural contextual bandits algorithms theoretically [30, 28] and empirically

[20], according to those we adapt two most popular algorithms into our framework [3, 28] (see below).

**Neural Dropout UCB (N-Dropout-UCB)** As studied by Gal and Ghahramani [5], the uncertainty
of predictions can be approximated by dropout applied to a neural network with arbitrary depth
and non-linearity. Dropout can be viewed as performing approximate variational inference, with a
variational family that is a discrete distribution over the value of the parameters and zero. Dropout
UCB policies follow this principle, where for user-item pair (u, i), one can predict the click scores
with Monte-Carlo dropout enabled, Yu,i[n] [= [ˆ][y]u,i[1] _[, . . .,][ ˆ][y]u,i[n]_ []][, where][ ˆ][y][u,i][ =][ f][ u]t−1[(][u][)][T][ f][ n]t−1[(][i][)][. Then]
using the mean of the predictions ¯yu,i as central tendency and the standard deviation σu,i as the
uncertainty, one can follow UCB policy defined in E.q. (1).

**Neural Generalised Linear UCB (N-GLM-UCB)** To utilise the representation power of DNNs
and the exploration ability from linear bandits, Neural-Linear [20, 28] learns contextual embedding

-----

from DNNs and use it as input of a linear model. Since our reward is binary, we extend neural LinUCB

[28] to neural generalised linear UCB, where we first get the deep contextual embedding learnt from
NRMS model, and then follow the same acquisition function as in E.q. (2). Applying existing neural
contextual bandits algorithms directly on recommender systems may be computationally expensive or
lead to suboptimal performance. For example, uncertainties inferred from Monte-Carlo can have high
variance [20]. Also, learning coefficients for each arm in neural-linear models is unrealistic, since
one needs enough samples for each of the millions of news items. In our simulation, the number of
users is much smaller than the news items, hence we learn coefficients per user. From our experiment
in Table 2, we observe that performance still drop when the number of users increases.

**3.2** **Proposed Policies: Additive and Bilinear UCB**

We consider shared bandits models where the parameters are shared by all pairs of users and (or)
news items. Coefficient sharing across entities can make the model learned more efficient and more
generalisable. One also needs to design how to capture both the item and user embedding in the
contextual information. We propose the generalised additive linear or generalised bilinear models to
handle this. Recall xi ∈ R[d][1] as item i representation and zu ∈ R[d][2] as user u representation.

**Shared Neural Generalised Additive Linear UCB (S-N-GALM-UCB)** We consider an additive
linear model, where the item-related coefficient θx[∗] [and user-related coefficient][ θ]z[∗] [are modelled]
separately, i.e. E[yu,i|xi, zu] = ρ(γx[T]i **_[θ]x[∗]_** [+ ˜][γ][θ]z[∗]T zu), where γ is a hyperparameter, ˜γ = 1 − _γ._

_α[S][−][N]_ _[−][GALM]_ _[−][UCB](u, i) := ρ(γx[T]i_ **_[θ][ˆ][x]_** [+ ˜][γ][ ˆ][θ]z[T] **_[z][u][) +][ β][(][γ][∥][x][i][∥]A[−]i_** [1] + ˜γ∥zu∥A−u 1 [)][,] (3)

where Ai = Di[T] _[D][i][ +][ I][d]1[, with][ D][i][ ∈]_ [R][n][i][×][d][1][ be a design matrix at iteration][ t][, where each row]
contains item representations that user u that has been observed up to iteration t; Au = Du[T] _[D][u]_ [+][ I][d]2 [,]
with Du ∈ R[n][u][×][d][2] be a design matrix at iteration t, where each row contains user representations
that item i has been recommended to up to iteration t. In this way, the additive model handles the
user and item uncertainties separately.

**Shared Neural Generalised Bilinear UCB (S-N-GBLM-UCB)** Inspired by the Bilinear UCB
algorithm (rank r Oracle UCB) proposed by Jang et al. [14], we consider a Generalised bilinear
model, where we assume E[yu,i|xi, zu] = ρ(x[T]i **_[θ][∗][z][u][)][,][ with the coefficient][ θ][∗]_** [shared by all user-item]
pairs.

_α[S][−][N]_ _[−][GBLM]_ _[−][UCB](u, i) := ρ(x[T]i_ **_[θz][ˆ]_** _[u][) +][ β][∥][vec][(][x][i][z]u[T]_ [)][∥]Wt[−][1] _,_ (4)

where Wt = W0 + [�][t]s[−]=1[1] _[vec][(][x][i]s_ **_[z]u[T]s_** [)][vec][(][x][i]s **_[z]u[T]s_** [)][T][ ∈] [R][d][1][d][2][×][d][1][d][2][, and][ W][0] [= I][d]1[d]2[. Computing]
the confidence interval might be computationally costly due to the inverse of a potentially large design
matrix. Different from Jang et al. [14], instead recommending a pair of arms (u, i), we consider the
item i as arm to be recommended, and user u as side information instead of an arm. The two-tower
model in recommender system is naturally expressed in terms of bilinear structure.

A bilinear bandit can be reinterpreted in the form of linear bandits [14], x[T]i **_[θ][∗][z][u]_** =
�vec �xizu[⊤]� _, vec (θ[∗])�. So linear bandits policies can be applied on bilinear bandits problem_
�
with regret upper bound _O[˜](_ _d[2]1[d][2]2[T]_ [)][, where][ ˜][O][ ignores polylogarithmic factors in][ T] [. However naive]

linear bandit approaches cannot fully utilise the characteristics of the parameters space. The bilinear
policy [14] shows the regret upper bound _O[˜]([√]d1d2drT_ ), with d = max (d1, d2) and r = rank (θ[∗]).

**3.3** **Related Work**

**Hierarchical Exploration** To address large item spaces, hierarchical search is employed. For
two-stage bandits work, Hron et al. [10, 11] studied the effect of exploration in both two stages with
linear bandits algorithms and Mixture-of-Experts nominators. Ma et al. [17] proposed off-policy
policy-gradient two stage approaches, however, without explicit two-stage exploration. There is also
a branch of related work considering hierarchical exploration. Wang et al. [23], Song et al. [22]
explored on a pre-constructed tree of items in MAB or linear bandits setting. Zhang et al. [29] utilises
key-terms to organise items into subsets and relies on occasional conversational feedback from users.
As far as we know, no existing work studies two-stage exploration with deep contextual bandits.

-----

**Neural Contextual Bandits** Contextual bandits with deep models have been used as a popular
approach since it utilise good representations. Riquelme et al. [20] conducted a comprehensive
experiment on deep contextual bandits algorithms based on Thompson sampling, including dropout,
neural-linear and bootstrapped methods. Recently, there are work applying deep contextual bandits
to recommender system. Collier and Llorens [3] proposed a Thompson sampling algorithm based
on inference time Concrete Dropout [6] with learnable dropout rate, and applied this approach on
marketing optimisation problems at HubSpot. Guo et al. [8] studied deep Bayesian bandits with a
bootstrapped model with multiple heads and dropout units, which was evaluated offline and online
in Twitter’s ad recommendation. Hao et al. [9] added representation uncertainty for embedding
to further encourage explore items whose embedding have not been sufficiently learned based on
recurrent neural network models.

Theoretically, Zhou et al. [30] proposed NeuralUCB and proved a sublinear regret bound, followed
which Gu et al. [7] studied the case where the parameters of DNN only update at the end of batches.
Xu et al. [28] proposed Neural-LinUCB to make the use of deep representation from deep neural
networks and shallow exploration with a linear UCB model, and provided a sublinear regret bound.
Zhu and Rigotti [31] proposed sample average uncertainty frequentist exploration, which only
depends on value predictions on each action and is computationally efficient.

To the best of our knowledge, among those utilised the power of deep representation from existing
network structures in online recommender system with bandits feedback, no existing work addressed
the generalised bilinear model for exploration, which suits the two-tower recommender system naturally; and no work has addressed the hierarchical exploration, which can increase the computational
efficiency and is important to the practical use in a large-scale recommender system.

### 4 Experiments

We conduct experiments on a large-scale news recommendation dataset, i.e. MIND [27], which was
collected from the user behaviour logs of Microsoft News. [2] The MIND dataset contains 1,000,000
users, 161,013 news, 285 topics and 24,155,470 samples, which is split to train, validation and test
data for machine learning algorithm usage.

We simulate the sequential recommendation based on MIND dataset. The experiments run in T
independent trials. For each trial τ ∈ [1, T ], we randomly select a set of users Uτ from the whole user
set as the candidate user dataset from trial τ . We randomly select ϵ% of samples Sknown from the
MIND-train dataset as known data to the bandit models and can be used to pre-train the parameters of
bandits neural model NRMS. Note we have removed the samples of the users in Uτ from Sknown for
each trial τ to avoid leak information. This simulates the case where in recommender system we have
collected some history clicks for other users and we would like to recommend news to new users
sequentially and learn their interests. In each iteration t of the total N simulation iterations within
each trial τ, we randomly sample a user ut _τ to simulate the way user ut randomly shows up to_
_∈U_
the recommender system.

To illustrate how the computational complexity of algorithms influence the performance, we follow
Song et al. [22] and introduce the computational budget b = 5000, which constraints the maximum
number of acquisition score over arms one can compute before conducting the recommendation. The
computational budget is set to evaluate the computational efficiency of algorithms and is meaningful
for practical applications like large-scale recommender system. For one-stage algorithms, we
randomly sample b news from the whole news set for the candidate news set of iteration t; for
two-stage algorithms, we first query all topics then use the left budget to explore the items.

We evaluate the performance by the cumulative rewards as defined in Definition 1. To make the
score more comparable between different number of recommendations, we further define the clickthrough-rate (CTR) inside a batch of1 �m _m recommendations at iteration t fo each trial τ as CTR[τ]t_ [=]

_m_ _i=1_ [I][{][y]t[τ] [= 1][}][. Then we evaluate the performance of bandits policies by the cumulative CTR]
over N iterations [�]t[N]=1 [CTR]t[τ] [. We report the mean and standard deviation of the cumulative reward]
or CTR over T trials.

[2https://microsoftnews.msn.com](https://microsoftnews.msn.com)

-----

Table 2: Cumulative CTR for one stage policies with different number of users. We recommend 5
news for each user and simulate the experiment with 2,000 iterations, 5 trials. In policy names, “S”
means shared parameters, and “N” means using neural contextual information from the NRMS.

**Policy \ # User** **10** **100** **1,000**

Random 320 4 320 2 320 2
_±_ _±_ _±_
GLM 442 4 340 4 320 6
_±_ _±_ _±_
N-GLM 1,140 39 522 58 341 11
_±_ _±_ _±_
N-Greedy 1,188 72 1,244 38 1,282 46
_±_ _±_ _±_
N-Dropout 1,198 41 1,256 34 1,286 44
_±_ _±_ _±_

S-N-GALM **1,538 ± 20** **1,522 ± 20** **1,540 ± 19**
S-N-GBLM 1,402 42 1,366 21 1,362 38
_±_ _±_ _±_

Table 3: Cumulative CTR for policies with different number of recommendation each iteration. We
select 100 users and simulate the experiment with 2,000 iterations, 5 trials. The prefix “2-” indicates
two-stage policies.

**Policy \ # Recs** **1** **5** **10**

Random 298 1 320 2 300 3
_±_ _±_ _±_
N-Greedy 418 224 1,244 38 1,364 32
_±_ _±_ _±_
N-Dropout 428 222 1,256 34 1,368 30
_±_ _±_ _±_
S-N-GALM 424 6 1,522 20 1,506 42
_±_ _±_ _±_
S-N-GBLM 422 6 1,366 21 1,443 6
_±_ _±_ _±_

2-Random 228 2 252 4 250 2
_±_ _±_ _±_
2-N-Greedy 426 435 1,450 28 1,315 28
_±_ _±_ _±_
2-N-Dropout 438 452 1,470 38 1,326 28
_±_ _±_ _±_

2-S-N-GALM **444 ± 10** **1,674 ± 45** **1,578 ± 25**
2-S-N-GBLM 428 8 1,655 23 1,556 22
_±_ _±_ _±_

Evaluation of contextual bandits algorithms on recommendation system is challenging. On the
one hand, deploying algorithms in live recommender systems can be logistically and economically
expensive. On the other hand, directly evaluating on logged the sparse recommendation data would
constrain the exploration effects. We consider the off-policy evaluation approach, and build a user_choice simulator to simulate user feedback for any given news. We train the simulator on the logged_
data (MIND-train) and evaluate different methods with the same simulator.

**4.1** **Main Results**

Directly learning from the logged data suffers selection bias and affects the simulator learned from it.
Follow [12, 22], we adopted a standard method used for off-policy evaluation of bandit algorithms,
the Itermediate Bias Mitigation Step via the Inverse Propensity Score (IPS) simulator [13], which
re-weigh the training samples by the inverse propensity score. In particular, we learn the IPS from
logged data via logistic regression [21]. We then convert the predicted scores ˆy [0, 1] from
_∈_
simulator to binary rewards 0, 1 by picking a threshold in order to serve the bandits simulation.
_{_ _}_
We pick the threshold with the largest f-score on validation dataset, where f-score is defined as
2(precision recall)/(precision + recall). To simulate the stochastic rewards, we flip the reward with
_·_
probability ε = 0.1.

We first evaluate the bandits policies for one-stage exploration to illustrate the improvement with
utilising deep representations and the effectiveness of our proposed policies. We evaluated all policies
with 2,000 iterations and 5 trials and show the cumulative CTR with one standard deviation in Table
2. For Random policy, we recommend news uniformly at random from the sampled news set Nt. For
_GLM-UCB policy shown in E.q. (2), the news item representation uses GloVe [19] vectors of the news_
titles, while in N-GLM-UCB, we use the NRMS model. In both policies, we learn **_θ[ˆ]u with collected_**
data for each user u. N-Greedy refers to the policy recommending arms greedily with the NRMS
model predictions and is the baseline for neural network based policies. For N-Dropout-UCB, we
infer 5 times with dropout enabled. For all UCB based algorithm, we set the exploitation-exploration
balance parameter β = 0.1. Results are shown in Table 2.

-----

**(a)** **(b)**

**(c)** **(d)**

Figure 2: Results analysis and ablation study. All policies are UCB policies except the greedy
policies. a) Improvement over random policy: the ratio of cumulative CTR of one-stage policies in
Table 2 and cumulative CTR of random policy for different number of users. b) Influence of number
of users: cumulative CTR ratio between different number of users for one-stage policies in Table
2. c) Improvement of two-stage design: cumulative CTR ratio between two-stage and one-stage
corresponding policies in Table 3. d) Ablation study for dynamic topic comparison (2,000 iteration,
recommendation size 5 and user size 100.). The prefix “2-” indicates two-stage policies.

For the two-stage experiments, we used 100 users, up to 2,000 iterations and 5 trials. We tested
recommendation size 1, 5, 10 in each iteration for each user and show results in Table 3. We
_{_ _}_
select the one-stage policies in Table 2 that perform well (beyond 1, 000 cumulative CTR) under 100
users, namely N-Greedy, N-DropoutUCB, S-N-GALM-UCB and S-N-GBLM-UCB, and test their
performance with additional topic-stage exploration. For two-stage policies, topic and item parts
follow the same policy. The last four rows follow the Algorithm 1. For two-stage Random policy, we
first select topics uniformly random from all topics and then randomly select news from the selected
topics.

**4.2** **Observations and Interpretations**
We show our observations from the main result tables in Section 4.1 and the analysis in Figure 2.

**Two-tower neural representation improves the Performance: In Table 2, compared with non-**
neural policies (first two rows), the neural network based policies (last 5 rows) has significant
improvement. Figure 2a shows the cumulative CTR ratio between policies in Table 2 and random
policies, which illustrates the improvement of neural based methods. Particularly, the only difference between N-GLM-UCB and GLM-UCB is the N-GLM-UCB makes use of neural news item
representation from two-tower model while GLM-UCB uses GLoVe directly. When there is enough
samples for each user (e.g. 10 users, 200 samples each user), the cumulative CTR of N-GLM-UCB is
2.58 times of that of GLM-UCB. Our proposed policies further improves the cumulative CTR by also
making use of neural user representation from two-tower model. This shows the power of combining
two-tower neural representations into the bandits recommendation framework.

**Shared weights for bandit model improves CTR: In Table 2, we can see the cumulative CTR**
for the disjoint policies like GLM-UCB and N-GLM-UCB drops dramatically when the number
of users increases (i.e. number of samples per user decreases), which shows the disjoint models
are hard to be scalable to the large user or item recommender system. This is because the disjoint
policies need enough samples to learn the coefficients for each user, as discussed in Section 3.1. Both
N-Greedy and N-Dropout-UCB outperform N-GLM-UCB on a large number of users, since both of
the policies based on neural networks directly and no additional parameters need to be learnt for each
user. Our proposed policies, which extend from N-GLM-UCB to share parameters across different
users or items, outperform disjoint policies as well. This is verified in Figure 2b, where we show the
cumulative CTR ratio between different number of users for the one-stage policies in Table 2. Except

-----

the ratios of the disjoint policies (GLM-UCB, N-GLM-UCB) are much lower than 1 (i.e. increase
number of users, CTR drops), the ratio of other policies are around 1.

**Two-stage outperforms one-stage: In Table 3, two-stage policies outperform corresponding one-**
stage policies since the topic exploration scope in the news space under promising topics and save the
computational budget. The exception is the two-stage Random policy, which is worse than one stage
Random since selecting bad topics at the first stage would limit the news selection and lead to a lower
click rate. This further shows the importance of a reasonable topic recommendation. We visualise
the cumulative CTR ratio between two-stage and one-stage policies in Figure 2c, where we can see
except the random policy (and N-Greedy, N-Dropout-UCB for 10 recommendations), the ratios are
above 1. The improvements of 5 recommendations and our proposed policies are higher than others.

**Proposed bandit policies outperform others: Both of our proposed policies (S-N-GBLM-UCB,**
S-N-GALM-UCB) have higher cumulative CTR compared other polices in Table 2 and 3, which
illustrates the effectiveness of the shared model and usage of the user representation from neural
network with additive (S-N-GALM-UCB) and bilinear (S-N-GBLM-UCB) structure. With 2,000
iterations, S-N-GALM-UCB slightly outperforms S-N-GBLM-UCB. Although S-N-GBLM-UCB is
able to capture user and item interaction in the generalised linear part, the larger parameter space
needs more time and sample to learn.

**Dynamic topic clustering improves CTR: We further show ablation study in Figure 2d, where we**
test how our dynamic topic construction in Algorithm 2 influences the performance of two-stage
policies in Table 3. We set the minimum reconstruct size p = 1000. We compare with the case where
only the top topic is recommended. To make the comparison fair, if the candidates news under the
recommended topic is smaller than the computational budget, we randomly sample news from the
whole news set to guarantee the number of news evaluated for two methods are the same. We can
observe that for all policies, using the dynamic topic construction improves the CTR significantly.

### 5 Conclusion

We consider the news recommendation task in the contextual bandits setting to balance the exploitation
and exploration in the sequential decision-making process. We propose a two-stage topic-news
recommendation framework with dynamically generated topics, to increase computational efficiency
in the large arm space. We utilise the deep representation from a two-tower neural model and propose
the generalised additive and bilinear upper confidence bound policies to generate uncertainties.
Empirical experiment on a large-scale news recommendation dataset shows our proposed two-stage
framework is computationally efficient and our proposed policies outperforms baselines.

-----

### References

[1] Peter Auer, Nicolo Cesa-Bianchi, and Paul Fischer. Finite-time analysis of the multiarmed
bandit problem. Machine learning, 47(2):235–256, 2002.

[2] Jiawei Chen, Hande Dong, Xiang Wang, Fuli Feng, Meng Wang, and Xiangnan He. Bias and
Debias in Recommender System: A Survey and Future Directions. arXiv:2010.03240 [cs],
[October 2020. URL http://arxiv.org/abs/2010.03240. arXiv: 2010.03240.](http://arxiv.org/abs/2010.03240)

[3] Mark Collier and Hector Urdiales Llorens. Deep Contextual Multi-armed Bandits. arxiv, page 6,
2018.

[4] Sarah Filippi, Olivier Cappe, Aurélien Garivier, and Csaba Szepesvári. Parametric Bandits: The Generalized Linear Case. In Advances in Neural Information Processing Sys_[tems, volume 23. Curran Associates, Inc., 2010. URL https://papers.nips.cc/paper/2010/hash/](https://papers.nips.cc/paper/2010/hash/c2626d850c80ea07e7511bbae4c76f4b-Abstract.html)_
[c2626d850c80ea07e7511bbae4c76f4b-Abstract.html.](https://papers.nips.cc/paper/2010/hash/c2626d850c80ea07e7511bbae4c76f4b-Abstract.html)

[5] Yarin Gal and Zoubin Ghahramani. Dropout as a Bayesian Approximation: Representing
Model Uncertainty in Deep Learning. arXiv:1506.02142 [cs, stat], October 2016. URL
[http://arxiv.org/abs/1506.02142. arXiv: 1506.02142.](http://arxiv.org/abs/1506.02142)

[6] Yarin Gal, Jiri Hron, and Alex Kendall. Concrete dropout. In Proceedings of the 31st Interna_tional Conference on Neural Information Processing Systems, NIPS’17, pages 3584–3593, Red_
Hook, NY, USA, December 2017. Curran Associates Inc. ISBN 978-1-5108-6096-4.

[7] Quanquan Gu, Amin Karbasi, Khashayar Khosravi, Vahab Mirrokni, and Dongruo Zhou.
[Batched Neural Bandits. arXiv:2102.13028 [cs, stat], February 2021. URL http://arxiv.org/abs/](http://arxiv.org/abs/2102.13028)
[2102.13028. arXiv: 2102.13028.](http://arxiv.org/abs/2102.13028)

[8] Dalin Guo, Sofia Ira Ktena, Pranay Kumar Myana, Ferenc Huszar, Wenzhe Shi, Alykhan Tejani,
Michael Kneier, and Sourav Das. Deep Bayesian Bandits: Exploring in Online Personalized
Recommendations. In Fourteenth ACM Conference on Recommender Systems, pages 456–461,
Virtual Event Brazil, September 2020. ACM. ISBN 978-1-4503-7583-2. doi: 10.1145/3383313.
[3412214. URL https://dl.acm.org/doi/10.1145/3383313.3412214.](https://dl.acm.org/doi/10.1145/3383313.3412214)

[9] Wang Hao, Ma Yifei, Ding Hao, and Wang Yuyang. Context uncertainty
in contextual bandits with applications to recommender systems. _AAAI,_
2022. URL [https://assets.amazon.science/47/ec/32c4052c47debab118da516fe532/](https://assets.amazon.science/47/ec/32c4052c47debab118da516fe532/context-uncertainty-in-contextual-bandits-with-applications-to-recommender-systems.pdf)
[context-uncertainty-in-contextual-bandits-with-applications-to-recommender-systems.pdf.](https://assets.amazon.science/47/ec/32c4052c47debab118da516fe532/context-uncertainty-in-contextual-bandits-with-applications-to-recommender-systems.pdf)

[10] Jiri Hron, Karl Krauth, Michael I. Jordan, and Niki Kilbertus. Exploration in two-stage
[recommender systems. arXiv:2009.08956 [cs, stat], September 2020. URL http://arxiv.org/abs/](http://arxiv.org/abs/2009.08956)
[2009.08956. arXiv: 2009.08956.](http://arxiv.org/abs/2009.08956)

[11] Jiri Hron, Karl Krauth, Michael I. Jordan, and Niki Kilbertus. On component interactions
[in two-stage recommender systems. arXiv:2106.14979 [cs, stat], June 2021. URL http:](http://arxiv.org/abs/2106.14979)
[//arxiv.org/abs/2106.14979. arXiv: 2106.14979.](http://arxiv.org/abs/2106.14979)

[12] Jin Huang, Harrie Oosterhuis, Maarten de Rijke, and Herke van Hoof. Keeping Dataset Biases
out of the Simulation: A Debiased Simulator for Reinforcement Learning based Recommender
Systems. In Fourteenth ACM Conference on Recommender Systems, pages 190–199, Virtual
Event Brazil, September 2020. ACM. ISBN 978-1-4503-7583-2. doi: 10.1145/3383313.
[3412252. URL https://dl.acm.org/doi/10.1145/3383313.3412252.](https://dl.acm.org/doi/10.1145/3383313.3412252)

[13] Guido W Imbens and Donald B Rubin. Causal inference in statistics, social, and biomedical
_sciences. Cambridge University Press, 2015._

[14] Kyoungseok Jang, Kwang-Sung Jun, Se-Young Yun, and Wanmo Kang. Improved Regret
Bounds of Bilinear Bandits using Action Space Analysis. In Proceedings of the 38th In_ternational Conference on Machine Learning, pages 4744–4754. PMLR, July 2021. URL_
[https://proceedings.mlr.press/v139/jang21a.html. ISSN: 2640-3498.](https://proceedings.mlr.press/v139/jang21a.html)

-----

[15] Ray Jiang, Silvia Chiappa, Tor Lattimore, András György, and Pushmeet Kohli. Degenerate
Feedback Loops in Recommender Systems. Proceedings of the 2019 AAAI/ACM Conference on
_AI, Ethics, and Society, pages 383–390, January 2019. doi: 10.1145/3306618.3314288. URL_
[http://arxiv.org/abs/1902.10730. arXiv: 1902.10730.](http://arxiv.org/abs/1902.10730)

[16] Lihong Li, Wei Chu, John Langford, and Robert E. Schapire. A contextual-bandit approach to
personalized news article recommendation. In Proceedings of the 19th international conference
_on World wide web - WWW ’10, page 661, Raleigh, North Carolina, USA, 2010. ACM Press._
[ISBN 978-1-60558-799-8. doi: 10.1145/1772690.1772758. URL http://portal.acm.org/citation.](http://portal.acm.org/citation.cfm?doid=1772690.1772758)
[cfm?doid=1772690.1772758.](http://portal.acm.org/citation.cfm?doid=1772690.1772758)

[17] Jiaqi Ma, Zhe Zhao, Xinyang Yi, Ji Yang, Minmin Chen, Jiaxi Tang, Lichan Hong, and Ed H
Chi. Off-policy learning in two-stage recommender systems. In Proceedings of The Web
_Conference 2020, pages 463–473, 2020._

[18] John Ashworth Nelder and Robert WM Wedderburn. Generalized linear models. Journal of the
_Royal Statistical Society: Series A (General), 135(3):370–384, 1972._

[19] Jeffrey Pennington, Richard Socher, and Christopher D. Manning. Glove: Global vectors for
word representation. In Empirical Methods in Natural Language Processing (EMNLP), pages
[1532–1543, 2014. URL http://www.aclweb.org/anthology/D14-1162.](http://www.aclweb.org/anthology/D14-1162)

[20] Carlos Riquelme, George Tucker, and Jasper Snoek. DEEP BAYESIAN BANDITS SHOWDOWN. ICLR, page 27, 2018.

[21] Tobias Schnabel, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims.
Recommendations as Treatments: Debiasing Learning and Evaluation. arXiv:1602.05352

_[[cs], May 2016. URL http://arxiv.org/abs/1602.05352. International Conference on Machine](http://arxiv.org/abs/1602.05352)_
Learning.

[22] Yu Song, Jianxun Lian, Shuai Sun, Hong Huang, Yu Li, Hai Jin, and Xing Xie. Show Me the
Whole World: Towards Entire Item Space Exploration for Interactive Personalized Recommen[dations. WSDM, October 2021. URL http://arxiv.org/abs/2110.09905.](http://arxiv.org/abs/2110.09905)

[23] Qing Wang, Tao Li, SS Iyengar, Larisa Shwartz, and Genady Ya Grabarnik. Online it ticket
automation recommendation using hierarchical multi-armed bandit algorithms. In Proceedings
_of the 2018 SIAM International Conference on Data Mining, pages 657–665. SIAM, 2018._

[24] Chuhan Wu, Fangzhao Wu, Suyu Ge, Tao Qi, Yongfeng Huang, and Xing Xie. Neural News
Recommendation with Multi-Head Self-Attention. In Proceedings of the 2019 Conference on
_Empirical Methods in Natural Language Processing and the 9th International Joint Conference_
_on Natural Language Processing (EMNLP-IJCNLP), pages 6389–6394, Hong Kong, China,_
November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1671. URL
[https://aclanthology.org/D19-1671.](https://aclanthology.org/D19-1671)

[25] Chuhan Wu, Fangzhao Wu, Yongfeng Huang, and Xing Xie. Personalized news recommendation: A survey. arXiv preprint arXiv:2106.08934, 2021.

[26] Chuhan Wu, Fangzhao Wu, Tao Qi, and Yongfeng Huang. Empowering News Recommendation
[with Pre-trained Language Models. arXiv:2104.07413 [cs], April 2021. URL http://arxiv.org/](http://arxiv.org/abs/2104.07413)
[abs/2104.07413. arXiv: 2104.07413.](http://arxiv.org/abs/2104.07413)

[27] Fangzhao Wu, Ying Qiao, Jiun-Hung Chen, Chuhan Wu, Tao Qi, Jianxun Lian, Danyang Liu,
Xing Xie, Jianfeng Gao, Winnie Wu, and Ming Zhou. MIND: A Large-scale Dataset for
News Recommendation. In Proceedings of the 58th Annual Meeting of the Association for
_Computational Linguistics, pages 3597–3606, Online, July 2020. Association for Computational_
[Linguistics. doi: 10.18653/v1/2020.acl-main.331. URL https://aclanthology.org/2020.acl-main.](https://aclanthology.org/2020.acl-main.331)
[331.](https://aclanthology.org/2020.acl-main.331)

[28] Pan Xu, Zheng Wen, Handong Zhao, and Quanquan Gu. Neural Contextual Bandits with Deep
Representation and Shallow Exploration. arXiv:2012.01780 [cs, stat], December 2020. URL
[http://arxiv.org/abs/2012.01780. arXiv: 2012.01780.](http://arxiv.org/abs/2012.01780)

-----

[29] Xiaoying Zhang, Hong Xie, Hang Li, and John C. S. Lui. Conversational Contextual Bandit:
[Algorithm and Application. arXiv:1906.01219 [cs, stat], January 2020. URL http://arxiv.org/](http://arxiv.org/abs/1906.01219)
[abs/1906.01219. arXiv: 1906.01219.](http://arxiv.org/abs/1906.01219)

[30] Dongruo Zhou, Lihong Li, and Quanquan Gu. Neural Contextual Bandits with UCB-based
[Exploration. arXiv:1911.04462 [cs, stat], July 2020. URL http://arxiv.org/abs/1911.04462.](http://arxiv.org/abs/1911.04462)
arXiv: 1911.04462.

[31] Rong Zhu and Mattia Rigotti. Deep Bandits Show-Off: Simple and Efficient Exploration with
Deep Networks. Thirty-fifth Conference on Neural Information Processing Systems, page 25,
2021.

-----

### Appendix

**Algorithm 2 Dynamic Topic Reconstruction**
**Input: lst : topic list sorted according to topic acquisition score in non-increasing order, constructed**
topic group arms _, . . .,_, minimum reconstruction topic size p.
_S_ [1] _S_ _[m]_

1: while there exists at least one topic group arm has size smaller than p do
2: **for v = 1 to m do**

3: **if |S** _[v]| < p then_

4: _S_ _[v]_ _←S_ _[v]_ _∪_ _lst[0]; lst = lst/lst[0]_

5: **end if**

6: **end for**

7: end while
**Return Reconstructed topic group arms S** [1], . . ., S _[m]._

### A Supplementary Experiment Details

Our experiment is conducted in python 3.8 (with PyTorch 1.9). We run our experiments on 2 Titan V
GPUs. We provide our code and instructions to reproduce our main experiments in supplementary
materials, and provide more experiment details below.

**A.1** **Simulated Rewards**

**Off-policy user feedback training** In this part, we describe in details our training method to
simulate user feedback based on a large-scale news recommendation dataset (MIND) [27]. We build
the user feedback module upon the neural news recommendation with multi-head self-attention
(NRMS) [24]. Specifically, given a user u and an news item i, NRMS builds a user encoder
_∈U_ _∈A_
_f_ _[u]_ : U → R[d] and a news encoder f _[i]_ : A → R[d], where the architectures for f _[u]_ and f _[u]_ are given in

[24, Figure 2]. Given such encoders, the click probability score is computed by the inner product of
the user representation vector and the news representation vector, i.e. ˆyu,i = f _[u][u](T)_ _f_ _[i](i)._

To train such a click probability score model above, initially Wu et al. [24] use softmax loss with
negative sampling techniques. That is, for a given user, each news browsed by the user (regarded as a
positive sample) is combined with K randomly sampled news in the same impression but not clicked
by the user (regarded as negative samples) to form a set of samples with the corresponding click
probability scores ˆyi[+][,][ ˆ][y]i,[−]1[, . . .,][ ˆ][y]i,K[−] [. The softmax score for the positive sample is then computed as]

exp(yi[+][)]
_pi =_ �K _._
_j=1_ [exp(][y]i,j[−] [)]

The final loss function is the negative log-likelihood of all positive samples S:

�
_L = −_ log pi.

_i∈S_

To simulate binary rewards, in our work, we instead using binary cross-entropy loss with negative
sampling techniques. In particular, with the same notations above, the binary cross-entropy we used
in our work is

�
_LBCE :=_ (bce(yi[+][) +]

_i∈S_

_K_
�

_bce(yi,j[−]_ [))][,]
_j=1_

where bce(yi[+][) :=][ −] [log][ sigmoid][(][y]i[+][)][ and][ bce][(][y]i,j[−] [) :=][ −] [log(1][ −] [sigmoid][(][y]i,j[−] [))][.]

However, LBCE is biased as samples (including both positive and negative samples) are not equally
distributed, as the fixed dataset has been collected by some unknown behaviour policy, which is
not necessarily a uniform sampling. To de-bias our initially proposed loss LBCE, we leverage an

-----

off-policy evaluation approach via Hájek estimator

_bce(yi[+][)]_ _bce(yi,j[−]_ [)]

� _P (Ou,i=1)_ [+][ �]j[K]=1 _P (Ou,j_ =1)
_LBCE[debiased]_ := 1 1 _,_

_i∈S_ _P (Ou,i=1)_ [+][ �]j[K]=1 _P (Ou,j_ =1)

where Ou,i ∈{0, 1} is the random variable that indicates if the feedback is observed for a user-item
pair (u, i), and u denotes the user associated with the positive sample i in the current impression list
(note that in each impression list in MIND dataset is associated with a unique user). In practice, we
simply estimate P (Ou,i = 1) using its empirical estimate directly from the dataset:

_Pˆ(Ou,i = 1) = [#][of times][ u][ sees][ i]_ (5)

# of times u appears

**Result** Our debiased training method described above produces a user feedback simulator with
AUC score of 68.46%, higher than the reported AUC of 68.18% of the original NRMS trained with
the negative sampling techniques [26, Table 2]. We used K = 4 in our experiment.

**Binary feedback simulation** Given our trained user feedback model above, we need to convert
the click probability score ˆyu,i into a binary reward. For this, we first convert the click probability
score ˆyu,i into a valid probability by applying the sigmoid function on the score. We then pick
a threshold by maximizing f -score of the predicted probabilities over the entire dataset. As a
result, we obtain the threshold value THRES = 0.38414. Then the simulated binary reward is
_yu,i := 1{yˆu,i ≥_ _THRES}. Such threshold approach gives a deterministic binary reward. In_
practice, however, the user feedback can be stochastic. For example, given a fixed user and fixed
news, the user might not click on that news when (s)he sees the news for the first time but not
for later times when (s)he sees the news again as this time his/her preference might have changed.
To model such user preference uncertainty, we simply flip the value of the deterministic reward
_yu,i = 1{yˆu,i ≥_ _THRES} with some probability p. This flipping reward is our modelling choice_
rather than a data-driven choice as it is difficult to infer a user’s preference uncertainty from a fixed
dataset. In our experiment, we used p = 0.1.

**A.2** **NRMS Neural Model**

**News Item Neural Model** For news items, we follow the NRMS model [24]. It contains news
_encoder and user encoder. The news encoder learns news representation from news titles, which_
contains a word embedding layer, word-level multi-head self-attention and additive work attention
network. The user encoder learns user representation from their browsed news, which contains newslevel multi-head self-attention and additive news attention network. We follow the hyperparameter
settings in [24] and change the news representation dimension to 64.

**Topic Neural Model** We use the same architecture and hyperparameter settings of news encoder
and user encoder as in the News Item Neural Model to get user representation. For each topic, we
randomly initialise a vector with the same dimension of the user representation. The topic encoder
takes the topic name as input and contains a word embedding layer and a multi-layer perceptron.
We use dot product between the user representation and the topic representation to get user interest
in topics in stage one and train the model with binary cross-entropy. To balance the positive and
negative samples, we further adopt the negative sampling approach [24] with positive and negative
sample ratio as 1.

**A.3** **Simulation Settings**

We specify the additional parameter setting for simulation which has not been specified in the main
paper. We update item neural models every 100 iterations, topic neural models every 50 iterations,
topic and item generalised linear models every iteration (if there exist clicks from recommendations).
We inference Monte-Carlo dropout 5 times and dropout rate is set to be 0.2. Dropout is applied in
the news encoder after the word embedding layer and multi-head attention layer. Since our user
representation is based on the clicked news representation, the dropout uncertainty includes both
the news and user uncertainty. We set the minimum topic construction size as 1,000. We train the
generalised linear models by gradient descent and select the learning rate as 0.01 (for bilinear learning
rate is 0.001). Except specified, we set the UCB parameter β = 0.1.

-----

Figure 3: Cumulative CTR for proposed one and two stage algorithms for T = 10,000. The left and
right show the first and last 2,000 iterations respectively. The experiment is conduct with 5 trials,
recommendation size 5 and user size 100.

Figure 4: UCB Hyperarameter β tuning. “2-"" represents two-stage policies. The experiment is
conducted with 2,000 iteration, recommendation size 5 and user size 100.

**A.4** **Additional experiments and observations**

**Small recommendation size has low CTR: In Table 3, we can observe for all policies, the cumu-**
lative CTR for recommendation size 1 is much smaller than those of recommendation sizes 5 and
10. The reason is that the small recommendation size restricts the number of feedback the system
can get and thus with the same number of iterations, the parameter learning is slow for both neural
and generalised linear models with recommendation size 1. Additionally, we can observe that the
N-Greedy and N-Dropout-UCB based policies have a large variance for the top-1 recommendation,
while our proposed policies perform more stable in this case.

**Cumulative CTR for large iterations: In Table 2 and 3, we can see additive based policies have**
higher cumulative CTR than bilinear based models for 2,000 iterations. We further verify our
interpretation about bilinear policies take more time to train and need more samples to learn. We
compare the cumulative CTR curves for our proposed policies in one stage and two stages with
10,000 iterations. We show the curves for first 2,000 iterations (left) and last 2,000 iterations (right)
in Figure 3. We can see on the left, for both one and two stages, GALM outperforms GBLM for
small iterations, while on the right, 2-S-N-GALM and 2-S-N-GBLM have similar performance
(2-S-N-GBLM is lightly better), and S-N-GALM is still better than S-N-GBLM.

**Hyperparameter tuning: In Figure 4, we show how changing the exploitation-exploration balance**
parameter β influences the cumulative CTR for our two-stage proposed algorithms, where the choice
is β is the same for both the topic and item stage. We can observe that for both of the policies,
relatively small β gives a high CTR. In particular, a large β (e.g. β = 2) will lead to a performance
drop since it involves too much exploration.

-----
