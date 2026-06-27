#!/usr/bin/env python3
"""
AI/ML Daily Learning Bot
Sends a daily lesson at 8 AM via Telegram.
Designed to run as a Hermes cron job or standalone cron.

Supports .env files and environment variables for configuration.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

from telegram import Bot
from telegram.error import TelegramError, NetworkError, TimedOut

# ── .env support ───────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

# ── Logging ────────────────────────────────────────────────────────────
LOG_FILE = Path(__file__).parent / "bot.log"
STATE_FILE = Path(__file__).parent / "current_day.txt"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler(sys.stderr),
    ],
)
log = logging.getLogger("aiml_bot")


# ── Config ─────────────────────────────────────────────────────────────
def _get_env_or_die(key: str) -> str:
    """Get required env var or exit with a clear message."""
    value = os.environ.get(key)
    if not value:
        log.error(
            "Missing %s. Set it via environment variable or .env file.\n"
            "  export %s='...'\n"
            "  or create .env with: %s=...",
            key, key, key,
        )
        sys.exit(1)
    return value


TELEGRAM_BOT_TOKEN = _get_env_or_die("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _get_env_or_die("TELEGRAM_CHAT_ID")


# ── Curriculum ─────────────────────────────────────────────────────────
CURRICULUM = [
    {
        "day": 1,
        "title": "What is AI?",
        "content": """🤖 *Day 1 — What is Artificial Intelligence?*

*Definition*
AI is the simulation of human intelligence by machines — enabling them to reason, learn, problem-solve, perceive, and understand language.

*Three Tiers*
• *Narrow AI* — Does one specific task extremely well (ChatGPT, image recognition, spam filters). Everything we have today.
• *General AI (AGI)* — Matches human-level reasoning across any domain. Doesn't exist yet.
• *Superintelligence* — Exceeds human intelligence across all domains. Theoretical.

*Key Milestones*
• 1950 — Alan Turing proposes the Turing Test
• 1956 — "Artificial Intelligence" coined at Dartmouth Conference
• 1997 — Deep Blue beats world chess champion Kasparov
• 2012 — Deep learning breakthrough (ImageNet)
• 2017 — Transformer architecture invented (basis of all modern LLMs)
• 2022 — ChatGPT launches, AI goes mainstream

*AI vs ML vs Deep Learning*
Think of concentric circles:
AI (outer) → Machine Learning (middle) → Deep Learning (inner)
Deep Learning is a subset of ML, which is a subset of AI.

*Real-world examples you use daily*
• Gmail spam filter → Narrow AI
• Google Maps ETA prediction → ML
• Claude/ChatGPT → Deep Learning (Transformers)

📌 *Tomorrow:* What is Machine Learning? The 3 types explained."""
    },
    {
        "day": 2,
        "title": "What is Machine Learning?",
        "content": """🧠 *Day 2 — What is Machine Learning?*

*Definition*
ML is teaching computers to learn from data — instead of explicitly programming every rule, you feed examples and let the algorithm figure out the pattern.

*The 3 Types*

*1. Supervised Learning*
Learn from labelled examples.
→ Input: email + label (spam/not spam)
→ Output: model that classifies new emails
Examples: fraud detection, house price prediction, image classification

*2. Unsupervised Learning*
Find hidden patterns in unlabelled data.
→ Input: customer purchase history (no labels)
→ Output: natural groupings (clusters) of similar customers
Examples: customer segmentation, anomaly detection, topic modelling

*3. Reinforcement Learning*
Learn by trial, error, and reward signals.
→ Agent takes actions → gets reward or penalty → improves
Examples: AlphaGo, game-playing AI, robotics, self-driving cars

*The Core ML Workflow*
1. Collect & clean data
2. Choose a model/algorithm
3. Train (model learns from data)
4. Evaluate (test on unseen data)
5. Deploy & monitor

*Key insight*
Traditional programming: Rules + Data → Output
Machine Learning: Data + Output → Rules (learned automatically)

📌 *Tomorrow:* Data — the fuel of ML. Features, labels, and why data quality beats algorithm choice."""
    },
    {
        "day": 3,
        "title": "Data — The Fuel of ML",
        "content": """📊 *Day 3 — Data: The Fuel of Machine Learning*

*Why data matters more than algorithms*
A mediocre algorithm with great data beats a great algorithm with bad data. Every time.

*Key Terminology*

• *Dataset* — Your full collection of examples
• *Feature (X)* — An input variable (age, salary, job title)
• *Label (y)* — The output you're predicting (promoted: yes/no)
• *Sample/Instance* — One row in your dataset

*The Three Splits*
Never train and test on the same data — the model just memorises.

• *Training set* (~70%) — Model learns from this
• *Validation set* (~15%) — Tune and compare models
• *Test set* (~15%) — Final, untouched evaluation. Use once.

*Data Quality Problems*
• *Missing values* — Need to impute or drop
• *Outliers* — Extreme values that skew learning
• *Class imbalance* — 99% not-fraud, 1% fraud → model learns to always say "not fraud"
• *Data leakage* — Future information accidentally leaking into training data (silent killer)

*Feature Engineering*
Transforming raw data into useful features.
Example: From a date field, extract day_of_week, is_weekend, month — each potentially more useful than the raw date.

*Real talk*
In enterprise ML (your world), 80% of time is data prep. The algorithm is the easy part.

📌 *Tomorrow:* Linear Regression — the simplest ML model and the foundation of everything."""
    },
    {
        "day": 4,
        "title": "Linear Regression",
        "content": """📈 *Day 4 — Linear Regression & Gradient Descent*

*What it does*
Predicts a continuous number by fitting the best straight line through data.
Example: predict house price from square footage.

*The Equation*
`y = mx + b`
• y = prediction (house price)
• x = input feature (sq footage)
• m = weight/slope (learned)
• b = bias/intercept (learned)

Multiple features: `y = w₁x₁ + w₂x₂ + ... + b`

*How does it "learn"? — Loss Functions*
The model measures how wrong it is using Mean Squared Error (MSE):
`MSE = average of (predicted - actual)²`

Goal: minimise this error.

*Gradient Descent*
The algorithm that minimises error:
1. Start with random weights
2. Calculate the error (loss)
3. Calculate which direction reduces error (gradient)
4. Take a small step in that direction
5. Repeat thousands of times

Think of it as: blindfolded on a hilly landscape, always stepping downhill to find the valley (minimum error).

*Learning Rate*
How big each step is.
• Too large → overshoot the minimum, never converge
• Too small → takes forever
• Just right → converges efficiently

*Key insight*
Gradient descent is the engine behind almost ALL of modern ML and deep learning. Master this concept and everything else makes sense.

