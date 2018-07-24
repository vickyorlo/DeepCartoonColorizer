import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('result_formatted.csv', delimiter=';', index_col=0)

_, cols = df.shape
half = int(cols / 2) + 1


data_seen = df.iloc[:, 1:half].values
data_unseen = df.iloc[:, half:].values
data_all = df.iloc[:, 1:].values

df_seen = pd.DataFrame(data_seen, columns=['R{}'.format(x) for x in range(1, 13)])
df_unseen = pd.DataFrame(data_unseen, columns=['U{}'.format(x) for x in range(1, 13)])

cols = ['R{}'.format(x) for x in range(1, 13)] + ['U{}'.format(x) for x in range(1, 13)]
df_all = pd.DataFrame(data_all, columns=cols)


boxplot_seen = df_seen.plot.box()
plt.xlabel('Case ID')
plt.ylabel('Raters score')
plt.savefig('seen.png')

boxplot_unseen = df_unseen.plot.box()
plt.xlabel('Case ID')
plt.ylabel('Raters score')
plt.savefig('unseen.png')

boxplot_data_all = df_all.plot.box()
plt.xlabel('Case ID')
plt.ylabel('Raters score')
plt.savefig('data_all.png')
plt.show()
