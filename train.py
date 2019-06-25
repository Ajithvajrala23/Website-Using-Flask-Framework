from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
from textblob.sentiments import NaiveBayesAnalyzer
import io

blob = TextBlob("I lov you ", analyzer=NaiveBayesAnalyzer())
#
postive = blob.sentiment.p_pos
negative = blob.sentiment.p_neg
height = [postive, negative]

bars = ('positive', 'Negative')
y_pos = np.arange(len(bars))


plt.bar(y_pos, height, color=('green', 'red'))
plt.xticks(y_pos, bars)
#plt.show()
img = io.StringIO()
print(postive, negative)

plt.savefig(img, format='png')
img.seek(0)
plot_url = base64.b64encode(img.getvalue())