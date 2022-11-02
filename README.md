# M5 WRMSSE

Calculate the WRMSSE of a 28-day forecast for the M5 competition hosted by Kaggle. Instead of uploading submission files to Kaggle for an accuracy score, install the m5-wrmsse package and calculate it locally.

For more information on the derivation, visit

<a href="https://www.pmorgan.com.au/tutorials/wrmsse-for-the-m5-dataset/">https://www.pmorgan.com.au/tutorials/wrmsse-for-the-m5-dataset/</a>

## Installation

Clone the repo

	git clone git@github.com:pmrgn/m5-wrmsse.git

Or download and install the package using `pip`

	pip install m5-wrmsse

## Usage

The `wrmsse` function returns the WRMSSE of a 28-day forecast, equivalent to what Kaggle calculates for it's public leaderboard. First, import the function

	from m5_wrmsse import wrmsse

Pass your forecast as a numpy array to the function, which must be of shape (30490, 28).
	
	my_forecast = np.ones((30490,28))     # Forecast example containing all ones
	score = wrmsse(my_forecast)