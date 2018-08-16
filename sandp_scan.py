from iexfinance import get_historical_data
from datetime import datetime
import pandas as pd
import numpy as np
from list import s_and_p

# current_symbol = 'AAPL'

for symb in s_and_p:
	try:
		start = datetime(2013, 9, 10)
		end = datetime(2018, 8, 10)

		df = get_historical_data(symb, start=start, end=end, output_format='pandas')

		# df.drop(['high', 'low', 'volume'], axis=1)
		df = df.drop(columns=['high', 'low','volume'])
		df = df.rename(columns={"open": symb})


		# S_shifted is the close price at the targeted trading out by a number of days
		df['S_shifted'] = df.close.shift(-1)



		df['number_index'] = range(1, len(df) + 1)
		df['date'] = df.index
		df.index = df['number_index']

		df.drop(columns='number_index', axis=1, inplace=True)


		# change_per is the chnage percentage from the last trading day
		df['change_per'] = ((df['close']-df['close'].shift(1))/df['close'])*100 
		df['symbol']=symb
		df = df.round(2)
		# print(df)

		target_change = [5, -5.0,]

		for change in target_change:
			returns = []
			Average = 0

			for index, row in df.iterrows():
				

				if change > 0:
					if 	float(row['change_per']) > change:
						
						# difference_per is the percentage change between the target day's close and this day's close
						difference_per = ((row['S_shifted']-row['close'])/row['close'])*100

						# print(row['symbol'], row['change_per'], row['close'], row['date'],row['S_shifted'])
						# print(round(difference_per,2))
						returns.append(round(difference_per,2))

				if change < 0:
					if 	float(row['change_per']) < change:
						
						# difference_per is the percentage change between the target day's close and this day's close
						difference_per = ((row['S_shifted']-row['close'])/row['close'])*100

						# print(row['symbol'], row['change_per'], row['close'], row['date'],row['S_shifted'])
						# print(round(difference_per,2))
						returns.append(round(difference_per,2))


			if returns:			
				Average = np.mean(returns)
			if (Average > .75 or Average < -.75) and len(returns) > 3:
				print(symb, 'Targ Change: ',change, 'Avg Ret: ', round(Average,2), 'Occurences: ',len(returns))
	except:
		pass