📌 *Tomorrow:* Classification — when the answer isn't a number but a category."""
    },
    {
        "day": 5,
        "title": "Classification",
        "content": """🎯 *Day 5 — Classification & Logistic Regression*

*Classification vs Regression*
• Regression → predict a number (price, temperature)
• Classification → predict a category (spam/not spam, cat/dog)

*Logistic Regression*
Despite the name, it's a classification algorithm.
Uses the sigmoid function to squash any number into 0–1 (a probability).

`P(y=1) = 1 / (1 + e^(-z))`

Output: "70% probability this email is spam" → classify as spam if > 0.5

*Decision Boundary*
The line (or curve) separating classes.
Everything on one side → Class A. Other side → Class B.

*Evaluation Metrics*
Accuracy alone is misleading (remember class imbalance from Day 3).

• *Precision* — Of all predicted positives, how many were actually positive?
• *Recall* — Of all actual positives, how many did we catch?
• *F1 Score* — Harmonic mean of precision and recall
• *Confusion Matrix* — True positives, false positives, true negatives, false negatives

*The Precision-Recall Tradeoff*
• Cancer screening → maximise recall (catch every case, even false alarms)
• Spam filter → maximise precision (don't delete real emails)

*Multi-class Classification*
Not just binary. E.g., classify handwritten digits 0–9.
Approaches: One-vs-Rest, Softmax (outputs probabilities for all classes, sums to 1).

📌 *Tomorrow:* Overfitting vs Underfitting — the most common reason ML models fail in production."""
    },
    {
        "day": 6,
        "title": "Overfitting vs Underfitting",
        "content": """⚖️ *Day 6 — Overfitting, Underfitting & the Bias-Variance Tradeoff*

*The core problem*
A model that memorises training data is useless on new data.
A model that's too simple misses real patterns.

*Underfitting (High Bias)*
Model is too simple → misses patterns even in training data.
Example: fitting a straight line to curved data.
Symptoms: high training error AND high test error.
Fix: more complex model, more features, less regularisation.

*Overfitting (High Variance)*
Model is too complex → memorises noise in training data.
Fails on new data it hasn't seen.
Example: a model that memorises 10,000 training examples perfectly but fails on example 10,001.
Symptoms: low training error but HIGH test error.
Fix: more data, simpler model, regularisation, dropout.

*The Bias-Variance Tradeoff*
• *Bias* — Error from wrong assumptions (underfitting)
• *Variance* — Error from sensitivity to small fluctuations in training data (overfitting)
• You can't minimise both simultaneously — find the sweet spot.

*Fixes for Overfitting*
• *More training data* — Best fix if available
• *Regularisation* — L1 (Lasso), L2 (Ridge) — penalise large weights
• *Dropout* — Randomly disable neurons during training (deep learning)
• *Early stopping* — Stop training when validation error starts rising
• *Cross-validation* — K-fold: train/test on K different splits, average results

*The golden rule*
Always evaluate on data the model has never seen. If you touch the test set more than once, you're cheating.

📌 *Tomorrow:* Week 1 review — consolidate everything before moving to algorithms."""
    },
    {
        "day": 7,
        "title": "Week 1 Review",
        "content": """🔁 *Day 7 — Week 1 Review & Self-Check*

Consolidate before moving forward. Answer these without scrolling back:

*Quick-fire Questions*

1. What's the difference between Narrow AI and AGI?
2. Name the 3 types of Machine Learning.
3. What is a feature? What is a label?
4. Why do we split data into train/validation/test?
5. What does gradient descent do?
6. Why is accuracy a bad metric for imbalanced datasets?
7. What's the difference between overfitting and underfitting?
8. Name two fixes for overfitting.

*Key Concepts to Own*
✅ AI → ML → Deep Learning (concentric circles)
✅ Supervised / Unsupervised / Reinforcement Learning
✅ Features, Labels, Train/Val/Test splits
✅ Loss function → Gradient Descent → Learning
✅ Classification metrics: Precision, Recall, F1
✅ Bias-Variance Tradeoff

*Answers*
1. Narrow AI does one task; AGI matches human reasoning across all domains.
2. Supervised, Unsupervised, Reinforcement.
3. Feature = input variable; Label = output you're predicting.
4. To evaluate on data the model hasn't seen — prevent cheating.
5. Iteratively adjusts weights to minimise the loss function.
6. Model can score 99% by always predicting the majority class.
7. Underfitting = too simple (high bias); Overfitting = memorises noise (high variance).
8. More data, regularisation, dropout, early stopping, simpler model.

*Week 2 Preview*
Decision Trees → Random Forests → SVMs → Neural Networks → Backpropagation → Deep Learning

📌 *Tomorrow:* Decision Trees & Random Forests — intuitive, powerful, and everywhere in enterprise ML."""
    },
    {
        "day": 8,
        "title": "Decision Trees & Random Forests",
        "content": """🌳 *Day 8 — Decision Trees & Random Forests*

*Decision Trees*
A flowchart-like model that splits data based on feature values.

Example:
```
Is salary > £50k?
├── Yes → Is experience > 5 years? → Promote / Don't Promote
└── No → Don't Promote
```

Each split maximises information gain (reduces uncertainty).
Measured by: Gini Impurity or Entropy.

*Strengths*
• Highly interpretable — you can explain every decision
• Handles numerical and categorical data
• No feature scaling needed

*Weakness*
• Prone to overfitting — grows too deep and memorises training data

*Random Forests*
Fix overfitting by building MANY trees and averaging their predictions.

How it works:
1. Take N random samples of the training data (with replacement = "bagging")
2. For each sample, train a decision tree — but only consider a random subset of features at each split
3. For prediction: take majority vote (classification) or average (regression)

*Why it works*
Each tree is slightly different → errors are random and cancel out → ensemble is more accurate and robust than any single tree.

*Key hyperparameters*
• `n_estimators` — number of trees (more = better up to a point)
• `max_depth` — limits tree depth (controls overfitting)
• `max_features` — features considered at each split

*Still widely used in production*
Random Forests power many real-world enterprise systems — interpretable, robust, fast to train, no GPU needed.

📌 *Tomorrow:* Support Vector Machines — finding the widest possible margin between classes."""
    },
    {
        "day": 9,
        "title": "Support Vector Machines",
        "content": """🎯 *Day 9 — Support Vector Machines (SVMs)*

*Core Idea*
Find the decision boundary (hyperplane) that maximises the margin between classes.

Not just any line that separates — the one with the *widest gap*.

*Key Concepts*

*Support Vectors*
The data points closest to the decision boundary.
These are the only points that matter — removing others doesn't change the boundary.

*Margin*
The distance between the boundary and the nearest support vectors.
SVM maximises this margin → better generalisation to new data.

*Hard vs Soft Margin*
• Hard margin → perfectly separable data (rare in real world)
• Soft margin → allows some misclassifications (controlled by parameter C)

*The Kernel Trick*
What if data isn't linearly separable?
Map data to higher dimensions where it becomes separable — without computing the transformation explicitly.

Common kernels:
• Linear — straight-line boundary
• RBF (Radial Basis Function) — most common, handles complex boundaries
• Polynomial — curved boundaries

*When to use SVMs*
✅ High-dimensional data (text classification)
✅ Small-to-medium datasets
✅ Clear margin of separation expected
❌ Very large datasets (slow to train)
❌ Noisy data with overlapping classes

*Historical note*
SVMs dominated ML from ~1995–2012. Now mostly replaced by deep learning and gradient boosting (XGBoost) for most tasks — but still excellent for certain problems.

📌 *Tomorrow:* k-NN and k-Means — two simple but powerful algorithms for classification and clustering."""
    },
    {
        "day": 10,
        "title": "k-NN and k-Means",
        "content": """📍 *Day 10 — k-Nearest Neighbours & k-Means Clustering*

━━━━━━━━━━━━━━━━━━━━
*k-Nearest Neighbours (k-NN) — Supervised*
━━━━━━━━━━━━━━━━━━━━

*Idea*: To classify a new point, find the k most similar training examples and take a majority vote.

No training phase — just memorise all data. Classification happens at query time.

*How similarity is measured*: Euclidean distance (straight-line distance between points in feature space).

*Choosing k*:
• k=1 → overfits (too sensitive to noise)
• k=large → underfits (too smooth)
• Rule of thumb: k = √(number of samples), tune with cross-validation

*Strengths*: Simple, no assumptions about data distribution, naturally handles multi-class.
*Weaknesses*: Slow at prediction (searches all training data), poor on high-dimensional data (curse of dimensionality).

━━━━━━━━━━━━━━━━━━━━
*k-Means Clustering — Unsupervised*
━━━━━━━━━━━━━━━━━━━━

*Idea*: Group data into k clusters where each point belongs to the nearest cluster centre (centroid).

*Algorithm*:
1. Randomly place k centroids
2. Assign each point to nearest centroid
3. Move each centroid to the mean of its assigned points
4. Repeat 2–3 until centroids stop moving

*Choosing k*: The Elbow Method — plot inertia (within-cluster variance) vs k; pick the "elbow" where gains diminish.

*Use cases*: Customer segmentation, document clustering, anomaly detection, image compression.

*Weakness*: Assumes spherical clusters of similar size. Fails on irregular shapes.

📌 *Tomorrow:* Neural Networks — how the brain inspired the most powerful class of ML models."""
    },
    {
        "day": 11,
        "title": "Neural Networks",
        "content": """🧬 *Day 11 — Neural Networks*

*The Biological Inspiration*
Human brain: ~86 billion neurons, each connected to thousands of others.
Artificial neural networks loosely mimic this — but the math matters more than the biology.

*The Building Block: A Neuron (Perceptron)*
1. Takes multiple inputs (x₁, x₂, x₃...)
2. Multiplies each by a weight (w₁, w₂, w₃...)
3. Sums them up and adds a bias
4. Passes through an *activation function*
5. Outputs a value

`output = activation(w₁x₁ + w₂x₂ + ... + b)`

*Activation Functions — Why They Matter*
Without them, the whole network collapses to a single linear equation.
Activations introduce non-linearity — allowing networks to learn complex patterns.

• *ReLU* — `max(0, x)` — most common in hidden layers, fast, works well
• *Sigmoid* — squashes to (0,1) — used in output for binary classification
• *Softmax* — squashes to probabilities summing to 1 — multi-class output
• *Tanh* — squashes to (-1,1) — used in RNNs

*Network Architecture*
• *Input layer* — one neuron per feature
• *Hidden layers* — where learning happens (can be many)
• *Output layer* — one neuron per class (or one for regression)

*Depth vs Width*
• More layers (depth) → learns more abstract representations
• More neurons per layer (width) → captures more patterns at each level

*Universal Approximation Theorem*
A neural network with even one hidden layer can approximate any continuous function — given enough neurons. This is the theoretical basis for why NNs work.

📌 *Tomorrow:* Backpropagation — how neural networks actually learn."""
    },
    {
        "day": 12,
        "title": "Backpropagation",
        "content": """⚙️ *Day 12 — Backpropagation*

*The Problem*
A neural network has millions of weights. How do you adjust all of them to reduce error?

*The Answer: Backpropagation + Gradient Descent*

*Forward Pass*
1. Input data flows through the network layer by layer
2. Each layer applies weights, biases, and activation functions
3. Final layer produces a prediction
4. Loss function measures how wrong the prediction is

*Backward Pass (Backprop)*
1. Calculate the gradient of the loss with respect to the output
2. Use the *chain rule* from calculus to propagate gradients backwards through each layer
3. Each weight gets a gradient: "increase this weight → loss goes up/down by X"
4. Gradient descent updates every weight: `w = w - learning_rate × gradient`

*Chain Rule (simplified)*
If `z = f(g(x))`, then `dz/dx = dz/dg × dg/dx`
Backprop applies this repeatedly across every layer.

*One Training Step*
Forward pass → compute loss → backward pass → update weights → repeat.
This cycle is called one *iteration* or *step*.
One pass through all training data = one *epoch*.

*Vanishing Gradient Problem*
In deep networks, gradients shrink as they flow backward.
Early layers barely update → network doesn't learn.
Solution: ReLU activation, batch normalisation, residual connections (skip connections in ResNets).

*Key insight*
Backprop is the reason deep learning works. It's not magic — it's just efficient calculus applied at scale. Modern frameworks (PyTorch, TensorFlow) compute all of this automatically via *autograd*.

📌 *Tomorrow:* Deep Learning — what "deep" actually means and why it changed everything."""
    },
    {
        "day": 13,
        "title": "Deep Learning",
        "content": """🚀 *Day 13 — Deep Learning*

*What makes it "deep"?*
Simply: many layers. A "shallow" network has 1–2 hidden layers. "Deep" means 10, 50, 100+ layers.

But depth alone isn't why it works.

*The Key Insight: Hierarchical Feature Learning*
Each layer learns increasingly abstract representations:
• Layer 1 → edges and colours (in images)
• Layer 2 → shapes and textures
• Layer 3 → parts (eyes, wheels)
• Layer 4+ → objects, concepts

You don't hand-engineer features — the network learns them from raw data.

*Why Deep Learning Took Off (2012+)*
Three things aligned:
1. *Big Data* — internet-scale datasets (ImageNet: 1.2M images)
2. *GPUs* — parallel computation made training feasible
3. *Better algorithms* — ReLU, dropout, batch norm, better initialisation

*Major Deep Learning Architectures*
• *CNNs* — images and spatial data (Day 15)
• *RNNs/LSTMs* — sequences and time series (Day 16)
• *Transformers* — language, vision, everything now (Day 17)

*Frameworks*
• *PyTorch* — dominant in research, flexible
• *TensorFlow/Keras* — dominant in production deployment
• Both have automatic differentiation (no manual backprop)

*The Hardware Reality*
Training large models requires GPUs or TPUs.
Inference (using a trained model) can run on CPU or even mobile.
This is why cloud AI services (AWS, Azure, GCP) exist — most companies don't own the hardware.

*Deep Learning ≠ Always Better*
For tabular/structured data (your SAP world), gradient boosting (XGBoost, LightGBM) often beats deep learning.
Deep learning wins on: images, text, audio, video, unstructured data.

📌 *Tomorrow:* Week 2 review — then Week 3 goes into the modern architectures driving today's AI."""
    },
    {
        "day": 14,
        "title": "Week 2 Review",
        "content": """🔁 *Day 14 — Week 2 Review*

Self-check before Week 3 (the exciting stuff — Transformers, LLMs, RAG).

*Quick-fire Questions*

1. How does a Decision Tree decide where to split?
2. What is "bagging" and why does Random Forest use it?
3. What does SVM maximise?
4. What does the kernel trick do?
5. In k-NN, what happens when k is too small? Too large?
6. What is an activation function and why is it needed?
7. What are the two passes in neural network training?
8. What is the vanishing gradient problem?
9. Name the three things that enabled deep learning to take off.
10. When should you NOT use deep learning?

*Answers*
1. Maximises information gain (minimises Gini impurity / entropy).
2. Training each tree on a random data sample — reduces variance, prevents overfitting.
3. The margin between classes (distance from boundary to nearest support vectors).
4. Maps non-linearly separable data to higher dimensions where it becomes separable.
5. Too small → overfits (sensitive to noise). Too large → underfits (too smooth).
6. Introduces non-linearity so the network can learn complex patterns.
7. Forward pass (prediction) and backward pass (backpropagation of gradients).
8. Gradients shrink to near-zero in early layers — those layers stop learning.
9. Big Data, GPUs, better algorithms (ReLU, dropout, batch norm).
10. Structured/tabular data — gradient boosting often wins there.

*Week 3 Preview*
CNNs → RNNs/LSTMs → Transformers → LLMs → Embeddings → RAG

This is where it gets directly relevant to the tools you build.

📌 *Tomorrow:* CNNs — how machines see and understand images."""
    },
    {
        "day": 15,
        "title": "Convolutional Neural Networks",
        "content": """👁️ *Day 15 — Convolutional Neural Networks (CNNs)*

*The Problem with Regular Neural Networks for Images*
A 224×224 image = 150,528 pixels × 3 colour channels = 451,584 inputs.
A fully connected layer would have hundreds of millions of parameters. Impractical — and it ignores spatial structure.

*The CNN Solution*
Instead of connecting every neuron to every pixel, use:

*1. Convolutional Layers*
A small filter (e.g., 3×3) slides across the image, computing dot products.
Each filter detects one feature (edge, colour gradient, texture).
Multiple filters → multiple feature maps.
Key: weights are *shared* across the image → massive parameter reduction.

*2. Pooling Layers*
Reduce spatial dimensions (downsample).
Max pooling: take the maximum value in each 2×2 region.
Result: smaller feature maps, more robust to small translations.

*3. Fully Connected Layers*
After several conv+pool blocks, flatten and pass through regular neural network layers for final classification.

*What CNNs Learn (Visualised)*
• Early layers → edges, corners, colours
• Middle layers → textures, patterns
• Deep layers → object parts, faces, wheels, text

*Famous Architectures*
• LeNet (1998) — digit recognition, first practical CNN
• AlexNet (2012) — ImageNet breakthrough
• VGG, ResNet, EfficientNet — increasingly powerful
• ResNet introduced skip connections → solved vanishing gradient for very deep networks

*Beyond Images*
CNNs work on anything with spatial/local structure:
• Text (1D convolutions)
• Audio spectrograms
• Time-series data

📌 *Tomorrow:* RNNs and LSTMs — how AI handles sequences: text, time series, speech."""
    },
    {
        "day": 16,
        "title": "RNNs and LSTMs",
        "content": """🔄 *Day 16 — RNNs & LSTMs: Sequence Models*

*Why Standard Networks Fail on Sequences*
"The cat sat on the ___"
To predict "mat", you need context from earlier in the sentence.
Regular neural networks have no memory — each input is independent.

*Recurrent Neural Networks (RNNs)*
Process sequences by maintaining a hidden state — a "memory" passed from step to step.

At each time step:
`h_t = activation(W_h × h_(t-1) + W_x × x_t + b)`

The hidden state h_t captures everything seen so far.

*The Problem: Vanishing Gradients Over Long Sequences*
For long sequences, gradients from early steps shrink to near zero by the time backprop reaches them. The network can't learn long-range dependencies.
("The cat that sat on the mat near the window was ___" — "cat" is far back)

*LSTMs — Long Short-Term Memory*
Introduced in 1997. Solve the vanishing gradient problem with a gating mechanism:

• *Forget gate* — what to erase from memory
• *Input gate* — what new information to add
• *Output gate* — what to output at this step
• *Cell state* — the long-term memory highway (gradients flow without shrinking)

LSTMs can remember information from hundreds of steps back.

*GRU (Gated Recurrent Unit)*
Simplified LSTM — fewer parameters, similar performance, faster to train.

*Applications*
• Text generation, translation, sentiment analysis
• Speech recognition
• Time-series forecasting
• Anomaly detection in logs

*Historical note*
LSTMs dominated NLP from ~2014–2017.
Then Transformers arrived (2017) and made them largely obsolete for language tasks.
But LSTMs still excel at streaming time-series where transformer's full-context attention is overkill.

📌 *Tomorrow:* Transformers — the architecture that powers Claude, GPT, Gemini, and everything modern AI."""
    },
    {
        "day": 17,
        "title": "Transformers",
        "content": """⚡ *Day 17 — Transformers: The Architecture Behind Modern AI*

*The 2017 Paper That Changed Everything*
"Attention Is All You Need" — Google, 2017.
Eliminated recurrence entirely. Processes sequences in parallel. Scales to massive datasets.

*The Core Mechanism: Self-Attention*
Every word looks at every other word and decides how much to "attend" to it.

Example: "The animal didn't cross the street because *it* was too tired"
What does "it" refer to? Self-attention figures out "it" → "animal" with high weight.

*How Self-Attention Works (Simplified)*
For each word, compute three vectors:
• *Query (Q)* — "what am I looking for?"
• *Key (K)* — "what do I contain?"
• *Value (V)* — "what do I contribute?"

Attention score = Q × Kᵀ (softmaxed) → weighted sum of Values

*Multi-Head Attention*
Run self-attention multiple times in parallel with different learned projections.
Each head learns different relationships (syntactic, semantic, coreference).

*Positional Encoding*
Unlike RNNs, Transformers process all positions simultaneously — so position info must be injected explicitly via positional encodings added to word embeddings.

*The Transformer Architecture*
• *Encoder* — reads input, builds rich contextual representations
• *Decoder* — generates output autoregressively (one token at a time)
• Original: Encoder-Decoder (translation)
• BERT: Encoder only (understanding)
• GPT/Claude: Decoder only (generation)

*Why Transformers Win*
• Parallelisable → trains on massive data quickly (GPUs love it)
• Long-range dependencies handled natively
• Scales extremely well: more data + bigger model = better performance

📌 *Tomorrow:* Large Language Models — how GPT, Claude, and Gemini are actually built and trained."""
    },
    {
        "day": 18,
        "title": "Large Language Models",
        "content": """🌐 *Day 18 — Large Language Models (LLMs)*

*What is an LLM?*
A very large Transformer (decoder-only) trained to predict the next token given all previous tokens.
That's it. The emergent capabilities (reasoning, coding, translation) arise from scale.

*The Training Process*

*Phase 1: Pre-training*
• Dataset: trillions of tokens from the internet, books, code, papers
• Objective: predict the next token (self-supervised — no labels needed)
• Duration: weeks to months on thousands of GPUs
• Result: a "base model" with broad world knowledge

*Phase 2: Supervised Fine-Tuning (SFT)*
• Dataset: human-written demonstrations of helpful responses
• Teaches the model to follow instructions and be an assistant

*Phase 3: RLHF (Reinforcement Learning from Human Feedback)*
• Humans rank pairs of model responses
• Train a reward model on these rankings
• Use RL (PPO) to optimise the LLM toward higher-ranked responses
• This is what makes the model "aligned" — helpful, harmless, honest

*Scale Laws*
More parameters + more data + more compute = better performance.
Predictably. This is the Chinchilla scaling law (2022).

*Emergent Capabilities*
Abilities that appear suddenly at sufficient scale:
• Few-shot learning
• Chain-of-thought reasoning
• Code generation
• Multi-step planning

*Key Models*
• GPT-4, GPT-4o (OpenAI)
• Claude 3.5/4 (Anthropic)
• Gemini (Google)
• Llama 3 (Meta — open source)
• Mistral, Qwen, DeepSeek (open/efficient models)

*Context Window*
How many tokens the model can "see" at once.
Claude: up to 200K tokens. GPT-4: 128K. This matters enormously for long documents.

📌 *Tomorrow:* Embeddings and Vector Databases — how AI understands meaning and similarity."""
    },
    {
        "day": 19,
        "title": "Embeddings & Vector Databases",
        "content": """🔢 *Day 19 — Embeddings & Vector Databases*

*The Problem*
Computers work with numbers. Text, images, and code don't have inherent numerical structure.
How do you represent meaning mathematically?

*Embeddings*
Convert discrete objects (words, sentences, images) into dense vectors of numbers that encode semantic meaning.

Key property: *similar meaning → similar vectors (nearby in space)*

"king" - "man" + "woman" ≈ "queen"
(Famous Word2Vec result demonstrating semantic arithmetic)

*How Text Embeddings Work*
Pass text through an encoder model → get a vector (e.g., 1536 dimensions for OpenAI's model).
Similar sentences cluster together in this high-dimensional space.

*Use Cases*
• Semantic search (find meaning, not keywords)
• Recommendation systems
• Duplicate detection
• Clustering documents by topic
• The foundation of RAG (tomorrow's topic)

*Vector Databases*
Storing and querying millions of embedding vectors efficiently.
The query: "Find the 10 vectors most similar to this query vector."
Similarity metric: cosine similarity or dot product.

*Key Vector DBs*
• *Pinecone* — fully managed, popular
• *Weaviate* — open source, supports hybrid search
• *Qdrant* — open source, Rust-based, fast
• *pgvector* — PostgreSQL extension (easiest if you already run Postgres)
• *ChromaDB* — lightweight, perfect for local/small projects

*Why This Matters for Your Stack*
sf-position-integrity-checker uses SQLite. Adding pgvector or ChromaDB would let you do semantic search across SF metadata, job descriptions, or position hierarchies — far more powerful than keyword matching.

📌 *Tomorrow:* RAG — Retrieval-Augmented Generation. The architecture behind knowledge-grounded AI."""
    },
    {
        "day": 20,
        "title": "Retrieval-Augmented Generation (RAG)",
        "content": """📚 *Day 20 — Retrieval-Augmented Generation (RAG)*

*The Problem with Pure LLMs*
• Knowledge cutoff — don't know recent events
• Hallucination — confidently wrong on specific facts
• No access to your private data (HR records, internal docs)
• Can't cite sources

*The RAG Solution*
Combine a retrieval system with an LLM:
1. Retrieve relevant documents from your knowledge base
2. Inject them into the LLM's context
3. LLM generates an answer grounded in retrieved facts

*The RAG Pipeline*

*Indexing (offline)*
1. Chunk your documents (e.g., 512-token chunks)
2. Embed each chunk → vector
3. Store vectors in a vector database

*Querying (runtime)*
1. User asks a question
2. Embed the question → query vector
3. Find top-k most similar chunks (nearest neighbour search)
4. Inject retrieved chunks + question into LLM prompt
5. LLM answers using the context

*Chunking Strategy Matters*
• Too small → not enough context per chunk
• Too large → dilutes relevance, hits context limits
• Overlap between chunks → prevents cutting context at bad boundaries

*Advanced RAG Techniques*
• *Hybrid search* — combine vector search + keyword search (BM25)
• *Reranking* — second model re-scores top results for relevance
• *HyDE* — generate a hypothetical answer first, then search for similar documents
• *Agentic RAG* — LLM decides what to retrieve and when

*Direct Application to Your Work*
A RAG system over your SF EC documentation, migration runbooks, and cutover plans would let any team member query: "What's the fallback procedure for KR go-live?" and get an accurate, cited answer from your actual documents.

📌 *Tomorrow:* Prompt Engineering — getting the best from LLMs. The most immediately applicable skill."""
    },
    {
        "day": 21,
        "title": "Week 3 Review",
        "content": """🔁 *Day 21 — Week 3 Review*

*Quick-fire Questions*

1. What does a convolutional filter do?
2. What problem do LSTMs solve that vanilla RNNs can't?
3. What are Q, K, and V in self-attention?
4. Why does Transformer training parallelise better than RNNs?
5. What are the three phases of LLM training?
6. What property makes embeddings useful?
7. Name two vector databases.
8. What are the two phases of a RAG system?
9. Why does RAG reduce hallucination?
10. What is a context window?

*Answers*
1. Slides across the input detecting one specific local feature (edge, texture, pattern).
2. Long-range dependencies — LSTMs can remember information from much earlier in the sequence.
3. Query (what I'm looking for), Key (what I contain), Value (what I contribute).
4. Processes all positions simultaneously; RNNs are sequential (each step depends on previous).
5. Pre-training (next token prediction), SFT (instruction following), RLHF (alignment).
6. Similar meaning → similar vectors (close together in embedding space).
7. Any two of: Pinecone, Weaviate, Qdrant, pgvector, ChromaDB.
8. Indexing (embed + store documents) and Querying (retrieve relevant chunks, generate answer).
9. LLM answers from retrieved facts rather than parametric memory — grounded in real documents.
10. Maximum tokens the model can process in one call (its "working memory").

*Week 4 Preview*
Prompt Engineering → AI Agents → MLOps → AI Ethics → Generative AI → AI in Enterprise → RLHF → Frontier Models → Your Personal Learning Path

📌 *Tomorrow:* Prompt Engineering — the most immediately useful skill in the AI toolkit."""
    },
    {
        "day": 22,
        "title": "Prompt Engineering",
        "content": """✍️ *Day 22 — Prompt Engineering*

*What it is*
The craft of designing inputs to LLMs to get reliably excellent outputs.
Not magic — structured communication with a probabilistic system.

*Core Techniques*

*1. Be Specific and Detailed*
Bad: "Summarise this"
Good: "Summarise this in 3 bullet points for a non-technical executive audience, focusing on business impact and timeline"

*2. Role Assignment*
"You are a senior SAP SuccessFactors consultant reviewing a data migration checklist. Identify any gaps."
Sets tone, expertise level, and perspective.

*3. Few-Shot Examples*
Show the model what good output looks like before asking:
"Here are 2 examples of the format I want: [example 1] [example 2]. Now do the same for: [your task]"

*4. Chain-of-Thought (CoT)*
"Think step by step before answering."
Forces the model to reason before concluding → dramatically better on complex tasks.

*5. Output Format Control*
"Respond only in JSON with keys: risk, mitigation, owner, deadline"
Structures output for programmatic use.

*6. Negative Constraints*
"Do not include caveats, disclaimers, or suggestions to consult a professional."

*7. Decomposition*
Break complex tasks into sub-prompts.
Don't ask for a full migration plan in one shot — ask for risks first, then mitigations, then timeline.

*System vs User Prompts*
• System prompt → persistent instructions, persona, constraints
• User prompt → the actual request

*The Prompt Stack for Production Systems*
System prompt (behaviour) + Retrieved context (RAG) + Conversation history + User message = what the LLM sees.

*Meta-skill*
You already do this intuitively — your mega-prompt, output-heavy style is applied prompt engineering.

📌 *Tomorrow:* AI Agents — autonomous systems that plan, use tools, and execute multi-step tasks."""
    },
    {
        "day": 23,
        "title": "AI Agents",
        "content": """🤖 *Day 23 — AI Agents & Agentic Systems*

*What is an AI Agent?*
An LLM that doesn't just respond — it plans, takes actions, observes results, and iterates until a goal is achieved.

Standard LLM: question → answer (one shot)
Agent: goal → plan → action → observe → replan → action → ... → result

*Core Components*

• *Brain (LLM)* — Reasoning, planning, decision-making
• *Tools* — Functions the agent can call (search, code execution, API calls, file I/O)
• *Memory* — Short-term (context window) + long-term (vector DB or files)
• *Orchestrator* — Loop that runs: think → act → observe → repeat

*ReAct Pattern (Reason + Act)*
The dominant agent framework:
```
Thought: I need to find the current SF API endpoint for EC position data
Action: web_search("SAP SuccessFactors EC OData API position entity 2025")
Observation: [search results]
Thought: Now I have the endpoint. I should test it.
Action: api_call(...)
...
```

*Tool Use / Function Calling*
Modern LLMs can call tools by outputting structured JSON specifying function name and arguments.
The orchestrator executes the function and feeds the result back.

*Multi-Agent Systems*
Multiple specialised agents collaborating:
• Planner agent → breaks goal into subtasks
• Executor agents → carry out specific subtasks
• Critic agent → reviews outputs

*Your Hermes Setup*
Hermes IS an agent framework — always-on Oracle Cloud instance orchestrating tasks.
Adding tool use (SF API calls, GitHub Actions triggers, calendar lookups) turns it into a proper autonomous agent.

*Challenges*
• Reliability — agents can get stuck in loops
• Cost — many LLM calls per task
• Safety — agents taking real-world actions need careful guardrails

📌 *Tomorrow:* MLOps — deploying and maintaining ML models in production."""
    },
    {
        "day": 24,
        "title": "MLOps",
        "content": """⚙️ *Day 24 — MLOps: ML in Production*

*The Gap*
Building a model in a notebook is easy. Keeping it accurate, available, and trustworthy in production for 2 years is hard.
MLOps is the discipline that bridges research and production.

*The ML Lifecycle*
Data → Feature Engineering → Training → Evaluation → Deployment → Monitoring → Retraining → (repeat)

*Key MLOps Concerns*

*1. Reproducibility*
Can you recreate your model exactly? Track:
• Code version (Git)
• Data version (DVC, Delta Lake)
• Hyperparameters and model config
• Training environment (Docker, conda env)
Tools: MLflow, Weights & Biases, DVC

*2. CI/CD for ML*
Every code change triggers: unit tests → data validation → model training → evaluation → deployment (if metrics pass).
Same principle as software CI/CD, applied to model pipelines.

*3. Model Serving*
How users/systems access the model:
• REST API (FastAPI + model loaded in memory)
• Batch inference (scheduled jobs on large datasets)
• Streaming inference (real-time event processing)
Tools: BentoML, TorchServe, Triton, SageMaker

*4. Model Monitoring*
Models degrade silently in production.
Monitor for:
• *Data drift* — input distribution changes vs training data
• *Concept drift* — relationship between features and labels changes
• *Performance drift* — accuracy drops on new data
• *Latency and error rates*

*5. Feature Stores*
Centralised repository for computed features — ensures training and serving use identical feature computation.
Tools: Feast, Tecton, Hopsworks

*The Production Reality*
Most ML models never reach production. Of those that do, most degrade within months without active monitoring.
MLOps is what separates ML experiments from ML products.

📌 *Tomorrow:* AI Ethics, Bias, and Safety — the non-negotiable layer."""
    },
    {
        "day": 25,
        "title": "AI Ethics & Safety",
        "content": """⚖️ *Day 25 — AI Ethics, Bias & Safety*

*Why it matters technically, not just morally*
Biased models create legal liability, poor products, and erode user trust.
Safety failures in agentic systems can cause real-world harm.
Understanding this makes you a better AI engineer.

*Types of Bias*

*Data Bias*
Training data reflects historical human decisions — which contain historical discrimination.
Example: CV screening model trained on past hires → perpetuates hiring biases.

*Representation Bias*
Certain groups underrepresented in training data → worse performance for them.
Example: facial recognition failing on darker skin tones (trained mostly on lighter faces).

*Measurement Bias*
Proxy metrics don't capture what you actually care about.
Example: using arrest rates as a crime proxy — reflects policing patterns, not actual crime.

*Amplification Bias*
Models learn and amplify correlations in data.
"Doctor" → male, "nurse" → female (from historical text).

*Fairness Metrics (often in conflict)*
• Individual fairness: similar people get similar outcomes
• Group fairness: equal error rates across demographic groups
• Calibration: predicted probabilities match actual frequencies
You usually can't optimise all simultaneously.

*AI Safety*
• *Alignment* — ensuring AI does what humans actually want (not just what we specified)
• *Robustness* — behaving correctly on unusual inputs, adversarial attacks
• *Interpretability* — understanding WHY a model made a decision (critical in regulated industries)
• *Containment* — preventing agentic systems from taking unintended real-world actions

*In Your Domain*
SF EC data migration decisions affect people's employment records, payroll, and entitlements.
Any ML/AI applied to HR data carries significant fairness and regulatory obligations (GDPR, employment law).

📌 *Tomorrow:* Generative AI — diffusion models, image generation, video, and multimodal AI."""
    },
    {
        "day": 26,
        "title": "Generative AI",
        "content": """🎨 *Day 26 — Generative AI: Images, Video & Multimodal*

*What is Generative AI?*
AI that creates new content — images, audio, video, code, 3D — rather than classifying existing content.

*Two Dominant Paradigms*

━━━━━━━━━━━━━━━
*GANs (Generative Adversarial Networks) — 2014*
Two networks trained adversarially:
• *Generator* — creates fake images
• *Discriminator* — distinguishes real vs fake
They compete: Generator gets better at fooling Discriminator, which gets better at detecting fakes.
Result: photorealistic image generation.

Problems: training instability, mode collapse (generator finds one trick and repeats it).

━━━━━━━━━━━━━━━
*Diffusion Models — 2020–present*
Current state of the art (Stable Diffusion, DALL-E 3, Midjourney, Sora).

Training: gradually add Gaussian noise to images until pure noise → train model to reverse this process (denoise).
Generation: start from random noise → iteratively denoise → coherent image.

Advantages: stable training, high quality, controllable via text prompts.

*Text-to-Image Pipeline*
1. Text prompt → CLIP/text encoder → text embedding
2. Random noise in latent space
3. U-Net iteratively denoises conditioned on text embedding
4. Decode latent → full-resolution image

*Video Generation*
Extend diffusion to temporal dimension.
Sora (OpenAI), Runway Gen-3, Kling — model motion, physics, scene consistency across frames.

*Multimodal Models*
Handle multiple modalities in one model:
• Text + Image → GPT-4V, Claude, Gemini
• Text + Audio + Video → Gemini 1.5

*The Convergence*
Everything is becoming one model: text, image, audio, video, code — all embeddings in a shared representation space.

📌 *Tomorrow:* AI in Enterprise — where AI actually creates value in businesses like yours."""
    },
    {
        "day": 27,
        "title": "AI in Enterprise",
        "content": """🏢 *Day 27 — AI in Enterprise & Your Domain*

*Where Enterprise AI Actually Creates Value*
Not robots replacing workers — mostly: automating repetitive cognitive tasks, augmenting decision-making, extracting signal from large datasets.

*High-ROI Enterprise Use Cases*

*Document Processing*
• Contract analysis, invoice extraction, compliance checking
• IDP (Intelligent Document Processing) — structured extraction from unstructured docs
• Direct relevance: SF EC data migration involves massive legacy HR document ingestion

*Predictive HR Analytics*
• Attrition prediction — who's likely to leave in the next 6 months
• Workforce planning — demand forecasting by skill and location
• Compensation benchmarking — market data + internal equity analysis

*Intelligent Search*
• Enterprise knowledge bases searchable by meaning, not keywords
• "Find all positions in the Netherlands with grade band 4–6 that don't have a cost centre assigned" → RAG over SF data

*Code Generation & Review*
• GitHub Copilot, Cursor → 20–40% productivity gains for developers
• ABAP code generation — still early but improving

*Process Automation*
• Agentic systems handling multi-step approval workflows
• SF approval chain automation (stuck approval detection → your sf-workflow-monitor)

*SAP + AI*
SAP Joule — SAP's embedded AI assistant across S/4HANA, SuccessFactors.
Current capabilities: natural language queries, auto-populate fields, anomaly detection in time data.
Future: autonomous HR process execution.

*The Honest Assessment*
Most "enterprise AI" is still RAG + LLM wrapper over internal documents.
The companies winning are those with clean, structured data — exactly what SF EC data migration creates.

Your migration work is foundational infrastructure for enterprise AI. The better the data model, the more powerful the AI layer on top.

📌 *Tomorrow:* RLHF — the technique that makes LLMs helpful and aligned."""
    },
    {
        "day": 28,
        "title": "RLHF",
        "content": """🎯 *Day 28 — Reinforcement Learning from Human Feedback (RLHF)*

*The Problem RLHF Solves*
A base LLM trained on internet text can generate harmful, dishonest, or unhelpful content.
Pre-training optimises for predicting text — not for being a useful assistant.
RLHF aligns the model's behaviour with human values and preferences.

*The Three-Stage Pipeline*

*Stage 1: Supervised Fine-Tuning (SFT)*
• Human labellers write ideal responses to diverse prompts
• Fine-tune the base model on these demonstrations
• Result: model that knows roughly what good responses look like

*Stage 2: Train a Reward Model (RM)*
• Present human labellers with pairs of model responses to the same prompt
• Labellers rank which response is better (and why)
• Train a separate neural network (Reward Model) to predict human preference scores
• Result: automated proxy for "human thinks this is a good response"

*Stage 3: RL Optimisation (PPO)*
• Use the reward model as the reward signal
• Optimise the LLM using Proximal Policy Optimisation (PPO) — an RL algorithm
• Constraint: don't diverge too far from the SFT model (KL penalty) — prevents reward hacking

*Reward Hacking*
The model finds ways to score highly on the reward model without being genuinely good.
Example: verbosity (longer answers scored higher) → model learns to pad responses.
The reward model is an imperfect proxy. Optimise it too hard → Goodhart's Law.

*Modern Alternatives*
• *DPO (Direct Preference Optimisation)* — eliminates the separate reward model; simpler, more stable
• *Constitutional AI (Anthropic)* — model critiques and revises its own outputs against a constitution
• *RLAIF* — AI feedback instead of human feedback (scalable but less grounded)

*Why This Matters*
RLHF is what turns a raw language model into Claude, ChatGPT, or Gemini.
Without it: capable but uncontrollable.
With it: capable AND helpful, harmless, and honest.

📌 *Tomorrow:* Frontier Models & the AGI Debate — where is AI actually headed?"""
    },
    {
        "day": 29,
        "title": "Frontier Models & the AGI Debate",
        "content": """🔭 *Day 29 — Frontier Models & the AGI Debate*

*What are Frontier Models?*
The most capable AI systems at any point in time — pushing the boundary of what's possible.
Current frontier: GPT-4o, Claude 3.5/4, Gemini 1.5 Ultra, Llama 3 405B.

*Scaling Laws — The Engine of Progress*
Empirical finding: model capability scales predictably with:
compute × data × parameters

This means progress is somewhat *guaranteed* if you have the resources.
Frontier labs are spending $1B+ per training run.

*Emergent Capabilities*
At sufficient scale, new abilities appear with no explicit training:
• Multi-step reasoning
• Code generation
• Mathematical problem-solving
• Theory of mind (limited)

No one fully understands WHY this happens — it's one of the deepest open questions in AI.

*The AGI Debate*

*Optimist view (Altman, Hassabis)*
AGI within 5–10 years. Scaling continues to work. Models are approaching general problem-solving ability.

*Sceptic view (LeCun, Marcus)*
Current architectures are fundamentally limited. LLMs are sophisticated pattern matchers, not reasoners. True understanding requires embodiment, causality, world models.

*The honest answer*
Nobody knows. "AGI" isn't even well-defined. Current systems are genuinely impressive and genuinely limited in specific ways.

*Trends to Watch*
• *Test-time compute* — models thinking longer (chain-of-thought, o1/o3 style) rather than just bigger
• *Multimodal* — text + image + audio + video as native inputs
• *Agents* — models taking real-world actions autonomously
• *Open source* — Llama, Mistral, Qwen closing the gap with proprietary models
• *Specialised models* — smaller, domain-specific models outperforming giant general models on narrow tasks

*What This Means For You*
AI is a platform shift — like mobile or cloud.
The practitioners who understand both the capabilities AND the limitations will build the most valuable things.
You're already doing this.

📌 *Tomorrow:* Day 30 — Full review + your personalised path forward."""
    },
    {
        "day": 30,
        "title": "Full Review & Your Path Forward",
        "content": """🎓 *Day 30 — Full Review & Your Personalised Path Forward*

Congratulations. 30 days. The full ML/AI stack.

*What You Now Know*

*Foundations (Week 1)*
✅ AI taxonomy (Narrow → AGI → ASI)
✅ ML types: Supervised, Unsupervised, Reinforcement
✅ Data: features, labels, train/val/test splits
✅ Linear regression, gradient descent, loss functions
✅ Classification, precision/recall, F1
✅ Overfitting, underfitting, bias-variance tradeoff

*Core Algorithms (Week 2)*
✅ Decision Trees, Random Forests (bagging, ensemble)
✅ SVMs (margin maximisation, kernel trick)
✅ k-NN (lazy learning), k-Means (clustering)
✅ Neural networks (perceptrons, activation functions, layers)
✅ Backpropagation (chain rule, gradient flow)
✅ Deep Learning (hierarchical features, scale, GPUs)

*Modern AI (Week 3)*
✅ CNNs (convolution, pooling, feature maps)
✅ RNNs/LSTMs (sequence modelling, gating, memory)
✅ Transformers (self-attention, Q/K/V, parallelism)
✅ LLMs (pre-training, SFT, RLHF, scaling laws)
✅ Embeddings (semantic vectors, similarity search)
✅ RAG (retrieval-augmented generation, chunking, indexing)

*Applied (Week 4)*
✅ Prompt engineering (CoT, few-shot, format control)
✅ AI Agents (ReAct, tool use, multi-agent)
✅ MLOps (drift, monitoring, CI/CD for ML)
✅ AI Ethics (bias types, fairness, alignment)
✅ Generative AI (diffusion models, GANs, multimodal)
✅ Enterprise AI (HR analytics, RAG over internal data)
✅ RLHF (reward model, PPO, DPO, Constitutional AI)
✅ Frontier models (scaling, emergence, AGI debate)

*Your Natural Next Steps*

Given your stack (Python, GitHub Actions, Oracle Cloud, SF OData, Hermes agent):

1. *Build a RAG system over your SF documentation*
   Chunk your runbooks → embed → ChromaDB → query interface.
   Most impactful immediate project.

2. *Add tool use to Hermes*
   SF API calls + GitHub triggers + calendar = genuine autonomous agent.

3. *Learn PyTorch basics*
   Not to train models from scratch — to understand fine-tuning and embeddings at code level.
   fast.ai course is the best entry point.

4. *Explore LangChain or LlamaIndex*
   Orchestration frameworks for RAG + agents. Accelerate the RAG project.

5. *Target: ML Engineering, not Data Science*
   Your strength is systems and integration. ML Engineering (deploying, integrating, maintaining AI systems) is where your SAP + Python + cloud background creates massive leverage.

You've built the mental model. Now build things with it. 🚀"""
    },
]


