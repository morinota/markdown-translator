# Off-Policy Evaluation for Large Action Spaces via Embeddings
2 2 0 2   n u J   6 1     ] G L . s c [     2 v 7 1 3 6 0 . 2 0 2 2 : v i X r a
## Yuta Saito 1 Thorsten Joachims 1
# Abstract
Off-policy evaluation (OPE) in contextual bandits has seen rapid adoption in real-world systems, since it enables ofﬂine evaluation of new policies using only historic log data. Unfortunately, when the number of actions is large, existing OPE es- timators – most of which are based on inverse propensity score weighting – degrade severely and can suffer from extreme bias and variance. This foils the use of OPE in many applications from recommender systems to language models. To overcome this issue, we propose a new OPE estimator that leverages marginalized importance weights when action embeddings provide struc- ture in the action space. We characterize the bias, variance, and mean squared error of the proposed estimator and analyze the conditions under which the action embedding provides statistical beneﬁts over conventional estimators. In addition to the theoretical analysis, we ﬁnd that the empirical performance improvement can be substantial, en- abling reliable OPE even when existing estimators collapse due to a large number of actions.
# 1. Introduction
Many intelligent systems (e.g., recommender systems, voice assistants, search engines) interact with the environment through a contextual bandit process where a policy observes a context, takes an action, and obtains a reward. Logs of these interactions provide valuable data for off-policy evalu- ation (OPE), which aims to accurately evaluate the perfor- mance of new policies without ever deploying them in the ﬁeld. OPE is of great practical relevance, as it helps avoid costly online A/B tests and can also act as subroutines for batch policy learning (Dud´ık et al., 2014; Su et al., 2020a). However, OPE is challenging, since the logs contain only partial-information feedback – speciﬁcally the reward of the 1Department of Computer Science, Cornell University, Ithaca, NY, USA. Correspondence to: Yuta Saito <ys552@cornell.edu>, Thorsten Joachims <tj@cs.cornell.edu>. Proceedings of the 39 th International Conference on Machine Learning, Baltimore, Maryland, USA, PMLR 162, 2022. Copy- right 2022 by the author(s). chosen action, but not the counterfactual rewards of all the other actions a different policy might choose. When the action space is small, recent advances in the design of OPE estimators have led to a number of reliable methods with good theoretical guarantees (Dud´ık et al., 2014; Swami- nathan & Joachims, 2015a; Wang et al., 2017; Farajtabar et al., 2018; Su et al., 2019; 2020a; Metelli et al., 2021). Unfortunately, these estimators can degrade severely when the number of available actions is large. Large action spaces are prevalent in many potential applications of OPE, such as recommender systems where policies have to handle thou- sands or millions of items (e.g., movies, songs, products). In such a situation, the existing estimators based on inverse propensity score (IPS) weighting (Horvitz & Thompson, 1952) can incur high bias and variance, and as a result, be impractical for OPE. First, a large action space makes it challenging for the logging policy to have common support with the target policies, and IPS is biased under support deﬁciency (Sachdeva et al., 2020). Second, a large num- ber of actions typically leads to high variance of IPS due to large importance weights. To illustrate, we ﬁnd in our experiments that the variance and mean squared error of IPS inﬂate by a factor of over 300 when the number of actions increases from 10 to 5000 given a ﬁxed sample size. While doubly robust (DR) estimators can somewhat reduce the variance by introducing a reward estimator as a control vari- ate (Dud´ık et al., 2014), they do not address the fundamental issues that come with large action spaces. To overcome the limitations of the existing estimators when the action space is large, we leverage additional informa- tion about the actions in the form of action embeddings. There are many cases where we have access to such prior information. For example, movies are characterized by aux- iliary information such as genres (e.g., adventure, science ﬁction, documentary), director, or actors. We should then be able to utilize these supplemental data to infer the value of actions under-explored by the logging policy, potentially achieving much more accurate policy evaluation than the existing estimators. We ﬁrst provide the conditions under which action embeddings provide another path for unbiased OPE, even with support deﬁcient actions. We then propose the Marginalized IPS (MIPS) estimator, which uses the marginal distribution of action embeddings, rather than ac- tual actions, to deﬁne a new type of importance weights. We
### Off-Policy Evaluation for Large Action Spaces via Embeddings
show that MIPS is unbiased under an alternative condition, which states that the action embeddings should mediate ev- ery causal effect of the action on the reward. Moreover, we show that MIPS has a lower variance than IPS, especially when there is a large number of actions, and thus the vanilla importance weights have a high variance. We also charac- terize the gain in MSE provided by MIPS, which implies an interesting bias-variance trade-off with respect to the qual- ity of the action embeddings. Including many embedding dimensions captures the causal effect better, leading to a smaller bias of MIPS. In contrast, using only a subset of the embedding dimensions reduces the variance more. We thus propose a strategy to intentionally violate the assumption about the action embeddings by discarding less relevant embedding dimensions for achieving a better MSE at the cost of introducing some bias. Comprehensive experiments on synthetic and real-world bandit data verify the theoreti- cal ﬁndings, indicating that MIPS can provide an effective bias-variance trade-off in the presence of many actions.
# 2. Off-Policy Evaluation
We follow the general contextual bandit setup, and an ex- tensive discussion of related work is given in Appendix A. Let x ∈ X ⊆ Rdx be a dx-dimensional context vector drawn i.i.d. from an unknown distribution p(x). Given context x, a possibly stochastic policy π(a|x) chooses ac- tion a from a ﬁnite action space denoted as A. The reward r ∈ [0, rmax] is then sampled from an unknown conditional distribution p(r|x, a). We measure the effectiveness of a policy π through its value V (π) := Ep(x)π(a|x)p(r|x,a)[r] = Ep(x)π(a|x)[q(x, a)], (1) where q(x, a) := E[r|x, a] denotes the expected reward given context x and action a. In OPE, we are given logged bandit data collected by a logging policy π0. Speciﬁcally, let D := {(xi, ai, ri)}n i=1 be a sample of logged bandit data containing n independent observations drawn from the logging policy as (x, a, r) ∼ p(x)π0(a|x)p(r|x, a). We aim to develop an estimator ˆV for the value of a target policy π (which is different from π0) using only the logged data in D. The accuracy of ˆV is quantiﬁed by its mean squared error (MSE)
$$
(cid:104)(cid:0)V (π) − ˆV (π;D)(cid:1)2(cid:105)
$$
$$
= Bias( ˆV (π))2 + VD(cid:2) ˆV (π;D)(cid:3),
$$
$$
(cid:104)(cid:0) ˆV (π;D) − ED[ ˆV (π;D)](cid:1)2(cid:105)
$$
.
$$
Bias( ˆV (π)) := ED[ ˆV (π;D)] − V (π),
$$
$$
VD(cid:2) ˆV (π;D)(cid:3) := ED
$$
where ED[·] takes the expectation over the logged data and
$$
MSE( ˆV (π)) : = ED
$$
In the following theoretical analysis, we focus on the IPS estimator, since most advanced OPE estimators are based on IPS weighting (Dud´ık et al., 2014; Wang et al., 2017; Su et al., 2019; 2020a; Metelli et al., 2021). IPS estimates the value of π by re-weighting the observed rewards as follows.
$$
ˆVIPS(π;D) :=
$$
$$
1
$$
n π(ai|xi) π0(ai|xi) ri =
$$
1
$$
n w(xi, ai)ri n(cid:88) i=1 n(cid:88) i=1 where w(x, a) := π(a|x)/π0(a|x) is called the (vanilla) importance weight. This estimator is unbiased (i.e., ED[ ˆVIPS(π;D)] = V (π)) under the following common support assumption. Assumption 2.1. (Common Support) The logging policy π0 is said to have common support for policy π if π(a|x) > 0 → π0(a|x) > 0 for all a ∈ A and x ∈ X . The unbiasedness of IPS is desirable, making this simple re-weighting technique so popular. However, IPS can still be highly biased, particularly when the action space is large. Sachdeva et al. (2020) indicate that IPS has the following bias when Assumption 2.1 is not true.  , π(a|x)q(x, a)
$$
(cid:12)(cid:12)Bias( ˆVIPS(π))(cid:12)(cid:12) = Ep(x)
$$
 (cid:88) a∈U0(x,π0) where U0(x, π0) := {a ∈ A | π0(a|x) = 0} is the set of unsupported or deﬁcient actions for context x under π0. Note that U0(x, π0) can be large especially when A is large. This bias is due to the fact that the logged dataset D does not contain any information about the unsupported actions. Another critical issue of IPS is that its variance can be large, which is given as follows (Dud´ık et al., 2014). nVD(cid:2) ˆVIPS(π;D)(cid:3) = Ep(x)π0(a|x)[w(x, a)2σ2(x, a)] (cid:2)Eπ0(a|x)[w(x, a)q(x, a)](cid:3) (cid:2)Vπ0(a|x)[w(x, a)q(x, a)](cid:3) , + Vp(x) + Ep(x) (2) where σ2(x, a) := V[r|x, a]. The variance consists of three terms. The ﬁrst term reﬂects the randomness in the rewards. The second term represents the variance due to the random- ness over the contexts. The ﬁnal term is the penalty arising from the use of IPS weighting, and it is proportional to the weights and the true expected reward. The variance con- tributed by the ﬁrst and third terms can be extremely large when the weights w(x, a) have a wide range, which occurs when π assigns large probabilities to actions that have low probability under π0. The latter can be expected when the action space A is large and the logging policy π0 aims to have universal support (i.e., π0(a|x) > 0 for all a and x). Swaminathan et al. (2017) also point out that the variance of IPS grows linearly with w(x, a), which can be Ω(|A|).
### Off-Policy Evaluation for Large Action Spaces via Embeddings
This variance issue can be lessened by incorporating a re- ward estimator ˆq(x, a) ≈ q(x, a) as a control variate, re- sulting in the DR estimator (Dud´ık et al., 2014). DR often improves the MSE of IPS due to its variance reduction prop- erty. However, DR still suffers when the number of actions is large, and it can experience substantial performance dete- rioration as we demonstrate in our experiments.
# 3. The Marginalized IPS Estimator
The following proposes a new estimator that circumvents the challenges of IPS for large action spaces. Our approach is to bring additional structure into the estimation problem, providing a path forward despite the minimax optimality of IPS and DR. In particular, IPS and DR achieve the minimax optimal MSE of at most O(n−1(Eπ0[w(x, a)2σ2(x, a) + max])), which means that they are impossible w(x, a)2r2 to improve upon in the worst case beyond constant fac- tors (Wang et al., 2017; Swaminathan et al., 2017), unless we bring in additional structure. Our key idea for overcoming the limits of IPS and DR is to assume the existence of action embeddings as prior in- formation. The intuition is that this can help the estimator transfer information between similar actions. More formally, suppose we are given a de-dimensional action embedding e ∈ E ⊆ Rde for each action a, where we merely assume that the embedding is drawn i.i.d. from some unknown dis- tribution p(e|x, a). The simplest example is to construct action embeddings using predeﬁned category information (e.g., product category). Then, the embedding distribution is independent of the context and it is deterministic given the action. Our framework is also applicable to the most general case of continuous, stochastic, and context-dependent action embeddings. For example, product prices may be generated by a personalized pricing algorithm running behind the sys- tem. In this case, the embedding is continuous, depends on the user context, and can be stochastic if there is some randomness in the pricing algorithm. Using the action embeddings, we now reﬁne the deﬁnition of the policy value as: V (π) = Ep(x)π(a|x)p(e|x,a)p(r|x,a,e)[r]. Note here that q(x, a) = Ep(e|x,a)[q(x, a, e)] where q(x, a, e) := E[r|x, a, e], so the above reﬁnement does not contradict the original deﬁnition given in Eq. (1). A logged bandit dataset now contains action embeddings for each observation in D = {(xi, ai, ei, ri)}n i=1, where each tuple is generated by the logging policy as (x, a, e, r) ∼ p(x)π0(a|x)p(e|x, a)p(r|x, a, e). Our strategy is to lever- age this additional information for achieving a more accurate OPE for large action spaces. To motivate our approach, we introduce two properties char- Figure 1. Causal Graph Consistent with Assumption 3.2 Note: Grey arrows indicate the existence of causal effect of the tail variable on the head variable. The dashed red arrow is a direct causal effect that is ruled out by Assumption 3.2. and x ∈ X , where p(e|x, π) :=(cid:80) acterizing an action embedding. Assumption 3.1. (Common Embedding Support) The log- ging policy π0 is said to have common embedding support for policy π if p(e|x, π) > 0 → p(e|x, π0) > 0 for all e ∈ E a∈A p(e|x, a)π(a|x) is the marginal distribution over the action embedding space given context x and policy π. Assumption 3.1 is analogous to Assumption 2.1, but re- quires only the common support with respect to the action embedding space, which can be substantially more com- pact than the action space itself. Indeed, Assumption 3.1 is weaker than common support of IPS (Assumption 2.1).1 Next, we characterize the expressiveness of the embedding in the ideal case, but we will relax this assumption later. Assumption 3.2. (No Direct Effect) Action a has no direct effect on the reward r, i.e., a ⊥ r | x, e. As illustrated in Figure 1, Assumption 3.2 requires that every possible effect of a on r be fully mediated by the observed embedding e. For now, we rely on the validity of Assump- tion 3.2, as it is convenient for introducing the proposed estimator. However, we later show that it is often beneﬁcial to strategically discard some embedding dimensions and violate the assumption to achieve a better MSE. We start the derivation of our new estimator with the obser- vation that Assumption 3.2 gives us another path to unbiased estimation of the policy value without Assumption 2.1. Proposition 3.3. Under Assumption 3.2, we have V (π) = Ep(x)p(e|x,π)p(r|x,e)[r] See Appendix B.1 for the proof. Proposition 3.3 provides another expression of the pol- icy value without explicitly relying on the action variable a. This new expression naturally leads to the following marginalized inverse propensity score (MIPS) estimator, 1First, if Assumption 2.1 is true, Assumption 3.1 is also true because p(e|x, a) remains the same for the target and logging policies. Table 1 will provide a counterexample for the opposite statement (i.e., Assumption 3.1 does not imply Assumption 2.1).
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Table 1. A toy example illustrating the beneﬁts of marginal importance weights p(e|x1, π0) π0(a|x1) a1 a2 a3 0.0 0.2 0.8 π(a|x1) w(x1, a) N/A 4.0 0.0 0.2 0.8 0.0 p(e1|a) 0.25 0.5 0.25 p(e2|a) 0.25 0.25 0.5 p(e3|a) 0.5 0.25 0.25 a1 a2 a3 e1 e2 e3 0.3 0.45 0.25 p(e|x1, π) w(x1, e) 0.45 0.25 0.3 1.5 0.55 1.2 which is our main proposal.
$$
ˆVMIPS(π;D) :=
$$
$$
1
$$
n p(ei|xi, π) p(ei|xi, π0) ri = n(cid:88) i=1 n(cid:88) i=1
$$
1
$$
n w(xi, ei)ri, where w(x, e) := p(e|x, π)/p(e|x, π0) is the marginal im- portance weight deﬁned with respect to the marginal distri- bution over the action embedding space. To obtain an intuition for the beneﬁts of MIPS, we provide a toy example in Table 1 with X = {x1}, A = {a1, a2, a3}, and E = {e1, e2, e3} (a special case of our formulation with a discrete embedding space). The left table describes the logging and target policies with respect to A and implies that Assumption 2.1 is violated (π0(a1|x1) = 0.0). The middle table describes the conditional distribution of the action embedding e given action a (e.g., probability of a movie a belonging to a genre e). The right table describes the marginal distributions over E, which are calculable from the other two tables. By considering the marginal distri- bution, Assumption 3.1 is ensured in the right table, even if Assumption 2.1 is not true in the left table. Moreover, the maximum importance weight is smaller for the right table (maxe∈E w(x1, e) < maxa∈A w(x1, a)), which may contribute to a variance reduction of the resulting estimator. Below, we formally analyze the key statistical properties of MIPS and compare them with those of IPS, including the realistic case where Assumption 3.2 is violated.
## 3.1. Theoretical Analysis
First, the following proposition shows that MIPS is unbiased under assumptions different from those of IPS. Proposition 3.4. Under Assumptions 3.1 and 3.2, MIPS is unbiased, i.e., ED[ ˆVMIPS(π;D)] = V (π) for any π. See Appendix B.2 for the proof. Proposition 3.4 states that, even when π0 fails to provide common support over A such that IPS is biased, MIPS can still be unbiased if π0 provides common support over E (Assumption 3.1) and e fully captures the causal effect of a on r (Assumption 3.2). Having multiple estimators that enable unbiased OPE under different assumptions is in itself desirable, as we can choose the appropriate estimator depending on the data generating process. However, it is also helpful to understand how vio- lations of the assumptions inﬂuence the bias of the resulting estimator. In particular, for MIPS, it is difﬁcult to verify whether Assumption 3.2 is true in practice. The following theorem characterizes the bias of MIPS. Theorem 3.5. (Bias of MIPS) If Assumption 3.1 is true, but Assumption 3.2 is violated, MIPS has the following bias.
$$
Bias( ˆVMIPS(π))
$$
= Ep(x)p(e|x,π0) (cid:20)(cid:88) a<b π0(a|x, e)π0(b|x, e) × (q(x, a, e) − q(x, b, e)) × (w(x, b) − w(x, a)) (cid:21) , where a, b ∈ A. See Appendix B.3 for the proof. Theorem 3.5 suggests that three factors contribute to the bias of MIPS when Assumption 3.2 is violated. The ﬁrst factor is the predictivity of the action embeddings with re- spect to the actual actions. When action a is predictable given context x and embedding e, π0(a|x, e) is close to zero or one (deterministic), meaning that π0(a|x, e)π0(b|x, e) is close to zero. This suggests that even if Assumption 3.2 is violated, action embeddings that identify the actions well still enable a nearly unbiased estimation of MIPS. The sec- ond factor is the amount of direct effect of the action on the reward, which is quantiﬁed by q(x, a, e) − q(x, b, e). When the direct effect of a on r is small, q(x, a, e) − q(x, b, e) also becomes small and so is the bias of MIPS. In an ideal situation where Assumption 3.2 is satisﬁed, we have q(x, a, e) = q(x, b, e) = q(x, e), thus MIPS is unbiased, which is consistent with Proposition 3.4. Note that the ﬁrst two factors suggest that, to reduce the bias, the action embeddings should be informative so that they are either predictive of the actions or mediate a large amount of the causal effect. The ﬁnal factor is the similarity between log- ging and target policies quantiﬁed by w(x, a) − w(x, b). When Assumption 3.2 is satisﬁed, MIPS is unbiased for any target policy, however, Theorem 3.5 suggests that if the assumption is not true, MIPS produces a larger bias for target policies dissimilar from the logging policy.2 2When π = π0, the bias is zero regardless of the other factors as w(x, a) = w(x, b) = 1, meaning that on-policy estimation is always unbiased, which is quite intuitive.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Next, we analyze the variance of MIPS, which we show is never worse than that of IPS and can be substantially lower. Theorem 3.6. (Variance Reduction of MIPS) Under As- sumptions 2.1, 3.1, and 3.2, we have
$$
(cid:16)VD[ ˆVIPS(π;D)] − VD[ ˆVMIPS(π;D)]
$$
(cid:17) (cid:2)Ep(r|x,e) (cid:2)r2(cid:3) Vπ0(a|x,e) [w(x, a)](cid:3) , n = Ep(x)p(e|x,π0) which is non-negative. Note that the variance reduction is also lower bounded by zero even when Assumption 3.2 is not true. See Appendix B.4 for the proof. There are two factors that affect the amount of variance reduction. The ﬁrst factor is the second moment of the re- ward with respect to p(r|x, e). This term becomes large when, for example, the reward is noisy even after condition- ing on the action embedding e. The second factor is the variance of w(x, a) with respect to the conditional distribu- tion π0(a|x, e), which becomes large when (i) w(x, a) has a wide range or (ii) there remain large variations in a even after conditioning on action embedding e so that π0(a|x, e) remains stochastic. Therefore, MIPS becomes increasingly favorable compared to IPS for larger action spaces where the variance of w(x, a) becomes larger. Moreover, to obtain a large variance reduction, the action embedding should ideally not be unnecessarily predictive of the actions. Finally, the next theorem describes the gain in MSE we can obtain from MIPS when Assumption 3.2 is violated. Theorem 3.7. (MSE Gain of MIPS) Under Assumptions 2.1 and 3.1, we have
$$
MSE( ˆVIPS(π)) − MSE( ˆVMIPS(π))
$$
(cid:2)(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,a,e)[r2](cid:3) n = Ex,a,e∼π0
$$
+ 2V (π)Bias( ˆVMIPS(π)) + (1 − n)Bias( ˆVMIPS(π))2.
$$
(cid:16) (cid:17) See Appendix B.5 for the proof. Note that IPS can have some bias when Assumption 2.1 is not true, possibly producing a greater MSE gain for MIPS.
## 3.2. Data-Driven Embedding Selection
The analysis in the previous section implies a clear bias- variance trade-off with respect to the quality of the action embeddings. Speciﬁcally, Theorem 3.5 suggests that the action embeddings should be as informative as possible to reduce the bias when Assumption 3.2 is violated. On the other hand, Theorem 3.6 suggests that the action embed- dings should be as coarse as possible to gain a greater vari- ance reduction. Theorem 3.7 summarizes the bias-variance trade-off in terms of MSE. A possible criticism to MIPS is Assumption 3.2, as it is hard to verify whether this assumption is satisﬁed using only the observed logged data. However, the above discussion about the bias-variance trade-off implies that it might be effective to strategically violate Assumption 3.2 by discarding some embedding dimensions. This action embedding selection can lead to a large variance reduction at the cost of introduc- ing some bias, possibly improving the MSE of MIPS. To implement the action embedding selection, we can adapt the estimator selection method called SLOPE proposed in Su et al. (2020b) and Tucker & Lee (2021). SLOPE is based on Lepski’s principle for bandwidth selection in nonparametric statistics (Lepski & Spokoiny, 1997) and is used to tune the hyperparameters of OPE estimators. A beneﬁt of SLOPE is that it avoids estimating the bias of the estimator, which is as difﬁcult as OPE. Appendix C describes how to apply SLOPE to the action embedding selection in our setup, and Section 4 evaluates its beneﬁt empirically.
## 3.3. Estimating the Marginal Importance Weights
When using MIPS, we might have to estimate w(x, e) de- pending on how the embeddings are given. A simple ap- proach to this is to utilize the following transformation. w(x, e) = Eπ0(a|x,e) [w(x, a)] . (3) Eq. (3) implies that we need an estimate of π0(a|x, e), which we compute by regressing a on (x, e). We can then estimate w(x, e) as ˆw(x, e) = Eˆπ0(a|x,e) [w(x, a)].3 This procedure is easy to implement and tractable, even when the embedding space is high-dimensional and continuous. Note that, even if there are some deﬁcient actions, we can directly estimate w(x, e) by solving density ratio estimation as binary classiﬁcation as done in Sondhi et al. (2020).
# 4. Empirical Evaluation
We ﬁrst evaluate MIPS on synthetic data to identify the situa- tions where it enables a more accurate OPE. Second, we val- idate real-world applicability on data from an online fashion store. Our experiments are conducted using the OpenBandit- Pipeline (OBP)4, an open-source software for OPE provided by Saito et al. (2020). Our experiment implementation is available at https://github.com/usaito/icml2022-mips.
## 4.1. Synthetic Data
For the ﬁrst set of experiments, we create synthetic data to be able to compare the estimates to the ground-truth value of the target policies. To create the data, we sample 10- dimensional context vectors x from the standard normal distribution. We also sample de-dimensional categorical action embedding e ∈ E from the following conditional 3Appendix B.7 describes the bias and variance of MIPS with estimated marginal importance weights ˆw(x, e). 4https://github.com/st-tech/zr-obp
### Off-Policy Evaluation for Large Action Spaces via Embeddings
distribution given action a. p(e | a) = de(cid:89) k=1 (cid:80)
$$
exp(αa,ek )
$$
e(cid:48)∈Ek
$$
exp(αa,e(cid:48))
$$
, (4) which is independent of the context x in the synthetic experi- ment. {αa,ek} is a set of parameters sampled independently from the standard normal distribution. Each dimension of E has a cardinality of 10, i.e., Ek = {1, 2, . . . , 10}. We then synthesize the expected reward as ηk ·(cid:0)x(cid:62)M xek + θ(cid:62) x x + θ(cid:62) e xek (cid:1) , de(cid:88) k=1 q(x, e) = 4.1.1. BASELINES We compare our estimator with Direct Method (DM), IPS, and DR.5 We use the Random Forest (Breiman, 2001) im- plemented in scikit-learn (Pedregosa et al., 2011) along with 2-fold cross-ﬁtting (Newey & Robins, 2018) to obtain ˆq(x, e) for DR and DM. We use the Logistic Regression of scikit-learn to estimate ˆπ0(a|x, e) for MIPS. We also report the results of MIPS with the true importance weights as “MIPS (true)”. MIPS (true) provides the best performance we could achieve by improving the procedure for estimating the importance weights of MIPS. (5) 4.1.2. RESULTS so that(cid:80)de where M, θx, and θe are parameter matrices or vectors to deﬁne the expected reward. These parameters are sampled from a uniform distribution with range [−1, 1]. xek is a context vector corresponding to the k-th dimension of the action embedding, which is unobserved to the estimators. ηk speciﬁes the importance of the k-th dimension of the action embedding, which is sampled from Dirichlet distribution k=1 ηk = 1. Note that if we observe all dimen- sions of E, then q(x, e) = q(x, a, e). On the other hand, q(x, e) (cid:54)= q(x, a, e), if there are some missing dimensions, which means that Assumption 3.2 is violated. We synthesize the logging policy π0 by applying the softmax function to q(x, a) = Ep(e|a)[q(x, e)] as π0(a | x) = (cid:80)
$$
exp(β · q(x, a))
$$
$$
a(cid:48)∈A exp(β · q(x, a(cid:48)))
$$
, (6) where β is a parameter that controls the optimality and en- tropy of the logging policy. A large positive value of β leads to a near-deterministic and well-performing logging policy, while lower values make the logging policy increasingly worse. In the main text, we use β = −1, and additional results for other values of β can be found in Appendix D.2. In contrast, the target policy π is deﬁned as
$$
π(a | x) = (1 − ) · I(cid:8)a = arg max
$$
q(x, a(cid:48))(cid:9) + /|A|, a(cid:48)∈A where the noise  ∈ [0, 1] controls the quality of π. In the main text, we set  = 0.05, which produces a near-optimal and near-deterministic target policy. We share additional results for other values of  in Appendix D.2. To summarize, we ﬁrst sample context x and deﬁne the expected reward q(x, e) as in Eq. (5). We then sample discrete action a from π0 based on Eq. (6). Given action a, we sample categorical action embedding e based on Eq. (4). Finally, we sample the reward from a normal distribution with mean q(x, e) and standard deviation σ = 2.5. Iterating this procedure n times generates logged data D with n independent copies of (x, a, e, r). The following reports and discusses the MSE, squared bias, and variance of the estimators computed over 100 different sets of logged data replicated with different seeds.
## How does MIPS perform with varying numbers of ac-
tions? First, we evaluate the estimators’ performance when we vary the number of actions from 10 to 5000. The sample size is ﬁxed at n = 10000. Figure 2 shows how the number of actions affects the estimators’ MSE (both on linear- and log-scale). We observe that MIPS provides substantial improvements over IPS and DR par- ticularly for larger action sets. More speciﬁcally, when |A| = 10, MSE( ˆVIPS)
$$
= 12.38
$$
MSE( ˆVMIPS) for |A| = 5000, indicating a signiﬁcant performance im- provement of MIPS for larger action spaces as suggested in Theorem 3.6. MIPS is also consistently better than DM, which suffers from high bias. The ﬁgure also shows that MIPS (true) is even better than MIPS in large action sets, mostly due to the reduced bias when using the true marginal importance weights. This observation implies that there is room for further improvement in how to estimate the marginal importance weights. = 1.38, while MSE( ˆVIPS) MSE( ˆVMIPS)
## How does MIPS perform with varying sample sizes?
Next, we compare the estimators under varying numbers
$$
of samples (n ∈ {800, 1600, 3200, 6400, 12800, 25600}).
$$
The number of actions is ﬁxed at |A| = 1000. Figure 3 reports how the estimators’ MSE changes with the size of logged bandit data. We can see that MIPS is appeal- ing in particular for small sample sizes where it outper- forms IPS and DR by a larger margin than in large sam- 5Appendix D.2 provides more comprehensive experiment re- sults including Switch-DR (Wang et al., 2017), DR with Optimistic Shrinkage (DRos) (Su et al., 2020a), and DR-λ (Metelli et al., 2021) as additional baseline estimators. The additional experimen- tal results suggest that all of these existing estimators based on IPS weighting experience signiﬁcant accuracy deterioration with large action spaces due to either large bias or variance. Moreover, we observe that MIPS is more robust and outperforms all these baselines in a range of settings.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Figure 2. MSE (both on linear- and log-scale) with varying number of actions. Figure 3. MSE (both on linear- and log-scale) with varying number of samples. = 9.10 when n = 800, while ple regimes ( MSE( ˆVIPS) MSE( ˆVMIPS) MSE( ˆVIPS) = 4.87 when n = 25600). With the growing MSE( ˆVMIPS) sample size, MIPS, IPS, and DR improve their MSE as their variance decreases. In contrast, the accuracy of DM does not change across different sample sizes, but it performs better than IPS and DR because they converge very slowly in the presence of many actions. In contrast, MIPS is bet- ter than DM except for n = 800, as the bias of MIPS is much smaller than that of DM. Moreover, MIPS becomes increasingly better than DM with the growing sample size, as the variance of MIPS decreases while DM remains highly biased.
## How does MIPS perform with varying numbers of
deﬁcient actions? We also compare the estimators under varying numbers of deﬁcient actions (|U0| ∈ {0, 100, 300, 500, 700, 900}) with a ﬁxed action set (|A| = 1000). Figure 4 shows how the number of deﬁcient actions affects the estimators’ MSE, squared bias, and variance. The results suggest that MIPS (true) is robust and not affected by the existence of deﬁcient actions. In addition, MIPS is mostly better than DM, IPS, and DR even when there are many deﬁcient actions. However, we also observe that the gap between MIPS and MIPS (true) increases for large num- bers of deﬁcient actions due to the bias in estimating the marginal importance weights. Note that the MSE of IPS and DR decreases with increasing number of deﬁcient actions, because their variance becomes smaller with a smaller num- ber of supported actions, even though their bias increases as suggested by Sachdeva et al. (2020).
## How does MIPS perform when Assumption 3.2 is vio-
lated? Here, we evaluate the accuracy of MIPS when As- sumption 3.2 is violated. To adjust the amount of violation, we modify the action embedding space and reduce the cardi- nality of each dimension of E to 2 (i.e., Ek = {0, 1}), while we increase the number of dimensions to 20 (de = 20). This leads to |E| = 220 = 1, 048, 576, and we can now drop some dimensions to increase violation. In particular, when we observe all dimensions of E, Assumption 3.2 is perfectly satisﬁed. However, when we withhold {0, 2, 4, . . . , 18} em- bedding dimensions, the assumption becomes increasingly invalid. When many dimensions are missing, the bias of MIPS is expected to increase as suggested in Theorem 3.5, potentially leading to a worse MSE.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Figure 4. MSE, Squared Bias, and Variance with varying number of deﬁcient actions.
### Figure 5. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings.
Figure 6. MSE, Squared Bias, and Variance of MIPS w/ or w/o action embedding selection (SLOPE). Figure 5 shows how the MSE, squared bias, and variance of the estimators change with varying numbers of unobserved embedding dimensions. Somewhat surprisingly, we observe that MIPS and MIPS (true) perform better when there are some missing dimensions, even if it leads to the violated assumption. Speciﬁcally, the MSE of MIPS and MIPS (true) is minimized when there are 4 and 8 missing dimensions (out of 20), respectively. This phenomenon is due to the reduced variance. The third column of Figure 5 implies that the variance of MIPS and MIPS (true) decreases substan- tially with an increasing number of unobserved dimensions, while the bias increases with the violated assumption as ex- pected. These observations suggest that MIPS can be highly effective despite the violated assumption.
## How does data-driven embedding selection perform
combined with MIPS? The previous section showed that there is a potential to improve the accuracy of MIPS by selecting a subset of dimensions for estimating the marginal importance weights. We now evaluate whether we can ef- fectively address this embedding selection problem. Figure 6 compares the MSE, squared bias, and variance of MIPS and MIPS with SLOPE (MIPS w/ SLOPE) using the same embedding space as in the previous section. Note that we vary the sample size n and ﬁx |A| = 1000. The results suggest that the data-driven embedding selection provides a substantial improvement in MSE for small sample sizes. As shown in the second and third columns in Figure 6, the embedding selection signiﬁcantly reduces the variance at the cost of introducing some bias by strategically violating the assumption, which results in a better MSE.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
squared errors estimated with 150 different bootstrapped samples of the logged data. Note that the squared errors are normalized by that of IPS. We ﬁnd that MIPS (w/ SLOPE) outperforms IPS in about 80% of the simulation runs, while other estimators, including MIPS (w/o SLOPE), work sim- ilarly to IPS. This result demonstrates the real-world ap- plicability of our estimator as well as the importance of implementing action embedding selection in practice. We report qualitatively similar results for other sample sizes (from 10,000 to 500,000) in Appendix D.3.
# 5. Conclusion and Future Work
We explored the problem of OPE for large action spaces. In this setting, existing estimators based on IPS suffer from impractical variance, which limits their applicability. This problem is highly relevant for practical applications, as many real decision making problems such as recommender systems have to deal with a large number of discrete actions. To achieve an accurate OPE for large action spaces, we propose the MIPS estimator, which builds on the marginal importance weights computed with action embeddings. We characterize the important statistical properties of the pro- posed estimator and discuss when it is superior to the con- ventional ones. Extensive experiments demonstrate that MIPS provides a signiﬁcant gain in MSE when the vanilla importance weights become large due to large action spaces, substantially outperforming IPS and related estimators. Our work raises several interesting research questions. For example, this work assumes the existence of some prede- ﬁned action embeddings and analyzes the resulting statis- tical properties of MIPS. Even though we discussed how to choose which embedding dimensions to use for OPE (Section 3.2), it would be intriguing to develop a more prin- cipled method to optimize or learn (possibly continuous) action embeddings from the logged data for further improv- ing MIPS. Developing a method for accurately estimating the marginal importance weight would also be crucial to ﬁll the gap between MIPS and MIPS (true) observed in our ex- periments. It would also be interesting to explore off-policy learning using action embeddings and possible applications of marginal importance weighting to other estimators that depend on the vanilla importance weight such as DR.
# Acknowledgements
This research was supported in part by NSF Awards IIS- 1901168 and IIS-2008139. Yuta Saito was supported by the Funai Overseas Scholarship. All content represents the opinion of the authors, which is not necessarily shared or endorsed by their respective employers and/or sponsors. Figure 7. CDF of relative squared error w.r.t IPS. Other beneﬁts of MIPS. MIPS has additional beneﬁts over the conventional estimators. In fact, in addition to the case with many actions, IPS is also vulnerable when logging and target policies differ substantially and the reward is noisy (see Eq. (2)). Appendix D.2 empirically investigates the additional beneﬁts of MIPS with varying logging/target policies and varying noise levels with a ﬁxed action set. We observe that MIPS is substantially more robust to the changes in policies and added noise than IPS or DR, which provides further arguments for the applicability of MIPS.
## 4.2. Real-World Data
To assess the real-world applicability of MIPS, we now evaluate MIPS on real-world bandit data. In particular, we use the Open Bandit Dataset (OBD)6 (Saito et al., 2020), a publicly available logged bandit dataset collected on a large-scale fashion e-commerce platform. We use 100,000 observations that are randomly sub-sampled from the “ALL” campaign of OBD. The dataset contains user contexts x, fashion items to recommend as action a ∈ A where |A| = 240, and resulting clicks as reward r ∈ {0, 1}. OBD also includes 4-dimensional action embedding vectors such as hierarchical category information about the fashion items. The dataset consists of two sets of logged bandit data collected by two different policies (uniform random and Thompson sampling) during an A/B test of these policies. We regard uniform random and Thompson sampling as log- ging and target policies, respectively, to perform an evalua- tion of OPE estimators. Appendix D.3 describes the detailed experimental procedure to evaluate the accuracy of the esti- mators on real-world bandit data. Results. We evaluate MIPS (w/o SLOPE) and MIPS (w/ SLOPE) in comparison to DM, IPS, DR, Switch-DR, More Robust DR (Farajtabar et al., 2018), DRos, and DR-λ. We apply SLOPE to tune the built-in hyperparameters of Switch- DR, DRos, and DR-λ. Figure 7 compares the estimators by drawing the cumulative distribution function (CDF) of their 6https://research.zozo.com/data.html
### Off-Policy Evaluation for Large Action Spaces via Embeddings
# References
Agrawal, R. The continuum-armed bandit problem. SIAM journal on control and optimization, 33(6):1926–1951, 1995. Agrawal, S. and Goyal, N. Thompson sampling for contex- tual bandits with linear payoffs. In International Confer- ence on Machine Learning, pp. 127–135. PMLR, 2013. Athey, S., Chetty, R., Imbens, G. W., and Kang, H. The sur- rogate index: Combining short-term proxies to estimate long-term treatment effects more rapidly and precisely. Technical report, National Bureau of Economic Research, 2019. Athey, S., Chetty, R., and Imbens, G. Combining experimen- tal and observational data to estimate treatment effects on long term outcomes. arXiv preprint arXiv:2006.09676, 2020. Borisov, A., Markov, I., De Rijke, M., and Serdyukov, P. A neural click model for web search. In Proceedings of the 25th International Conference on World Wide Web, pp. 531–541, 2016. Breiman, L. Random forests. Machine learning, 45(1): 5–32, 2001. Bubeck, S., Munos, R., Stoltz, G., and Szepesv´ari, C. X- armed bandits. Journal of Machine Learning Research, 12(5), 2011. Chandak, Y., Theocharous, G., Kostas, J., Jordan, S., and Thomas, P. Learning action representations for reinforce- ment learning. In International Conference on Machine Learning, pp. 941–950. PMLR, 2019. Chen, J. and Ritzwoller, D. M. Semiparametric esti- mation of long-term treatment effects. arXiv preprint arXiv:2107.14405, 2021. Chu, W., Li, L., Reyzin, L., and Schapire, R. Contextual In Proceedings bandits with linear payoff functions. of the Fourteenth International Conference on Artiﬁcial Intelligence and Statistics, pp. 208–214. JMLR Workshop and Conference Proceedings, 2011. Chuklin, A., Markov, I., and Rijke, M. d. Click models for web search. Synthesis lectures on information concepts, retrieval, and services, 7(3):1–115, 2015. Demirer, M., Syrgkanis, V., Lewis, G., and Chernozhukov, V. Semi-parametric efﬁcient policy learning with continu- ous actions. Advances in Neural Information Processing Systems, 32, 2019. Dud´ık, M., Erhan, D., Langford, J., and Li, L. Doubly robust policy evaluation and optimization. Statistical Science, 29(4):485–511, 2014. Dulac-Arnold, G., Denoyer, L., Preux, P., and Gallinari, P. Fast reinforcement learning with large action sets using error-correcting output codes for mdp factoriza- tion. In Joint European Conference on Machine Learning and Knowledge Discovery in Databases, pp. 180–194. Springer, 2012. Dulac-Arnold, G., Evans, R., van Hasselt, H., Sunehag, P., Lillicrap, T., Hunt, J., Mann, T., Weber, T., Degris, T., and Coppin, B. Deep reinforcement learning in large discrete action spaces. arXiv preprint arXiv:1512.07679, 2015. Farajtabar, M., Chow, Y., and Ghavamzadeh, M. More robust doubly robust off-policy evaluation. In Proceed- ings of the 35th International Conference on Machine Learning, volume 80, pp. 1447–1456. PMLR, 2018. Guo, F., Liu, C., and Wang, Y. M. Efﬁcient multiple-click models in web search. In Proceedings of the 2nd ACM In- ternational Conference on Web Search and Data Mining, pp. 124–131, 2009. Guo, R., Zhao, X., Henderson, A., Hong, L., and Liu, H. Debiasing grid-based product search in e-commerce. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 2852–2860, 2020. Horvitz, D. G. and Thompson, D. J. A generalization of sam- pling without replacement from a ﬁnite universe. Journal of the American statistical Association, 47(260):663–685, 1952. Jiang, N. and Li, L. Doubly robust off-policy value eval- In Proceedings of uation for reinforcement learning. the 33rd International Conference on Machine Learning, volume 48, pp. 652–661. PMLR, 2016. Kallus, N. and Mao, X. On the role of surrogates in the efﬁ- cient estimation of treatment effects with limited outcome data. arXiv preprint arXiv:2003.12408, 2020. Kallus, N. and Uehara, M. Double reinforcement learn- ing for efﬁcient off-policy evaluation in markov decision processes. J. Mach. Learn. Res., 21:167–1, 2020. Kallus, N. and Zhou, A. Policy evaluation and optimization with continuous treatments. In International Conference on Artiﬁcial Intelligence and Statistics, pp. 1243–1251. PMLR, 2018. Kallus, N., Saito, Y., and Uehara, M. Optimal off-policy evaluation from multiple logging policies. In Proceed- ings of the 38th International Conference on Machine Learning, volume 139, pp. 5247–5256. PMLR, 2021.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Kiyohara, H., Saito, Y., Matsuhiro, T., Narita, Y., Shimizu, N., and Yamamoto, Y. Doubly robust off-policy eval- uation for ranking policies under the cascade behavior model. In Proceedings of the 15th International Confer- ence on Web Search and Data Mining, 2022. Kleinberg, R. Nearly tight bounds for the continuum-armed bandit problem. Advances in Neural Information Process- ing Systems, 17:697–704, 2004. Kleinberg, R., Slivkins, A., and Upfal, E. Bandits and experts in metric spaces. Journal of the ACM (JACM), 66 (4):1–77, 2019. Krishnamurthy, A., Langford, J., Slivkins, A., and Zhang, C. Contextual bandits with continuous actions: Smooth- ing, zooming, and adapting. In Conference on Learning Theory, pp. 2025–2027. PMLR, 2019. Lepski, O. V. and Spokoiny, V. G. Optimal pointwise adap- tive methods in nonparametric estimation. The Annals of Statistics, pp. 2512–2546, 1997. Li, S., Abbasi-Yadkori, Y., Kveton, B., Muthukrishnan, S., Vinay, V., and Wen, Z. Ofﬂine evaluation of ranking policies with click models. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 1685–1694, 2018. inﬁnite-horizon off-policy estimation. Liu, Q., Li, L., Tang, Z., and Zhou, D. Breaking the curse In of horizon: Proceedings of the 32nd International Conference on Neural Information Processing Systems, pp. 5361–5371, 2018. Liu, Y., Bacon, P.-L., and Brunskill, E. Understanding the curse of horizon in off-policy evaluation via conditional importance sampling. In International Conference on Machine Learning, pp. 6184–6193. PMLR, 2020a. Liu, Y., Swaminathan, A., Agarwal, A., and Brunskill, E. Off-policy policy gradient with stationary distribution correction. In Uncertainty in Artiﬁcial Intelligence, pp. 1180–1190. PMLR, 2020b. Lopez, R., Dhillon, I. S., and Jordan, M. I. Learning from extreme bandit feedback. Proc. Association for the Ad- vancement of Artiﬁcial Intelligence, 2021. McInerney, J., Brost, B., Chandar, P., Mehrotra, R., and Carterette, B. Counterfactual evaluation of slate recom- mendations with sequential reward interactions. In Pro- ceedings of the 26th ACM SIGKDD International Con- ference on Knowledge Discovery and Data Mining, pp. 1779–1788, 2020. Metelli, A. M., Russo, A., and Restelli, M. Subgaussian and differentiable importance sampling for off-policy eval- uation and learning. Advances in Neural Information Processing Systems, 34, 2021. Narita, Y., Yasui, S., and Yata, K. Efﬁcient counterfactual learning from bandit feedback. In Proceedings of the AAAI Conference on Artiﬁcial Intelligence, volume 33, pp. 4634–4641, 2019. Newey, W. K. and Robins, J. R. Cross-ﬁtting and fast remainder rates for semiparametric estimation. arXiv preprint arXiv:1801.09138, 2018. Pazis, J. and Parr, R. Generalized value functions for large action sets. In Proceedings of the 28th International Con- ference on International Conference on Machine Learn- ing, pp. 1185–1192, 2011. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cour- napeau, D., Brucher, M., Perrot, M., and ´Edouard Duch- esnay. Scikit-learn: Machine learning in python. Journal of Machine Learning Research, 12:2825–2830, 2011. Sachdeva, N., Su, Y., and Joachims, T. Off-policy ban- dits with deﬁcient support. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 965–975, 2020. Saito, Y. Doubly robust estimator for ranking metrics with post-click conversions. In 14th ACM Conference on Rec- ommender Systems, pp. 92–100, 2020. Saito, Y., Aihara, S., Matsutani, M., and Narita, Y. Open bandit dataset and pipeline: Towards realistic and reproducible off-policy evaluation. arXiv preprint arXiv:2008.07146, 2020. Saito, Y., Udagawa, T., Kiyohara, H., Mogi, K., Narita, Y., and Tateno, K. Evaluating the robustness of off-policy evaluation. In Proceedings of the 15th ACM Conference on Recommender Systems, pp. 114–123, 2021. Slivkins, A. Introduction to multi-armed bandits. arXiv preprint arXiv:1904.07272, 2019. Sondhi, A., Arbour, D., and Dimmery, D. Balanced off- policy evaluation in general action spaces. In Interna- tional Conference on Artiﬁcial Intelligence and Statistics, pp. 2413–2423. PMLR, 2020. Su, Y., Wang, L., Santacatterina, M., and Joachims, T. Cab: Continuous adaptive blending for policy evaluation and learning. In International Conference on Machine Learn- ing, volume 84, pp. 6005–6014, 2019.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Voloshin, C., Le, H. M., Jiang, N., and Yue, Y. Empirical study of off-policy policy evaluation for reinforcement learning. arXiv preprint arXiv:1911.06854, 2019. Wang, Y.-X., Agarwal, A., and Dudık, M. Optimal and adaptive off-policy evaluation in contextual bandits. In International Conference on Machine Learning, pp. 3589– 3597. PMLR, 2017. Xie, T., Ma, Y., and Wang, Y.-X. Towards optimal off-policy evaluation for reinforcement learning with marginalized importance sampling. In Advances in Neural Information Processing Systems, pp. 9665–9675, 2019. Su, Y., Dimakopoulou, M., Krishnamurthy, A., and Dud´ık, M. Doubly robust off-policy evaluation with shrinkage. In Proceedings of the 37th International Conference on Machine Learning, volume 119, pp. 9167–9176. PMLR, 2020a. Su, Y., Srinath, P., and Krishnamurthy, A. Adaptive es- timator selection for off-policy evaluation. In Interna- tional Conference on Machine Learning, pp. 9196–9205. PMLR, 2020b. Swaminathan, A. and Joachims, T. Batch learning from logged bandit feedback through counterfactual risk min- imization. The Journal of Machine Learning Research, 16(1):1731–1755, 2015a. Swaminathan, A. and Joachims, T. Counterfactual risk minimization: Learning from logged bandit feedback. In International Conference on Machine Learning, pp. 814–823. PMLR, 2015b. Swaminathan, A. and Joachims, T. The self-normalized estimator for counterfactual learning. Advances in Neural Information Processing Systems, 28, 2015c. Swaminathan, A., Krishnamurthy, A., Agarwal, A., Dudik, M., Langford, J., Jose, D., and Zitouni, I. Off-policy In Advances in evaluation for slate recommendation. Neural Information Processing Systems, volume 30, pp. 3632–3642, 2017. Tennenholtz, G. and Mannor, S. The natural language of ac- tions. In International Conference on Machine Learning, pp. 6196–6205. PMLR, 2019. Thomas, P. and Brunskill, E. Data-efﬁcient off-policy policy evaluation for reinforcement learning. In Proceedings of the 33rd International Conference on Machine Learning, volume 48, pp. 2139–2148. PMLR, 2016. Thomas, P., Theocharous, G., and Ghavamzadeh, M. High conﬁdence policy improvement. In Proceedings of the 32th International Conference on Machine Learning, pp. 2380–2388, 2015. Tucker, G. and Lee, J. Improved estimator selection for off- policy evaluation. Workshop on Reinforcement Learning Theory at the 38th International Conference on Machine Learning, 2021. Van Hasselt, H. and Wiering, M. A. Using continuous action spaces to solve discrete problems. In 2009 International Joint Conference on Neural Networks, pp. 1149–1156. IEEE, 2009. Vlassis, N., Chandrashekar, A., Gil, F. A., and Kallus, N. Control variates for slate off-policy evaluation. Advances in Neural Information Processing Systems, 34, 2021.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
# A. Related Work
Off-Policy Evaluation: Off-policy evaluation of counterfactual policies has extensively been studied in both contextual bandits (Dud´ık et al., 2014; Wang et al., 2017; Liu et al., 2018; Farajtabar et al., 2018; Su et al., 2019; 2020a; Kallus et al., 2021; Metelli et al., 2021) and reinforcement learning (RL) (Jiang & Li, 2016; Thomas & Brunskill, 2016; Xie et al., 2019; Kallus & Uehara, 2020; Liu et al., 2020a). There are three main approaches in the literature. The ﬁrst approach is DM, which estimates the policy value based on the estimated reward ˆq. DM has a lower variance than IPS, and is also proposed as an approach to deal with support deﬁcient data (Sachdeva et al., 2020) where IPS is biased. A drawback is that it is susceptible to misspeciﬁcation of the reward function. This misspeciﬁcation issue is problematic, as the extent of misspeciﬁcation cannot be easily evaluated for real-world data (Farajtabar et al., 2018; Voloshin et al., 2019). The second approach is IPS, which estimates the value of a policy by applying importance weighting to the observed reward. With some assumptions for identiﬁcation such as common support, IPS is unbiased and consistent. However, IPS can suffer from high bias and variance when the action space is large. It can have a high bias when the logging policy fails to satisfy the common support condition, which is likely to occur for large action spaces (Sachdeva et al., 2020). Variance is also a critical issue especially when the action space is large, as the importance weights are likely to take larger values. The weight clipping (Swaminathan & Joachims, 2015b; Su et al., 2019; 2020a) and normalization (Swaminathan & Joachims, 2015c) are often used to address the variance issue, but they produce additional bias. Thus, DR has gained particular attention as the third approach. This estimator is a hybrid of the previous two approaches, and can achieve a lower bias than DM, and a lower variance than IPS (Dud´ık et al., 2014; Farajtabar et al., 2018). It can also achieve the lowest possible asymptotic variance, a property known as efﬁciency (Narita et al., 2019). Several recent works have extended DR to improve its performance with small samples (Wang et al., 2017; Su et al., 2020a) or under model misspeciﬁcation (Farajtabar et al., 2018). Though there are a number of extensions of DR both in bandits (as described above) and RL (Jiang & Li, 2016; Thomas & Brunskill, 2016; Kallus & Uehara, 2020), none of them tackle the large discrete action space. Demirer et al. (2019) describe an estimator for ﬁnitely many possible actions as a special case of their main proposal, which is for continuous action spaces. However, this method is based on a linearity assumption of the reward function, which rarely holds in practice. Moreover, the bias arises from violating the assumption and the variance reduction due to the additional assumption are not analyzed. Kallus & Zhou (2018) formulate the problem of OPE for continuous action spaces and propose some estimators building on the kernel smoothing in nonparametric statistics. Speciﬁcally, kernel functions are used to infer the rewards among similar continuous actions where the bias-variance trade-off is controlled by a bandwidth hyperparameter. If every dimension of the action embedding space E is continuous, the continuous-action estimators of Kallus & Zhou (2018) might be applied to our setup under smoothness assumption. However, this naive application can suffer from the curse of dimensionality where the kernel smoothing performs dramatically worse as the number of embedding dimensions increases. In contrast, MIPS avoids the curse of dimensionality by estimating the marginal importance weights via supervised classiﬁcation as in Section 3.3. Note that there is an estimator called marginalized importance sampling in OPE of RL (Liu et al., 2018; Xie et al., 2019; Liu et al., 2020b). This method estimates the state marginal distribution and applies importance weighting with respect to this marginal distribution rather than the trajectory distribution. Although marginalization is a key trick of this estimator, it is aimed at resolving the curse of horizon, a problem speciﬁc to RL. In contrast, our approach utilizes the marginal distribution over action embeddings to deal with large action spaces. Applications of our estimator are not limited to RL. Off-Policy Evaluation for Slate and Ranking Policies: Another line of work that shares the similar motivation to ours is OPE of slate or ranking policies (Swaminathan et al., 2017; Li et al., 2018; McInerney et al., 2020; Saito, 2020; Su et al., 2020a; Vlassis et al., 2021; Lopez et al., 2021; Kiyohara et al., 2022). In this setting, the estimators have to handle the combinatorial action space, which could be very large even if the number of unique actions is not. Therefore, some additional assumptions are imposed to make the combinatorial action space tractable. A primary problem setting in this direction is OPE for slate bandit policies, where it is assumed that only a single, slate-level reward is observed for each data. Swaminathan et al. (2017) tackle this setting by positing a linearity assumption on the reward function. The proposed pseudoinverse (PI) estimator was shown to provide an exponential gain in the sample complexity over IPS. Following this seminal work, Su et al. (2020a) extend their Doubly Robust with Optimistic Shrinkage, originally proposed for the general OPE problem, to the slate action case. Vlassis et al. (2021) improve the PI estimator by optimizing a set of control variates. Although PI is compelling, applications of this class of estimators are limited to the speciﬁc problem of slate bandits. On the other hand, our framework is more general and applicable not only to slate bandits, but also to other problem instances including OPE for ranking policies with observable slot-level rewards (described below) or general contextual bandits with large action spaces. In addition, all estimators for slate bandits rely on the linearity assumption, while our MIPS builds on a different assumption about the quality of the action embedding.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Another similar setting is OPE for ranking policies where it is assumed that the rewards for every slot in a ranking (slot-level rewards) are observable, a setting also known as semi-bandit feedback. PI and its variants discussed above are applicable to this setting, but McInerney et al. (2020) empirically verify that the PI estimators do not work well, as they do not utilize additional information about the slot-level rewards. To leverage slot-level rewards to further improve OPE, assumptions are made to capture different types of user behaviors to control the bias-variance trade-off in OPE. For example, Li et al. (2018) assume that users interact with items presented in different positions of a ranking totally independently. In contrast, McInerney et al. (2020) and Kiyohara et al. (2022) assume that users go down a ranking from top to bottom. These assumptions correspond to click models such as cascade model in information retrieval (Guo et al., 2009; Chuklin et al., 2015) and are useful in reducing the variance. However, whether these assumptions are reasonable depends highly on a ranking interface and real user behavior. If the assumption fails to capture real user behavior, this approach can produce unexpected bias. For example, the cascade model is only applicable when a ranking interface is vertical, however, real-world ranking interfaces are often more complex (Guo et al., 2020). Moreover, real-world user behaviors are often too diverse to model with a single, universal assumption (Borisov et al., 2016). In contrast, our approach is applicable to any ranking interfaces, once they are represented as action embeddings, without assuming any particular user behavior. Moreover, ours is more general in that its application is not limited to information retrieval and recommender systems, but includes robotics, education, conversational agents, or personalized medicine where click models are not applicable. Reinforcement Learning for Large Action Spaces: Although we focus on OPE, there have been several attempts to enable high-performance policy learning for large action spaces. A typical approach is to factorize the action space into binary sub-spaces (Pazis & Parr, 2011; Dulac-Arnold et al., 2012). For example, Pazis & Parr (2011) represent each action with a binary format and train a value function for each bit. On the other hand, Van Hasselt & Wiering (2009) and Dulac-Arnold et al. (2015) assume the existence of continuous representations of discrete actions as prior knowledge. They perform policy gradients with the continuous actions and search the nearest discrete action. Similar to these works, we assume the existence of some predeﬁned action embeddings and propose to use that prior information to enable an accurate OPE for large action spaces. We also analyze the bias-variance trade-off of the resulting estimator and relate it to the quality of the action embeddings. Some recent works also tackle how to learn useful action representations from only available data. Tennenholtz & Mannor (2019) achieve this by leveraging expert demonstrations, while Chandak et al. (2019) perform supervised learning to predict the state transitions and obtain action representations with no prior knowledge. Following these works, it may be valuable to develop an algorithm to optimize or learn (possibly continuous) action embeddings from the data to further improve OPE for large action spaces. Multi-Armed Bandits with Side Information: There are two prominent approaches to deal with large or inﬁnite action spaces in the online bandit literature (Krishnamurthy et al., 2019; Slivkins, 2019). The ﬁrst one is the parametric approach such as linear or combinatorial bandits, which assumes that the expected reward can be represented as a parametric function of the action such as a linear function (Chu et al., 2011; Agrawal & Goyal, 2013). There is also a nonparametric approach, which typically makes much weaker assumptions about the rewards, e.g., Lipschitz assumptions. Lipschitz bandits have been studied to address large, structured action spaces such as the [0, 1] interval, where the applications range from dynamic pricing to ad auction. A basic idea in this literature is that similar arms should have similar quality, as per Lipschitz-continuity or some corresponding assumptions on the structure of the action space. The Lipschitz assumption was introduced by Agrawal (1995) to the bandit setting. Kleinberg (2004) optimally solve this problem in the worst case. Kleinberg et al. (2019) and Bubeck et al. (2011) rely on the zooming algorithms, which gradually zoom in to the more promising regions of the action space to achieve data-dependent regret bounds. Further works extend this direction by relaxing the assumptions with various local deﬁnitions, as well as incorporating contexts into account, as surveyed in Section 4 of Slivkins (2019). Causal Inference with Surrogates: From a statistical standpoint, causal inference with surrogates is also related (Athey et al., 2019; 2020; Kallus & Mao, 2020; Chen & Ritzwoller, 2021). Its aim is to identify and estimate the causal effect of some treatments (e.g., job training) on a primary outcome, which is unobservable without waiting for decades (e.g., lifetime earnings) (Athey et al., 2019). Instead of waiting for a long period to collect the data, these works assume the availability of surrogate outcomes such as test scores and college attendance rates, which could be observed in a much shorter period. In particular, Athey et al. (2019) build on what is called the surrogacy condition to identify the average treatment effect of treatments on the primary outcome. The surrogacy condition is analogous to Assumption 3.2 and states that there should not be any direct effect of treatments on the primary outcome. Although our formulation and assumptions share a similar structure, we would argue that our motivation is to enable an accurate OPE of decision making policies for large action spaces, which is quite different from identifying the average causal effect of binary treatments on a long-term outcome.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
# B. Proofs, Derivations, and Additional Analysis
## B.1. Proof of Proposition 3.3
Proof. V (π) = Ep(x)π(a|x)p(e|x,a)[q(x, a, e)] = Ep(x)π(a|x)p(e|x,a)[q(x, e)] a∈A (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) e∈E e∈E = Ep(x) = Ep(x) = Ep(x) π(a|x) p(e|x, a) · q(x, e) q(x, e) · π(a|x) · p(e|x, a) (cid:88) (cid:32)(cid:88) e∈E a∈A (cid:35) p(e|x, π) · q(x, e) (cid:35) (cid:33)(cid:35) (7) (8) where we use Assumption 3.2 in Eq. (7) and p(e|x, π) =(cid:80) = Ep(x)p(e|x,π)[q(x, e)] = Ep(x)p(e|x,π)p(r|x,e)[r] a∈A π(a|x)p(e|x, a) in Eq. (8).
## B.2. Proof of Proposition 3.4
Proof. From the linearity of expectation, we have ED[ ˆVMIPS(π;D)] = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r]. Thus, we calculate only the expectation of w(x, e)r (RHS of the equation) below. Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r] = Ep(x)π0(a|x)p(e|x,a)[w(x, e) · q(x, a, e)] = Ep(x)π0(a|x)p(e|x,a)[w(x, e) · q(x, e)] = Ep(x) p(e|x, a) π0(a|x) (cid:88) e∈E (cid:35) q(x, e) p(e|x, π) p(e|x, π0) (cid:32)(cid:88) a∈A (cid:35) · p(e|x, π0) · q(x, e) · q(x, e) · p(e|x, a) · π0(a|x) (cid:33)(cid:35) a∈A (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) e∈E = Ep(x) = Ep(x) p(e|x, π) p(e|x, π0) p(e|x, π) p(e|x, π0) = Ep(x)p(e|x,π)[q(x, e)] = Ep(x)p(e|x,π)p(r|x,e)[r]
$$
= V (π)
$$
e∈E (9) (10) a∈[m] g(a) = 1, we have where we use Assumption 3.2 in Eq. (9) and p(e|x, π0) =(cid:80) Lemma B.1. For real-valued, bounded functions f : N → R, g : N → R, h : N → R where(cid:80) a∈A π0(a|x)p(e|x, a) in Eq. (10). To prove Theorem 3.5, we ﬁrst state a lemma.
## B.3. Proof of Theorem 3.5
(cid:88) a∈[m] (cid:16) h(a) − (cid:88) b∈[m] (cid:17) (cid:88) a<b≤m f (a)g(a) g(b)h(b)
$$
=
$$
$$
g(a)g(b)(h(a) − h(b))(f (a) − f (b))
$$
(11)
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Proof. We prove this lemma via induction. First, we show the m = 2 case below.
$$
f (1)g(1) (h(1) − (g(1)h(1) + g(2)h(2))) + f (2)g(2) (h(2) − (g(1)h(1) + g(2)h(2)))
$$
$$
= f (1)g(1)h(1) − f (1)g(1)(g(1)h(1) + g(2)h(2)) + f (2)g(2)h(2) − f (2)g(2)(g(1)h(1) + g(2)h(2))
$$
$$
= f (1)g(1)h(1) − f (1)g(1)((1 − g(2))h(1) + g(2)h(2)) + f (2)g(2)h(2) − f (2)g(2)(g(1)h(1) + (1 − g(1))h(2))
$$
$$
= −f (1)g(1)(−g(2)h(1) + g(2)h(2)) − f (2)g(2)(g(1)h(1) − g(1)h(2))
$$
$$
= −f (1)g(1)g(2)(h(2) − h(1)) + f (2)g(1)g(2)(h(2) − h(1))
$$
$$
= g(1)g(2)(h(2) − h(1))(f (2) − f (1))
$$
Note that g(1) + g(2) = 1 from the statement. Next, we assume Eq. (11) is true for the m = k − 1 case and show that it is also true for the m = k case. First, note that (cid:88) (cid:88) a<b≤k
$$
=
$$
a<b≤k−1
$$
g(a)g(b)(h(a) − h(b))(f (a) − f (b))
$$
$$
g(a)g(b)(h(a) − h(b))(f (a) − f (b)) +
$$
(cid:88) a∈[k−1]
$$
g(a)g(k)(h(a) − h(k))(f (a) − f (k))
$$
(cid:17) Then, we have a∈[k] (cid:16) g(b)h(b)
$$
=
$$
$$
=
$$
$$
=
$$
b∈[k] b∈[k] a∈[k−1] a∈[k−1] a∈[k−1] f (a)g(a) f (a)g(a) f (a)g(a) f (a)g(a) (cid:88) (cid:88) (cid:88) (cid:88) (cid:88) h(a) − (cid:88) (cid:16) h(a) − (cid:88) (cid:16) h(a) − (cid:88) (cid:16) h(a) − (cid:88) (cid:16) h(a) − (cid:88) (cid:88)
$$
=(cid:0)1 − g(k)(cid:1) (cid:88)
$$
(cid:88)
$$
=(cid:0)1 − g(k)(cid:1)2 (cid:88)
$$
a∈[k−1] − g(k)h(k) − g(k)h(k) f (a)g(a)
$$
f (a)˜g(a)
$$
$$
f (a)˜g(a)
$$
a∈[k−1] a∈[k−1] a∈[k−1] b∈[k−1] b∈[k−1]
$$
=
$$
b∈[k−1] b∈[k] (cid:17) (cid:17) g(b)h(b) g(b)h(b) g(b)h(b) g(b)h(b) g(b)h(b) a∈[k−1]
$$
+ f (k)g(k)
$$
(cid:16) h(k) − (cid:88)
$$
 + f (k)g(k)h(k) − f (k)g(k)
