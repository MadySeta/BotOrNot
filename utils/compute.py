import numpy as np

def BotRatio(all_predictions : list):
  ratio = all_predictions.count("bot")/len(all_predictions)
  return ratio 
def HumanRatio(all_predictions : list):
  ratio = all_predictions.count("bot")/len(all_predictions)
  return ratio 
  
def FollowersBotHumanPercentage( humanprobabilities, botprobabilities):
    trust_bot_array = np.array(botprobabilities)
    trust_human_array = np.array(humanprobabilities)

    average_bot = np.mean(trust_bot_array)
    average_human = np.mean(trust_human_array)

    return average_bot , average_human
