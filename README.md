# Simple python script to track bus
- Use open data from PTX: https://ptx.transportdata.tw/PTX/
- OData API doc: https://ptx.transportdata.tw/MOTC

# Usage
```bash
$ export LINE_TOKENS=token001,token002,token003
$ python main.py <bus_number> <direction, 0:去程, 1:返程> <target_stop>
```
ex.  
> export LINE_TOKEN=my-line-token  
> python main.py 672 1 博仁醫院

## LINE notify token
1. Login to https://notify-bot.line.me/my/
2. `發行權杖`
3. Choose `透過一對一聊天室接收LINE Notify的通知`
4. Copy and remember the token


# Implementation

## Used API
- [Get stops of a bus route](https://ptx.transportdata.tw/MOTC/?urls.primaryName=%E5%85%AC%E8%BB%8AV2#/CityBus/CityBusApi_StopOfRoute_2039)
- [Get realtime near stop buses](https://ptx.transportdata.tw/MOTC/?urls.primaryName=%E5%85%AC%E8%BB%8AV2#/CityBus/CityBusApi_RealTimeNearStop_2031)

## Steps
1. Get data of stops of the target bus route (ex '672', directiton 1)
2. Use data of stops to get the target stop (ex. '博仁醫院')
3. Get the running buses that are near bus stops
4. If any of the stops are ahead of the target stop by 3~5 stops, notify users with LINE notify API
5. Sleep for several seconds and start from step (3) to check for next round