$$
(cid:17) − g(k)h(k) (cid:17) − g(k)h(k) (cid:88) (cid:17) (cid:0)1 − g(k)(cid:1)(cid:16) (cid:16) h(a) − (cid:88) (cid:88) h(a) − (cid:88) (cid:88) (cid:88) (cid:88) 
$$
+ g(k)h(a)
$$
a∈[k−1] a∈[k−1]
$$
˜g(b)h(b)
$$
$$
˜g(b)h(b)
$$
b∈[k−1] b∈[k−1] (cid:17) (cid:17) f (a)g(a) − f (k)g(k) a∈[k−1] a∈[k−1] (cid:88)
$$
+ g(k)
$$
a∈[k−1] a∈[k−1] f (a)g(a)h(a) − g(k)h(k)
$$
f (a)g(a) + f (k)h(k)g(k) − f (k)g(k)
$$
g(a)h(a) − f (k)g(k)h(k)
$$
f (a)g(a) + f (k)h(k)g(k) − f (k)g(k)
$$
g(a)h(a) − f (k)g(k)g(k)h(k) where we use g(k) = 1 −(cid:80)
$$
a∈[k−1] g(a) and deﬁne ˜g(a) := g(a)/((cid:80)
$$
$$
a∈[k−1] g(a)) = g(a)/(1 − g(k)).
$$
(cid:88) a∈[k] g(a)h(a) (cid:88) a∈[k]
$$
f (a)g(a) + f (k)g(k)h(k) − f (k)g(k)
$$
g(a)h(a) 1 − (cid:88) a∈[k−1]  g(a) (cid:88) a∈[k−1] g(a) (12)
$$
g(a)h(a) + f (k)g(k)h(k)
$$
The ﬁrst term of Eq. (12) is the m = k − 1 case, so we have the following from the assumption of induction.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
(cid:16) h(a) − (cid:88) b∈[k−1]
$$
f (a)˜g(a)
$$
$$
˜g(b)h(b)
$$
(cid:17)
$$
=(cid:0)1 − g(k)(cid:1)2 (cid:88)
$$
(cid:88) a<b≤k−1
$$
=
$$
a<b≤k−1
$$
˜g(a)˜g(b)(h(a) − h(b))(f (a) − f (b))
$$
$$
g(a)g(b)(h(a) − h(b))(f (a) − f (b))
$$
(cid:0)1 − g(k)(cid:1)2 (cid:88) Note that(cid:80) a∈[k−1] a∈[k−1] ˜g(a) = 1. Rearranging the remaining terms of Eq. (12) yields (cid:16) h(a) − (cid:88) b∈[k] (cid:17) g(b)h(b) (cid:88) a∈[k]
$$
=
$$
f (a)g(a) (cid:88) a<b≤k−1 (cid:88) a∈[k−1]
$$
g(a)g(b)(h(a) − h(b))(f (a) − f (b)) +
$$
$$
g(a)g(k)(h(a) − h(k))(f (a) − f (k))
$$
Implying that the m = k case is true if the m = k − 1 case is true. We then use the above Lemma to prove Theorem 3.5. Proof. Bias( ˆVMIPS(π)) = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r] − V (π) p(e|x, a) · q(x, a, e) (cid:35) (13) (cid:34)(cid:88) (cid:34)(cid:88) = Ep(x)π0(a|x)p(e|x,a)[w(x, e) · q(x, a, e)] − Ep(x)π(a|x)p(e|x,a)[q(x, a, e)] (cid:35) = Ep(x)π0(a|x) p(e|x, a) · w(x, e) · q(x, a, e) − Ep(x)π(a|x) (cid:35) p(e|x, π0) · π0(a|x, e) e∈E · w(x, e) · q(x, a, e) e∈E π0(a|x) = Ep(x) π0(a|x) p(e|x, π0) · π0(a|x, e) π0(a|x) − Ep(x) π(a|x) e∈E a∈A p(e|x, π0) · w(x, e) = Ep(x) (cid:88) a∈A · q(x, a, e) (cid:35) π0(a|x, e) · q(x, a, e) (cid:88) (cid:88) e∈E a∈A (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) e∈E p(e|x, π0) w(x, a) · π0(a|x, e) · q(x, a, e) (cid:35) (cid:35) (cid:35) π0(a|x, e) · q(x, a, e) a∈A w(x, a) · π0(a|x, e) · q(x, a, e) a∈A w(x, a) · π0(a|x, e) (cid:88) b∈A (cid:35) (cid:35) (cid:35) π0(b|x, e) · q(x, b, c) − Ep(x) e∈E = Ep(x)p(e|x,π0) (cid:34) − Ep(x)p(e|x,π0) = Ep(x)p(e|x,π0) (cid:88) (cid:88) a∈A w(x, e) (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) a∈A a∈A − Ep(x)p(e|x,π0) w(x, a) · π0(a|x, e) · q(x, a, e) = Ep(x)p(e|x,π0) a∈A w(x, a) · π0(a|x, e) · (cid:32)(cid:16)(cid:88) b∈A (14) (cid:33)(cid:35) (cid:17) − q(x, a, e) π0(b|x, e) · q(x, b, c) where we use p(e|x, a) = p(e|x,π0)π0(a|x,e) By applying Lemma A.1 to the last line (setting f (a) = w(·, a), g(a) = π0(a|·,·), h(a) = q(·, a,·)), we get the ﬁnal expression of the bias. in Eq. (13) and w(x, e) = Eπ0(a|x,e)[w(x, a)] in Eq. (14). π0(a|x)
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## B.4. Proof of Theorem 3.6
Proof. Under Assumptions 2.1, 3.1, and 3.2, IPS and MIPS are both unbiased. Thus, the difference in their variance is attributed to the difference in their second moment, which is calculated below. Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, a)r] − Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r] = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, a)2 · r2] − Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)2 · r2] = Ep(x)π0(a|x)p(e|x,a) = Ep(x)π0(a|x)p(e|x,a) π0(a|x) = Ep(x) (cid:2)w(x, a)2 · Ep(r|x,a,e)[r2](cid:3) − Ep(x)π0(a|x)p(e|x,a) (cid:2)w(x, e)2 · Ep(r|x,a,e)[r2](cid:3) (cid:2)(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,e)[r2](cid:3) (cid:35) (cid:88) p(e|x, a) ·(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,e)[r2] (cid:88) π0(a|x, e) ·(cid:0)w(x, a)2 − w(x, e)2(cid:1)(cid:35) (cid:88) (cid:33)(cid:35) (cid:32)(cid:16)(cid:88) π0(a|x, e) · w(x, a)2(cid:17) − w(x, e)2 (cid:35) ·(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,e)[r2] (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) p(e|x, π0) · Ep(r|x,e)[r2] = Ep(x) = Ep(x) p(e|x, π0) · π0(a|x, e) Ep(r|x,e)[r2] · = Ep(x)p(e|x,π0) π0(a|x) π0(a|x) (cid:34) a∈A a∈A a∈A e∈E e∈E e∈E a∈A (15) (16) where we use Assumption 3.2 in Eq. (15), p(e|x, a) = p(e|x,π0)π0(a|x,e) π0(a|x) in Eq. (16). Here, we have (cid:33) (cid:32)(cid:88) (cid:33)2 π0(a|x, e) · w(x, a)2 (cid:2)w(x, a)2(cid:3) −(cid:0)Eπ0(a|x,e) [w(x, a)](cid:1)2 a∈A − π0(a|x, e) · w(x, a) = Eπ0(a|x,e)
$$
= Vπ0(a|x,e) [w(x, a)]
$$
(cid:32)(cid:88) a∈A π0(a|x, e) · w(x, a)2 − w(x, e)2 = (cid:33) (cid:32)(cid:88) a∈A where w(x, e) = Eπ0(a|x,e)[w(x, a)]. Therefore, Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, a)2 · r2] − Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)2 · r2] = Ep(x)p(e|x,π0) π0(a|x, e) · w(x, a)2(cid:17) − w(x, e)2 Ep(r|x,e)[r2] · (cid:32)(cid:16)(cid:88) (cid:34) (cid:2)Ep(r|x,e)[r2] · Vπ0(a|x,e) [w(x, a)](cid:3) a∈A = Ep(x)p(e|x,π0) (cid:33)(cid:35) Finally, as samples are independent, nVD[ ˆVIPS(π;D)] = Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, a)r] and nVD[ ˆVMIPS(π;D)] = Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r] .
## B.5. Proof of Theorem 3.7
Proof. First, we express the MSE gain of MIPS over the vanilla IPS with their bias and variance as follows.
$$
MSE(cid:0) ˆVIPS(π)(cid:1) − MSE(cid:0) ˆVMIPS(π)(cid:1) = VD[ ˆVIPS(π;D)] − VD[ ˆVMIPS(π;D)] − Bias( ˆVMIPS(π))2
$$
$$
MSE(cid:0) ˆVIPS(π)(cid:1) − MSE(cid:0) ˆVMIPS(π)(cid:1)(cid:17)
$$
(cid:16)
$$
= Vx,a,r[w(x, a)r] − Vx,e,r[w(x, e)r] − nBias( ˆVMIPS(π))2
$$
Since the samples are assumed to be independent, we can simply rescale the MSE gain as follows. n
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Below, we calculate the difference in variance. Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, a)r] − Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r] = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, a)2 · r2] − V (π)2 (cid:16) − (cid:18) Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)2 · r2] −(cid:16)
$$
V (π) + Bias( ˆVMIPS(π))
$$
(cid:2)(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,a,e)[r2](cid:3) − V (π)2 +
$$
(cid:2)(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,a,e)[r2](cid:3) + 2V (π)Bias( ˆVMIPS(π)) + Bias( ˆVMIPS(π))2
$$
(cid:17)2(cid:19)
$$
V (π)2 + 2V (π)Bias( ˆVMIPS(π)) + Bias( ˆVMIPS(π))2(cid:17)
$$
= Ep(x)π0(a|x)p(e|x,a) = Ep(x)π0(a|x)p(e|x,a) Thus, we have
$$
(cid:16)VD[ ˆVIPS(π;D)] − VD[ ˆVMIPS(π;D)] − Bias( ˆVMIPS(π))2(cid:17)
$$
n = Ep(x)π0(a|x)p(e|x,a)
$$
(cid:2)(cid:0)w(x, a)2 − w(x, e)2(cid:1) · Ep(r|x,a,e)[r2](cid:3) + 2V (π)Bias( ˆVMIPS(π)) + (1 − n)Bias( ˆVMIPS(π))2
$$
The ﬁrst term becomes large when the scale of the marginal importance weights is smaller than that of the vanilla importance weights. The second term becomes large when the value of π is large and MIPS overestimates it by a large margin. The third term can take a large negative value when the sample size is large and the bias of MIPS is large. This summarizes the bias-variance trade-off between the vanilla IPS and MIPS. When the sample size is small, the ﬁrst and second terms in the MSE gain are dominant, and MIPS is more appealing due to its variance reduction property. However, as the sample size gets larger, the bias becomes dominant, and IPS is expected to overtake MIPS at some point. We would argue that, when the action space is large, the variance reduction of MIPS often provides the gain in MSE, as the variance components are more dominant, which is supported by our experiment.
## B.6. Derivation of Eq. (3) in Section 3.3
w(x, e) =
$$
=
$$
$$
=
$$
$$
=
$$
p(e|x, π) p(e|x, π0) (cid:80) a∈A p(e|x, a) · π(a|x) p(e|x, π0)(cid:80) (cid:88) p(e|x, π0) π0(a|x, e) a∈A
$$
= Eπ0(a|x,e) [w(x, a)]
$$
p(e|x, π0) a∈A(π0(a|x, e)/π0(a|x)) · π(a|x) π(a|x) π0(a|x) (17) where we use p(e|x, a) = p(e|x,π0)π0(a|x,e) π0(a|x) in Eq. (17).
## B.7. Bias and Variance of MIPS with Estimated Marginal Importance Weights
Theorem B.2. (Bias of MIPS with Estimated Marginal Importance Weights) If Assumption 3.1 is true, but Assumption 3.2 is violated, MIPS with the estimated marginal importance weight ˆw(x, e) has the following bias.
$$
Bias( ˆVMIPS(π; ˆw)) = Bias( ˆVMIPS(π)) − Ep(x)p(e|x,π) [δ(x, e)q(x, π0, e)] ,
$$
$$
where ˆVMIPS(π; ˆw) := n−1(cid:80)n
$$
i=1 ˆw(xi, ei)ri, δ(x, e) := 1 − ( ˆw(x, e)/w(x, e)), and q(x, π0, e) := (cid:80) a∈A π0(a|x, e) · q(x, a, e).
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Proof.
$$
Bias( ˆVMIPS(π; ˆw)) = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[ ˆw(x, e)r] − V (π)
$$
(18) (19) where we use ED[ ˆVMIPS(π;D, ˆw)] = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[ ˆw(x, e)r] (as samples are assumed to be independent) in Eq. (18) and decompose the bias into the bias of MIPS with the true w(x, e) and bias due to the estimation error of ˆw(x, e) in Eq. (19). We know the bias of MIPS with the true weight from Theorem 3.5, so we calculate only the bias due to estimating the weight.
$$
(cid:2)( ˆw(x, e) − w(x, e)) · r(cid:3) + Bias( ˆVMIPS(π))
$$
= Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e) Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[( ˆw(x, e) − w(x, e)) · r] = Ep(x)π0(a|x)p(e|x,a)[( ˆw(x, e) − w(x, e)) · q(x, a, e)] = Ep(x) π0(a|x) p(e|x, a) · ( ˆw(x, e) − w(x, e)) · q(x, a, e) (cid:35) π0(a|x) p(e|x, π0) · π0(a|x, e) π0(a|x) · ( ˆw(x, e) − w(x, e)) · q(x, a, e) p(e|x, π0) · ( ˆw(x, e) − w(x, e)) π0(a|x, e) · q(x, a, e) (cid:35) (cid:35) (cid:88) (cid:88) e∈E e∈E a∈A (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) (cid:34)(cid:88) a∈A e∈E = Ep(x) = Ep(x) (cid:88) (cid:35) a∈A p(e|x, π) · δ(x, e) · q(x, π0, e) = −Ep(x) = −Ep(x)p(e|x,π) [δ(x, e) · q(x, π0, e)] e∈E in Eq. (20) and q(x, π0, e) =(cid:80) (20) (21) where we use p(e|x, a) = p(e|x,π0)π0(a|x,e) Theorem B.3. (Variance of MIPS with Estimated Marginal Importance Weights) Under Assumptions 3.1 and 3.2, we have a∈A π0(a|x, e)q(x, a, e) in Eq. (21). π0(a|x)
$$
nVD( ˆVMIPS(π;D, ˆw)) = Ep(x)p(e|x,π)
$$
where δ(x, e) := 1−( ˆw(x, e)/w(x, e)), q(x, π0, e) :=(cid:80) + Ep(x) + Vp(x) σ2(x, a, e). (cid:2)(1 − δ(x, e))2w(x, e)σ2(x, π0, e)(cid:3) (cid:2)Vπ0(a|x)p(e|x,a) [ ˆw(x, e)q(x, a, e)](cid:3) (cid:2)Ep(e|x,π) [(1 − δ(x, e))q(x, π0, e)](cid:3) a∈A π0(a|x, e)·q(x, a, e), and σ2(x, π0, e) :=(cid:80) a∈A π0(a|x, e)· Proof. Since the samples are assumed to be independent, we have nVD( ˆVMIPS(π;D, ˆw)) = Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e) [ ˆw(x, e)r] . Below we apply the law of total variance twice to the RHS of the above equation. Vp(x)π0(a|x)p(e|x,a)p(r|x,a,e) [ ˆw(x, e)r] = Ep(x)π0(a|x)p(e|x,a) + Vp(x)π0(a|x)p(e|x,a) = Ep(x)π0(a|x)p(e|x,a) + Vp(x)π0(a|x)p(e|x,a) [ ˆw(x, e) · q(x, a, e)] = Ep(x)π0(a|x)p(e|x,a) (cid:2) ˆw(x, e)2 · Vp(r|x,a,e)[r](cid:3) (cid:2) ˆw(x, e) · Ep(r|x,a,e)[r](cid:3) (cid:2) ˆw(x, e)2 · σ2(x, a, e)(cid:3) (cid:2) ˆw(x, e)2 · σ2(x, a, e)(cid:3) (cid:2)Vπ0(a|x)p(e|x,a) [ ˆw(x, e) · q(x, a, e)](cid:3) (cid:2)Eπ0(a|x)p(e|x,a) [ ˆw(x, e) · q(x, a, e)](cid:3) (cid:2)(1 − δ(x, e))2 · w(x, e) · σ2(x, π0, e)(cid:3) (cid:2)Vπ0(a|x)p(e|x,a) [ ˆw(x, e) · q(x, a, e)](cid:3) (cid:2)Ep(e|x,π) [(1 − δ(x, e)) · q(x, π0, e)](cid:3) + Ep(x) + Vp(x) + Ep(x) + Vp(x) = Ep(x)p(e|x,π) (22)
### Off-Policy Evaluation for Large Action Spaces via Embeddings
where we Eπ0(a|x)p(e|x,a)[ ˆw(x, e)q(x, a, e)] = Ep(e|x,π)[(1 − δ(x, e))q(x, π0, e)] in Eq. (22) use Eπ0(a|x)p(e|x,a)[ ˆw(x, e)2σ2(x, a, e)]
$$
=
$$
Ep(e|x,π)[(1 − δ(x, e))2w(x, e)σ2(x, π0, e)] and
## B.8. Bias of MIPS with Deﬁcient Embedding Support
Theorem B.4. (Bias of MIPS with Deﬁcient Embedding Support) If Assumption 3.2 is true, but Assumption 3.1 is violated, MIPS has the following bias.
$$
(cid:12)(cid:12)Bias( ˆVMIPS(π))(cid:12)(cid:12) = Ep(x)
$$
 (cid:88) e∈U e 0 (x,π0)  , p(e|x, π)q(x, e) where U e 0 (x, π0) := {e ∈ E | p(e|x, π0) = 0} is the space of unsupported embeddings for context x under π0. Proof. We follow Proposition 1 of Sachdeva et al. (2020) to derive the bias under deﬁcient embedding support. Bias( ˆVMIPS(π)) = Ep(x)π0(a|x)p(e|x,a)p(r|x,a,e)[w(x, e)r] − V (π) e∈(U e  (cid:88)  (cid:88)  (cid:88) e∈(U e 0 (x,π0))c 0 (x,π0))c e∈U e 0 (x,π0) = Ep(x) = Ep(x) = −Ep(x) a∈A w(x, e)q(x, e) (cid:88) p(e|x, π)q(x, e) −(cid:88)  p(e|x, π)q(x, e) e∈E  − Ep(x)p(e|x,π)[q(x, e)]  π0(a|x)p(e|x, a) p(e|x, π)q(x, e) (23) (24) where Eq. (23) is due to Assumption 3.2 and Eq. (24) is from p(e|x, a) = p(e|x,π0)π0(a|x,e) π0(a|x) .
