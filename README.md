This repository contains code for https://arxiv.org/abs/2005.09803. "A Computational Analysis of Polarization on Indian and Pakistani Social Media"

File propogation.py contains the code used for hashtag propogation model used in the paper. 

## Data Collection and Statistics

We collected Twitter data using the standard Twitter API (https://developer.twitter.com/en/docs/tweets/search/overview/standard). The API collects relevant tweets that contain the provided keywords from the last 7 days. We collected data on February 20th, February 26th, and March 4th to obtain tweets during the relevant time period. All the data collection was done using the keywords given below except *Balakot* and *Abhinandan*, which were added after the airstrikes. We de-duplicated the collected tweets to remove tweets collected twice during multiple collection runs. 

To check whether our collected tweets covered most of the debate on these events, we scraped the timelines of the 100 most-followed politicians in India and Pakistan during the incidents. For Pakistan politicians, we found that 1,566 tweets were in our original keyword-based collection of tweets and 333 tweets were not part of our collection. On manual inspection, out of the total 333, only 40 tweets were found to be related to Pulwama and the rest were not relevant. For Indian politicians, we found that 2,615 tweets were in the original keyword-based collection and 70 tweets were not, out of which only 23 tweets were found to be related to the incident. Thus, we believe our data set contains comprehensive coverage of tweets related to these events.

**Keywords used for data collection**:
PulwamaAttack, 
Pulwama, 
TerroristArmy, 
PhulwamaTerrorAttack, 
PhulwamaRevenge, 
KashmirTerror, 
PakistanZindaba, 
KashmiriStudents, 
KashmirBleeds,
KashmirBanegaPakistan,
JihadKashmir,
SurgicalStrike, 
SayNoToWar, 
JeM, 
JaisheMohammad,
Jaish,
IndiaWantsRevenge, 
Gaddar, 
FreeKashmir, 
Fidayin, 
CrpfConvoyAttack, 
AzadKashmir, 
AJK, 
Balakot,
AdilahMaddar, 
LethopraSuicidalAttack, 
Abhinandan





Data statistics (counts) for tweets collected during and after Pulwama attack. The values in parentheses are network density values.

Statistic | Value | Statitic | Value
----------|-------|----------|------
Unique Users | 567K | Mentions |  725K (2.25*1e-6)
Total Tweets (Including Retweets) | 2.5M  | Reciprocal  |  36K (2.2*1e-7) 
Total Unique Hashtags  |  67K | Replies  |  43K (1.3*1e-7) 
Total Communication Links  |  2.3M (7.24*1e-6) | Retweets  |  1.6M (4.9*1e-6) 
Min. Tweets/User | 1 | Max. Tweets/User | 3166 
Avg. Tweets/User | 4.4 | SD Tweets/User | 13.2 



Table above reports statistics about the collected data, including the types of communication present. Twitter allows three types of interactive communication: mentions (e.g., $@username$), replies, and retweets. We classify retweets with comments as retweets. We also define reciprocal communication as two users mentioning each other, and all communication is the sum of the above three types of communication.
Furthermore, we construct networks for each type of communication, where users are nodes, and an edge exists between two nodes if those two users interacted with the specified type of communication. The Table reports both the frequency of each communication type in our data set and the densities of the constructed communication networks. Retweets occur more frequently and also result in higher network density than other forms of communication.


## Evaluation Analysis

**Sample inferred Pro-Aggression Hashtags**
stonehearted, pakistantakesrevenge, trustarmy, baaphaitumhare, barkhaspreadsporn, planprepare, pakistanamurdabad, indiaagainstantinationals, indianarmyourpridd, boycott\_pakistani\_players, yh\_aag\_na\_thandi\_hopaye, timestorevenge, ab\_hoga\_tanav, candleofrevenge, pulawamaislamicterrorattack, indiamusttakerevenge, avengeforpulwamaattack, russiawithmodi,boycottsnehawagh, iamwaitingindia


**Sample inferred Pro-Peace Hashtags** saynotoindopakmedia, savefamily, wekashmiridontwantwar, southasian, uniteasia, sayyestorobo, letstabletalk, saynotopakproxywar, saynotononsense, doyourjob, neverunderestimate, wecandobetter, wngcmdrabhinandan, stopmakingnonsensestatements, yestocricket, pleasenohate, flowersfrompakistan, peacepreaching, saynotocheapmedia, indianeedseducatedpm



India/Pakistan Confusion Matrix for the manual evaluation described in the paper.
  Label | True Pro-India | True Pro-Pakistan | True Neutral
---|--------------|---------------------|-----------
Predicted Pro-India | 45  | 1 | 3 
Predicted Pro-Pakistan | 10 | 24 | 0 
Predicted Neutral/Unclassified | 10 | 2 | 5 



Aggression/Peace War Confusion Matrix for the manual evaluation described in the paper.

Label | True Pro-Aggression | True Pro-Peace | True Neutral
------|---------------------|----------------|-------------
Predicted Pro-Aggression | 21 |  0 | 6
Predicted Pro-Peace | 24 | 31 | 10
Predicted Neutral/Unclassified | 2  | 1 | 5 


Tables above show the confusion matrices for the network-based hashtag propagation method over the manually annotated data set described in the paper. In the Pro-India/Pro-Pakistan dimension, classification accuracy is generally high with few misclassified examples. In the Pro-Aggression/Pro-Peace dimension, the most common error is predicting tweets that are actually Pro-Aggression as Pro-Peace. This error likely results because numerous Pro-Aggression tweets exhibited ``hashjacking'', in which users co-opted the hashtags preferred by adversaries. For example:

*``1993 Mumbai
1998 Coimbatore
2001 Parliament attack
2002 Akshardham
2003, 2006 Mumbai trains
2005 Delhi
2006 Varanasi
2007 Samjhauta + Hyderabad
2008 Mumbai 26/11
2016 Uri
2019 Pulwama
Hundreds more...
Did our Pak lovers say \#SayNoToWar then? Only applies when India strikes back?''*

*``While we were celebrating \#Abhinandan’s return, \#Pakistan continued to violate the ceasefire in J\&K. Two jawans were martyred and three civilians including a 5 year old and a nine month old were killed. And they talk about \#peace and \#PeaceGestures. Enough of this double speak!''*

As most of our analysis focuses on analyzing pro-aggression polarity, and we have no evidence that this type of hashjacking was more prevalent  for any given sub-group, we do not expect errors of this type to substantially change our findings. On the contrary, these types of errors suggest that our analysis is a conservative  estimate of the level of pro-aggression polarity.

Furthermore, of the 100 annotated data points, in the Pro-India/Pro-Pakistan dimension, none of them were unclassified. In the pro-Aggression/Pro-Peace dimension, 8 were unclassified. 5 of these were labelled as neutral or Can't determine by annotators, 2 were labeled pro-aggression, and 1 was labelled pro-peace. Thus, this evaluation supports our conclusion in the paper, that unclassified tweets primarily contain non-polarized language, and we have no reason to believe that our method fails to classify tweets of either polarity more often.





## Seed Hashtags
Seed hashtags used for the results reported in the paper:
Pro-India seeds: IndiaWantsRevenge, PhulwamaRevenge, ModiUnstoppable, AbhinandhanMyHero, RespectToIndianArmy, IndiaAgainstTerroristan, JusticeForPhulwamaAttack
Pro-Pakistan seeds: AzadKashmir, KashmirBanegaPakistan, PakistanZindabad,HindustaanMurdabaad, PakistanArmyGreatArmy, PakistanArmyZindabad, SaluteToOurPakistanArmy
Pro-Aggression seeds: SayYesToWar, 4kebadle400
Pro-Peace seeds: SayNoToWar, SaveHumanity


## Additional Data Analysis
Sample inferred pro-aggression tweets by BJP members: *````Pakistan will pay heavy price for \#Pulwama attack. Free hand given to our forces, Terrorists will pay a heavy price, It's time to unite for our nation." - PM Sri @narendramodi, I'am sure our retribution will make more noise than \#JihadiTerror \#CRPF \#KashmirTerrorAttack"* and *``\#IndiaWantsRevenge | We need to give a befitting reply to Pakistan, we will strike back. But people who support the separatists and maoists and even terrorists, the country does not need them"*

Network densities of different derived networks. All values are 1e-5.

Network Type | Pro-India  | Pro-Pakistan | Pro-Aggression  | Pro-Peace
-------------|-------------|--------------|----------------|----------
Retweet | 3.8 | 2.8 | 4.1 | 1.3
Mention | 5 | 3.4 | 4 | 1.6 
Reply | 0.14 | 0.11 | 0.13 | 0.062 
All Communication | 5 | 3.4 | 5.1 | 1.6




The number of Tweets and Retweets by different politicians is uploaded as tweet_volume.png