# ── Core Logic ─────────────────────────────────────────────────────────

async def send_lesson(bot: Bot, day: int) -> bool:
    """Send the lesson for the given day (1-indexed)."""
    if day < 1 or day > len(CURRICULUM):
        log.error("Day %d out of range (1-%d)", day, len(CURRICULUM))
        return False

    lesson = CURRICULUM[day - 1]
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=lesson["content"],
            parse_mode="Markdown",
        )
        log.info("Sent Day %d: %s", day, lesson["title"])
        return True
    except TelegramError as e:
        # If Markdown parsing fails (special chars), retry as plain text
        if "can't parse entities" in str(e).lower():
            log.warning("Markdown parse failed for Day %d, retrying as plain text", day)
            try:
                await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=lesson["content"],
                )
                log.info("Sent Day %d (plain text fallback): %s", day, lesson["title"])
                return True
            except TelegramError as e2:
                log.error("Plain-text fallback also failed for Day %d: %s", day, e2)
                return False
        log.error("Telegram error on Day %d: %s", day, e)
        return False


async def get_current_day() -> int:
    """Read current day from state file. Creates file at day 1 if missing."""
    if not STATE_FILE.exists():
        STATE_FILE.write_text("1")
        log.info("Initialised state file at day 1")
        return 1
    try:
        return int(STATE_FILE.read_text().strip())
    except (ValueError, OSError) as exc:
        log.error("Corrupted state file: %s. Resetting to day 1.", exc)
        STATE_FILE.write_text("1")
        return 1


