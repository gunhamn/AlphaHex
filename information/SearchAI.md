# Search in AI notes

- Backpropogation is a semi-intelligent local search, not connected to domain knowledge, but connected to knowledge about the neural network itself 

## Reinforcement learning

- Interested in the sequence as well as the goal state
- The sequence is implicitly encoded in a policy: mapping: state -> action 
- Often combined with a value function mapping: state -> evaluation, where evaluation = total expected reward from the state to a goal state 
- RL search = combination of exploration and exploitation: intelligent trial and error 
- Modify the value function and policy in parallel 
- Model = mapping: (state, action) -> state 
- Dynamic programming (know models beforehand) goes backward 
- Model-free: the mapping is learned by exploration of state space 
- Bootstrapping: evaluations of states are updated based on the evaluations of their child, grandchild, etc. States 
- Neural net = a function approximator (funcapp) from states to evaluations (critic) or states to actions (actor) 

### GO

- No heuristic is good enough
- Monte carlo simulations for training cases for a neural network, so that the neural network will evaluate (pick action) the node (state) 
- Rollout is basically depth-first search but with a policy, propogate all the values up to the node? 
- State and value in each node 
- When feeding a state into a neural network, we typically transform it into a more syntactic representation 