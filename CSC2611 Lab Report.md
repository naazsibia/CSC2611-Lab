# CSC2611 Lab: Word embedding and semantic change

**Student**: Naaz Sibia

**Utorid**: `sibianaa`

**Student Number**: `1004432321`

**GitHub Repository**: [link](https://github.com/naazsibia/CSC2611-Lab)

--------

### Synchronic Change

**Check** `synchronic.ipynb`

For *analogy test* on LSA models, please check `basic-exercise.ipynb`. (I didn't want to duplicate code)

####  Pearson correlation between word2vec-based and human similarities

Calculating the correlation between word2vec and human similarities, I get the value 0.7627 -- which is very good to excellent correlation. Comparing this to the values I got from LSA and word-context vectors:

```
Correlation with M1: 0.14360014298240253
Correlation with M1+: 0.2421342509950241
Correlation with M2_10: 0.167807592945941
Correlation with M2_100: 0.3328363250230704
Correlation with M2_300: 0.3515146719359085
```

We can see that the correlation with word2vec is *notably* more effective compared to LSA and word-context vectors in capturing human-like similarities. 

In the earlier exercise, I saw that applying PPMI (M1+) improved the correlation with human-judged scores slightly compared to the word context vector model (M1), suggesting that PPMI offered a better representation of word relationships in this case than raw bigram frequencies. This might be because, in the word context vector model, some words might just frequently occur together by chance without having meaningful relationships. On the other hand, PMI aims to highlight words that co-occur more often than expected by chance. 

Conducting latent semantic analysis (LSA) improved the correlations a bit more when we reduced the dimensionality to 100 and 300 components while reducing the dimensionality to just 10 components reduced our correlation a lot although it was still slightly better than the word context model, suggesting that it might be overfitting.

Using word2vec, a neural-network-based approach, improved the correlation a lot more than LSA demonstrating that this approach is more aligned with human judgement scores than a matrix-based approach like LSA.



#### Analogy Tests

**Analogy Test on word2vec**

Conducting semantic (N = 8869 tests) and syntactic (N = 10675 tests) analogy tests with the pre-trained word2vec embeddings resulted in an accuracy of 74.15% for semantic analogies and 73.90% for syntactic analogies, indicating that the model predicts correctly more than 73% of the time for both tests. When I filter the tests to *only* include words present in both the word2vec and LSA models, I get a semantic (N = 162 tests) accuracy of 88.88% from word2vec and a syntactic (N = 2045 tests) accuracy of 67.87%.



**Analogy Test on LSA Model**

Conducting the same tests with the LSA model, I got a result of 0% for both the semantic (N = 162) and syntactic (N = 2045) analogy tests. If this result is right, then it appears that LSA is not good at capturing relational information between words like word2vec can. Methods like word2vec are specifically designed for this task. LSA focuses on capturing the underlying structure of the data by reducing its dimensionality, but this might come at the cost of losing some relationships between words.

---------------------------

#### Suggestions to improve vector-based models

**More Data**: For our matrices, we extracted bigrams from the Brown corpus which has around 1 million words. Meanwhile, the Google News dataset which word2vec is trained on has about 100 billion words. Having a larger training dataset can improve the scores calculated by our vector-based models. While my response here really tries to capture the *frequency* aspect by data size more, I will also expand on datasets a bit further below.

**Temporal Dynamics**: The Brown Corpus mainly captures dynamics from the 1960s. Meanwhile, the Google News dataset spans many years. It is important to acknowledge here that this shouldn't really be affecting our current results as the human scores we saw (RG65) come from a paper published in 1965, so adding more temporal dynamics to the dataset may not improve the scores to our current tests much (comparison to human scores). However, they can improve the model's performance on other human tests.

**Cultural Diversity:** The texts in the Brown corpus are primarily from American authors, which might not capture the full range of English dialects and their idiosyncrasies. Meanwhile, the human similarity scores that we compared the models against might come from a range of different cultures. So training the models on more culturally diverse texts might improve its performance.

**Model improvements:** in terms of the model itself, we can consider refining our embeddings by using resources such as *WordNet* as it groups words together based on their meanings. 

As we saw earlier, the choice of dimensions also played an important role in the performance of our models. So it is important to consider various dimensions to see which model fits best. We used PCA in this exercise, and people commonly use the *elbow method* to evaluate what a good number of features might be. 

--------

# Diachronic Change

**Check** `diachronic.ipynb`

### Three Different Methods

The three methods I chose were:

- Cosine distance between the first and last decade for a word's embeddings
- Maximum cosine distance between each consecutive decade for a word's embeddings
- Average cosine distance per decade change

I believe the first method can identify words which have changed significantly between 1900-2000 - but it can fail to identify any words that may have changed for a few years but gone back to their original meaning (temporary change). The second method might be adept at highlighting words that experience sharp semantic pivots, but it may miss out on words that exhibited more gradual, yet significant, changes over the entire century. Finally, the last method can capture both slow and more dramatic shifts. However, it might dilute the impact of significant changes that happened over a shorter duration, especially if they're counterbalanced by periods of stability.



To save space, I will redirect you to check the top 20 most and least common words from each method in the `diachronic.ipynb` file! Link.

#### Intercorrelations

```
      M1          M2        M3
M1[1         0.61023698 0.64038365]
M2[0.61023698 1         0.81572133]
M3[0.64038365 0.81572133 1        ]
```

As we can see, M2 and M3 are most correlated - which can be explained by the fact that both methods look for changes in each decade while the first method, M1, looks for changes across the century. We also see that M1 might be more similar to M3 than M1, which makes sense as M3 might be better at capturing more gradual changes than M2.



### Accuracy

To evaluate the accuracy of my methods, I used the human similarity judgements of English word pairs from different time periods shared in this paper: https://aclanthology.org/2020.acl-main.365/

The aggregate.csv file [here](https://zenodo.org/records/3773250) captures similarity scores from different people on a scale from 1-4. I used the lemmas in this file and only included words which were present in both this file and the embeddings given. Next, I took an average of the human scores in the file and compared them to the scores generated by the three methods outlined above. Pearson correlation tests revealed the following:

```
Pearson correlation for Method 1: 0.960132915191522
Pearson correlation for Method 2: 0.878203900604992
Pearson correlation for Method 3: 0.7860157388397276
```

While the correlations here are high, I will note that for a more reliable evaluation, I will need to use a dataset with a lot more words. But the current tests reveal that method 1 may perform better than methods 2 and 3.



### Detecting Point Change

To detect point change, I propose calculating changes in cosine similarities between words in each decade (note: I have to restrict to a decade here since we only have embeddings for each decade). We can use this list of similarities to check when the change in similarities is greater than a certain threshold. In my code, I have used the threshold 0.1. 

The three most common words I got were: `['signal', 'card', 'mirror']` 

Using my method I got the following graphs:

![image-20231027003102878](/Users/naazsibia/Library/Application Support/typora-user-images/image-20231027003102878.png)

![image-20231027003118204](/Users/naazsibia/Library/Application Support/typora-user-images/image-20231027003118204.png)

![image-20231027003125026](/Users/naazsibia/Library/Application Support/typora-user-images/image-20231027003125026.png)

The graphs show that the word `signal` may have changed earlier in the decade just like `mirror`. While the word signal is known to have changed due to technological advancements such as the use radio or television as opposed to just signalling or signing. The word `mirror` has also changed from referring to a polished surface to also being used in literary work ("mirror to the society") as well as scientific advancements such as mirrors in telescopes. However, I am uncertain that it may have changed as drastically as suggested here, and the embeddings might need to be examined further. Cards as we know have switched from being used to refer to playing cards and greeting cards to even sim cards and memory cards.  