async def increment_day(current: int) -> None:
    """Increment day counter."""
    STATE_FILE.write_text(str(current + 1))


async def main() -> None:
    """Send today's lesson and increment counter."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Verify bot connection
    try:
        me = await bot.get_me()
        log.info("Bot connected: @%s", me.username)
    except (NetworkError, TimedOut, TelegramError) as exc:
        log.error("Failed to connect to Telegram: %s", exc)
        sys.exit(1)

    day = await get_current_day()

    if day > len(CURRICULUM):
        if day == len(CURRICULUM) + 1:
            # First time completing -- send congratulations once
            log.info("Curriculum complete! All %d days sent.", len(CURRICULUM))
            try:
                await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=(
                        "🎓 *AI/ML 30-Day Course Complete!*\n\n"
                        "You've covered the full curriculum.\n"
                        "Review any day by running: `python bot.py --day N`\n"
                        "Reset to start over: delete `current_day.txt`"
                    ),
                    parse_mode="Markdown",
                )
            except TelegramError as exc:
                log.error("Failed to send completion message: %s", exc)
        else:
            # Already completed -- no-op so GitHub Actions doesn't re-spam
            log.debug("Curriculum already complete (day=%d). Nothing to do.", day)
        return

    success = await send_lesson(bot, day)
    if success:
        await increment_day(day)
        log.info("Day %d sent successfully. Next: Day %d", day, day + 1)
    else:
        log.error("Failed to send Day %d. Counter NOT incremented.", day)
        sys.exit(1)


# ── Entry Point ────────────────────────────────────────────────────────
if __name__ == "__main__":
    if "--day" in sys.argv:
        try:
            idx = sys.argv.index("--day")
            day_override = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("Usage: python bot.py --day <1-30>", file=sys.stderr)
            sys.exit(2)

        async def run_specific() -> None:
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            ok = await send_lesson(bot, day_override)
            if ok:
                log.info("Manual send: Day %d sent (counter unchanged)", day_override)
            else:
                log.error("Manual send: Day %d FAILED", day_override)
                sys.exit(1)
        asyncio.run(run_specific())
    else:
        asyncio.run(main())
