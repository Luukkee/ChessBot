# Chess Engine & Chess Game

This is a personal project where I created the game of chess and a machine learning model designed to play it, with a target performance goal of approximately 2000 Elo (Currently at ~1700 - 1800). Unlike many traditional chess engines that rely on complex search algorithms such as Monte-Carlo Tree Search (MCTS) or alpha-beta pruning, this engine takes a unique approach: it operates **completely searchless**.

### Key Concept

The philosophy behind this engine can be likened to the words of **José Raúl Capablanca**, a chess world champion known for his deep intuition:

> "I see only one move ahead, but it is always the correct one."

Instead of evaluating potential outcomes through deep searches and simulations, the engine relies purely on its ability to predict the best move directly from the current board state, focusing on pattern recognition and experience learned from its training data.

### Model Architecture

The model architecture is a **CNN-Transformer hybrid**, augmented with **residual connections**. The **CNN (Convolutional Neural Network)** is used to extract spatial features from the chess board state, identifying piece patterns and configurations. The **Transformer** part of the model takes these extracted features and makes predictions based on them, leveraging its ability to model long-term dependencies and relational data. The **residual connections** help the model retain and combine useful information across multiple layers, enhancing its ability to learn complex board patterns.

This combination is particularly effective in chess because it allows the model to recognize intricate board patterns and predict moves that align with strategic goals.

- **CNN**: Captures local board features and piece interactions, such as tactical combinations and immediate threats.
- **Transformer**: Builds on the CNN's output to understand more complex, long-term strategies and positional patterns across the entire board.
- **Residuals**: Helps the model maintain important feature information across layers, improving training and prediction accuracy.

The model has been trained on **3 million elite-level games** from **Lichess**, using data from [this dataset](https://database.nikonoel.fr/), giving it access to high-quality, human-driven decision-making data. This helps the engine understand both tactical and strategic aspects of the game.

### Features

- **Searchless Engine**: No tree search or brute-force algorithms. The engine makes predictions based on learned patterns and board evaluations alone.
- **Machine Learning Model**: The core model is built to evaluate the board and select moves in real time, similar to how a human player might analyze positions and make decisions.
- **Chess Game Implementation**: A fully functional chess game has been implemented using **Pygame**, integrated with the machine learning model for an interactive experience.
- **Version 1.0**: The current version (V1.0) of the engine has shown promising results, performing well against other engines and providing a challenging game experience for human players.

### How It Works

The chess engine processes each board state as an input and outputs the move it believes to be the best, based entirely on the model's prediction. The core machine learning model has been trained on thousands of chess games, learning to evaluate positions and make decisions without the need for lookahead search.

This creates a unique challenge for the engine, as it must rely solely on its training and intuition, unlike most engines that calculate deeply into future moves. The trade-off is an engine that can make lightning-fast decisions, ideal for blitz games or real-time applications.

### Future Plans

- **Improving Model Performance**: Continue refining the model's architecture and training process to push its performance closer to the target Elo of 2000.
- **Version 2.0**: The next version will incorporate new training data and potentially a deeper model architecture to improve positional understanding and long-term planning. It might even take advantage of Reinforcement Learning.
- **Web Integration**: The engine will soon be available to play online, with a web interface where users can challenge the bot in real time. 
