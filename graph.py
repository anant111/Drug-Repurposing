import pandas as pd 
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("pos.csv")
columns = list(df)


#fig, axes = plt.subplots()
#bplot1 = axes.boxplot(df[columns[0]])  # will be used to label x-ticks
#axes.set_title('Rectangular box plot')
#plt.show()



#sns.set(style="whitegrid")
#a = '/home/anant/Pictures/pos/'
#plt.ylim(-1000, 50000)
#splot = sns.boxplot(y=df[columns[0]],width = 0.2)
#splot = sns.swarmplot(y=df[columns[0]])
#fig = splot.get_figure()
#plt.show()
#fig.savefig("output.png")

#for i in columns:
#	myFig = plt.figure();
#	boxplot = df.boxplot(column=i)
#	plt.ylim(-5, 10000)
#
#	myFig.savefig(a+str(i)+'.svg', format="svg",vert = False)
#	plt.close()
#	break

a = df[columns[0]].plot.kde() #distribtuion
plt.show()