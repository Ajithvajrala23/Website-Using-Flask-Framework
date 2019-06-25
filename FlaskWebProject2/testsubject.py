from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    negative = score['neg']
    positive = score['pos']
    neutral = score['neu']
    #print("{:-<40} {}".format(sentence, str(score)))
    print(positive, negative, neutral)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())


sentiment_analyzer_scores("I really hate this restaurant. the food is totally bad and stupid")