# C. Data-Driven Action Feature Selection Based on Tucker & Lee (2021) and Su et al. (2020b)
Wang et al. (2017) and Su et al. (2020a) describe a procedure for data-driven estimator selection, which is used to tune the built-in hyperparameters of their own estimators. However, their methods need to estimate the bias (or its loose upper bound as a proxy) of the estimator as a subroutine, which is as difﬁcult as OPE itself. Su et al. (2020b) develop a generic data-driven method for estimator selection for OPE called SLOPE, which is based on Lepski’s principle (Lepski & Spokoiny, 1997) and does not need a bias estimator. Tucker & Lee (2021) improve the theoretical analysis of Su et al. (2020b), resulting in a reﬁned procedure called SLOPE++. Given a ﬁnite set of estimators { ˆVm}M m=1, which is often constructed by varying the value of hyperparameters, the estimator selection problem aims at identifying the estimator that minimizes some notion of estimation error such as the following absolute error with respect to a given target policy π.
$$
(cid:12)(cid:12)(cid:12)V (π) − ˆVm(π;D)
$$
(cid:12)(cid:12)(cid:12) ,
$$
m∗ := arg min
$$
m∈[M ] where D is a given logged bandit dataset. For solving this selection problem, SLOPE++ requires the following monotonicity assumption (SLOPE requires a slightly stronger assumption).
## Assumption C.1. (Monotonicity)
$$
1. Bias( ˆVm) ≤ Bias( ˆVm+1), ∀m ∈ [M ]
$$
$$
2. CNF( ˆVm+1) ≤ CNF( ˆVm), ∀m ∈ [M ]
$$
### Off-Policy Evaluation for Large Action Spaces via Embeddings
where CNF( ˆV ) is a high probability bound on the deviation of ˆV , which requires that the following holds with a probability at least 1 − δ. (cid:12)(cid:12)(cid:12)ED
$$
(cid:104) ˆV (π;D)
$$
$$
(cid:105) − ˆV (π;D)
$$
$$
(cid:12)(cid:12)(cid:12) ≤ CNF( ˆV ),
$$
which we can generally bound with high conﬁdence using techniques such as concentration inequalities. Based on this assumption, Tucker & Lee (2021) derive the following universal bound. Theorem C.2. (Theorem 1 of Tucker & Lee (2021)) Given δ > 0, high conﬁdence bound CNF( ˆVm) on the deviations, and that we have ordered the candidate estimators such that CNF( ˆVm+1) ≤ CNF( ˆVm). Selecting the estimator as (25)
$$
(cid:12)(cid:12) ≤ CNF(m) + (
$$
√ (cid:111)
$$
6 − 1)CNF(j), j < m
$$
(cid:19)
$$
6 + 3) min
$$
m
$$
max
$$
j≤m
$$
Bias(j) + CNF(m)
$$
. ensures that with probability at least 1 − δ, Under Assumption C.1, the bound simpliﬁes to
$$
ˆm := max
$$
√ (cid:110) m :(cid:12)(cid:12) ˆVm − ˆVj (cid:12)(cid:12)(cid:12) ˆV ˆm − ˆVm∗ (cid:12)(cid:12)(cid:12) ≤ ( (cid:12)(cid:12)(cid:12) ˆV ˆm − ˆVm∗ (cid:12)(cid:12)(cid:12) ≤ ( (cid:12)(cid:12)(cid:12) ≤ ( (cid:12)(cid:12)(cid:12) ˆV ˆm − ˆVm∗ √ √ (cid:18) (cid:18) In contrast, when the set of estimators is not ordered with respect to CNF(·), we have a looser bound as below.
$$
6 + 3) min
$$
m
$$
(Bias(m) + CNF(m)) .
$$
$$
6 + 3) min
$$
m
$$
max
$$
j≤m
$$
Bias(j) + max
$$
k≤m
$$
CNF(k)
$$
. (cid:19) Note that Tucker & Lee (2021) also provide the corresponding universal upper bound with respect to MSE in their Corollary 1.1. We build on the selection procedure given in Eq. (25) to implement data-driven action feature selection. Speciﬁcally, in our case, the task is to identify which dimensions of the action embedding e we should use to minimize the MSE of the resulting MIPS as follows.
$$
minE⊆V Bias(cid:0) ˆVMIPS (π;E)(cid:1)2
$$
+ VD(cid:2) ˆVMIPS (cid:0)π;D,E(cid:1)(cid:3) where V := {E1,E2, . . . ,Ek} is a set of available action features. Note that we make the dependence of MIPS on the action embedding space E explicit in the above formulation. As described in Theorems 3.5, 3.6, and 3.7, we should use as many dimensions as possible to reduce the bias, while we should use as coarse information as possible to gain a large variance reduction. For identifying useful features to compute the marginal importance weights, we construct a set of estimators { ˆVMIPS (π;D,E)}E⊆V and simply apply Eq. (25). Note that when the number of embedding dimensions is not small, the brute-force search over all possible combinations of the embedding dimensions is not tractable. Thus, we sometime deﬁne the action embedding search space V via a greedy procedure to make the embedding selection tractable. In our experiments, we perform action embedding selection based on the greedy version of SLOPE++, and we estimate a high probability bound on the deviation (CNF( ˆV )) based on the Student’s t distribution as done in Thomas et al. (2015). The MIPS estimator along with the exact and greedy versions of embedding dimension selection is now implemented in the OBP package.7.
# D. Experiment Details and Additional Results
## D.1. Baseline Estimators
Below, we deﬁne and describe the baseline estimators in detail. 7https://github.com/st-tech/zr-obp
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Direct Method (DM) DM is deﬁned as follows.
$$
ˆVDM(π;D, ˆq) :=
$$
$$
1
$$
n
$$
Eπ(a|xi)[ˆq(xi, a)] =
$$
n(cid:88) (cid:88) i=1 a∈A
$$
1
$$
n π(a|xi)ˆq(xi, a), n(cid:88) i=1 n(cid:88) i=1 where ˆq(x, a) estimates q(x, a) based on logged bandit data. The accuracy of DM depends on the quality of ˆq(x, a). If ˆq(x, a) is accurate, so is DM. However, if ˆq(x, a) fails to estimate the expected reward accurately, the ﬁnal estimator is no longer consistent. As discussed in Appendix A, the misspeciﬁcation issue is challenging, as it cannot be easily detected from available data (Farajtabar et al., 2018; Voloshin et al., 2019). This is why DM is often described as a high bias estimator.
## Doubly Robust (DR) (Dud´ık et al., 2014) DR is deﬁned as follows.
$$
ˆVDR(π;D, ˆq) :=
$$
$$
1
$$
n (cid:8)Eπ(a|xi)[ˆq(xi, a)] + w(xi, ai)(ri − ˆq(xi, ai))(cid:9) , which combines DM and IPS in a way to reduce the variance. More speciﬁcally, DR utilizes ˆq as a control variate. If the expected reward is correctly speciﬁed, DR is semiparametric efﬁcient meaning that it achieves the minimum possible asymptotic variance among regular estimators (Narita et al., 2019). A problem is that, if the expected reward is misspeciﬁed, this estimator can have a larger asymptotic MSE compared to IPS. Switch Doubly Robust (Switch-DR) (Wang et al., 2017) Although DR generally reduces the variance of IPS and is also minimax optimal (Wang et al., 2017), it can still suffer from the variance issue in practice, particularly when the importance weights are large due to a weak overlap between target and logging policies. Switch-DR is introduced to further deal with the variance issue and is deﬁned as follows. (cid:8)Eπ(a|xi)[ˆq(xi, a)] + w(xi, ai)I{w(xi, ai) ≤ λ}(ri − ˆq(xi, ai))(cid:9) , ˆVSwitchDR(π;D, ˆq, λ) :=
$$
1
$$
n n(cid:88) i=1 where I{·} is the indicator function and λ ≥ 0 is a hyperparameter. When λ = 0, Switch-DR becomes DM, while λ → ∞ leads to DR. Switch-DR is also minimax optimal when λ is appropriately set (Wang et al., 2017).
## More Robust Doubly Robust (Farajtabar et al., 2018) MRDR uses an expected reward estimator (ˆqMRDR) derived
by minimizing the variance of the resulting DR estimator. This estimator is deﬁned as ˆVMRDR(π;D, ˆqMRDR) := ˆVDR(π;D, ˆqMRDR), where ˆqMRDR is derived by minimizing the (empirical) variance objective: ˆqMRDR ∈ arg minˆq∈Q Vn( ˆVDR(π;D, ˆq)), where Q is a function class for ˆq. When Q is well-speciﬁed, then ˆqMRDR = q. The main point is that, even if Q is misspeciﬁed, MRDR is still expected to perform reasonably well, as the target function is the resulting variance. To implement MRDR, we follow Farajtabar et al. (2018) and Su et al. (2020a), and derive ˆqMRDR by minimizing the weighted squared loss with respect to the reward prediction on the logged data.
## Doubly Robust with Optimistic Shrinkage (Su et al., 2020a) DRos is deﬁned via minimizing an upper bound of the
MSE and is deﬁned as follows.
$$
ˆVDRos(π;D, ˆq, λ) :=
$$
$$
1
$$
n
$$
Eπ(a|xi)[ˆq(xi, a)] +
$$
λw(xi, ai) w(xi, ai)2 + λ
$$
(ri − ˆq(xi, ai))
$$
where λ ≥ 0 is a hyperparameter. When λ = 0, DRos is equal to DM, while λ → ∞ makes DRos identical to DR. DRos is aimed at improving the small sample performance of DR, but is indeed biased due to the weight shrinkage. DR-λ (Metelli et al., 2021) DR-λ is a recent estimator building on a “smooth shrinkage” of the importance weights to mitigate the heavy-tailed behavior of the previous estimators. This estimator is deﬁned as follows. (cid:27) , (cid:27)
$$
ˆVDR−λ(π;D, ˆq, λ) :=
$$
$$
1
$$
n
$$
Eπ(a|xi)[ˆq(xi, a)] +
$$
w(xi, ai) 1 − λ + λw(xi, ai)
$$
(ri − ˆq(xi, ai))
$$
, (cid:26) n(cid:88) i=1 (cid:26) n(cid:88) i=1 where λ ∈ [0, 1] is a hyperparameter. Note that Metelli et al. (2021) deﬁne a more general weight, ((1 − λ)w(x, a)s + λ) 1 s , with an additional hyperparameter s. The above instance is a special case with s = 1, which is the main proposal of Metelli et al. (2021).
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## D.2. Additional Results on Synthetic Bandit Data
In this section, we explore two additional research questions regarding the estimators’ performance for different logging/target policies and different levels of noise on the rewards. We demonstrate that MIPS works particularly better than other baselines when the target and logging policies differ greatly and the reward is noisy. After discussing the two research questions, we report detailed experimental results regarding the research questions addressed in the main text with additional baselines.
## How does MIPS perform with varying logging and target policies? We compare the MSE, squared bias, and variance
of the estimators (DM, IPS, DR, MIPS, and MIPS with the true weights) with varying logging and target policies. We can do this by varying the values of β and  as described in Section 4. Note that we set β = −1 and  = 0.05 for all synthetic results in the main text. First, Figure 8 reports the results with varying logging policies (β ∈ {−3,−2,−1, 0, 1, 2, 3}) and with a near-optimal/near- deterministic target policy deﬁned by  = 0.05 (ﬁxed). A large negative value of β leads to a worse logging policy, meaning that it creates a large discrepancy between logging and target policies in this setup. The left column of Figure 8 demonstrates that the MSEs of the estimators generally become larger for larger negative values of β as expected. Most notably, the MSEs of IPS and DR blow up for β = −3,−2 due to their inﬂated variance as suggested in the right column of the same ﬁgure. On the other hand, MIPS and MIPS (true) work robustly for a range of logging policies, suggesting the strong variance reduction for the case with a large discrepancy between policies. DM also suffers from a larger discrepancy between logging and target policies due to its increased bias caused by the extrapolation error issue. Next, Figure 9 shows the results with varying target policies ( = {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}) and with a logging policy slightly worse than uniform random deﬁned by β = −1 (ﬁxed). A larger value of  introduces a larger entropy for the target policy, making it closer to the logging policy in this setup (an extreme case with  = 1.0 produces a uniform random target policy). On the other hand,  = 0 produces the optimal, deterministic target policy, which makes OPE harder given β = −1. The left column of Figure 9 suggests that all estimators perform worse for smaller values of  as expected. IPS and DR perform worse as their variance increases with decreasing , while DM performs worse as it produces larger bias. The variance of MIPS also increases with decreasing , but it is often much smaller and robust than those of IPS and DR. Note that, for the uniform random target policy ( = 1.0), all estimators are very accurate and there is no signiﬁcant difference among the estimators. How does MIPS perform with varying noise levels? Next, we explore how the level of noise on the rewards affects the comparison of the estimators. To this end, we vary the noise level σ ∈ {0.5, 1.0, 1.5, . . . , 4.0} where σ is the standard deviation of the Gaussian noise, i.e., r ∼ N (q(x, a), σ2). As stated in the main text, the variance of IPS grows when the reward is noisy. Theorem 3.6 also implies that the variance reduction of MIPS becomes more appealing with the noisy rewards. Figure 10 empirically supports these claims. Speciﬁcally, IPS signiﬁcantly exacerbates its MSE from 0.55 (when σ = 0.5) to 3.22 (when σ = 4.0). MIPS also struggles with noisy rewards, but the improvement of MIPS compared to IPS/DR becomes larger with the added noise. When the noise level is small (σ = 0.5), MSE( ˆVIPS) = 2.97, while MSE( ˆVMIPS) MSE( ˆVIPS) = 14.98 when the noise is large (σ = 4.0). Different from IPS, DR, and MIPS, DM is not affected so much by MSE( ˆVMIPS) the noise level and becomes increasingly better than IPS and DR in noisy environments. Nontheless, MIPS achieves much smaller MSE than DM even with noisy rewards.
## Comparison with additional baselines across additional experimental conditions. We include additional baselines
(Switch-DR, DRos, and DR-λ) described in Appendix D.1 to the empirical evaluations. Their built-in hyperparameters are tuned with SLOPE++ proposed by Tucker & Lee (2021), which slightly improves the original SLOPE of Su et al. (2020b). We use implementations of these advanced estimators provided by OBP (version 0.5.5). We evaluate the four research questions addressed in the main text with six different pairs of (β, ). Figures 11-14 report the results with β = −1 and  = 0.05. Figures 15-18 report the results with β = −1 and  = 0.8. Figures 19-22 report the results with β = 0 and  = 0.05. Figures 23-26 report the results with β = 0 and  = 0.8. Figures 27-30 report the results with β = 1 and  = 0.05. Figures 31-34 report the results with β = 1 and  = 0.8. In general, we observe results similar to those reported in the main text. Speciﬁcally, MIPS works better than all existing estimators, including the advanced ones, in a range of situations, in particular for small data and large action spaces. This result suggests that even the recent state-of-the-art estimators fail to deal with large action spaces. Regarding the additional baselines, Switch-DR, DRos, and DR-λ work similarly to DM. These estimators fail to improve their variance with the
### Off-Policy Evaluation for Large Action Spaces via Embeddings
growing sample sizes and become worse than IPS and DR in large sample regimes. This observation suggests that SLOPE++ avoids huge importance weights and favors low variance, but highly biased estimators in our setup. We indeed also tested the More Robust Doubly Robust (MRDR) estimator (Farajtabar et al., 2018), but ﬁnd that MRDR suffers from its growing variance with a growing number of actions and works similarly to IPS and DR.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Figure 8. MSE, Squared Bias, and Variance with varying logging policies (β) Figure 9. MSE, Squared Bias, and Variance with varying target policies () Figure 10. MSE, Squared Bias, and Variance with varying noise levels (σ) Note: We set n = 10, 000 and |A| = 1, 000. For Figure 8, we ﬁx  = 0.05, σ = 2.5, for Figure 9, we ﬁx β = −1, σ = 2.5, and for Figure 10, we ﬁx  = 0.05, β = −1. The results are averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## MSE
## Squared Bias
## Variance
Figure 11. MSE, Squared Bias, and Variance with varying number of actions Figure 12. MSE, Squared Bias, and Variance with varying sample size Figure 13. MSE, Squared Bias, and Variance with varying number of deﬁcient actions
### Figure 14. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings
### Note: We set β = −1 and  = 0.05, which produce logging policy slightly worse than uniform random and
near-optimal/near-deterministic target policy. The results are averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap. The y-axis of MSE and Variance plots (the left and right columns) is reported on log-scale.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## MSE
## Squared Bias
## Variance
Figure 15. MSE, Squared Bias, and Variance with varying number of actions Figure 16. MSE, Squared Bias, and Variance with varying sample size Figure 17. MSE, Squared Bias, and Variance with varying number of deﬁcient actions
### Figure 18. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings
### Note: We set β = −1 and  = 0.8, which produce logging policy slightly worse than uniform random and near-uniform target
policy. The results are averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap. The y-axis of MSE and Variance plots (the left and right columns) is reported on log-scale.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## MSE
## Squared Bias
## Variance
Figure 19. MSE, Squared Bias, and Variance with varying number of actions Figure 20. MSE, Squared Bias, and Variance with varying sample size Figure 21. MSE, Squared Bias, and Variance with varying number of deﬁcient actions
### Figure 22. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings
### Note: We set β = 0 and  = 0.05, which produce uniform random logging policy and near-optimal/near-deterministic target
policy. The results are averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap. The y-axis of MSE and Variance plots (the left and right columns) is reported on log-scale.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## MSE
## Squared Bias
## Variance
Figure 23. MSE, Squared Bias, and Variance with varying number of actions Figure 24. MSE, Squared Bias, and Variance with varying sample size Figure 25. MSE, Squared Bias, and Variance with varying number of deﬁcient actions
### Figure 26. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings
### Note: We set β = 0 and  = 0.8, which produce uniform random logging policy and near-uniform target policy. The results are
averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap. The y-axis of MSE and Variance plots (the left and right columns) is reported on log-scale.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## MSE
## Squared Bias
## Variance
Figure 27. MSE, Squared Bias, and Variance with varying number of actions Figure 28. MSE, Squared Bias, and Variance with varying sample size Figure 29. MSE, Squared Bias, and Variance with varying number of deﬁcient actions
### Figure 30. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings
### Note: We set β = 1 and  = 0.05, which produce logging policy slightly better than uniform random and
near-optimal/near-deterministic target policy. The results are averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap. The y-axis of MSE and Variance plots (the left and right columns) is reported on log-scale.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
## MSE
## Squared Bias
## Variance
Figure 31. MSE, Squared Bias, and Variance with varying number of actions Figure 32. MSE, Squared Bias, and Variance with varying sample size Figure 33. MSE, Squared Bias, and Variance with varying number of deﬁcient actions
### Figure 34. MSE, Squared Bias, and Variance with varying number of unobserved dimensions in action embeddings
### Note: We set β = 1 and  = 0.8, which produce logging policy slightly better than uniform random and near-uniform target policy.
The results are averaged over 100 different sets of synthetic logged data replicated with different random seeds. The shaded regions in the MSE plots represent the 95% conﬁdence intervals estimated with bootstrap. The y-axis of MSE and Variance plots (the left and right columns) is reported on log-scale.
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Algorithm 1 An Experimental Procedure to Evaluate an OPE Estimator with Real-World Bandit Data Require: an estimator to be evaluated ˆV , target policy and corresponding logged bandit data (π,D), logging policy and corresponding logged bandit data (π0,D0), sample size in OPE n, number of random seeds T
$$
z(cid:48) ←(cid:0)Von(π;D) − ˆV (π;D∗
$$
0,t)(cid:1)2 Ensure: empirical CDF of the squared error ( ˆFZ) 1: Z ← ∅ (initialize set of results) 2: for t = 1, 2, . . . , T do 3: D∗
$$
0,t ← Bootstrap(D0; n)
$$
4: 5:
## 6: end for
7: Estimate CDF of relative SE (FZ) based on Z (Eq. 26) Z ← Z ∪ {z(cid:48)}
$$
/(cid:0)Von(π;D) − ˆVIPS(π;D∗
$$
0,t)(cid:1)2 // randomly sample size n of bootstrapped samples // calculate the relative SE of ˆV w.r.t IPS // store the result Figure 35. CDF of squared errors relative to IPS with different sample sizes (From left to right, n = 10000, 50000, 500000). CDFs are estimated with 150 different sets of bootstrapped logged bandit data. Note that the x-axis is reported on a log-scale.
## D.3. Experimental Procedure to Evaluate OPE Estimators on Real-World Bandit Data
Following Saito et al. (2020; 2021), we empirically evaluate the accuracy of the estimators by leveraging two sources of logged bandit data collected by running two different policies denoted as π (regarded as target policy) and π0 (regarded as logging policy). We let D denote a logged bandit dataset collected by π and D0 denote that collected by π0. We then apply the following procedure to evaluate the accuracy of an OPE estimator ˆV . 1. Perform bootstrap sampling on D0 and construct D∗ i , r∗ i=1, which consists of size n of independently
$$
0 := {(x∗
$$
i )}n i , a∗ resampled data with replacement. 2. Estimate the policy value of π using D∗ 3. Evaluate the estimation accuracy of ˆV with the following relative squared error w.r.t IPS (rel-SE): 0 and OPE estimator ˆV . We represent a policy value estimated by ˆV as ˆV (π;D∗ 0).
$$
0) :=(cid:0)Von(π;D) − ˆV (π;D∗
$$
0)(cid:1)2
$$
/(cid:0)Von(π;D) − ˆVIPS(π;D∗
$$
0)(cid:1)2 ,
$$
where ˆVon(π;D) := |D|−1(cid:80)
$$
rel-SE( ˆV ;D∗ (·,·,rj )∈D rj is the Monte-Carlo estimate of V (π) based on on-policy data D. 4. Repeat the above process T times with different random seeds, and estimate the CDF of the relative SE as follows. I(cid:8)rel-SEt( ˆV ;D∗ 0,t) ≤ z(cid:9), T(cid:88) t=1
$$
ˆFZ(z) :=
$$
$$
1
$$
T (26) where rel-SE( ˆV ;D∗ 0,t) is the relative SE of ˆV computed with the t-th bootstrapped samples D∗ 0,t. Algorithm 1 describes this experimental protocol for evaluating OPE estimators in detail. Figure 35 reports the results with real bandit data for varying numbers of logged data (n = 10000, 50000, 500000). Note that we use the Random Forest implemented in scikit-learn along with 2-fold cross-ﬁtting (Newey & Robins, 2018) to obtain ˆq(x, e) for the model-dependent estimators. We also use the Categorical Naive Bayes8 to estimate ˆπ0(a|x, e) for MIPS. 8https://scikit-learn.org/stable/modules/generated/sklearn.naive bayes.CategoricalNB.html
### Off-Policy Evaluation for Large Action Spaces via Embeddings
Note that we use OBD’s “ALL” campaign, because it has the largest number of actions among the three available campaigns. We also regard the same action presented at a different position in a recommendation interface as different actions. As OBD has 80 unique actions and 3 different positions in its recommendation interface, the resulting action space has the cardinality
$$
of 80 × 3 = 240.
$$
