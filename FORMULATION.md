# Mathematical Formulation

This document outlines the theoretical and stochastic foundations powering the Probabilistic Delivery Risk Engine. 

## 1. Multi-Stage Delivery Model
A delivery route $R$ consists of $n$ discrete, sequential operational stages (e.g., Pickup, Transit, Drop). Let $T_{total}$ denote the continuous random variable representing the total delivery duration.

$$
T_{total} = \sum_{i=1}^{n} T_i
$$

Where $T_i$ is a random variable mapping the time taken to complete the $i$-th stage.

## 2. Stage Distribution (Independent Mode)
Under independence assumptions, each stage duration is distributed normally:

$$
\tilde{T}_i \sim \mathcal{N}(\mu_i, \sigma_i^2)
$$

Where $\mu_i$ is the expected time for stage $i$, and $\sigma_i^2$ is the variance accounting for local uncertainty. To prevent physically impossible negative time loops from the Gaussian tail, the actual sampled time is bounded:

$$
T_i = \max(\tilde{T}_i, 0)
$$

## 3. Traffic Adjustment Factor
To introduce exogenous map conditions, we define a deterministic scaling factor $\lambda \in \mathbb{R}^+$ corresponding to the severity of local traffic. The adjusted expectation modifies the distribution mapping:

$$
\mu_{i}^{(\lambda)} = \lambda \cdot \mu_i \implies \tilde{T}_i \sim \mathcal{N}(\mu_{i}^{(\lambda)}, \sigma_i^2)
$$

## 4. Monte Carlo Simulation Framework
To estimate the intractable combined distribution resulting from the bounded convolutions, we apply Monte Carlo methods. For $k \in \{1, 2, \dots, N\}$ independent simulation runs, we sample total time paths:

$$
T_{total}^{(k)} = \sum_{i=1}^{n} T_i^{(k)}
$$

By the Law of Large Numbers, as $N \to \infty$, the sample distribution converges to the true ETA distribution.

## 5. Delay Probability & Empirical Risk Metric
Given an explicit Service Level Agreement (SLA) threshold sequence $S$:

**Expected Delivery Time:**

$$
\mathbb{E}[T_{total}] \approx \frac{1}{N} \sum_{k=1}^{N} T_{total}^{(k)}
$$

**95th Percentile ($P_{95}$):**

$$
P_{95} = \inf \{ t \in \mathbb{R} : P(T_{total} \le t) \ge 0.95 \}
$$

**Delay Risk Probability ($P_{delay}$):**
Calculated using the indicator function $\mathbf{1}$:

$$
P(T_{total} > S) = \mathbb{E}[\mathbf{1}_{T_{total} > S}] \approx \frac{1}{N} \sum_{k=1}^{N} \mathbf{1}_{\{T_{total}^{(k)} > S\}}
$$

## 6. Random Walk with Drift (Dependent Process)
To model cumulative variance dependencies across the sequence of the route, we construct a discrete-time random walk where increments vary by stage:

$$
T_n = \sum_{i=1}^{n} (\mu_i + \varepsilon_i) = T_{n-1} + \mu_n + \varepsilon_n
$$

Where the systemic drift is $\mu_n$ and the noise increment is $\varepsilon_n \sim \mathcal{N}(0, \sigma_n^2)$. This structure accurately treats the sequential delivery steps as an underlying stochastic process rather than purely decoupled events.

## 7. Markov Chain for Hidden Delay States
To capture the reality of cascading delays (where one delay severely increases the probability of another), we define a hidden discrete state space representing operational health:

$$
\mathcal{S} = \{\text{ON-TIME},\ \text{DELAYED},\ \text{SEVERE}\}
$$

Let $X_i \in \mathcal{S}$ be the realized state during stage $i$. Transitions obey the Memoryless Markov Property:

$$
P(X_{i+1} = j \mid X_i = k) = P_{kj}
$$

Where $P$ represents the fixed $3 \times 3$ transition probability matrix. The stage time sampling is strictly conditioned on the realized state sequence:

$$
T_i \mid X_i \sim \mathcal{N}(\mu_i \cdot \gamma(X_i),\ \sigma_i^2)
$$

Where $\gamma(X_i)$ is an explicit state-dependent penalty multiplier (e.g., $\gamma(\text{ON-TIME}) = 1.0$, whereas $\gamma(\text{SEVERE}) = 1.8$).
