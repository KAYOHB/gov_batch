# gov_batch
Gov updates
This project is a simple end-to-end pipeline which extracts data from the Injective API on https://lcd.injective.network/swagger/#/

The Data is then cleaned and then Loaded into a local MySQL database and then sent to the Injective community telegram chat. It uses the Telegram API service where updates are sent to the localhost address which is listening to webhook events.

The most challenging task was to to transform the denom values to a readable format as each denom has a specific decimals value. Denoms from Ethereum vary to Denoms from Cosmos chain, so when you have a market such as atom/usdt, you have to automate the code to take this into consideration

The code isn't perfect and needs improving but the good thing is that I understand where I can imrpove on and will do so for the next patch!
