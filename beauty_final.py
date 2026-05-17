import numpy as np
import random

# (c) Marco Lardelli 2026 (see https://lardel.li)

POPULATION_SIZE = 200  # the number of people
NO_OF_FEATURES = 10  # how many physical features shall we consider?
NO_OF_EPISODES = 1000  # how many times to repeat
EPSILON = 0.05  # update rate of desired_features (should be rather small)



# Initialization of population
population = []
for i in range(POPULATION_SIZE):
    # initialize each persons physical features randomly
    features = np.random.randn(NO_OF_FEATURES)  # from normal distribution
    # humans cannot be infintely extreme -> limit range of feature values
    features = np.clip(features, -1.5, 1.5)

    # now similarly for the desired features
    desired_features = np.random.randn(NO_OF_FEATURES)
    desired_features = np.clip(desired_features, -1.5, 1.5) # humans cannot be infintely extreme

    population.append({
        'id': i,
        'sex': 'F' if random.random()<0.5 else 'M', # men / women 50:50
        'features': features, 
        'personality': np.linalg.norm(features),
        'desired_features': desired_features,
        'avg_desired': 0.0, # how much do people desire this person on average (i.e. attractiveness)
        'n_desirers': 0 # number of people who have already expressed their desire (only required to simplify the update of avg_desired!)
    })


# the simulation loop
avg_avg_desired = 0.0  # average attractiveness in the population
for e in range(NO_OF_EPISODES):
    for person in population:
        while True: # repeat until we have found a suitable match for the person
            # choose a random target
            target = random.choice(population)
            if person['sex'] != target['sex'] and person['id'] != target['id']: # one can not rate oneself!
                # 1. Calculate how attractive the person finds the target
                # how far apart are the person's desired_features and the target's features?
                distance = np.linalg.norm(target['features']-person['desired_features'])
                if distance == 0:  # this is rare but makes big trouble!
                    break  # we leave it!
                # the smaller the distance, the more the person desires the target
                desire = 10/distance  # desire can be small, but is always positive (the 10 is there because desire is measured in the international unit "Kardashian" (symbol "Ka", with "Impact"-font))

                # 2. Update the desired_features of the person in the direction of the target's features
                direction = target['features'] - person['desired_features']
                distance = np.linalg.norm(direction)
                # normalize the direction to unit length (i.e. 1)
                direction = direction / distance
                # fashion variable: how much larger is the attractiveness of the target compared to the average?
                fashion = (target['avg_desired'] - avg_avg_desired)
                if fashion>0:
                    # update the desired_features of the person proportionally to the fashion variable towards the features of the target
                    fashion = min(fashion, 0.1 * distance/EPSILON)  # limit to avoid overshooting! (just to be safe here)
                    person['desired_features'] += EPSILON * fashion * direction

                # 3. Update of avg_desired of the target with the desire of the person
                # (this must be done after 2. so this rating does not influence 2.)
                n = target['n_desirers']
                target['avg_desired'] = (n * target['avg_desired'] + desire) / (n + 1)
                target['n_desirers'] += 1

                break

    # calculate the new average attractiveness (average of avg_desired) in the whole population
    # for reasons of efficiency, we do this only once every episode
    avg_avg_desired = np.mean( np.array( [p['avg_desired'] for p in population] ) , axis=0)
   


sorted_population = sorted(population, key=lambda d: d["avg_desired"], reverse=True)

print("\nMost / least attractive:")

# top 10 most attractive
for i,p in enumerate(sorted_population[0:5]):
    print("Attractiveness=",p['avg_desired'],"Personality=",p['personality'])

print('...')

# 10 least attractive
for i,p in enumerate(sorted_population[-5:]):
    print("Attractiveness=",p['avg_desired'],"Personality=",p['personality'])



    